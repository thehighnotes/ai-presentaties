"""
XOR Neural Network Training Visualization
Interactive presentation showing how neural networks learn

EXACT match to original Neural Network.py with standardized controls
Architecture: 2 inputs → 3 hidden → 1 output

Controls:
- SPACE: Train 10 epochs
- B: Previous view
- Q: Quit
- S: Return to presentation selection
- T: Train 100 epochs
- N: Next view
- P: Previous view
- R: Reset network
- F: Toggle fullscreen
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import PresentationStyle


class XORNeuralNetwork:
    """Simple XOR Neural Network for visualization - EXACT ORIGINAL"""

    def __init__(self):
        # Network architecture: 2 inputs, 3 hidden, 1 output (ORIGINAL)
        np.random.seed(42)
        self.weights_input_hidden = np.random.randn(2, 3) * 0.5
        self.bias_hidden = np.random.randn(3) * 0.5
        self.weights_hidden_output = np.random.randn(3, 1) * 0.5
        self.bias_output = np.random.randn(1) * 0.5

        # Training data
        self.X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        self.y = np.array([[0], [1], [1], [0]])

        # Training history
        self.loss_history = []
        self.epoch = 0
        self.learning_rate = 0.5

        # For visualization
        self.last_hidden = None
        self.last_output = None

    def sigmoid(self, x):
        """Sigmoid activation function"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def sigmoid_derivative(self, x):
        """Derivative of sigmoid"""
        return x * (1 - x)

    def forward(self, X):
        """Forward pass"""
        # Hidden layer
        hidden_input = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        hidden_output = self.sigmoid(hidden_input)

        # Output layer
        output_input = np.dot(hidden_output, self.weights_hidden_output) + self.bias_output
        output = self.sigmoid(output_input)

        self.last_hidden = hidden_output
        self.last_output = output

        return hidden_output, output

    def backward(self, X, y, hidden_output, output):
        """Backward pass (backpropagation)"""
        # Output layer error
        output_error = y - output
        output_delta = output_error * self.sigmoid_derivative(output)

        # Hidden layer error
        hidden_error = output_delta.dot(self.weights_hidden_output.T)
        hidden_delta = hidden_error * self.sigmoid_derivative(hidden_output)

        # Update weights
        self.weights_hidden_output += hidden_output.T.dot(output_delta) * self.learning_rate
        self.bias_output += np.sum(output_delta, axis=0) * self.learning_rate
        self.weights_input_hidden += X.T.dot(hidden_delta) * self.learning_rate
        self.bias_hidden += np.sum(hidden_delta, axis=0) * self.learning_rate

    def train_epoch(self):
        """Train for one epoch"""
        hidden_output, output = self.forward(self.X)
        self.backward(self.X, self.y, hidden_output, output)

        # Calculate loss
        loss = np.mean((self.y - output) ** 2)
        self.loss_history.append(loss)
        self.epoch += 1

        return loss

    def predict(self, X):
        """Make prediction"""
        _, output = self.forward(X)
        return output


