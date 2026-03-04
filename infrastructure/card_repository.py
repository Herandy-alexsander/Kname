import os
import json
import copy
from domain.entities.card import Card
from domain.enums.card_type import CardType


class CardRepository:

    def __init__(self, cards_path="data/cards"):
        self.cards_path = cards_path
        self.cards = {}

    # ==============================
    # CARREGAR CARTAS DO JSON
    # ==============================
    def load_cards(self):

        self.cards.clear()  # evita duplicação

        if not os.path.exists(self.cards_path):
            return

        for filename in os.listdir(self.cards_path):
            if filename.endswith(".json"):

                file_path = os.path.join(self.cards_path, filename)

                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                    try:
                        card = Card(
                            id=data["id"],
                            name=data["name"],
                            card_type=CardType(data["type"]),
                            cost=data["cost"],
                            power=data.get("power", 0),
                            toughness=data.get("toughness", 0),
                            effects=data.get("effects", []),
                            image_path=data.get("image", None)
                        )

                        self.cards[card.id] = card

                    except Exception as e:
                        print(f"Erro ao carregar carta {filename}: {e}")

    # ==============================
    # BUSCAR CARTA POR ID
    # ==============================
    def get_card(self, card_id):
        card = self.cards.get(card_id)
        return copy.deepcopy(card) if card else None

    # ==============================
    # LISTAR TODAS
    # ==============================
    def get_all_cards(self):
        return [copy.deepcopy(card) for card in self.cards.values()]

    def get_card_by_name(self, name):
        for card in self.cards.values():
            if card.name.lower() == name.lower():
                return copy.deepcopy(card)
        return None
