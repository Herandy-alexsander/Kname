from player import Player
from game import Game
from card import Card

# Decks de exemplo (temporário)
deck1 = [Card("Soldado", 1), Card("Guerreiro", 2)] * 20
deck2 = [Card("Arqueiro", 1), Card("Cavaleiro", 2)] * 20

player1 = Player("Jogador 1", deck1)
player2 = Player("Jogador 2", deck2)

game = Game(player1, player2)
game.start_game()

while True:
    game.next_turn()
