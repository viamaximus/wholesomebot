import random

class Dice:
    def __init__(self, num_dice, num_sides):
        if num_sides < 1 or num_dice < 1: 
            raise ValueError("Number of sides must be at least 1.")
        self.sides = num_sides
        self.dice = num_dice

    def roll(self, sum_results=False):
        #rolls the dice and returns the result or sum
        results = [random.randint(1, self.sides) for _ in range(self.dice)]
        if sum_results:
            return sum(results)
        return results