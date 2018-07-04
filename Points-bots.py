from typing import List
import Hands
import itertools

Deck = Hands.Deck()


class Point_Counter:
    def __init__(self, playerhand):
        self.p1hand = playerhand
        self.ll: List[int] = []
        self.p1handnums = []
        self.p1handrealnums = []
        self.p2handnums = []
        self.p2handrealnums = []
        self.p1handsuits = []
        self.p2handsuits = []
        self.combinations = []
        self.combinationsofrealnumbers = []
        self.combinationsofsuits = []
        self.points_of_combination = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.x = 0
        self.y = 0
        self.z = 0
        self.a = 0
        self.b = 0
        self.get_variables(self.p1hand)

    def get_variables(self, playerhand):
        for card in playerhand:
            self.value = Deck.numbers.index(card.num)+1
            self.value2 = Deck.numbers.index(card.num)+1
            if self.value > 10:
                self.value = 10
            self.p1handnums.append(self.value)
            self.p1handsuits.append(card.suit)
            self.p1handrealnums.append(self.value2)
        for subset in itertools.combinations(self.p1handnums, 4):
            self.combinations.append(subset)
        for subset in itertools.combinations(self.p1handrealnums, 4):
            self.combinationsofrealnumbers.append(subset)
        for subset in itertools.combinations(self.p1handsuits, 4):
            self.combinationsofsuits.append(subset)
        self.calculation()
    def calculation(self):
        for tuple in self.combinationsofrealnumbers:
            for number in tuple:
                if tuple.count(number) > 1:
                    self.y += 1
            if self.y == 2:
                self.points_of_combination[self.z] += 2
            if self.y == 3:
                self.points_of_combination[self.z] += 6
            if self.y == 4:
                self.points_of_combination[self.z] += 4
            self.y = 0
            self.z += 1

        for tuple in self.combinations:
            for i in range(1, len(tuple) + 1):
                for subset in itertools.combinations(tuple, i):
                    if sum(subset) == 15:
                        self.points_of_combination[self.x] += 2
            self.x += 1

        for tuple in self.combinationsofsuits:
            if tuple.count(tuple[0]) == 4:
                self.points_of_combination[self.a] += 4
            self.a += 1

        for combo in self.combinationsofrealnumbers:
            ll = []
            for i in sorted(combo):
                if i + 1 in sorted(combo) or (i - 1 in combo):
                    ll.append(i + 1)
            if len(ll) >= 2 and ll[len(ll) - 1] - ll[0] > 1 and ll[len(ll) - 1] - ll[0] < len(ll):
                self.points_of_combination[self.b] + (len(set(ll)) * (len(ll) - len(set(ll)) + 1))
            self.b += 1
        print(self.points_of_combination)