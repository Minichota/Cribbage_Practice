from Tands import Deck, Hands
import itertools

Deck = Deck()
Hand = Hands()


class Point_Counter:
    def __init__(self):
        self.handnums = []
        self.handrealnums = []
        self.handsuits = []
        self.y = 0

    def calculation(self, Choice, Extra):
        self.choice = Choice+Extra
        self.p1points = 0
        for card in self.choice:
            self.value = Deck.numbers.index(card.num) + 1
            self.value2 = Deck.numbers.index(card.num) + 1
            if self.value > 10:
                self.value = 10
            self.handnums.append(self.value)
            self.handsuits.append(card.suit)
            self.handrealnums.append(self.value2)


        for num in self.handrealnums:
            if self.handrealnums.count(num) > 1:
                self.y += self.handrealnums.count(num)
        if self.y == 4:
            self.p1points += 2
        elif self.y == 8:
            self.p1points += 4
        elif self.y == 9:
            self.p1points += 6
        elif self.y == 13:
            self.p1points += 8
        elif self.y == 16:
            self.p1points += 12
        self.y = 0
        for i in range(2, 6):
            for subset in itertools.combinations(self.handnums, i):
                if sum(subset) == 15:
                    self.p1points += 2

        if self.handsuits.count(self.choice[0].suit) == 4 and self.handsuits.count(self.choice[4].suit) != 4:
            self.p1points += 4
        elif self.handsuits.count(self.choice[0].suit) == 5:
            self.p1points += 5
        else:
             pass

        self.ll = []
        for i in sorted(self.handrealnums):
            if i+1 in sorted(self.handrealnums) or (i-1 in sorted(self.handrealnums)):
                self.ll.append(i)
        if len(self.ll) >= 2 and self.ll[-1] - self.ll[0] > 1 and self.ll[-1] - self.ll[0] < len(self.ll):
            self.p1points += (len(set(self.ll)) * (len(self.ll) - len(set(self.ll)) + 1))

        self.newnums = []
        for i in Choice:
            self.newnums.append(i)
        for i in self.newnums:
            if Extra[0].suit == i.suit and Deck.numbers.index(i.num) == 10:
                self.p1points += 1
                print('knobs')
        self.__init__()


    def calculation2(self, Choice, Extra):
        self.choice = Choice+Extra
        self.p2points = 0
        for card in self.choice:
            self.value = Deck.numbers.index(card.num) + 1
            self.value2 = Deck.numbers.index(card.num) + 1
            if self.value > 10:
                self.value = 10
            self.handnums.append(self.value)
            self.handsuits.append(card.suit)
            self.handrealnums.append(self.value2)


        for num in self.handrealnums:
            if self.handrealnums.count(num) > 1:
                self.y += self.handrealnums.count(num)
        if self.y == 4:
            self.p2points += 2
        elif self.y == 8:
            self.p2points += 4
        elif self.y == 9:
            self.p2points += 6
        elif self.y == 13:
            self.p2points += 8
        elif self.y == 16:
            self.p2points += 12
        self.y = 0


        for i in range(2, 6):
            for subset in itertools.combinations(self.handnums, i):
                if sum(subset) == 15:
                    self.p2points += 2


        if self.handsuits.count(self.choice[0].suit) == 4 and self.handsuits.count(self.choice[4].suit) != 4:
            self.p2points += 4
        elif self.handsuits.count(self.choice[0].suit) == 5:
            self.p2points += 5
        else:
             pass


        self.ll = []
        for i in sorted(self.handrealnums):
            if i+1 in sorted(self.handrealnums) or (i-1 in sorted(self.handrealnums)):
                self.ll.append(i)
        if len(self.ll) >= 2 and self.ll[-1] - self.ll[0] > 1 and self.ll[-1] - self.ll[0] < len(self.ll):
            self.p2points += (len(set(self.ll)) * (len(self.ll) - len(set(self.ll)) + 1))
        self.newnums = []
        for i in Choice:
            self.newnums.append(i)
        for i in self.newnums:
            if Extra[0].suit == i.suit and Deck.numbers.index(i.num) == 10:
                self.p2points += 1
                print('knobs')
        self.__init__()

    def get_var1(self):
        return(self.p1points)

    def get_var2(self):
        return(self.p2points)