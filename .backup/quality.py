"""
AI Quality Governance - Kennissessie Slotstuk
Van AI-kennis naar Kwaliteitszorg in de Praktijk

Dit is het sluitstuk na Vector/RAG/Finetuning presentaties.
Geen terugblik, maar vooruitkijken: wat betekent dit voor onze datastromen?

Controls:
- SPACE: Start/Volgende stap
- B: Vorige stap  
- Q/ESC: Afsluiten
- F: Volledig scherm
- R: Reset animatie
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge, Arc
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

class AIQualityGovernance:
    def __init__(self):
        self.fig = plt.figure(figsize=(16, 9), facecolor='#0a0a0a')
        
        # Animation state
        self.current_step = -1
        self.step_names = [
            'Landing',
            'Decision Moment',
            'Quality Dimensions Matrix',
            'Data Quality Pipeline',
            'Stakeholder Web',
            'Governance Questions',
            'Risk Patterns',
            'Integration Reality',
            'Continuous Loop'
        ]
        
        self.is_animating = False
        self.animation = None
        
        # Kleuren schema - consistent met andere presentaties
        self.colors = {
            'primary': '#3B82F6',      # Blauw
            'secondary': '#10B981',    # Groen
            'accent': '#F59E0B',       # Oranje
            'highlight': '#EC4899',    # Roze
            'purple': '#A78BFA',       # Paars
            'cyan': '#06B6D4',         # Cyaan
            'text': '#F0F0F0',
            'dim': '#6B7280',
            'bg': '#0a0a0a',
            'bg_light': '#1a1a1a',
            'warning': '#EF4444',      # Rood
            'success': '#10B981'       # Groen
        }
        
        # AI Scenarios met hun specifieke kwaliteitseisen
        self.scenarios = {
            'RAG': {
                'color': self.colors['primary'],
                'icon': '🔍',
                'name': 'RAG',
                'quality_focus': ['Bronkwaliteit', 'Actualiteit', 'Relevantie', 'Traceerbaarheid']
            },
            'Finetuning': {
                'color': self.colors['secondary'],
                'icon': '🎯',
                'name': 'Finetuning',
                'quality_focus': ['Datavolume', 'Representativiteit', 'Labeling', 'Bias']
            },
            'Hybrid': {
                'color': self.colors['purple'],
                'icon': '⚡',
                'name': 'Hybrid',
                'quality_focus': ['Balans', 'Complexiteit', 'Onderhoud', 'Consistentie']
            }
        }
        
        # Stakeholders - breed spectrum!
        self.stakeholders = [
            {'name': 'Informatie-\nmanagement', 'angle': 0, 'color': self.colors['primary'], 'distance': 3},
            {'name': 'Data-\ngovernance', 'angle': 45, 'color': self.colors['secondary'], 'distance': 3.2},
            {'name': 'Privacy &\nSecurity', 'angle': 90, 'color': self.colors['warning'], 'distance': 3},
            {'name': 'Business\nOwners', 'angle': 135, 'color': self.colors['accent'], 'distance': 3.2},
            {'name': 'ICT /\nDevelopment', 'angle': 180, 'color': self.colors['cyan'], 'distance': 3},
            {'name': 'Compliance &\nAudit', 'angle': 225, 'color': self.colors['purple'], 'distance': 3.2},
            {'name': 'Gebruikers &\nExperts', 'angle': 270, 'color': self.colors['highlight'], 'distance': 3},
            {'name': 'Architectuur', 'angle': 315, 'color': '#60A5FA', 'distance': 3.2}
        ]
        
        # Governance vragen per domein
        self.governance_questions = {
            'Data': [
                'Waar komen de data vandaan?',
                'Hoe actueel moeten ze zijn?',
                'Wie is eigenaar van de data?',
                'Wat is de kwaliteit van brondata?'
            ],
            'Model': [
                'Welke AI-aanpak past het beste?',
                'Hoe valideren we output?',
                'Wat zijn acceptabele foutenmarges?',
                'Hoe monitoren we performance?'
            ],
            'Proces': [
                'Wie autoriseert wijzigingen?',
                'Hoe testen we voor productie?',
                'Wat is de rollback strategie?',
                'Hoe documenteren we?'
            ],
            'Mensen': [
                'Wie heeft welke rol?',
                'Wat is ieders verantwoordelijkheid?',
                'Hoe communiceren we?',
                'Wie neemt besluiten?'
            ],
            'Ethics': [
                'Is output eerlijk & onbevooroordeeld?',
                'Kunnen we uitleg geven?',
                'Respecteren we privacy?',
                'Wat zijn de risico\'s?'
            ]
        }
        
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
                self.reset_animation()
        elif event.key in ['q', 'escape']:
            plt.close()
        elif event.key == 'f':
            manager = plt.get_current_fig_manager()
            manager.full_screen_toggle()
    
    def show_landing_page(self):
        """Opening scherm"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Hoofdtitel met glow effect
        title_box = FancyBboxPatch(
            (10, 50), 80, 30,
            boxstyle="round,pad=2",
            facecolor='#1a1a1a',
            edgecolor=self.colors['primary'],
            linewidth=4,
            alpha=0.95
        )
        ax.add_patch(title_box)
        
        # Gradient effect met meerdere teksten
        ax.text(50, 70, 'Van AI-kennis', 
                fontsize=42, fontweight='bold', ha='center', va='center',
                color=self.colors['primary'])
        
        ax.text(50, 62, 'naar', 
                fontsize=28, ha='center', va='center',
                color=self.colors['text'], alpha=0.6, style='italic')
        
        ax.text(50, 53, 'Kwaliteitszorg', 
                fontsize=42, fontweight='bold', ha='center', va='center',
                color=self.colors['secondary'])
        
        # Subtitel
        ax.text(50, 40, 'Wat betekent dit nu écht voor onze datastromen?',
                fontsize=20, ha='center', va='center',
                color=self.colors['highlight'], alpha=0.9)
        
        # Key insight box
        insight_box = FancyBboxPatch(
            (15, 20), 70, 12,
            boxstyle="round,pad=1",
            facecolor=self.colors['bg_light'],
            edgecolor=self.colors['accent'],
            linewidth=3,
            alpha=0.9
        )
        ax.add_patch(insight_box)
        
        ax.text(50, 28, '💡 Je snapt nu Vectors, RAG en Finetuning...',
                fontsize=14, ha='center', va='center',
                color=self.colors['text'], alpha=0.8)
        
        ax.text(50, 24, 'Maar welke vragen moet je stellen voordat je begint?',
                fontsize=14, ha='center', va='center',
                color=self.colors['accent'], fontweight='bold')
        
        # Instructies
        ax.text(50, 8, '✨ Druk op SPATIE om te starten',
                fontsize=16, ha='center', va='center',
                color=self.colors['dim'], alpha=0.8)
        
        ax.text(50, 4, 'Controls: SPACE=Volgende | B=Vorige | R=Reset | F=Fullscreen | Q=Quit',
                fontsize=11, ha='center', va='center',
                color=self.colors['dim'], alpha=0.6)
        
        plt.tight_layout()
        plt.draw()
    
    def start_next_step(self):
        """Start animatie naar volgende stap"""
        if self.current_step < len(self.step_names) - 1:
            self.current_step += 1
            self.is_animating = True
            
            print(f"\n{'='*60}")
            print(f"Stap {self.current_step + 1}/{len(self.step_names)}: {self.step_names[self.current_step]}")
            print(f"{'='*60}")
            
            # Start smooth animation
            self.animation = FuncAnimation(
                self.fig, 
                self.animate_step,
                frames=60,
                interval=30,
                repeat=False,
                blit=False
            )
            plt.draw()
    
    def previous_step(self):
        """Ga terug naar vorige stap"""
        if self.current_step > -1:
            self.current_step -= 1
            self.draw_current_step_static()
    
    def reset_animation(self):
        """Reset naar begin"""
        self.current_step = -1
        self.show_landing_page()
    
    def animate_step(self, frame):
        """Animeer huidige stap"""
        progress = frame / 59.0  # 0 tot 1
        
        if self.current_step == 0:
            self.draw_decision_moment(progress)
        elif self.current_step == 1:
            self.draw_quality_dimensions(progress)
        elif self.current_step == 2:
            self.draw_data_pipeline(progress)
        elif self.current_step == 3:
            self.draw_stakeholder_web(progress)
        elif self.current_step == 4:
            self.draw_governance_questions(progress)
        elif self.current_step == 5:
            self.draw_risk_patterns(progress)
        elif self.current_step == 6:
            self.draw_integration_reality(progress)
        elif self.current_step == 7:
            self.draw_continuous_loop(progress)
        
        if frame == 59:
            self.is_animating = False
            print("✓ Stap compleet - Druk op SPATIE voor volgende stap")
        
        return []
    
    def draw_current_step_static(self):
        """Teken huidige stap als statisch beeld"""
        if self.current_step == -1:
            self.show_landing_page()
        elif self.current_step == 0:
            self.draw_decision_moment(1.0)
        elif self.current_step == 1:
            self.draw_quality_dimensions(1.0)
        elif self.current_step == 2:
            self.draw_data_pipeline(1.0)
        elif self.current_step == 3:
            self.draw_stakeholder_web(1.0)
        elif self.current_step == 4:
            self.draw_governance_questions(1.0)
        elif self.current_step == 5:
            self.draw_risk_patterns(1.0)
        elif self.current_step == 6:
            self.draw_integration_reality(1.0)
        elif self.current_step == 7:
            self.draw_continuous_loop(1.0)
    
    def add_status_indicator(self, is_animating=True):
        """Voeg status indicator toe onderaan"""
        status_text = "⏵ Animeren..." if is_animating else "⏸ Druk SPATIE voor volgende stap"
        self.fig.text(0.5, 0.02, status_text,
                     ha='center', va='bottom',
                     fontsize=10, color=self.colors['dim'], alpha=0.6)
        
        # Progress indicator
        progress_text = f"Stap {self.current_step + 1}/{len(self.step_names)}"
        self.fig.text(0.95, 0.02, progress_text,
                     ha='right', va='bottom',
                     fontsize=10, color=self.colors['dim'], alpha=0.6)
    
    def draw_decision_moment(self, progress):
        """Stap 1: Het beslismoment - welke AI aanpak?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        title_alpha = min(1.0, progress * 2)
        ax.text(50, 95, 'Stap 1: Het Beslismoment',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['text'], alpha=title_alpha)
        
        ax.text(50, 89, 'Welke AI-aanpak kies je voor jouw datastroom?',
                fontsize=16, ha='center', va='top',
                color=self.colors['dim'], alpha=title_alpha * 0.8, style='italic')
        
        # Centrale vraag cirkel
        if progress > 0.15:
            q_alpha = min(1.0, (progress - 0.15) / 0.15)
            
            center_circle = Circle((50, 60), 8, 
                                  facecolor=self.colors['bg_light'],
                                  edgecolor=self.colors['highlight'],
                                  linewidth=4, alpha=0.95 * q_alpha)
            ax.add_patch(center_circle)
            
            ax.text(50, 62, '❓',
                   fontsize=40, ha='center', va='center',
                   alpha=q_alpha)
            
            ax.text(50, 56, 'Welke\naanpak?',
                   fontsize=12, ha='center', va='center',
                   color=self.colors['text'], alpha=q_alpha,
                   fontweight='bold')
        
        # Drie scenario's - uitwaaierend vanuit centrum
        scenarios_data = [
            ('RAG', 20, 60, self.colors['primary'], '🔍'),
            ('Finetuning', 50, 35, self.colors['secondary'], '🎯'),
            ('Hybrid', 80, 60, self.colors['purple'], '⚡')
        ]
        
        for idx, (name, x, y, color, icon) in enumerate(scenarios_data):
            delay = 0.3 + idx * 0.15
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.15)
                
                # Lijn vanuit centrum
                line_x = [50 + 8 * np.cos(np.radians((idx - 1) * 60)), x]
                line_y = [60 + 8 * np.sin(np.radians((idx - 1) * 60)), y]
                ax.plot(line_x, line_y, color=color, linewidth=2, 
                       alpha=alpha * 0.5, linestyle='--')
                
                # Scenario box
                box = FancyBboxPatch(
                    (x - 10, y - 6), 20, 12,
                    boxstyle="round,pad=0.8",
                    facecolor=self.colors['bg_light'],
                    edgecolor=color,
                    linewidth=3,
                    alpha=0.95 * alpha
                )
                ax.add_patch(box)
                
                ax.text(x, y + 3, icon,
                       fontsize=24, ha='center', va='center',
                       alpha=alpha)
                
                ax.text(x, y - 1, name,
                       fontsize=13, ha='center', va='center',
                       color=color, fontweight='bold',
                       alpha=alpha)
        
        # Key insight onderaan
        if progress > 0.7:
            insight_alpha = min(1.0, (progress - 0.7) / 0.3)
            
            insight_box = FancyBboxPatch(
                (15, 10), 70, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=2,
                alpha=0.9 * insight_alpha
            )
            ax.add_patch(insight_box)
            
            ax.text(50, 20, '⚡ Elk scenario heeft eigen kwaliteitseisen',
                   fontsize=14, ha='center', va='center',
                   color=self.colors['accent'], fontweight='bold',
                   alpha=insight_alpha)
            
            ax.text(50, 15, 'De keuze bepaalt wát je moet controleren en mét wie',
                   fontsize=12, ha='center', va='center',
                   color=self.colors['text'], alpha=insight_alpha * 0.8)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_quality_dimensions(self, progress):
        """Stap 2: Quality Dimensions Matrix - wat moet je per scenario checken?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 96, 'Stap 2: Kwaliteitsdimensies per Scenario',
                fontsize=26, fontweight='bold', ha='center', va='top',
                color=self.colors['text'])
        
        ax.text(50, 91, 'Verschillende aanpakken, verschillende aandachtspunten',
                fontsize=14, ha='center', va='top',
                color=self.colors['dim'], alpha=0.8, style='italic')
        
        # Matrix grid - 3 scenarios x 5 dimensies
        dimensions = [
            ('📊 Data\nKwaliteit', 'volledigheid, correctheid, actualiteit'),
            ('🔒 Privacy &\nSecurity', 'AVG, toegangscontrole, audit trails'),
            ('⚖️ Bias &\nEthics', 'eerlijkheid, transparantie, verantwoording'),
            ('🎯 Performance &\nAccuracy', 'foutenmarges, validatie, monitoring'),
            ('🔧 Onderhoud &\nGovernance', 'eigenaarschap, procedures, documentatie')
        ]
        
        scenarios = ['RAG', 'Finetuning', 'Hybrid']
        scenario_colors = [self.colors['primary'], self.colors['secondary'], self.colors['purple']]
        
        # Teken matrix
        start_x = 20
        col_width = 25
        row_height = 15
        start_y = 75
        
        # Kolomheaders (scenarios)
        if progress > 0.1:
            header_alpha = min(1.0, (progress - 0.1) / 0.15)
            for i, (scenario, color) in enumerate(zip(scenarios, scenario_colors)):
                x = start_x + (i + 1) * col_width
                
                icon = ['🔍', '🎯', '⚡'][i]
                ax.text(x, start_y + 5, f'{icon} {scenario}',
                       fontsize=11, ha='center', va='center',
                       color=color, fontweight='bold',
                       alpha=header_alpha)
        
        # Rijen met dimensies en checks
        for row_idx, (dim_name, dim_desc) in enumerate(dimensions):
            row_delay = 0.25 + row_idx * 0.12
            if progress > row_delay:
                row_alpha = min(1.0, (progress - row_delay) / 0.12)
                
                y = start_y - (row_idx + 1) * row_height
                
                # Dimensie naam (links)
                ax.text(start_x - 2, y, dim_name,
                       fontsize=9, ha='right', va='center',
                       color=self.colors['text'], alpha=row_alpha,
                       fontweight='bold')
                
                # Beschrijving (klein, onder naam)
                wrapped_desc = textwrap.fill(dim_desc, width=20)
                ax.text(start_x - 2, y - 3.5, wrapped_desc,
                       fontsize=7, ha='right', va='center',
                       color=self.colors['dim'], alpha=row_alpha * 0.7)
                
                # Check marks per scenario (variërend per relevantie)
                relevance = [
                    [3, 2, 3],  # Data Quality: RAG hoog, Finetuning medium, Hybrid hoog
                    [2, 1, 2],  # Privacy: medium, laag, medium
                    [1, 3, 2],  # Bias: laag, hoog, medium
                    [2, 3, 3],  # Performance: medium, hoog, hoog
                    [2, 2, 3]   # Governance: medium, medium, hoog
                ]
                
                for col_idx, rel in enumerate(relevance[row_idx]):
                    x = start_x + (col_idx + 1) * col_width
                    
                    # Teken indicator
                    if rel == 3:
                        indicator = '●●●'
                        alpha_mult = 1.0
                    elif rel == 2:
                        indicator = '●●○'
                        alpha_mult = 0.7
                    else:
                        indicator = '●○○'
                        alpha_mult = 0.4
                    
                    ax.text(x, y, indicator,
                           fontsize=14, ha='center', va='center',
                           color=scenario_colors[col_idx],
                           alpha=row_alpha * alpha_mult)
        
        # Legend
        if progress > 0.85:
            legend_alpha = min(1.0, (progress - 0.85) / 0.15)
            
            ax.text(50, 8, '●●● = Kritisch  |  ●●○ = Belangrijk  |  ●○○ = Relevant',
                   fontsize=10, ha='center', va='center',
                   color=self.colors['dim'], alpha=legend_alpha * 0.8)
        
        # Insight
        if progress > 0.75:
            insight_alpha = min(1.0, (progress - 0.75) / 0.15)
            
            ax.text(50, 3, '💡 Geen scenario is "makkelijk" - elk vraagt andere aandacht',
                   fontsize=11, ha='center', va='center',
                   color=self.colors['accent'], fontweight='bold',
                   alpha=insight_alpha)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_data_pipeline(self, progress):
        """Stap 3: Data Quality Pipeline - waar zitten de checkpoints?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 96, 'Stap 3: Data Quality Checkpoints',
                fontsize=26, fontweight='bold', ha='center', va='top',
                color=self.colors['text'])
        
        ax.text(50, 91, 'Waar in je datastroom moet je kwaliteit waarborgen?',
                fontsize=14, ha='center', va='top',
                color=self.colors['dim'], alpha=0.8, style='italic')
        
        # Pipeline flow (van links naar rechts)
        pipeline_stages = [
            {'name': 'Bron\nData', 'x': 10, 'y': 60, 'checks': ['Volledigheid', 'Actualiteit', 'Eigenaarschap'], 
             'color': self.colors['warning'], 'icon': '📊'},
            {'name': 'Data\nPreparatie', 'x': 27, 'y': 60, 'checks': ['Opschoning', 'Transformatie', 'Validatie'],
             'color': self.colors['primary'], 'icon': '🔧'},
            {'name': 'Model\nInput', 'x': 44, 'y': 60, 'checks': ['Format', 'Encoding', 'Bias check'],
             'color': self.colors['secondary'], 'icon': '⚙️'},
            {'name': 'AI\nVerwerking', 'x': 61, 'y': 60, 'checks': ['Monitoring', 'Logging', 'Explainability'],
             'color': self.colors['purple'], 'icon': '🤖'},
            {'name': 'Output\nValidatie', 'x': 78, 'y': 60, 'checks': ['Accuracy', 'Bias', 'Safety'],
             'color': self.colors['highlight'], 'icon': '✓'},
        ]
        
        # Teken pipeline flow
        for idx, stage in enumerate(pipeline_stages):
            delay = 0.15 + idx * 0.15
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.15)
                
                # Stage box
                box = FancyBboxPatch(
                    (stage['x'] - 5, stage['y'] - 5), 10, 10,
                    boxstyle="round,pad=0.5",
                    facecolor=self.colors['bg_light'],
                    edgecolor=stage['color'],
                    linewidth=3,
                    alpha=0.95 * alpha
                )
                ax.add_patch(box)
                
                # Icon en naam
                ax.text(stage['x'], stage['y'] + 1, stage['icon'],
                       fontsize=20, ha='center', va='center',
                       alpha=alpha)
                
                ax.text(stage['x'], stage['y'] - 3, stage['name'],
                       fontsize=8, ha='center', va='center',
                       color=stage['color'], fontweight='bold',
                       alpha=alpha)
                
                # Checks onder stage
                check_y = stage['y'] - 15
                for check_idx, check in enumerate(stage['checks']):
                    check_alpha = min(1.0, (progress - delay - 0.05 * check_idx) / 0.1)
                    if check_alpha > 0:
                        ax.text(stage['x'], check_y - check_idx * 4, f'• {check}',
                               fontsize=7, ha='center', va='center',
                               color=self.colors['text'], alpha=check_alpha * 0.8)
                
                # Pijl naar volgende stage
                if idx < len(pipeline_stages) - 1:
                    arrow_alpha = min(1.0, (progress - delay) / 0.1)
                    if arrow_alpha > 0:
                        next_stage = pipeline_stages[idx + 1]
                        arrow = FancyArrowPatch(
                            (stage['x'] + 5, stage['y']),
                            (next_stage['x'] - 5, next_stage['y']),
                            arrowstyle='->,head_width=0.4,head_length=0.8',
                            color=self.colors['dim'],
                            linewidth=2,
                            alpha=arrow_alpha * 0.6
                        )
                        ax.add_patch(arrow)
        
        # Feedback loop (bottom)
        if progress > 0.8:
            feedback_alpha = min(1.0, (progress - 0.8) / 0.2)
            
            # Gebogen pijl terug
            arc = Arc((44, 35), 60, 30, angle=0, theta1=180, theta2=360,
                     color=self.colors['secondary'], linewidth=2, 
                     linestyle='--', alpha=feedback_alpha * 0.7)
            ax.add_patch(arc)
            
            ax.text(44, 22, '🔄 Continuous Monitoring & Improvement',
                   fontsize=10, ha='center', va='center',
                   color=self.colors['secondary'], fontweight='bold',
                   alpha=feedback_alpha)
        
        # Key insight
        if progress > 0.85:
            insight_alpha = min(1.0, (progress - 0.85) / 0.15)
            
            insight_box = FancyBboxPatch(
                (10, 5), 80, 10,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=2,
                alpha=0.9 * insight_alpha
            )
            ax.add_patch(insight_box)
            
            ax.text(50, 10, '⚠️ Elk checkpoint vraagt andere expertise en verantwoordelijkheden',
                   fontsize=12, ha='center', va='center',
                   color=self.colors['accent'], fontweight='bold',
                   alpha=insight_alpha)
            
            ax.text(50, 7, 'Dit is geen ICT-taak alleen - dit vraagt samenwerking over de hele keten',
                   fontsize=10, ha='center', va='center',
                   color=self.colors['text'], alpha=insight_alpha * 0.8)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_stakeholder_web(self, progress):
        """Stap 4: Stakeholder Web - wie moet betrokken zijn? (BREED SPECTRUM!)"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(-10, 110)
        ax.set_ylim(-10, 110)
        
        # Titel
        ax.text(50, 98, 'Stap 4: Het Stakeholder Web',
                fontsize=26, fontweight='bold', ha='center', va='top',
                color=self.colors['text'])
        
        ax.text(50, 93, 'AI kwaliteit is geen ICT-ding - het vraagt ketenbrede afstemming',
                fontsize=14, ha='center', va='top',
                color=self.colors['accent'], alpha=0.9, fontweight='bold')
        
        # Centrum: AI Quality
        if progress > 0.1:
            center_alpha = min(1.0, (progress - 0.1) / 0.15)
            
            center_circle = Circle((50, 50), 6, 
                                  facecolor=self.colors['bg_light'],
                                  edgecolor=self.colors['highlight'],
                                  linewidth=4, alpha=0.95 * center_alpha)
            ax.add_patch(center_circle)
            
            ax.text(50, 51, 'AI\nQuality',
                   fontsize=11, ha='center', va='center',
                   color=self.colors['highlight'], fontweight='bold',
                   alpha=center_alpha)
        
        # Stakeholders in cirkel rondom centrum
        for idx, stakeholder in enumerate(self.stakeholders):
            delay = 0.25 + idx * 0.08
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.1)
                
                # Bereken positie
                angle_rad = np.radians(stakeholder['angle'])
                distance = stakeholder['distance'] * 12  # schaal voor visualisatie
                x = 50 + distance * np.cos(angle_rad)
                y = 50 + distance * np.sin(angle_rad)
                
                # Lijn naar centrum
                line_alpha = min(1.0, (progress - delay) / 0.08)
                if line_alpha > 0:
                    ax.plot([50, x], [50, y], 
                           color=stakeholder['color'], 
                           linewidth=1.5, 
                           alpha=line_alpha * 0.4,
                           linestyle='-')
                
                # Stakeholder node
                node = Circle((x, y), 4,
                            facecolor=self.colors['bg_light'],
                            edgecolor=stakeholder['color'],
                            linewidth=2.5,
                            alpha=0.95 * alpha)
                ax.add_patch(node)
                
                # Label
                ax.text(x, y, stakeholder['name'],
                       fontsize=8, ha='center', va='center',
                       color=stakeholder['color'], fontweight='bold',
                       alpha=alpha)
        
        # Interconnections (sommige stakeholders moeten ook met elkaar praten!)
        if progress > 0.75:
            connection_alpha = min(1.0, (progress - 0.75) / 0.2)
            
            # Belangrijke verbindingen tussen stakeholders
            key_connections = [
                (0, 1),  # Informatie mgmt <-> Data governance
                (1, 2),  # Data governance <-> Privacy
                (3, 4),  # Business <-> ICT
                (4, 7),  # ICT <-> Architectuur
                (5, 6),  # Compliance <-> Gebruikers
                (0, 3),  # Informatie mgmt <-> Business
            ]
            
            for conn_idx, (idx1, idx2) in enumerate(key_connections):
                conn_delay = connection_alpha - conn_idx * 0.05
                if conn_delay > 0:
                    s1 = self.stakeholders[idx1]
                    s2 = self.stakeholders[idx2]
                    
                    angle_rad1 = np.radians(s1['angle'])
                    angle_rad2 = np.radians(s2['angle'])
                    x1 = 50 + s1['distance'] * 12 * np.cos(angle_rad1)
                    y1 = 50 + s1['distance'] * 12 * np.sin(angle_rad1)
                    x2 = 50 + s2['distance'] * 12 * np.cos(angle_rad2)
                    y2 = 50 + s2['distance'] * 12 * np.sin(angle_rad2)
                    
                    ax.plot([x1, x2], [y1, y2],
                           color=self.colors['dim'],
                           linewidth=1,
                           alpha=conn_delay * 0.3,
                           linestyle=':')
        
        # Key insight
        if progress > 0.85:
            insight_alpha = min(1.0, (progress - 0.85) / 0.15)
            
            insight_box = FancyBboxPatch(
                (10, 3), 80, 10,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['warning'],
                linewidth=2,
                alpha=0.9 * insight_alpha
            )
            ax.add_patch(insight_box)
            
            ax.text(50, 9, '⚡ Elk stakeholder heeft eigen perspectief en verantwoordelijkheid',
                   fontsize=11, ha='center', va='center',
                   color=self.colors['warning'], fontweight='bold',
                   alpha=insight_alpha)
            
            ax.text(50, 5.5, 'Zonder goede afstemming loop je risico\'s - zowel operationeel als compliance',
                   fontsize=10, ha='center', va='center',
                   color=self.colors['text'], alpha=insight_alpha * 0.8)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_governance_questions(self, progress):
        """Stap 5: Governance Questions - welke vragen MOETEN gesteld worden?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 96, 'Stap 5: De Kwaliteitsvragen',
                fontsize=26, fontweight='bold', ha='center', va='top',
                color=self.colors['text'])
        
        ax.text(50, 91, 'Wat moet je ALTIJD vragen voordat je AI met datastromen inzet?',
                fontsize=13, ha='center', va='top',
                color=self.colors['dim'], alpha=0.8, style='italic')
        
        # 5 domeinen met vragen
        domains = ['Data', 'Model', 'Proces', 'Mensen', 'Ethics']
        domain_colors = [
            self.colors['primary'],
            self.colors['secondary'],
            self.colors['accent'],
            self.colors['purple'],
            self.colors['highlight']
        ]
        
        # Grid layout: 2 rijen, eerste rij 3 kolommen, tweede rij 2 kolommen
        positions = [
            (18, 65),  # Data
            (50, 65),  # Model
            (82, 65),  # Proces
            (33, 30),  # Mensen
            (67, 30)   # Ethics
        ]
        
        for idx, (domain, color, pos) in enumerate(zip(domains, domain_colors, positions)):
            delay = 0.15 + idx * 0.15
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.15)
                
                x, y = pos
                
                # Domain box
                box = FancyBboxPatch(
                    (x - 13, y + 8), 26, 7,
                    boxstyle="round,pad=0.5",
                    facecolor=self.colors['bg_light'],
                    edgecolor=color,
                    linewidth=3,
                    alpha=0.95 * alpha
                )
                ax.add_patch(box)
                
                ax.text(x, y + 11.5, domain,
                       fontsize=12, ha='center', va='center',
                       color=color, fontweight='bold',
                       alpha=alpha)
                
                # Vragen onder domain
                questions = self.governance_questions[domain]
                for q_idx, question in enumerate(questions):
                    q_delay = delay + 0.05 + q_idx * 0.03
                    if progress > q_delay:
                        q_alpha = min(1.0, (progress - q_delay) / 0.08)
                        
                        q_y = y - q_idx * 4.2
                        
                        wrapped_q = textwrap.fill(f'• {question}', width=28)
                        ax.text(x, q_y, wrapped_q,
                               fontsize=7.5, ha='center', va='center',
                               color=self.colors['text'], alpha=q_alpha * 0.85,
                               linespacing=1.4)
        
        # Key insight
        if progress > 0.85:
            insight_alpha = min(1.0, (progress - 0.85) / 0.15)
            
            insight_box = FancyBboxPatch(
                (10, 3), 80, 9,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=2,
                alpha=0.9 * insight_alpha
            )
            ax.add_patch(insight_box)
            
            ax.text(50, 8.5, '💡 Deze vragen MOETEN antwoorden hebben voordat je begint',
                   fontsize=12, ha='center', va='center',
                   color=self.colors['accent'], fontweight='bold',
                   alpha=insight_alpha)
            
            ax.text(50, 5.5, 'Geen antwoord = risico op kwaliteitsissues, compliance problemen of bias',
                   fontsize=10, ha='center', va='center',
                   color=self.colors['text'], alpha=insight_alpha * 0.8)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_risk_patterns(self, progress):
        """Stap 6: Risk Patterns - wat gaat er vaak mis?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 96, 'Stap 6: Wat Gaat Er Vaak Mis?',
                fontsize=26, fontweight='bold', ha='center', va='top',
                color=self.colors['warning'])
        
        ax.text(50, 91, 'Veelvoorkomende risicopatronen bij AI met datastromen',
                fontsize=13, ha='center', va='top',
                color=self.colors['dim'], alpha=0.8, style='italic')
        
        # Risk patterns in 3x2 grid
        risk_patterns = [
            {
                'name': '📊 Data Drift',
                'desc': 'Brondata verandert,\nmodel niet geüpdatet',
                'impact': 'Hoog',
                'color': self.colors['warning']
            },
            {
                'name': '🎭 Hidden Bias',
                'desc': 'Bias in trainingsdata\nwordt niet gedetecteerd',
                'impact': 'Hoog',
                'color': self.colors['warning']
            },
            {
                'name': '👻 Ownership Gap',
                'desc': 'Onduidelijk wie\nverantwoordelijk is',
                'impact': 'Medium',
                'color': self.colors['accent']
            },
            {
                'name': '🔧 Poor Monitoring',
                'desc': 'Geen monitoring van\noutput kwaliteit',
                'impact': 'Hoog',
                'color': self.colors['warning']
            },
            {
                'name': '📝 Documentation',
                'desc': 'Besluiten en keuzes\nniet gedocumenteerd',
                'impact': 'Medium',
                'color': self.colors['accent']
            },
            {
                'name': '🤝 Silos',
                'desc': 'Teams werken langs\nelkaar heen',
                'impact': 'Hoog',
                'color': self.colors['warning']
            }
        ]
        
        # Grid positions
        cols = 3
        rows = 2
        start_x = 15
        start_y = 72
        col_width = 28
        row_height = 30
        
        for idx, risk in enumerate(risk_patterns):
            delay = 0.15 + idx * 0.12
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.12)
                
                col = idx % cols
                row = idx // cols
                
                x = start_x + col * col_width
                y = start_y - row * row_height
                
                # Risk box
                box = FancyBboxPatch(
                    (x, y - 8), 24, 16,
                    boxstyle="round,pad=0.7",
                    facecolor=self.colors['bg_light'],
                    edgecolor=risk['color'],
                    linewidth=2.5,
                    alpha=0.95 * alpha
                )
                ax.add_patch(box)
                
                # Risk name
                ax.text(x + 12, y + 4, risk['name'],
                       fontsize=10, ha='center', va='center',
                       color=risk['color'], fontweight='bold',
                       alpha=alpha)
                
                # Description
                ax.text(x + 12, y - 1, risk['desc'],
                       fontsize=8, ha='center', va='center',
                       color=self.colors['text'], alpha=alpha * 0.8,
                       linespacing=1.3)
                
                # Impact badge
                impact_color = self.colors['warning'] if risk['impact'] == 'Hoog' else self.colors['accent']
                ax.text(x + 12, y - 6.5, f"Impact: {risk['impact']}",
                       fontsize=7, ha='center', va='center',
                       bbox=dict(boxstyle='round,pad=0.3',
                               facecolor=impact_color,
                               alpha=0.3),
                       color=impact_color, fontweight='bold',
                       alpha=alpha)
        
        # Key insight
        if progress > 0.8:
            insight_alpha = min(1.0, (progress - 0.8) / 0.2)
            
            insight_box = FancyBboxPatch(
                (10, 4), 80, 10,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.9 * insight_alpha
            )
            ax.add_patch(insight_box)
            
            ax.text(50, 10, '✅ Deze risico\'s zijn te managen met de juiste governance',
                   fontsize=12, ha='center', va='center',
                   color=self.colors['secondary'], fontweight='bold',
                   alpha=insight_alpha)
            
            ax.text(50, 6.5, 'Maar dan moet je ze wel identificeren én de juiste mensen betrekken',
                   fontsize=10, ha='center', va='center',
                   color=self.colors['text'], alpha=insight_alpha * 0.8)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_integration_reality(self, progress):
        """Stap 7: Integration Reality - hoe ziet dit eruit in de praktijk?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 96, 'Stap 7: De Praktijk - Alles Hangt Samen',
                fontsize=26, fontweight='bold', ha='center', va='top',
                color=self.colors['text'])
        
        ax.text(50, 91, 'AI kwaliteit is geen losse activiteit - het zit in je hele werkwijze',
                fontsize=13, ha='center', va='top',
                color=self.colors['dim'], alpha=0.8, style='italic')
        
        # Centrale integratie hub
        if progress > 0.1:
            hub_alpha = min(1.0, (progress - 0.1) / 0.15)
            
            center = Circle((50, 50), 9,
                           facecolor=self.colors['bg_light'],
                           edgecolor=self.colors['highlight'],
                           linewidth=4, alpha=0.95 * hub_alpha)
            ax.add_patch(center)
            
            ax.text(50, 52, 'AI Quality\nIntegration',
                   fontsize=11, ha='center', va='center',
                   color=self.colors['highlight'], fontweight='bold',
                   alpha=hub_alpha,
                   linespacing=1.3)
        
        # Integratiepunten rondom centrum
        integration_points = [
            {'name': 'BiSL\nProcessen', 'angle': 0, 'icon': '📋', 'color': self.colors['primary']},
            {'name': 'Change\nManagement', 'angle': 45, 'icon': '🔄', 'color': self.colors['secondary']},
            {'name': 'Security &\nPrivacy', 'angle': 90, 'icon': '🔒', 'color': self.colors['warning']},
            {'name': 'Service\nCatalogue', 'angle': 135, 'icon': '📖', 'color': self.colors['accent']},
            {'name': 'Architecture\nGovernance', 'angle': 180, 'icon': '🏛️', 'color': self.colors['cyan']},
            {'name': 'Data\nGovernance', 'angle': 225, 'icon': '📊', 'color': self.colors['purple']},
            {'name': 'Incident\nManagement', 'angle': 270, 'icon': '🚨', 'color': '#EF4444'},
            {'name': 'Continuous\nImprovement', 'angle': 315, 'icon': '📈', 'color': '#10B981'}
        ]
        
        for idx, point in enumerate(integration_points):
            delay = 0.25 + idx * 0.08
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.1)
                
                # Bereken positie
                angle_rad = np.radians(point['angle'])
                distance = 32
                x = 50 + distance * np.cos(angle_rad)
                y = 50 + distance * np.sin(angle_rad)
                
                # Lijn naar centrum
                ax.plot([50, x], [50, y],
                       color=point['color'],
                       linewidth=2,
                       alpha=alpha * 0.5,
                       linestyle='-')
                
                # Integration point
                point_circle = Circle((x, y), 6,
                                    facecolor=self.colors['bg_light'],
                                    edgecolor=point['color'],
                                    linewidth=2.5,
                                    alpha=0.95 * alpha)
                ax.add_patch(point_circle)
                
                # Icon
                ax.text(x, y + 1.5, point['icon'],
                       fontsize=14, ha='center', va='center',
                       alpha=alpha)
                
                # Label buiten cirkel
                label_distance = 8
                label_x = 50 + (distance + label_distance) * np.cos(angle_rad)
                label_y = 50 + (distance + label_distance) * np.sin(angle_rad)
                
                ax.text(label_x, label_y, point['name'],
                       fontsize=8, ha='center', va='center',
                       color=point['color'], fontweight='bold',
                       alpha=alpha,
                       linespacing=1.2)
        
        # Interconnection lines (sommige punten hangen direct samen)
        if progress > 0.75:
            conn_alpha = min(1.0, (progress - 0.75) / 0.2)
            
            key_links = [
                (0, 1),  # BiSL <-> Change Mgmt
                (2, 5),  # Security <-> Data Governance
                (4, 5),  # Architecture <-> Data Governance
                (6, 7),  # Incident <-> Continuous Improvement
            ]
            
            for link_idx, (idx1, idx2) in enumerate(key_links):
                p1 = integration_points[idx1]
                p2 = integration_points[idx2]
                
                angle_rad1 = np.radians(p1['angle'])
                angle_rad2 = np.radians(p2['angle'])
                x1 = 50 + 32 * np.cos(angle_rad1)
                y1 = 50 + 32 * np.sin(angle_rad1)
                x2 = 50 + 32 * np.cos(angle_rad2)
                y2 = 50 + 32 * np.sin(angle_rad2)
                
                ax.plot([x1, x2], [y1, y2],
                       color=self.colors['dim'],
                       linewidth=1,
                       alpha=conn_alpha * 0.3,
                       linestyle=':')
        
        # Key insight
        if progress > 0.85:
            insight_alpha = min(1.0, (progress - 0.85) / 0.15)
            
            insight_box = FancyBboxPatch(
                (10, 3), 80, 10,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=2,
                alpha=0.9 * insight_alpha
            )
            ax.add_patch(insight_box)
            
            ax.text(50, 9, '⚡ AI Quality is geen add-on - het moet geïntegreerd zijn',
                   fontsize=12, ha='center', va='center',
                   color=self.colors['highlight'], fontweight='bold',
                   alpha=insight_alpha)
            
            ax.text(50, 5.5, 'Gebruik bestaande processen en governance structuren als fundament',
                   fontsize=10, ha='center', va='center',
                   color=self.colors['text'], alpha=insight_alpha * 0.8)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_continuous_loop(self, progress):
        """Stap 8: Continuous Quality Loop - het eindigt nooit!"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        title_alpha = min(1.0, progress * 2)
        ax.text(50, 96, 'Slotstuk: Quality is een Continu Proces',
                fontsize=26, fontweight='bold', ha='center', va='top',
                color=self.colors['text'], alpha=title_alpha)
        
        ax.text(50, 91, 'AI met datastromen vraagt permanente aandacht',
                fontsize=13, ha='center', va='top',
                color=self.colors['dim'], alpha=title_alpha * 0.8, style='italic')
        
        # Circulair proces (PDCA-achtig maar voor AI Quality)
        loop_stages = [
            {'name': 'Plan', 'desc': 'Definieer kwaliteitseisen\nBetrek stakeholders\nStel governance in', 
             'angle': 90, 'color': self.colors['primary'], 'icon': '📋'},
            {'name': 'Build', 'desc': 'Implementeer checkpoints\nValideer datastromen\nTest grondig', 
             'angle': 0, 'color': self.colors['secondary'], 'icon': '🔧'},
            {'name': 'Monitor', 'desc': 'Track performance\nDetecteer afwijkingen\nLog beslissingen', 
             'angle': 270, 'color': self.colors['accent'], 'icon': '📊'},
            {'name': 'Improve', 'desc': 'Analyseer feedback\nOptimaliseer processen\nUpdate documentatie', 
             'angle': 180, 'color': self.colors['purple'], 'icon': '📈'}
        ]
        
        # Teken circulair proces
        radius = 22
        center_x, center_y = 50, 55
        
        for idx, stage in enumerate(loop_stages):
            delay = 0.15 + idx * 0.15
            if progress > delay:
                alpha = min(1.0, (progress - delay) / 0.15)
                
                # Positie berekenen
                angle_rad = np.radians(stage['angle'])
                x = center_x + radius * np.cos(angle_rad)
                y = center_y + radius * np.sin(angle_rad)
                
                # Stage cirkel
                stage_circle = Circle((x, y), 8,
                                     facecolor=self.colors['bg_light'],
                                     edgecolor=stage['color'],
                                     linewidth=3,
                                     alpha=0.95 * alpha)
                ax.add_patch(stage_circle)
                
                # Icon en naam
                ax.text(x, y + 2, stage['icon'],
                       fontsize=20, ha='center', va='center',
                       alpha=alpha)
                
                ax.text(x, y - 2, stage['name'],
                       fontsize=10, ha='center', va='center',
                       color=stage['color'], fontweight='bold',
                       alpha=alpha)
                
                # Beschrijving buiten cirkel
                desc_distance = 15
                desc_x = center_x + (radius + desc_distance) * np.cos(angle_rad)
                desc_y = center_y + (radius + desc_distance) * np.sin(angle_rad)
                
                wrapped_desc = textwrap.fill(stage['desc'], width=22)
                ax.text(desc_x, desc_y, wrapped_desc,
                       fontsize=8, ha='center', va='center',
                       color=self.colors['text'], alpha=alpha * 0.8,
                       linespacing=1.4)
                
                # Pijl naar volgende stage
                next_idx = (idx + 1) % len(loop_stages)
                next_angle = np.radians(loop_stages[next_idx]['angle'])
                
                # Gebogen pijl
                arc_angle_start = stage['angle'] - 45
                arc_angle_end = loop_stages[next_idx]['angle'] + 45
                
                if progress > delay + 0.1:
                    arrow_alpha = min(1.0, (progress - delay - 0.1) / 0.1)
                    
                    # Simpele rechte pijl (gebogen is complex in matplotlib)
                    next_x = center_x + radius * np.cos(next_angle)
                    next_y = center_y + radius * np.sin(next_angle)
                    
                    # Bereken tussenposities voor gebogen effect
                    mid_angle = np.radians((stage['angle'] + loop_stages[next_idx]['angle']) / 2)
                    mid_radius = radius + 3
                    mid_x = center_x + mid_radius * np.cos(mid_angle)
                    mid_y = center_y + mid_radius * np.sin(mid_angle)
                    
                    arrow = FancyArrowPatch(
                        (x + 7 * np.cos(angle_rad - np.pi/4), y + 7 * np.sin(angle_rad - np.pi/4)),
                        (next_x - 7 * np.cos(next_angle + np.pi/4), next_y - 7 * np.sin(next_angle + np.pi/4)),
                        arrowstyle='->,head_width=0.6,head_length=1',
                        color=self.colors['highlight'],
                        linewidth=3,
                        alpha=arrow_alpha * 0.7,
                        connectionstyle="arc3,rad=0.3"
                    )
                    ax.add_patch(arrow)
        
        # Centrum: Continuous
        if progress > 0.7:
            center_alpha = min(1.0, (progress - 0.7) / 0.2)
            
            center_circle = Circle((center_x, center_y), 5,
                                  facecolor=self.colors['bg_light'],
                                  edgecolor=self.colors['highlight'],
                                  linewidth=3,
                                  alpha=0.95 * center_alpha)
            ax.add_patch(center_circle)
            
            ax.text(center_x, center_y, '🔄',
                   fontsize=16, ha='center', va='center',
                   alpha=center_alpha)
        
        # Final insight
        if progress > 0.85:
            final_alpha = min(1.0, (progress - 0.85) / 0.15)
            
            final_box = FancyBboxPatch(
                (10, 3), 80, 20,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * final_alpha
            )
            ax.add_patch(final_box)
            
            ax.text(50, 18, '🎯 Takeaway: AI Quality is ketenbrede verantwoordelijkheid',
                   fontsize=14, ha='center', va='center',
                   color=self.colors['secondary'], fontweight='bold',
                   alpha=final_alpha)
            
            key_points = [
                '✓ Stel de juiste vragen voordat je begint',
                '✓ Betrek alle stakeholders - niet alleen ICT',
                '✓ Bouw quality checkpoints in je datastroom',
                '✓ Monitor continu en verbeter waar nodig'
            ]
            
            for idx, point in enumerate(key_points):
                ax.text(50, 13 - idx * 3, point,
                       fontsize=10, ha='center', va='center',
                       color=self.colors['text'], alpha=final_alpha * 0.9)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def show(self):
        """Toon de presentatie"""
        plt.show()

