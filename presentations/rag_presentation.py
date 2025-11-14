"""
RAG Journey Visualization
Retrieval Augmented Generation step-by-step
Integrated with BasePresentation for standardized controls
"""

import sys
import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.animation import FuncAnimation
import numpy as np
import textwrap

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import (BasePresentation, PresentationStyle, ParticleSystem,
                  SimilarityMeter, Performance3D, AnimationHelpers)


class RAGPresentation(BasePresentation):
    """RAG Journey visualization with standardized controls"""

    def __init__(self):
        """Initialize RAG presentation"""
        step_names = [
            'Landing',
            'Kennisartikel Tonen',
            'Tekst Chunking',
            'Semantisch Zoeken - Waarom Embeddings?',
            'Embeddings Creëren',
            'Vector Database',
            'Gebruikersvraag',
            'Query Embedding',
            'Similarity Search',
            'Context Ophalen',
            'LLM Generatie',
            'Antwoord Tonen'
        ]

        super().__init__("RAG Journey", step_names)

        # Customer Service Knowledge article
        self.artikel = """
        KENNISARTIKEL: Retourbeleid Webwinkel

        Ons retourbeleid is ontworpen om online winkelen zorgeloos te maken.
        Klanten kunnen producten binnen 30 dagen retourneren.

        Verschillende soorten retouren:
        - Standaard retour: product voldoet niet aan verwachting
        - Defect product: technisch defect of beschadigd ontvangen
        - Verkeerde bestelling: verkeerd artikel ontvangen

        Het retourproces bestaat uit de volgende stappen:
        1. Retour aanmelden via website of klantenservice
        2. Retourlabel ontvangen per email
        3. Product veilig inpakken met originele verpakking
        4. Pakket afgeven bij verzendpunt
        5. Terugbetaling binnen 5 werkdagen na ontvangst

        Belangrijke voorwaarden:
        - Product moet ongebruikt en compleet zijn
        - Originele verpakking en labels moeten aanwezig zijn
        - Hygiënische producten kunnen niet geretourneerd
        - Gepersonaliseerde artikelen zijn uitgesloten

        Kosten en vergoeding:
        - Retourzendingen binnen Nederland zijn gratis
        - Bij defect artikel vergoeden wij ook verzendkosten
        - Terugbetaling gebeurt via oorspronkelijke betaalmethode
        - Cadeaubonnen worden omgezet in winkelkrediet
        """

        self.vraag = "Wat zijn de stappen om een product te retourneren?"

        self.antwoord = """
        Om een product te retourneren volg je deze stappen:

        1. **Retour aanmelden** - Meld de retour aan via de website of bel klantenservice
        2. **Retourlabel ontvangen** - Je ontvangt per email een gratis retourlabel
        3. **Product inpakken** - Pak het product veilig in met de originele verpakking
        4. **Verzenden** - Geef het pakket af bij een verzendpunt
        5. **Terugbetaling** - Je ontvangt je geld terug binnen 5 werkdagen
        """

        # Chunks after splitting
        self.chunks = [
            "Ons retourbeleid is ontworpen om online winkelen zorgeloos te maken. Klanten kunnen producten binnen 30 dagen retourneren.",
            "Verschillende soorten retouren: Standaard retour (product voldoet niet aan verwachting), Defect product (technisch defect), Verkeerde bestelling (verkeerd artikel ontvangen).",
            "Het retourproces bestaat uit vijf stappen: 1) Retour aanmelden via website of klantenservice, 2) Retourlabel ontvangen per email, 3) Product inpakken, 4) Pakket afgeven, 5) Terugbetaling binnen 5 werkdagen.",
            "Belangrijke voorwaarden: Product ongebruikt en compleet, originele verpakking aanwezig, hygiënische producten uitgesloten, geen gepersonaliseerde artikelen.",
            "Kosten en vergoeding: Gratis retour binnen Nederland, bij defect ook verzendkosten vergoed, terugbetaling via originele betaalmethode, cadeaubonnen worden winkelkrediet."
        ]

        self.relevante_chunk_index = 2

        # Initialize particle systems for data flow animations
        self.particle_systems = {}

        # Initialize similarity meter
        self.similarity_meter = None

        self.show_landing_page()

    def get_frames_for_step(self, step: int) -> int:
        """Custom frame counts per step"""
        frames = {
            -1: 30, 0: 60, 1: 90, 2: 80, 3: 70, 4: 70, 5: 50,
            6: 60, 7: 100, 8: 70, 9: 90, 10: 80
        }
        return frames.get(step, 60)

    def show_landing_page(self):
        """Display RAG landing page"""
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
            edgecolor=self.colors['primary'],
            linewidth=4,
            alpha=0.95
        )
        ax.add_patch(title_box)

        ax.text(50, 72, 'RAG Journey',
                fontsize=72, fontweight='bold', ha='center', va='center',
                color=self.colors['primary'])

        ax.text(50, 64, 'Van Kennisartikel naar Antwoord',
                fontsize=33, ha='center', va='center',
                color=self.colors['text'], alpha=0.8, style='italic')

        ax.text(50, 45, 'Ontdek hoe AI jouw kennisbank doorzoekt',
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

        ax.text(50, 25, '>> Druk op SPATIE om te beginnen <<',
                fontsize=36, ha='center', va='center',
                color=self.colors['secondary'], fontweight='bold')

        ax.text(50, 20, 'B = Terug  •  Q = Afsluiten  •  F = Volledig scherm',
                fontsize=18, ha='center', va='center',
                color=self.colors['dim'], style='italic')

        ax.text(50, 5, 'Stapsgewijze visualisatie van Retrieval Augmented Generation',
                fontsize=18, ha='center', va='center',
                color=self.colors['text'], alpha=0.5)

        plt.tight_layout()

    def animate_step(self, frame: int):
        """Animate current step"""
        total_frames = self.get_frames_for_step(self.current_step)
        progress = frame / (total_frames - 1) if total_frames > 1 else 1

        if self.current_step == 0:
            self.draw_kennisartikel(progress)
        elif self.current_step == 1:
            self.draw_chunking(progress)
        elif self.current_step == 2:
            self.draw_semantic_search_intro(progress)
        elif self.current_step == 3:
            self.draw_embeddings(progress)
        elif self.current_step == 4:
            self.draw_vector_db(progress)
        elif self.current_step == 5:
            self.draw_gebruikersvraag(progress)
        elif self.current_step == 6:
            self.draw_query_embedding(progress)
        elif self.current_step == 7:
            self.draw_similarity_search(progress)
        elif self.current_step == 8:
            self.draw_context_ophalen(progress)
        elif self.current_step == 9:
            self.draw_llm_generatie(progress)
        elif self.current_step == 10:
            self.draw_antwoord(progress)

        if frame >= total_frames - 1:
            self.is_animating = False

    def draw_current_step_static(self):
        """Draw current step without animation"""
        if self.current_step == -1:
            self.show_landing_page()
        elif self.current_step == 0:
            self.draw_kennisartikel(1.0)
        elif self.current_step == 1:
            self.draw_chunking(1.0)
        elif self.current_step == 2:
            self.draw_semantic_search_intro(1.0)
        elif self.current_step == 3:
            self.draw_embeddings(1.0)
        elif self.current_step == 4:
            self.draw_vector_db(1.0)
        elif self.current_step == 5:
            self.draw_gebruikersvraag(1.0)
        elif self.current_step == 6:
            self.draw_query_embedding(1.0)
        elif self.current_step == 7:
            self.draw_similarity_search(1.0)
        elif self.current_step == 8:
            self.draw_context_ophalen(1.0)
        elif self.current_step == 9:
            self.draw_llm_generatie(1.0)
        elif self.current_step == 10:
            self.draw_antwoord(1.0)
        plt.draw()

    def draw_kennisartikel(self, progress):
        """Step 0: Show knowledge article"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        alpha = min(1.0, progress * 2)
        ax.text(50, 95, 'Stap 1: Het Kennisartikel',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'], alpha=alpha)

        # Document box - ALTIJD VOLLEDIG (geen animatie)
        if progress > 0.2:
            doc_alpha = min(1.0, (progress - 0.2) / 0.3)
            
            doc_box = FancyBboxPatch(
                (8, 5), 85, 80,  # VASTE grootte
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.9 * doc_alpha
            )
            ax.add_patch(doc_box)

         # Text content - typewriter effect BINNEN vaste box
        if progress > 0.4:
            text_progress = (progress - 0.4) / 0.6
            lines = self.artikel.strip().split('\n')
            num_lines = max(1, int(len(lines) * text_progress))
            displayed_text = '\n'.join(lines[:num_lines])

            # Wrap text
            wrapped_lines = []
            for line in displayed_text.split('\n'):
                if line.strip():
                    wrapped = textwrap.fill(line, width=70)
                    wrapped_lines.append(wrapped)
                else:
                    wrapped_lines.append('')

            final_text = '\n'.join(wrapped_lines)
            
            # Text verschijnt BINNEN de vaste boxq
            ax.text(50, 84, final_text,
                    fontsize=13, ha='center', va='top',
                    color=self.colors['text'],
                    family='monospace',
                    alpha=min(1.0, text_progress * 1.5))

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_chunking(self, progress):
        """Step 1: Show text chunking - SMOOTH TRANSITION"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        ax.text(50, 97, 'Stap 2: Tekst Chunking',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['secondary'])

        ax.text(50, 90, 'Artikel wordt opgedeeld in beheersbare stukken',
                fontsize=27, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # FASE 1 (0-0.3): Toon VOLLEDIGE ARTIKEL TEKST (zoals stap 1)
        if progress < 0.3:
            phase = progress / 0.3
            
            doc_box = FancyBboxPatch(
                (8, 5), 85, 80,  # VASTE grootte
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.9
            )
            ax.add_patch(doc_box)
            
            # VOLLEDIGE tekst zoals in stap 1
            lines = self.artikel.strip().split('\n')
            displayed_text = '\n'.join(lines)
            
            wrapped_lines = []
            for line in displayed_text.split('\n'):
                if line.strip():
                    wrapped = textwrap.fill(line, width=70)
                    wrapped_lines.append(wrapped)
                else:
                    wrapped_lines.append('')
            
            final_text = '\n'.join(wrapped_lines)
            ax.text(50, 84, final_text,
                    fontsize=13, ha='center', va='top',
                    color=self.colors['text'],
                    family='monospace',
                    alpha=1.0)

        # FASE 2 (0.3-0.6): Toon scheidingslijnen OVER de tekst
        elif progress < 0.6:
            phase = (progress - 0.3) / 0.3
            
            # Tekst blijft zichtbaar
            doc_box = FancyBboxPatch(
                (8, 5), 85, 80,  # VASTE grootte
                boxstyle="round,pad=1.5",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['primary'],
                linewidth=3,
                alpha=0.9
            )
            ax.add_patch(doc_box)
            
            lines = self.artikel.strip().split('\n')
            displayed_text = '\n'.join(lines)
            wrapped_lines = []
            for line in displayed_text.split('\n'):
                if line.strip():
                    wrapped = textwrap.fill(line, width=70)
                    wrapped_lines.append(wrapped)
                else:
                    wrapped_lines.append('')
            final_text = '\n'.join(wrapped_lines)
            
            ax.text(50, 84, final_text,
                    fontsize=13, ha='center', va='top',
                    color=self.colors['text'],
                    family='monospace',
                    alpha=0.5)  # Iets dimmen voor de lijnen
            
            # Scheidingslijnen verschijnen
            for i in range(4):
                line_y = 75 - (i * 15)
                line_alpha = min(1.0, max(0, (phase - i * 0.15) / 0.15))
                if line_alpha > 0:
                    ax.plot([15, 85], [line_y, line_y],
                        color=self.colors['accent'],
                        linewidth=3, linestyle='--',
                        alpha=line_alpha)

        # FASE 3 (0.6-1.0): Fade naar chunks
        else:
            phase = (progress - 0.6) / 0.4
            
            # Oude tekst fade out
            if phase < 0.3:
                old_alpha = 1.0 - (phase / 0.3)
                doc_box = FancyBboxPatch(
                    (8, 5), 85, 80,  # VASTE grootte
                    boxstyle="round,pad=1.5",
                    facecolor=self.colors['bg_light'],
                    edgecolor=self.colors['primary'],
                    linewidth=3,
                    alpha=0.9 * old_alpha
                )
                ax.add_patch(doc_box)
                
                lines = self.artikel.strip().split('\n')
                displayed_text = '\n'.join(lines)
                wrapped_lines = []
                for line in displayed_text.split('\n'):
                    if line.strip():
                        wrapped = textwrap.fill(line, width=70)
                        wrapped_lines.append(wrapped)
                    else:
                        wrapped_lines.append('')
                final_text = '\n'.join(wrapped_lines)
                
                ax.text(50, 84, final_text,
                        fontsize=13, ha='center', va='top',
                        color=self.colors['text'],
                        family='monospace',
                        alpha=0.5 * old_alpha)
            
            # Chunks fade in
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

                    short_text = chunk[:60] + "..." if len(chunk) > 60 else chunk
                    ax.text(50, y_pos + chunk_height/2, short_text,
                            fontsize=18, ha='center', va='center',
                            color=self.colors['text'],
                            alpha=chunk_alpha)

                    ax.text(12, y_pos + chunk_height/2, f'{i+1}',
                            fontsize=24, ha='center', va='center',
                            color=self.colors['secondary'],
                            fontweight='bold',
                            alpha=chunk_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()


    def draw_semantic_search_intro(self, progress):
        """Step 2.5: Introduce semantic search - why embeddings?"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Title
        ax.text(50, 96, 'Semantisch Zoeken - Waarom Embeddings?',
                fontsize=48, fontweight='bold', ha='center', va='top',
                color=self.colors['highlight'])

        ax.text(50, 90, 'Hoe vinden we de juiste chunks bij een vraag?',
                fontsize=24, ha='center', va='top',
                color=self.colors['text'], alpha=0.7, style='italic')

        # Probleem: Keyword search
        if progress > 0.15:
            keyword_alpha = min(1.0, (progress - 0.15) / 0.25)

            keyword_box = FancyBboxPatch(
                (8, 62), 40, 20,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['error'],
                linewidth=3,
                alpha=0.95 * keyword_alpha
            )
            ax.add_patch(keyword_box)

            ax.text(28, 77, 'Keyword Zoeken',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['error'], fontweight='bold',
                    alpha=keyword_alpha)

            ax.text(28, 72, 'Vraag: "Wat is een RFC?"',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['text'], alpha=keyword_alpha,
                    style='italic')

            ax.text(28, 67, 'Zoekt alleen exact "RFC"',
                    fontsize=15, ha='center', va='center',
                    color=self.colors['text'], alpha=keyword_alpha * 0.8)

            # Cross symbol
            ax.text(40, 69, '✗', fontsize=40, ha='center', va='center',
                    color=self.colors['error'], alpha=keyword_alpha)

        # Oplossing: Semantic search
        if progress > 0.45:
            semantic_alpha = min(1.0, (progress - 0.45) / 0.25)

            semantic_box = FancyBboxPatch(
                (52, 62), 40, 20,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['secondary'],
                linewidth=3,
                alpha=0.95 * semantic_alpha
            )
            ax.add_patch(semantic_box)

            ax.text(72, 77, 'Semantisch Zoeken',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['secondary'], fontweight='bold',
                    alpha=semantic_alpha)

            ax.text(72, 72, 'Vraag: "Wat is een RFC?"',
                    fontsize=16, ha='center', va='center',
                    color=self.colors['text'], alpha=semantic_alpha,
                    style='italic')

            # Wrapped text
            results_text = textwrap.fill(
                'Vindt ook: "Request for Change", "wijzigingsaanvraag", RFC uitleg',
                width=30
            )
            ax.text(72, 66, results_text,
                    fontsize=14, ha='center', va='center',
                    color=self.colors['text'], alpha=semantic_alpha * 0.9)

            # Check symbol
            ax.text(85, 70, '✓', fontsize=40, ha='center', va='center',
                    color=self.colors['secondary'], alpha=semantic_alpha)

        # Voorbeelden
        if progress > 0.72:
            examples_alpha = min(1.0, (progress - 0.72) / 0.25)

            examples_box = FancyBboxPatch(
                (10, 32), 80, 25,
                boxstyle="round,pad=1.2",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['cyan'],
                linewidth=3,
                alpha=0.95 * examples_alpha
            )
            ax.add_patch(examples_box)

            ax.text(50, 53, 'Praktische Voorbeelden van Semantisch Zoeken:',
                    fontsize=21, ha='center', va='center',
                    color=self.colors['cyan'], fontweight='bold',
                    alpha=examples_alpha)

            # Example 1
            ax.text(15, 47, '1. Synoniemen:', fontsize=17, ha='left', va='center',
                    color=self.colors['text'], fontweight='bold', alpha=examples_alpha)
            ax.text(18, 43.5, '"RFC" matcht ook "Request for Change"',
                    fontsize=15, ha='left', va='center',
                    color=self.colors['text'], alpha=examples_alpha * 0.9)

            # Example 2
            ax.text(15, 39, '2. Concepten:', fontsize=17, ha='left', va='center',
                    color=self.colors['text'], fontweight='bold', alpha=examples_alpha)
            ax.text(18, 35.5, '"wijzigingsproces" vindt ook "change management"',
                    fontsize=15, ha='left', va='center',
                    color=self.colors['text'], alpha=examples_alpha * 0.9)

        # Conclusie
        if progress > 0.88:
            conclusion_alpha = min(1.0, (progress - 0.88) / 0.12)

            conclusion_box = FancyBboxPatch(
                (10, 8), 80, 20,
                boxstyle="round,pad=1",
                facecolor=self.colors['bg_light'],
                edgecolor=self.colors['accent'],
                linewidth=4,
                alpha=0.95 * conclusion_alpha
            )
            ax.add_patch(conclusion_box)

            ax.text(50, 22, '>> Daarom gebruiken we Embeddings:',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['accent'], fontweight='bold',
                    alpha=conclusion_alpha)

            conclusion_text = textwrap.fill(
                'Embeddings zetten tekst om in vectoren die de BETEKENIS vastleggen, '
                'zodat we semantisch kunnen zoeken in plaats van alleen keywords.',
                width=80
            )
            ax.text(50, 14, conclusion_text,
                    fontsize=16, ha='center', va='center',
                    color=self.colors['text'], alpha=conclusion_alpha * 0.9)

        self.add_status_indicator(progress < 1.0)

    def draw_embeddings(self, progress):
        """Step 2: Show embedding creation"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        ax.text(50, 97, 'Stap 4: Embeddings Creëren',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['accent'])

        ax.text(50, 90, 'Elke chunk wordt een vector in 384-dimensionale ruimte',
                fontsize=27, ha='center', va='top',
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
                        fontsize=21, ha='center', va='center',
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
                        fontsize=18, ha='center', va='center',
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

            # Robot icon (as text to avoid emoji font issues)
            ax.text(50, 52, 'AI',
                    fontsize=60, ha='center', va='center',
                    fontweight='bold',
                    color=self.colors['primary'],
                    alpha=model_alpha)

            ax.text(50, 38, 'Embedding',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['primary'],
                    fontweight='bold',
                    alpha=model_alpha)

            ax.text(50, 34, 'Model',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['primary'],
                    fontweight='bold',
                    alpha=model_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_vector_db(self, progress):
        """Step 3: Vector database with 3D visualization - IMPROVED"""
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection='3d')

        # 3D setup
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_zlim(-5, 5)
        ax.view_init(elev=20, azim=45 + progress * 90)  # Slower rotation

        # Background styling - make axes more visible
        ax.set_facecolor(self.colors['bg'])
        ax.xaxis.pane.fill = True
        ax.yaxis.pane.fill = True
        ax.zaxis.pane.fill = True
        ax.xaxis.pane.set_facecolor((0.05, 0.05, 0.05, 0.3))
        ax.yaxis.pane.set_facecolor((0.05, 0.05, 0.05, 0.3))
        ax.zaxis.pane.set_facecolor((0.05, 0.05, 0.05, 0.3))
        ax.xaxis.pane.set_edgecolor((0.2, 0.2, 0.2, 0.5))
        ax.yaxis.pane.set_edgecolor((0.2, 0.2, 0.2, 0.5))
        ax.zaxis.pane.set_edgecolor((0.2, 0.2, 0.2, 0.5))

        # Add grid for better depth perception
        ax.grid(True, alpha=0.2, color=self.colors['grid'])

        # Show tick labels for scale
        ax.set_xlabel('X', fontsize=16, color=self.colors['text'])
        ax.set_ylabel('Y', fontsize=16, color=self.colors['text'])
        ax.set_zlabel('Z', fontsize=16, color=self.colors['text'])
        ax.tick_params(colors=self.colors['text'], labelsize=12)

        # Titel (in 2D overlay)
        self.fig.text(0.5, 0.97, 'Stap 5: Vector Database',
                     fontsize=51, fontweight='bold', ha='center', va='top',
                     color=self.colors['highlight'])

        self.fig.text(0.5, 0.90, 'Alle chunks als vectoren in semantische ruimte',
                     fontsize=27, ha='center', va='top',
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
            self.colors['cyan'],
            self.colors['cyan'],
            self.colors['highlight'],  # Relevante chunk
            self.colors['accent'],
            self.colors['accent']
        ]

        # Draw origin point
        if progress > 0.05:
            origin_alpha = min(1.0, progress / 0.1)
            ax.scatter([0], [0], [0], s=200, c=self.colors['text'],
                      marker='x', linewidths=3, alpha=origin_alpha * 0.5)

        # Laat punten verschijnen met delay
        for i, pos in enumerate(chunk_positions):
            if progress > i * 0.15:
                point_alpha = min(1.0, (progress - i * 0.15) / 0.15)

                # Speciaal effect voor relevante chunk
                is_relevant = (i == 2)
                size = 800 if is_relevant else 500

                if is_relevant and progress > 0.7:
                    pulse = 1 + 0.3 * np.sin(progress * 20)
                    size *= pulse

                # Draw vector line from origin to point
                if progress > i * 0.15 + 0.05:
                    line_alpha = min(1.0, (progress - (i * 0.15 + 0.05)) / 0.1)
                    ax.plot([0, pos[0]], [0, pos[1]], [0, pos[2]],
                           color=colors_chunks[i],
                           linewidth=2 if is_relevant else 1.5,
                           alpha=line_alpha * 0.6,
                           linestyle='-' if is_relevant else '--')

                # Draw the point itself
                ax.scatter([pos[0]], [pos[1]], [pos[2]],
                          s=size,
                          c=[colors_chunks[i]],
                          edgecolors='white',
                          linewidths=3 if is_relevant else 2,
                          alpha=point_alpha * 0.9,
                          depthshade=True)

                # Add glow effect for relevant chunk
                if is_relevant and progress > 0.5:
                    glow_alpha = min(1.0, (progress - 0.5) / 0.2) * 0.3
                    ax.scatter([pos[0]], [pos[1]], [pos[2]],
                              s=size * 1.8,
                              c=[colors_chunks[i]],
                              alpha=glow_alpha,
                              edgecolors='none',
                              depthshade=False)

                # Label with background box
                if progress > i * 0.15 + 0.1:
                    label_text = f'Chunk {i+1}'
                    if is_relevant:
                        label_text += '\n(Relevant!)'

                    ax.text(pos[0], pos[1], pos[2] + 0.7,
                           label_text,
                           fontsize=19 if is_relevant else 16,
                           ha='center',
                           color='white',
                           fontweight='bold' if is_relevant else 'normal',
                           alpha=point_alpha,
                           bbox=dict(boxstyle='round,pad=0.5',
                                   facecolor=colors_chunks[i],
                                   edgecolor='white' if is_relevant else 'none',
                                   linewidth=2,
                                   alpha=0.9))

        # Verbindingslijnen tussen gerelateerde chunks
        if progress > 0.8:
            line_alpha = (progress - 0.8) / 0.2
            # Chunk 1-2-3 cluster (gerelateerd aan wijzigingsproces)
            for i, j in [(0, 1), (1, 2), (0, 2)]:
                ax.plot([chunk_positions[i][0], chunk_positions[j][0]],
                       [chunk_positions[i][1], chunk_positions[j][1]],
                       [chunk_positions[i][2], chunk_positions[j][2]],
                       color=self.colors['cyan'],
                       linestyle=':',
                       alpha=0.4 * line_alpha,
                       linewidth=1.5)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_gebruikersvraag(self, progress):
        """Step 4: User question with typewriter effect"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Titel met fade-in
        alpha = min(1.0, progress * 2)
        ax.text(50, 90, 'Stap 6: Gebruikersvraag',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['highlight'],
                alpha=alpha)

        # Vraagtekenicon
        if progress > 0.2:
            icon_alpha = min(1.0, (progress - 0.2) / 0.3)
            ax.text(50, 70, '?',
                    fontsize=120, ha='center', va='center',
                    fontweight='bold',
                    color=self.colors['highlight'],
                    alpha=icon_alpha)

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
                    fontsize=33, ha='center', va='center',
                    color=self.colors['text'],
                    wrap=True)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_query_embedding(self, progress):
        """Step 5: Query embedding with detailed visualization"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Titel
        ax.text(50, 97, 'Stap 7: Query Embedding',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['accent'])

        ax.text(50, 90, 'Vraag wordt ook omgezet naar vector',
                fontsize=27, ha='center', va='top',
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
                    fontsize=16, ha='center', va='center',
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

            ax.text(50, 52, 'AI',
                    fontsize=45, ha='center', va='center',
                    fontweight='bold',
                    color=self.colors['primary'],
                    alpha=model_alpha)

            ax.text(50, 43, 'Embedding',
                    fontsize=16, ha='center', va='center',
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
                    fontsize=24, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold',
                    alpha=vec_alpha)

            ax.text(80, 45, '[0.31, -0.22, 0.87,\n..., 384 dims]',
                    fontsize=13, ha='center', va='center',
                    color=self.colors['text'],
                    family='monospace',
                    alpha=vec_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_similarity_search(self, progress):
        """Step 6: Similarity search with SIMPLIFIED 3D visualization - PERFORMANCE FIX"""
        self.fig.clear()
        ax = self.fig.add_subplot(111, projection='3d')

        # 3D setup - FIXED angle (no rotation for performance)
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_zlim(-5, 5)
        ax.view_init(elev=20, azim=45)  # Fixed angle - no rotation

        # Background styling - make axes more visible
        ax.set_facecolor(self.colors['bg'])
        ax.xaxis.pane.fill = True
        ax.yaxis.pane.fill = True
        ax.zaxis.pane.fill = True
        ax.xaxis.pane.set_facecolor((0.05, 0.05, 0.05, 0.3))
        ax.yaxis.pane.set_facecolor((0.05, 0.05, 0.05, 0.3))
        ax.zaxis.pane.set_facecolor((0.05, 0.05, 0.05, 0.3))
        ax.xaxis.pane.set_edgecolor((0.2, 0.2, 0.2, 0.5))
        ax.yaxis.pane.set_edgecolor((0.2, 0.2, 0.2, 0.5))
        ax.zaxis.pane.set_edgecolor((0.2, 0.2, 0.2, 0.5))

        # Add grid
        ax.grid(True, alpha=0.2, color=self.colors['grid'])

        # Show axes labels
        ax.set_xlabel('X', fontsize=16, color=self.colors['text'])
        ax.set_ylabel('Y', fontsize=16, color=self.colors['text'])
        ax.set_zlabel('Z', fontsize=16, color=self.colors['text'])
        ax.tick_params(colors=self.colors['text'], labelsize=12)

        # Titel
        self.fig.text(0.5, 0.97, 'Stap 8: Similarity Search',
                     fontsize=51, fontweight='bold', ha='center', va='top',
                     color=self.colors['secondary'])

        self.fig.text(0.5, 0.90, 'Zoek chunks die het dichtst bij de vraag liggen',
                     fontsize=27, ha='center', va='top',
                     color=self.colors['text'], alpha=0.7, style='italic')

        # Chunk posities (zelfde als eerder)
        chunk_positions = np.array([
            [2.5, 2.0, 1.5],
            [2.8, 1.5, 2.0],
            [3.0, 2.5, 1.8],   # Relevant
            [-2.0, 1.0, -1.5],
            [-2.5, -1.0, 1.0]
        ])

        # Query positie (dichtbij chunk 3)
        query_pos = np.array([3.2, 2.3, 2.0])

        # Skip ground shadows for performance

        # Query vector verschijnt met animatie (simplified)
        if progress > 0:
            query_alpha = min(1.0, progress / 0.2)

            # Query star - SIMPLIFIED (no pulse)
            ax.scatter([query_pos[0]], [query_pos[1]], [query_pos[2]],
                      s=600,
                      c=self.colors['highlight'],
                      marker='*',
                      edgecolors='white',
                      linewidths=3,
                      alpha=query_alpha,
                      depthshade=True)

            ax.text(query_pos[0], query_pos[1], query_pos[2] + 0.8,
                   'Vraag Vector',
                   fontsize=27,
                   ha='center',
                   color=self.colors['highlight'],
                   fontweight='bold',
                   alpha=query_alpha)

        # Chunks verschijnen (simplified animation)
        for i, pos in enumerate(chunk_positions):
            chunk_start = 0.15 + i * 0.05
            if progress > chunk_start:
                chunk_alpha = min(1.0, (progress - chunk_start) / 0.15)

                # Highlight relevante chunk anders
                is_relevant = (i == 2)
                color = self.colors['cyan'] if not is_relevant else self.colors['accent']
                size = 600 if is_relevant else 500

                # Draw vector line from origin
                ax.plot([0, pos[0]], [0, pos[1]], [0, pos[2]],
                       color=color,
                       linewidth=2 if is_relevant else 1.5,
                       alpha=chunk_alpha * 0.5,
                       linestyle='-' if is_relevant else '--')

                # Draw the point itself - SIMPLIFIED (no breathing)
                ax.scatter([pos[0]], [pos[1]], [pos[2]],
                          s=size,
                          c=[color],
                          edgecolors='white',
                          linewidths=3 if is_relevant else 2,
                          alpha=chunk_alpha * 0.9,
                          depthshade=True)

                # Label
                ax.text(pos[0], pos[1], pos[2] - 0.6,
                       f'Chunk {i+1}',
                       fontsize=18 if is_relevant else 16,
                       ha='center',
                       color='white',
                       fontweight='bold' if is_relevant else 'normal',
                       alpha=chunk_alpha,
                       bbox=dict(boxstyle='round,pad=0.4',
                               facecolor=color,
                               edgecolor='white' if is_relevant else 'none',
                               linewidth=2,
                               alpha=0.8))

        # Simplified search rays (NO particles for performance)
        if progress > 0.4:
            ray_progress = min(1.0, (progress - 0.4) / 0.2)

            for i, pos in enumerate(chunk_positions):
                # Simple dotted lines - much faster
                ax.plot([query_pos[0], pos[0]],
                       [query_pos[1], pos[1]],
                       [query_pos[2], pos[2]],
                       color=self.colors['secondary'],
                       linestyle=':',
                       alpha=0.6 * ray_progress,
                       linewidth=2)

        # Highlight beste match (chunk 3) - SIMPLIFIED
        if progress > 0.65:
            best_alpha = min(1.0, (progress - 0.65) / 0.2)
            best_pos = chunk_positions[2]

            # Single highlight layer (no pulse, no multiple layers)
            ax.scatter([best_pos[0]], [best_pos[1]], [best_pos[2]],
                      s=800,
                      c=[self.colors['secondary']],
                      edgecolors='white',
                      linewidths=5,
                      alpha=best_alpha * 0.95,
                      depthshade=True)

            # Thick connection line
            ax.plot([query_pos[0], best_pos[0]],
                   [query_pos[1], best_pos[1]],
                   [query_pos[2], best_pos[2]],
                   color=self.colors['secondary'],
                   linestyle='-',
                   alpha=0.95 * best_alpha,
                   linewidth=6)

            # Distance indicator
            distance = np.linalg.norm(query_pos - best_pos)
            mid_point = (query_pos + best_pos) / 2

            ax.text(best_pos[0], best_pos[1], best_pos[2] - 1.2,
                   'Chunk 3\nBeste Match!',
                   fontsize=20,
                   ha='center',
                   color='white',
                   fontweight='bold',
                   alpha=best_alpha,
                   bbox=dict(boxstyle='round,pad=0.6',
                            facecolor=self.colors['secondary'],
                            edgecolor='white',
                            linewidth=3,
                            alpha=0.95))

        # Similarity Meter (2D overlay on 3D plot)
        if progress > 0.75:
            meter_progress = min(1.0, (progress - 0.75) / 0.25)

            # Initialize similarity meter if not exists
            if self.similarity_meter is None:
                # Position in figure coordinates (separate from 3D plot)
                self.similarity_meter = SimilarityMeter(
                    x=85, y=25, radius=10,
                    colors={
                        'low': self.colors['warning'],
                        'medium': self.colors['accent'],
                        'high': self.colors['secondary']
                    }
                )

            # Create 2D overlay axes for the meter
            ax2d = self.fig.add_axes([0.75, 0.05, 0.2, 0.2])
            ax2d.set_xlim(70, 100)
            ax2d.set_ylim(10, 40)
            ax2d.axis('off')

            # Draw similarity meter
            self.similarity_meter.draw(ax2d, score=89.0, progress=meter_progress)

        self.add_status_indicator(progress < 1.0)
        # Skip tight_layout for 3D plots - causes issues

    def draw_context_ophalen(self, progress):
        """Step 7: Context retrieval with flying chunk animation"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Titel
        ax.text(50, 97, 'Stap 9: Context Ophalen',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['secondary'])

        ax.text(50, 90, 'Meest relevante chunk wordt opgehaald',
                fontsize=27, ha='center', va='top',
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

            ax.text(20, 50, 'DB',
                    fontsize=52, ha='center', va='center',
                    fontweight='bold',
                    color=self.colors['primary'],
                    alpha=db_alpha)

            ax.text(20, 41, 'Vector DB',
                    fontsize=21, ha='center', va='center',
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
                    fontsize=21, ha='center', va='center',
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
                    fontsize=33, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold',
                    alpha=context_alpha)

            # Chunk inhoud
            wrapped_chunk = textwrap.fill(self.chunks[2], width=25)
            ax.text(80, 50, wrapped_chunk,
                    fontsize=18, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=context_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_llm_generatie(self, progress):
        """Step 8: LLM generation with detailed inputs"""
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.axis('off')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)

        # Titel
        ax.text(50, 97, 'Stap 10: LLM Generatie',
                fontsize=51, fontweight='bold', ha='center', va='top',
                color=self.colors['primary'])

        ax.text(50, 90, 'Language Model combineert vraag + context tot antwoord',
                fontsize=27, ha='center', va='top',
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
                    fontsize=16, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold',
                    alpha=input_alpha)

            wrapped_vraag = textwrap.fill(self.vraag, width=30)
            ax.text(27.5, 69, wrapped_vraag,
                    fontsize=18, ha='center', va='center',
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
                    fontsize=16, ha='center', va='center',
                    color=self.colors['secondary'],
                    fontweight='bold',
                    alpha=input_alpha)

            ax.text(72.5, 69, 'Chunk 3:\n"Het wijzigingsproces..."',
                    fontsize=18, ha='center', va='center',
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

            ax.text(50, 50, 'LLM',
                    fontsize=67, ha='center', va='center',
                    fontweight='bold',
                    color=self.colors['primary'],
                    alpha=llm_alpha)

            ax.text(50, 38, 'Language Model',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['primary'],
                    fontweight='bold',
                    alpha=llm_alpha)

        # "Denk" animatie
        if 0.5 < progress < 0.8:
            think_progress = (progress - 0.5) / 0.3
            num_dots = int(think_progress * 3) % 4
            dots = '.' * num_dots

            ax.text(50, 30, f'Aan het verwerken{dots}',
                    fontsize=16, ha='center', va='center',
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

            ax.text(50, 15, '>> Antwoord',
                    fontsize=33, ha='center', va='center',
                    color=self.colors['primary'],
                    fontweight='bold',
                    alpha=output_alpha)

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def draw_antwoord(self, progress):
        """Step 9: Final answer with typewriter effect and pulse"""
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
            fontsize = 42 * pulse
        else:
            fontsize = 42

        ax.text(50, 95, 'Stap 11: Het Antwoord!',
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
                    fontsize=19, ha='center', va='top',
                    color=self.colors['text'],
                    alpha=min(1.0, text_progress * 1.5))

        # Succesboodschap
        if progress > 0.9:
            success_alpha = (progress - 0.9) / 0.1

            ax.text(50, 10, '*** RAG Journey Compleet! ***',
                    fontsize=33, ha='center', va='center',
                    color=self.colors['highlight'],
                    fontweight='bold',
                    alpha=success_alpha)

            ax.text(50, 5, 'Van kennisartikel naar accuraat antwoord in 10 stappen',
                    fontsize=24, ha='center', va='center',
                    color=self.colors['text'],
                    alpha=0.7 * success_alpha,
                    style='italic')

        self.add_status_indicator(progress < 1.0)
        plt.tight_layout()

    def add_status_indicator(self, is_animating):
        """Add progress indicator"""
        if is_animating:
            self.fig.text(0.95, 0.02, '...', fontsize=24, ha='right', va='bottom',
                         color=self.colors['accent'], fontweight='bold')


def main():
    """Main entry point"""
    print("="*80)
    print("RAG JOURNEY VISUALIZATION")
    print("="*80)
    print("\n🔍 Deze presentatie toont Retrieval Augmented Generation:")
    print("  1. Kennisartikel - Retourbeleid webwinkel")
    print("  2. Tekst Chunking - Opdelen in stukken")
    print("  3. Embeddings - Chunks → Vectors")
    print("  4. Vector Database - Opslag")
    print("  5. Gebruikersvraag - Input")
    print("  6. Query Embedding - Vraag → Vector")
    print("  7. Similarity Search - Beste match vinden")
    print("  8. Context Ophalen - Relevante chunk")
    print("  9. LLM Generatie - Antwoord genereren")
    print(" 10. Antwoord Tonen - Resultaat!")
    print("\n[Keys]  Controls: SPACE=Next | B=Previous | R=Reset | S=Menu | Q=Quit")
    print("="*80 + "\n")

    presentation = RAGPresentation()
    presentation.show()


if __name__ == "__main__":
    main()
