import os
import json


class CardService:

    def __init__(self, save_path="data/cards"):
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)

    def save_card(self, card_data):
        file_path = os.path.join(self.save_path, f"{card_data['id']}.json")

        if os.path.exists(file_path):
            raise ValueError("Já existe uma carta com esse ID.")

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(card_data, file, indent=4, ensure_ascii=False)
