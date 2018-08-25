from itertools import combinations
from Deckdata import deck


class PointCounter:
    def __init__(self, choice, extra):
        self.choice1 = choice
        try:
            self.choice = choice + deck.Extra
        except TypeError:
            self.choice = choice + tuple(deck.Extra)
        self.pairs = {0: 0, 4: 2, 8: 4, 9: 6, 13: 8, 16: 12}
        if extra:
            self.hand_nums = [min(10, deck.numbers.index(card.num) + 1) for card in self.choice]
            self.hand_real_nums = [deck.numbers.index(card.num) + 1 for card in self.choice]
            self.hand_suits = [card.suit for card in self.choice]
        else:
            self.hand_nums = [min(10, deck.numbers.index(card.num) + 1) for card in choice]
            self.hand_real_nums = [deck.numbers.index(card.num) + 1 for card in choice]
            self.hand_suits = [card.suit for card in choice]

    def calculation(self):
        points = 0

        #  runs
        y = 0
        for num in self.hand_real_nums:
            if self.hand_real_nums.count(num) > 1:
                y += self.hand_real_nums.count(num)
        points += self.pairs[y]

        #  15's
        for i in range(2, 6):
            for subset in combinations(self.hand_nums, i):
                if sum(subset) == 15:
                    points += 2

        #  flushes
        if self.hand_suits.count(self.choice[0].suit) == 4 and self.hand_suits.count(self.choice[4].suit) != 4:
            points += 4
        elif self.hand_suits.count(self.choice[0].suit) == 5:
            points += 5
        else:
            pass

        #  runs
        sett = [0, 0, 0]
        for i in range(3, 6):
            for combo in combinations(sorted(self.hand_real_nums), i):
                valid = []
                for num in range(1, len(combo)):
                    prev = combo[num - 1]
                    if prev + 1 == combo[num]:
                        valid.append(num)
                        if len(valid) == len(combo) - 1:
                            sett[len(combo) - 3] += len(combo)
                    else:
                        break
        sett.reverse()
        for i in sett:
            if i != 0:
                points += i
                break

        #  knobs
        for card in self.choice1:
            if deck.Extra[0].suit == card.suit and deck.numbers.index(card.num) == 10:
                print('knobs')
                print(card)
                points += 1

        return points

    def extra_less(self):
        points = 0

        #  pairs
        y = 0
        for num in self.hand_real_nums:
            if self.hand_real_nums.count(num) > 1:
                y += self.hand_real_nums.count(num)
        points += self.pairs[y]

        #  15's
        for i in range(2, 6):
            for combo in combinations(self.hand_nums, i):
                if sum(combo) == 15:
                    points += 2

        #  flushes
        if self.hand_suits.count(self.choice[0].suit) == 4:
            points += 4

        #  runs
        sett = [0, 0, 0]
        for i in range(3, 6):
            for combo in combinations(sorted(self.hand_real_nums), i):
                valid = []
                for num in range(1, len(combo)):
                    prev = combo[num - 1]
                    if prev + 1 == combo[num]:
                        valid.append(num)
                        if len(valid) == len(combo) - 1:
                            sett[len(combo) - 3] += len(combo)
                    else:
                        break
        sett.reverse()
        for i in sett:
            if i != 0:
                points += i
                break

        return points

    def crib(self):
        points = 0
        y = 0

        for num in self.hand_real_nums:
            if self.hand_real_nums.count(num) > 1:
                y += self.hand_real_nums.count(num)
        points += self.pairs[y]

        for i in range(2, 6):
            for subset in combinations(self.hand_nums, i):
                if sum(subset) == 15:
                    points += 2

        if self.hand_suits.count(self.choice[0].suit) == 5:
            points += 5

        sett = [0, 0, 0]
        for i in range(3, 6):
            for combo in combinations(sorted(self.hand_real_nums), i):
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
                points += i
                break

        for i in self.choice1:
            if deck.Extra[0].suit == i.suit and deck.numbers.index(i.num) == 10:
                points += 1

        return points