class NeuralNetworkPresentation:
    """
    EXACT match to original XORPresentation with standardized controls
    """
    def __init__(self):
        # Use dark mode styling
        PresentationStyle.apply_dark_mode()
        self.fig = plt.figure(figsize=(16, 9), facecolor=PresentationStyle.COLORS['bg'])

        self.nn = XORNeuralNetwork()
        self.view_mode = 0  # 0: network, 1: decision boundary, 2: loss curve, 3: combined
        self.view_names = ['Network Architecture', 'Decision Boundary', 'Training Loss', 'Combined View']

        # Use dark mode colors
        self.colors = {
            'neuron': PresentationStyle.COLORS['neuron'],
            'active': PresentationStyle.COLORS['secondary'],
            'inactive': PresentationStyle.COLORS['dim'],
            'correct': PresentationStyle.COLORS['correct'],
            'wrong': PresentationStyle.COLORS['wrong'],
            'connection': PresentationStyle.COLORS['connection']
        }

        # Current input being visualized (cycles through XOR inputs)
        self.current_input_idx = 0

        self.setup_view()
        self.setup_controls()

    def setup_controls(self):
        """Setup keyboard controls - STANDARDIZED + ORIGINAL"""
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def on_key_press(self, event):
        """Handle keyboard press events - STANDARDIZED CONTROLS"""
        if event.key == ' ':  # STANDARD: Space - train
            self.train_step()
        elif event.key == 'b':  # STANDARD: B - previous view
            self.view_mode = (self.view_mode - 1) % len(self.view_names)
            self.setup_view()
        elif event.key in ['q', 'escape']:  # STANDARD: Q - quit
            plt.close()
        elif event.key == 's':  # STANDARD: S - selection menu
            plt.close()
            # Main controller will handle this
        # ORIGINAL CONTROLS (kept for compatibility)
        elif event.key == 'r':  # Reset
            self.reset_network()
        elif event.key == 'n':  # Next view
            self.view_mode = (self.view_mode + 1) % len(self.view_names)
            self.setup_view()
        elif event.key == 'p':  # Previous view (same as B)
            self.view_mode = (self.view_mode - 1) % len(self.view_names)
            self.setup_view()
        elif event.key == 't':  # Train 100 epochs (extra training)
            for _ in range(10):
                self.train_step()
        elif event.key == 'f':  # Fullscreen
            manager = plt.get_current_fig_manager()
            try:
                manager.full_screen_toggle()
            except:
                pass
        elif event.key == 'c':  # Cycle through inputs
            self.current_input_idx = (self.current_input_idx + 1) % len(self.nn.X)
            self.setup_view()
            print(f"Showing input: {self.nn.X[self.current_input_idx]} -> {self.nn.y[self.current_input_idx][0]}")

    def setup_view(self):
        """Setup current view - EXACT ORIGINAL"""
        self.fig.clear()

        if self.view_mode == 0:
            self.draw_network()
        elif self.view_mode == 1:
            self.draw_decision_boundary()
        elif self.view_mode == 2:
            self.draw_loss_curve()
        elif self.view_mode == 3:
            self.draw_combined()

        plt.tight_layout()
        plt.draw()

    def draw_network(self):
        """Draw neural network architecture - EXACT ORIGINAL WITH ALL ELEMENTS"""
        ax = self.fig.add_subplot(111, facecolor=PresentationStyle.COLORS['bg'])
        ax.set_xlim(-1, 11)
        ax.set_ylim(-1, 6)
        ax.axis('off')

        # Layer positions - ORIGINAL (3 hidden neurons!)
        input_x, hidden_x, output_x = 1, 5, 9
        input_y = [1.5, 3.5]
        hidden_y = [0.5, 2.5, 4.5]  # 3 HIDDEN NEURONS
        output_y = [2.5]

        # Get current input for visualization
        current_x = self.nn.X[self.current_input_idx]
        current_y = self.nn.y[self.current_input_idx]
        _, _ = self.nn.forward(current_x.reshape(1, -1))

        # Draw connections with weights - IMPROVED READABILITY
        for i, iy in enumerate(input_y):
            for j, hy in enumerate(hidden_y):
                weight = self.nn.weights_input_hidden[i, j]
                color = self.colors['active'] if weight > 0 else self.colors['inactive']
                alpha = min(abs(weight) * 0.7, 0.9)
                ax.plot([input_x, hidden_x], [iy, hy], color=color,
                       linewidth=3, alpha=alpha, zorder=1)
                # Weight value - READABLE ON TV
                mid_x, mid_y = (input_x + hidden_x) / 2, (iy + hy) / 2
                ax.text(mid_x, mid_y, f'{weight:.1f}', fontsize=21, fontweight='bold',
                       ha='center', va='center',
                       bbox=dict(boxstyle='round,pad=0.5',
                                facecolor=PresentationStyle.COLORS['bg_light'],
                                edgecolor=color, linewidth=2, alpha=0.95),
                       color=PresentationStyle.COLORS['text'])

        for i, hy in enumerate(hidden_y):
            weight = self.nn.weights_hidden_output[i, 0]
            color = self.colors['active'] if weight > 0 else self.colors['inactive']
            alpha = min(abs(weight) * 0.7, 0.9)
            ax.plot([hidden_x, output_x], [hy, output_y[0]], color=color,
                   linewidth=3, alpha=alpha, zorder=1)
            # Weight value - READABLE ON TV
            mid_x, mid_y = (hidden_x + output_x) / 2, (hy + output_y[0]) / 2
            ax.text(mid_x, mid_y, f'{weight:.1f}', fontsize=21, fontweight='bold',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.5',
                            facecolor=PresentationStyle.COLORS['bg_light'],
                            edgecolor=color, linewidth=2, alpha=0.95),
                   color=PresentationStyle.COLORS['text'])

        # Draw neurons
        neuron_size = 0.5  # Slightly larger for TV readability

        # Input layer - SHOW ACTUAL INPUT VALUES
        for i, y in enumerate(input_y):
            input_value = current_x[i]
            # Use bright color for active inputs
            neuron_color = self.colors['active'] if input_value > 0.5 else PresentationStyle.COLORS['bg_light']
            circle = Circle((input_x, y), neuron_size, color=neuron_color,
                          ec='white', linewidth=4, zorder=3)
            ax.add_patch(circle)
            # Show actual value
            ax.text(input_x, y, f'{input_value:.0f}', ha='center', va='center',
                   fontweight='bold', fontsize=27, color='white',
                   bbox=dict(boxstyle='circle,pad=0.3', facecolor='black',
                            edgecolor='none', alpha=0.7))
            ax.text(input_x - 0.9, y, f'Input {i}', ha='right', va='center',
                   fontsize=24, fontweight='bold', color=PresentationStyle.COLORS['text'])

        # Hidden layer - READABLE ACTIVATION VALUES
        for i, y in enumerate(hidden_y):
            activation = 0
            if self.nn.last_hidden is not None:
                activation = self.nn.last_hidden[0, i]
            # Semi-transparent colored background
            color = plt.cm.RdYlGn(activation)
            circle = Circle((hidden_x, y), neuron_size, color=color,
                          ec='white', linewidth=4, alpha=0.8, zorder=3)
            ax.add_patch(circle)
            # Show activation value with readable contrast
            ax.text(hidden_x, y, f'{activation:.2f}', ha='center', va='center',
                   fontweight='bold', fontsize=21, color='white',
                   bbox=dict(boxstyle='circle,pad=0.3', facecolor='black',
                            edgecolor='none', alpha=0.7))
            # Label
            ax.text(hidden_x, y - 0.8, f'H{i}', ha='center',
                   va='top', fontsize=21, fontweight='bold',
                   color=PresentationStyle.COLORS['text'])

        # Output layer - READABLE OUTPUT VALUE
        activation = 0
        if self.nn.last_output is not None:
            activation = self.nn.last_output[0, 0]
        color = plt.cm.RdYlGn(activation)
        circle = Circle((output_x, output_y[0]), neuron_size, color=color,
                      ec='white', linewidth=4, alpha=0.8, zorder=3)
        ax.add_patch(circle)
        # Show output value with readable contrast
        ax.text(output_x, output_y[0], f'{activation:.2f}', ha='center', va='center',
               fontweight='bold', fontsize=21, color='white',
               bbox=dict(boxstyle='circle,pad=0.3', facecolor='black',
                        edgecolor='none', alpha=0.7))
        ax.text(output_x + 0.9, output_y[0], 'Output', ha='left', va='center',
               fontsize=24, fontweight='bold', color=PresentationStyle.COLORS['text'])
        # Show expected value
        ax.text(output_x, output_y[0] - 0.8, f'Target: {current_y[0]:.0f}', ha='center',
               va='top', fontsize=21, fontweight='bold',
               color=self.colors['correct' if abs(activation - current_y[0]) < 0.3 else 'wrong'])

        # Layer labels
        ax.text(input_x, 5.5, 'Input Layer', ha='center', fontsize=27, fontweight='bold',
               color=PresentationStyle.COLORS['text'])
        ax.text(hidden_x, 5.5, 'Hidden Layer', ha='center', fontsize=27, fontweight='bold',
               color=PresentationStyle.COLORS['text'])
        ax.text(output_x, 5.5, 'Output Layer', ha='center', fontsize=27, fontweight='bold',
               color=PresentationStyle.COLORS['text'])

        # Training info with current input
        loss_text = f"{self.nn.loss_history[-1]:.4f}" if self.nn.loss_history else "N/A"
        input_text = f"{int(current_x[0])} ⊕ {int(current_x[1])} = {current_y[0]:.0f}"
        info_text = f"Epoch: {self.nn.epoch} | Loss: {loss_text} | Showing: {input_text}"
        self.fig.text(0.5, 0.95, info_text, ha='center', fontsize=36, fontweight='bold',
                     color=PresentationStyle.COLORS['text'],
                     bbox=dict(boxstyle='round,pad=0.8', facecolor=PresentationStyle.COLORS['bg_light'],
                             edgecolor=self.colors['active'], linewidth=3))

        # XOR Truth table - ORIGINAL FEATURE
        truth_table = "XOR Truth Table:\n"
        truth_table += "0⊕0=0  0⊕1=1\n"
        truth_table += "1⊕0=1  1⊕1=0"
        self.fig.text(0.02, 0.98, truth_table, ha='left', va='top', fontsize=24,
                     family='monospace', color=PresentationStyle.COLORS['text'],
                     bbox=dict(boxstyle='round,pad=0.6', facecolor=PresentationStyle.COLORS['bg_light'],
                              edgecolor=PresentationStyle.COLORS['accent'], linewidth=2, alpha=0.9))

        # Current predictions - ORIGINAL FEATURE
        if self.nn.last_output is not None:
            pred_text = "Current Predictions:\n"
            for i, (x, y_true) in enumerate(zip(self.nn.X, self.nn.y)):
                _, pred = self.nn.forward(x.reshape(1, -1))
                pred_val = pred[0, 0]
                correct = '[OK]' if abs(pred_val - y_true[0]) < 0.3 else '[X]'
                pred_text += f"{int(x[0])}⊕{int(x[1])}={y_true[0]:.0f} → {pred_val:.3f} {correct}\n"

            self.fig.text(0.98, 0.98, pred_text, ha='right', va='top', fontsize=24,
                         family='monospace', color=PresentationStyle.COLORS['text'],
                         bbox=dict(boxstyle='round,pad=0.6', facecolor=PresentationStyle.COLORS['bg_light'],
                                  edgecolor=PresentationStyle.COLORS['secondary'], linewidth=2, alpha=0.9))

        # Instructions - UPDATED WITH STANDARD CONTROLS
        instructions = "SPACE: Train 10 epochs | C: Cycle Input | B/N: Change View | T: Train 100 | R: Reset | Q: Quit"
        self.fig.text(0.5, 0.02, instructions, ha='center', fontsize=21, style='italic',
                     alpha=0.7, color=PresentationStyle.COLORS['dim'], fontweight='bold')

        # View name
        self.fig.text(0.5, 0.88, self.view_names[self.view_mode], ha='center',
                     fontsize=30, color=PresentationStyle.COLORS['dim'], style='italic')

        # Weight explanation box - ADDED FOR CLARITY
        weight_explanation = "[WEIGHTS UITLEG]\n"
        weight_explanation += "• Gewicht = Sterkte verbinding\n"
        weight_explanation += "• Positief (groen) = Versterkt signaal\n"
        weight_explanation += "• Negatief (grijs) = Verzwakt signaal\n"
        weight_explanation += "• Getal op lijn = Gewicht waarde"
        self.fig.text(0.5, 0.12, weight_explanation, ha='center', va='center',
                     fontsize=19, family='monospace',
                     color=PresentationStyle.COLORS['text'],
                     bbox=dict(boxstyle='round,pad=0.8',
                             facecolor=PresentationStyle.COLORS['bg_light'],
                             edgecolor=PresentationStyle.COLORS['purple'],
                             linewidth=3, alpha=0.95))

    def draw_decision_boundary(self):
        """Draw decision boundary visualization - EXACT ORIGINAL"""
        ax = self.fig.add_subplot(111, facecolor=PresentationStyle.COLORS['bg'])

        # Create mesh
        h = 0.02
        x_min, x_max = -0.5, 1.5
        y_min, y_max = -0.5, 1.5
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                            np.arange(y_min, y_max, h))

        # Make predictions
        mesh_input = np.c_[xx.ravel(), yy.ravel()]
        Z = self.nn.predict(mesh_input)
        Z = Z.reshape(xx.shape)

        # Plot decision boundary
        contour = ax.contourf(xx, yy, Z, levels=20, cmap='RdYlGn', alpha=0.6)
        ax.contour(xx, yy, Z, levels=[0.5], colors=PresentationStyle.COLORS['text'], linewidths=3)

        # Plot training points
        for i, (x, y) in enumerate(zip(self.nn.X, self.nn.y)):
            color = self.colors['correct'] if y[0] == 1 else self.colors['wrong']
            ax.scatter(x[0], x[1], s=500, c=color, edgecolors='white',
                      linewidths=3, zorder=5)
            ax.text(x[0], x[1], f'{int(x[0])}⊕{int(x[1])}\n={int(y[0])}',
                   ha='center', va='center', fontsize=24, fontweight='bold', color='white')

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_xlabel('Input 0', fontsize=27, fontweight='bold', color=PresentationStyle.COLORS['text'])
        ax.set_ylabel('Input 1', fontsize=27, fontweight='bold', color=PresentationStyle.COLORS['text'])
        ax.grid(True, alpha=0.3, color=PresentationStyle.COLORS['dim'])
        ax.set_aspect('equal')
        ax.tick_params(colors=PresentationStyle.COLORS['text'])

        # Colorbar
        cbar = plt.colorbar(contour, ax=ax)
        cbar.set_label('Network Output', fontsize=24, fontweight='bold', color=PresentationStyle.COLORS['text'])
        cbar.ax.yaxis.set_tick_params(color=PresentationStyle.COLORS['text'])
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color=PresentationStyle.COLORS['text'])

        # Training info
        info_text = f"Epoch: {self.nn.epoch} | Loss: {self.nn.loss_history[-1]:.4f}" if self.nn.loss_history else f"Epoch: {self.nn.epoch} | Loss: N/A"
        self.fig.text(0.5, 0.95, info_text, ha='center', fontsize=36, fontweight='bold',
                     color=PresentationStyle.COLORS['text'],
                     bbox=dict(boxstyle='round,pad=0.8', facecolor=PresentationStyle.COLORS['bg_light'],
                             edgecolor=self.colors['active'], linewidth=3))

        # Instructions
        instructions = "SPACE: Train | B/N/P: Change View | T: Train 100 | R: Reset | S: Menu | Q: Quit"
        self.fig.text(0.5, 0.02, instructions, ha='center', fontsize=21, style='italic',
                     alpha=0.7, color=PresentationStyle.COLORS['dim'], fontweight='bold')

        # View name
        self.fig.text(0.5, 0.88, self.view_names[self.view_mode], ha='center',
                     fontsize=30, color=PresentationStyle.COLORS['dim'], style='italic')

    def draw_loss_curve(self):
        """Draw training loss curve - EXACT ORIGINAL WITH ALL FEATURES"""
        ax = self.fig.add_subplot(111, facecolor=PresentationStyle.COLORS['bg'])

        if len(self.nn.loss_history) > 0:
            epochs = range(1, len(self.nn.loss_history) + 1)
            ax.plot(epochs, self.nn.loss_history, linewidth=3, color=self.colors['active'],
                   marker='o', markersize=4, label='Training Loss')

            # Add exponential moving average - ORIGINAL FEATURE
            if len(self.nn.loss_history) > 10:
                window = min(10, len(self.nn.loss_history) // 5)
                ema = np.convolve(self.nn.loss_history, np.ones(window)/window, mode='valid')
                ax.plot(range(window, len(self.nn.loss_history) + 1), ema,
                       linewidth=2, color=PresentationStyle.COLORS['secondary'], linestyle='--',
                       alpha=0.7, label='Moving Average')

            ax.set_xlabel('Epoch', fontsize=27, fontweight='bold', color=PresentationStyle.COLORS['text'])
            ax.set_ylabel('Mean Squared Error', fontsize=27, fontweight='bold', color=PresentationStyle.COLORS['text'])
            ax.grid(True, alpha=0.3, linestyle='--', color=PresentationStyle.COLORS['dim'])
            ax.legend(fontsize=24, facecolor=PresentationStyle.COLORS['bg_light'], edgecolor=PresentationStyle.COLORS['dim'])
            ax.tick_params(colors=PresentationStyle.COLORS['text'])

            # Add convergence line - ORIGINAL FEATURE
            ax.axhline(y=0.01, color=self.colors['correct'], linestyle=':', linewidth=2,
                      alpha=0.7, label='Target')
            ax.text(len(epochs) * 0.95, 0.01, 'Converged', ha='right', va='bottom',
                   fontsize=21, color=self.colors['correct'], fontweight='bold')
        else:
            ax.text(0.5, 0.5, 'Press SPACE to start training',
                   ha='center', va='center', transform=ax.transAxes,
                   fontsize=33, color=PresentationStyle.COLORS['dim'], style='italic', fontweight='bold')

        # Training info
        info_text = f"Epoch: {self.nn.epoch} | Loss: {self.nn.loss_history[-1]:.4f}" if self.nn.loss_history else f"Epoch: {self.nn.epoch} | Loss: N/A"
        self.fig.text(0.5, 0.95, info_text, ha='center', fontsize=36, fontweight='bold',
                     color=PresentationStyle.COLORS['text'],
                     bbox=dict(boxstyle='round,pad=0.8', facecolor=PresentationStyle.COLORS['bg_light'],
                             edgecolor=self.colors['active'], linewidth=3))

        # Instructions
        instructions = "SPACE: Train | B/N/P: Change View | T: Train 100 | R: Reset | S: Menu | Q: Quit"
        self.fig.text(0.5, 0.02, instructions, ha='center', fontsize=21, style='italic',
                     alpha=0.7, color=PresentationStyle.COLORS['dim'], fontweight='bold')

        # View name
        self.fig.text(0.5, 0.88, self.view_names[self.view_mode], ha='center',
                     fontsize=30, color=PresentationStyle.COLORS['dim'], style='italic')

    def draw_combined(self):
        """Draw combined view - EXACT ORIGINAL"""
        gs = self.fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        # Network (top-left)
        ax1 = self.fig.add_subplot(gs[0, 0], facecolor=PresentationStyle.COLORS['bg'])
        ax1.set_xlim(-1, 11)
        ax1.set_ylim(-1, 6)
        ax1.axis('off')
        ax1.set_title('Network Architecture', fontsize=24, fontweight='bold',
                     color=PresentationStyle.COLORS['text'])

        # Simplified network drawing (3 hidden neurons!)
        input_x, hidden_x, output_x = 1, 5, 9
        input_y = [2, 4]
        hidden_y = [1, 3, 5]  # 3 HIDDEN NEURONS
        output_y = [3]

        # Connections
        for i, iy in enumerate(input_y):
            for j, hy in enumerate(hidden_y):
                weight = self.nn.weights_input_hidden[i, j]
                color = self.colors['active'] if weight > 0 else self.colors['inactive']
                alpha = min(abs(weight), 1.0)
                ax1.plot([input_x, hidden_x], [iy, hy], color=color, linewidth=1, alpha=alpha)

        for i, hy in enumerate(hidden_y):
            weight = self.nn.weights_hidden_output[i, 0]
            color = self.colors['active'] if weight > 0 else self.colors['inactive']
            alpha = min(abs(weight), 1.0)
            ax1.plot([hidden_x, output_x], [hy, output_y[0]], color=color, linewidth=1, alpha=alpha)

        # Neurons (smaller)
        for y in input_y:
            circle = Circle((input_x, y), 0.3, color=self.colors['neuron'], ec='white', linewidth=2)
            ax1.add_patch(circle)
        for y in hidden_y:
            circle = Circle((hidden_x, y), 0.3, color=self.colors['neuron'], ec='white', linewidth=2)
            ax1.add_patch(circle)
        circle = Circle((output_x, output_y[0]), 0.3, color=self.colors['neuron'], ec='white', linewidth=2)
        ax1.add_patch(circle)

        # Decision boundary (top-right)
        ax2 = self.fig.add_subplot(gs[0, 1], facecolor=PresentationStyle.COLORS['bg'])
        ax2.set_title('Decision Boundary', fontsize=24, fontweight='bold',
                     color=PresentationStyle.COLORS['text'])

        h = 0.05
        x_min, x_max = -0.5, 1.5
        y_min, y_max = -0.5, 1.5
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        Z = self.nn.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

        ax2.contourf(xx, yy, Z, levels=20, cmap='RdYlGn', alpha=0.6)
        ax2.contour(xx, yy, Z, levels=[0.5], colors=PresentationStyle.COLORS['text'], linewidths=2)

        for x, y in zip(self.nn.X, self.nn.y):
            color = self.colors['correct'] if y[0] == 1 else self.colors['wrong']
            ax2.scatter(x[0], x[1], s=200, c=color, edgecolors='white', linewidths=2)

        ax2.set_xlim(x_min, x_max)
        ax2.set_ylim(y_min, y_max)
        ax2.set_xlabel('Input 0', fontsize=21, color=PresentationStyle.COLORS['text'], fontweight='bold')
        ax2.set_ylabel('Input 1', fontsize=21, color=PresentationStyle.COLORS['text'], fontweight='bold')
        ax2.grid(True, alpha=0.3, color=PresentationStyle.COLORS['dim'])
        ax2.tick_params(colors=PresentationStyle.COLORS['text'])

        # Loss curve (bottom, spanning both columns)
        ax3 = self.fig.add_subplot(gs[1, :], facecolor=PresentationStyle.COLORS['bg'])
        ax3.set_title('Training Loss', fontsize=24, fontweight='bold',
                     color=PresentationStyle.COLORS['text'])

        if len(self.nn.loss_history) > 0:
            epochs = range(1, len(self.nn.loss_history) + 1)
            ax3.plot(epochs, self.nn.loss_history, linewidth=2, color=self.colors['active'],
                    marker='o', markersize=3)
            ax3.axhline(y=0.01, color=self.colors['correct'], linestyle=':', linewidth=2, alpha=0.7)
            ax3.set_xlabel('Epoch', fontsize=21, color=PresentationStyle.COLORS['text'], fontweight='bold')
            ax3.set_ylabel('MSE', fontsize=21, color=PresentationStyle.COLORS['text'], fontweight='bold')
            ax3.grid(True, alpha=0.3, color=PresentationStyle.COLORS['dim'])
            ax3.tick_params(colors=PresentationStyle.COLORS['text'])

        # Training info
        info_text = f"Epoch: {self.nn.epoch} | Loss: {self.nn.loss_history[-1]:.4f}" if self.nn.loss_history else f"Epoch: {self.nn.epoch} | Loss: N/A"
        self.fig.text(0.5, 0.96, info_text, ha='center', fontsize=30, fontweight='bold',
                     color=PresentationStyle.COLORS['text'],
                     bbox=dict(boxstyle='round,pad=0.6', facecolor=PresentationStyle.COLORS['bg_light'],
                             edgecolor=self.colors['active'], linewidth=2))

        # Instructions
        instructions = "SPACE: Train | B/N/P: Change View | T: Train 100 | R: Reset | S: Menu | Q: Quit"
        self.fig.text(0.5, 0.01, instructions, ha='center', fontsize=21, style='italic',
                     alpha=0.7, color=PresentationStyle.COLORS['dim'], fontweight='bold')

    def train_step(self):
        """Train for multiple epochs - EXACT ORIGINAL"""
        for _ in range(10):  # Train 10 epochs at a time
            self.nn.train_epoch()

        # Auto-cycle through inputs to show different examples
        self.current_input_idx = (self.current_input_idx + 1) % len(self.nn.X)

        self.setup_view()

        # Print progress
        if self.nn.epoch % 10 == 0:
            print(f"Epoch {self.nn.epoch}: Loss = {self.nn.loss_history[-1]:.4f}")

    def reset_network(self):
        """Reset the neural network - EXACT ORIGINAL"""
        self.nn = XORNeuralNetwork()
        self.setup_view()
        print("Network reset!")

    def show(self):
        """Show the presentation"""
        manager = plt.get_current_fig_manager()
        try:
            manager.window.state('zoomed')
        except:
            try:
                manager.window.showMaximized()
            except:
                pass

        plt.show()


def main():
    """Main function"""
    print("=" * 80)
    print("XOR NEURAL NETWORK TRAINING VISUALIZATION")
    print("=" * 80)
    print("\nArchitecture: 2 inputs → 3 hidden → 1 output")
    print("\nControls:")
    print("  SPACE     : Train 10 epochs (keep pressing for more!)")
    print("  C         : Cycle through different XOR inputs")
    print("  B / N / P : Change view")
    print("  T         : Train 100 epochs")
    print("  R         : Reset network")
    print("  S         : Selection menu")
    print("  Q         : Quit")
    print("  F         : Toggle fullscreen")
    print("\nViews:")
    print("  1. Network Architecture - See weights and activations in REAL TIME")
    print("  2. Decision Boundary - See how network separates classes")
    print("  3. Training Loss - See convergence over time")
    print("  4. Combined View - See everything at once")
    print("\nTIP: Press SPACE repeatedly to watch the network learn!")
    print("     Each press auto-cycles through XOR inputs: 0⊕0, 0⊕1, 1⊕0, 1⊕1")
    print("     Press C to manually cycle through inputs")
    print("=" * 80)

    presentation = NeuralNetworkPresentation()
    presentation.show()


if __name__ == "__main__":
    main()
