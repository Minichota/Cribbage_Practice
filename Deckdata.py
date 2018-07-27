import random


class Card:
    def __init__(self, num, suit):
        self.num = num
        self.suit = suit
        self.path = self.num.lower() + '_of_' + suit.lower() + '.png'

    def __repr__(self):
        return (self.num + " of " + self.suit)

    def find(self, card):
        print(deck.deck.index(card))


class Deck:
    def __init__(self):
        self.suits = ['Diamonds', 'Clubs', 'Spades', 'Hearts']
        self.numbers = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen',
                        'King']
        self.deck = []
        for suit in self.suits:
            for number in self.numbers:
                self.deck.append(Card(number, suit))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)


class Hands:
    def build(self):
        self.p1hand = [deck.deck[0], deck.deck[2], deck.deck[4], deck.deck[6], deck.deck[8], deck.deck[10]]
        self.p2hand = [deck.deck[1], deck.deck[3], deck.deck[5], deck.deck[7], deck.deck[9], deck.deck[11]]
        self.Extra = [deck.deck[12]]


class Handscore:
    def __init__(self):
        self.p1score = 0
        self.p2score = 0

    def update(self, p1scored, p2scored):
        self.p1score += p1scored
        self.p2score += p2scored
        return p1scored, p2scored

    def get_var1(self):
        return self.p1score

    def get_var2(self):
        return self.p2score

    def reset(self):
        self.__init__()


deck = Deck()
hand = Hands()
handscores = Handscore()
