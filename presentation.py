
#!/usr/bin/env python3
"""
AI Presentation Suite - Main Controller
Navigate between all presentations with unified controls

Usage:
    python presentation.py              # Show menu
    python presentation.py vector       # Start with vector presentation
    python presentation.py all          # Auto-play all presentations in sequence
"""

import sys
import importlib
from typing import Optional, List
from presentations.main_menu import MainMenu


class PresentationController:
    """
    Main controller for the AI Presentation Suite
    Manages navigation between multiple presentations
    """

    def __init__(self):
        """Initialize the presentation controller"""
        # Define presentation order and metadata
        self.presentations = [
            {
                'id': 'vector',
                'name': 'Vector & Embeddings',
                'module': 'presentations.vector_presentation',
                'class': 'VectorPresentation',
                'description': 'Begrijp vectorruimtes en semantische embeddings',
                'icon': '[V]',
                'duration': '~8 minuten'
            },
            {
                'id': 'neural',
                'name': 'Neural Networks',
                'module': 'presentations.neural_network_presentation_new',
                'class': 'NeuralNetworkPresentation',
                'description': 'Stapsgewijze uitleg: van concept naar XOR training',
                'icon': '[NN]',
                'duration': '~8 minuten'
            },
            {
                'id': 'rag',
                'name': 'RAG Journey',
                'module': 'presentations.rag_presentation',
                'class': 'RAGPresentation',
                'description': 'Van kennisartikel naar AI-antwoord met RAG',
                'icon': '[<>]',
                'duration': '~10 minuten'
            },
            {
                'id': 'finetuning',
                'name': 'Finetuning Journey',
                'module': 'presentations.finetuning_presentation',
                'class': 'FinetuningPresentation',
                'description': 'Van basis model naar domein-specialist',
                'icon': '>>',
                'duration': '~12 minuten'
            },
            {
                'id': 'quality',
                'name': 'AI Quality',
                'module': 'presentations.quality_presentation_new',
                'class': 'QualityPresentation',
                'description': 'Praktische inzichten: keuzes, modellen & actie',
                'icon': '[!]',
                'duration': '~6 minuten'
            }
        ]

        self.current_index = 0

    def show_menu(self):
        """Display visual interactive menu for presentation selection"""
        menu = MainMenu(self.presentations)
        choice = menu.show()

        # Convert choice to presentation ID
        if choice == 'q' or choice is None:
            return None
        elif choice == 'all':
            return 'all'
        else:
            # Choice is a number (1-5)
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.presentations):
                    return self.presentations[idx]['id']
            except (ValueError, IndexError):
                return None

        return None

    def get_user_choice(self) -> Optional[str]:
        """
        Get user's menu choice

        Returns:
            Presentation ID or 'all' or None to quit
        """
        while True:
            choice = input("\n👉 Keuze: ").strip().lower()

            if choice == 'q':
                return None

            if choice == 'all':
                return 'all'

            # Check if it's a number
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.presentations):
                    return self.presentations[idx]['id']
                else:
                    print(f"❌ Ongeldige keuze. Kies 1-{len(self.presentations)}, 'all', of 'q'")
            except ValueError:
                # Try to match by ID
                matching = [p for p in self.presentations if p['id'].startswith(choice)]
                if len(matching) == 1:
                    return matching[0]['id']
                elif len(matching) > 1:
                    print(f"❌ Meerdere matches. Wees specifieker: {[p['id'] for p in matching]}")
                else:
                    print(f"❌ Onbekende presentatie: '{choice}'")

    def run_presentation(self, presentation_id: str) -> bool:
        """
        Run a specific presentation

        Args:
            presentation_id: ID of presentation to run

        Returns:
            True if successful, False otherwise
        """
        # Find presentation
        pres_info = next((p for p in self.presentations if p['id'] == presentation_id), None)
        if not pres_info:
            print(f"❌ Presentatie niet gevonden: {presentation_id}")
            return False

        print(f"\n▶️  Starting: {pres_info['icon']} {pres_info['name']}")
        print(f"   {pres_info['description']}")
        print(f"   {pres_info['duration']}\n")

        try:
            # Dynamically import and instantiate presentation
            module = importlib.import_module(pres_info['module'])
            presentation_class = getattr(module, pres_info['class'])

            # Create and show presentation
            presentation = presentation_class()
            presentation.show()

            print(f"\n✅ Presentatie '{pres_info['name']}' afgesloten")
            return True

        except ModuleNotFoundError as e:
            print(f"\n❌ Presentatie module niet gevonden: {e}")
            print(f"   Zorg dat {pres_info['module']}.py bestaat in de juiste map")
            return False

        except Exception as e:
            print(f"\n❌ Fout bij laden presentatie: {e}")
            import traceback
            traceback.print_exc()
            return False

    def run_all_presentations(self):
        """Run all presentations in sequence"""
        print(f"\n🎬 Start volledige presentatie suite ({len(self.presentations)} presentaties)")
        print("   Druk Q in elke presentatie om terug te gaan naar menu\n")

        for idx, pres in enumerate(self.presentations, 1):
            print(f"\n{'='*80}")
            print(f"Presentatie {idx}/{len(self.presentations)}")
            print(f"{'='*80}")

            success = self.run_presentation(pres['id'])

            if not success:
                print(f"\n(!)  Overslaan naar volgende presentatie...")

        print(f"\n🎉 Presentatie suite compleet!")
        print("   Terug naar hoofdmenu...\n")

    def run(self):
        """Main entry point - run the controller"""
        # Check for command line argument
        if len(sys.argv) > 1:
            arg = sys.argv[1].lower()

            if arg == 'all':
                self.run_all_presentations()
                # After 'all', continue to menu instead of returning
            elif self.run_presentation(arg):
                # After running specific presentation, continue to menu
                print("\n   Terug naar hoofdmenu...\n")
            else:
                # If failed, show menu
                print(f"(!)  Onbekend argument: {arg}")
                print("   Toon hoofdmenu...\n")

        # Show interactive menu - loop until quit
        while True:
            choice = self.show_menu()

            if choice is None:
                # User pressed Q in menu
                print("\n👋 Tot ziens!")
                break

            if choice == 'all':
                self.run_all_presentations()
                # After running all, return to menu automatically
            else:
                self.run_presentation(choice)
                # After presentation ends (Q pressed), return to menu automatically


def main():
    """Main entry point"""
    try:
        controller = PresentationController()
        controller.run()
    except KeyboardInterrupt:
        print("\n\n👋 Presentatie afgebroken. Tot ziens!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Onverwachte fout: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
