import os
import json
from infrastructure.card_repository import CardRepository


class DeckService:

    MAX_CARDS = 40
    MAX_COPIES = 3

    def __init__(self, save_path="data/decks"):
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)
        self.card_repository = CardRepository()
        self.card_repository.load_cards()

    # ==============================
    # VALIDAÇÃO DO DECK
    # ==============================
    def validate_deck(self, deck_cards):

        if len(deck_cards) != self.MAX_CARDS:
            raise ValueError("O deck deve conter exatamente 40 cartas.")

        copies = {}
        for card_id in deck_cards:

            if not self.card_repository.get_card(card_id):
                raise ValueError(f"Carta inexistente: {card_id}")

            copies[card_id] = copies.get(card_id, 0) + 1

            if copies[card_id] > self.MAX_COPIES:
                raise ValueError(f"Máximo de 3 cópias permitido para {card_id}")

    # ==============================
    # SALVAR DECK
    # ==============================
    def save_deck(self, deck_name, deck_cards):

        self.validate_deck(deck_cards)

        file_path = os.path.join(self.save_path, f"{deck_name}.json")

        deck_data = {
            "deck_name": deck_name,
            "cards": deck_cards
        }

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(deck_data, file, indent=4, ensure_ascii=False)

        print(f"Deck '{deck_name}' salvo com sucesso!")
