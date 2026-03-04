from application.card_creator import CardCreator
from tools.deck_builder import DeckBuilder

from domain.entities.player import Player
from domain.game import Game
from domain.services.turn_service import TurnService
from presentation.cli_interface import CLIInterface
from infrastructure.card_repository import CardRepository

import json
import os
import random


# ==========================================
# INICIAR PARTIDA USANDO DECK SALVO
# ==========================================
def iniciar_partida():

    repo = CardRepository()
    repo.load_cards()

    print("\nDecks disponíveis:")
    listar_decks()

    deck_name1 = input("\nNome do deck do Jogador 1: ")
    deck_name2 = input("Nome do deck do Jogador 2: ")

    deck1 = carregar_deck(deck_name1, repo)
    deck2 = carregar_deck(deck_name2, repo)

    if not deck1 or not deck2:
        print("Erro ao carregar decks.")
        return

    player1 = Player("Jogador 1", deck1)
    player2 = Player("Jogador 2", deck2)

    game = Game(player1, player2)
    interface = CLIInterface()

    game.start()

    while game.is_running:
        TurnService.next_phase(game, interface)

        winner = game.check_winner()
        if winner:
            print(f"\n🏆 {winner.name} venceu o jogo!")
            game.end()


# ==========================================
# CARREGAR DECK DO JSON
# ==========================================
def carregar_deck(deck_name, repo):

    file_path = os.path.join("data/decks", f"{deck_name}.json")

    if not os.path.exists(file_path):
        print(f"Deck '{deck_name}' não encontrado.")
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    deck_cards = []

    for card_id in data["cards"]:
        card = repo.get_card(card_id)
        if card:
            deck_cards.append(card)

    random.shuffle(deck_cards)

    return deck_cards


# ==========================================
# LISTAR DECKS DISPONÍVEIS
# ==========================================
def listar_decks():

    decks_path = "data/decks"

    if not os.path.exists(decks_path):
        print("Nenhum deck encontrado.")
        return

    for file in os.listdir(decks_path):
        if file.endswith(".json"):
            print("-", file.replace(".json", ""))


# ==========================================
# MENU PRINCIPAL
# ==========================================
def menu():

    while True:
        print("\n=== KNAME ===")
        print("1 - Iniciar Partida")
        print("2 - Cadastrar Carta")
        print("3 - Cadastrar Deck")
        print("4 - Sair")

        choice = input("Escolha uma opção: ")

        if choice == "1":
            iniciar_partida()

        elif choice == "2":
            creator = CardCreator()
            creator.start()

        elif choice == "3":
            builder = DeckBuilder()
            builder.start()

        elif choice == "4":
            print("Encerrando...")
            break

        else:
            print("Opção inválida.")


# ==========================================
# ENTRY POINT
# ==========================================
if __name__ == "__main__":
    menu()
