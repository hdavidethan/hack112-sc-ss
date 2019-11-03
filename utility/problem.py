from constants import Constants
import random

class Problem:
    def __init__(self, x, y, direction, problem):
        self.x = x
        self.y = y
        self.direction = direction
        self.problem = problem
    
    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __hash__(self):
        return hash((self.x, self.y, self.direction))

    def __eq__(self, other):
        return isinstance(other, Problem) and hash(self) == hash(other)

    def draw(self, mode, canvas):
        img = mode.app.assets[self.problem]
        sx, sy = mode.scrollX, mode.scrollY
        cx, cy = mode.getBounds(self.x, self.y)
        canvas.create_image(cx - sx, cy - sy, image=img)

    @staticmethod
    def randomProblem(year):
        problems = Constants.problems
        
        year -= 1
        year = min(year, len(problems)-1)

        probset = problems[year]
        idx = random.randrange(0, len(probset) - 1)

        return probset[idx]

