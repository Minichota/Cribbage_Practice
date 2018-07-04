from Tands import Hands, Deck, update_hands, Card
from itertools import groupby
import operator
Deck, Hand = update_hands()
Hand = Hands()
class player1hand:
    def __init__(self):
        self.discarded_cards = []
        self.pointsearned = 0

    def playcard1(self, card):
        self.discarded_cards.append(card)
        game.cardsplayed.append(card)
class player2hand:
    def __init__(self):
        self.discarded_cards = []
        self.pointsearned = 0

    def playcard2(self, card):
        self.discarded_cards.append(card)
        game.cardsplayed.append(card)

player1 = player1hand()
player2 = player2hand()

class Game:
    def __init__(self):
        self.currentvalue = 0
        self.cardsplayed = []

    def player1(self, selection):
        player1.playcard1(selection)
        score = score_points()
        score.basic(player1, player2, selection)

    def player2(self, selection):
        player2.playcard2(selection)
        score = score_points()
        score.basic(player2, player1, selection)

class score_points:
    game = Game()
    currentcards = []
    allcards = game.cardsplayed
    def basic(self, player, otherplayer, selection):
        value = Deck.numbers.index(selection.num)+1
        if value > 10:
            value = 10
        if game.currentvalue + value <= 31:
            game.currentvalue += value

            if game.currentvalue == 15:
                player.pointsearned += 2

            elif game.currentvalue == 31:
                player.pointsearned += 2
                game.currentvalue = 0
                self.currentcards = []

        else:
            game.currentvalue = 0
            self.currentcards = []
            otherplayer.pointsearned += 1
            game.currentvalue += value

        self.currentcards.append(selection)
        self.allcards.append(selection)

        self.runs(player)

    def pairs(self, player):
        if len(self.currentcards) > 2:
            if self.currentcards[-1].num == self.currentcards[-2].num == self.currentcards[-3].num == self.currentcards[-4]:
                player.pointsearned += 12
            else:
                if self.currentcards[-1].num == self.currentcards[-2].num == self.currentcards[-3].num:
                    player.pointsearned += 6
                elif len(self.currentcards) > 1:
                    if self.currentcards[-1].num == self.currentcards[-2].num:
                        player.pointsearned += 2
        self.flushes(player)

    def flushes(self, player):
        self.newlist = []
        for i in self.currentcards:
            self.newlist.append(i.suit)
        self.count = 0
        for i in range(4, len(self.newlist) + 1):
            size = len(set(self.newlist[-i:]))
            if size != 1:
                break
            self.count = i
        if self.count >= 4:
            player.pointsearned += self.count
        self.runs(player)

    def runs(self, player):
        self.nums = []
        for card in self.currentcards:
            self.value = Deck.numbers.index(card.num)+1
            self.nums.append(self.value)
        if len(self.currentcards) > 2:
            try:
                player.pointsearned += self.calculation(self.nums)
            except TypeError:
                pass
    def calculation(self, list):
        self.lengths = 0
        self.Bool = False
        for j in range(1, len(list) - 1):
            self.Bool = False
            self.newlist = sorted(list[-len(list) + j - 1:])
            for i in range(len(list) - j, 0, -1):
                if self.newlist[i - len(self.newlist)] - self.newlist[i - len(self.newlist) - 1] == 1:
                    self.Bool = True
                else:
                    self.Bool = False
                    break
            if self.Bool:
                return len(list) - j + 1
                break
game = Game()
# if __name__ == '__main__':
#     player1hand()
#     player2hand()
#     game = Game()
#     score = score_points(game.cardsplayed)
#     for i in range(4):
#         game.player1(Hand.p2hand[i])
#         print(game.currentvalue)
#         game.player2(Hand.p2hand[i])
#         print(game.currentvalue)
#     print(player1.pointsearned, player2.pointsearned)
