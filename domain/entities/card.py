class Card:
	
	self.current_toughness
	
	
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
        self.cost = cost
        self.power = power
        self.toughness = toughness
        self.effects = effects or []
        self.image_path = image_path

    def __repr__(self):
        return f"<Card {self.name} ({self.card_type})>"
        
    def take_damage(self, amount):
    self.current_toughness -= amount
        
        
