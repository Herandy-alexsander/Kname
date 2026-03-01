class Stack:
    def __init__(self):
        self.items = []

    def push(self, effect):
        self.items.append(effect)

    def resolve(self):
        while self.items:
            effect = self.items.pop()
            effect.resolve()
