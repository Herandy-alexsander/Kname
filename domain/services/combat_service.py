from domain.services.state_based_actions import StateBasedActions


class CombatService:

    @staticmethod
    def handle_combat(game, interface):

        attacker_player = game.current_player
        defender_player = [p for p in game.players if p != attacker_player][0]

        interface.show_message("\n=== FASE DE COMBATE ===")

        while True:

            # -------------------------
            # 1️⃣ Escolher atacante
            # -------------------------
            attacking_troop = interface.choose_attacker(attacker_player)

            if attacking_troop is None:
                interface.show_message("Encerrando fase de combate.")
                break

            if getattr(attacking_troop, "has_attacked", False):
                interface.show_message("Essa tropa já atacou este turno.")
                continue

            # -------------------------
            # 2️⃣ Escolher bloqueadores
            # -------------------------
            blockers = interface.choose_blockers(defender_player, attacking_troop)

            # -------------------------
            # 3️⃣ Resolver dano
            # -------------------------
            if not blockers:
                interface.show_message(
                    f"{attacking_troop.name} causa "
                    f"{attacking_troop.power} de dano direto!"
                )
                defender_player.take_damage(attacking_troop.power)

            else:
                interface.show_message(
                    f"{attacking_troop.name} foi bloqueada por "
                    f"{', '.join(b.name for b in blockers)}"
                )

                # Dano do atacante em TODOS bloqueadores
                for blocker in blockers:
                    blocker.take_damage(attacking_troop.power)

                # Soma do poder dos bloqueadores no atacante
                total_block_power = sum(b.power for b in blockers)
                attacking_troop.take_damage(total_block_power)

            attacking_troop.has_attacked = True

            # -------------------------
            # 4️⃣ State Based Actions
            # -------------------------
            StateBasedActions.check_all(game)

            # Verifica se alguém morreu
            if defender_player.is_dead() or attacker_player.is_dead():
                break
