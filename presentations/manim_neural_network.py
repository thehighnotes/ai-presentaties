"""
Manim XOR Neural Network Visualization
Complete Manim implementation with stunning animations

Architecture: 2 inputs → 3 hidden → 1 output

Scenes:
1. ForwardPropagation - Data flowing through network
2. TrainingVisualization - Gradient descent animation
3. DecisionBoundaryEvolution - Boundary morphing during training
4. CompleteOverview - Combined view with all elements

Usage:
    manim -pql manim_neural_network.py ForwardPropagation
    manim -pqh manim_neural_network.py TrainingVisualization
    manim -pqk manim_neural_network.py DecisionBoundaryEvolution  # 4K quality
    manim -pqk manim_neural_network.py CompleteOverview
"""

from manim import *
import numpy as np

# Configure Manim to use Pango instead of LaTeX
config.renderer = "cairo"


class XORNetwork:
    """XOR Neural Network for Manim visualization"""

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

        # Training state
        self.loss_history = []
        self.epoch = 0
        self.learning_rate = 0.5

        # Cache for visualization
        self.last_hidden = None
        self.last_output = None

    def sigmoid(self, x):
        """Sigmoid activation"""
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
        """Backward pass"""
        # Output error
        output_error = y - output
        output_delta = output_error * self.sigmoid_derivative(output)

        # Hidden error
        hidden_error = output_delta.dot(self.weights_hidden_output.T)
        hidden_delta = hidden_error * self.sigmoid_derivative(hidden_output)

        # Update weights
        self.weights_hidden_output += hidden_output.T.dot(output_delta) * self.learning_rate
        self.bias_output += np.sum(output_delta, axis=0) * self.learning_rate
        self.weights_input_hidden += X.T.dot(hidden_delta) * self.learning_rate
        self.bias_hidden += np.sum(hidden_delta, axis=0) * self.learning_rate

    def train_epoch(self):
        """Train one epoch"""
        hidden_output, output = self.forward(self.X)
        self.backward(self.X, self.y, hidden_output, output)

        loss = np.mean((self.y - output) ** 2)
        self.loss_history.append(loss)
        self.epoch += 1

        return loss

    def predict(self, X):
        """Prediction"""
        _, output = self.forward(X)
        return output


