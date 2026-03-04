# presentation/cli_interface.py

class CLIInterface:

    # ==============================
    # UTILITÁRIOS
    # ==============================

    def show_message(self, message):
        print(message)

    def handle_mulligan(self, player):
        while True:
            choice = input(f"{player.name}, deseja mulligan? (s/n): ")
            if choice.lower() == "s":
                player.mulligan()
            elif choice.lower() == "n":
                break
            else:
                print("Opção inválida.")

    # ==============================
    # FASE PRINCIPAL
    # ==============================

    def handle_main_phase(self, game):

        player = game.current_player

        while True:
            print("\n===== FASE PRINCIPAL =====")
            print(f"Recursos disponíveis: {player.resources}")
            print("1 - Jogar carta")
            print("2 - Gerar recurso")
            print("3 - Encerrar fase")

            choice = input("Escolha uma opção: ")

            if choice == "1":
                self.play_card(game)

            elif choice == "2":
                self.generate_resource(game)

            elif choice == "3":
                break

            else:
                print("Opção inválida.")

    # ==============================
    # JOGAR CARTA
    # ==============================

    def play_card(self, game):

        player = game.current_player

        if not player.hand:
            print("Você não tem cartas na mão.")
            return

        print("\nCartas na mão:")
        for i, card in enumerate(player.hand):
            print(f"{i} - {card.name} (Custo: {card.cost})")

        choice = input("Escolha o número da carta ou X para cancelar: ")

        if choice.lower() == "x":
            return

        if not choice.isdigit():
            print("Entrada inválida.")
            return

        index = int(choice)

        if index < 0 or index >= len(player.hand):
            print("Carta inválida.")
            return

        card = player.hand[index]

        if player.resources < card.cost:
            print("Recursos insuficientes.")
            return

        # Pagar custo
        player.resources -= card.cost

        # Mover carta
        player.hand.remove(card)
        player.battlefield.append(card)

        print(f"{card.name} entrou em campo!")

        # Executar habilidade ETB se existir
        if hasattr(card, "on_enter"):
            card.on_enter(game)

    # ==============================
    # GERAR RECURSO
    # ==============================

    def generate_resource(self, game):

        player = game.current_player

        if not player.discard_pile:
            print("Não há cartas no descarte.")
            return

        card = player.discard_pile.pop()
        player.deck.append(card)
        player.resources += 1

        print("Recurso gerado com sucesso!")

    # ==============================
    # DESCARTE (LIMITE DE MÃO)
    # ==============================

    def choose_card_to_discard(self, player):

        print("\nVocê precisa descartar até ficar com 5 cartas.")

        for i, card in enumerate(player.hand):
            print(f"{i} - {card.name}")

        while True:
            choice = input("Escolha o número da carta para descartar: ")

            if choice.isdigit():
                index = int(choice)

                if 0 <= index < len(player.hand):
                    return player.hand[index]

            print("Escolha inválida.")

    # ==============================
    # COMBATE
    # ==============================

    def choose_attacker(self, player):

        available = [
            card for card in player.battlefield
            if card.type == "TROPA" and not getattr(card, "has_attacked", False)
        ]

        if not available:
            print("Nenhuma tropa disponível para atacar.")
            return None

        print("\nTropas disponíveis para atacar:")

        for i, troop in enumerate(available):
            print(f"{i} - {troop.name} ({troop.power}/{troop.current_toughness})")

        print("X - Encerrar combate")
        choice = input("> ")

        if choice.lower() == "x":
            return None

        if choice.isdigit():
            i = int(choice)
            if 0 <= i < len(available):
                return available[i]

        print("Escolha inválida.")
        return None

    def choose_blockers(self, defender, attacking_troop):

        available = [
            card for card in defender.battlefield
            if card.type == "TROPA"
        ]

        if not available:
            print("Sem bloqueadores disponíveis.")
            return []

        print(f"\nEscolha bloqueadores para {attacking_troop.name}:")

        for i, troop in enumerate(available):
            print(f"{i} - {troop.name} ({troop.power}/{troop.current_toughness})")

        print("Digite índices separados por vírgula ou X para não bloquear")
        choice = input("> ")

        if choice.lower() == "x":
            return []

        indices = choice.split(",")

        blockers = []
        for idx in indices:
            if idx.strip().isdigit():
                i = int(idx.strip())
                if 0 <= i < len(available):
                    blockers.append(available[i])

        return blockers
