from Deckdata import deck


class ScorePoints:
    def __init__(self):
        self.cards_played = []
        self.current_cards = []
        self.pips = []
        self.current_value = 0

    def basic(self, player, other_player, selection):
        self.resetter = False
        value = deck.numbers.index(selection.num)+1
        if value > 10:
            value = 10
        if self.current_value + value <= 31:
            self.current_value += value
            self.current_cards.append(selection)
            if self.current_value == 15:
                player.points_earned += 2
                self.pips.append(str(player.name) + ' scored a 15!')
            if self.current_value == 31:
                player.points_earned += 2
                self.resetter = True
        else:
            self.current_value = 0
            self.current_cards = []
            other_player.points_earned += 1
            self.current_cards.append(selection)
            self.current_value += value
            self.pips.append(str(other_player.name) + " got go'd")
        self.pairs(player)

    def pairs(self, player):
        my_bool = True
        if len(self.current_cards) > 1:
            try:
                if self.current_cards[-1].num == self.current_cards[-2].num == \
                        self.current_cards[-3].num == self.current_cards[-4]:
                    player.points_earned += 12
                    self.pips.append(str(player.name) + ' got a pair of 4!')
                    my_bool = False
            except IndexError:
                pass
            if my_bool:
                try:
                    if self.current_cards[-1].num == self.current_cards[-2].num == self.current_cards[-3].num:
                        self.pips.append(str(player.name) + ' got a pair of 3!')
                        player.points_earned += 6
                        my_bool = False
                except IndexError:
                    pass
            if my_bool:
                if self.current_cards[-1].num == self.current_cards[-2].num:
                    player.points_earned += 2
                    self.pips.append(str(player.name) + ' scored a pair of 2!')
        self.runs(player)

    def runs(self, player):
        nums = []
        for card in self.current_cards:
            value = deck.numbers.index(card.num) + 1
            nums.append(value)
        if len(nums) > 2:
            try:
                player.points_earned += self.calculation(nums)
                self.pips.append(str(player.name) + ' scored a run of ' + str(self.calculation(nums)))
            except TypeError:
                pass
        self.end(player)

    def calculation(self, nums):
        for j in range(1, len(nums) - 1):
            done = False
            new = sorted(nums[-len(nums) + j - 1:])
            for i in range(len(nums) - j, 0, -1):
                if new[i - len(new)] - new[i - len(new) - 1] == 1:
                    done = True
                else:
                    done = False
                    break
            if done:
                return len(nums) - j + 1

    def end(self, player):
        if self.resetter:
            self.current_value = 0
            self.current_cards = []
            self.pips.append(str(player.name) + ' scored a 31!')

        if len(self.cards_played) == 8:
            player.points_earned += 1
            self.pips.append(str(player.name) + ' played the last card')

    def reset(self):
        self.__init__()


gameplay = ScorePoints()
