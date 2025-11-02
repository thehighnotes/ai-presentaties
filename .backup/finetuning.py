"""
Finetuning Journey Visualisatie - AI Kennissessie
Interactieve stap-voor-stap animatie: Van basis model naar gespecialiseerd gedrag

Controls:
- SPACE: Start/Volgende stap
- B: Vorige stap
- Q/ESC: Afsluiten
- F: Volledig scherm
- R: Reset animatie
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge
import numpy as np
from matplotlib.animation import FuncAnimation
import textwrap
from matplotlib.lines import Line2D

# Dark mode styling
plt.style.use('dark_background')
import matplotlib
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['axes.facecolor'] = '#0a0a0a'
matplotlib.rcParams['figure.facecolor'] = '#0a0a0a'

class FinetuningVisualization:
    def __init__(self):
        self.fig = plt.figure(figsize=(16, 9), facecolor='#0a0a0a')
        
        # Animation state
        self.current_step = -1  # Start met landing page
        self.step_names = [
            'Landing',
            'Base Model',
            'Training Data',
            'Model Predictions - Fouten!',  # NIEUWE STAP
            'Loss Function',
            'Gradient Updates',
            'Weight Adjustment',
            'Finetuned Model',
            'Comparison',
            'Azure AI / Local Setup'
        ]
        
        self.is_animating = False
        self.animation = None
        
        # Kleuren schema
        self.colors = {
            'primary': '#3B82F6',      # Blauw
            'secondary': '#10B981',    # Groen
            'accent': '#F59E0B',       # Oranje
            'highlight': '#EC4899',    # Roze
            'purple': '#A78BFA',       # Paars
            'text': '#F0F0F0',
            'dim': '#6B7280',
            'bg': '#0a0a0a',
            'bg_light': '#1a1a1a',
            'error': '#EF4444'         # Rood
        }
        
        # Training examples
        self.training_examples = [
            {
                'input': 'Wat is een RFC?',
                'output': 'RFC staat voor Request for Change - een formele aanvraag voor wijziging binnen BiSL.',
                'category': 'BiSL Terminologie'
            },
            {
                'input': 'Leg CAB uit',
                'output': 'CAB (Change Advisory Board) beoordeelt normale wijzigingen en adviseert over risico\'s en impact.',
                'category': 'BiSL Processen'
            },
            {
                'input': 'Verschil standaard en normale wijziging?',
                'output': 'Standaard wijzigingen zijn vooraf goedgekeurd en laag risico. Normale wijzigingen vereisen CAB beoordeling.',
                'category': 'BiSL Definities'
            }
        ]
        
        # Weights (simplified representation)
        self.base_weights = np.random.randn(50) * 0.5
        self.finetuned_weights = self.base_weights + np.random.randn(50) * 0.2
        
        self.show_landing_page()
        self.setup_controls()
    
    def setup_controls(self):
        """Setup keyboard controls"""
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
    
    def on_key(self, event):
        """Handle keyboard events"""
        if event.key == ' ':
            if not self.is_animating:
                self.start_next_step()
        elif event.key == 'b':
            if not self.is_animating:
                self.previous_step()
        elif event.key == 'r':
            if not self.is_animating:
                self.current_step = -1
                self.show_landing_page()
                plt.draw()
        elif event.key in ['q', 'escape']:
            plt.close()
        elif event.key == 'f':
            manager = plt.get_current_fig_manager()
            manager.full_screen_toggle()
    
    def show_landing_page(self):
        """Toon opening scherm"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Hoofdtitel met glow effect
        title_box = FancyBboxPatch(
            (10, 55), 80, 25,
            boxstyle="round,pad=2",
            facecolor='#1a1a1a',
            edgecolor=self.colors['purple'],
            linewidth=4,
            alpha=0.95
        )
        ax.add_patch(title_box)
        
        ax.text(50, 72, 'Finetuning Journey', 
                fontsize=48, fontweight='bold', ha='center', va='center',
                color=self.colors['purple'])
        
        ax.text(50, 64, 'Van Algemeen Model naar Specialist',
                fontsize=22, ha='center', va='center',
                color=self.colors['text'], alpha=0.8, style='italic')
        
        # Brain icon met gears
        ax.text(30, 67, '🧠', fontsize=60, ha='center', va='center')
        ax.text(70, 67, '⚙️', fontsize=60, ha='center', va='center')
        
        # Subtitel
        ax.text(50, 45, 'Leer hoe je AI traint voor specifieke taken',
                fontsize=18, ha='center', va='center',
                color=self.colors['secondary'], alpha=0.9)
        
        # Instructies
        instr_box = FancyBboxPatch(
            (25, 15), 50, 15,
            boxstyle="round,pad=1",
            facecolor='#1a1a1a',
            edgecolor=self.colors['secondary'],
            linewidth=3,
            alpha=0.9
        )
        ax.add_patch(instr_box)
        
        ax.text(50, 25, '✨ Druk op SPATIE om te beginnen ✨',
                fontsize=20, ha='center', va='center',
                color=self.colors['secondary'], fontweight='bold')
        
        ax.text(50, 20, 'B = Terug  •  R = Reset  •  Q = Afsluiten  •  F = Volledig scherm',
                fontsize=12, ha='center', va='center',
                color=self.colors['dim'], style='italic')
        
        # Footer
        ax.text(50, 5, 'Inclusief Azure AI Studio en Local LLM voorbeelden',
                fontsize=12, ha='center', va='center',
                color=self.colors['text'], alpha=0.5)
        
        plt.tight_layout()
    
    def start_next_step(self):
        """Start volgende stap"""
        if self.current_step < len(self.step_names) - 1:
            self.current_step += 1
            print(f"â†’ Stap {self.current_step + 1}/{len(self.step_names)}: {self.step_names[self.current_step]}")
            self.start_step_animation()
        else:
            print("âœ“ Laatste stap bereikt!")
    
    def previous_step(self):
        """Ga terug naar vorige stap"""
        if self.current_step > -1:
            self.current_step -= 1
            print(f"â† Stap {self.current_step + 1}/{len(self.step_names)}: {self.step_names[self.current_step]}")
            
            if self.current_step == -1:
                self.show_landing_page()
            else:
                self.draw_current_step_static()
            plt.draw()
        else:
            print("âœ“ Al bij eerste stap!")
    
    def start_step_animation(self):
        """Start animatie voor huidige stap"""
        self.is_animating = True
        self.animation_frame = 0
        
        # Aantal frames per stap
        frames_dict = {
            -1: 30,   # Landing
            0: 80,    # Base Model
            1: 90,    # Training Data
            2: 100,   # Model Predictions - Fouten! (NIEUW)
            3: 100,   # Loss Function
            4: 120,   # Gradient Updates
            5: 100,   # Weight Adjustment
            6: 80,    # Finetuned Model
            7: 100,   # Comparison
            8: 90     # Azure/Local Setup
        }
        
        total_frames = frames_dict.get(self.current_step, 60)
        
        self.animation = FuncAnimation(
            self.fig,
            self.animate_step,
            frames=total_frames,
            interval=25,
            blit=False,
            repeat=False
        )
        
        plt.draw()
    
    def animate_step(self, frame):
        """Animeer huidige stap"""
        frames_dict = {-1: 30, 0: 80, 1: 90, 2: 100, 3: 100, 4: 120, 5: 100, 6: 80, 7: 100, 8: 90}
        total = frames_dict.get(self.current_step, 60)
        progress = frame / total
        
        if self.current_step == -1:
            pass  # Landing page is statisch
        elif self.current_step == 0:
            self.draw_base_model(progress)
        elif self.current_step == 1:
            self.draw_training_data(progress)
        elif self.current_step == 2:
            self.draw_model_predictions(progress)  # NIEUWE STAP
        elif self.current_step == 3:
            self.draw_loss_function(progress)
        elif self.current_step == 4:
            self.draw_gradient_updates(progress)
        elif self.current_step == 5:
            self.draw_weight_adjustment(progress)
        elif self.current_step == 6:
            self.draw_finetuned_model(progress)
        elif self.current_step == 7:
            self.draw_comparison(progress)
        elif self.current_step == 8:
            self.draw_azure_local_setup(progress)
        
        if frame >= total - 1:
            self.is_animating = False
            print(f"  âœ“ Stap {self.current_step + 1} compleet. SPATIE = volgende stap")
    
    def draw_current_step_static(self):
        """Teken huidige stap statisch"""
        if self.current_step == 0:
            self.draw_base_model(1.0)
        elif self.current_step == 1:
            self.draw_training_data(1.0)
        elif self.current_step == 2:
            self.draw_model_predictions(1.0)  # NIEUWE STAP
        elif self.current_step == 3:
            self.draw_loss_function(1.0)
        elif self.current_step == 4:
            self.draw_gradient_updates(1.0)
        elif self.current_step == 5:
            self.draw_weight_adjustment(1.0)
        elif self.current_step == 6:
            self.draw_finetuned_model(1.0)
        elif self.current_step == 7:
            self.draw_comparison(1.0)
        elif self.current_step == 8:
            self.draw_azure_local_setup(1.0)
    
    def draw_base_model(self, progress):
        """Stap 0: Toon basis model (pre-trained)"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        title_alpha = min(1.0, progress / 0.15)
        ax.text(50, 95, 'Stap 1: Het Basis Model',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=title_alpha)
        
        ax.text(50, 90, 'Een pre-trained model met algemene kennis',
                fontsize=14, ha='center', va='top',
                color=self.colors['text'], alpha=0.7 * title_alpha, style='italic')
        
        # Model box (centrum)
        if progress > 0.2:
            model_alpha = min(1.0, (progress - 0.2) / 0.3)
            
            # Pulse effect
            if progress > 0.7:
                pulse = 1 + 0.05 * np.sin(progress * 20)
            else:
                pulse = 1.0
            
            model_box = FancyBboxPatch(
                (30, 35), 40 * pulse, 30 * pulse,
                boxstyle="round,pad=2",
                facecolor='#1a2a4a',
                edgecolor=self.colors['primary'],
                linewidth=4,
                alpha=0.95 * model_alpha
            )
            ax.add_patch(model_box)
            
            ax.text(50, 55, '🧠', fontsize=80, ha='center', va='center',
                    alpha=model_alpha)
            
            ax.text(50, 40, 'GPT / LLaMA / Phi',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['primary'],
                    fontweight='bold',
                    alpha=model_alpha)
        
        # Kennis wolken (wat het model weet)
        knowledge_items = [
            ('ðŸ“š Algemene kennis', 15, 70, 0.3),
            ('ðŸŒ Talen & cultuur', 85, 70, 0.35),
            ('ðŸ’» Programmeren', 15, 30, 0.4),
            ('ðŸ”¬ Wetenschap', 85, 30, 0.45),
            ('ðŸ“– Literatuur', 50, 15, 0.5)
        ]
        
        for text, x, y, delay in knowledge_items:
            if progress > delay:
                item_alpha = min(1.0, (progress - delay) / 0.2)
                
                bubble = FancyBboxPatch(
                    (x - 10, y - 4), 20, 8,
                    boxstyle="round,pad=0.5",
                    facecolor=self.colors['bg_light'],
                    edgecolor=self.colors['secondary'],
                    linewidth=2,
                    alpha=0.8 * item_alpha
                )
                ax.add_patch(bubble)
                
                ax.text(x, y, text,
                        fontsize=11, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=item_alpha)
        
        # Explanatory text
        if progress > 0.7:
            exp_alpha = min(1.0, (progress - 0.7) / 0.3)
            
            ax.text(50, 8, 'ðŸ’¡ Het model kent veel, maar mist specifieke domeinkennis',
                    fontsize=13, ha='center', va='center',
                    color=self.colors['accent'],
                    alpha=0.8 * exp_alpha,
                    style='italic')
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_training_data(self, progress):
        """Stap 1: Toon training data"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 95, 'Stap 2: Training Data Verzamelen',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['secondary'])
        
        ax.text(50, 90, 'Voorbeelden van gewenst gedrag in input/output paren',
                fontsize=14, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')
        
        # Training examples verschijnen Ã©Ã©n voor Ã©Ã©n
        y_positions = [75, 50, 25]
        
        for i, (example, y_pos) in enumerate(zip(self.training_examples, y_positions)):
            if progress > i * 0.25:
                example_alpha = min(1.0, (progress - i * 0.25) / 0.20)
                
                # Box voor example
                box_width = 80
                box_height = 20
                box_x = 10
                
                example_box = FancyBboxPatch(
                    (box_x, y_pos - box_height/2), box_width, box_height,
                    boxstyle="round,pad=1",
                    facecolor=self.colors['bg_light'],
                    edgecolor=self.colors['secondary'],
                    linewidth=2,
                    alpha=0.9 * example_alpha
                )
                ax.add_patch(example_box)
                
                # Category badge
                ax.text(box_x + 2, y_pos + box_height/2 - 2, example['category'],
                        fontsize=9, ha='left', va='top',
                        bbox=dict(boxstyle='round,pad=0.3', 
                                facecolor=self.colors['purple'],
                                edgecolor='none',
                                alpha=0.8),
                        color='white',
                        fontweight='bold',
                        alpha=example_alpha)
                
                # Input (vraag)
                wrapped_input = textwrap.fill(f"ðŸ“¥ Input: {example['input']}", width=60)
                ax.text(box_x + box_width/2, y_pos + 4, wrapped_input,
                        fontsize=10, ha='center', va='center',
                        color=self.colors['accent'],
                        alpha=example_alpha,
                        fontweight='bold')
                
                # Output (antwoord)
                wrapped_output = textwrap.fill(f"ðŸ“¤ Output: {example['output']}", width=60)
                ax.text(box_x + box_width/2, y_pos - 4, wrapped_output,
                        fontsize=9, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=example_alpha * 0.9)
        
        # Data count indicator
        if progress > 0.8:
            count_alpha = min(1.0, (progress - 0.8) / 0.2)
            
            ax.text(50, 8, 'ðŸ’¾ Typisch: 100-10.000+ voorbeelden nodig',
                    fontsize=13, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.5',
                            facecolor=self.colors['bg_light'],
                            edgecolor=self.colors['highlight'],
                            linewidth=2,
                            alpha=0.9),
                    color=self.colors['highlight'],
                    fontweight='bold',
                    alpha=count_alpha)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_model_predictions(self, progress):
        """Stap 2: Toon dat model fouten maakt - het PROBLEEM visualiseren"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 95, 'Stap 3: Het Probleem - Model Maakt Fouten!',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['error'])
        
        ax.text(50, 90, 'Zonder training geeft het model vaak verkeerde antwoorden',
                fontsize=14, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')
        
        # Input vraag (bovenaan)
        if progress > 0.05:
            input_alpha = min(1.0, (progress - 0.05) / 0.1)
            
            input_box = FancyBboxPatch(
                (20, 78), 60, 8,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=2,
                alpha=0.9 * input_alpha
            )
            ax.add_patch(input_box)
            
            ax.text(50, 82, 'â“ Input: "Wat is een RFC in BiSL?"',
                   fontsize=12, ha='center', va='center',
                   color=self.colors['accent'],
                   fontweight='bold',
                   alpha=input_alpha)
        
        # Model (centrum)
        if progress > 0.15:
            model_alpha = min(1.0, (progress - 0.15) / 0.15)
            
            model_box = FancyBboxPatch(
                (35, 58), 30, 15,
                boxstyle="round,pad=1",
                facecolor='#1a2a4a',
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.9 * model_alpha
            )
            ax.add_patch(model_box)
            
            ax.text(50, 68, '🧠', fontsize=35, ha='center', va='center',
                   alpha=model_alpha)
            ax.text(50, 61, 'Base Model\n(Niet getraind)', fontsize=10, ha='center', va='center',
                   color=self.colors['primary'], alpha=model_alpha)
            
            # Pijl van input naar model
            arrow = FancyArrowPatch(
                (50, 78), (50, 73),
                arrowstyle='-|>',
                mutation_scale=20,
                linewidth=2,
                color=self.colors['accent'],
                alpha=model_alpha
            )
            ax.add_artist(arrow)
        
        # Model Output (FOUT - links onder)
        if progress > 0.35:
            output_alpha = min(1.0, (progress - 0.35) / 0.15)
            
            # Pijl van model naar output
            arrow = FancyArrowPatch(
                (42, 58), (30, 48),
                arrowstyle='-|>',
                mutation_scale=25,
                linewidth=3,
                color=self.colors['error'],
                alpha=output_alpha
            )
            ax.add_artist(arrow)
            
            output_box = FancyBboxPatch(
                (5, 30), 40, 18,
                boxstyle="round,pad=1",
                facecolor='#3a1a1a',
                edgecolor=self.colors['error'],
                linewidth=3,
                alpha=0.95 * output_alpha
            )
            ax.add_patch(output_box)
            
            ax.text(25, 44, 'âŒ Model Output (Fout!)',
                   fontsize=11, ha='center', va='center',
                   color=self.colors['error'],
                   fontweight='bold',
                   alpha=output_alpha)
            
            wrong_answer = textwrap.fill(
                "Een RFC is een algemeen document in IT projecten voor het delen van informatie.",
                width=35
            )
            ax.text(25, 36, wrong_answer,
                   fontsize=9, ha='center', va='center',
                   color=self.colors['text'],
                   alpha=output_alpha * 0.9)
            
            # Shake effect voor fout antwoord
            if progress > 0.5 and progress < 0.55:
                shake = np.sin(progress * 100) * 2
                output_box.set_x(5 + shake)
        
        # Gewenst Output (CORRECT - rechts onder)
        if progress > 0.5:
            target_alpha = min(1.0, (progress - 0.5) / 0.15)
            
            target_box = FancyBboxPatch(
                (55, 30), 40, 18,
                boxstyle="round,pad=1",
                facecolor='#1a3a1a',
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * target_alpha
            )
            ax.add_patch(target_box)
            
            ax.text(75, 44, 'âœ… Gewenst Output (Correct)',
                   fontsize=11, ha='center', va='center',
                   color=self.colors['secondary'],
                   fontweight='bold',
                   alpha=target_alpha)
            
            correct_answer = textwrap.fill(
                "RFC staat voor Request for Change - een formele aanvraag voor wijziging binnen BiSL.",
                width=35
            )
            ax.text(75, 36, correct_answer,
                   fontsize=9, ha='center', va='center',
                   color=self.colors['text'],
                   alpha=target_alpha * 0.95)
        
        # Verschil indicator (groot verschil!)
        if progress > 0.7:
            diff_alpha = min(1.0, (progress - 0.7) / 0.2)
            
            # Lijnen die het verschil tonen
            ax.plot([25, 75], [39, 39], color=self.colors['highlight'],
                   linewidth=2, alpha=0.3 * diff_alpha, linestyle=':')
            
            # Grote rode X tussen beiden
            ax.text(50, 39, 'âš ï¸', fontsize=40, ha='center', va='center',
                   alpha=diff_alpha)
            
            diff_box = FancyBboxPatch(
                (35, 20), 30, 8,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['highlight'],
                edgecolor='white',
                linewidth=2,
                alpha=0.95 * diff_alpha
            )
            ax.add_patch(diff_box)
            
            ax.text(50, 24, 'Groot Verschil!',
                   fontsize=13, ha='center', va='center',
                   color='white',
                   fontweight='bold',
                   alpha=diff_alpha)
        
        # Probleem statement
        if progress > 0.82:
            problem_alpha = min(1.0, (progress - 0.82) / 0.15)
            
            problem_box = FancyBboxPatch(
                (15, 5), 70, 10,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=3,
                alpha=0.95 * problem_alpha
            )
            ax.add_patch(problem_box)
            
            ax.text(50, 12, 'ðŸŽ¯ Het Doel van Finetuning:',
                   fontsize=12, ha='center', va='center',
                   color=self.colors['accent'],
                   fontweight='bold',
                   alpha=problem_alpha)
            
            ax.text(50, 7.5, 'Het verschil tussen Model Output en Gewenst Output MINIMALISEREN',
                   fontsize=11, ha='center', va='center',
                   color=self.colors['text'],
                   alpha=problem_alpha * 0.9)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_loss_function(self, progress):
        """Stap 2: Toon loss function concept"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 95, 'Stap 4: Loss Function - Fouten Meten',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['accent'])
        
        ax.text(50, 90, 'Hoe goed komt het model output overeen met gewenst antwoord?',
                fontsize=14, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')
        
        # Model in het midden
        if progress > 0.1:
            model_alpha = min(1.0, (progress - 0.1) / 0.15)
            
            model_box = FancyBboxPatch(
                (35, 45), 30, 20,
                boxstyle="round,pad=1",
                facecolor='#1a2a4a',
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.9 * model_alpha
            )
            ax.add_patch(model_box)
            
            ax.text(50, 58, '🧠', fontsize=40, ha='center', va='center',
                    alpha=model_alpha)
            ax.text(50, 48, 'Model', fontsize=12, ha='center', va='center',
                    color=self.colors['primary'], fontweight='bold',
                    alpha=model_alpha)
        
        # Input (links)
        if progress > 0.25:
            input_alpha = min(1.0, (progress - 0.25) / 0.15)
            
            input_box = FancyBboxPatch(
                (5, 50), 25, 10,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.9 * input_alpha
            )
            ax.add_patch(input_box)
            
            ax.text(17.5, 55, 'Wat is RFC?',
                    fontsize=10, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=input_alpha)
            
            # Pijl naar model
            arrow = FancyArrowPatch(
                (30, 55), (35, 55),
                arrowstyle='-|>',
                mutation_scale=20,
                linewidth=2,
                color=self.colors['secondary'],
                alpha=input_alpha
            )
            ax.add_artist(arrow)
        
        # Model output (rechts boven - fout)
        if progress > 0.4:
            output_alpha = min(1.0, (progress - 0.4) / 0.15)
            
            output_box = FancyBboxPatch(
                (70, 60), 25, 12,
                boxstyle="round,pad=0.5",
                facecolor='#3a1a1a',
                edgecolor=self.colors['error'],
                linewidth=2,
                alpha=0.9 * output_alpha
            )
            ax.add_patch(output_box)
            
            ax.text(82.5, 68, 'âŒ Model Output',
                    fontsize=9, ha='center', va='center',
                    color=self.colors['error'],
                    fontweight='bold',
                    alpha=output_alpha)
            
            wrapped_output = textwrap.fill("RFC is een document...", width=20)
            ax.text(82.5, 63, wrapped_output,
                    fontsize=8, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=output_alpha * 0.8)
            
            # Pijl van model
            arrow = FancyArrowPatch(
                (65, 58), (70, 64),
                arrowstyle='-|>',
                mutation_scale=20,
                linewidth=2,
                color=self.colors['error'],
                alpha=output_alpha
            )
            ax.add_artist(arrow)
        
        # Expected output (rechts onder - correct)
        if progress > 0.5:
            expected_alpha = min(1.0, (progress - 0.5) / 0.15)
            
            expected_box = FancyBboxPatch(
                (70, 42), 25, 12,
                boxstyle="round,pad=0.5",
                facecolor='#1a3a1a',
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.9 * expected_alpha
            )
            ax.add_patch(expected_box)
            
            ax.text(82.5, 50, 'âœ… Gewenst Output',
                    fontsize=9, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold',
                    alpha=expected_alpha)
            
            wrapped_expected = textwrap.fill("RFC = Request for Change...", width=20)
            ax.text(82.5, 45, wrapped_expected,
                    fontsize=8, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=expected_alpha * 0.8)
        
        # Loss calculation (tussen beide outputs)
        if progress > 0.65:
            loss_alpha = min(1.0, (progress - 0.65) / 0.25)
            
            # Comparison arrows
            arrow1 = FancyArrowPatch(
                (82.5, 60), (82.5, 54),
                arrowstyle='<->',
                mutation_scale=25,
                linewidth=3,
                color=self.colors['accent'],
                alpha=loss_alpha
            )
            ax.add_artist(arrow1)
            
            # Loss value box
            loss_box = FancyBboxPatch(
                (75, 55), 15, 6,
                boxstyle="round,pad=0.3",
                facecolor=self.colors['accent'],
                edgecolor='white',
                linewidth=2,
                alpha=0.95 * loss_alpha
            )
            ax.add_patch(loss_box)
            
            ax.text(82.5, 58, 'ðŸ“Š Loss = 0.82',
                    fontsize=11, ha='center', va='center',
                    color='white',
                    fontweight='bold',
                    alpha=loss_alpha)
        
        # Explanation
        if progress > 0.85:
            exp_alpha = min(1.0, (progress - 0.85) / 0.15)
            
            explanation = "Lagere loss = betere overeenkomst\nDoel: Loss minimaliseren"
            ax.text(50, 25, explanation,
                    fontsize=13, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.8',
                            facecolor=self.colors['bg_light'],
                            edgecolor=self.colors['accent'],
                            linewidth=2,
                            alpha=0.9),
                    color=self.colors['accent'],
                    alpha=exp_alpha,
                    fontweight='bold')
        
        # Formula hint
        if progress > 0.9:
            formula_alpha = (progress - 0.9) / 0.1
            ax.text(50, 10, 'Cross-Entropy Loss: â„’ = -Î£ y log(Å·)',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['dim'],
                    alpha=0.7 * formula_alpha,
                    style='italic',
                    family='monospace')
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_gradient_updates(self, progress):
        """Stap 3: Toon gradient descent process"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 95, 'Stap 5: Gradient Updates - Leren!',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['highlight'])
        
        ax.text(50, 90, 'Model gewichten aanpassen om loss te verlagen',
                fontsize=14, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')
        
        # Loss landscape (simplified 2D visualization)
        if progress > 0.1:
            landscape_alpha = min(1.0, (progress - 0.1) / 0.2)
            
            # Draw loss curve - INVERSE valley (berg met dal in het midden)
            x = np.linspace(10, 90, 100)
            # Create a valley shape (U-vorm) - laag in het midden, hoog aan de zijkanten
            y_center = 45  # Centrum van de curve
            y_min = 30     # Laagste punt (dal)
            y_max = 70     # Hoogste punten (bergtoppen)
            
            # Parabool: hoog aan de zijkanten, laag in het midden
            # y = a*(x - center)^2 + min_height
            x_normalized = (x - 50) / 40  # Normaliseer -1 tot 1
            y = y_min + (y_max - y_min) * (x_normalized ** 2)
            
            ax.plot(x, y, color=self.colors['primary'], linewidth=3, 
                   alpha=landscape_alpha, zorder=1)
            
            # Fill under curve
            ax.fill_between(x, y, 20, color=self.colors['primary'], 
                           alpha=0.2 * landscape_alpha, zorder=0)
            
            # Labels - hoog aan de zijkanten
            ax.text(15, 73, 'Hoge Loss', fontsize=11, ha='left', va='center',
                   color=self.colors['error'], fontweight='bold',
                   alpha=landscape_alpha)
            ax.text(85, 73, 'Hoge Loss', fontsize=11, ha='right', va='center',
                   color=self.colors['error'], fontweight='bold',
                   alpha=landscape_alpha)
            # Label - laag in het midden (dal)
            ax.text(50, 23, 'Optimale Weights\n(Lage Loss)', 
                   fontsize=11, ha='center', va='top',
                   color=self.colors['secondary'], fontweight='bold',
                   alpha=landscape_alpha)
        
        # Ball rolling down (gradient descent visualization)
        if progress > 0.3:
            descent_progress = min(1.0, (progress - 0.3) / 0.6)
            
            # Position along the curve
            t = descent_progress
            # Ease-out curve voor smooth landing
            t_eased = 1 - (1 - t) ** 3
            
            # Start linksboven (x=15), eindig in het dal (x=50)
            current_x = 15 + t_eased * 35  # Van 15 naar 50
            # Bereken y positie op de curve
            x_normalized = (current_x - 50) / 40
            current_y = y_min + (y_max - y_min) * (x_normalized ** 2)
            
            # Ball
            ball_size = 800
            ax.scatter([current_x], [current_y], s=ball_size, 
                      c=self.colors['highlight'], edgecolors='white',
                      linewidths=3, zorder=10, alpha=0.9)
            
            # Trail effect - laat zien waar de bal vandaan komt
            if t > 0.1:
                trail_x = np.linspace(15, current_x, 20)
                # Bereken y voor elk punt op het trail
                trail_x_norm = (trail_x - 50) / 40
                trail_y = y_min + (y_max - y_min) * (trail_x_norm ** 2)
                ax.plot(trail_x, trail_y, color=self.colors['highlight'],
                       linewidth=4, alpha=0.5, zorder=5, linestyle='--')
            
            # Gradient arrow - wijst OMLAAG naar het dal (richting lagere loss)
            if t < 0.95:
                # Bereken de richting van de gradient (afgeleid van de parabool)
                # dy/dx = 2a(x - center), wijst naar het dal
                gradient_direction = -2 * (x_normalized)  # Negatief = naar centrum
                
                # Arrow altijd naar beneden en naar het centrum
                arrow_length = 10
                dx = arrow_length * (0.5 if current_x < 50 else -0.5)  # Naar centrum
                dy = -arrow_length * 0.7  # Naar beneden
                
                arrow = FancyArrowPatch(
                    (current_x, current_y),
                    (current_x + dx, current_y + dy),
                    arrowstyle='-|>',
                    mutation_scale=30,
                    linewidth=4,
                    color=self.colors['accent'],
                    alpha=0.8,
                    zorder=9
                )
                ax.add_artist(arrow)
                
                # Gradient label (âˆ‡L wijst naar beneden = loss daalt)
                ax.text(current_x + dx + 2, current_y + dy - 2, 'âˆ‡L',
                       fontsize=16, ha='center', va='center',
                       color=self.colors['accent'],
                       fontweight='bold')
        
        # Iteration counter
        if progress > 0.4:
            iteration = int((progress - 0.4) * 100)
            iter_alpha = min(1.0, (progress - 0.4) / 0.1)
            
            ax.text(50, 15, f'Iteratie: {iteration}',
                   fontsize=14, ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.5',
                           facecolor=self.colors['bg_light'],
                           edgecolor=self.colors['highlight'],
                           linewidth=2,
                           alpha=0.9),
                   color=self.colors['highlight'],
                   fontweight='bold',
                   alpha=iter_alpha)
        
        # Learning rate hint
        if progress > 0.9:
            lr_alpha = (progress - 0.9) / 0.1
            ax.text(50, 8, '⚙️ Learning Rate (Î±): hoe grote stappen we nemen',
                   fontsize=11, ha='center', va='center',
                   color=self.colors['dim'],
                   alpha=0.7 * lr_alpha,
                   style='italic')
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_weight_adjustment(self, progress):
        """Stap 4: Toon weight aanpassingen visueel"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 95, 'Stap 6: Weight Adjustment',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['purple'])
        
        ax.text(50, 90, 'Honderden miljoenen parameters worden aangepast',
                fontsize=14, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')
        
        # Before weights (links)
        if progress > 0.1:
            before_alpha = min(1.0, (progress - 0.1) / 0.2)
            
            ax.text(25, 78, 'ðŸ”µ Voor Finetuning', fontsize=14, ha='center',
                   color=self.colors['primary'], fontweight='bold',
                   alpha=before_alpha)
            
            # Weight bars
            num_bars = 30
            bar_width = 0.8
            bar_x_offset = 15
            
            for i in range(num_bars):
                if progress > 0.15 + i * 0.005:
                    bar_alpha = min(1.0, (progress - (0.15 + i * 0.005)) / 0.1)
                    
                    weight_val = self.base_weights[i]
                    bar_height = abs(weight_val) * 10
                    bar_y = 50 - bar_height / 2
                    
                    bar_color = self.colors['primary'] if weight_val > 0 else self.colors['error']
                    
                    bar = patches.Rectangle(
                        (bar_x_offset + i * bar_width, bar_y),
                        bar_width * 0.9, bar_height,
                        facecolor=bar_color,
                        edgecolor='none',
                        alpha=0.6 * bar_alpha
                    )
                    ax.add_patch(bar)
        
        # After weights (rechts)
        if progress > 0.5:
            after_alpha = min(1.0, (progress - 0.5) / 0.2)
            
            ax.text(75, 78, 'ðŸŸ¢ Na Finetuning', fontsize=14, ha='center',
                   color=self.colors['secondary'], fontweight='bold',
                   alpha=after_alpha)
            
            # Weight bars
            bar_x_offset = 65
            
            for i in range(num_bars):
                if progress > 0.55 + i * 0.005:
                    bar_alpha = min(1.0, (progress - (0.55 + i * 0.005)) / 0.1)
                    
                    weight_val = self.finetuned_weights[i]
                    bar_height = abs(weight_val) * 10
                    bar_y = 50 - bar_height / 2
                    
                    bar_color = self.colors['secondary'] if weight_val > 0 else self.colors['accent']
                    
                    bar = patches.Rectangle(
                        (bar_x_offset + i * bar_width, bar_y),
                        bar_width * 0.9, bar_height,
                        facecolor=bar_color,
                        edgecolor='none',
                        alpha=0.7 * bar_alpha
                    )
                    ax.add_patch(bar)
        
        # Comparison arrows
        if progress > 0.8:
            arrow_alpha = min(1.0, (progress - 0.8) / 0.15)
            
            # Show some changes
            for i in [5, 12, 20, 28]:
                y_before = 50
                y_after = 50
                
                arrow = FancyArrowPatch(
                    (bar_x_offset - 25 + i * bar_width, y_before),
                    (bar_x_offset + i * bar_width, y_after),
                    arrowstyle='->',
                    mutation_scale=15,
                    linewidth=1.5,
                    color=self.colors['accent'],
                    alpha=0.4 * arrow_alpha,
                    linestyle='--'
                )
                ax.add_artist(arrow)
        
        # Stats box
        if progress > 0.85:
            stats_alpha = min(1.0, (progress - 0.85) / 0.15)
            
            stats_box = FancyBboxPatch(
                (30, 20), 40, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['purple'],
                linewidth=3,
                alpha=0.95 * stats_alpha
            )
            ax.add_patch(stats_box)
            
            stats_text = "ðŸ“Š Parameters aangepast\n7B model â‰ˆ 7.000.000.000\n13B model â‰ˆ 13.000.000.000"
            ax.text(50, 27.5, stats_text,
                   fontsize=11, ha='center', va='center',
                   color=self.colors['text'],
                   alpha=stats_alpha)
        
        # Explanation
        if progress > 0.92:
            exp_alpha = (progress - 0.92) / 0.08
            ax.text(50, 8, 'ðŸ’¡ Kleine aanpassingen â†’ Grote impact op gedrag',
                   fontsize=12, ha='center', va='center',
                   color=self.colors['accent'],
                   alpha=0.8 * exp_alpha,
                   style='italic')
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_finetuned_model(self, progress):
        """Stap 5: Toon gefinetuned model"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 95, 'Stap 7: Gefinetuned Model! ðŸŽ‰',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['secondary'])
        
        ax.text(50, 90, 'Het model is nu een BiSL specialist',
                fontsize=14, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')
        
        # Model met glow effect
        if progress > 0.1:
            model_alpha = min(1.0, (progress - 0.1) / 0.2)
            
            # Pulse/glow effect
            if progress > 0.4:
                pulse = 1 + 0.1 * np.sin(progress * 15)
            else:
                pulse = 1.0
            
            # Glow circles
            for radius in [25, 22, 19]:
                glow_alpha = model_alpha * 0.15 * pulse
                glow = Circle((50, 50), radius, 
                            facecolor='none',
                            edgecolor=self.colors['secondary'],
                            linewidth=2,
                            alpha=glow_alpha)
                ax.add_patch(glow)
            
            model_box = FancyBboxPatch(
                (32, 37), 36 * pulse, 26 * pulse,
                boxstyle="round,pad=1.5",
                facecolor='#1a3a2a',
                edgecolor=self.colors['secondary'],
                linewidth=4,
                alpha=0.95 * model_alpha
            )
            ax.add_patch(model_box)
            
            ax.text(50, 55, '🧠✨', fontsize=60, ha='center', va='center',
                    alpha=model_alpha)
            
            ax.text(50, 42, 'BiSL Expert Model',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold',
                    alpha=model_alpha)
        
        # Capabilities (sterren verschijnen)
        capabilities = [
            ('âœ… BiSL terminologie', 20, 70, 0.3),
            ('âœ… Procesbeschrijvingen', 80, 70, 0.35),
            ('âœ… Best practices', 20, 30, 0.4),
            ('âœ… Nederlandse context', 80, 30, 0.45)
        ]
        
        for text, x, y, delay in capabilities:
            if progress > delay:
                cap_alpha = min(1.0, (progress - delay) / 0.15)
                
                cap_box = FancyBboxPatch(
                    (x - 12, y - 4), 24, 8,
                    boxstyle="round,pad=0.5",
                    facecolor='#1a3a1a',
                    edgecolor=self.colors['secondary'],
                    linewidth=2,
                    alpha=0.9 * cap_alpha
                )
                ax.add_patch(cap_box)
                
                ax.text(x, y, text,
                        fontsize=11, ha='center', va='center',
                        color=self.colors['text'],
                        fontweight='bold',
                        alpha=cap_alpha)
        
        # Performance metrics
        if progress > 0.65:
            metrics_alpha = min(1.0, (progress - 0.65) / 0.25)
            
            metrics_box = FancyBboxPatch(
                (25, 10), 50, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=3,
                alpha=0.95 * metrics_alpha
            )
            ax.add_patch(metrics_box)
            
            ax.text(50, 18, 'ðŸ“ˆ Performance Verbetering', fontsize=12, 
                   ha='center', va='center',
                   color=self.colors['highlight'], fontweight='bold',
                   alpha=metrics_alpha)
            
            ax.text(50, 14, 'Accuraatheid: 65% â†’ 92% | Relevantie: +40%',
                   fontsize=10, ha='center', va='center',
                   color=self.colors['text'],
                   alpha=metrics_alpha)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_comparison(self, progress):
        """Stap 6: Side-by-side vergelijking"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 95, 'Stap 8: Voor vs Na Vergelijking',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['highlight'])
        
        ax.text(50, 90, 'Hetzelfde model, maar met domeinkennis',
                fontsize=14, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')
        
        # Vraag (bovenaan)
        if progress > 0.05:
            q_alpha = min(1.0, (progress - 0.05) / 0.1)
            
            q_box = FancyBboxPatch(
                (15, 78), 70, 8,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=2,
                alpha=0.9 * q_alpha
            )
            ax.add_patch(q_box)
            
            ax.text(50, 82, 'â“ "Wat is het verschil tussen standaard en normale wijziging?"',
                   fontsize=11, ha='center', va='center',
                   color=self.colors['accent'],
                   fontweight='bold',
                   alpha=q_alpha)
        
        # Base Model response (links)
        if progress > 0.2:
            base_alpha = min(1.0, (progress - 0.2) / 0.2)
            
            ax.text(25, 70, 'ðŸ”´ Base Model', fontsize=13, ha='center',
                   color=self.colors['error'], fontweight='bold',
                   alpha=base_alpha)
            
            base_box = FancyBboxPatch(
                (5, 35), 40, 30,
                boxstyle="round,pad=1",
                facecolor='#2a1a1a',
                edgecolor=self.colors['error'],
                linewidth=2,
                alpha=0.9 * base_alpha
            )
            ax.add_patch(base_box)
            
            base_response = textwrap.fill(
                "Een standaard wijziging is een reguliere aanpassing, "
                "terwijl een normale wijziging meer gebruikelijk is. "
                "Dit zijn algemene termen in projectmanagement.",
                width=35
            )
            
            ax.text(25, 50, base_response,
                   fontsize=9, ha='center', va='center',
                   color=self.colors['text'],
                   alpha=base_alpha * 0.9)
            
            # Waarschuwing
            if progress > 0.35:
                warn_alpha = min(1.0, (progress - 0.35) / 0.15)
                ax.text(25, 38, 'âš ï¸ Vaag & onnauwkeurig',
                       fontsize=9, ha='center', va='center',
                       color=self.colors['error'],
                       alpha=warn_alpha * 0.8,
                       style='italic')
        
        # Finetuned Model response (rechts)
        if progress > 0.5:
            ft_alpha = min(1.0, (progress - 0.5) / 0.2)
            
            ax.text(75, 70, 'ðŸŸ¢ Finetuned Model', fontsize=13, ha='center',
                   color=self.colors['secondary'], fontweight='bold',
                   alpha=ft_alpha)
            
            ft_box = FancyBboxPatch(
                (55, 35), 40, 30,
                boxstyle="round,pad=1",
                facecolor='#1a3a1a',
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * ft_alpha
            )
            ax.add_patch(ft_box)
            
            ft_response = textwrap.fill(
                "Binnen BiSL: Standaard wijzigingen zijn vooraf "
                "goedgekeurd en laag risico. Normale wijzigingen "
                "vereisen CAB beoordeling en autorisatie. "
                "Standaard = sneller, Normaal = meer controle.",
                width=35
            )
            
            ax.text(75, 50, ft_response,
                   fontsize=9, ha='center', va='center',
                   color=self.colors['text'],
                   alpha=ft_alpha * 0.95)
            
            # Check
            if progress > 0.65:
                check_alpha = min(1.0, (progress - 0.65) / 0.15)
                ax.text(75, 38, 'âœ… Nauwkeurig & specifiek',
                       fontsize=9, ha='center', va='center',
                       color=self.colors['secondary'],
                       alpha=check_alpha * 0.9,
                       fontweight='bold')
        
        # Scores
        if progress > 0.8:
            score_alpha = min(1.0, (progress - 0.8) / 0.2)
            
            # Base score
            ax.text(25, 28, 'ðŸ“Š Score: 4/10', fontsize=11, ha='center',
                   bbox=dict(boxstyle='round,pad=0.4',
                           facecolor=self.colors['error'],
                           alpha=0.3),
                   color=self.colors['error'],
                   fontweight='bold',
                   alpha=score_alpha)
            
            # Finetuned score
            ax.text(75, 28, 'ðŸ“Š Score: 9.5/10', fontsize=11, ha='center',
                   bbox=dict(boxstyle='round,pad=0.4',
                           facecolor=self.colors['secondary'],
                           alpha=0.3),
                   color=self.colors['secondary'],
                   fontweight='bold',
                   alpha=score_alpha)
        
        # Key takeaway
        if progress > 0.9:
            takeaway_alpha = (progress - 0.9) / 0.1
            
            ax.text(50, 15, 'ðŸ’¡ Finetuning = Model wordt domeinexpert zonder algemene kennis te verliezen',
                   fontsize=12, ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.6',
                           facecolor=self.colors['bg_light'],
                           edgecolor=self.colors['highlight'],
                           linewidth=2,
                           alpha=0.9),
                   color=self.colors['highlight'],
                   alpha=takeaway_alpha,
                   fontweight='bold')
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_azure_local_setup(self, progress):
        """Stap 7: Azure AI Studio en Local LLM setup"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 95, 'Stap 9: Finetuning in de Praktijk',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'])
        
        ax.text(50, 90, 'Azure AI Studio vs Local LLM - Beide kunnen!',
                fontsize=14, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')
        
        # Azure AI Studio (links)
        if progress > 0.1:
            azure_alpha = min(1.0, (progress - 0.1) / 0.2)
            
            azure_box = FancyBboxPatch(
                (5, 25), 40, 55,
                boxstyle="round,pad=1.5",
                facecolor='#1a2a3a',
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.95 * azure_alpha
            )
            ax.add_patch(azure_box)
            
            # Azure logo area
            ax.text(25, 75, 'â˜ï¸', fontsize=50, ha='center', va='center',
                   alpha=azure_alpha)
            
            ax.text(25, 68, 'Azure AI Studio', fontsize=14, ha='center',
                   color=self.colors['primary'], fontweight='bold',
                   alpha=azure_alpha)
            
            # Features
            azure_features = [
                ('âœ“ Cloud-based', 60),
                ('âœ“ GPU compute', 54),
                ('âœ“ Managed service', 48),
                ('âœ“ GPT-4, Phi-3', 42),
                ('âœ“ Auto-scaling', 36)
            ]
            
            for feat, y in azure_features:
                if progress > 0.2 + (60 - y) * 0.01:
                    feat_alpha = min(1.0, (progress - (0.2 + (60 - y) * 0.01)) / 0.1)
                    ax.text(25, y, feat, fontsize=10, ha='center',
                           color=self.colors['text'],
                           alpha=feat_alpha * azure_alpha)
        
        # Local LLM (rechts)
        if progress > 0.4:
            local_alpha = min(1.0, (progress - 0.4) / 0.2)
            
            local_box = FancyBboxPatch(
                (55, 25), 40, 55,
                boxstyle="round,pad=1.5",
                facecolor='#2a1a3a',
                edgecolor=self.colors['purple'],
                linewidth=3,
                alpha=0.95 * local_alpha
            )
            ax.add_patch(local_box)
            
            # Computer icon
            ax.text(75, 75, 'ðŸ’»', fontsize=50, ha='center', va='center',
                   alpha=local_alpha)
            
            ax.text(75, 68, 'Local LLM', fontsize=14, ha='center',
                   color=self.colors['purple'], fontweight='bold',
                   alpha=local_alpha)
            
            # Features
            local_features = [
                ('âœ“ On-premise', 60),
                ('âœ“ Privacy control', 54),
                ('âœ“ LLaMA, Mistral', 48),
                ('âœ“ LoRA, QLoRA', 42),
                ('âœ“ Cost efficient', 36)
            ]
            
            for feat, y in local_features:
                if progress > 0.5 + (60 - y) * 0.01:
                    feat_alpha = min(1.0, (progress - (0.5 + (60 - y) * 0.01)) / 0.1)
                    ax.text(75, y, feat, fontsize=10, ha='center',
                           color=self.colors['text'],
                           alpha=feat_alpha * local_alpha)
        
        # Workflow (onder Azure)
        if progress > 0.65:
            workflow_alpha = min(1.0, (progress - 0.65) / 0.2)
            
            azure_steps = "1. Upload data\n2. Select model\n3. Configure\n4. Deploy"
            ax.text(25, 30, azure_steps, fontsize=9, ha='center', va='center',
                   color=self.colors['dim'],
                   alpha=workflow_alpha * 0.8,
                   style='italic')
        
        # Workflow (onder Local)
        if progress > 0.75:
            workflow_alpha = min(1.0, (progress - 0.75) / 0.2)
            
            local_steps = "1. Setup env\n2. Load model\n3. Train script\n4. Evaluate"
            ax.text(75, 30, local_steps, fontsize=9, ha='center', va='center',
                   color=self.colors['dim'],
                   alpha=workflow_alpha * 0.8,
                   style='italic')
        
        # Bottom comparison
        if progress > 0.85:
            comp_alpha = min(1.0, (progress - 0.85) / 0.15)
            
            comp_box = FancyBboxPatch(
                (10, 8), 80, 12,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.9 * comp_alpha
            )
            ax.add_patch(comp_box)
            
            ax.text(50, 16, 'âš–ï¸ Keuze afweging', fontsize=12, ha='center',
                   color=self.colors['secondary'], fontweight='bold',
                   alpha=comp_alpha)
            
            comparison_text = "Azure: Sneller, minder technisch • Local: Meer controle, privacy"
            ax.text(50, 11, comparison_text, fontsize=10, ha='center',
                   color=self.colors['text'],
                   alpha=comp_alpha * 0.9)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def add_status_indicator(self, is_animating):
        """Voeg status indicator toe"""
        if is_animating:
            status_text = "ðŸŽ¬ ANIMEREN..."
            status_color = self.colors['accent']
        else:
            status_text = "â¸ GEPAUZEERD - Druk SPATIE voor volgende stap"
            status_color = self.colors['secondary']
        
        self.fig.text(0.5, 0.98, status_text,
                     fontsize=12, ha='center', va='top',
                     bbox=dict(boxstyle='round,pad=0.4', 
                             facecolor='#1a1a1a',
                             edgecolor=status_color,
                             linewidth=2,
                             alpha=0.9),
                     color=status_color,
                     fontweight='bold')
        
        # Voortgangsbalk
        step_num = max(0, self.current_step)
        total_steps = len(self.step_names) - 1
        progress_pct = step_num / total_steps if total_steps > 0 else 0
        
        # Achtergrond balk
        bar_width = 0.6
        bar_x = 0.2
        bar_y = 0.01
        
        bar_bg = patches.Rectangle(
            (bar_x, bar_y), bar_width, 0.01,
            transform=self.fig.transFigure,
            facecolor='#2a2a2a',
            edgecolor=self.colors['dim'],
            linewidth=1
        )
        self.fig.patches.append(bar_bg)
        
        # Voortgang
        if progress_pct > 0:
            bar_fg = patches.Rectangle(
                (bar_x, bar_y), bar_width * progress_pct, 0.01,
                transform=self.fig.transFigure,
                facecolor=status_color,
                edgecolor='none'
            )
            self.fig.patches.append(bar_fg)
        
        # Stap nummer
        self.fig.text(0.5, 0.015, f'Stap {step_num + 1} / {total_steps + 1}',
                     fontsize=10, ha='center', va='center',
                     color=self.colors['text'],
                     alpha=0.7)
    
    def show(self):
        """Toon de visualisatie"""
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
    """Main functie"""
    print("=" * 80)
    print("FINETUNING JOURNEY VISUALISATIE - AI Kennissessie")
    print("=" * 80)
    print("\nðŸŽ“ Deze presentatie legt uit hoe Finetuning werkt:")
    print("  1. Base Model - Pre-trained algemeen model")
    print("  2. Training Data - Voorbeelden van gewenst gedrag")
    print("  3. Model Predictions - Het probleem: foute antwoorden!")
    print("  4. Loss Function - Hoe goed is de output?")
    print("  5. Gradient Updates - Leerproces visualisatie")
    print("  6. Weight Adjustment - Parameters worden aangepast")
    print("  7. Finetuned Model - Het resultaat!")
    print("  8. Comparison - Voor vs Na vergelijking")
    print("  9. Azure AI / Local Setup - Praktische implementatie")
    print("\nðŸ’¡ Stap 3 is NIEUW:")
    print("  â†’ Maakt het probleem visueel voordat we naar Loss gaan")
    print("  â†’ Laat zien: Model maakt fouten â†’ We moeten verschil verkleinen")
    print("  â†’ Brug tussen 'Training Data' en 'Loss Function'")
    print("\n⚙️ Technische Details:")
    print("  • Azure AI Studio: Cloud-based, managed, GPT-4/Phi-3")
    print("  • Local LLM: On-premise, LLaMA/Mistral, LoRA/QLoRA")
    print("  • Training: 100-10.000+ voorbeelden typisch")
    print("  • Models: 7B-70B parameters")
    print("\nðŸŽ® Bediening:")
    print("  SPATIE    : Start/Volgende stap")
    print("  B         : Vorige stap")
    print("  R         : Reset naar begin")
    print("  F         : Volledig scherm")
    print("  Q of ESC  : Afsluiten")
    print("\nðŸ’¡ Voorbeeld Use Case:")
    print("  • Doel: BiSL-specialist maken van algemeen model")
    print("  • Data: BiSL terminologie, processen, best practices")
    print("  • Resultaat: Model dat BiSL begrippen nauwkeurig uitlegt")
    print("\nDruk op SPATIE om te beginnen...")
    print("=" * 80)
    
    viz = FinetuningVisualization()
    viz.show()

if __name__ == "__main__":
    main()