class NetworkNode(VGroup):
    """Animated neuron node with glow effect"""

    def __init__(self, value=0, radius=0.4, label="", **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.radius = radius

        # Main circle
        self.circle = Circle(
            radius=radius,
            fill_opacity=0.8,
            stroke_width=4,
            stroke_color=WHITE
        )

        # Glow effect (multiple circles)
        self.glow = VGroup()
        for i in range(3):
            glow_circle = Circle(
                radius=radius * (1 + 0.15 * (i + 1)),
                stroke_width=2 - i * 0.5,
                stroke_opacity=0.3 - i * 0.1,
                fill_opacity=0
            )
            self.glow.add(glow_circle)

        # Value text - use Text instead of DecimalNumber to avoid LaTeX dependency
        self.value_text = Text(
            f"{value:.2f}",
            font_size=28,
            color=WHITE
        )

        # Label
        self.label = Text(label, font_size=24, color=GRAY).next_to(self.circle, DOWN, buff=0.2)

        self.add(self.glow, self.circle, self.value_text, self.label)
        self.update_color()

    def update_color(self):
        """Update color based on value"""
        # Interpolate between red (0) and green (1)
        color = interpolate_color(RED, GREEN, self.value)
        self.circle.set_fill(color, opacity=0.8)
        self.glow.set_stroke(color)

    def set_value(self, value):
        """Update value and color"""
        self.value = value
        # Update text content
        new_text = Text(f"{value:.2f}", font_size=28, color=WHITE)
        new_text.move_to(self.value_text.get_center())
        self.remove(self.value_text)
        self.value_text = new_text
        self.add(self.value_text)
        self.update_color()

    def pulse(self):
        """Pulse animation"""
        return Succession(
            self.circle.animate(rate_func=rush_into).scale(1.2),
            self.circle.animate(rate_func=rush_from).scale(1/1.2)
        )


class ConnectionEdge(VGroup):
    """Animated connection with weight visualization"""

    def __init__(self, start_node, end_node, weight=1.0, **kwargs):
        super().__init__(**kwargs)
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight

        # Main line
        self.line = Line(
            start_node.get_center(),
            end_node.get_center(),
            stroke_width=abs(weight) * 3 + 1,
            stroke_opacity=0.7
        )

        # Weight label - use Text instead of DecimalNumber
        self.weight_label = Text(
            f"{weight:.1f}",
            font_size=20,
            color=WHITE
        ).move_to(self.line.get_center())

        # Background for label
        self.label_bg = BackgroundRectangle(
            self.weight_label,
            fill_opacity=0.8,
            buff=0.1,
            corner_radius=0.1
        )

        self.add(self.line, self.label_bg, self.weight_label)
        self.update_color()

    def update_color(self):
        """Update color based on weight"""
        color = GREEN if self.weight > 0 else RED
        self.line.set_stroke(color, opacity=min(abs(self.weight) * 0.7, 0.9))
        self.label_bg.set_fill(color, opacity=0.6)

    def update_line(self):
        """Update line position"""
        new_line = Line(
            self.start_node.get_center(),
            self.end_node.get_center(),
            stroke_width=abs(self.weight) * 3 + 1
        )
        self.line.become(new_line)
        self.weight_label.move_to(self.line.get_center())
        self.label_bg.move_to(self.weight_label.get_center())
        self.update_color()


class DataFlowParticle(Dot):
    """Particle that flows along connections"""

    def __init__(self, color=YELLOW, **kwargs):
        super().__init__(
            radius=0.08,
            color=color,
            fill_opacity=1.0,
            **kwargs
        )

        # Add glow
        self.glow = Circle(
            radius=0.15,
            stroke_color=color,
            stroke_width=2,
            stroke_opacity=0.5,
            fill_opacity=0
        ).move_to(self.get_center())

    def flow_along(self, path, run_time=1.5, **kwargs):
        """Animate flowing along a path"""
        return AnimationGroup(
            MoveAlongPath(self, path, run_time=run_time, rate_func=smooth, **kwargs),
            MoveAlongPath(self.glow, path, run_time=run_time, rate_func=smooth, **kwargs)
        )


class ForwardPropagation(Scene):
    """Scene 1: Forward Propagation Animation with flowing data"""

    def construct(self):
        # Title
        title = Text("XOR Neural Network: Forward Propagation", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Initialize network
        self.network = XORNetwork()

        # Create network visualization
        self.create_network()

        # Show initial state
        self.play(
            *[Create(node) for node in self.all_nodes],
            run_time=1.5
        )
        self.wait(0.5)

        # Draw connections
        self.play(
            *[Create(edge) for edge in self.all_edges],
            run_time=2
        )
        self.wait(0.5)

        # Demonstrate forward propagation for each XOR input
        xor_inputs = [
            ([0, 0], 0, "0 ⊕ 0 = 0"),
            ([0, 1], 1, "0 ⊕ 1 = 1"),
            ([1, 0], 1, "1 ⊕ 0 = 1"),
            ([1, 1], 0, "1 ⊕ 1 = 0")
        ]

        for input_data, expected, label_text in xor_inputs:
            # Show input label
            input_label = Text(label_text, font_size=36, color=YELLOW).to_edge(DOWN)
            self.play(Write(input_label))

            # Forward pass animation
            self.animate_forward_pass(input_data, expected)

            self.play(FadeOut(input_label))
            self.wait(0.5)

        # Conclusion
        conclusion = Text(
            "Network needs training to learn XOR!",
            font_size=40,
            color=RED
        ).to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)

        # Fade out
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

    def create_network(self):
        """Create network nodes and connections"""
        # Layer positions
        input_x, hidden_x, output_x = -4, 0, 4

        # Input layer (2 nodes)
        self.input_nodes = VGroup()
        for i in range(2):
            y = 1.5 - i * 3  # Spacing: 1.5, -1.5
            node = NetworkNode(value=0, label=f"Input {i}")
            node.move_to([input_x, y, 0])
            self.input_nodes.add(node)

        # Hidden layer (3 nodes)
        self.hidden_nodes = VGroup()
        for i in range(3):
            y = 2 - i * 2  # Spacing: 2, 0, -2
            node = NetworkNode(value=0, label=f"H{i}")
            node.move_to([hidden_x, y, 0])
            self.hidden_nodes.add(node)

        # Output layer (1 node)
        self.output_node = NetworkNode(value=0, label="Output")
        self.output_node.move_to([output_x, 0, 0])

        self.all_nodes = VGroup(self.input_nodes, self.hidden_nodes, self.output_node)

        # Create connections
        self.input_hidden_edges = VGroup()
        for i, input_node in enumerate(self.input_nodes):
            for j, hidden_node in enumerate(self.hidden_nodes):
                weight = self.network.weights_input_hidden[i, j]
                edge = ConnectionEdge(input_node, hidden_node, weight)
                self.input_hidden_edges.add(edge)

        self.hidden_output_edges = VGroup()
        for i, hidden_node in enumerate(self.hidden_nodes):
            weight = self.network.weights_hidden_output[i, 0]
            edge = ConnectionEdge(hidden_node, self.output_node, weight)
            self.hidden_output_edges.add(edge)

        self.all_edges = VGroup(self.input_hidden_edges, self.hidden_output_edges)

    def animate_forward_pass(self, input_data, expected_output):
        """Animate forward propagation"""
        # Set input values
        for i, (node, value) in enumerate(zip(self.input_nodes, input_data)):
            node.set_value(value)
            self.play(
                Indicate(node, color=YELLOW, scale_factor=1.3),
                run_time=0.5
            )

        self.wait(0.3)

        # Animate data flowing from input to hidden
        particles_to_hidden = VGroup()
        animations = []

        for i, input_node in enumerate(self.input_nodes):
            if input_data[i] > 0:  # Only show particles for active inputs
                for j, hidden_node in enumerate(self.hidden_nodes):
                    particle = DataFlowParticle(color=YELLOW)
                    particle.move_to(input_node.get_center())
                    particles_to_hidden.add(particle, particle.glow)

                    path = Line(input_node.get_center(), hidden_node.get_center())
                    animations.append(particle.flow_along(path, run_time=1.0))

        if animations:
            self.play(*animations)
            self.play(FadeOut(particles_to_hidden))

        # Compute hidden activations
        hidden_output, output = self.network.forward(np.array(input_data).reshape(1, -1))

        # Update hidden nodes with pulse
        for i, node in enumerate(self.hidden_nodes):
            activation = hidden_output[0, i]
            node.set_value(activation)
            self.play(node.pulse(), run_time=0.4)

        self.wait(0.3)

        # Animate data flowing from hidden to output
        particles_to_output = VGroup()
        animations = []

        for i, hidden_node in enumerate(self.hidden_nodes):
            particle = DataFlowParticle(color=BLUE)
            particle.move_to(hidden_node.get_center())
            particles_to_output.add(particle, particle.glow)

            path = Line(hidden_node.get_center(), self.output_node.get_center())
            animations.append(particle.flow_along(path, run_time=1.0))

        self.play(*animations)
        self.play(FadeOut(particles_to_output))

        # Update output node
        output_value = output[0, 0]
        self.output_node.set_value(output_value)
        self.play(self.output_node.pulse(), run_time=0.5)

        # Show prediction vs expected
        error = abs(output_value - expected_output)
        color = GREEN if error < 0.3 else RED

        result_text = Text(
            f"Output: {output_value:.2f} | Expected: {expected_output} | Error: {error:.2f}",
            font_size=28,
            color=color
        ).next_to(self.output_node, RIGHT, buff=0.5)

        self.play(Write(result_text))
        self.wait(1)
        self.play(FadeOut(result_text))


class TrainingVisualization(Scene):
    """Scene 2: Training with gradient descent and weight updates"""

    def construct(self):
        # Title
        title = Text("Neural Network Training: Gradient Descent", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create split view: Network on left, Loss curve on right
        self.create_split_view()

        # Training loop visualization
        epochs_to_show = [0, 1, 5, 10, 20, 50, 100]

        for target_epoch in epochs_to_show:
            # Train to target epoch
            while self.network.epoch < target_epoch:
                self.network.train_epoch()

            # Update visualization
            self.update_network_weights()
            self.update_loss_curve()

            # Show epoch label
            epoch_label = Text(
                f"Epoch: {self.network.epoch}",
                font_size=36,
                color=YELLOW
            ).to_edge(DOWN)

            if hasattr(self, 'current_epoch_label'):
                self.play(Transform(self.current_epoch_label, epoch_label))
            else:
                self.current_epoch_label = epoch_label
                self.play(Write(epoch_label))

            self.wait(0.5)

        # Final message
        final_text = Text(
            "Network trained successfully!",
            font_size=40,
            color=GREEN
        ).to_edge(DOWN)
        self.play(Transform(self.current_epoch_label, final_text))
        self.wait(2)

        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def create_split_view(self):
        """Create split view with network and loss curve"""
        # Initialize network
        self.network = XORNetwork()

        # Network view (left side)
        self.create_simple_network()
        self.network_group = VGroup(self.simple_nodes, self.simple_edges)
        self.network_group.scale(0.6).shift(LEFT * 3.5)

        self.play(Create(self.network_group))

        # Loss curve axes (right side)
        self.loss_axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 1, 0.2],
            x_length=5,
            y_length=3,
            axis_config={"color": BLUE},
            tips=False
        ).shift(RIGHT * 3)

        self.loss_axes_labels = self.loss_axes.get_axis_labels(
            x_label="Epoch",
            y_label="Loss"
        )

        self.play(Create(self.loss_axes), Write(self.loss_axes_labels))

        # Initialize loss curve
        self.loss_curve = VMobject(color=YELLOW, stroke_width=3)
        self.loss_points = []

    def create_simple_network(self):
        """Create simplified network visualization"""
        # Simplified positions
        input_x, hidden_x, output_x = -2, 0, 2

        # Input nodes
        self.simple_input = VGroup()
        for i in range(2):
            y = 1 - i * 2
            node = Circle(radius=0.3, fill_opacity=0.8, color=BLUE)
            node.move_to([input_x, y, 0])
            self.simple_input.add(node)

        # Hidden nodes
        self.simple_hidden = VGroup()
        for i in range(3):
            y = 1.5 - i * 1.5
            node = Circle(radius=0.3, fill_opacity=0.8, color=GREEN)
            node.move_to([hidden_x, y, 0])
            self.simple_hidden.add(node)

        # Output node
        self.simple_output = Circle(radius=0.3, fill_opacity=0.8, color=RED)
        self.simple_output.move_to([output_x, 0, 0])

        self.simple_nodes = VGroup(self.simple_input, self.simple_hidden, self.simple_output)

        # Connections
        self.simple_edges = VGroup()
        for input_node in self.simple_input:
            for hidden_node in self.simple_hidden:
                line = Line(input_node.get_center(), hidden_node.get_center(), stroke_width=2, color=GRAY)
                self.simple_edges.add(line)

        for hidden_node in self.simple_hidden:
            line = Line(hidden_node.get_center(), self.simple_output.get_center(), stroke_width=2, color=GRAY)
            self.simple_edges.add(line)

    def update_network_weights(self):
        """Update network visualization with new weights"""
        # Flash to indicate update
        self.play(
            self.network_group.animate.set_opacity(0.5),
            run_time=0.2
        )
        self.play(
            self.network_group.animate.set_opacity(1.0),
            run_time=0.2
        )

    def update_loss_curve(self):
        """Update loss curve with new data point"""
        if len(self.network.loss_history) == 0:
            return

        # Add new point
        epoch = self.network.epoch
        loss = self.network.loss_history[-1]

        point = self.loss_axes.coords_to_point(epoch, loss)
        self.loss_points.append(point)

        # Update curve
        if len(self.loss_points) > 1:
            new_curve = VMobject(color=YELLOW, stroke_width=3)
            new_curve.set_points_as_corners(self.loss_points)

            if hasattr(self, 'loss_curve') and len(self.loss_curve.points) > 0:
                self.play(
                    Transform(self.loss_curve, new_curve),
                    run_time=0.3
                )
            else:
                self.loss_curve = new_curve
                self.add(self.loss_curve)

        # Add dot at current point
        dot = Dot(point, color=RED, radius=0.05)
        self.play(FadeIn(dot), run_time=0.2)


