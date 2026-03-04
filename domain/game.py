from domain.enums.phase import Phase


class Game:

    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player = player1
        self.first_player = player1
        self.turn_number = 1
        self.phase = Phase.DRAW
        self.is_running = False

    # ==============================
    # CONTROLE DE JOGO
    # ==============================

    def start(self):
        self.is_running = True

        # Cada jogador compra mão inicial
        for player in self.players:
            player.draw_starting_hand()

    def end(self):
        self.is_running = False

    # ==============================
    # TROCAR JOGADOR
    # ==============================

    def switch_player(self):
        current_index = self.players.index(self.current_player)
        next_index = (current_index + 1) % len(self.players)
        self.current_player = self.players[next_index]

    # ==============================
    # VERIFICAR VENCEDOR
    # ==============================

    def check_winner(self):
        for player in self.players:
            if player.is_dead():
                return [p for p in self.players if p != player][0]
        return None
