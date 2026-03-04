from application.deck_service import DeckService
from infrastructure.card_repository import CardRepository
import tkinter as tk
from tkinter import filedialog


class DeckBuilder:

    def __init__(self):
        self.service = DeckService()
        self.repository = CardRepository()
        self.repository.load_cards()

    def start(self):
        print("=== DECK BUILDER (Importar por TXT) ===")

        deck_name = input("Nome do deck: ")

        file_path = self._select_file()

        if not file_path:
            print("Nenhum arquivo selecionado.")
            return

        deck_cards = self._parse_txt(file_path)

        try:
            self.service.save_deck(deck_name, deck_cards)
        except ValueError as e:
            print("Erro:", e)

    # ===============================
    # Abrir janela para selecionar TXT
    # ===============================
    def _select_file(self):
        root = tk.Tk()
        root.withdraw()
        return filedialog.askopenfilename(
            title="Selecione o arquivo do deck",
            filetypes=[("Text files", "*.txt")]
        )

    # ===============================
    # Ler TXT e converter em IDs
    # ===============================
    def _parse_txt(self, file_path):
        deck_cards = []

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:

                line = line.strip()
                if not line:
                    continue

                try:
                    quantity, card_name = line.split(" ", 1)
                    quantity = int(quantity)
                except ValueError:
                    print(f"Linha inválida: {line}")
                    continue

                card = self.repository.get_card_by_name(card_name)

                if not card:
                    print(f"Carta não encontrada: {card_name}")
                    continue

                for _ in range(quantity):
                    deck_cards.append(card.id)

        return deck_cards


if __name__ == "__main__":
    builder = DeckBuilder()
    builder.start()
