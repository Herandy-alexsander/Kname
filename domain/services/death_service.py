class DeathService:

    @staticmethod
    def check_dead_troops(game):
        """
        Remove tropas mortas do campo e envia para o cemitério.
        """

        for player in game.players:
            dead_troops = []

            for card in player.battlefield:
                if hasattr(card, "is_dead") and card.is_dead():
                    dead_troops.append(card)

            for troop in dead_troops:
                player.battlefield.remove(troop)
                player.graveyard.append(troop)
