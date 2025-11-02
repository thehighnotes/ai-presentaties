"""
Neural Network Presentation - Step-by-step explanation
Gradually introduces neural network concepts without overwhelming

Steps:
1. Landing page
2. What is a Neural Network? (Simple explanation)
3. Input > Black Box > Output (Conceptual)
4. Opening the Black Box - Hidden Layer
5. XOR Problem Introduction
6. Interactive XOR Training (Original network, cleaner UI)

Features:
- Drawing mode (Left mouse click to draw, C to clear)
- Step-by-step progression with SPACE
- Clean, educational approach
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch, Rectangle
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import BasePresentation, PresentationStyle


class XORNeuralNetwork:
    """Simple XOR Neural Network - Same as original"""

    def __init__(self):
        np.random.seed(42)
        self.weights_input_hidden = np.random.randn(2, 3) * 0.5
        self.bias_hidden = np.random.randn(3) * 0.5
        self.weights_hidden_output = np.random.randn(3, 1) * 0.5
        self.bias_output = np.random.randn(1) * 0.5

        self.X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        self.y = np.array([[0], [1], [1], [0]])

        self.loss_history = []
        self.epoch = 0
        self.learning_rate = 0.5

        self.last_hidden = None
        self.last_output = None

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def forward(self, X):
        hidden_input = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        hidden_output = self.sigmoid(hidden_input)

        output_input = np.dot(hidden_output, self.weights_hidden_output) + self.bias_output
        output = self.sigmoid(output_input)

        self.last_hidden = hidden_output
        self.last_output = output

        return hidden_output, output

    def backward(self, X, y, hidden_output, output):
        output_error = y - output
        output_delta = output_error * self.sigmoid_derivative(output)

        hidden_error = output_delta.dot(self.weights_hidden_output.T)
        hidden_delta = hidden_error * self.sigmoid_derivative(hidden_output)

        self.weights_hidden_output += hidden_output.T.dot(output_delta) * self.learning_rate
        self.bias_output += np.sum(output_delta, axis=0) * self.learning_rate
        self.weights_input_hidden += X.T.dot(hidden_delta) * self.learning_rate
        self.bias_hidden += np.sum(hidden_delta, axis=0) * self.learning_rate

    def train_epoch(self):
        hidden_output, output = self.forward(self.X)
        self.backward(self.X, self.y, hidden_output, output)

        loss = np.mean((self.y - output) ** 2)
        self.loss_history.append(loss)
        self.epoch += 1

        return loss

    def predict(self, X):
        _, output = self.forward(X)
        return output


class NeuralNetworkPresentation(BasePresentation):
    """Step-by-step Neural Network explanation"""

    def __init__(self):
        step_names = [
            'Landing',
            'Wat is een Neural Network?',
            'Input > Black Box > Output',
            'De Hidden Layer Onthuld',
            'Het XOR Probleem',
            'Interactieve XOR Training'
        ]

        super().__init__("Neural Networks Uitgelegd", step_names)

        # Neural network for training step
        self.nn = XORNeuralNetwork()
        self.current_input_idx = 0

        # Drawing mode
        self.is_drawing = False
        self.drawing_points = []
        self.current_stroke = []

        # Mouse connections for drag drawing
        self.fig.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

        self.show_landing_page()

    def on_mouse_press(self, event):
        """Handle mouse press for drawing"""
        if event.button == 1 and event.inaxes:  # Left click
            self.is_drawing = True
            self.current_stroke = [(event.xdata, event.ydata)]

    def on_mouse_release(self, event):
        """Handle mouse release"""
        if event.button == 1 and self.is_drawing:
            self.is_drawing = False
            if len(self.current_stroke) > 1:
                # Save the completed stroke
                self.drawing_points.append(self.current_stroke.copy())
            self.current_stroke = []
            self.draw_current_step_static()

    def on_mouse_move(self, event):
        """Handle mouse movement for drag drawing"""
        if self.is_drawing and event.inaxes:
            self.current_stroke.append((event.xdata, event.ydata))
            # Redraw in real-time
            self.draw_current_step_static()

    def show_landing_page(self):
        """Landing page"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title box
        title_box = FancyBboxPatch(
            (10, 55), 80, 25,
            boxstyle="round,pad=2",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['secondary'],
            linewidth=4,
            alpha=0.95
        )
        ax.add_patch(title_box)

        ax.text(50, 72, 'Neural Networks',
                fontsize=72, fontweight='bold', ha='center', va='center',
                color=self.colors['secondary'])

        ax.text(50, 64, 'Van Simpel naar Complex - Stap voor Stap',
                fontsize=33, ha='center', va='center',
                color=self.colors['text'], alpha=0.8, style='italic')

        # Simple network icon
        ax.text(50, 45, '[O]---[O]---[O]',
                fontsize=60, ha='center', va='center',
                color=self.colors['accent'], family='monospace')

        # Instructions
        instr_box = FancyBboxPatch(
            (20, 15), 60, 15,
            boxstyle="round,pad=1",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['accent'],
            linewidth=3,
            alpha=0.9
        )
        ax.add_patch(instr_box)

        ax.text(50, 25, '>> Druk op SPATIE om te starten <<',
                fontsize=36, ha='center', va='center',
                color=self.colors['accent'], fontweight='bold')

        ax.text(50, 20, 'B=Terug • R=Reset • C=Clear tekening • Linkermuisklik=Teken',
                fontsize=20, ha='center', va='center',
                color=self.colors['dim'], style='italic')

        # Footer
        ax.text(50, 5, 'Interactief leren met tekenfunctie en stapsgewijze uitleg',
                fontsize=24, ha='center', va='center',
                color=self.colors['text'], alpha=0.5)

        plt.tight_layout()

    def get_frames_for_step(self, step: int) -> int:
        """Animation frames per step"""
        frames_dict = {
            0: 30,   # Landing
            1: 90,   # What is NN
            2: 100,  # Black box
            3: 110,  # Hidden layer
            4: 90,   # XOR problem
            5: 60    # Interactive (static, training is manual)
        }
        return frames_dict.get(step, 60)

    def animate_step(self, frame: int):
        """Animate current step"""
        total_frames = self.get_frames_for_step(self.current_step)
        progress = frame / (total_frames - 1) if total_frames > 1 else 1

        if self.current_step == 0:
            pass  # Landing is static
        elif self.current_step == 1:
            self.draw_what_is_nn(progress)
        elif self.current_step == 2:
            self.draw_black_box(progress)
        elif self.current_step == 3:
            self.draw_hidden_layer_revealed(progress)
        elif self.current_step == 4:
            self.draw_xor_problem(progress)
        elif self.current_step == 5:
            self.draw_interactive_training(progress)

        if frame >= total_frames - 1:
            self.on_animation_complete()

    def draw_current_step_static(self):
        """Draw current step as static image"""
        if self.current_step == -1:
            self.show_landing_page()
        elif self.current_step == 1:
            self.draw_what_is_nn(1.0)
        elif self.current_step == 2:
            self.draw_black_box(1.0)
        elif self.current_step == 3:
            self.draw_hidden_layer_revealed(1.0)
        elif self.current_step == 4:
            self.draw_xor_problem(1.0)
        elif self.current_step == 5:
            self.draw_interactive_training(1.0)

        # Draw any user drawings (completed strokes)
        if len(self.drawing_points) > 0 and len(self.fig.axes) > 0:
            ax = self.fig.axes[0]
            for stroke in self.drawing_points:
                if len(stroke) > 1:
                    xs = [p[0] for p in stroke]
                    ys = [p[1] for p in stroke]
                    ax.plot(xs, ys, color=self.colors['highlight'],
                           linewidth=4, alpha=0.9, solid_capstyle='round')

        # Draw current stroke being drawn
        if len(self.current_stroke) > 1 and len(self.fig.axes) > 0:
            ax = self.fig.axes[0]
            xs = [p[0] for p in self.current_stroke]
            ys = [p[1] for p in self.current_stroke]
            ax.plot(xs, ys, color=self.colors['highlight'],
                   linewidth=4, alpha=0.7, solid_capstyle='round')

        plt.draw()

    def on_custom_key(self, key):
        """Handle custom keyboard input - called by ControlHandler"""
        if key == 'c':  # Clear drawing
            self.drawing_points = []
            self.current_stroke = []
            self.is_drawing = False
            self.draw_current_step_static()
            print("✓ Tekeningen gewist!")
        elif key == 't':  # Train (alternative to space in step 5)
            if self.current_step == 5:
                self.train_network_step()

    def start_next_step(self):
        """Override to handle space in training step"""
        if self.current_step == 5:
            # In training step, space trains instead of advancing
            self.train_network_step()
        else:
            # Normal behavior
            super().start_next_step()

    def reset(self):
        """Reset presentation and neural network"""
        # Reset the neural network
        self.nn = XORNeuralNetwork()
        self.current_input_idx = 0

        # Clear drawings
        self.drawing_points = []
        self.current_stroke = []
        self.is_drawing = False

        # Call parent reset
        super().reset()
        print("✓ Neural network ook gereset!")

    def train_network_step(self):
        """Train network for 10 epochs"""
        for _ in range(10):
            self.nn.train_epoch()

        self.current_input_idx = (self.current_input_idx + 1) % len(self.nn.X)

        # Redraw the interactive training view
        self.draw_interactive_training(1.0)

        # Re-apply drawings
        if len(self.drawing_points) > 0 and len(self.fig.axes) > 0:
            ax = self.fig.axes[0]
            for stroke in self.drawing_points:
                if len(stroke) > 1:
                    xs = [p[0] for p in stroke]
                    ys = [p[1] for p in stroke]
                    ax.plot(xs, ys, color=self.colors['highlight'],
                           linewidth=4, alpha=0.9, solid_capstyle='round')

        plt.draw()

        # Print progress
        print(f"Epoch {self.nn.epoch}: Loss = {self.nn.loss_history[-1]:.4f}")

    def draw_what_is_nn(self, progress: float):
        """Step 1: What is a Neural Network?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        alpha = min(1.0, progress / 0.15)
        ax.text(50, 95, 'Wat is een Neural Network?',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['secondary'], alpha=alpha)

        # Simple explanation
        if progress > 0.2:
            exp_alpha = min(1.0, (progress - 0.2) / 0.2)

            explanation_box = FancyBboxPatch(
                (10, 70), 80, 18,
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=3,
                alpha=0.95 * exp_alpha
            )
            ax.add_patch(explanation_box)

            explanation = "Een Neural Network is een wiskundig model\ngeïnspireerd door het menselijk brein"
            ax.text(50, 79, explanation,
                    fontsize=27, ha='center', va='center',
                    color=self.colors['text'], alpha=exp_alpha)

        # Brain analogy
        if progress > 0.4:
            brain_alpha = min(1.0, (progress - 0.4) / 0.2)

            # Left: Brain
            ax.text(20, 55, '[BRAIN]',
                    fontsize=48, ha='center', va='center',
                    color=self.colors['purple'], alpha=brain_alpha)

            ax.text(20, 48, 'Menselijk Brein\nNeuronen',
                    fontsize=19, ha='center', va='center',
                    color=self.colors['text'], alpha=brain_alpha)

            # Arrow
            arrow = FancyArrowPatch(
                (30, 55), (45, 55),
                arrowstyle='-|>',
                mutation_scale=40,
                linewidth=4,
                color=self.colors['accent'],
                alpha=brain_alpha
            )
            ax.add_artist(arrow)

            ax.text(37.5, 58, 'inspireert',
                    fontsize=16, ha='center', va='bottom',
                    color=self.colors['accent'], alpha=brain_alpha,
                    style='italic')

            # Right: Neural Network
            ax.text(80, 55, '[O]--[O]--[O]',
                    fontsize=36, ha='center', va='center',
                    color=self.colors['secondary'], alpha=brain_alpha,
                    family='monospace')

            ax.text(80, 48, 'Artificial Neural Network\nKunstmatige Neuronen',
                    fontsize=19, ha='center', va='center',
                    color=self.colors['text'], alpha=brain_alpha)

        # Key concept
        if progress > 0.65:
            concept_alpha = min(1.0, (progress - 0.65) / 0.25)

            concept_box = FancyBboxPatch(
                (15, 20), 70, 20,
                boxstyle="round,pad=1.2",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=3,
                alpha=0.95 * concept_alpha
            )
            ax.add_patch(concept_box)

            ax.text(50, 34, '[i] Kernidee',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['highlight'], fontweight='bold',
                    alpha=concept_alpha)

            concept_text = "• Leert van voorbeelden (net als mensen)\n"
            concept_text += "• Herkent patronen in data\n"
            concept_text += "• Wordt slimmer door training"

            ax.text(50, 25, concept_text,
                    fontsize=21, ha='center', va='center',
                    color=self.colors['text'], alpha=concept_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_black_box(self, progress: float):
        """Step 2: Input > Black Box > Output concept"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Input > Black Box > Output',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['accent'])

        ax.text(50, 90, 'Hoe een Neural Network werkt - Vereenvoudigd',
                fontsize=27, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Input (left)
        if progress > 0.1:
            input_alpha = min(1.0, (progress - 0.1) / 0.2)

            input_box = FancyBboxPatch(
                (5, 45), 20, 25,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['cyan'],
                linewidth=3,
                alpha=0.95 * input_alpha
            )
            ax.add_patch(input_box)

            ax.text(15, 63, 'INPUT',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['cyan'], fontweight='bold',
                    alpha=input_alpha)

            # Show concrete numbers instead of abstract [DATA]
            ax.text(15, 58, 'Getal 1:',
                    fontsize=20, ha='center', va='center',
                    color=self.colors['text'], alpha=input_alpha * 0.8)

            ax.text(15, 54.5, '0',
                    fontsize=42, ha='center', va='center',
                    color=self.colors['cyan'], fontweight='bold',
                    alpha=input_alpha)

            ax.text(15, 49.5, 'Getal 2:',
                    fontsize=20, ha='center', va='center',
                    color=self.colors['text'], alpha=input_alpha * 0.8)

            ax.text(15, 46, '1',
                    fontsize=42, ha='center', va='center',
                    color=self.colors['cyan'], fontweight='bold',
                    alpha=input_alpha)

        # Arrow to black box
        if progress > 0.25:
            arrow_alpha = min(1.0, (progress - 0.25) / 0.15)
            arrow = FancyArrowPatch(
                (25, 57.5), (35, 57.5),
                arrowstyle='-|>',
                mutation_scale=35,
                linewidth=5,
                color=self.colors['accent'],
                alpha=arrow_alpha
            )
            ax.add_artist(arrow)

        # Black Box (center)
        if progress > 0.35:
            box_alpha = min(1.0, (progress - 0.35) / 0.25)

            black_box = FancyBboxPatch(
                (35, 40), 30, 35,
                boxstyle="round,pad=1.5",
                facecolor='#0a0a0a',
                edgecolor=self.colors['warning'],
                linewidth=4,
                alpha=0.95 * box_alpha
            )
            ax.add_patch(black_box)

            ax.text(50, 68, '[?] BLACK BOX [?]',
                    fontsize=21, ha='center', va='center',
                    color=self.colors['warning'], fontweight='bold',
                    alpha=box_alpha)

            ax.text(50, 62, 'Hidden Layer',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['text'], alpha=box_alpha,
                    style='italic')

            ax.text(50, 55, '???',
                    fontsize=60, ha='center', va='center',
                    color=self.colors['dim'], alpha=box_alpha * 0.5)

            ax.text(50, 45, 'Magie gebeurt hier',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=box_alpha * 0.7)

        # Arrow to output
        if progress > 0.6:
            arrow_alpha = min(1.0, (progress - 0.6) / 0.15)
            arrow = FancyArrowPatch(
                (65, 57.5), (75, 57.5),
                arrowstyle='-|>',
                mutation_scale=35,
                linewidth=5,
                color=self.colors['accent'],
                alpha=arrow_alpha
            )
            ax.add_artist(arrow)

        # Output (right)
        if progress > 0.7:
            output_alpha = min(1.0, (progress - 0.7) / 0.25)

            output_box = FancyBboxPatch(
                (75, 45), 20, 25,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * output_alpha
            )
            ax.add_patch(output_box)

            ax.text(85, 63, 'OUTPUT',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=output_alpha)

            ax.text(85, 57, '[RESULT]',
                    fontsize=33, ha='center', va='center',
                    color=self.colors['text'], alpha=output_alpha)

            ax.text(85, 51, 'Voorspelling:\n1',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'], alpha=output_alpha)

        # Explanation
        if progress > 0.85:
            exp_alpha = min(1.0, (progress - 0.85) / 0.15)

            exp_box = FancyBboxPatch(
                (15, 15), 70, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['purple'],
                linewidth=3,
                alpha=0.95 * exp_alpha
            )
            ax.add_patch(exp_box)

            ax.text(50, 25, '[>>] Volgende stap: We openen de Black Box!',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['purple'], fontweight='bold',
                    alpha=exp_alpha)

            ax.text(50, 19, 'Ontdek wat er binnen gebeurt...',
                    fontsize=19, ha='center', va='center',
                    color=self.colors['text'], alpha=exp_alpha,
                    style='italic')

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_hidden_layer_revealed(self, progress: float):
        """Step 3: Opening the black box - show hidden layer"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'De Hidden Layer Onthuld!',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['highlight'])

        ax.text(50, 90, 'Wat zit er in de Black Box?',
                fontsize=27, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Show simple network structure
        input_x, hidden_x, output_x = 15, 50, 85
        input_y = [50, 65]
        hidden_y = [45, 57.5, 70]
        output_y = [57.5]

        # Input layer
        if progress > 0.1:
            input_alpha = min(1.0, (progress - 0.1) / 0.15)

            for i, y in enumerate(input_y):
                circle = Circle((input_x, y), 4,
                               facecolor=self.colors['cyan'],
                               edgecolor='white', linewidth=3,
                               alpha=input_alpha)
                ax.add_patch(circle)

                ax.text(input_x, y, f'{i}',
                        fontsize=24, ha='center', va='center',
                        color='white', fontweight='bold',
                        alpha=input_alpha)

            ax.text(input_x, 80, 'INPUT\n(2 getallen)',
                    fontsize=21, ha='center', va='center',
                    color=self.colors['cyan'], fontweight='bold',
                    alpha=input_alpha)

        # Hidden layer - revealed!
        if progress > 0.35:
            hidden_alpha = min(1.0, (progress - 0.35) / 0.25)

            # Box around hidden layer
            hidden_box = FancyBboxPatch(
                (40, 38), 20, 37,
                boxstyle="round,pad=1.2",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=4,
                alpha=0.9 * hidden_alpha
            )
            ax.add_patch(hidden_box)

            for i, y in enumerate(hidden_y):
                circle = Circle((hidden_x, y), 4,
                               facecolor=self.colors['secondary'],
                               edgecolor='white', linewidth=3,
                               alpha=hidden_alpha)
                ax.add_patch(circle)

                ax.text(hidden_x, y, f'H{i}',
                        fontsize=19, ha='center', va='center',
                        color='white', fontweight='bold',
                        alpha=hidden_alpha)

            ax.text(hidden_x, 80, 'HIDDEN LAYER\n(3 neuronen)',
                    fontsize=21, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=hidden_alpha)

        # Connections with explanation
        if progress > 0.55:
            conn_alpha = min(1.0, (progress - 0.55) / 0.2)

            # Draw a few connections as examples
            for i in range(2):
                for j in range(3):
                    ax.plot([input_x + 4, hidden_x - 4],
                           [input_y[i], hidden_y[j]],
                           color=self.colors['accent'],
                           linewidth=2, alpha=conn_alpha * 0.6,
                           linestyle='--')

        # Output layer
        if progress > 0.7:
            output_alpha = min(1.0, (progress - 0.7) / 0.2)

            circle = Circle((output_x, output_y[0]), 4,
                           facecolor=self.colors['highlight'],
                           edgecolor='white', linewidth=3,
                           alpha=output_alpha)
            ax.add_patch(circle)

            ax.text(output_x, output_y[0], 'R',
                    fontsize=24, ha='center', va='center',
                    color='white', fontweight='bold',
                    alpha=output_alpha)

            ax.text(output_x, 80, 'OUTPUT\n(resultaat)',
                    fontsize=21, ha='center', va='center',
                    color=self.colors['highlight'], fontweight='bold',
                    alpha=output_alpha)

            # Connections from hidden to output
            for j in range(3):
                ax.plot([hidden_x + 4, output_x - 4],
                       [hidden_y[j], output_y[0]],
                       color=self.colors['accent'],
                       linewidth=2, alpha=output_alpha * 0.6,
                       linestyle='--')

        # Explanation of hidden layer
        if progress > 0.85:
            exp_alpha = min(1.0, (progress - 0.85) / 0.15)

            exp_box = FancyBboxPatch(
                (10, 10), 80, 22,
                boxstyle="round,pad=1.2",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['purple'],
                linewidth=3,
                alpha=0.95 * exp_alpha
            )
            ax.add_patch(exp_box)

            ax.text(50, 26, '[i] Hidden Layer = Combinaties Detecteren',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['purple'], fontweight='bold',
                    alpha=exp_alpha)

            explanation = "Elke neuron in de hidden layer ontvangt ALLE inputs\n"
            explanation += "en maakt verschillende combinaties:\n"
            explanation += "H0 = Combinatie van Input 0 + Input 1 (met gewichten)\n"
            explanation += "H1 = Een andere combinatie van Input 0 + Input 1\n"
            explanation += "H2 = Nog een andere combinatie..."

            ax.text(50, 15, explanation,
                    fontsize=16, ha='center', va='center',
                    color=self.colors['text'], alpha=exp_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_xor_problem(self, progress: float):
        """Step 4: Introduce XOR problem - SIMPLIFIED"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 95, 'Het XOR Probleem',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['accent'])

        ax.text(50, 89, 'Een klassiek probleem om Neural Networks te demonstreren',
                fontsize=24, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Simple XOR explanation
        if progress > 0.15:
            exp_alpha = min(1.0, (progress - 0.15) / 0.25)

            xor_box = FancyBboxPatch(
                (15, 67), 70, 15,
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['cyan'],
                linewidth=4,
                alpha=0.95 * exp_alpha
            )
            ax.add_patch(xor_box)

            ax.text(50, 77, 'XOR = "Exclusive OR"',
                    fontsize=33, ha='center', va='center',
                    color=self.colors['cyan'], fontweight='bold',
                    alpha=exp_alpha)

            ax.text(50, 70.5, 'Output is 1 alleen wanneer de inputs VERSCHILLEN',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['text'], alpha=exp_alpha)

        # Show 4 examples in a clear row
        if progress > 0.4:
            examples_alpha = min(1.0, (progress - 0.4) / 0.3)

            # Title for examples
            ax.text(50, 57, 'De 4 Mogelijkheden:',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['text'], fontweight='bold',
                    alpha=examples_alpha)

            # 4 examples in a horizontal row
            examples = [
                ('0 XOR 0', '0', False, 17),
                ('0 XOR 1', '1', True, 38),
                ('1 XOR 0', '1', True, 59),
                ('1 XOR 1', '0', False, 80)
            ]

            for label, result, is_true, x_pos in examples:
                # Box color based on output
                box_color = self.colors['secondary'] if is_true else self.colors['error']

                example_box = FancyBboxPatch(
                    (x_pos - 8, 30), 16, 21,
                    boxstyle="round,pad=1",
                    facecolor=box_color,
                    edgecolor='white',
                    linewidth=4,
                    alpha=examples_alpha * 0.85
                )
                ax.add_patch(example_box)

                # Input label
                ax.text(x_pos, 47, label,
                        fontsize=21, ha='center', va='center',
                        color='white', fontweight='bold',
                        alpha=examples_alpha)

                # Arrow
                ax.text(x_pos, 40, '↓',
                        fontsize=30, ha='center', va='center',
                        color='white', alpha=examples_alpha)

                # Output result
                ax.text(x_pos, 34, result,
                        fontsize=48, ha='center', va='center',
                        color='white', fontweight='bold',
                        alpha=examples_alpha)

        # Challenge box
        if progress > 0.7:
            challenge_alpha = min(1.0, (progress - 0.7) / 0.25)

            challenge_box = FancyBboxPatch(
                (15, 8), 70, 15,
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=4,
                alpha=0.95 * challenge_alpha
            )
            ax.add_patch(challenge_box)

            ax.text(50, 18.5, '[!] Uitdaging: Train een Neural Network om XOR te leren!',
                    fontsize=27, ha='center', va='center',
                    color=self.colors['highlight'], fontweight='bold',
                    alpha=challenge_alpha)

            ax.text(50, 12, 'Druk SPATIE om naar de interactieve training te gaan >>',
                    fontsize=21, ha='center', va='center',
                    color=self.colors['text'], alpha=challenge_alpha,
                    style='italic')

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_interactive_training(self, progress: float):
        """Step 5: Interactive XOR training - cleaner UI"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(-1, 11)
        ax.set_ylim(-1, 6)

        # Network structure
        input_x, hidden_x, output_x = 1, 5, 9
        input_y = [1.5, 3.5]
        hidden_y = [0.5, 2.5, 4.5]
        output_y = [2.5]

        # Get current input
        current_x = self.nn.X[self.current_input_idx]
        current_y = self.nn.y[self.current_input_idx]
        _, _ = self.nn.forward(current_x.reshape(1, -1))

        # Draw connections with weights
        for i, iy in enumerate(input_y):
            for j, hy in enumerate(hidden_y):
                weight = self.nn.weights_input_hidden[i, j]
                color = self.colors['secondary'] if weight > 0 else self.colors['dim']
                alpha = min(abs(weight) * 0.7, 0.9)
                ax.plot([input_x, hidden_x], [iy, hy], color=color,
                       linewidth=2, alpha=alpha, zorder=1)

                # Weight value
                mid_x, mid_y = (input_x + hidden_x) / 2, (iy + hy) / 2
                ax.text(mid_x, mid_y, f'{weight:.1f}', fontsize=13, fontweight='bold',
                       ha='center', va='center',
                       bbox=dict(boxstyle='round,pad=0.3',
                                facecolor=self.colors['bg_light'],
                                edgecolor=color, linewidth=1.5, alpha=0.9),
                       color=self.colors['text'])

        for i, hy in enumerate(hidden_y):
            weight = self.nn.weights_hidden_output[i, 0]
            color = self.colors['secondary'] if weight > 0 else self.colors['dim']
            alpha = min(abs(weight) * 0.7, 0.9)
            ax.plot([hidden_x, output_x], [hy, output_y[0]], color=color,
                   linewidth=2, alpha=alpha, zorder=1)

            mid_x, mid_y = (hidden_x + output_x) / 2, (hy + output_y[0]) / 2
            ax.text(mid_x, mid_y, f'{weight:.1f}', fontsize=13, fontweight='bold',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.3',
                            facecolor=self.colors['bg_light'],
                            edgecolor=color, linewidth=1.5, alpha=0.9),
                   color=self.colors['text'])

        # Draw neurons
        neuron_size = 0.4

        # Input neurons
        for i, y in enumerate(input_y):
            input_value = current_x[i]
            neuron_color = self.colors['cyan'] if input_value > 0.5 else self.colors['bg_light']
            circle = Circle((input_x, y), neuron_size, color=neuron_color,
                          ec='white', linewidth=3, zorder=3)
            ax.add_patch(circle)

            ax.text(input_x, y, f'{input_value:.0f}',
                   fontsize=21, ha='center', va='center',
                   color='white', fontweight='bold')

            ax.text(input_x - 0.7, y, f'I{i}', ha='right', va='center',
                   fontsize=18, color=self.colors['text'])

        # Hidden neurons - SHOW COMBINATIONS
        for i, y in enumerate(hidden_y):
            activation = 0
            if self.nn.last_hidden is not None:
                activation = self.nn.last_hidden[0, i]

            color = plt.cm.RdYlGn(activation)
            circle = Circle((hidden_x, y), neuron_size, color=color,
                          ec='white', linewidth=3, alpha=0.9, zorder=3)
            ax.add_patch(circle)

            ax.text(hidden_x, y, f'{activation:.2f}',
                   fontsize=16, ha='center', va='center',
                   color='white', fontweight='bold')

            # Label showing it's a combination
            ax.text(hidden_x, y - 0.65, f'H{i}',
                   fontsize=15, ha='center', va='top',
                   color=self.colors['text'], fontweight='bold')

        # Output neuron
        activation = 0
        if self.nn.last_output is not None:
            activation = self.nn.last_output[0, 0]

        color = plt.cm.RdYlGn(activation)
        circle = Circle((output_x, output_y[0]), neuron_size, color=color,
                      ec='white', linewidth=3, alpha=0.9, zorder=3)
        ax.add_patch(circle)

        ax.text(output_x, output_y[0], f'{activation:.2f}',
               fontsize=18, ha='center', va='center',
               color='white', fontweight='bold')

        ax.text(output_x + 0.7, output_y[0], 'Output',
               fontsize=18, ha='left', va='center',
               color=self.colors['text'])

        # Target value
        ax.text(output_x, output_y[0] - 0.65, f'Target: {current_y[0]:.0f}',
               fontsize=16, ha='center', va='top',
               color=self.colors['secondary'] if abs(activation - current_y[0]) < 0.3 else self.colors['error'],
               fontweight='bold')

        # Layer labels
        ax.text(input_x, 5.2, 'Input', ha='center', fontsize=21,
               color=self.colors['cyan'], fontweight='bold')
        ax.text(hidden_x, 5.2, 'Hidden (Combinaties)', ha='center', fontsize=21,
               color=self.colors['secondary'], fontweight='bold')
        ax.text(output_x, 5.2, 'Output', ha='center', fontsize=21,
               color=self.colors['highlight'], fontweight='bold')

        # Training info
        loss_text = f"{self.nn.loss_history[-1]:.4f}" if self.nn.loss_history else "N/A"
        input_text = f"{int(current_x[0])} XOR {int(current_x[1])} = {current_y[0]:.0f}"
        info_text = f"Epoch: {self.nn.epoch} | Loss: {loss_text} | Input: {input_text}"

        self.fig.text(0.5, 0.95, info_text, ha='center', fontsize=27, fontweight='bold',
                     color=self.colors['text'],
                     bbox=dict(boxstyle='round,pad=0.6',
                             facecolor=self.colors['bg_light'],
                             edgecolor=self.colors['accent'],
                             linewidth=2))

        # Instructions
        instructions = "SPATIE: Train 10 epochs | C: Clear tekening | B: Terug | R: Reset"
        self.fig.text(0.5, 0.02, instructions, ha='center', fontsize=18,
                     color=self.colors['dim'], style='italic')

        # Explanation box - Hidden layer combinations (rechts onder)
        combo_text = "[i] Hidden Layer maakt combinaties:\n"
        combo_text += f"H0 krijgt I0({current_x[0]:.0f}) + I1({current_x[1]:.0f})\n"
        combo_text += f"H1 krijgt I0({current_x[0]:.0f}) + I1({current_x[1]:.0f})\n"
        combo_text += f"H2 krijgt I0({current_x[0]:.0f}) + I1({current_x[1]:.0f})\n"
        combo_text += "Elk met eigen gewichten!"

        self.fig.text(0.98, 0.15, combo_text, ha='right', va='bottom',
                     fontsize=16, family='monospace',
                     color=self.colors['text'],
                     bbox=dict(boxstyle='round,pad=0.6',
                             facecolor=self.colors['bg_light'],
                             edgecolor=self.colors['purple'],
                             linewidth=2, alpha=0.9))

        plt.tight_layout()


def main():
    """Main entry point"""
    print("="*80)
    print("NEURAL NETWORKS UITGELEGD - STAPSGEWIJS")
    print("="*80)
    print("\nDeze presentatie legt Neural Networks uit zonder te overweldigen:")
    print("  1. Landing - Introductie")
    print("  2. Wat is een Neural Network?")
    print("  3. Input > Black Box > Output concept")
    print("  4. De Hidden Layer onthuld (combinaties!)")
    print("  5. Het XOR probleem")
    print("  6. Interactieve XOR training")
    print("\nControls:")
    print("  SPACE       : Volgende stap / Train (in stap 6)")
    print("  B           : Vorige stap")
    print("  R           : Reset")
    print("  C           : Clear tekening")
    print("  LINKERMUISKLIK : Teken op scherm")
    print("  Q           : Afsluiten")
    print("\nFeatures:")
    print("  • Tekenfunctionaliteit voor annotaties")
    print("  • Duidelijke uitleg van Hidden Layer als combinatie-detector")
    print("  • Stapsgewijze opbouw zonder overweldiging")
    print("  • Focus op begrip, niet op complexiteit")
    print("="*80)
    print()

    presentation = NeuralNetworkPresentation()
    presentation.show()


if __name__ == "__main__":
    main()
