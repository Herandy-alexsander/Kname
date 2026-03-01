import os
import json
from domain.enums.card_type import CardType


class CardCreator:

    def __init__(self, save_path="data/cards"):
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)

    def create_card(self):
        print("=== Cadastro de Nova Carta ===")

        card_id = input("ID da carta: ").strip()
        name = input("Nome da carta: ").strip()

        print("Tipos disponíveis: tropa, item, reacao")
        card_type_input = input("Tipo da carta: ").strip().lower()

        if card_type_input not in [t.value for t in CardType]:
            print("Tipo inválido.")
            return

        cost = int(input("Custo: "))
        power = int(input("Poder (0 se não tiver): "))
        toughness = int(input("Resistência (0 se não tiver): "))

        card_data = {
            "id": card_id,
            "name": name,
            "type": card_type_input,
            "cost": cost,
            "power": power,
            "toughness": toughness,
            "effects": [],
            "image": ""  # reservado para futuro sistema de imagens
        }

        self._save_to_json(card_data)

        print(f"\nCarta '{name}' criada com sucesso!")

    def _save_to_json(self, card_data):
        file_path = os.path.join(self.save_path, f"{card_data['id']}.json")

        if os.path.exists(file_path):
            print("Já existe uma carta com esse ID.")
            return

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(card_data, file, indent=4, ensure_ascii=False)
