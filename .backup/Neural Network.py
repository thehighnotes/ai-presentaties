"""
XOR Neural Network Training Visualization
Interactive presentation showing how neural networks learn

Controls:
- SPACE: Start/Continue training (10 epochs at a time)
- R: Reset network (start over)
- N: Next visualization view
- P: Previous visualization view
- F: Toggle fullscreen
- Q/ESC: Quit
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
from matplotlib.collections import LineCollection
import matplotlib.animation as animation
import matplotlib

# Set presentation style
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['font.family'] = 'sans-serif'

class XORNeuralNetwork:
    """Simple XOR Neural Network for visualization"""
    
    def __init__(self):
        # Network architecture: 2 inputs, 3 hidden, 1 output
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

class XORPresentation:
    def __init__(self):
        self.fig = plt.figure(figsize=(16, 9))
        self.nn = XORNeuralNetwork()
        self.view_mode = 0  # 0: network, 1: decision boundary, 2: loss curve, 3: combined
        self.view_names = ['Network Architecture', 'Decision Boundary', 'Training Loss', 'Combined View']
        
        self.colors = {
            'neuron': '#4ECDC4',
            'active': '#FF6B6B',
            'inactive': '#95A5A6',
            'correct': '#2ECC71',
            'wrong': '#E74C3C',
            'connection': '#BDC3C7'
        }
        
        self.setup_view()
        self.setup_controls()
        
    def setup_controls(self):
        """Setup keyboard controls"""
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        
    def on_key(self, event):
        """Handle keyboard events"""
        if event.key == ' ':  # Space - train
            self.train_step()
        elif event.key == 'r':  # Reset
            self.reset_network()
        elif event.key == 'n':  # Next view
            self.view_mode = (self.view_mode + 1) % len(self.view_names)
            self.setup_view()
        elif event.key == 'p':  # Previous view
            self.view_mode = (self.view_mode - 1) % len(self.view_names)
            self.setup_view()
        elif event.key in ['q', 'escape']:
            plt.close()
        elif event.key == 'f':
            manager = plt.get_current_fig_manager()
            manager.full_screen_toggle()
    
    def setup_view(self):
        """Setup current view"""
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
        """Draw neural network architecture"""
        ax = self.fig.add_subplot(111)
        ax.set_xlim(-1, 11)
        ax.set_ylim(-1, 6)
        ax.axis('off')
        
        # Layer positions
        input_x, hidden_x, output_x = 1, 5, 9
        input_y = [1.5, 3.5]
        hidden_y = [0.5, 2.5, 4.5]
        output_y = [2.5]
        
        # Draw connections with weights
        for i, iy in enumerate(input_y):
            for j, hy in enumerate(hidden_y):
                weight = self.nn.weights_input_hidden[i, j]
                color = self.colors['active'] if weight > 0 else self.colors['inactive']
                alpha = min(abs(weight), 1.0)
                ax.plot([input_x, hidden_x], [iy, hy], color=color, 
                       linewidth=2, alpha=alpha, zorder=1)
                # Weight value
                mid_x, mid_y = (input_x + hidden_x) / 2, (iy + hy) / 2
                ax.text(mid_x, mid_y, f'{weight:.2f}', fontsize=8, 
                       ha='center', va='center',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        for i, hy in enumerate(hidden_y):
            weight = self.nn.weights_hidden_output[i, 0]
            color = self.colors['active'] if weight > 0 else self.colors['inactive']
            alpha = min(abs(weight), 1.0)
            ax.plot([hidden_x, output_x], [hy, output_y[0]], color=color, 
                   linewidth=2, alpha=alpha, zorder=1)
            # Weight value
            mid_x, mid_y = (hidden_x + output_x) / 2, (hy + output_y[0]) / 2
            ax.text(mid_x, mid_y, f'{weight:.2f}', fontsize=8,
                   ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        # Draw neurons
        neuron_size = 0.4
        
        # Input layer
        for i, y in enumerate(input_y):
            circle = Circle((input_x, y), neuron_size, color=self.colors['neuron'], 
                          ec='white', linewidth=3, zorder=3)
            ax.add_patch(circle)
            ax.text(input_x, y, f'I{i}', ha='center', va='center', 
                   fontweight='bold', fontsize=12, color='white')
            ax.text(input_x - 0.8, y, f'Input {i}', ha='right', va='center', fontsize=10)
        
        # Hidden layer
        for i, y in enumerate(hidden_y):
            activation = 0
            if self.nn.last_hidden is not None:
                activation = np.mean(self.nn.last_hidden[:, i])
            color = plt.cm.RdYlGn(activation)
            circle = Circle((hidden_x, y), neuron_size, color=color, 
                          ec='white', linewidth=3, zorder=3)
            ax.add_patch(circle)
            ax.text(hidden_x, y, f'H{i}', ha='center', va='center', 
                   fontweight='bold', fontsize=12, color='white')
            ax.text(hidden_x, y - 0.7, f'{activation:.2f}', ha='center', 
                   va='top', fontsize=8, style='italic')
        
        # Output layer
        activation = 0
        if self.nn.last_output is not None:
            activation = np.mean(self.nn.last_output)
        color = plt.cm.RdYlGn(activation)
        circle = Circle((output_x, output_y[0]), neuron_size, color=color, 
                      ec='white', linewidth=3, zorder=3)
        ax.add_patch(circle)
        ax.text(output_x, output_y[0], 'O', ha='center', va='center', 
               fontweight='bold', fontsize=12, color='white')
        ax.text(output_x + 0.8, output_y[0], 'Output', ha='left', va='center', fontsize=10)
        ax.text(output_x, output_y[0] - 0.7, f'{activation:.2f}', ha='center', 
               va='top', fontsize=8, style='italic')
        
        # Layer labels
        ax.text(input_x, 5.5, 'Input Layer', ha='center', fontsize=14, fontweight='bold')
        ax.text(hidden_x, 5.5, 'Hidden Layer', ha='center', fontsize=14, fontweight='bold')
        ax.text(output_x, 5.5, 'Output Layer', ha='center', fontsize=14, fontweight='bold')
        
        # Training info
        info_text = f"Epoch: {self.nn.epoch} | Loss: {self.nn.loss_history[-1]:.4f}" if self.nn.loss_history else f"Epoch: {self.nn.epoch} | Loss: N/A"
        self.fig.text(0.5, 0.95, info_text, ha='center', fontsize=20, fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.8', facecolor='white', 
                             edgecolor=self.colors['active'], linewidth=3))
        
        # XOR Truth table
        truth_table = "XOR Truth Table:\n"
        truth_table += "0⊕0=0  0⊕1=1\n"
        truth_table += "1⊕0=1  1⊕1=0"
        self.fig.text(0.02, 0.98, truth_table, ha='left', va='top', fontsize=11,
                     family='monospace',
                     bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))
        
        # Current predictions
        if self.nn.last_output is not None:
            pred_text = "Current Predictions:\n"
            for i, (x, y_true) in enumerate(zip(self.nn.X, self.nn.y)):
                _, pred = self.nn.forward(x.reshape(1, -1))
                pred_val = pred[0, 0]
                correct = '✓' if abs(pred_val - y_true[0]) < 0.3 else '✗'
                color = 'green' if correct == '✓' else 'red'
                pred_text += f"{int(x[0])}⊕{int(x[1])}={y_true[0]:.0f} → {pred_val:.3f} {correct}\n"
            
            self.fig.text(0.98, 0.98, pred_text, ha='right', va='top', fontsize=11,
                         family='monospace',
                         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))
        
        # Instructions
        instructions = "SPACE: Train | R: Reset | N/P: Change View | F: Fullscreen | Q: Quit"
        self.fig.text(0.5, 0.02, instructions, ha='center', fontsize=11, style='italic', alpha=0.7)
        
        # View name
        self.fig.text(0.5, 0.88, self.view_names[self.view_mode], ha='center', 
                     fontsize=16, color='gray', style='italic')
    
    def draw_decision_boundary(self):
        """Draw decision boundary visualization"""
        ax = self.fig.add_subplot(111)
        
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
        ax.contour(xx, yy, Z, levels=[0.5], colors='black', linewidths=3)
        
        # Plot training points
        for i, (x, y) in enumerate(zip(self.nn.X, self.nn.y)):
            color = self.colors['correct'] if y[0] == 1 else self.colors['wrong']
            ax.scatter(x[0], x[1], s=500, c=color, edgecolors='white', 
                      linewidths=3, zorder=5)
            ax.text(x[0], x[1], f'{int(x[0])}⊕{int(x[1])}\n={int(y[0])}', 
                   ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_xlabel('Input 0', fontsize=14, fontweight='bold')
        ax.set_ylabel('Input 1', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        
        # Colorbar
        cbar = plt.colorbar(contour, ax=ax)
        cbar.set_label('Network Output', fontsize=12, fontweight='bold')
        
        # Training info
        info_text = f"Epoch: {self.nn.epoch} | Loss: {self.nn.loss_history[-1]:.4f}" if self.nn.loss_history else f"Epoch: {self.nn.epoch} | Loss: N/A"
        self.fig.text(0.5, 0.95, info_text, ha='center', fontsize=20, fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.8', facecolor='white',
                             edgecolor=self.colors['active'], linewidth=3))
        
        # Instructions
        instructions = "SPACE: Train | R: Reset | N/P: Change View | F: Fullscreen | Q: Quit"
        self.fig.text(0.5, 0.02, instructions, ha='center', fontsize=11, style='italic', alpha=0.7)
        
        # View name
        self.fig.text(0.5, 0.88, self.view_names[self.view_mode], ha='center',
                     fontsize=16, color='gray', style='italic')
    
    def draw_loss_curve(self):
        """Draw training loss curve"""
        ax = self.fig.add_subplot(111)
        
        if len(self.nn.loss_history) > 0:
            epochs = range(1, len(self.nn.loss_history) + 1)
            ax.plot(epochs, self.nn.loss_history, linewidth=3, color=self.colors['active'], 
                   marker='o', markersize=4, label='Training Loss')
            
            # Add exponential moving average
            if len(self.nn.loss_history) > 10:
                window = min(10, len(self.nn.loss_history) // 5)
                ema = np.convolve(self.nn.loss_history, np.ones(window)/window, mode='valid')
                ax.plot(range(window, len(self.nn.loss_history) + 1), ema, 
                       linewidth=2, color='blue', linestyle='--', alpha=0.7, label='Moving Average')
            
            ax.set_xlabel('Epoch', fontsize=14, fontweight='bold')
            ax.set_ylabel('Mean Squared Error', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.legend(fontsize=12)
            
            # Add convergence line
            ax.axhline(y=0.01, color='green', linestyle=':', linewidth=2, alpha=0.7, label='Target')
            ax.text(len(epochs) * 0.95, 0.01, 'Converged', ha='right', va='bottom', 
                   fontsize=10, color='green', fontweight='bold')
        else:
            ax.text(0.5, 0.5, 'Press SPACE to start training', 
                   ha='center', va='center', transform=ax.transAxes,
                   fontsize=18, color='gray', style='italic')
        
        # Training info
        info_text = f"Epoch: {self.nn.epoch} | Loss: {self.nn.loss_history[-1]:.4f}" if self.nn.loss_history else f"Epoch: {self.nn.epoch} | Loss: N/A"
        self.fig.text(0.5, 0.95, info_text, ha='center', fontsize=20, fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.8', facecolor='white',
                             edgecolor=self.colors['active'], linewidth=3))
        
        # Instructions
        instructions = "SPACE: Train | R: Reset | N/P: Change View | F: Fullscreen | Q: Quit"
        self.fig.text(0.5, 0.02, instructions, ha='center', fontsize=11, style='italic', alpha=0.7)
        
        # View name
        self.fig.text(0.5, 0.88, self.view_names[self.view_mode], ha='center',
                     fontsize=16, color='gray', style='italic')
    
    def draw_combined(self):
        """Draw combined view"""
        gs = self.fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # Network (top-left)
        ax1 = self.fig.add_subplot(gs[0, 0])
        ax1.set_xlim(-1, 11)
        ax1.set_ylim(-1, 6)
        ax1.axis('off')
        ax1.set_title('Network Architecture', fontsize=12, fontweight='bold')
        
        # Simplified network drawing
        input_x, hidden_x, output_x = 1, 5, 9
        input_y = [2, 4]
        hidden_y = [1, 3, 5]
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
        ax2 = self.fig.add_subplot(gs[0, 1])
        ax2.set_title('Decision Boundary', fontsize=12, fontweight='bold')
        
        h = 0.05
        x_min, x_max = -0.5, 1.5
        y_min, y_max = -0.5, 1.5
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        Z = self.nn.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        
        ax2.contourf(xx, yy, Z, levels=20, cmap='RdYlGn', alpha=0.6)
        ax2.contour(xx, yy, Z, levels=[0.5], colors='black', linewidths=2)
        
        for x, y in zip(self.nn.X, self.nn.y):
            color = self.colors['correct'] if y[0] == 1 else self.colors['wrong']
            ax2.scatter(x[0], x[1], s=200, c=color, edgecolors='white', linewidths=2)
        
        ax2.set_xlim(x_min, x_max)
        ax2.set_ylim(y_min, y_max)
        ax2.set_xlabel('Input 0', fontsize=10)
        ax2.set_ylabel('Input 1', fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        # Loss curve (bottom, spanning both columns)
        ax3 = self.fig.add_subplot(gs[1, :])
        ax3.set_title('Training Loss', fontsize=12, fontweight='bold')
        
        if len(self.nn.loss_history) > 0:
            epochs = range(1, len(self.nn.loss_history) + 1)
            ax3.plot(epochs, self.nn.loss_history, linewidth=2, color=self.colors['active'], 
                    marker='o', markersize=3)
            ax3.axhline(y=0.01, color='green', linestyle=':', linewidth=2, alpha=0.7)
            ax3.set_xlabel('Epoch', fontsize=10)
            ax3.set_ylabel('MSE', fontsize=10)
            ax3.grid(True, alpha=0.3)
        
        # Training info
        info_text = f"Epoch: {self.nn.epoch} | Loss: {self.nn.loss_history[-1]:.4f}" if self.nn.loss_history else f"Epoch: {self.nn.epoch} | Loss: N/A"
        self.fig.text(0.5, 0.96, info_text, ha='center', fontsize=16, fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.6', facecolor='white',
                             edgecolor=self.colors['active'], linewidth=2))
        
        # Instructions
        instructions = "SPACE: Train | R: Reset | N/P: Change View | F: Fullscreen | Q: Quit"
        self.fig.text(0.5, 0.01, instructions, ha='center', fontsize=10, style='italic', alpha=0.7)
    
    def train_step(self):
        """Train for multiple epochs"""
        for _ in range(10):  # Train 10 epochs at a time
            self.nn.train_epoch()
        self.setup_view()
        
        # Print progress
        if self.nn.epoch % 10 == 0:
            print(f"Epoch {self.nn.epoch}: Loss = {self.nn.loss_history[-1]:.4f}")
    
    def reset_network(self):
        """Reset the neural network"""
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
    print("=" * 60)
    print("XOR NEURAL NETWORK TRAINING VISUALIZATION")
    print("=" * 60)
    print("\nControls:")
    print("  SPACE     : Train 10 epochs")
    print("  R         : Reset network")
    print("  N/P       : Next/Previous view")
    print("  F         : Toggle fullscreen")
    print("  Q or ESC  : Quit")
    print("\nViews:")
    print("  1. Network Architecture - See weights and activations")
    print("  2. Decision Boundary - See how network separates classes")
    print("  3. Training Loss - See convergence over time")
    print("  4. Combined View - See everything at once")
    print("\nPress SPACE to start training...")
    print("=" * 60)
    
    presentation = XORPresentation()
    presentation.show()

if __name__ == "__main__":
    main()