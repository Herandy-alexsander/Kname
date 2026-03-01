import os
from application.card_service import CardService


class CardEditor:

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

    def __init__(self):
        self.service = CardService()
        self.save_path = self.service.save_path

    # ==========================
    # MENU PRINCIPAL
    # ==========================
    def start(self):
        print("=== EDITOR DE CARTAS ===")
        print("1 - Criação Rápida")
        print("2 - Criação Detalhada")
        print("3 - Sair")

        option = input("Escolha uma opção: ")

        if option == "1":
            self.quick_create()
        elif option == "2":
            self.detailed_create()
        else:
            print("Encerrando editor...")

    # ==========================
    # MENU DE TIPO NUMÉRICO
    # ==========================
    def choose_type(self):
        print("\nEscolha o tipo da carta:")
        print("1 - Tropa")
        print("2 - Item")
        print("3 - Reação")

        option = input("Digite o número correspondente: ")

        if option not in self.TYPE_MENU:
            raise ValueError("Tipo inválido.")

        return self.TYPE_MENU[option]

    # ==========================
    # GERAÇÃO AUTOMÁTICA DE ID
    # ==========================
    def generate_serial_id(self, card_type):

        prefix = self.PREFIX_MAP.get(card_type)

        if not prefix:
            raise ValueError("Tipo inválido.")

        existing_numbers = []

        for filename in os.listdir(self.save_path):
            if filename.startswith(prefix) and filename.endswith(".json"):
                number_part = filename.replace(prefix, "").replace(".json", "")
                if number_part.isdigit():
                    existing_numbers.append(int(number_part))

        next_number = 1 if not existing_numbers else max(existing_numbers) + 1

        return f"{prefix}{next_number:03d}"

    # ==========================
    # CRIAÇÃO RÁPIDA
    # ==========================
    def quick_create(self):
        print("\n=== Criação Rápida ===")

        card_type = self.choose_type()
        card_id = self.generate_serial_id(card_type)

        card_data = {
            "id": card_id,
            "name": input("Nome: "),
            "type": card_type,
            "cost": int(input("Custo: ")),
            "power": 0,
            "toughness": 0,
            "effects": [],
            "image": ""
        }

        self.service.save_card(card_data)
        print(f"\nCarta criada com sucesso! ID gerado: {card_id}\n")

    # ==========================
    # CRIAÇÃO DETALHADA
    # ==========================
    def detailed_create(self):
        print("\n=== Criação Detalhada ===")

        card_type = self.choose_type()
        card_id = self.generate_serial_id(card_type)

        name = input("Nome: ")
        cost = int(input("Custo: "))
        power = int(input("Poder: "))
        toughness = int(input("Resistência: "))

        effects = []
        print("Digite efeitos (digite 'fim' para encerrar):")

        while True:
            effect = input("Efeito: ")
            if effect.lower() == "fim":
                break
            effects.append(effect)

        card_data = {
            "id": card_id,
            "name": name,
            "type": card_type,
            "cost": cost,
            "power": power,
            "toughness": toughness,
            "effects": effects,
            "image": ""
        }

        self.service.save_card(card_data)
        print(f"\nCarta criada com sucesso! ID gerado: {card_id}\n")


if __name__ == "__main__":
    editor = CardEditor()
    editor.start()
