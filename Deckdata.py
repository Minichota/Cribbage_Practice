import random


class Card:
    def __init__(self, num, suit):
        self.num = num
        self.suit = suit
        self.path = self.num.lower() + '_of_' + suit.lower() + '.png'

    def __repr__(self):
        return self.num + " of " + self.suit


class Deck:
    def __init__(self):
        self.suits = ['Diamonds', 'Clubs', 'Spades', 'Hearts']
        self.numbers = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        self.deck = []
        for suit in self.suits:
            for number in self.numbers:
                self.deck.append(Card(number, suit))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)
        self.Extra = [self.deck[12]]


class Scoring:
    def __init__(self, p1score, p2score):
        self.p1score = p1score
        self.p2score = p2score

    def update(self, p1scored, p2scored, *args):
        self.p1score += p1scored
        self.p2score += p2scored

        if len(args) > 0:
            if args[1] == 'player1':
                self.p1score += args[0]
            if args[1] == 'player2':
                self.p2score += args[0]

    def reset(self):
        self.__init__(0, 0)


class Crib:
    def __init__(self, owner, crib):
        self.points = 0
        self.owner = owner
        self.crib = crib

    def score(self):
        from Points import PointCounter
        pointer = PointCounter(self.crib)
        self.points += pointer.crib()


deck = Deck()
