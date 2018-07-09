from Tands import Hands, Deck, update_hands, Card
from itertools import groupby
import operator
Deck, Hand = update_hands()
Hand = Hands()
class player1hand:
    def __init__(self):
        self.name = 'player1'
        self.discarded_cards = []
        self.pointsearned = 0

    def playcard1(self, card):
        self.discarded_cards.append(card)
        score.cardsplayed.append(card)
        score.basic(player1, player2, card)

class player2hand:
    def __init__(self):
        self.name = 'player2'
        self.discarded_cards = []
        self.pointsearned = 0

    def playcard2(self, card):
        self.discarded_cards.append(card)
        score.cardsplayed.append(card)
        score.basic(player2, player1, card)

player1 = player1hand()
player2 = player2hand()


class score_points:
    def __init__(self):
        self.cardsplayed = []
        self.currentcards = []
        self.pips = []
        self.currentvalue = 0

    def basic(self, player, otherplayer, selection):
        value = Deck.numbers.index(selection.num)+1
        if value > 10:
            value = 10
        if self.currentvalue + value <= 31:
            self.currentvalue += value

            if self.currentvalue == 15:
                player.pointsearned += 2
                self.pips.append.append(str(player.name) + ' scored a 15!')
            if self.currentvalue == 31:
                player.pointsearned += 2
                self.currentvalue = 0
                self.currentcards = []
                self.pips.append(str(player.name) + ' scored a 31!')
        else:
            self.currentvalue = 0
            self.currentcards = []
            otherplayer.pointsearned += 1
            self.currentvalue += value
            self.pips.append(str(otherplayer.name) + " got go'd")
        self.currentcards.append(selection)
        if len(self.cardsplayed) == 8:
            player.pointsearned += 1
            self.pips.append(str(player.name)+' played the last card')
        self.pairs(player)

    def pairs(self, player):
        self.mybool = True
        if len(self.currentcards) > 1:
            try:
                if self.currentcards[-1].num == self.currentcards[-2].num == self.currentcards[-3].num == self.currentcards[-4]:
                    player.pointsearned += 12
                    self.pips.append(str(player.name) + ' got a pair of 4!')
                    self.mybool = False
            except IndexError:
                pass
            if self.mybool == True:
                try:
                    if self.currentcards[-1].num == self.currentcards[-2].num == self.currentcards[-3].num:
                        self.pips.append(str(player.name) + ' got a pair of 3!')
                        player.pointsearned += 6
                        self.mybool = False
                except IndexError:
                    pass
            if self.mybool == True:
                if self.currentcards[-1].num == self.currentcards[-2].num:
                        player.pointsearned += 2
                        self.pips.append(str(player.name) + ' scored a pair of 2!')
                        self.mybool = False
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
            self.pips.append(str(player.name) + ' scored a flush')
        self.runs(player)

    def runs(self, player):
        self.nums = []
        for card in self.currentcards:
            self.value = Deck.numbers.index(card.num)+1
            self.nums.append(self.value)
        if len(self.currentcards) > 2:
            try:
                player.pointsearned += self.calculation(self.nums)
                self.pips.append(str(player.name) + ' scored a run of ' + str(self.calculation(self.nums)))
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


score = score_points()
# if __name__ == '__main__':
#     player1hand()
#     player2hand()
#     for i in range(4):
#         print('p1:' + str(Hand.p1hand[i]))
#         game.player1(Hand.p1hand[i])
#         print(self.currentvalue)
#         print('p2:' + str(Hand.p2hand[i]))
#         game.player2(Hand.p2hand[i])
#         print(self.currentvalue)
#     print(player1.pointsearned, player2.pointsearned)
#     print(score.pips)