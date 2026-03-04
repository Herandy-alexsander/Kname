import random
from domain.services.turn_service import TurnService
from domain.enums.phase import Phase


class MatchController:

    def __init__(self, game, interface):
        self.game = game
        self.interface = interface

    def start_match(self):

        # ===== INÍCIO DO JOGO =====

        # Compra inicial (5 cartas)
        for player in self.game.players:
            player.draw_starting_hand()
            self.interface.handle_mulligan(player)

        # Decide primeiro jogador aleatoriamente
        self.game.first_player = random.choice(self.game.players)
        self.game.current_player = self.game.first_player

        # Inicialização oficial do turno
        self.game.phase = Phase.DRAW
        self.game.turn_number = 1

        self.interface.show_message(
            f"{self.game.current_player.name} começa o jogo!"
        )

        # ===== LOOP PRINCIPAL =====
        while not self.is_game_over():

            self.interface.show_message(
                f"\n=== TURNO {self.game.turn_number} | {self.game.phase.name} ==="
            )

            # 🔥 AGORA PASSA A INTERFACE
            TurnService.next_phase(self.game, self.interface)

        self.end_game()

    def is_game_over(self):
        return any(player.is_dead() for player in self.game.players)

    def end_game(self):
        loser = next(p for p in self.game.players if p.is_dead())
        winner = next(p for p in self.game.players if not p.is_dead())

        self.interface.show_message(
            f"{winner.name} venceu! {loser.name} perdeu."
        )
