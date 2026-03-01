import random


class Player:
    def __init__(self, name, deck):
        self.name = name
        self.life = 12

        # Zonas
        self.deck = deck[:]  # copia do deck
        self.hand = []
        self.battlefield = []
        self.discard_pile = []
        self.limbo = []

        # Recursos permanentes
        self.resources = 0

        self.shuffle_deck()

    # ------------------------
    # Funções básicas
    # ------------------------

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def draw(self):
        if len(self.deck) == 0:
            print(f"{self.name} não pode comprar, deck vazio!")
            return None

        card = self.deck.pop(0)
        self.hand.append(card)
        return card

    def draw_starting_hand(self):
        for _ in range(5):
            self.draw()

    def mulligan(self):
        self.deck.extend(self.hand)
        self.hand.clear()
        self.shuffle_deck()
        self.draw_starting_hand()

    # ------------------------
    # Sistema de Recurso
    # ------------------------

    def generate_resource(self):
        if len(self.discard_pile) == 0:
            print("Não há cartas no descarte para gerar recurso.")
            return False

        card = self.discard_pile.pop()  # topo do descarte
        self.deck.append(card)          # vai para o fundo do deck
        self.resources += 1

        print(f"{self.name} gerou 1 recurso permanente! Total: {self.resources}")
        return True

    # ------------------------
    # Movimento entre zonas
    # ------------------------

    def move_to_discard(self, card):
        """
        Move carta da mão ou campo para o descarte.
        """
        if card in self.hand:
            self.hand.remove(card)
        elif card in self.battlefield:
            self.battlefield.remove(card)

        self.discard_pile.append(card)

    def move_to_limbo(self, card):
        """
        Move carta para zona de limbo.
        """
        if card in self.hand:
            self.hand.remove(card)
        elif card in self.battlefield:
            self.battlefield.remove(card)
        elif card in self.discard_pile:
            self.discard_pile.remove(card)

        self.limbo.append(card)

    # ------------------------
    # Jogar carta
    # ------------------------

    def play_card(self, card):
        if card not in self.hand:
            print("Carta não está na mão.")
            return False

        if card.cost > self.resources:
            print("Recursos insuficientes.")
            return False

        self.resources -= card.cost
        self.hand.remove(card)

        # Define dono da carta
        card.owner = self

        # Se for tropa ou item vai pro campo
        if card.type in ["TROPA", "ITEM"]:
            self.battlefield.append(card)
        else:
            # Reações podem ir direto para descarte após uso
            self.discard_pile.append(card)

        print(f"{self.name} jogou {card.name}")
        return True

    # ------------------------
    # Dano ao jogador
    # ------------------------

    def take_damage(self, amount):
        self.life -= amount
        print(f"{self.name} recebeu {amount} de dano. Vida atual: {self.life}")

    def is_dead(self):
        return self.life <= 0

    # ------------------------
    # Verificação de mortes no campo
    # ------------------------

    def check_dead_troops(self):
        """
        Verifica tropas destruídas e envia ao descarte.
        """
        dead_cards = [card for card in self.battlefield
                      if card.type == "TROPA" and card.is_dead()]

        for card in dead_cards:
            print(f"{card.name} foi destruída!")
            self.battlefield.remove(card)
            self.discard_pile.append(card)

    # ------------------------
    # Início de turno
    # ------------------------

    def start_turn(self):
        """
        Reseta estados de turno.
        """
        for card in self.battlefield:
            card.reset_turn()
