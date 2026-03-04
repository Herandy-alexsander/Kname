# domain/entities/troop.py

class Troop(Card):
    def __init__(self, id, name, cost, power, toughness, effects=None, image_path=None):
        super().__init__(id, name, "tropa", cost, power, toughness, effects, image_path)
        self.damage_taken = 0  # DANO TEMPORÁRIO

    @property
    def current_toughness(self):
        return self.base_toughness - self.damage_taken
    
    def take_damage(self, amount):
        self.damage_taken += amount

    def is_dead(self):
        return self.damage_taken >= self.toughness

    def reset_damage(self):
        self.damage_taken = 0
