"""
RAG Journey Visualisatie - BiSL Kennisartikel
Cinematische stap-voor-stap animatie van tekst naar antwoord

Controls:
- SPACE: Start/Volgende stap
- B: Vorige stap
- Q/ESC: Afsluiten
- F: Volledig scherm
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from matplotlib.animation import FuncAnimation
import textwrap

# Dark mode styling
plt.style.use('dark_background')
import matplotlib
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['axes.facecolor'] = '#0a0a0a'
matplotlib.rcParams['figure.facecolor'] = '#0a0a0a'

class RAGJourneyVisualization:
    def __init__(self):
        self.fig = plt.figure(figsize=(16, 9), facecolor='#0a0a0a')
        
        # BiSL Kennisartikel (voorbeeld)
        self.artikel = """
        KENNISARTIKEL: Wijzigingsbeheer in BiSL

        Wijzigingsbeheer is een essentieel proces binnen de informatievoorziening. 
        Het doel is om wijzigingen gecontroleerd en efficiënt door te voeren.

        Binnen BiSL onderscheiden we verschillende soorten wijzigingen:
        - Standaard wijzigingen: vooraf goedgekeurde, laagrisico aanpassingen
        - Normale wijzigingen: vereisen beoordeling door het Change Advisory Board
        - Spoed wijzigingen: voor urgente situaties met versnelde procedure

        Het wijzigingsproces bestaat uit de volgende stappen:
        1. Registratie van de wijzigingsaanvraag (RFC)
        2. Beoordeling van impact en risico's
        3. Autorisatie door bevoegd gezag
        4. Implementatie van de wijziging
        5. Evaluatie en afsluiting

        Rollen in wijzigingsbeheer:
        - Change Manager: coördineert het wijzigingsproces
        - Change Advisory Board (CAB): beoordeelt normale wijzigingen
        - Informatiemanager: autoriseert wijzigingen binnen mandaat

        Kritische succesfactoren:
        - Heldere procedures en werkafspraken
        - Adequate communicatie naar stakeholders
        - Goede samenwerking tussen functioneel en technisch beheer
        - Registratie in een CMDB voor traceerbaarheid
        """
        
        # Gebruikersvraag
        self.vraag = "Wat zijn de stappen in het wijzigingsproces volgens BiSL?"
        
        # Verwacht antwoord (wat RAG zou genereren)
        self.antwoord = """
        Volgens BiSL bestaat het wijzigingsproces uit vijf stappen:

        1. **Registratie** - De wijzigingsaanvraag (RFC) wordt geregistreerd
        2. **Beoordeling** - Impact en risico's worden beoordeeld
        3. **Autorisatie** - Bevoegd gezag geeft toestemming
        4. **Implementatie** - De wijziging wordt doorgevoerd
        5. **Evaluatie** - Proces wordt geëvalueerd en afgesloten
        """
        
        # Animation state
        self.current_step = -1  # Start met landing page
        self.step_names = [
            'Landing',
            'Kennisartikel Tonen',
            'Tekst Chunking',
            'Embeddings Creëren',
            'Vector Database',
            'Gebruikersvraag',
            'Query Embedding',
            'Similarity Search',
            'Context Ophalen',
            'LLM Generatie',
            'Antwoord Tonen'
        ]
        
        self.is_animating = False
        self.animation = None
        
        # Kleuren schema
        self.colors = {
            'primary': '#3B82F6',      # Blauw
            'secondary': '#10B981',    # Groen
            'accent': '#F59E0B',       # Oranje
            'highlight': '#EC4899',    # Roze
            'text': '#F0F0F0',
            'dim': '#6B7280',
            'bg': '#0a0a0a',
            'bg_light': '#1a1a1a'
        }
        
        # Chunks (na splitting)
        self.chunks = [
            "Wijzigingsbeheer is een essentieel proces binnen de informatievoorziening. Het doel is om wijzigingen gecontroleerd en efficiënt door te voeren.",
            
            "Binnen BiSL onderscheiden we verschillende soorten wijzigingen: Standaard wijzigingen (vooraf goedgekeurde, laagrisico), Normale wijzigingen (vereisen CAB beoordeling), en Spoed wijzigingen (urgente situaties).",
            
            "Het wijzigingsproces bestaat uit vijf stappen: 1) Registratie RFC, 2) Beoordeling impact en risico's, 3) Autorisatie, 4) Implementatie, 5) Evaluatie en afsluiting.",
            
            "Rollen in wijzigingsbeheer: Change Manager coördineert het proces, Change Advisory Board beoordeelt wijzigingen, Informatiemanager autoriseert binnen mandaat.",
            
            "Kritische succesfactoren: Heldere procedures, adequate communicatie, goede samenwerking tussen functioneel en technisch beheer, CMDB registratie voor traceerbaarheid."
        ]
        
        # Welke chunk is meest relevant voor de vraag
        self.relevante_chunk_index = 2  # "Het wijzigingsproces bestaat uit..."
        
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
            edgecolor=self.colors['primary'],
            linewidth=4,
            alpha=0.95
        )
        ax.add_patch(title_box)
        
        ax.text(50, 72, 'RAG Journey', 
                fontsize=48, fontweight='bold', ha='center', va='center',
                color=self.colors['primary'])
        
        ax.text(50, 64, 'Van Kennisartikel naar Antwoord',
                fontsize=22, ha='center', va='center',
                color=self.colors['text'], alpha=0.8, style='italic')
        
        # Subtitel
        ax.text(50, 45, 'Ontdek hoe AI jouw BiSL-kennis doorzoekt',
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
        
        ax.text(50, 20, 'B = Terug  •  Q = Afsluiten  •  F = Volledig scherm',
                fontsize=12, ha='center', va='center',
                color=self.colors['dim'], style='italic')
        
        # Footer
        ax.text(50, 5, 'Stapsgewijze visualisatie van Retrieval Augmented Generation',
                fontsize=12, ha='center', va='center',
                color=self.colors['text'], alpha=0.5)
        
        plt.tight_layout()
    
    def start_next_step(self):
        """Start volgende stap"""
        if self.current_step < len(self.step_names) - 1:
            self.current_step += 1
            print(f"→ Stap {self.current_step + 1}/{len(self.step_names)}: {self.step_names[self.current_step]}")
            self.start_step_animation()
        else:
            print("✓ Laatste stap bereikt!")
    
    def previous_step(self):
        """Ga terug naar vorige stap"""
        if self.current_step > -1:
            self.current_step -= 1
            print(f"← Stap {self.current_step + 1}/{len(self.step_names)}: {self.step_names[self.current_step]}")
            
            if self.current_step == -1:
                self.show_landing_page()
            else:
                self.draw_current_step_static()
            plt.draw()
        else:
            print("✓ Al bij eerste stap!")
    
    def start_step_animation(self):
        """Start animatie voor huidige stap"""
        self.is_animating = True
        self.animation_frame = 0
        
        # Aantal frames per stap
        frames_dict = {
            -1: 30,   # Landing
            0: 60,    # Kennisartikel tonen
            1: 90,    # Chunking
            2: 80,    # Embeddings
            3: 70,    # Vector DB
            4: 50,    # Gebruikersvraag
            5: 60,    # Query embedding
            6: 100,   # Similarity search
            7: 70,    # Context ophalen
            8: 90,    # LLM generatie
            9: 80     # Antwoord tonen
        }
        
        total_frames = frames_dict.get(self.current_step, 60)
        
        self.animation = FuncAnimation(
            self.fig,
            self.animate_step,
            frames=total_frames,
            interval=30,
            blit=False,
            repeat=False
        )
        
        plt.draw()
    
    def animate_step(self, frame):
        """Animeer huidige stap"""
        # Determine progress based on frame count for current step
        if self.current_step == -1:
            pass  # Landing page is statisch
        elif self.current_step == 0:
            self.draw_kennisartikel(frame / 60)
        elif self.current_step == 1:
            self.draw_chunking(frame / 90)
        elif self.current_step == 2:
            self.draw_embeddings(frame / 80)
        elif self.current_step == 3:
            self.draw_vector_db(frame / 70)
        elif self.current_step == 4:
            self.draw_gebruikersvraag(frame / 50)
        elif self.current_step == 5:
            self.draw_query_embedding(frame / 60)
        elif self.current_step == 6:
            self.draw_similarity_search(frame / 100)
        elif self.current_step == 7:
            self.draw_context_ophalen(frame / 70)
        elif self.current_step == 8:
            self.draw_llm_generatie(frame / 90)
        elif self.current_step == 9:
            self.draw_antwoord(frame / 80)
        
        # Check of animatie klaar is
        frames_dict = {-1: 30, 0: 60, 1: 90, 2: 80, 3: 70, 4: 50, 5: 60, 6: 100, 7: 70, 8: 90, 9: 80}
        if frame >= frames_dict.get(self.current_step, 60) - 1:
            self.is_animating = False
            print(f"  ✓ Stap {self.current_step + 1} compleet. SPATIE = volgende stap")
    
    def draw_current_step_static(self):
        """Teken huidige stap statisch (gepauzeerd)"""
        if self.current_step == 0:
            self.draw_kennisartikel(1.0)
        elif self.current_step == 1:
            self.draw_chunking(1.0)
        elif self.current_step == 2:
            self.draw_embeddings(1.0)
        elif self.current_step == 3:
            self.draw_vector_db(1.0)
        elif self.current_step == 4:
            self.draw_gebruikersvraag(1.0)
        elif self.current_step == 5:
            self.draw_query_embedding(1.0)
        elif self.current_step == 6:
            self.draw_similarity_search(1.0)
        elif self.current_step == 7:
            self.draw_context_ophalen(1.0)
        elif self.current_step == 8:
            self.draw_llm_generatie(1.0)
        elif self.current_step == 9:
            self.draw_antwoord(1.0)
    
    def draw_kennisartikel(self, progress):
        """Stap 0: Toon kennisartikel met fade-in animatie"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        alpha = min(1.0, progress * 2)
        ax.text(50, 95, 'Stap 1: Het Kennisartikel',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=alpha)
        
        # Document achtergrond
        if progress > 0.2:
            doc_alpha = min(1.0, (progress - 0.2) / 0.3)
            doc_box = FancyBboxPatch(
                (10, 10), 80, 75,
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.9 * doc_alpha
            )
            ax.add_patch(doc_box)
        
        # Tekst verschijnt regel voor regel
        if progress > 0.4:
            text_progress = (progress - 0.4) / 0.6
            lines = self.artikel.strip().split('\n')
            num_lines = max(1, int(len(lines) * text_progress))
            
            displayed_text = '\n'.join(lines[:num_lines])
            
            # Wrap tekst
            wrapped_lines = []
            for line in displayed_text.split('\n'):
                if line.strip():
                    wrapped = textwrap.fill(line, width=70)
                    wrapped_lines.append(wrapped)
                else:
                    wrapped_lines.append('')
            
            final_text = '\n'.join(wrapped_lines)
            
            ax.text(50, 80, final_text,
                    fontsize=10, ha='center', va='top',
                    color=self.colors['text'],
                    family='monospace',
                    alpha=min(1.0, text_progress * 1.5))
        
        # Status indicator
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_chunking(self, progress):
        """Stap 1: Toon hoe tekst wordt opgesplitst in chunks"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 95, 'Stap 2: Tekst Chunking',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['secondary'])
        
        ax.text(50, 90, 'Artikel wordt opgedeeld in beheersbare stukken',
                fontsize=14, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')
        
        # Fase 1: Document (0-0.3)
        if progress < 0.3:
            phase = progress / 0.3
            doc_box = FancyBboxPatch(
                (20, 30), 60, 50,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.9 * phase
            )
            ax.add_patch(doc_box)
            
            ax.text(50, 55, 'Volledig Artikel',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['primary'], fontweight='bold',
                    alpha=phase)
        
        # Fase 2: Splitting animatie (0.3-0.6)
        elif progress < 0.6:
            phase = (progress - 0.3) / 0.3
            
            # Scheidingslijnen animeren
            for i in range(4):
                line_y = 75 - (i * 15)
                line_alpha = min(1.0, max(0, (phase - i * 0.15) / 0.15))
                
                if line_alpha > 0:
                    ax.plot([20, 80], [line_y, line_y],
                           color=self.colors['accent'],
                           linewidth=2, linestyle='--',
                           alpha=line_alpha)
        
        # Fase 3: Aparte chunks (0.6-1.0)
        else:
            phase = (progress - 0.6) / 0.4
            
            # 5 chunks verticaal gestapeld
            chunk_height = 12
            chunk_spacing = 2
            start_y = 70
            
            for i, chunk in enumerate(self.chunks):
                chunk_alpha = min(1.0, max(0, (phase - i * 0.1) / 0.3))
                
                if chunk_alpha > 0:
                    y_pos = start_y - (i * (chunk_height + chunk_spacing))
                    
                    chunk_box = FancyBboxPatch(
                        (15, y_pos), 70, chunk_height,
                        boxstyle="round,pad=0.5",
                        facecolor=self.colors['bg_light'],
                        edgecolor=self.colors['secondary'],
                        linewidth=2,
                        alpha=0.9 * chunk_alpha
                    )
                    ax.add_patch(chunk_box)
                    
                    # Chunk tekst (ingekort)
                    short_text = chunk[:60] + "..." if len(chunk) > 60 else chunk
                    ax.text(50, y_pos + chunk_height/2, short_text,
                            fontsize=8, ha='center', va='center',
                            color=self.colors['text'],
                            alpha=chunk_alpha)
                    
                    # Chunk nummer
                    ax.text(12, y_pos + chunk_height/2, f'{i+1}',
                            fontsize=12, ha='center', va='center',
                            color=self.colors['secondary'],
                            fontweight='bold',
                            alpha=chunk_alpha)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_embeddings(self, progress):
        """Stap 2: Toon hoe chunks worden omgezet naar vectors"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 95, 'Stap 3: Embeddings Creëren',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['accent'])
        
        ax.text(50, 90, 'Elke chunk wordt een vector in 384-dimensionale ruimte',
                fontsize=14, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')
        
        # Links: Tekstchunks
        chunk_y_positions = [75, 60, 45, 30, 15]
        
        for i in range(5):
            # Chunk verschijnt
            if progress > i * 0.15:
                chunk_alpha = min(1.0, (progress - i * 0.15) / 0.15)
                
                chunk_box = FancyBboxPatch(
                    (5, chunk_y_positions[i] - 3), 25, 6,
                    boxstyle="round,pad=0.3",
                    facecolor=self.colors['bg_light'],
                    edgecolor=self.colors['text'],
                    linewidth=1,
                    alpha=0.7 * chunk_alpha
                )
                ax.add_patch(chunk_box)
                
                ax.text(17.5, chunk_y_positions[i], f'Chunk {i+1}',
                        fontsize=10, ha='center', va='center',
                        color=self.colors['text'],
                        alpha=chunk_alpha)
            
            # Pijl naar embedding model
            if progress > i * 0.15 + 0.2:
                arrow_alpha = min(1.0, (progress - (i * 0.15 + 0.2)) / 0.15)
                
                arrow = FancyArrowPatch(
                    (30, chunk_y_positions[i]),
                    (42, chunk_y_positions[i]),
                    arrowstyle='-|>',
                    mutation_scale=20,
                    linewidth=2,
                    color=self.colors['accent'],
                    alpha=arrow_alpha
                )
                ax.add_artist(arrow)
            
            # Vector verschijnt rechts
            if progress > i * 0.15 + 0.4:
                vec_alpha = min(1.0, (progress - (i * 0.15 + 0.4)) / 0.15)
                
                # Vector als lijst met getallen
                vec_box = FancyBboxPatch(
                    (58, chunk_y_positions[i] - 3), 37, 6,
                    boxstyle="round,pad=0.3",
                    facecolor='#1a3a1a',
                    edgecolor=self.colors['secondary'],
                    linewidth=2,
                    alpha=0.9 * vec_alpha
                )
                ax.add_patch(vec_box)
                
                ax.text(76.5, chunk_y_positions[i], '[0.23, -0.18, 0.91, ... 384 dimensies]',
                        fontsize=8, ha='center', va='center',
                        color=self.colors['secondary'],
                        family='monospace',
                        alpha=vec_alpha)
        
        # Embedding Model in het midden
        if progress > 0.3:
            model_alpha = min(1.0, (progress - 0.3) / 0.2)
            
            model_box = FancyBboxPatch(
                (42, 20), 16, 50,
                boxstyle="round,pad=1",
                facecolor='#2a2a3a',
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.95 * model_alpha
            )
            ax.add_patch(model_box)
            
            ax.text(50, 50, '🤖',
                    fontsize=40, ha='center', va='center',
                    alpha=model_alpha)
            
            ax.text(50, 38, 'Embedding',
                    fontsize=12, ha='center', va='center',
                    color=self.colors['primary'],
                    fontweight='bold',
                    alpha=model_alpha)
            
            ax.text(50, 34, 'Model',
                    fontsize=12, ha='center', va='center',
                    color=self.colors['primary'],
                    fontweight='bold',
                    alpha=model_alpha)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_vector_db(self, progress):
        """Stap 3: Toon vector database met alle embeddings"""
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection='3d')
        
        # 3D setup
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_zlim(-5, 5)
        ax.view_init(elev=20, azim=45 + progress * 180)  # Roteer
        
        # Verberg assen voor cleaner look
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('none')
        ax.yaxis.pane.set_edgecolor('none')
        ax.zaxis.pane.set_edgecolor('none')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        
        # Titel (in 2D overlay)
        self.fig.text(0.5, 0.95, 'Stap 4: Vector Database',
                     fontsize=28, fontweight='bold', ha='center', va='top',
                     color=self.colors['highlight'])
        
        self.fig.text(0.5, 0.90, 'Alle chunks als vectoren in semantische ruimte',
                     fontsize=14, ha='center', va='top',
                     color=self.colors['text'], alpha=0.7, style='italic')
        
        # 5 chunks als 3D punten (pseudo-posities voor visualisatie)
        chunk_positions = [
            np.array([2.5, 2.0, 1.5]),   # Chunk 1
            np.array([2.8, 1.5, 2.0]),   # Chunk 2  
            np.array([3.0, 2.5, 1.8]),   # Chunk 3 - relevant!
            np.array([-2.0, 1.0, -1.5]), # Chunk 4
            np.array([-2.5, -1.0, 1.0])  # Chunk 5
        ]
        
        colors_chunks = [
            self.colors['primary'],
            self.colors['primary'],
            self.colors['highlight'],  # Relevante chunk
            self.colors['primary'],
            self.colors['primary']
        ]
        
        # Laat punten verschijnen met delay
        for i, pos in enumerate(chunk_positions):
            if progress > i * 0.15:
                point_alpha = min(1.0, (progress - i * 0.15) / 0.15)
                
                # Speciaal effect voor relevante chunk
                size = 500 if i == 2 else 300
                if i == 2 and progress > 0.7:
                    pulse = 1 + 0.3 * np.sin(progress * 20)
                    size *= pulse
                
                ax.scatter([pos[0]], [pos[1]], [pos[2]],
                          s=size,
                          c=colors_chunks[i],
                          edgecolors='white',
                          linewidths=2,
                          alpha=point_alpha,
                          depthshade=False)
                
                # Label
                if progress > i * 0.15 + 0.1:
                    label_text = f'Chunk {i+1}'
                    if i == 2:
                        label_text += '\n(Relevant!)'
                    
                    ax.text(pos[0], pos[1], pos[2] + 0.5,
                           label_text,
                           fontsize=10,
                           ha='center',
                           color=colors_chunks[i],
                           fontweight='bold' if i == 2 else 'normal',
                           alpha=point_alpha)
        
        # Verbindingslijnen tussen gerelateerde chunks
        if progress > 0.8:
            line_alpha = (progress - 0.8) / 0.2
            # Chunk 1-2-3 cluster (gerelateerd aan wijzigingsproces)
            for i, j in [(0, 1), (1, 2), (0, 2)]:
                ax.plot([chunk_positions[i][0], chunk_positions[j][0]],
                       [chunk_positions[i][1], chunk_positions[j][1]],
                       [chunk_positions[i][2], chunk_positions[j][2]],
                       color=self.colors['primary'],
                       linestyle='--',
                       alpha=0.3 * line_alpha,
                       linewidth=1)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_gebruikersvraag(self, progress):
        """Stap 4: Toon gebruikersvraag"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel met fade-in
        alpha = min(1.0, progress * 2)
        ax.text(50, 90, 'Stap 5: Gebruikersvraag',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['highlight'],
                alpha=alpha)
        
        # Vraag verschijnt letter voor letter (typewriter effect)
        if progress > 0.3:
            type_progress = (progress - 0.3) / 0.7
            num_chars = int(len(self.vraag) * type_progress)
            displayed_vraag = self.vraag[:num_chars]
            
            # Cursor knippert
            if num_chars < len(self.vraag):
                cursor = '|' if int(progress * 10) % 2 == 0 else ''
                displayed_vraag += cursor
            
            vraag_box = FancyBboxPatch(
                (15, 35), 70, 25,
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=3,
                alpha=0.95
            )
            ax.add_patch(vraag_box)
            
            ax.text(50, 47.5, displayed_vraag,
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'],
                    wrap=True)
        
        # Vraagtekenicon
        if progress > 0.2:
            icon_alpha = min(1.0, (progress - 0.2) / 0.3)
            ax.text(50, 70, '❓',
                    fontsize=60, ha='center', va='center',
                    alpha=icon_alpha)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_query_embedding(self, progress):
        """Stap 5: Vraag wordt ook een embedding"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 95, 'Stap 6: Query Embedding',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['accent'])
        
        ax.text(50, 90, 'Vraag wordt ook omgezet naar vector',
                fontsize=14, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')
        
        # Links: Vraag
        if progress > 0:
            vraag_alpha = min(1.0, progress / 0.2)
            
            vraag_box = FancyBboxPatch(
                (5, 40), 30, 15,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=2,
                alpha=0.9 * vraag_alpha
            )
            ax.add_patch(vraag_box)
            
            wrapped_vraag = textwrap.fill(self.vraag, width=25)
            ax.text(20, 47.5, wrapped_vraag,
                    fontsize=11, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=vraag_alpha)
        
        # Pijl
        if progress > 0.3:
            arrow_alpha = min(1.0, (progress - 0.3) / 0.2)
            
            arrow = FancyArrowPatch(
                (35, 47.5), (42, 47.5),
                arrowstyle='-|>',
                mutation_scale=25,
                linewidth=3,
                color=self.colors['accent'],
                alpha=arrow_alpha
            )
            ax.add_artist(arrow)
        
        # Embedding Model
        if progress > 0.4:
            model_alpha = min(1.0, (progress - 0.4) / 0.2)
            
            model_box = FancyBboxPatch(
                (42, 35), 16, 25,
                boxstyle="round,pad=1",
                facecolor='#2a2a3a',
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.95 * model_alpha
            )
            ax.add_patch(model_box)
            
            ax.text(50, 52, '🤖',
                    fontsize=30, ha='center', va='center',
                    alpha=model_alpha)
            
            ax.text(50, 43, 'Embedding',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['primary'],
                    fontweight='bold',
                    alpha=model_alpha)
        
        # Rechts: Query Vector
        if progress > 0.7:
            vec_alpha = min(1.0, (progress - 0.7) / 0.3)
            
            vec_box = FancyBboxPatch(
                (65, 40), 30, 15,
                boxstyle="round,pad=1",
                facecolor='#3a1a2a',
                edgecolor=self.colors['highlight'],
                linewidth=2,
                alpha=0.9 * vec_alpha
            )
            ax.add_patch(vec_box)
            
            ax.text(80, 50, 'Query Vector',
                    fontsize=12, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold',
                    alpha=vec_alpha)
            
            ax.text(80, 45, '[0.31, -0.22, 0.87,\n..., 384 dims]',
                    fontsize=9, ha='center', va='center',
                    color=self.colors['text'],
                    family='monospace',
                    alpha=vec_alpha)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_similarity_search(self, progress):
        """Stap 6: Zoek meest vergelijkbare chunks"""
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection='3d')
        
        # 3D setup
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_zlim(-5, 5)
        ax.view_init(elev=20, azim=60)
        
        # Verberg assen
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('none')
        ax.yaxis.pane.set_edgecolor('none')
        ax.zaxis.pane.set_edgecolor('none')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        
        # Titel
        self.fig.text(0.5, 0.95, 'Stap 7: Similarity Search',
                     fontsize=28, fontweight='bold', ha='center', va='top',
                     color=self.colors['secondary'])
        
        self.fig.text(0.5, 0.90, 'Zoek chunks die het dichtst bij de vraag liggen',
                     fontsize=14, ha='center', va='top',
                     color=self.colors['text'], alpha=0.7, style='italic')
        
        # Chunk posities (zelfde als eerder)
        chunk_positions = [
            np.array([2.5, 2.0, 1.5]),
            np.array([2.8, 1.5, 2.0]),
            np.array([3.0, 2.5, 1.8]),   # Relevant
            np.array([-2.0, 1.0, -1.5]),
            np.array([-2.5, -1.0, 1.0])
        ]
        
        # Query positie (dichtbij chunk 3)
        query_pos = np.array([3.2, 2.3, 2.0])
        
        # Query vector verschijnt
        if progress > 0:
            query_alpha = min(1.0, progress / 0.2)
            
            ax.scatter([query_pos[0]], [query_pos[1]], [query_pos[2]],
                      s=600,
                      c=self.colors['highlight'],
                      marker='*',
                      edgecolors='white',
                      linewidths=3,
                      alpha=query_alpha,
                      depthshade=False)
            
            ax.text(query_pos[0], query_pos[1], query_pos[2] + 0.7,
                   'Vraag',
                   fontsize=12,
                   ha='center',
                   color=self.colors['highlight'],
                   fontweight='bold',
                   alpha=query_alpha)
        
        # Chunks verschijnen
        for i, pos in enumerate(chunk_positions):
            if progress > 0.2:
                chunk_alpha = min(1.0, (progress - 0.2) / 0.2)
                
                color = self.colors['dim']
                size = 300
                
                ax.scatter([pos[0]], [pos[1]], [pos[2]],
                          s=size,
                          c=color,
                          edgecolors='white',
                          linewidths=2,
                          alpha=chunk_alpha * 0.5,
                          depthshade=False)
                
                ax.text(pos[0], pos[1], pos[2] - 0.5,
                       f'Chunk {i+1}',
                       fontsize=9,
                       ha='center',
                       color=color,
                       alpha=chunk_alpha * 0.5)
        
        # Zoekstralen (vanaf query naar alle chunks)
        if progress > 0.4:
            ray_progress = (progress - 0.4) / 0.3
            
            for i, pos in enumerate(chunk_positions):
                ray_alpha = min(1.0, ray_progress)
                
                ax.plot([query_pos[0], pos[0]],
                       [query_pos[1], pos[1]],
                       [query_pos[2], pos[2]],
                       color=self.colors['accent'],
                       linestyle=':',
                       alpha=0.3 * ray_alpha,
                       linewidth=1.5)
        
        # Highlight beste match (chunk 3)
        if progress > 0.7:
            best_alpha = min(1.0, (progress - 0.7) / 0.3)
            
            best_pos = chunk_positions[2]
            
            # Pulse effect
            pulse = 1 + 0.4 * np.sin(progress * 15)
            
            ax.scatter([best_pos[0]], [best_pos[1]], [best_pos[2]],
                      s=500 * pulse,
                      c=self.colors['secondary'],
                      edgecolors='white',
                      linewidths=3,
                      alpha=best_alpha,
                      depthshade=False)
            
            # Verbindingslijn (dikker)
            ax.plot([query_pos[0], best_pos[0]],
                   [query_pos[1], best_pos[1]],
                   [query_pos[2], best_pos[2]],
                   color=self.colors['secondary'],
                   linestyle='-',
                   alpha=0.8 * best_alpha,
                   linewidth=4)
            
            ax.text(best_pos[0], best_pos[1], best_pos[2] - 0.7,
                   'Chunk 3\n(Beste match!)',
                   fontsize=11,
                   ha='center',
                   color=self.colors['secondary'],
                   fontweight='bold',
                   alpha=best_alpha)
            
            # Score
            if progress > 0.85:
                score_alpha = (progress - 0.85) / 0.15
                mid_x = (query_pos[0] + best_pos[0]) / 2
                mid_y = (query_pos[1] + best_pos[1]) / 2
                mid_z = (query_pos[2] + best_pos[2]) / 2
                
                ax.text(mid_x, mid_y, mid_z + 0.5,
                       'Similarity: 0.89',
                       fontsize=10,
                       ha='center',
                       bbox=dict(boxstyle='round,pad=0.3',
                               facecolor='#1a1a1a',
                               edgecolor=self.colors['secondary'],
                               alpha=0.9),
                       color=self.colors['secondary'],
                       fontweight='bold',
                       alpha=score_alpha)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_context_ophalen(self, progress):
        """Stap 7: Haal relevante chunk op"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 95, 'Stap 8: Context Ophalen',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['secondary'])
        
        ax.text(50, 90, 'Meest relevante chunk wordt opgehaald',
                fontsize=14, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')
        
        # Database icoon (links)
        if progress > 0:
            db_alpha = min(1.0, progress / 0.2)
            
            db_box = FancyBboxPatch(
                (10, 40), 20, 20,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.9 * db_alpha
            )
            ax.add_patch(db_box)
            
            ax.text(20, 50, '💾',
                    fontsize=40, ha='center', va='center',
                    alpha=db_alpha)
            
            ax.text(20, 38, 'Vector DB',
                    fontsize=10, ha='center', va='center',
                    color=self.colors['primary'],
                    fontweight='bold',
                    alpha=db_alpha)
        
        # Pijl met chunk die "vliegt"
        if progress > 0.3:
            fly_progress = (progress - 0.3) / 0.5
            
            start_x, start_y = 30, 50
            end_x, end_y = 65, 50
            
            current_x = start_x + (end_x - start_x) * fly_progress
            current_y = start_y + 15 * np.sin(fly_progress * np.pi)  # Arc
            
            # Trail effect
            if fly_progress < 1:
                trail_alpha = min(1.0, fly_progress)
                ax.plot([start_x, current_x], [start_y, current_y],
                       color=self.colors['secondary'],
                       linewidth=2,
                       alpha=0.3 * trail_alpha,
                       linestyle='--')
            
            # Vliegende chunk
            chunk_size = 15
            chunk_box = FancyBboxPatch(
                (current_x - chunk_size/2, current_y - 5),
                chunk_size, 10,
                boxstyle="round,pad=0.5",
                facecolor=self.colors['secondary'],
                edgecolor='white',
                linewidth=2,
                alpha=0.9
            )
            ax.add_patch(chunk_box)
            
            ax.text(current_x, current_y, 'Chunk 3',
                    fontsize=10, ha='center', va='center',
                    color='white',
                    fontweight='bold')
        
        # Context box (rechts)
        if progress > 0.8:
            context_alpha = min(1.0, (progress - 0.8) / 0.2)
            
            context_box = FancyBboxPatch(
                (65, 30), 30, 40,
                boxstyle="round,pad=1.5",
                facecolor='#1a3a1a',
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * context_alpha
            )
            ax.add_patch(context_box)
            
            ax.text(80, 65, 'Context',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold',
                    alpha=context_alpha)
            
            # Chunk inhoud
            wrapped_chunk = textwrap.fill(self.chunks[2], width=25)
            ax.text(80, 45, wrapped_chunk,
                    fontsize=8, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=context_alpha)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_llm_generatie(self, progress):
        """Stap 8: LLM genereert antwoord"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel
        ax.text(50, 95, 'Stap 9: LLM Generatie',
                fontsize=28, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'])
        
        ax.text(50, 90, 'Language Model combineert vraag + context tot antwoord',
                fontsize=14, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')
        
        # Inputs (boven)
        if progress > 0:
            input_alpha = min(1.0, progress / 0.2)
            
            # Vraag (links boven)
            vraag_box = FancyBboxPatch(
                (10, 65), 35, 15,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['highlight'],
                linewidth=2,
                alpha=0.9 * input_alpha
            )
            ax.add_patch(vraag_box)
            
            ax.text(27.5, 75, 'Vraag',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold',
                    alpha=input_alpha)
            
            wrapped_vraag = textwrap.fill(self.vraag, width=30)
            ax.text(27.5, 69, wrapped_vraag,
                    fontsize=8, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=input_alpha)
            
            # Context (rechts boven)
            context_box = FancyBboxPatch(
                (55, 65), 35, 15,
                boxstyle="round,pad=0.8",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=2,
                alpha=0.9 * input_alpha
            )
            ax.add_patch(context_box)
            
            ax.text(72.5, 75, 'Context',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold',
                    alpha=input_alpha)
            
            ax.text(72.5, 69, 'Chunk 3:\n"Het wijzigingsproces..."',
                    fontsize=8, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=input_alpha)
        
        # Pijlen naar LLM
        if progress > 0.25:
            arrow_alpha = min(1.0, (progress - 0.25) / 0.15)
            
            # Linker pijl
            arrow1 = FancyArrowPatch(
                (27.5, 65), (40, 55),
                arrowstyle='-|>',
                mutation_scale=20,
                linewidth=2,
                color=self.colors['highlight'],
                alpha=arrow_alpha
            )
            ax.add_artist(arrow1)
            
            # Rechter pijl
            arrow2 = FancyArrowPatch(
                (72.5, 65), (60, 55),
                arrowstyle='-|>',
                mutation_scale=20,
                linewidth=2,
                color=self.colors['secondary'],
                alpha=arrow_alpha
            )
            ax.add_artist(arrow2)
        
        # LLM (midden)
        if progress > 0.3:
            llm_alpha = min(1.0, (progress - 0.3) / 0.2)
            
            llm_box = FancyBboxPatch(
                (35, 35), 30, 20,
                boxstyle="round,pad=1.5",
                facecolor='#2a2a4a',
                edgecolor=self.colors['primary'],
                linewidth=4,
                alpha=0.95 * llm_alpha
            )
            ax.add_patch(llm_box)
            
            ax.text(50, 50, '🧠',
                    fontsize=50, ha='center', va='center',
                    alpha=llm_alpha)
            
            ax.text(50, 38, 'Language Model',
                    fontsize=12, ha='center', va='center',
                    color=self.colors['primary'],
                    fontweight='bold',
                    alpha=llm_alpha)
        
        # "Denk" animatie
        if 0.5 < progress < 0.8:
            think_progress = (progress - 0.5) / 0.3
            num_dots = int(think_progress * 3) % 4
            dots = '.' * num_dots
            
            ax.text(50, 30, f'Aan het verwerken{dots}',
                    fontsize=11, ha='center', va='center',
                    color=self.colors['accent'],
                    style='italic')
        
        # Pijl naar beneden
        if progress > 0.8:
            down_alpha = min(1.0, (progress - 0.8) / 0.1)
            
            arrow_down = FancyArrowPatch(
                (50, 35), (50, 25),
                arrowstyle='-|>',
                mutation_scale=25,
                linewidth=3,
                color=self.colors['primary'],
                alpha=down_alpha
            )
            ax.add_artist(arrow_down)
        
        # Output hint
        if progress > 0.9:
            output_alpha = (progress - 0.9) / 0.1
            
            ax.text(50, 15, '📄 Antwoord',
                    fontsize=14, ha='center', va='center',
                    color=self.colors['primary'],
                    fontweight='bold',
                    alpha=output_alpha)
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def draw_antwoord(self, progress):
        """Stap 9: Toon gegenereerd antwoord"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        
        # Titel met succes animatie
        alpha = min(1.0, progress * 2)
        
        # Pulse effect op titel
        if progress > 0.8:
            pulse = 1 + 0.1 * np.sin(progress * 15)
            fontsize = 28 * pulse
        else:
            fontsize = 28
        
        ax.text(50, 95, 'Stap 10: Het Antwoord! ✅',
                fontsize=fontsize, fontweight='bold', ha='center', va='top',
                color=self.colors['secondary'],
                alpha=alpha)
        
        # Antwoord box
        if progress > 0.2:
            box_alpha = min(1.0, (progress - 0.2) / 0.3)
            
            antwoord_box = FancyBboxPatch(
                (10, 15), 80, 70,
                boxstyle="round,pad=2",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=4,
                alpha=0.95 * box_alpha
            )
            ax.add_patch(antwoord_box)
        
        # Antwoord tekst verschijnt regel voor regel
        if progress > 0.4:
            text_progress = (progress - 0.4) / 0.6
            lines = self.antwoord.strip().split('\n')
            num_lines = max(1, int(len(lines) * text_progress))
            
            displayed_antwoord = '\n'.join(lines[:num_lines])
            
            # Typewriter cursor
            if num_lines < len(lines):
                cursor = '|' if int(progress * 10) % 2 == 0 else ''
                displayed_antwoord += cursor
            
            ax.text(50, 75, displayed_antwoord,
                    fontsize=13, ha='center', va='top',
                    color=self.colors['text'],
                    alpha=min(1.0, text_progress * 1.5))
        
        # Succesboodschap
        if progress > 0.9:
            success_alpha = (progress - 0.9) / 0.1
            
            ax.text(50, 10, '🎉 RAG Journey Compleet! 🎉',
                    fontsize=18, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold',
                    alpha=success_alpha)
            
            ax.text(50, 5, 'Van kennisartikel naar accuraat antwoord in 10 stappen',
                    fontsize=12, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=0.7 * success_alpha,
                    style='italic')
        
        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()
    
    def add_status_indicator(self, is_animating):
        """Voeg status indicator toe"""
        if is_animating:
            status_text = "🎬 ANIMEREN..."
            status_color = self.colors['accent']
        else:
            status_text = "⏸ GEPAUZEERD - Druk SPATIE voor volgende stap"
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
    print("=" * 70)
    print("RAG JOURNEY VISUALISATIE - BiSL Kennisartikel")
    print("=" * 70)
    print("\n📚 Deze visualisatie toont hoe RAG werkt:")
    print("  1. Kennisartikel wordt opgesplitst in chunks")
    print("  2. Chunks worden embeddings (vectoren)")
    print("  3. Gebruiker stelt een vraag")
    print("  4. Vraag wordt ook een embedding")
    print("  5. Meest relevante chunks worden gevonden")
    print("  6. LLM gebruikt context om antwoord te genereren")
    print("\n⌨️  Bediening:")
    print("  SPATIE    : Start/Volgende stap")
    print("  B         : Vorige stap")
    print("  F         : Volledig scherm")
    print("  Q of ESC  : Afsluiten")
    print("\n🎯 Voorbeeld: BiSL Wijzigingsbeheer")
    print("  Vraag: 'Wat zijn de stappen in het wijzigingsproces?'")
    print("  RAG vindt het antwoord in de kennisbank!")
    print("\nDruk op SPATIE om te beginnen...")
    print("=" * 70)
    
    viz = RAGJourneyVisualization()
    viz.show()

if __name__ == "__main__":
    main()