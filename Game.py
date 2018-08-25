class Game:
    def __init__(self, turn, other_turn):
        self.turn = turn
        self.other_turn = other_turn

    def switch(self):
        self.turn, self.other_turn = self.other_turn, self.turn

    def serialize(self):
        return {
            'turn': self.turn,
            'other_turn': self.other_turn
        }
