"""
Unified styling configuration for all presentations
Dark mode theme with consistent colors, fonts, and UI elements
"""

import matplotlib
import matplotlib.pyplot as plt


class PresentationStyle:
    """
    Centralized styling configuration for all AI presentations
    Ensures consistent visual appearance across the suite
    """

    # Color palette - Dark mode optimized
    COLORS = {
        'primary': '#3B82F6',      # Blue - main actions, headers
        'secondary': '#10B981',    # Green - success, complete states
        'accent': '#F59E0B',       # Orange - warnings, highlights
        'highlight': '#EC4899',    # Pink - special emphasis
        'purple': '#A78BFA',       # Purple - advanced concepts
        'cyan': '#06B6D4',         # Cyan - technical elements
        'text': '#F0F0F0',         # Light gray - main text
        'dim': '#6B7280',          # Medium gray - secondary text
        'bg': '#0a0a0a',           # Near black - background
        'bg_light': '#1a1a1a',     # Dark gray - elevated surfaces
        'warning': '#EF4444',      # Red - errors, critical
        'success': '#10B981',      # Green - success states
        'vector': '#FF6B9D',       # Pink - vector visualizations
        'grid': '#303030',         # Dark gray - grid lines
        'axis': '#60A5FA',         # Light blue - axis lines
        'point': '#34D399',        # Teal - data points
        'projection': '#6B7280',   # Gray - projection lines
        'neuron': '#4ECDC4',       # Teal - neural network nodes
        'active': '#FF6B6B',       # Coral - active states
        'inactive': '#95A5A6',     # Gray - inactive states
        'correct': '#2ECC71',      # Green - correct answers
        'wrong': '#E74C3C',        # Red - wrong answers
        'connection': '#BDC3C7',   # Light gray - connections
        'error': '#EF4444',        # Red - errors
    }

    # Figure settings - 4K optimized
    FIGURE_SIZE = (16, 9)  # 16:9 aspect ratio for presentations
    FIGURE_DPI = 150  # Higher DPI for sharper rendering on 4K

    # Font settings - 4K display optimized (scaled down for better readability)
    FONT_FAMILY = 'sans-serif'
    FONT_SIZE_TITLE = 36      # Was 48 - Main titles
    FONT_SIZE_SUBTITLE = 26   # Was 32 - Subtitles and axis labels
    FONT_SIZE_NORMAL = 22     # Was 28 - Normal text, legend
    FONT_SIZE_SMALL = 18      # Was 24 - Small labels
    FONT_SIZE_TINY = 16       # Was 20 - Tiny annotations

    # Animation settings
    ANIMATION_INTERVAL = 30  # milliseconds
    ANIMATION_FRAMES_SHORT = 60
    ANIMATION_FRAMES_MEDIUM = 90
    ANIMATION_FRAMES_LONG = 120

    # UI element sizes - 4K optimized
    STATUS_FONT_SIZE = 20          # Was 26 - Status text
    PROGRESS_BAR_HEIGHT = 0.015    # Slightly taller for visibility
    PROGRESS_BAR_WIDTH = 0.6

    @classmethod
    def apply_dark_mode(cls):
        """
        Apply dark mode styling to matplotlib globally
        Call this once at the start of each presentation
        """
        plt.style.use('dark_background')

        # Configure matplotlib parameters
        matplotlib.rcParams.update({
            'font.size': cls.FONT_SIZE_NORMAL,
            'font.family': cls.FONT_FAMILY,
            'axes.titlesize': cls.FONT_SIZE_TITLE,
            'axes.labelsize': cls.FONT_SIZE_SUBTITLE,
            'xtick.labelsize': cls.FONT_SIZE_SMALL,  # Tick label size for 4K
            'ytick.labelsize': cls.FONT_SIZE_SMALL,  # Tick label size for 4K
            'legend.fontsize': cls.FONT_SIZE_NORMAL,  # Legend font size for 4K
            'figure.facecolor': cls.COLORS['bg'],
            'axes.facecolor': cls.COLORS['bg_light'],
            'axes.edgecolor': '#404040',
            'grid.color': cls.COLORS['grid'],
            'text.color': cls.COLORS['text'],
            'axes.labelcolor': cls.COLORS['text'],
            'xtick.color': cls.COLORS['text'],
            'ytick.color': cls.COLORS['text'],
            'lines.linewidth': 2.5,  # Thicker lines for 4K visibility
            'axes.linewidth': 2.0,  # Thicker axis lines for 4K
            'grid.linewidth': 1.5,  # Thicker grid lines for 4K
        })

    @classmethod
    def create_figure(cls):
        """Create a new figure with standard dark mode settings and proper layout"""
        fig = plt.figure(figsize=cls.FIGURE_SIZE, facecolor=cls.COLORS['bg'])

        # Use tight layout to prevent clipping and maintain proper spacing
        fig.set_tight_layout(True)

        return fig

    @classmethod
    def setup_3d_axis(cls, ax):
        """Configure 3D axis with dark mode styling"""
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('none')
        ax.yaxis.pane.set_edgecolor('none')
        ax.zaxis.pane.set_edgecolor('none')
        ax.set_facecolor(cls.COLORS['bg_light'])

    @classmethod
    def get_color(cls, name: str, default: str = None) -> str:
        """
        Get a color by name with optional fallback

        Args:
            name: Color name from COLORS dict
            default: Fallback color if name not found

        Returns:
            Hex color string
        """
        return cls.COLORS.get(name, default or cls.COLORS['text'])

    @classmethod
    def create_box_style(cls, edge_color: str, face_color: str = None,
                         linewidth: int = 3, alpha: float = 0.95):
        """
        Create consistent box styling parameters

        Args:
            edge_color: Border color
            face_color: Fill color (defaults to bg_light)
            linewidth: Border width
            alpha: Transparency

        Returns:
            Dict of box style parameters
        """
        if face_color is None:
            face_color = cls.COLORS['bg_light']

        return {
            'boxstyle': 'round,pad=1',
            'facecolor': face_color,
            'edgecolor': edge_color,
            'linewidth': linewidth,
            'alpha': alpha
        }

    @classmethod
    def get_gradient_color(cls, progress: float, start_color: str, end_color: str) -> str:
        """
        Generate a gradient color between two colors based on progress

        Args:
            progress: Value between 0 and 1
            start_color: Starting color name
            end_color: Ending color name

        Returns:
            Interpolated color (simplified version)
        """
        # Simple implementation - just return start or end based on threshold
        return cls.COLORS[end_color] if progress > 0.5 else cls.COLORS[start_color]

    @classmethod
    def scale_fontsize(cls, original_size: int) -> int:
        """
        Scale font size for 4K display readability
        Multiplies original font sizes by 1.5x for optimal 4K viewing

        Args:
            original_size: Original font size

        Returns:
            Scaled font size optimized for 4K displays
        """
        # 1.5x scaling factor for 4K displays
        return int(original_size * 1.5)
