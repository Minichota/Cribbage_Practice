from itertools import combinations
from Deckdata import deck

class Point_Counter:
    def __init__(self):
        self.y = 0
        self.p1points = 0
        self.p2points = 0
        self.pairs = {0: 0, 4: 2, 8: 4, 9: 6, 13: 8, 16: 12}

    def calculation(self, Choice, Extra, player):
        self.choice = Choice+Extra
        self.handnums = []
        self.handrealnums = []
        self.handsuits = []
        self.points = 0

        for card in self.choice:
            self.value = deck.numbers.index(card.num) + 1
            self.value2 = deck.numbers.index(card.num) + 1
            if self.value > 10:
                self.value = 10
            self.handnums.append(self.value)
            self.handsuits.append(card.suit)
            self.handrealnums.append(self.value2)

        for num in self.handrealnums:
            if self.handrealnums.count(num) > 1:
                self.y += self.handrealnums.count(num)
        self.points += self.pairs[self.y]
        self.y = 0

        for i in range(2, 6):
            for subset in combinations(self.handnums, i):
                if sum(subset) == 15:
                    self.points += 2

        if self.handsuits.count(self.choice[0].suit) == 4 and self.handsuits.count(self.choice[4].suit) != 4:
            self.points += 4
        elif self.handsuits.count(self.choice[0].suit) == 5:
            self.points += 5
        else:
             pass
        sett = [0, 0, 0]
        for i in range(3, 6):
            for combo in combinations(sorted(self.handrealnums), i):
                ll = []
                for num in range(1, len(combo)):
                    prev = combo[num - 1]
                    if prev + 1 == combo[num]:
                        ll.append(num)
                        if len(ll) == len(combo) - 1:
                            sett[len(combo) - 3] += len(combo)
                    else:
                        break
        sett.reverse()
        for i in sett:
            if i != 0:
                self.points += i
                break

        self.newnums = []
        for i in Choice:
            self.newnums.append(i)
        for i in self.newnums:
            if Extra[0].suit == i.suit and deck.numbers.index(i.num) == 10:
                self.points += 1
        if player == 'p1':
            self.p1points += self.points
        elif player == 'p2':
            self.p2points += self.points


    def get_var1(self):
        return self.p1points

    def get_var2(self):
        return self.p2points

point = Point_Counter()