class DecisionBoundaryEvolution(Scene):
    """Scene 3: Decision boundary morphing during training"""

    def construct(self):
        # Title
        title = Text("Decision Boundary Evolution", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create axes
        self.axes = Axes(
            x_range=[-0.5, 1.5, 0.5],
            y_range=[-0.5, 1.5, 0.5],
            x_length=6,
            y_length=6,
            axis_config={"color": BLUE},
        )
        self.axes_labels = self.axes.get_axis_labels(x_label="Input 0", y_label="Input 1")

        self.play(Create(self.axes), Write(self.axes_labels))

        # Plot XOR training points
        xor_points = VGroup()
        xor_data = [
            ([0, 0], 0, RED),
            ([0, 1], 1, GREEN),
            ([1, 0], 1, GREEN),
            ([1, 1], 0, RED)
        ]

        for (x, y), label, color in xor_data:
            point_pos = self.axes.coords_to_point(x, y)
            point = Dot(point_pos, radius=0.15, color=color, fill_opacity=1)

            # Add label
            text = Text(f"{x}⊕{y}={label}", font_size=20, color=WHITE)
            text.next_to(point, UP, buff=0.1)

            xor_points.add(point, text)

        self.play(Create(xor_points))
        self.wait(0.5)

        # Initialize network
        self.network = XORNetwork()

        # Training epochs to visualize
        epochs = [0, 5, 10, 20, 50, 100, 200]

        for i, target_epoch in enumerate(epochs):
            # Train to target epoch
            while self.network.epoch < target_epoch:
                self.network.train_epoch()

            # Create decision boundary surface
            boundary = self.create_decision_boundary()

            if i == 0:
                self.current_boundary = boundary
                self.play(FadeIn(boundary))
            else:
                # Morph boundary
                self.play(
                    Transform(self.current_boundary, boundary),
                    run_time=1.5
                )

            # Show epoch label
            epoch_text = Text(
                f"Epoch: {self.network.epoch} | Loss: {self.network.loss_history[-1]:.4f}",
                font_size=28,
                color=YELLOW
            ).to_edge(DOWN)

            if hasattr(self, 'epoch_label'):
                self.play(Transform(self.epoch_label, epoch_text), run_time=0.3)
            else:
                self.epoch_label = epoch_text
                self.play(Write(epoch_text))

            self.wait(0.5)

        # Final message
        final_text = Text(
            "Perfect XOR boundary learned!",
            font_size=36,
            color=GREEN
        ).to_edge(DOWN)
        self.play(Transform(self.epoch_label, final_text))
        self.wait(2)

        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def create_decision_boundary(self):
        """Create decision boundary visualization"""
        # Create mesh of points
        resolution = 30
        x_vals = np.linspace(-0.5, 1.5, resolution)
        y_vals = np.linspace(-0.5, 1.5, resolution)

        # Create colored squares based on prediction
        boundary_group = VGroup()

        for i in range(resolution - 1):
            for j in range(resolution - 1):
                x = x_vals[i]
                y = y_vals[j]

                # Get prediction
                pred = self.network.predict(np.array([[x, y]]))[0, 0]

                # Create colored square
                color = interpolate_color(RED, GREEN, pred)

                # Get corners in axes coordinates
                p1 = self.axes.coords_to_point(x_vals[i], y_vals[j])
                p2 = self.axes.coords_to_point(x_vals[i+1], y_vals[j])
                p3 = self.axes.coords_to_point(x_vals[i+1], y_vals[j+1])
                p4 = self.axes.coords_to_point(x_vals[i], y_vals[j+1])

                square = Polygon(p1, p2, p3, p4, fill_color=color, fill_opacity=0.5, stroke_width=0)
                boundary_group.add(square)

        return boundary_group


class CompleteOverview(Scene):
    """Scene 4: Complete overview with all visualizations"""

    def construct(self):
        # Title
        title = Text("XOR Neural Network: Complete Training Overview", font_size=42, color=BLUE)
        title.to_edge(UP, buff=0.2)
        self.play(Write(title))
        self.wait(0.5)

        # Create three panels: Network, Boundary, Loss
        self.create_three_panel_view()

        # Training loop
        epochs_to_show = [0, 10, 20, 50, 100, 200]

        for target_epoch in epochs_to_show:
            while self.network.epoch < target_epoch:
                self.network.train_epoch()

            # Update all panels
            self.update_all_panels()

            # Show epoch
            epoch_text = Text(
                f"Epoch: {self.network.epoch}",
                font_size=32,
                color=YELLOW
            ).to_edge(DOWN)

            if hasattr(self, 'epoch_label'):
                self.play(Transform(self.epoch_label, epoch_text), run_time=0.3)
            else:
                self.epoch_label = epoch_text
                self.play(Write(epoch_text))

            self.wait(0.5)

        # Final celebration
        final_text = Text(
            "Training Complete! ✓",
            font_size=48,
            color=GREEN,
            weight=BOLD
        ).to_edge(DOWN)
        self.play(
            Transform(self.epoch_label, final_text),
            Flash(self.epoch_label.get_center(), color=GREEN, line_length=1.0, num_lines=20)
        )
        self.wait(3)

        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def create_three_panel_view(self):
        """Create three panels for network, boundary, and loss"""
        self.network = XORNetwork()

        # Panel 1: Network (top left)
        self.create_mini_network()
        self.mini_network.scale(0.4).move_to([-4, 1.5, 0])
        self.play(Create(self.mini_network))

        network_label = Text("Network", font_size=24, color=GRAY)
        network_label.next_to(self.mini_network, UP, buff=0.2)
        self.play(Write(network_label))

        # Panel 2: Decision Boundary (top right)
        self.boundary_axes = Axes(
            x_range=[-0.5, 1.5, 0.5],
            y_range=[-0.5, 1.5, 0.5],
            x_length=3,
            y_length=3,
            axis_config={"color": BLUE, "include_tip": False},
        ).move_to([3, 1.5, 0])

        self.play(Create(self.boundary_axes))

        boundary_label = Text("Decision Boundary", font_size=24, color=GRAY)
        boundary_label.next_to(self.boundary_axes, UP, buff=0.2)
        self.play(Write(boundary_label))

        # Add XOR points
        xor_points = VGroup()
        for (x, y), label, color in [([0, 0], 0, RED), ([0, 1], 1, GREEN), ([1, 0], 1, GREEN), ([1, 1], 0, RED)]:
            point_pos = self.boundary_axes.coords_to_point(x, y)
            point = Dot(point_pos, radius=0.08, color=color)
            xor_points.add(point)
        self.play(Create(xor_points))

        # Panel 3: Loss Curve (bottom)
        self.loss_axes = Axes(
            x_range=[0, 200, 50],
            y_range=[0, 1, 0.25],
            x_length=7,
            y_length=2,
            axis_config={"color": BLUE},
        ).move_to([0, -2, 0])

        self.loss_axes_labels = self.loss_axes.get_axis_labels(x_label="Epoch", y_label="Loss")
        self.play(Create(self.loss_axes), Write(self.loss_axes_labels))

        loss_label = Text("Training Loss", font_size=24, color=GRAY)
        loss_label.next_to(self.loss_axes, UP, buff=0.1)
        self.play(Write(loss_label))

        # Initialize tracking
        self.loss_points = []
        self.loss_curve = VMobject(color=YELLOW, stroke_width=2)

    def create_mini_network(self):
        """Create miniature network"""
        self.mini_network = VGroup()

        # Simplified network
        input_x, hidden_x, output_x = -1.5, 0, 1.5

        # Nodes
        input_nodes = VGroup()
        for i in range(2):
            y = 0.5 - i
            node = Circle(radius=0.2, fill_opacity=0.8, color=BLUE)
            node.move_to([input_x, y, 0])
            input_nodes.add(node)

        hidden_nodes = VGroup()
        for i in range(3):
            y = 0.7 - i * 0.7
            node = Circle(radius=0.2, fill_opacity=0.8, color=GREEN)
            node.move_to([hidden_x, y, 0])
            hidden_nodes.add(node)

        output_node = Circle(radius=0.2, fill_opacity=0.8, color=RED)
        output_node.move_to([output_x, 0, 0])

        # Connections
        edges = VGroup()
        for inp in input_nodes:
            for hid in hidden_nodes:
                edges.add(Line(inp.get_center(), hid.get_center(), stroke_width=1, color=GRAY))
        for hid in hidden_nodes:
            edges.add(Line(hid.get_center(), output_node.get_center(), stroke_width=1, color=GRAY))

        self.mini_network.add(edges, input_nodes, hidden_nodes, output_node)

    def update_all_panels(self):
        """Update all three panels"""
        # Flash network
        self.play(Indicate(self.mini_network, scale_factor=1.1), run_time=0.3)

        # Update decision boundary
        if self.network.epoch > 0:
            boundary = self.create_mini_decision_boundary()
            if hasattr(self, 'current_mini_boundary'):
                self.play(Transform(self.current_mini_boundary, boundary), run_time=0.5)
            else:
                self.current_mini_boundary = boundary
                self.play(FadeIn(boundary))

        # Update loss curve
        if len(self.network.loss_history) > 0:
            epoch = self.network.epoch
            loss = self.network.loss_history[-1]
            point = self.loss_axes.coords_to_point(epoch, loss)
            self.loss_points.append(point)

            if len(self.loss_points) > 1:
                new_curve = VMobject(color=YELLOW, stroke_width=2)
                new_curve.set_points_as_corners(self.loss_points)

                if len(self.loss_curve.points) > 0:
                    self.play(Transform(self.loss_curve, new_curve), run_time=0.3)
                else:
                    self.loss_curve = new_curve
                    self.add(self.loss_curve)

    def create_mini_decision_boundary(self):
        """Create miniature decision boundary"""
        resolution = 20
        x_vals = np.linspace(-0.5, 1.5, resolution)
        y_vals = np.linspace(-0.5, 1.5, resolution)

        boundary_group = VGroup()

        for i in range(resolution - 1):
            for j in range(resolution - 1):
                x, y = x_vals[i], y_vals[j]
                pred = self.network.predict(np.array([[x, y]]))[0, 0]
                color = interpolate_color(RED, GREEN, pred)

                p1 = self.boundary_axes.coords_to_point(x_vals[i], y_vals[j])
                p2 = self.boundary_axes.coords_to_point(x_vals[i+1], y_vals[j])
                p3 = self.boundary_axes.coords_to_point(x_vals[i+1], y_vals[j+1])
                p4 = self.boundary_axes.coords_to_point(x_vals[i], y_vals[j+1])

                square = Polygon(p1, p2, p3, p4, fill_color=color, fill_opacity=0.6, stroke_width=0)
                boundary_group.add(square)

        return boundary_group


# CLI helper for rendering
if __name__ == "__main__":
    print("=" * 80)
    print("MANIM XOR NEURAL NETWORK VISUALIZATION")
    print("=" * 80)
    print("\nAvailable scenes:")
    print("  1. ForwardPropagation      - Data flowing through network")
    print("  2. TrainingVisualization   - Gradient descent animation")
    print("  3. DecisionBoundaryEvolution - Boundary morphing")
    print("  4. CompleteOverview        - All visualizations combined")
    print("\nRender commands:")
    print("  Low quality  (preview):  manim -pql manim_neural_network.py <SceneName>")
    print("  High quality (720p):     manim -pqh manim_neural_network.py <SceneName>")
    print("  4K quality   (2160p):    manim -pqk manim_neural_network.py <SceneName>")
    print("\nExample:")
    print("  manim -pqh manim_neural_network.py ForwardPropagation")
    print("=" * 80)
