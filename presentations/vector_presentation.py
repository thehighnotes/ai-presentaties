"""
Vector Visualization Presentation
2D/3D vector space exploration with semantic embeddings
Integrated with BasePresentation for standardized controls
"""

import sys
import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from mpl_toolkits.mplot3d import proj3d, Axes3D
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import BasePresentation, PresentationStyle


class Arrow3D(FancyArrowPatch):
    """Custom 3D arrow for visualization"""
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs)


class VectorPresentation(BasePresentation):
    """Vector visualization with 2D/3D transformations"""

    def __init__(self):
        """Initialize vector presentation"""
        step_names = [
            'Landing',
            '2D to 3D Vector Space',
            'Semantic Space',
            'Vector Arithmetic',
            'Real Embedding'
        ]

        super().__init__("Vector Exploration", step_names)

        # Vector data
        self.vector_x = 3.5
        self.vector_y = 2.8
        self.vector_z = 4.2

        # Semantic vectors
        self.semantic_vectors = {
            'Hond': np.array([3.2, 2.9, 1.5]),
            'Kat': np.array([3.0, 2.7, 1.3]),
            'Paard': np.array([3.5, 3.2, 1.8]),
            'Auto': np.array([-2.5, 1.0, 3.0]),
            'Fiets': np.array([-2.0, 0.8, 2.5]),
            'Vliegtuig': np.array([-3.0, 1.5, 4.0]),
        }

        # Vector arithmetic
        self.koning = np.array([2.0, 4.0, 2.5])
        self.man = np.array([1.5, 2.0, 1.0])
        self.vrouw = np.array([1.0, 2.5, 1.2])
        self.koningin = self.koning - self.man + self.vrouw

        # Real embedding (truncated for simplicity)
        self.real_embedding_preview = np.array([
            -0.0234, 0.0891, -0.0456, 0.1203, -0.0789, 0.0567,
            -0.0345, 0.0923, 0.0678, -0.0412, 0.0856, -0.0234
        ])

        # Camera settings
        self.camera_elev = 20
        self.camera_azim = 45

        self.show_landing_page()

    def get_frames_for_step(self, step: int) -> int:
        """Custom frame counts per step"""
        frames = {
            -1: 30,   # Landing page
            0: 120,   # 2D to 3D transition (longer for seamless animation)
            1: 90,    # Semantic space
            2: 100,   # Vector arithmetic
            3: 80     # Real embedding
        }
        return frames.get(step, 60)

    def show_landing_page(self):
        """Display vector landing page"""
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
            edgecolor=self.colors['vector'],
            linewidth=4,
            alpha=0.95
        )
        ax.add_patch(title_box)

        ax.text(50, 72, 'Vector Exploration',
                fontsize=72, fontweight='bold', ha='center', va='center',
                color=self.colors['vector'])

        ax.text(50, 64, 'Van 2D naar Semantische Ruimte',
                fontsize=33, ha='center', va='center',
                color=self.colors['text'], alpha=0.8, style='italic')

        ax.text(50, 45, 'Ontdek hoe AI betekenis vastlegt in vectoren',
                fontsize=27, ha='center', va='center',
                color=self.colors['secondary'], alpha=0.9)

        # Instructions box
        instr_box = FancyBboxPatch(
            (25, 15), 50, 15,
            boxstyle="round,pad=1",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['secondary'],
            linewidth=3,
            alpha=0.9
        )
        ax.add_patch(instr_box)

        ax.text(50, 25, '* Druk op SPATIE om te beginnen *',
                fontsize=30, ha='center', va='center',
                color=self.colors['secondary'], fontweight='bold')

        ax.text(50, 20, 'SPACE=Volgende | B=Vorige | S=Menu | R=Reset | Q=Quit',
                fontsize=18, ha='center', va='center',
                color=self.colors['dim'], style='italic')

        ax.text(50, 5, 'Interactieve visualisatie van vector embeddings',
                fontsize=18, ha='center', va='center',
                color=self.colors['text'], alpha=0.5)

        plt.tight_layout()

    def animate_step(self, frame: int):
        """Animate current step"""
        total_frames = self.get_frames_for_step(self.current_step)
        progress = frame / (total_frames - 1) if total_frames > 1 else 1

        if self.current_step == 0:
            self.draw_2d_vector_space(progress)
        elif self.current_step == 1:
            self.draw_semantic_space(progress)
        elif self.current_step == 2:
            self.draw_vector_arithmetic(progress)
        elif self.current_step == 3:
            self.draw_real_embedding(progress)

        if frame >= total_frames - 1:
            self.is_animating = False

    def draw_current_step_static(self):
        """Draw current step without animation"""
        if self.current_step == -1:
            self.show_landing_page()
        elif self.current_step == 0:
            self.draw_2d_vector_space(1.0)
        elif self.current_step == 1:
            self.draw_semantic_space(1.0)
        elif self.current_step == 2:
            self.draw_vector_arithmetic(1.0)
        elif self.current_step == 3:
            self.draw_real_embedding(1.0)
        plt.draw()

    def draw_2d_vector_space(self, progress):
        """Step 0: 2D vector visualization - seamlessly transitions to 3D at the end"""
        # Determine if we should show 3D (last 30% of animation)
        use_3d = progress > 0.7
        transition_progress = 0 if not use_3d else (progress - 0.7) / 0.3

        self.fig.clear()

        if use_3d:
            # Seamless transition to 3D
            ax = self.fig.add_subplot(111, projection='3d')

            # Setup 3D with SAME limits as 2D
            ax.set_xlim(-1, 6)
            ax.set_ylim(-1, 6)
            ax.set_zlim(0, 6)  # Z starts at 0

            # Camera rotation - start EXACTLY from top-down (like 2D), rotate to 3D view
            # At elev=90, azim=-90, the 3D view looks exactly like 2D (X right, Y up)
            elev = 90 - (transition_progress * 70)  # 90° (perfectly top-down) -> 20° (3D view)
            azim = -90 + (transition_progress * 135)  # -90° (2D alignment) -> 45° (3D angle)
            ax.view_init(elev=elev, azim=azim)

            # Style 3D axes - but keep them minimal at first
            PresentationStyle.setup_3d_axis(ax)

            # Show grid on Z=0 plane to match 2D grid
            if transition_progress < 0.3:
                # Draw grid lines on the ground plane to match 2D
                for i in range(-1, 7):
                    ax.plot([i, i], [-1, 6], [0, 0], color=self.colors['grid'],
                           alpha=0.3 * (1 - transition_progress * 3), linewidth=1)
                    ax.plot([-1, 6], [i, i], [0, 0], color=self.colors['grid'],
                           alpha=0.3 * (1 - transition_progress * 3), linewidth=1)

            # Axes - X and Y always visible, Z fades in
            ax.set_xlabel('X', fontsize=21, color=self.colors['text'])
            ax.set_ylabel('Y', fontsize=21, color=self.colors['text'])
            ax.set_zlabel('Z', fontsize=21, color=self.colors['text'], alpha=min(1.0, transition_progress * 2))

            # Axis lines on the ground (Z=0) to match 2D
            if transition_progress < 0.5:
                axis_alpha = 0.7 * (1 - transition_progress * 2)
                ax.plot([-1, 6], [0, 0], [0, 0], color=self.colors['axis'],
                       linewidth=2, alpha=axis_alpha)
                ax.plot([0, 0], [-1, 6], [0, 0], color=self.colors['axis'],
                       linewidth=2, alpha=axis_alpha)

            # Title transitions
            if transition_progress < 0.4:
                title = 'Stap 1: 2D Vector Space'
                title_color = self.colors['primary']
            else:
                title = 'Stap 1: 2D → 3D'
                title_color = self.colors['secondary']

            self.fig.suptitle(title, fontsize=36, fontweight='bold', color=title_color)

            # Draw the vector in 3D with growing Z component
            z_height = self.vector_z * transition_progress

            arrow = Arrow3D([0, self.vector_x], [0, self.vector_y], [0, z_height],
                          mutation_scale=20, linewidth=3,
                          arrowstyle='-|>', color=self.colors['vector'])
            ax.add_artist(arrow)

            # Start point
            ax.scatter([0], [0], [0], color=self.colors['vector'], s=200)
            # End point
            ax.scatter([self.vector_x], [self.vector_y], [z_height],
                      color=self.colors['vector'], s=200)

            # Ground projection becomes visible during transition
            if transition_progress > 0.3:
                proj_alpha = min(1.0, (transition_progress - 0.3) / 0.4)
                ax.plot([0, self.vector_x], [0, self.vector_y], [0, 0],
                       'o-', color=self.colors['projection'],
                       linewidth=2, markersize=6, alpha=proj_alpha * 0.5,
                       linestyle='--')
                # Vertical line from ground to vector tip
                ax.plot([self.vector_x, self.vector_x], [self.vector_y, self.vector_y],
                       [0, z_height],
                       color=self.colors['projection'], linewidth=1,
                       alpha=proj_alpha * 0.3, linestyle=':')

            # Label updates with Z coordinate
            label_text = f'v = ({self.vector_x:.1f}, {self.vector_y:.1f}, {z_height:.1f})'
            # Position label in 3D space
            ax.text(self.vector_x + 0.5, self.vector_y + 0.5, z_height + 0.5,
                   label_text,
                   fontsize=21, color=self.colors['vector'],
                   fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5',
                            facecolor=self.colors['bg_light'],
                            edgecolor=self.colors['vector'],
                            linewidth=2))

        else:
            # 2D view (first 70% of animation)
            ax = self.fig.add_subplot(111)
            ax.set_xlim(-1, 6)
            ax.set_ylim(-1, 6)
            ax.set_aspect('equal')
            ax.grid(True, alpha=0.3, color=self.colors['grid'])
            ax.set_facecolor(self.colors['bg_light'])

            # Title
            ax.text(2.5, 5.5, 'Stap 1: 2D Vector Space',
                    fontsize=36, fontweight='bold', ha='center',
                    color=self.colors['primary'])

            # Axes
            ax.axhline(y=0, color=self.colors['axis'], linewidth=2, alpha=0.7)
            ax.axvline(x=0, color=self.colors['axis'], linewidth=2, alpha=0.7)

            ax.set_xlabel('X', fontsize=21, color=self.colors['text'])
            ax.set_ylabel('Y', fontsize=21, color=self.colors['text'])
            ax.tick_params(colors=self.colors['text'])

            # Vector appears
            if progress > 0.2:
                vec_progress = min(1.0, (progress - 0.2) / 0.4)
                curr_x = self.vector_x * vec_progress
                curr_y = self.vector_y * vec_progress

                ax.arrow(0, 0, curr_x, curr_y,
                        head_width=0.3, head_length=0.3,
                        fc=self.colors['vector'], ec=self.colors['vector'],
                        linewidth=3, alpha=0.8, length_includes_head=True)

                ax.plot([0, curr_x], [0, curr_y], 'o',
                       color=self.colors['vector'], markersize=10)

            # Label in 2D
            if progress > 0.5:
                label_alpha = min(1.0, (progress - 0.5) / 0.2)
                ax.text(self.vector_x + 0.3, self.vector_y + 0.3,
                       f'v = ({self.vector_x:.1f}, {self.vector_y:.1f})',
                       fontsize=21, color=self.colors['vector'],
                       fontweight='bold', alpha=label_alpha,
                       bbox=dict(boxstyle='round,pad=0.5',
                                facecolor=self.colors['bg_light'],
                                edgecolor=self.colors['vector'],
                                linewidth=2))

        plt.tight_layout()

    def draw_semantic_space(self, progress):
        """Step 1: Semantic space visualization"""
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection='3d')

        ax.set_xlim(-4, 4)
        ax.set_ylim(-1, 5)
        ax.set_zlim(0, 5)
        ax.view_init(elev=25, azim=45 + progress * 90)

        PresentationStyle.setup_3d_axis(ax)

        self.fig.suptitle('Stap 2: Semantische Ruimte',
                         fontsize=36, fontweight='bold',
                         color=self.colors['highlight'])

        # Categories
        animals = ['Hond', 'Kat', 'Paard']
        vehicles = ['Auto', 'Fiets', 'Vliegtuig']

        # Draw animals (green)
        for i, name in enumerate(animals):
            if progress > i * 0.15:
                vec = self.semantic_vectors[name]
                alpha = min(1.0, (progress - i * 0.15) / 0.15)

                arrow = Arrow3D([0, vec[0]], [0, vec[1]], [0, vec[2]],
                              mutation_scale=15, linewidth=2,
                              arrowstyle='-|>', color=self.colors['correct'],
                              alpha=alpha)
                ax.add_artist(arrow)

                ax.text(vec[0], vec[1], vec[2] + 0.3, name,
                       fontsize=16, color=self.colors['correct'],
                       fontweight='bold', alpha=alpha)

        # Draw vehicles (orange)
        for i, name in enumerate(vehicles):
            if progress > 0.5 + i * 0.15:
                vec = self.semantic_vectors[name]
                alpha = min(1.0, (progress - (0.5 + i * 0.15)) / 0.15)

                arrow = Arrow3D([0, vec[0]], [0, vec[1]], [0, vec[2]],
                              mutation_scale=15, linewidth=2,
                              arrowstyle='-|>', color=self.colors['accent'],
                              alpha=alpha)
                ax.add_artist(arrow)

                ax.text(vec[0], vec[1], vec[2] + 0.3, name,
                       fontsize=16, color=self.colors['accent'],
                       fontweight='bold', alpha=alpha)

        plt.tight_layout()

    def draw_vector_arithmetic(self, progress):
        """Step 2: Vector arithmetic with improved label positioning"""
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection='3d')

        ax.set_xlim(-1, 4)
        ax.set_ylim(0, 5)
        ax.set_zlim(0, 4)
        ax.view_init(elev=20, azim=45)

        PresentationStyle.setup_3d_axis(ax)

        self.fig.suptitle('Stap 3: Vector Rekenen',
                         fontsize=36, fontweight='bold',
                         color=self.colors['primary'])

        # Koning - label positioned to the right with dotted line
        if progress > 0.15:
            alpha = min(1.0, (progress - 0.15) / 0.15)
            arrow = Arrow3D([0, self.koning[0]], [0, self.koning[1]], [0, self.koning[2]],
                          mutation_scale=15, linewidth=3,
                          arrowstyle='-|>', color=self.colors['primary'],
                          alpha=alpha)
            ax.add_artist(arrow)

            # Vector endpoint
            vec_end = [self.koning[0], self.koning[1], self.koning[2]]
            # Label position - offset to the right and up
            label_pos = [vec_end[0] + 1.2, vec_end[1] + 0.5, vec_end[2] + 0.8]

            # Dotted connection line from vector tip to label
            ax.plot([vec_end[0], label_pos[0]],
                   [vec_end[1], label_pos[1]],
                   [vec_end[2], label_pos[2]],
                   linestyle=':', linewidth=2, color=self.colors['primary'],
                   alpha=alpha * 0.6)

            ax.text(label_pos[0], label_pos[1], label_pos[2], 'Koning',
                   fontsize=21, color=self.colors['primary'],
                   fontweight='bold', alpha=alpha,
                   bbox=dict(boxstyle='round,pad=0.5',
                            facecolor=self.colors['bg_light'],
                            edgecolor=self.colors['primary'],
                            linewidth=2, alpha=0.9))

        # Man (subtract) - label positioned below left
        if progress > 0.35:
            alpha = min(1.0, (progress - 0.35) / 0.15)
            arrow = Arrow3D([0, self.man[0]], [0, self.man[1]], [0, self.man[2]],
                          mutation_scale=15, linewidth=2,
                          arrowstyle='-|>', color=self.colors['warning'],
                          alpha=alpha, linestyle='--')
            ax.add_artist(arrow)

            # Vector endpoint
            vec_end = [self.man[0], self.man[1], self.man[2]]
            # Label position - offset down and left
            label_pos = [vec_end[0] - 0.8, vec_end[1] - 0.5, vec_end[2] - 0.6]

            # Dotted connection line
            ax.plot([vec_end[0], label_pos[0]],
                   [vec_end[1], label_pos[1]],
                   [vec_end[2], label_pos[2]],
                   linestyle=':', linewidth=2, color=self.colors['warning'],
                   alpha=alpha * 0.6)

            ax.text(label_pos[0], label_pos[1], label_pos[2], 'Man (-)',
                   fontsize=19, color=self.colors['warning'],
                   fontweight='bold', alpha=alpha,
                   bbox=dict(boxstyle='round,pad=0.5',
                            facecolor=self.colors['bg_light'],
                            edgecolor=self.colors['warning'],
                            linewidth=2, alpha=0.9))

        # Vrouw (add) - label positioned to the left and up
        if progress > 0.55:
            alpha = min(1.0, (progress - 0.55) / 0.15)
            arrow = Arrow3D([0, self.vrouw[0]], [0, self.vrouw[1]], [0, self.vrouw[2]],
                          mutation_scale=15, linewidth=2,
                          arrowstyle='-|>', color=self.colors['secondary'],
                          alpha=alpha)
            ax.add_artist(arrow)

            # Vector endpoint
            vec_end = [self.vrouw[0], self.vrouw[1], self.vrouw[2]]
            # Label position - offset left and up
            label_pos = [vec_end[0] - 1.0, vec_end[1] + 0.8, vec_end[2] + 0.5]

            # Dotted connection line
            ax.plot([vec_end[0], label_pos[0]],
                   [vec_end[1], label_pos[1]],
                   [vec_end[2], label_pos[2]],
                   linestyle=':', linewidth=2, color=self.colors['secondary'],
                   alpha=alpha * 0.6)

            ax.text(label_pos[0], label_pos[1], label_pos[2], 'Vrouw (+)',
                   fontsize=19, color=self.colors['secondary'],
                   fontweight='bold', alpha=alpha,
                   bbox=dict(boxstyle='round,pad=0.5',
                            facecolor=self.colors['bg_light'],
                            edgecolor=self.colors['secondary'],
                            linewidth=2, alpha=0.9))

        # Koningin (result) - label positioned prominently at top right
        if progress > 0.75:
            alpha = min(1.0, (progress - 0.75) / 0.25)
            arrow = Arrow3D([0, self.koningin[0]], [0, self.koningin[1]], [0, self.koningin[2]],
                          mutation_scale=20, linewidth=4,
                          arrowstyle='-|>', color=self.colors['highlight'],
                          alpha=alpha)
            ax.add_artist(arrow)

            # Vector endpoint
            vec_end = [self.koningin[0], self.koningin[1], self.koningin[2]]
            # Label position - offset to top right for prominence
            label_pos = [vec_end[0] + 0.8, vec_end[1] + 1.0, vec_end[2] + 0.8]

            # Dotted connection line (thicker for result)
            ax.plot([vec_end[0], label_pos[0]],
                   [vec_end[1], label_pos[1]],
                   [vec_end[2], label_pos[2]],
                   linestyle=':', linewidth=3, color=self.colors['highlight'],
                   alpha=alpha * 0.7)

            ax.text(label_pos[0], label_pos[1], label_pos[2], 'Koningin! *',
                   fontsize=22, color=self.colors['highlight'],
                   fontweight='bold', alpha=alpha,
                   bbox=dict(boxstyle='round,pad=0.6',
                            facecolor=self.colors['bg_light'],
                            edgecolor=self.colors['highlight'],
                            linewidth=3, alpha=0.95))

        # Add formula at the bottom for clarity
        if progress > 0.85:
            formula_alpha = min(1.0, (progress - 0.85) / 0.15)
            formula_text = 'Koning - Man + Vrouw = Koningin'
            self.fig.text(0.5, 0.08, formula_text,
                         fontsize=24, ha='center', va='center',
                         color=self.colors['text'],
                         fontweight='bold', alpha=formula_alpha,
                         bbox=dict(boxstyle='round,pad=0.8',
                                  facecolor=self.colors['bg_light'],
                                  edgecolor=self.colors['highlight'],
                                  linewidth=3, alpha=0.95))

        plt.tight_layout()

    def draw_real_embedding(self, progress):
        """Step 3: Real embedding visualization - showing actual 376-dimensional embedding"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Generate realistic embedding (376 dimensions to match common models)
        np.random.seed(42)
        full_embedding = np.random.randn(376) * 0.08  # Smaller variance for realism

        # Title with border
        if progress > 0.1:
            alpha = min(1.0, (progress - 0.1) / 0.2)

            # Title box
            title_box = FancyBboxPatch(
                (8, 83), 84, 14,
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=3,
                alpha=alpha * 0.95
            )
            ax.add_patch(title_box)

            ax.text(50, 90, 'De Realiteit: 376-Dimensionale Vector',
                    fontsize=36, fontweight='bold', ha='center',
                    color=self.colors['text'], alpha=alpha)

        # Subtitle
        if progress > 0.2:
            text_alpha = min(1.0, (progress - 0.2) / 0.15)
            ax.text(50, 80, 'Dit is een echte embedding van een modern AI model',
                    fontsize=18, ha='center',
                    color=self.colors['purple'], alpha=text_alpha * 0.9)

            ax.text(50, 76, '(OpenAI ada-002, Sentence Transformers, etc.)',
                    fontsize=15, ha='center', style='italic',
                    color=self.colors['dim'], alpha=text_alpha * 0.7)

        # Main embedding display box with actual values
        if progress > 0.35:
            box_alpha = min(1.0, (progress - 0.35) / 0.25)

            # Large box containing the embedding values
            embedding_box = FancyBboxPatch(
                (12, 13), 76, 58,
                boxstyle="round,pad=1.2",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=3,
                alpha=box_alpha * 0.95
            )
            ax.add_patch(embedding_box)

            # Format embedding values as text (show them in a grid format)
            # Display values in rows of 6 values each
            values_per_row = 6
            num_rows_to_show = 30  # Show first 180 values, then ellipsis

            embedding_text = ""
            for i in range(num_rows_to_show):
                row_values = []
                for j in range(values_per_row):
                    idx = i * values_per_row + j
                    if idx < len(full_embedding):
                        val = full_embedding[idx]
                        row_values.append(f"{val:7.4f}")

                embedding_text += ", ".join(row_values) + ",\n"

            # Add ellipsis for remaining values
            embedding_text += "  ...\n"

            # Add last row to show it continues
            last_row_start = len(full_embedding) - values_per_row
            last_row_values = [f"{full_embedding[i]:7.4f}"
                             for i in range(last_row_start, len(full_embedding))]
            embedding_text += ", ".join(last_row_values)

            # Display the embedding values
            ax.text(50, 43, embedding_text,
                    fontsize=9, ha='center', va='center',
                    color=self.colors['cyan'],
                    family='monospace',
                    alpha=box_alpha,
                    bbox=dict(boxstyle='round,pad=1.2',
                             facecolor=self.colors['bg'],
                             edgecolor=self.colors['grid'],
                             linewidth=1.5, alpha=0.8))

        # Statistics box at bottom
        if progress > 0.65:
            stats_alpha = min(1.0, (progress - 0.65) / 0.2)

            # Calculate actual statistics
            dim_count = len(full_embedding)
            min_val = np.min(full_embedding)
            max_val = np.max(full_embedding)
            mean_val = np.mean(full_embedding)

            stats_box = FancyBboxPatch(
                (10, 6), 80, 6,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg'],
                edgecolor=self.colors['text'],
                linewidth=2,
                alpha=stats_alpha * 0.9
            )
            ax.add_patch(stats_box)

            stats_text = f'Dimensies: {dim_count}   •   Min: {min_val:.4f}   •   Max: {max_val:.4f}   •   Mean: {mean_val:.4f}'
            ax.text(50, 9, stats_text,
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'],
                    fontweight='bold',
                    family='monospace',
                    alpha=stats_alpha)

        # Bottom note about model usage
        if progress > 0.8:
            note_alpha = min(1.0, (progress - 0.8) / 0.2)
            ax.text(50, 2, '[] Moderne modellen gebruiken 384, 768, 1536, of zelfs 4096 dimensies!',
                    fontsize=17, ha='center', va='center',
                    color=self.colors['purple'], style='italic',
                    alpha=note_alpha * 0.8)

        plt.tight_layout()


def main():
    """Main entry point"""
    print("="*80)
    print("VECTOR EXPLORATION VISUALIZATION")
    print("="*80)
    print("\n[#] Deze presentatie toont vector embeddings:")
    print("  1. 2D to 3D Vector Space - Seamless transformatie")
    print("  2. Semantische Ruimte - Woorden als vectoren")
    print("  3. Vector Rekenen - Koning - Man + Vrouw = Koningin")
    print("  4. Echte Embeddings - 384-dimensionale vectoren")
    print("\n[Keys]  Controls: SPACE=Next | B=Previous | R=Reset | S=Menu | Q=Quit")
    print("="*80 + "\n")

    presentation = VectorPresentation()
    presentation.show()


if __name__ == "__main__":
    main()
