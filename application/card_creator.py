import os
import json
from domain.enums.card_type import CardType


class CardCreator:

    PREFIX_MAP = {
        "tropa": "TR",
        "item": "IT",
        "reacao": "RE"
    }

    TYPE_MENU = {
        "1": "tropa",
        "2": "item",
        "3": "reacao"
    }

    def __init__(self, save_path="data/cards"):
        self.save_path = save_path
        os.makedirs(self.save_path, exist_ok=True)

    # ==========================================
    # MENU INICIAL
    # ==========================================

    def start(self):
        print("=== CARD CREATOR ===")
        print("1 - Cadastrar carta individual")
        print("2 - Cadastrar múltiplas cartas (JSON)")
        choice = input("Escolha: ")

        if choice == "1":
            self.create_card()
        elif choice == "2":
            self.create_multiple_cards()
        else:
            print("Opção inválida.")

    # ==========================================
    # GERADOR DE ID AUTOMÁTICO
    # ==========================================

    def _generate_id(self, card_type):
        prefix = self.PREFIX_MAP[card_type]

        existing_files = os.listdir(self.save_path)
        numbers = []

        for filename in existing_files:
            if filename.startswith(prefix):
                number_part = filename.replace(prefix, "").replace(".json", "")
                if number_part.isdigit():
                    numbers.append(int(number_part))

        next_number = max(numbers, default=0) + 1

        return f"{prefix}{str(next_number).zfill(3)}"

    # ==========================================
    # SELECIONAR TIPO POR NÚMERO
    # ==========================================

    def _select_card_type(self):
        print("\nTipos disponíveis:")
        print("1 - Tropa")
        print("2 - Item")
        print("3 - Reação")

        choice = input("Escolha o número do tipo: ").strip()

        if choice not in self.TYPE_MENU:
            print("Tipo inválido.")
            return None

        return self.TYPE_MENU[choice]

    # ==========================================
    # CADASTRO INDIVIDUAL
    # ==========================================

    def create_card(self):
        print("\n=== Cadastro de Nova Carta ===")

        name = input("Nome da carta: ").strip()

        card_type_input = self._select_card_type()
        if not card_type_input:
            return

        cost = int(input("Custo: "))
        power = int(input("Poder (0 se não tiver): "))
        toughness = int(input("Resistência (0 se não tiver): "))

        card_id = self._generate_id(card_type_input)

        card_data = {
            "id": card_id,
            "name": name,
            "type": card_type_input,
            "cost": cost,
            "power": power,
            "toughness": toughness,
            "effects": [],
            "image": ""
        }

        self._save_to_json(card_data)

        print(f"\nCarta '{name}' criada com ID {card_id}!")

    # ==========================================
    # CADASTRO MÚLTIPLO (JSON)
    # ==========================================

    def create_multiple_cards(self):
        print("\nInforme o caminho do arquivo JSON:")
        file_path = input("> ").strip()

        if not os.path.exists(file_path):
            print("Arquivo não encontrado.")
            return

        with open(file_path, "r", encoding="utf-8") as file:
            cards = json.load(file)

        for card in cards:

            card_type = card.get("type")

            if card_type not in self.PREFIX_MAP:
                print(f"Tipo inválido para carta {card.get('name')}")
                continue

            card_id = self._generate_id(card_type)

            card_data = {
                "id": card_id,
                "name": card.get("name"),
                "type": card_type,
                "cost": card.get("cost", 0),
                "power": card.get("power", 0),
                "toughness": card.get("toughness", 0),
                "effects": card.get("effects", []),
                "image": card.get("image", "")
            }

            self._save_to_json(card_data)

            print(f"✔ {card_data['name']} criada com ID {card_id}")

    # ==========================================
    # SALVAR JSON
    # ==========================================

    def _save_to_json(self, card_data):
        file_path = os.path.join(self.save_path, f"{card_data['id']}.json")

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(card_data, file, indent=4, ensure_ascii=False)
