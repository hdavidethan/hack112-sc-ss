from constants import Constants
import random

class Problem:
    def __init__(self, x, y, direction, type):
        self.x = x
        self.y = y
        self.direction = direction
        self.type = type
    
    def __repr__(self):
        return f'({self.x}, {self.y})'

    @staticmethod
    def randomProblem(year):
        problems = Constants.problems
        
        year -= 1
        year = min(year, len(problems))

        probset = problems[year]
        idx = random.randrange(0, len(probset) - 1)

        return probset[idx]

