import random
from enum import Enum


class Phase(Enum):
    DRAW = 1
    COMBAT = 2
    MAIN = 3
    END = 4


class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player = None
        self.turn_count = 1
        self.first_player = None
        self.current_phase = None

    def start_game(self):
        for player in self.players:
            player.draw_starting_hand()
            self.handle_mulligan(player)

        self.first_player = random.choice(self.players)
        self.current_player = self.first_player

        print(f"{self.current_player.name} começa o jogo!")

    def handle_mulligan(self, player):
        while True:
            choice = input(f"{player.name}, deseja mulligan? (s/n): ")
            if choice.lower() == "s":
                player.mulligan()
            else:
                break

    def next_turn(self):
        print("\n======================")
        print(f"Turno {self.turn_count}")
        print(f"Vez de {self.current_player.name}")
        print("======================")

        self.current_player.start_turn()

        for phase in Phase:
            self.current_phase = phase
            print(f"\n--- Fase {phase.name} ---")

            if phase == Phase.DRAW:
                self.draw_phase()
            elif phase == Phase.COMBAT:
                self.combat_phase()
            elif phase == Phase.MAIN:
                self.main_phase()
            elif phase == Phase.END:
                self.end_phase()

        self.switch_player()
        self.turn_count += 1

    # =========================
    # DRAW
    # =========================

    def draw_phase(self):
        if not (self.turn_count == 1 and self.current_player == self.first_player):
            self.current_player.draw()
        else:
            print("Primeiro jogador não compra no turno 1.")

    # =========================
    # COMBATE COM BLOQUEIO
    # =========================

    def combat_phase(self):
        attacker = self.current_player
        defender = (
            self.players[1]
            if self.current_player == self.players[0]
            else self.players[0]
        )

        print("\n=== FASE DE COMBATE ===")

        while True:
            available_troops = [
                card for card in attacker.battlefield
                if card.type == "TROPA" and not card.has_attacked
            ]

            if not available_troops:
                print("Nenhuma tropa disponível para atacar.")
                break

            print("\nTropas disponíveis:")
            for i, troop in enumerate(available_troops):
                print(f"{i} - {troop.name} ({troop.power}/{troop.current_toughness})")

            print("X - Encerrar combate")

            choice = input("Escolha tropa para atacar: ")

            if choice.lower() == "x":
                break

            if not choice.isdigit():
                print("Entrada inválida.")
                continue

            index = int(choice)

            if 0 <= index < len(available_troops):
                troop = available_troops[index]
                print(f"{attacker.name} ataca com {troop.name}!")

                # =========================
                # BLOQUEIO
                # =========================

                blocking_troops = [
                    card for card in defender.battlefield
                    if card.type == "TROPA"
                ]

                if blocking_troops:
                    print("\nTropas defensoras disponíveis para bloquear:")
                    for i, block in enumerate(blocking_troops):
                        print(f"{i} - {block.name} ({block.power}/{block.current_toughness})")

                    print("X - Não bloquear")

                    block_choice = input("Escolha bloqueador: ")

                    if block_choice.lower() == "x":
                        print("Ataque não bloqueado!")
                        defender.take_damage(troop.power)

                    elif block_choice.isdigit():
                        block_index = int(block_choice)

                        if 0 <= block_index < len(blocking_troops):
                            blocker = blocking_troops[block_index]

                            print(f"{blocker.name} bloqueia {troop.name}!")

                            # Dano simultâneo
                            troop.current_toughness -= blocker.power
                            blocker.current_toughness -= troop.power

                            print(f"{troop.name} fica com {troop.current_toughness} de resistência.")
                            print(f"{blocker.name} fica com {blocker.current_toughness} de resistência.")

                        else:
                            print("Bloqueador inválido.")
                            defender.take_damage(troop.power)
                    else:
                        print("Entrada inválida. Ataque não bloqueado.")
                        defender.take_damage(troop.power)
                else:
                    print("Defensor não possui tropas para bloquear.")
                    defender.take_damage(troop.power)

                troop.mark_as_attacked()

                # Verifica mortes
                attacker.check_dead_troops()
                defender.check_dead_troops()

                if defender.is_dead():
                    print(f"{defender.name} perdeu o jogo!")
                    exit()

            else:
                print("Índice inválido.")

    # =========================
    # MAIN
    # =========================

    def main_phase(self):
        player = self.current_player

        while True:
            print(f"\nRecursos: {player.resources}")
            print("1 - Gerar Recurso")
            print("2 - Jogar Carta")
            print("3 - Encerrar Fase")

            choice = input("Escolha: ")

            if choice == "1":
                player.generate_resource()

            elif choice == "2":
                if len(player.hand) == 0:
                    print("Mão vazia.")
                    continue

                for i, card in enumerate(player.hand):
                    print(f"{i} - {card.name} (Custo {card.cost})")

                idx_input = input("Escolha carta: ")

                if idx_input.isdigit():
                    idx = int(idx_input)
                    if 0 <= idx < len(player.hand):
                        player.play_card(player.hand[idx])
                    else:
                        print("Índice inválido.")
                else:
                    print("Entrada inválida.")

            elif choice == "3":
                break

    # =========================
    # END
    # =========================

    def end_phase(self):
        print("Encerrando turno...")
        self.current_player.check_dead_troops()

        if self.current_player.is_dead():
            print(f"{self.current_player.name} perdeu o jogo!")
            exit()

    # =========================

    def switch_player(self):
        self.current_player = (
            self.players[1]
            if self.current_player == self.players[0]
            else self.players[0]
        )
