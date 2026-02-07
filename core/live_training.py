"""
Live Neural Network Training for Interactive Visualizations.

Provides real training that can be controlled, paused, and visualized.
Uses NumPy for simplicity (no PyTorch/TensorFlow dependency).

Optimized for smooth UI updates:
- Decision boundary computed only every N epochs
- Thread-safe callbacks via queue
- Batch training option for responsiveness
"""

import numpy as np
import threading
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Any
from queue import Queue, Empty

from core.training import TrainingState, TrainingSession


@dataclass
class NetworkConfig:
    """Configuration for a neural network."""
    layer_sizes: List[int] = field(default_factory=lambda: [2, 4, 1])
    activation: str = 'sigmoid'  # 'sigmoid', 'tanh', 'relu'
    learning_rate: float = 0.5
    momentum: float = 0.0
    weight_decay: float = 0.0
    dropout_rate: float = 0.0


class NeuralNetwork:
    """
    Simple feedforward neural network with backpropagation.
    Optimized for XOR-style problems with smooth visualization.
    """

    def __init__(self, config: NetworkConfig):
        self.config = config
        self.layers = config.layer_sizes

        # Initialize weights with Xavier initialization
        self.weights = []
        self.biases = []
        for i in range(len(self.layers) - 1):
            # Xavier initialization for better convergence
            scale = np.sqrt(2.0 / (self.layers[i] + self.layers[i+1]))
            w = np.random.randn(self.layers[i], self.layers[i+1]) * scale
            b = np.zeros((1, self.layers[i+1]))
            self.weights.append(w)
            self.biases.append(b)

        # Momentum velocities
        self.velocity_w = [np.zeros_like(w) for w in self.weights]
        self.velocity_b = [np.zeros_like(b) for b in self.biases]

        # Store activations for visualization
        self.activations = []
        self.gradients = []

    def _activate(self, x: np.ndarray) -> np.ndarray:
        """Apply activation function."""
        if self.config.activation == 'sigmoid':
            return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
        elif self.config.activation == 'tanh':
            return np.tanh(x)
        elif self.config.activation == 'relu':
            return np.maximum(0, x)
        return x

    def _activate_derivative(self, activated: np.ndarray) -> np.ndarray:
        """Derivative of activation function."""
        if self.config.activation == 'sigmoid':
            return activated * (1 - activated)
        elif self.config.activation == 'tanh':
            return 1 - activated ** 2
        elif self.config.activation == 'relu':
            return (activated > 0).astype(float)
        return np.ones_like(activated)

    def forward(self, X: np.ndarray) -> np.ndarray:
        """Forward pass, storing activations."""
        self.activations = [X]
        current = X

        for i, (w, b) in enumerate(zip(self.weights, self.biases)):
            z = current @ w + b
            # Use sigmoid for output layer, configured activation for hidden
            if i == len(self.weights) - 1:
                current = 1 / (1 + np.exp(-np.clip(z, -500, 500)))  # Sigmoid output
            else:
                current = self._activate(z)
            self.activations.append(current)

        return current

    def backward(self, X: np.ndarray, y: np.ndarray) -> float:
        """Backward pass with gradient descent."""
        m = X.shape[0]
        output = self.forward(X)

        # Compute loss
        loss = np.mean((y - output) ** 2)

        # Backpropagation
        self.gradients = []
        delta = (output - y) * output * (1 - output)  # Sigmoid derivative for output

        for i in reversed(range(len(self.weights))):
            # Gradient for weights
            grad_w = self.activations[i].T @ delta / m
            grad_b = np.mean(delta, axis=0, keepdims=True)

            # Store gradient magnitude for visualization
            self.gradients.insert(0, np.mean(np.abs(grad_w)))

            # Weight decay
            if self.config.weight_decay > 0:
                grad_w += self.config.weight_decay * self.weights[i]

            # Momentum update
            if self.config.momentum > 0:
                self.velocity_w[i] = self.config.momentum * self.velocity_w[i] - self.config.learning_rate * grad_w
                self.velocity_b[i] = self.config.momentum * self.velocity_b[i] - self.config.learning_rate * grad_b
                self.weights[i] += self.velocity_w[i]
                self.biases[i] += self.velocity_b[i]
            else:
                self.weights[i] -= self.config.learning_rate * grad_w
                self.biases[i] -= self.config.learning_rate * grad_b

            # Propagate delta
            if i > 0:
                delta = (delta @ self.weights[i].T) * self._activate_derivative(self.activations[i])

        return loss

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions."""
        return self.forward(X)

    def compute_decision_boundary(self, resolution: int = 30) -> np.ndarray:
        """
        Compute decision boundary over a grid.
        Lower resolution = faster computation.
        """
        x_range = np.linspace(-0.2, 1.2, resolution)
        y_range = np.linspace(-0.2, 1.2, resolution)

        boundary = np.zeros((resolution, resolution))
        for i, x in enumerate(x_range):
            for j, y in enumerate(y_range):
                pred = self.forward(np.array([[x, y]]))[0, 0]
                boundary[i, j] = pred

        return boundary

    def get_weights_dict(self) -> Dict[str, np.ndarray]:
        """Get weights as dictionary."""
        return {f'layer_{i}': w.copy() for i, w in enumerate(self.weights)}

    def get_gradients_dict(self) -> Dict[str, float]:
        """Get gradient magnitudes."""
        return {f'layer_{i}': g for i, g in enumerate(self.gradients)}


class LiveTrainer:
    """
    Live training controller that runs in a background thread.

    Optimized for smooth UI:
    - Uses a state queue for thread-safe updates
    - Only computes decision boundary every N epochs
    - Supports batch training for responsive stepping
    """

    def __init__(self, network: NeuralNetwork, X: np.ndarray, y: np.ndarray):
        self.network = network
        self.X = X
        self.y = y

        self.epoch = 0
        self.total_epochs = 1000
        self.loss_history = []
        self.accuracy_history = []

        self.session = TrainingSession('live_training')

        # Threading
        self._thread: Optional[threading.Thread] = None
        self._stop_requested = False
        self._lock = threading.Lock()
        self.is_running = False
        self.is_paused = False

        # State queue for thread-safe UI updates
        self._state_queue: Queue = Queue(maxsize=10)

        # Optimization settings
        self.boundary_update_interval = 10  # Only compute boundary every N epochs
        self._last_boundary: Optional[np.ndarray] = None

    def set_hyperparameters(self, **kwargs):
        """Update hyperparameters during training."""
        with self._lock:
            if 'learning_rate' in kwargs:
                self.network.config.learning_rate = kwargs['learning_rate']
            if 'momentum' in kwargs:
                self.network.config.momentum = kwargs['momentum']
            if 'dropout_rate' in kwargs:
                self.network.config.dropout_rate = kwargs['dropout_rate']

    def _create_state(self, compute_boundary: bool = False) -> TrainingState:
        """Create a training state snapshot."""
        predictions = (self.network.predict(self.X) > 0.5).astype(float)
        accuracy = np.mean(predictions == self.y)

        # Only compute boundary when requested
        if compute_boundary:
            self._last_boundary = self.network.compute_decision_boundary(resolution=25)

        return TrainingState(
            epoch=self.epoch,
            total_epochs=self.total_epochs,
            loss=self.loss_history[-1] if self.loss_history else 1.0,
            loss_history=self.loss_history.copy(),
            metrics={'accuracy': accuracy},
            metrics_history={'accuracy': self.accuracy_history.copy()},
            weights=self.network.get_weights_dict(),
            gradients=self.network.get_gradients_dict(),
            hyperparameters={
                'learning_rate': self.network.config.learning_rate,
                'dropout_rate': self.network.config.dropout_rate,
                'momentum': self.network.config.momentum,
            },
            decision_boundary=self._last_boundary,
            predictions=predictions,
        )

    def train_batch(self, num_epochs: int = 10) -> Optional[TrainingState]:
        """
        Train for a batch of epochs synchronously.
        Good for step-by-step training like the original presentation.
        """
        with self._lock:
            for _ in range(num_epochs):
                if self.epoch >= self.total_epochs:
                    break

                loss = self.network.backward(self.X, self.y)
                predictions = (self.network.predict(self.X) > 0.5).astype(float)
                accuracy = np.mean(predictions == self.y)

                self.loss_history.append(loss)
                self.accuracy_history.append(accuracy)
                self.epoch += 1

            # Compute boundary after batch
            state = self._create_state(compute_boundary=True)
            self.session.add_state(state)
            return state

    def start(self, epochs: int = 1000, epochs_per_second: float = 30):
        """Start continuous background training."""
        if self.is_running:
            return

        self.total_epochs = epochs
        self._stop_requested = False
        self.is_running = True
        self.is_paused = False

        epoch_interval = 1.0 / epochs_per_second

        def train_loop():
            while self.epoch < self.total_epochs and not self._stop_requested:
                if self.is_paused:
                    time.sleep(0.05)
                    continue

                start_time = time.time()

                with self._lock:
                    loss = self.network.backward(self.X, self.y)
                    predictions = (self.network.predict(self.X) > 0.5).astype(float)
                    accuracy = np.mean(predictions == self.y)

                    self.loss_history.append(loss)
                    self.accuracy_history.append(accuracy)
                    self.epoch += 1

                    # Only compute boundary periodically
                    compute_boundary = (self.epoch % self.boundary_update_interval == 0)
                    state = self._create_state(compute_boundary=compute_boundary)
                    self.session.add_state(state)

                    # Queue state for UI (drop old states if queue full)
                    try:
                        self._state_queue.put_nowait(state)
                    except:
                        try:
                            self._state_queue.get_nowait()
                            self._state_queue.put_nowait(state)
                        except:
                            pass

                # Maintain training speed
                elapsed = time.time() - start_time
                if elapsed < epoch_interval:
                    time.sleep(epoch_interval - elapsed)

            self.is_running = False

        self._thread = threading.Thread(target=train_loop, daemon=True)
        self._thread.start()

    def get_latest_state(self) -> Optional[TrainingState]:
        """Get latest state from queue (non-blocking, thread-safe)."""
        state = None
        try:
            # Drain queue, keep only latest
            while True:
                state = self._state_queue.get_nowait()
        except Empty:
            pass
        return state

    def pause(self):
        """Pause training."""
        self.is_paused = True

    def resume(self):
        """Resume training."""
        self.is_paused = False

    def stop(self):
        """Stop training completely."""
        self._stop_requested = True
        if self._thread:
            self._thread.join(timeout=1.0)
        self.is_running = False

    def reset(self):
        """Reset training to beginning."""
        self.stop()
        self.epoch = 0
        self.loss_history = []
        self.accuracy_history = []
        self._last_boundary = None

        # Reinitialize network
        self.network = NeuralNetwork(self.network.config)
        self.session = TrainingSession('live_training')

        # Clear queue
        while not self._state_queue.empty():
            try:
                self._state_queue.get_nowait()
            except:
                break

    def step(self, num_epochs: int = 1) -> Optional[TrainingState]:
        """Perform training steps (alias for train_batch with 1 epoch)."""
        return self.train_batch(num_epochs)

    def get_current_state(self) -> Optional[TrainingState]:
        """Get the current training state."""
        if self.session.states:
            return self.session.states[-1]
        return None


def create_xor_trainer(hidden_size: int = 4, learning_rate: float = 0.5) -> LiveTrainer:
    """
    Create a trainer for the XOR problem.

    Uses simpler architecture like the original presentation:
    2 inputs -> hidden -> 1 output
    """
    # XOR dataset
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    y = np.array([[0], [1], [1], [0]], dtype=float)

    # Simple network: 2 -> hidden -> 1 (like original 2->3->1)
    config = NetworkConfig(
        layer_sizes=[2, hidden_size, 1],
        activation='sigmoid',  # Use sigmoid like original
        learning_rate=learning_rate,
        momentum=0.9,
    )

    network = NeuralNetwork(config)
    return LiveTrainer(network, X, y)


def create_custom_trainer(X: np.ndarray, y: np.ndarray,
                          layer_sizes: List[int],
                          learning_rate: float = 0.01) -> LiveTrainer:
    """Create a trainer with custom data and architecture."""
    config = NetworkConfig(
        layer_sizes=layer_sizes,
        activation='tanh',
        learning_rate=learning_rate,
        momentum=0.9,
    )

    network = NeuralNetwork(config)
    return LiveTrainer(network, X, y)
