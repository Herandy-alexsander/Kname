from application.deck_service import DeckService
from infrastructure.card_repository import CardRepository


class DeckBuilder:

    def __init__(self):
        self.service = DeckService()
        self.repository = CardRepository()
        self.repository.load_cards()

    def start(self):
        print("=== DECK BUILDER ===")
        deck_name = input("Nome do deck: ")

        print("\nCartas disponíveis:")
        for card in self.repository.get_all_cards():
            print(f"{card.id} - {card.name}")

        deck_cards = []

        print("\nAdicione cartas pelo ID (digite 'fim' para parar):")

        while len(deck_cards) < 40:
            print(f"Cartas no deck: {len(deck_cards)}/40")
            card_id = input("ID da carta: ")

            if card_id.lower() == "fim":
                break

            deck_cards.append(card_id)

        try:
            self.service.save_deck(deck_name, deck_cards)
        except ValueError as e:
            print("Erro:", e)


if __name__ == "__main__":
    builder = DeckBuilder()
    builder.start()
