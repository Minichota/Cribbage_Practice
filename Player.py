from Gameplay import ScorePoints
from Deckdata import deck
from itertools import combinations
from Points import PointCounter
from copy import deepcopy
players = []


class Player:
    def __init__(self, name):
        self.name = name
        self.points_earned = 0

    def play_card(self, card, turn, obj):
        obj.cards_played.append(card)
        if turn == 'player1':
            obj.basic(player1, player2, card)
        else:
            obj.basic(player2, player1, card)

    def build(self, x):
        if x == '1':
            self.hand = [deck.deck[0], deck.deck[2], deck.deck[4], deck.deck[6], deck.deck[8], deck.deck[10]]
        if x == '2':
            self.hand = [deck.deck[1], deck.deck[3], deck.deck[5], deck.deck[7], deck.deck[9], deck.deck[11]]

    def best_hand(self):
        points = {}
        best = 0
        for i in combinations(self.hand, 4):
            point = PointCounter(i, False)
            points.update({point.extra_less(): i})
        for i in points.keys():
            if i > best:
                best = i
        return points[best]

    def best_play(self, played, choice):
        choices = {}
        tester = ScorePoints()
        players_leftovers = [x for x in choice if x not in played]

        for i in range(len(played)):
            player1.build('1')
            player2.build('2')
            if i % 2 == 0:
                self.play_card(played[i], self.name, tester)
            else:
                player1.play_card(played[i], 'player1', tester)
        clear_players()

        for i in range(len(players_leftovers)):
            clone = deepcopy(tester)
            self.play_card(players_leftovers[i], self.name, clone)
            choices.update({self.points_earned: players_leftovers[i]})
            clear_players()

        return choices[max(choices.keys())]


def clear_players():
    for i in players:
        i.__init__(i.name)


player1 = Player('You')
players.append(player1)
player2 = Player('Your enemy')
players.append(player2)

# if __name__ == '__main__':
#     player1.build('1')
#     player2.build('2')
#     played = []
#     for i in range(3):
#         played.append(player1.hand[i])
#         played.append(player2.hand[i])
#     print(played)
#     print(player1.best_play(played))
#     clearplayers()
