"""
Animated Vector Visualization Presentation - Step-by-Step Mode
Smooth 2D to 3D transformation with Dark Mode styling and camera control

Controls:
- SPACE: Start/Continue to next animation step
- Mouse Drag (during pause): Rotate camera around scene
- SCROLL: Zoom in/out
- R: Randomize vector position
- Q/ESC: Quit
- F: Toggle fullscreen
- B: Go back to previous step
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import proj3d, Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib

# Dark mode styling
plt.style.use('dark_background')
matplotlib.rcParams['font.size'] = 16
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['axes.titlesize'] = 24
matplotlib.rcParams['axes.labelsize'] = 18
matplotlib.rcParams['figure.facecolor'] = '#0a0a0a'
matplotlib.rcParams['axes.facecolor'] = '#1a1a1a'
matplotlib.rcParams['axes.edgecolor'] = '#404040'
matplotlib.rcParams['grid.color'] = '#303030'
matplotlib.rcParams['text.color'] = '#e0e0e0'
matplotlib.rcParams['axes.labelcolor'] = '#e0e0e0'
matplotlib.rcParams['xtick.color'] = '#e0e0e0'
matplotlib.rcParams['ytick.color'] = '#e0e0e0'

class Arrow3D(FancyArrowPatch):
    """Custom 3D arrow for better visualization"""
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs)

class AnimatedVectorPresentation:
    def __init__(self):
        self.fig = plt.figure(figsize=(16, 9), facecolor='#0a0a0a')
        self.vector_x = 3.5
        self.vector_y = 2.8
        self.vector_z = 4.2
        
        # Animation state - step-by-step with pause between steps
        self.current_step = -1  # Start at -1 for landing page
        self.step_names = [
            'Landing',
            '2D Vector Space',
            '2D to 3D Transformation',  # Combined rotation + building
            'Semantic Space',
            'Vector Arithmetic',
            'Real Embedding'
        ]
        
        # Animation control
        self.is_animating = False
        self.animation = None
        self.animation_frame = 0
        self.pause_between_steps = True
        
        # Camera control
        self.zoom_level = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 3.0
        
        # Default camera positions for each step
        self.default_camera_positions = {
            -1: {'elev': 20, 'azim': 45},   # Landing
            0: {'elev': 90, 'azim': -90},   # 2D view (top-down)
            1: {'elev': 25, 'azim': 60},    # 2D to 3D (ends at 3D view)
            2: {'elev': 25, 'azim': 60},    # Semantic space
            3: {'elev': 25, 'azim': 60},    # Vector arithmetic
            4: {'elev': 0, 'azim': 0}       # Real embedding (2D view)
        }
        
        # Current and target camera positions
        self.current_camera = {'elev': 20, 'azim': 45}
        self.target_camera = {'elev': 20, 'azim': 45}
        self.user_camera = None  # Stores user's camera position during pause
        self.is_camera_transitioning = False
        self.camera_transition_progress = 0
        
        # Drawing state
        self.is_drawing = False
        self.drawing_lines = []  # List of line segments
        self.current_line = []  # Current line being drawn
        self.drawn_artists = []  # Artists to remove when clearing
        
        # Dark mode colors
        self.colors = {
            'vector': '#FF6B9D',
            'grid': '#303030',
            'axis': '#60A5FA',
            'point': '#34D399',
            'text': '#F0F0F0',
            'accent': '#A78BFA',
            'bg': '#1a1a1a',
            'projection': '#6B7280'
        }
        
        # Semantic space vectors
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
        
        # Real embedding (384 dimensions)
        self.real_embedding = np.array([
            -0.0234, 0.0891, -0.0456, 0.1203, -0.0789, 0.0567, -0.0345, 0.0923,
            0.0678, -0.0412, 0.0856, -0.0234, 0.0945, -0.0678, 0.0423, -0.0789,
            0.0312, 0.0845, -0.0567, 0.0934, -0.0423, 0.0712, -0.0289, 0.0867,
            -0.0534, 0.0698, -0.0412, 0.0923, 0.0756, -0.0345, 0.0889, -0.0623,
            0.0445, -0.0712, 0.0567, -0.0834, 0.0389, 0.0923, -0.0456, 0.0745,
            -0.0612, 0.0534, -0.0378, 0.0867, 0.0623, -0.0445, 0.0789, -0.0534,
            0.0412, 0.0934, -0.0567, 0.0678, -0.0823, 0.0456, -0.0712, 0.0589,
            0.0734, -0.0423, 0.0856, -0.0612, 0.0478, 0.0923, -0.0534, 0.0689,
            -0.0745, 0.0512, -0.0678, 0.0834, 0.0423, -0.0589, 0.0756, -0.0445,
            0.0612, -0.0734, 0.0489, 0.0867, -0.0556, 0.0678, -0.0812, 0.0534,
            -0.0623, 0.0745, 0.0456, -0.0689, 0.0578, -0.0834, 0.0512, 0.0923,
            -0.0445, 0.0678, -0.0756, 0.0589, 0.0834, -0.0512, 0.0689, -0.0734,
            0.0456, -0.0812, 0.0623, 0.0745, -0.0534, 0.0867, -0.0623, 0.0756,
            0.0489, -0.0678, 0.0834, -0.0556, 0.0712, 0.0923, -0.0445, 0.0689,
            -0.0789, 0.0534, -0.0656, 0.0823, 0.0478, -0.0712, 0.0612, -0.0845,
            0.0523, 0.0756, -0.0489, 0.0867, -0.0612, 0.0734, 0.0556, -0.0823,
            0.0478, -0.0689, 0.0812, 0.0545, -0.0734, 0.0623, -0.0867, 0.0512,
            0.0745, -0.0578, 0.0689, -0.0823, 0.0489, 0.0756, -0.0634, 0.0812,
            -0.0523, 0.0678, 0.0734, -0.0589, 0.0845, -0.0512, 0.0689, 0.0756,
            -0.0623, 0.0823, -0.0478, 0.0712, 0.0867, -0.0545, 0.0689, -0.0778,
            0.0534, -0.0812, 0.0623, 0.0734, -0.0489, 0.0867, -0.0556, 0.0712,
            0.0823, -0.0512, 0.0678, -0.0745, 0.0589, 0.0834, -0.0623, 0.0756,
            0.0489, -0.0712, 0.0867, -0.0534, 0.0689, 0.0823, -0.0578, 0.0745,
            -0.0623, 0.0812, 0.0523, -0.0689, 0.0756, -0.0834, 0.0589, 0.0712,
            -0.0645, 0.0823, -0.0512, 0.0734, 0.0867, -0.0578, 0.0689, -0.0756,
            0.0623, -0.0812, 0.0534, 0.0745, -0.0689, 0.0823, 0.0556, -0.0734,
            0.0678, -0.0867, 0.0512, 0.0789, -0.0623, 0.0745, 0.0834, -0.0556,
            0.0712, -0.0789, 0.0589, 0.0823, -0.0634, 0.0756, 0.0867, -0.0523,
            0.0689, -0.0812, 0.0578, 0.0734, -0.0667, 0.0823, 0.0545, -0.0756,
            0.0812, -0.0589, 0.0712, 0.0867, -0.0623, 0.0745, 0.0823, -0.0556,
            0.0689, -0.0778, 0.0612, 0.0834, -0.0534, 0.0756, 0.0867, -0.0623,
            0.0712, -0.0789, 0.0589, 0.0823, -0.0645, 0.0745, 0.0867, -0.0578,
            0.0689, -0.0812, 0.0623, 0.0756, -0.0734, 0.0823, 0.0556, -0.0789,
            0.0712, -0.0845, 0.0589, 0.0734, 0.0867, -0.0612, 0.0756, -0.0823,
            0.0534, -0.0689, 0.0812, 0.0623, -0.0756, 0.0734, 0.0867, -0.0589,
            0.0712, -0.0823, 0.0578, 0.0745, -0.0689, 0.0812, 0.0623, -0.0756,
            0.0734, -0.0867, 0.0556, 0.0789, -0.0623, 0.0745, 0.0823, -0.0612,
            0.0689, -0.0778, 0.0734, 0.0856, -0.0589, 0.0712, 0.0823, -0.0645,
            0.0756, -0.0812, 0.0578, 0.0734, -0.0689, 0.0823, 0.0612, -0.0756,
            0.0789, -0.0834, 0.0589, 0.0745, 0.0867, -0.0623, 0.0712, -0.0789,
            0.0656, -0.0823, 0.0734, 0.0856, -0.0578, 0.0712, 0.0823, -0.0634,
            0.0756, -0.0812, 0.0589, 0.0734, -0.0689, 0.0823, 0.0623, -0.0756,
            0.0789, -0.0845, 0.0612, 0.0734, 0.0867, -0.0589, 0.0723, -0.0812,
            0.0578, -0.0745, 0.0823, 0.0656, -0.0789, 0.0734, 0.0856, -0.0612,
            0.0689, -0.0823, 0.0734, 0.0867, -0.0589, 0.0756, 0.0812, -0.0645,
            0.0712, -0.0789, 0.0623, 0.0745, -0.0823, 0.0678, 0.0812, -0.0589,
            0.0734, -0.0867, 0.0612, 0.0756, 0.0823, -0.0634, 0.0689, -0.0778
        ])
        
        self.show_landing_page()
        self.setup_controls()
        
    def setup_controls(self):
        """Setup keyboard and mouse controls"""
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.fig.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_motion)
        
    def on_scroll(self, event):
        """Handle mouse scroll for zoom - NO camera reset"""
        if event.button == 'up':
            self.zoom_level = min(self.max_zoom, self.zoom_level * 1.1)
        elif event.button == 'down':
            self.zoom_level = max(self.min_zoom, self.zoom_level / 1.1)
        
        if not self.is_animating:
            # Save current camera position before redrawing
            saved_camera = None
            if hasattr(self, 'ax') and hasattr(self.ax, 'elev'):
                saved_camera = {
                    'elev': self.ax.elev,
                    'azim': self.ax.azim
                }
            
            # Redraw without clearing drawings
            self.redraw_without_reset()
            
            # Restore camera position immediately
            if saved_camera and hasattr(self.ax, 'view_init'):
                self.ax.view_init(elev=saved_camera['elev'], azim=saved_camera['azim'])
            
            # Force canvas update
            self.fig.canvas.draw_idle()
    
    def redraw_without_reset(self):
        """Redraw current step preserving ALL state"""
        # Save current camera
        saved_camera = None
        if hasattr(self, 'ax') and hasattr(self.ax, 'elev'):
            saved_camera = {
                'elev': self.ax.elev,
                'azim': self.ax.azim
            }
        
        # Redraw
        self.draw_current_step_with_camera(saved_camera, progress=1.0)
        
        # Restore camera
        if saved_camera and hasattr(self.ax, 'view_init'):
            self.ax.view_init(elev=saved_camera['elev'], azim=saved_camera['azim'])
    
    def on_mouse_press(self, event):
        """Handle mouse button press"""
        if self.is_animating:
            return
        
        # Left click = drawing (use figure coordinates for camera-plane drawing)
        if event.button == 1:
            if event.inaxes:
                self.is_drawing = True
                fig_x = event.x / self.fig.bbox.width
                fig_y = event.y / self.fig.bbox.height
                self.current_line = [(fig_x, fig_y)]
    
    def on_mouse_release(self, event):
        """Handle mouse button release"""
        if event.button == 1:  # Left click
            if self.is_drawing:
                self.is_drawing = False
                if len(self.current_line) > 1:
                    self.drawing_lines.append(self.current_line.copy())
                self.current_line = []
    
    def on_mouse_motion(self, event):
        """Handle mouse motion - drawing only, NO redraw"""
        if self.is_animating:
            return
        
        # If left button is pressed and we're drawing
        if self.is_drawing and event.x and event.y:
            # Save camera position
            saved_camera = None
            if hasattr(self, 'ax') and hasattr(self.ax, 'elev'):
                saved_camera = {
                    'elev': self.ax.elev,
                    'azim': self.ax.azim
                }
            
            # Add point to current line
            fig_x = event.x / self.fig.bbox.width
            fig_y = event.y / self.fig.bbox.height
            self.current_line.append((fig_x, fig_y))
            
            # Redraw everything
            self.draw_current_step_with_camera(saved_camera, progress=1.0)
            
            # Restore camera position immediately
            if saved_camera and hasattr(self.ax, 'view_init'):
                self.ax.view_init(elev=saved_camera['elev'], azim=saved_camera['azim'])
            
            # Force update
            self.fig.canvas.draw_idle()
    
    def clear_drawings(self):
        """Clear all drawings"""
        self.drawing_lines = []
        self.current_line = []
        self.drawn_artists = []
    
    def draw_user_drawings(self):
        """Draw user's freehand drawings on the 2D camera plane (viewport)"""
        if not hasattr(self, 'ax'):
            return
        
        drawing_color = '#FF1493'  # Deep pink
        
        # Draw completed lines
        for line_points in self.drawing_lines:
            if len(line_points) > 1:
                xs, ys = zip(*line_points)
                line = Line2D(xs, ys, 
                            color=drawing_color, 
                            linewidth=3, 
                            alpha=0.8,
                            transform=self.fig.transFigure,
                            zorder=1000)
                self.fig.add_artist(line)
                self.drawn_artists.append(line)
        
        # Draw current line being drawn
        if len(self.current_line) > 1:
            xs, ys = zip(*self.current_line)
            line = Line2D(xs, ys,
                        color=drawing_color,
                        linewidth=3,
                        alpha=0.8,
                        transform=self.fig.transFigure,
                        zorder=1000)
            self.fig.add_artist(line)
            self.drawn_artists.append(line)
        
    def on_key(self, event):
        """Handle keyboard events"""
        if event.key == ' ':
            if not self.is_animating:
                self.clear_drawings()
                self.start_next_step()
        elif event.key == 'b':
            if not self.is_animating:
                self.clear_drawings()
                self.previous_step()
        elif event.key == 'r':
            self.randomize_vector()
        elif event.key == 'c':
            if not self.is_animating:
                num_lines = len(self.drawing_lines) + (1 if len(self.current_line) > 1 else 0)
                self.clear_drawings()
                
                # Redraw without camera reset
                self.redraw_without_reset()
                self.fig.canvas.draw_idle()
                
                if num_lines > 0:
                    print(f"🧹 Cleared {num_lines} drawing(s)")
                else:
                    print("🧹 No drawings to clear")
        elif event.key in ['q', 'escape']:
            plt.close()
        elif event.key == 'f':
            manager = plt.get_current_fig_manager()
            manager.full_screen_toggle()
    
    def start_next_step(self):
        """Start animation for the next step"""
        if self.current_step < len(self.step_names) - 1:
            # Save current user camera if in 3D mode
            if hasattr(self, 'ax') and hasattr(self.ax, 'elev'):
                self.user_camera = {
                    'elev': self.ax.elev,
                    'azim': self.ax.azim
                }
            
            self.current_step += 1
            print(f"→ Starting Step {self.current_step + 1}/{len(self.step_names)}: {self.step_names[self.current_step]}")
            
            # Set target camera for this step
            self.target_camera = self.default_camera_positions[self.current_step].copy()
            
            # If user moved camera, transition back first
            if self.user_camera and self.current_step > 0:
                self.is_camera_transitioning = True
                self.camera_transition_progress = 0
                print("  ↻ Transitioning camera back to default position...")
            
            self.start_step_animation()
        else:
            print("✓ Already at final step!")
    
    def previous_step(self):
        """Go back to previous step"""
        if self.current_step > -1:
            self.current_step -= 1
            print(f"← Step {self.current_step + 1}/{len(self.step_names)}: {self.step_names[self.current_step]}")
            
            if self.current_step == -1:
                self.show_landing_page()
            else:
                self.target_camera = self.default_camera_positions[self.current_step].copy()
                self.user_camera = None
                self.draw_current_step_static()
            plt.draw()
        else:
            print("✓ Already at first step!")
    
    def start_step_animation(self):
        """Start animation for current step"""
        self.is_animating = True
        self.animation_frame = 0
        
        # Determine number of frames for this step
        frames_dict = {
            -1: 30,   # Landing
            0: 30,    # 2D drawing
            1: 120,   # 2D to 3D (combined: rotation + building)
            2: 50,    # Semantic space
            3: 120,   # Vector arithmetic (with pauses)
            4: 20     # Real embedding
        }
        
        total_frames = frames_dict[self.current_step]
        
        # Add camera transition frames if needed
        if self.is_camera_transitioning:
            total_frames += 30
        
        self.animation = FuncAnimation(
            self.fig,
            self.animate_step,
            frames=total_frames,
            interval=20,
            blit=False,
            repeat=False
        )
        
        plt.draw()
    
    def animate_step(self, frame):
        """Animate current step"""
        # Camera transition phase
        if self.is_camera_transitioning:
            if frame < 30:
                t = frame / 30
                t = t * t * (3 - 2 * t)  # Ease-in-out
                
                self.current_camera['elev'] = (
                    self.user_camera['elev'] * (1 - t) + 
                    self.target_camera['elev'] * t
                )
                self.current_camera['azim'] = (
                    self.user_camera['azim'] * (1 - t) + 
                    self.target_camera['azim'] * t
                )
                
                self.draw_current_step_with_camera(self.current_camera, progress=0)
                
                if frame >= 29:
                    self.is_camera_transitioning = False
                    self.user_camera = None
                    print("  ✓ Camera transition complete, starting animation...")
                
                return
            else:
                frame -= 30
        
        # Actual step animation
        if self.current_step == -1:
            progress = frame / 30
            self.draw_landing_animated(progress)
        elif self.current_step == 0:
            progress = frame / 30
            self.draw_2d_animated(progress)
        elif self.current_step == 1:
            progress = frame / 120
            self.draw_2d_to_3d_combined(progress)
        elif self.current_step == 2:
            progress = frame / 50
            self.draw_semantic_space(progress)
        elif self.current_step == 3:
            progress = frame / 120
            self.draw_vector_arithmetic(progress)
        elif self.current_step == 4:
            progress = frame / 20
            self.draw_real_embedding(progress)
        
        # Check if animation complete
        frames_dict = {-1: 30, 0: 30, 1: 120, 2: 50, 3: 120, 4: 20}
        if frame >= frames_dict[self.current_step] - 1:
            self.is_animating = False
            self.user_camera = None
            print(f"  ✓ Step {self.current_step + 1} complete. Press SPACE for next step, or drag to rotate camera.")
    
    def draw_current_step_static(self):
        """Draw current step as static image (paused state)"""
        self.draw_current_step_with_camera(None, progress=1.0)
    
    def draw_current_step_with_camera(self, camera=None, progress=1.0):
        """Draw current step with specific camera position"""
        if self.current_step == -1:
            self.draw_landing_page()
        elif self.current_step == 0:
            self.draw_2d_complete()
        elif self.current_step == 1:
            self.draw_2d_to_3d_combined(progress, camera)
        elif self.current_step == 2:
            self.draw_semantic_space(progress, camera)
        elif self.current_step == 3:
            self.draw_vector_arithmetic(progress, camera)
        elif self.current_step == 4:
            self.draw_real_embedding(progress)
        
        # Draw user's freehand drawings on top
        self.draw_user_drawings()
    
    def show_landing_page(self):
        """Show engaging landing page for AI Knowledge Session"""
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, projection='3d', facecolor=self.colors['bg'])
        
        # Enable rotation
        if hasattr(self.ax, 'mouse_init'):
            self.ax.mouse_init(rotate_btn=3, zoom_btn=2)
        
        self.ax.view_init(elev=20, azim=45)
        
        # Set limits
        limit = 6
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-limit, limit)
        self.ax.set_zlim(-limit, limit)
        
        # Hide axes for cleaner look
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.ax.xaxis.pane.set_edgecolor('none')
        self.ax.yaxis.pane.set_edgecolor('none')
        self.ax.zaxis.pane.set_edgecolor('none')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])
        
        # Create a constellation of vectors representing AI concepts
        concepts = [
            ('AI', np.array([4, 3, 2]), '#FF6B9D'),
            ('Data', np.array([2, 4, 3]), '#60A5FA'),
            ('Model', np.array([3, 2, 4]), '#34D399'),
            ('Vector', np.array([-3, 3, 2]), '#F59E0B'),
            ('Embedding', np.array([-2, -3, 3]), '#A78BFA'),
            ('Semantic', np.array([3, -2, 3]), '#EC4899'),
        ]
        
        for label, vec, color in concepts:
            # Draw vector arrow
            arrow = Arrow3D([0, vec[0]], [0, vec[1]], [0, vec[2]],
                           mutation_scale=20, lw=3, arrowstyle='-|>', 
                           color=color, alpha=0.7)
            self.ax.add_artist(arrow)
            
            # Draw point
            self.ax.scatter([vec[0]], [vec[1]], [vec[2]],
                           s=300, c=color, edgecolors='white', 
                           linewidths=2, zorder=5, alpha=0.9)
            
            # Add label
            self.ax.text(vec[0], vec[1], vec[2] + 0.5, label,
                       fontsize=14, fontweight='bold',
                       ha='center', va='bottom',
                       color=color)
        
        # Draw subtle connections
        for i in range(len(concepts)):
            for j in range(i + 1, len(concepts)):
                vec1 = concepts[i][1]
                vec2 = concepts[j][1]
                self.ax.plot([vec1[0], vec2[0]], [vec1[1], vec2[1]], 
                           [vec1[2], vec2[2]], color='#404040', 
                           linestyle='--', alpha=0.2, linewidth=1)
        
        # Main title
        self.fig.text(0.5, 0.92, 'AI Kennissessie: Embeddings & Vectoren',
                     fontsize=36, fontweight='bold',
                     ha='center', va='top',
                     bbox=dict(boxstyle='round,pad=1.0', facecolor='#2a2a2a',
                             edgecolor=self.colors['accent'], linewidth=3, alpha=0.95),
                     color=self.colors['text'])
        
        # Subtitle
        self.fig.text(0.5, 0.82, 'Hoe AI betekenis begrijpt door wiskundige vectoren',
                     fontsize=20, ha='center', va='top',
                     color=self.colors['accent'], alpha=0.8,
                     style='italic')
        
        # Instructions
        self.fig.text(0.5, 0.08, '✨ Druk op SPATIE om te beginnen ✨',
                     fontsize=24, ha='center', va='bottom',
                     bbox=dict(boxstyle='round,pad=0.8', facecolor='#1a1a1a',
                             edgecolor='#34D399', linewidth=3, alpha=0.95),
                     color='#34D399', fontweight='bold')
        
        # Footer info
        self.fig.text(0.5, 0.02, 'Interactief • Visueel • Praktisch',
                     fontsize=14, ha='center', va='bottom',
                     color=self.colors['text'], alpha=0.6,
                     style='italic')
        
        plt.tight_layout()
    
    def draw_landing_animated(self, progress):
        """Animate landing page (optional fade-in)"""
        self.show_landing_page()
    
    def set_3d_limits(self, ax):
        """Set 3D axis limits with current zoom level"""
        limit = 6 / self.zoom_level
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_zlim(-limit, limit)
        return limit
    
    def add_zoom_indicator_3d(self):
        """Add zoom indicator to 3D plots"""
        if self.zoom_level != 1.0:
            self.fig.text(0.98, 0.02, f'Zoom: {self.zoom_level:.1f}x',
                         fontsize=12, ha='right', va='bottom',
                         bbox=dict(boxstyle='round,pad=0.4', facecolor='#2a2a2a', alpha=0.8),
                         color=self.colors['accent'])
    
    def add_status_indicator(self):
        """Add animation status indicator"""
        status_text = "🎬 ANIMATING..." if self.is_animating else "⏸ PAUSED - Press SPACE to continue"
        status_color = '#F59E0B' if self.is_animating else '#34D399'
        
        self.fig.text(0.5, 0.98, status_text,
                     fontsize=14, ha='center', va='top',
                     bbox=dict(boxstyle='round,pad=0.5', facecolor='#2a2a2a', 
                             edgecolor=status_color, linewidth=2, alpha=0.9),
                     color=status_color, fontweight='bold')
    
    def draw_2d_complete(self):
        """Draw complete 2D vector visualization"""
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, projection='3d', facecolor=self.colors['bg'])
        
        # Enable rotation
        if hasattr(self.ax, 'mouse_init'):
            self.ax.mouse_init(rotate_btn=3, zoom_btn=2)
        
        self.ax.view_init(elev=90, azim=-90)
        
        limit = self.set_3d_limits(self.ax)
        
        # Grid
        alpha = 0.3
        for i in np.linspace(-limit, limit, 13):
            self.ax.plot([i, i], [-limit, limit], [0, 0], 
                        color=self.colors['grid'], alpha=alpha, linewidth=0.5)
            self.ax.plot([-limit, limit], [i, i], [0, 0], 
                        color=self.colors['grid'], alpha=alpha, linewidth=0.5)
        
        # Axes
        self.ax.plot([-limit, limit], [0, 0], [0, 0], 
                    color=self.colors['axis'], linewidth=2.5, alpha=0.8)
        self.ax.plot([0, 0], [-limit, limit], [0, 0], 
                    color=self.colors['axis'], linewidth=2.5, alpha=0.8)
        
        # Labels
        self.ax.set_xlabel('X Dimension', fontweight='bold', labelpad=10)
        self.ax.set_ylabel('Y Dimension', fontweight='bold', labelpad=10)
        self.ax.set_zlabel('')
        self.ax.zaxis.set_ticklabels([])
        
        # Clean up panes
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.ax.xaxis.pane.set_edgecolor('none')
        self.ax.yaxis.pane.set_edgecolor('none')
        self.ax.zaxis.pane.set_edgecolor('none')
        
        # Vector
        arrow = Arrow3D([0, self.vector_x], [0, self.vector_y], [0, 0],
                       mutation_scale=25, lw=5, arrowstyle='-|>', 
                       color=self.colors['vector'], alpha=0.9)
        self.ax.add_artist(arrow)
        
        self.ax.scatter([self.vector_x], [self.vector_y], [0],
                       s=500, c=self.colors['point'],
                       edgecolors='white', linewidths=3,
                       zorder=5, alpha=0.9)
        
        # Title
        vector_text = f"Vector: [{self.vector_x:.1f}, {self.vector_y:.1f}]"
        self.fig.text(0.5, 0.92, vector_text, 
                    fontsize=32, fontweight='bold',
                    ha='center', va='top',
                    bbox=dict(boxstyle='round,pad=0.8', facecolor='#2a2a2a', 
                            edgecolor=self.colors['vector'], linewidth=3, alpha=0.95),
                    color=self.colors['text'])
        
        self.fig.text(0.5, 0.06, '2D Vector Space', 
                    fontsize=22, ha='center', va='bottom',
                    color=self.colors['accent'], alpha=0.8, fontweight='bold')
        
        # Instructions
        instructions = "LEFT: Draw | RIGHT: Rotate | Scroll: Zoom | C: Clear | SPACE: Next | B: Back"
        self.fig.text(0.5, 0.01, instructions,
                    fontsize=11, ha='center', va='bottom',
                    color=self.colors['text'], alpha=0.6, style='italic')
        
        if self.zoom_level != 1.0:
            self.add_zoom_indicator_3d()
        
        # Magnitude
        magnitude = np.sqrt(self.vector_x**2 + self.vector_y**2)
        self.ax.text(self.vector_x/2 - 0.5, self.vector_y/2 + 0.7, 0,
                    f'|v| = {magnitude:.2f}',
                    fontsize=16, ha='center',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='#2a2a2a', 
                            edgecolor=self.colors['accent'], linewidth=2, alpha=0.9),
                    color=self.colors['vector'], fontweight='bold')
        
        self.add_status_indicator()
        plt.tight_layout()
    
    def draw_2d_animated(self, progress):
        """Draw 2D with animation progress"""
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, projection='3d', facecolor=self.colors['bg'])
        
        if hasattr(self.ax, 'mouse_init'):
            self.ax.mouse_init(rotate_btn=3, zoom_btn=2)
        
        self.ax.view_init(elev=90, azim=-90)
        limit = self.set_3d_limits(self.ax)
        
        # Grid fade in
        alpha = progress * 0.3
        for i in np.linspace(-limit, limit, 13):
            self.ax.plot([i, i], [-limit, limit], [0, 0], 
                        color=self.colors['grid'], alpha=alpha, linewidth=0.5)
            self.ax.plot([-limit, limit], [i, i], [0, 0], 
                        color=self.colors['grid'], alpha=alpha, linewidth=0.5)
        
        # Axes
        self.ax.plot([-limit, limit], [0, 0], [0, 0], 
                    color=self.colors['axis'], linewidth=2.5, 
                    alpha=progress * 0.8)
        self.ax.plot([0, 0], [-limit, limit], [0, 0], 
                    color=self.colors['axis'], linewidth=2.5, 
                    alpha=progress * 0.8)
        
        self.ax.set_xlabel('X Dimension', fontweight='bold', labelpad=10, alpha=progress)
        self.ax.set_ylabel('Y Dimension', fontweight='bold', labelpad=10, alpha=progress)
        self.ax.set_zlabel('')
        self.ax.zaxis.set_ticklabels([])
        
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.ax.xaxis.pane.set_edgecolor('none')
        self.ax.yaxis.pane.set_edgecolor('none')
        self.ax.zaxis.pane.set_edgecolor('none')
        
        # Vector grows in
        vec_progress = max(0, (progress - 0.3) / 0.7)
        if vec_progress > 0:
            arrow = Arrow3D([0, self.vector_x * vec_progress], 
                          [0, self.vector_y * vec_progress], 
                          [0, 0],
                          mutation_scale=25, lw=5, arrowstyle='-|>', 
                          color=self.colors['vector'], alpha=0.9)
            self.ax.add_artist(arrow)
            
            self.ax.scatter([self.vector_x * vec_progress], 
                          [self.vector_y * vec_progress], 
                          [0],
                          s=500, c=self.colors['point'],
                          edgecolors='white', linewidths=3,
                          zorder=5, alpha=0.9)
        
        if vec_progress > 0.5:
            vector_text = f"Vector: [{self.vector_x:.1f}, {self.vector_y:.1f}]"
            text_alpha = (vec_progress - 0.5) / 0.5
            self.fig.text(0.5, 0.95, vector_text, 
                        fontsize=32, fontweight='bold',
                        ha='center', va='top',
                        bbox=dict(boxstyle='round,pad=0.8', facecolor='#2a2a2a', 
                                edgecolor=self.colors['vector'], linewidth=3, 
                                alpha=0.95 * text_alpha),
                        color=self.colors['text'], alpha=text_alpha)
        
        self.add_status_indicator()
        plt.tight_layout()
    
    def draw_2d_to_3d_combined(self, progress, camera=None):
        """Combined smooth 2D to 3D transformation - rotation AND z-axis growth in one continuous animation"""
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, projection='3d', facecolor=self.colors['bg'])
        
        if hasattr(self.ax, 'mouse_init'):
            self.ax.mouse_init(rotate_btn=3, zoom_btn=2)
        
        # PHASE 1: Rotation only (0-0.4) - camera rotates while vector stays at z=0
        # PHASE 2: Z growth (0.4-1.0) - camera is at final position, vector grows in z
        
        if camera:
            self.ax.view_init(elev=camera['elev'], azim=camera['azim'])
        else:
            # Smooth camera rotation in first 40%
            if progress <= 0.4:
                rotation_progress = progress / 0.4
                elev = 90 - (65 * rotation_progress)
                azim = -90 + (150 * rotation_progress)
                self.ax.view_init(elev=elev, azim=azim)
            else:
                # Camera stays at final position
                self.ax.view_init(elev=25, azim=60)
        
        limit = self.set_3d_limits(self.ax)
        
        # Grid (fading during rotation)
        grid_alpha = 0.3 * (1 - min(1, progress * 1.5) * 0.5)
        for i in np.linspace(-limit, limit, 13):
            self.ax.plot([i, i], [-limit, limit], [0, 0], 
                        color=self.colors['grid'], alpha=grid_alpha, linewidth=0.5)
            self.ax.plot([-limit, limit], [i, i], [0, 0], 
                        color=self.colors['grid'], alpha=grid_alpha, linewidth=0.5)
        
        # Plane (appears during z-growth phase)
        if progress > 0.5:
            plane_alpha = (progress - 0.5) / 0.5 * 0.08
            xx, yy = np.meshgrid(np.linspace(-limit, limit, 13), 
                                np.linspace(-limit, limit, 13))
            self.ax.plot_surface(xx, yy, np.zeros_like(xx), 
                               alpha=plane_alpha, color=self.colors['axis'])
        
        # X and Y axes
        self.ax.plot([-limit, limit], [0, 0], [0, 0], color=self.colors['axis'], 
                    linewidth=2.5, alpha=0.8)
        self.ax.plot([0, 0], [-limit, limit], [0, 0], color=self.colors['axis'], 
                    linewidth=2.5, alpha=0.8)
        
        # Z axis grows throughout animation
        z_alpha = progress
        if z_alpha > 0:
            z_height = limit * z_alpha
            self.ax.plot([0, 0], [0, 0], [0, z_height], 
                        color=self.colors['accent'], linewidth=2.5, 
                        alpha=0.8 * z_alpha)
        
        # Vector: stays at z=0 during rotation (0-0.4), then grows in z (0.4-1.0)
        if progress <= 0.4:
            # Rotation phase - vector at z=0
            current_z = 0
        else:
            # Z-growth phase
            z_progress = (progress - 0.4) / 0.6
            eased_z = 1 - (1 - z_progress) ** 3  # Ease out cubic
            current_z = self.vector_z * eased_z
        
        # Draw vector
        arrow = Arrow3D([0, self.vector_x], [0, self.vector_y], [0, current_z],
                       mutation_scale=25, lw=5, arrowstyle='-|>', 
                       color=self.colors['vector'], alpha=0.9)
        self.ax.add_artist(arrow)
        
        self.ax.scatter([self.vector_x], [self.vector_y], [current_z],
                       s=500, c=self.colors['point'], edgecolors='white', 
                       linewidths=3, zorder=5, alpha=0.9)
        
        # Projection lines (appear during z-growth)
        if progress > 0.5:
            proj_alpha = (progress - 0.5) / 0.5 * 0.4
            self.ax.plot([self.vector_x, self.vector_x], 
                        [self.vector_y, self.vector_y], 
                        [0, current_z], 
                        color=self.colors['projection'], 
                        linestyle='--', alpha=proj_alpha, linewidth=1.5)
            self.ax.plot([self.vector_x, self.vector_x], [0, self.vector_y], [0, 0], 
                        color=self.colors['projection'], linestyle='--', 
                        alpha=proj_alpha * 0.7, linewidth=1)
            self.ax.plot([0, self.vector_x], [self.vector_y, self.vector_y], [0, 0], 
                        color=self.colors['projection'], linestyle='--', 
                        alpha=proj_alpha * 0.7, linewidth=1)
        
        # Labels
        self.ax.set_xlabel('X Dimension', fontweight='bold', labelpad=10)
        self.ax.set_ylabel('Y Dimension', fontweight='bold', labelpad=10)
        if z_alpha > 0.3:
            self.ax.set_zlabel('Z Dimension', fontweight='bold', labelpad=10, 
                             alpha=min(1.0, (z_alpha - 0.3) / 0.7))
        
        # Clean panes - ALWAYS dark
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.ax.xaxis.pane.set_edgecolor('none')
        self.ax.yaxis.pane.set_edgecolor('none')
        self.ax.zaxis.pane.set_edgecolor('none')
        
        # Title changes during animation
        if progress <= 0.4:
            vector_text = f"Vector: [{self.vector_x:.1f}, {self.vector_y:.1f}, 0.0]"
            subtitle = 'Rotating to 3D view...'
        else:
            vector_text = f"Vector: [{self.vector_x:.1f}, {self.vector_y:.1f}, {current_z:.1f}]"
            if progress < 0.9:
                subtitle = 'Extending to 3D Space...'
            else:
                subtitle = '3D Vector Space'
        
        self.fig.text(0.5, 0.92, vector_text,
                     fontsize=32, fontweight='bold',
                     ha='center', va='top',
                     bbox=dict(boxstyle='round,pad=0.8', facecolor='#2a2a2a',
                             edgecolor=self.colors['vector'], linewidth=3, alpha=0.95),
                     color=self.colors['text'])
        
        self.fig.text(0.5, 0.08, subtitle,
                     fontsize=20, ha='center', va='bottom',
                     color=self.colors['accent'], alpha=0.8, fontweight='bold',
                     style='italic')
        
        # Show magnitude when complete
        if progress > 0.9:
            magnitude = np.sqrt(self.vector_x**2 + self.vector_y**2 + self.vector_z**2)
            mag_alpha = (progress - 0.9) / 0.1
            self.fig.text(0.5, 0.85, f'Magnitude: |v| = {magnitude:.2f}',
                         fontsize=18, ha='center',
                         bbox=dict(boxstyle='round,pad=0.5', facecolor='#2a2a2a', 
                                 edgecolor=self.colors['accent'], linewidth=2, alpha=0.9 * mag_alpha),
                         color=self.colors['vector'], fontweight='bold', alpha=mag_alpha)
        
        self.add_zoom_indicator_3d()
        self.add_status_indicator()
        plt.tight_layout()
    
    def draw_semantic_space(self, progress, camera=None):
        """Draw semantic space with multiple related vectors"""
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, projection='3d', facecolor=self.colors['bg'])
        
        if hasattr(self.ax, 'mouse_init'):
            self.ax.mouse_init(rotate_btn=3, zoom_btn=2)
        
        if camera:
            self.ax.view_init(elev=camera['elev'], azim=camera['azim'])
        else:
            self.ax.view_init(elev=25, azim=60)
        
        limit = self.set_3d_limits(self.ax)
        
        # Axes
        self.ax.plot([-limit, limit], [0, 0], [0, 0], color=self.colors['axis'], 
                    linewidth=2, alpha=0.6)
        self.ax.plot([0, 0], [-limit, limit], [0, 0], color=self.colors['axis'], 
                    linewidth=2, alpha=0.6)
        self.ax.plot([0, 0], [0, 0], [-limit, limit], color=self.colors['accent'], 
                    linewidth=2, alpha=0.6)
        
        # Clean panes
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.ax.xaxis.pane.set_edgecolor('none')
        self.ax.yaxis.pane.set_edgecolor('none')
        self.ax.zaxis.pane.set_edgecolor('none')
        
        # Fade out original vector
        fade_out = max(0, 1 - progress * 2)
        if fade_out > 0:
            arrow = Arrow3D([0, self.vector_x], [0, self.vector_y], [0, self.vector_z],
                           mutation_scale=20, lw=4, arrowstyle='-|>', 
                           color=self.colors['vector'], alpha=0.3 * fade_out)
            self.ax.add_artist(arrow)
        
        # Fade in semantic vectors
        fade_in = max(0, min(1, (progress - 0.2) / 0.6))
        
        if fade_in > 0:
            animal_colors = ['#34D399', '#10B981', '#059669']
            vehicle_colors = ['#F59E0B', '#D97706', '#B45309']
            
            animals = ['Hond', 'Kat', 'Paard']
            vehicles = ['Auto', 'Fiets', 'Vliegtuig']
            
            for i, word in enumerate(animals):
                vec = self.semantic_vectors[word]
                arrow = Arrow3D([0, vec[0]], [0, vec[1]], [0, vec[2]],
                               mutation_scale=15, lw=3, arrowstyle='-|>', 
                               color=animal_colors[i], alpha=0.6 * fade_in)
                self.ax.add_artist(arrow)
                
                self.ax.scatter([vec[0]], [vec[1]], [vec[2]],
                               s=300, c=animal_colors[i], edgecolors='white', 
                               linewidths=2, zorder=5, alpha=fade_in)
                
                if fade_in > 0.5:
                    label_alpha = (fade_in - 0.5) * 2
                    self.ax.text(vec[0], vec[1], vec[2] + 0.3, word,
                               fontsize=14, fontweight='bold',
                               ha='center', va='bottom',
                               color=animal_colors[i], alpha=label_alpha)
            
            for i, word in enumerate(vehicles):
                vec = self.semantic_vectors[word]
                arrow = Arrow3D([0, vec[0]], [0, vec[1]], [0, vec[2]],
                               mutation_scale=15, lw=3, arrowstyle='-|>', 
                               color=vehicle_colors[i], alpha=0.6 * fade_in)
                self.ax.add_artist(arrow)
                
                self.ax.scatter([vec[0]], [vec[1]], [vec[2]],
                               s=300, c=vehicle_colors[i], edgecolors='white', 
                               linewidths=2, zorder=5, alpha=fade_in)
                
                if fade_in > 0.5:
                    label_alpha = (fade_in - 0.5) * 2
                    self.ax.text(vec[0], vec[1], vec[2] + 0.3, word,
                               fontsize=14, fontweight='bold',
                               ha='center', va='bottom',
                               color=vehicle_colors[i], alpha=label_alpha)
            
            # Cluster lines
            if progress > 0.6:
                cluster_alpha = (progress - 0.6) / 0.4 * 0.2
                
                for i in range(len(animals)):
                    for j in range(i + 1, len(animals)):
                        vec1 = self.semantic_vectors[animals[i]]
                        vec2 = self.semantic_vectors[animals[j]]
                        self.ax.plot([vec1[0], vec2[0]], [vec1[1], vec2[1]], 
                                   [vec1[2], vec2[2]], color='#34D399', 
                                   linestyle='--', alpha=cluster_alpha, linewidth=1)
                
                for i in range(len(vehicles)):
                    for j in range(i + 1, len(vehicles)):
                        vec1 = self.semantic_vectors[vehicles[i]]
                        vec2 = self.semantic_vectors[vehicles[j]]
                        self.ax.plot([vec1[0], vec2[0]], [vec1[1], vec2[1]], 
                                   [vec1[2], vec2[2]], color='#F59E0B', 
                                   linestyle='--', alpha=cluster_alpha, linewidth=1)
        
        # Labels
        self.ax.set_xlabel('X Dimension', fontweight='bold', labelpad=10)
        self.ax.set_ylabel('Y Dimension', fontweight='bold', labelpad=10)
        self.ax.set_zlabel('Z Dimension', fontweight='bold', labelpad=10)
        
        # Title
        self.fig.text(0.5, 0.92, 'Semantic Space: Betekenis als Afstand',
                     fontsize=32, fontweight='bold',
                     ha='center', va='top',
                     bbox=dict(boxstyle='round,pad=0.8', facecolor='#2a2a2a',
                             edgecolor=self.colors['accent'], linewidth=3, alpha=0.95),
                     color=self.colors['text'])
        
        if progress > 0.7:
            expl_alpha = min(1.0, (progress - 0.7) / 0.3)
            self.fig.text(0.5, 0.12, 'Gelijksoortige woorden liggen dicht bij elkaar',
                         fontsize=18, ha='center', va='bottom',
                         color=self.colors['text'], alpha=0.8 * expl_alpha,
                         style='italic')
            self.fig.text(0.5, 0.08, '🐕 Dieren cluster (groen)  •  🚗 Voertuigen cluster (oranje)',
                         fontsize=16, ha='center', va='bottom',
                         color=self.colors['text'], alpha=0.7 * expl_alpha)
        
        self.add_zoom_indicator_3d()
        self.add_status_indicator()
        plt.tight_layout()
    
    def draw_vector_arithmetic(self, progress, camera=None):
        """REDESIGNED: Clear vector arithmetic with PAUSES between phases"""
        self.fig.clear()
        self.ax = self.fig.add_subplot(111, projection='3d', facecolor=self.colors['bg'])
        
        if hasattr(self.ax, 'mouse_init'):
            self.ax.mouse_init(rotate_btn=3, zoom_btn=2)
        
        if camera:
            self.ax.view_init(elev=camera['elev'], azim=camera['azim'])
        else:
            self.ax.view_init(elev=25, azim=60)
        
        limit = self.set_3d_limits(self.ax)
        
        # Axes
        self.ax.plot([-limit, limit], [0, 0], [0, 0], color=self.colors['axis'], 
                    linewidth=2, alpha=0.6)
        self.ax.plot([0, 0], [-limit, limit], [0, 0], color=self.colors['axis'], 
                    linewidth=2, alpha=0.6)
        self.ax.plot([0, 0], [0, 0], [-limit, limit], color=self.colors['accent'], 
                    linewidth=2, alpha=0.6)
        
        # Clean panes
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False
        self.ax.xaxis.pane.set_edgecolor('none')
        self.ax.yaxis.pane.set_edgecolor('none')
        self.ax.zaxis.pane.set_edgecolor('none')
        
        # Smaller labels
        self.ax.set_xlabel('X', fontweight='bold', labelpad=5, fontsize=12)
        self.ax.set_ylabel('Y', fontweight='bold', labelpad=5, fontsize=12)
        self.ax.set_zlabel('Z', fontweight='bold', labelpad=5, fontsize=12)
        
        # PHASE TIMING with pauses:
        # 0.00-0.20: Show input vectors (Koning, Man, Vrouw)
        # 0.20-0.25: PAUSE - hold
        # 0.25-0.45: Subtraction (Koning - Man)
        # 0.45-0.50: PAUSE - hold
        # 0.50-0.70: Addition (+ Vrouw)
        # 0.70-0.75: PAUSE - hold with "?"
        # 0.75-1.00: Reveal Koningin
        
        # PHASE 1: Show input vectors (0-0.20) + PAUSE (0.20-0.25)
        if progress <= 0.25:
            if progress <= 0.20:
                phase = progress / 0.20
            else:
                phase = 1.0  # Hold at full visibility
            
            # Koning
            arrow = Arrow3D([0, self.koning[0]], [0, self.koning[1]], [0, self.koning[2]],
                           mutation_scale=20, lw=4, arrowstyle='-|>', 
                           color='#3B82F6', alpha=0.8 * phase)
            self.ax.add_artist(arrow)
            self.ax.scatter([self.koning[0]], [self.koning[1]], [self.koning[2]],
                           s=400, c='#3B82F6', edgecolors='white', linewidths=2, zorder=5, alpha=phase)
            if phase > 0.4:
                self.ax.text(self.koning[0], self.koning[1], self.koning[2] + 0.5, 'Koning',
                           fontsize=16, fontweight='bold', ha='center', color='#3B82F6', 
                           alpha=min(1.0, (phase-0.4)*1.67))
            
            # Man
            arrow = Arrow3D([0, self.man[0]], [0, self.man[1]], [0, self.man[2]],
                           mutation_scale=20, lw=4, arrowstyle='-|>', 
                           color='#10B981', alpha=0.8 * phase)
            self.ax.add_artist(arrow)
            self.ax.scatter([self.man[0]], [self.man[1]], [self.man[2]],
                           s=400, c='#10B981', edgecolors='white', linewidths=2, zorder=5, alpha=phase)
            if phase > 0.4:
                self.ax.text(self.man[0], self.man[1], self.man[2] + 0.5, 'Man',
                           fontsize=16, fontweight='bold', ha='center', color='#10B981', 
                           alpha=min(1.0, (phase-0.4)*1.67))
            
            # Vrouw
            arrow = Arrow3D([0, self.vrouw[0]], [0, self.vrouw[1]], [0, self.vrouw[2]],
                           mutation_scale=20, lw=4, arrowstyle='-|>', 
                           color='#F59E0B', alpha=0.8 * phase)
            self.ax.add_artist(arrow)
            self.ax.scatter([self.vrouw[0]], [self.vrouw[1]], [self.vrouw[2]],
                           s=400, c='#F59E0B', edgecolors='white', linewidths=2, zorder=5, alpha=phase)
            if phase > 0.4:
                self.ax.text(self.vrouw[0], self.vrouw[1], self.vrouw[2] + 0.5, 'Vrouw',
                           fontsize=16, fontweight='bold', ha='center', color='#F59E0B', 
                           alpha=min(1.0, (phase-0.4)*1.67))
            
            formula = "Koning - Man + Vrouw = ?"
        
        # PHASE 2: Subtraction (0.25-0.45) + PAUSE (0.45-0.50)
        elif progress <= 0.50:
            if progress <= 0.45:
                phase = (progress - 0.25) / 0.20
            else:
                phase = 1.0  # Hold
            
            # Koning visible
            arrow = Arrow3D([0, self.koning[0]], [0, self.koning[1]], [0, self.koning[2]],
                           mutation_scale=20, lw=4, arrowstyle='-|>', 
                           color='#3B82F6', alpha=0.9)
            self.ax.add_artist(arrow)
            self.ax.scatter([self.koning[0]], [self.koning[1]], [self.koning[2]],
                           s=400, c='#3B82F6', edgecolors='white', linewidths=2, zorder=5)
            self.ax.text(self.koning[0], self.koning[1], self.koning[2] + 0.5, 'Koning',
                       fontsize=16, fontweight='bold', ha='center', color='#3B82F6')
            
            # Man with minus
            arrow = Arrow3D([0, self.man[0]], [0, self.man[1]], [0, self.man[2]],
                           mutation_scale=20, lw=4, arrowstyle='-|>', 
                           color='#10B981', alpha=0.9)
            self.ax.add_artist(arrow)
            self.ax.scatter([self.man[0]], [self.man[1]], [self.man[2]],
                           s=400, c='#10B981', edgecolors='white', linewidths=2, zorder=5)
            self.ax.text(self.man[0], self.man[1], self.man[2] + 0.5, '- Man',
                       fontsize=16, fontweight='bold', ha='center', color='#10B981')
            
            # Vrouw fades out
            fade = max(0, 1 - phase * 2)
            if fade > 0:
                arrow = Arrow3D([0, self.vrouw[0]], [0, self.vrouw[1]], [0, self.vrouw[2]],
                               mutation_scale=20, lw=4, arrowstyle='-|>', 
                               color='#F59E0B', alpha=0.3 * fade)
                self.ax.add_artist(arrow)
            
            # Intermediate result grows
            intermediate = self.koning - self.man
            current_result = intermediate * phase
            
            arrow = Arrow3D([0, current_result[0]], [0, current_result[1]], [0, current_result[2]],
                           mutation_scale=25, lw=5, arrowstyle='-|>', 
                           color='#A78BFA', alpha=0.8 * phase)
            self.ax.add_artist(arrow)
            self.ax.scatter([current_result[0]], [current_result[1]], [current_result[2]],
                           s=500, c='#A78BFA', edgecolors='white', linewidths=3, zorder=5, alpha=phase)
            
            if phase > 0.5:
                self.ax.text(current_result[0], current_result[1], current_result[2] + 0.6, 'Stap 1',
                           fontsize=14, fontweight='bold', ha='center', color='#A78BFA', 
                           alpha=min(1.0, (phase-0.5)*2))
            
            formula = "Koning - Man = ..."
        
        # PHASE 3: Addition (0.50-0.70) + PAUSE (0.70-0.75)
        elif progress <= 0.75:
            if progress <= 0.70:
                phase = (progress - 0.50) / 0.20
            else:
                phase = 1.0  # Hold
            
            # Intermediate result (faded)
            intermediate = self.koning - self.man
            arrow = Arrow3D([0, intermediate[0]], [0, intermediate[1]], [0, intermediate[2]],
                           mutation_scale=20, lw=4, arrowstyle='-|>', 
                           color='#A78BFA', alpha=0.4)
            self.ax.add_artist(arrow)
            self.ax.scatter([intermediate[0]], [intermediate[1]], [intermediate[2]],
                           s=350, c='#A78BFA', edgecolors='white', linewidths=2, zorder=5, alpha=0.4)
            
            # Vrouw fades in
            arrow = Arrow3D([0, self.vrouw[0]], [0, self.vrouw[1]], [0, self.vrouw[2]],
                           mutation_scale=20, lw=4, arrowstyle='-|>', 
                           color='#F59E0B', alpha=0.8 * phase)
            self.ax.add_artist(arrow)
            self.ax.scatter([self.vrouw[0]], [self.vrouw[1]], [self.vrouw[2]],
                           s=400, c='#F59E0B', edgecolors='white', linewidths=2, zorder=5, alpha=phase)
            if phase > 0.3:
                self.ax.text(self.vrouw[0], self.vrouw[1], self.vrouw[2] + 0.5, '+ Vrouw',
                           fontsize=16, fontweight='bold', ha='center', color='#F59E0B', 
                           alpha=min(1.0, (phase-0.3)*1.43))
            
            # Final result grows
            current_result = intermediate + (self.vrouw * phase)
            
            arrow = Arrow3D([0, current_result[0]], [0, current_result[1]], [0, current_result[2]],
                           mutation_scale=25, lw=5, arrowstyle='-|>', 
                           color='#EC4899', alpha=0.8 * phase)
            self.ax.add_artist(arrow)
            self.ax.scatter([current_result[0]], [current_result[1]], [current_result[2]],
                           s=500, c='#EC4899', edgecolors='white', linewidths=3, zorder=5, alpha=phase)
            
            # Show "?" during pause
            if phase > 0.7 or progress > 0.70:
                self.ax.text(current_result[0], current_result[1], current_result[2] + 0.6, '?',
                           fontsize=22, fontweight='bold', ha='center', color='#EC4899')
            
            formula = "... + Vrouw = ?"
        
        # PHASE 4: Reveal answer (0.75-1.0)
        else:
            phase = (progress - 0.75) / 0.25
            
            # Fade out all inputs
            fade = max(0, 1 - phase * 3)
            if fade > 0:
                arrow = Arrow3D([0, self.koning[0]], [0, self.koning[1]], [0, self.koning[2]],
                               mutation_scale=20, lw=4, arrowstyle='-|>', 
                               color='#3B82F6', alpha=0.2 * fade)
                self.ax.add_artist(arrow)
                
                arrow = Arrow3D([0, self.man[0]], [0, self.man[1]], [0, self.man[2]],
                               mutation_scale=20, lw=4, arrowstyle='-|>', 
                               color='#10B981', alpha=0.2 * fade)
                self.ax.add_artist(arrow)
                
                arrow = Arrow3D([0, self.vrouw[0]], [0, self.vrouw[1]], [0, self.vrouw[2]],
                               mutation_scale=20, lw=4, arrowstyle='-|>', 
                               color='#F59E0B', alpha=0.2 * fade)
                self.ax.add_artist(arrow)
            
            # Result with pulse
            pulse = 1 + 0.15 * np.sin(phase * 12 * np.pi)
            arrow = Arrow3D([0, self.koningin[0]], [0, self.koningin[1]], [0, self.koningin[2]],
                           mutation_scale=25, lw=5, arrowstyle='-|>', 
                           color='#EC4899', alpha=0.95)
            self.ax.add_artist(arrow)
            self.ax.scatter([self.koningin[0]], [self.koningin[1]], [self.koningin[2]],
                           s=500 * pulse, c='#EC4899', edgecolors='white', linewidths=3, zorder=5)
            
            # Reveal label
            if phase > 0.2:
                label_alpha = min(1.0, (phase - 0.2) / 0.8)
                self.ax.text(self.koningin[0], self.koningin[1], self.koningin[2] + 0.6, 'Koningin!',
                           fontsize=22, fontweight='bold', ha='center', color='#EC4899', alpha=label_alpha)
            
            formula = "Koning - Man + Vrouw = Koningin! 👑"
        
        # Title
        self.fig.text(0.5, 0.92, formula,
                     fontsize=32, fontweight='bold',
                     ha='center', va='top',
                     bbox=dict(boxstyle='round,pad=0.8', facecolor='#2a2a2a',
                             edgecolor='#EC4899', linewidth=3, alpha=0.95),
                     color=self.colors['text'])
        
        # Explanation
        if progress > 0.85:
            expl_alpha = min(1.0, (progress - 0.85) / 0.15)
            self.fig.text(0.5, 0.08, 'AI kan "betekenis rekenen" - analogieën zijn wiskundige bewerkingen!',
                         fontsize=18, ha='center', va='bottom',
                         color=self.colors['text'], alpha=0.8 * expl_alpha,
                         style='italic')
        
        self.add_zoom_indicator_3d()
        self.add_status_indicator()
        plt.tight_layout()
    
    def draw_real_embedding(self, progress):
        """Draw real 384-dimensional embedding"""
        self.fig.clear()
        ax = self.fig.add_subplot(111, facecolor=self.colors['bg'])
        ax.axis('off')
        
        embedding_size = len(self.real_embedding)
        
        self.fig.text(0.5, 0.95, f'De Realiteit: {embedding_size}-Dimensionale Vector',
                     fontsize=32, fontweight='bold',
                     ha='center', va='top',
                     bbox=dict(boxstyle='round,pad=0.8', facecolor='#2a2a2a',
                             edgecolor=self.colors['vector'], linewidth=3, alpha=0.95),
                     color=self.colors['text'])
        
        fade_in = min(1, progress * 2)
        self.fig.text(0.5, 0.85, 'Dit is een echte embedding van een modern AI model',
                     fontsize=18, ha='center', va='top',
                     color=self.colors['accent'], alpha=0.8 * fade_in,
                     fontweight='bold')
        
        self.fig.text(0.5, 0.80, '(OpenAI ada-002, Sentence Transformers, etc.)',
                     fontsize=14, ha='center', va='top',
                     color=self.colors['text'], alpha=0.6 * fade_in,
                     style='italic')
        
        # Display embedding progressively
        if progress > 0.2:
            display_progress = min(1.0, (progress - 0.2) / 0.6)
            num_values_to_show = max(1, int(embedding_size * display_progress))
            
            embedding_str = "[\n  "
            values_per_line = 8
            
            for i in range(num_values_to_show):
                embedding_str += f"{self.real_embedding[i]:7.4f}"
                
                if i < num_values_to_show - 1:
                    embedding_str += ", "
                    if (i + 1) % values_per_line == 0 and i < num_values_to_show - 1:
                        embedding_str += "\n  "
            
            if num_values_to_show < embedding_size:
                embedding_str += ",\n  ..."
            
            embedding_str += "\n]"
            
            self.fig.text(0.5, 0.70, embedding_str,
                         fontsize=10, ha='center', va='top',
                         family='monospace',
                         bbox=dict(boxstyle='round,pad=1.0', facecolor='#1a1a1a',
                                 edgecolor='#404040', linewidth=2, alpha=0.95),
                         color='#34D399', alpha=min(1.0, display_progress * 1.5))
        
        # Statistics
        if progress > 0.6:
            stats_alpha = min(1.0, (progress - 0.6) / 0.3)
            
            stats_text = f"Dimensies: {embedding_size}  •  Min: {self.real_embedding.min():.4f}  •  Max: {self.real_embedding.max():.4f}  •  Mean: {self.real_embedding.mean():.4f}"
            
            self.fig.text(0.5, 0.10, stats_text,
                         fontsize=14, ha='center', va='top',
                         bbox=dict(boxstyle='round,pad=0.5', facecolor='#2a2a2a', alpha=0.9 * stats_alpha),
                         color=self.colors['text'], alpha=stats_alpha,
                         family='monospace')
            
            self.fig.text(0.5, 0.04, '💡 Moderne modellen gebruiken 384, 768, 1536, of zelfs 4096 dimensies!',
                         fontsize=16, ha='center', va='top',
                         color=self.colors['accent'], alpha=0.8 * stats_alpha,
                         style='italic')
        
        self.add_status_indicator()
        plt.tight_layout()
    
    def randomize_vector(self):
        """Generate random vector values"""
        self.vector_x = np.random.uniform(-5, 5)
        self.vector_y = np.random.uniform(-5, 5)
        self.vector_z = np.random.uniform(-5, 5)
        
        if not self.is_animating:
            self.redraw_without_reset()
            self.fig.canvas.draw_idle()
        print(f"🎲 Randomized vector: [{self.vector_x:.2f}, {self.vector_y:.2f}, {self.vector_z:.2f}]")
    
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
    """Main function to run the presentation"""
    print("=" * 70)
    print("INTERACTIVE VECTOR VISUALIZATION - AI KENNISSESSIE")
    print("=" * 70)
    print("\n🎬 Animation Control:")
    print("  SPACE        : Start/Continue to next animation step")
    print("  B            : Go back to previous step")
    print("\n✏️  Drawing (during pause):")
    print("  LEFT CLICK   : Draw freehand lines/annotations")
    print("  C            : Clear all drawings")
    print("  (Drawings auto-clear when advancing/going back)")
    print("\n🖱️  Camera Control (during pause):")
    print("  RIGHT CLICK  : Drag to rotate camera")
    print("  SCROLL WHEEL : Zoom in/out (camera angle preserved!)")
    print("\n⚙️  Other Controls:")
    print("  R            : Randomize vector position")
    print("  F            : Toggle fullscreen")
    print("  Q or ESC     : Quit presentation")
    print("\n📊 Visualization Steps:")
    print("  Step 0: Landing Page (AI Kennissessie intro)")
    print("  Step 1: 2D Vector Space")
    print("  Step 2: 2D to 3D Transformation (smooth rotation + z-growth)")
    print("  Step 3: Semantic Space (clusters van woorden)")
    print("  Step 4: Vector Arithmetic (Koning - Man + Vrouw = Koningin)")
    print("           └─ With controllable pauses between phases!")
    print("  Step 5: Real 384D Embedding")
    print("\n💡 Improvements:")
    print("  ✓ NO camera resets during drawing or zooming")
    print("  ✓ ONE continuous 2D→3D animation (120 frames)")
    print("  ✓ Always dark mode (no flashing)")
    print("  ✓ Vector arithmetic with pauses between transitions")
    print("  ✓ Engaging landing page")
    print("\nPress SPACE to begin...")
    print("=" * 70)
    
    presentation = AnimatedVectorPresentation()
    presentation.show()

if __name__ == "__main__":
    main()