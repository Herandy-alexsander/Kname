from domain.enums.phase import Phase
from domain.services.combat_service import CombatService
from domain.services.state_based_actions import StateBasedActions


class TurnService:

    @staticmethod
    def next_phase(game, interface):

        # =========================
        # 1️⃣ ETAPA DE COMPRA
        # =========================
        if game.phase == Phase.DRAW:

            # Primeiro jogador NÃO compra no turno 1
            if not (
                game.turn_number == 1
                and game.current_player == game.first_player
            ):
                card = game.current_player.draw()
                if card:
                    interface.show_message(
                        f"{game.current_player.name} comprou {card.name}"
                    )

            game.phase = Phase.COMBAT
            return

        # =========================
        # 2️⃣ FASE DE COMBATE
        # =========================
        if game.phase == Phase.COMBAT:

            CombatService.handle_combat(game, interface)

            game.phase = Phase.MAIN
            return

        # =========================
        # 3️⃣ FASE PRINCIPAL
        # =========================
        if game.phase == Phase.MAIN:

            interface.handle_main_phase(game)

            game.phase = Phase.END
            return

        # =========================
        # 4️⃣ FASE FINAL
        # =========================
        if game.phase == Phase.END:

            TurnService.end_turn(game, interface)
            return

    @staticmethod
    def end_turn(game, interface):

        current_player = game.current_player

        # =========================
        # 1️⃣ AÇÕES BASEADAS EM ESTADO
        # =========================
        StateBasedActions.check_all(game)

        # =========================
        # 2️⃣ LIMITE DE MÃO (KNAME)
        # =========================
        while len(current_player.hand) > 5:

            interface.show_message(
                f"{current_player.name} tem mais de 5 cartas na mão e deve descartar."
            )

            card_to_discard = interface.choose_card_to_discard(current_player)

            if card_to_discard:
                current_player.hand.remove(card_to_discard)
                current_player.discard_pile.append(card_to_discard)

                interface.show_message(
                    f"{card_to_discard.name} foi descartada."
                )

        # =========================
        # 3️⃣ RESET DE TURNO DAS CARTAS
        # =========================
        for player in game.players:
            for card in player.battlefield:
                if hasattr(card, "reset_turn"):
                    card.reset_turn()

        # =========================
        # 4️⃣ TROCAR JOGADOR
        # =========================
        game.current_player = (
            game.players[0]
            if game.current_player == game.players[1]
            else game.players[1]
        )

        game.phase = Phase.DRAW
        game.turn_number += 1
