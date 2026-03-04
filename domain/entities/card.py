class Card:

    def __init__(
        self,
        id,
        name,
        card_type,
        cost,
        power=0,
        toughness=0,
        effects=None,
        image_path=None
    ):
        self.id = id
        self.name = name
        self.card_type = card_type
        self.type = card_type
        self.cost = cost
        self.power = power
        self.toughness = toughness
        self.current_toughness = toughness

        self.effects = effects or []
        self.image_path = image_path

        self.owner = None
        self.has_attacked = False

    def __repr__(self):
        return f"<Card {self.name} ({self.card_type})>"

    # ======================
    # COMBATE
    # ======================

    def take_damage(self, amount):
        self.current_toughness -= amount

    def is_dead(self):
        return self.current_toughness <= 0

    # ======================
    # RESET DE TURNO
    # ======================

    def reset_turn(self):
        self.has_attacked = False
        self.current_toughness = self.toughness
