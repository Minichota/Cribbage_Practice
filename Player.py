from Gameplay import score
from Deckdata import deck


class Player:
    players = []

    def __init__(self, name):
        self.players.append(name)
        self.name = name
        self.pointsearned = 0

    def play_card(self, card, turn):
        score.cardsplayed.append(card)
        if turn == 'player1':
            score.basic(player1, player2, card)
        else:
            score.basic(player2, player1, card)

    def build(self, x):
        if x == '1':
            self.hand = [deck.deck[0], deck.deck[2], deck.deck[4], deck.deck[6], deck.deck[8], deck.deck[10]]
        if x == '2':
            self.hand = [deck.deck[1], deck.deck[3], deck.deck[5], deck.deck[7], deck.deck[9], deck.deck[11]]


def clearplayers():
    for i in Player.players:
        i.__init__()


player1 = Player('player1')
Player.players.append('player1')
player2 = Player('player2')
Player.players.append('player2')
