import random
class Dice:
    @staticmethod
    def roll(num_dice=1, num_sides=1, sum_results=True):
        #roll a specified number of dice with a specified number of sides
        results = [random.randint(1, num_sides) for _ in range(num_dice)]
        return sum(results) if sum_results else results
    