def main():
    """Main entry point"""
    print("\n" + "="*80)
    print("AI QUALITY GOVERNANCE - Kennissessie Slotstuk")
    print("="*80)
    print("\n📊 Overzicht:")
    print("  Dit is het sluitstuk na Vector/RAG/Finetuning presentaties.")
    print("  Focus: Van AI-kennis naar kwaliteitszorg in de praktijk.\n")
    
    print("🎯 Stappen:")
    for i, step in enumerate(['Landing', 'Decision Moment', 'Quality Dimensions Matrix',
                             'Data Quality Pipeline', 'Stakeholder Web', 'Governance Questions',
                             'Risk Patterns', 'Integration Reality', 'Continuous Loop'], 1):
        print(f"  {i}. {step}")
    
    print("\n🎮 Bediening:")
    print("  SPATIE    : Start/Volgende stap")
    print("  B         : Vorige stap")
    print("  R         : Reset naar begin")
    print("  F         : Volledig scherm")
    print("  Q of ESC  : Afsluiten")
    
    print("\n💡 Kernboodschap:")
    print("  AI quality is geen ICT-taak alleen - het vraagt ketenbrede afstemming")
    print("  Visualiseert: stakeholders, quality checkpoints, governance vragen, risico's")
    
    print("\nDruk op SPATIE om te beginnen...")
    print("="*80 + "\n")
    
    viz = AIQualityGovernance()
    viz.show()

if __name__ == "__main__":
    main()