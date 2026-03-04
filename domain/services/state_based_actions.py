# domain/services/state_based_actions.py

class StateBasedActions:

    @staticmethod
    def check_deaths(player):
        """
        Verifica criaturas mortas no campo
        e move para o descarte
        """

        alive_cards = []

        for card in player.battlefield:

            # só verifica se for tropa
            if hasattr(card, "is_dead") and card.is_dead():
                print(f"{card.name} foi destruída!")
                player.discard_pile.append(card)
            else:
                alive_cards.append(card)

        player.battlefield = alive_cards

    # ==============================
    # NOVO MÉTODO ADICIONADO
    # ==============================

    @staticmethod
    def check_all(game):
        """
        Aplica ações baseadas em estado para todos os jogadores
        """

        for player in game.players:
            StateBasedActions.check_deaths(player)
