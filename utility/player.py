from constants import Constants

class Player:
    def __init__(self, mode):
        self.x = 0
        self.y = 0
        self.mode = mode

        self.currentYear = 1
        self.graduationYear = 5
        self.radius = 0.5 * self.mode.gridSize

    def movePlayer(self, dx, dy):
        self.x += dx
        self.y += dy
        if (self.x < 0 or self.x > Constants.gridWidth - 1):
            self.x -= dx
        if (self.y < 0 or self.y > Constants.gridHeight - 1):
            self.y -= dy
        self.wrapMovement()

    def wrapMovement(self):
        mode = self.mode
        px, py = mode.getBounds(self.x, self.y)
        # scroll to make player visible as needed
        if (px - self.radius < mode.scrollX + mode.margin):
            mode.scrollX = px - self.radius - mode.margin
        if (px + self.radius > mode.scrollX + mode.width - mode.margin):
            mode.scrollX = px + self.radius - mode.width + mode.margin
        if (py - self.radius < mode.scrollY + mode.margin):
            mode.scrollY = py - self.radius - mode.margin
        if (py + self.radius > mode.scrollY + mode.height - mode.margin):
            mode.scrollY = py + self.radius - mode.height + mode.margin

    def draw(self, mode, canvas):
        sx, sy = mode.scrollX, mode.scrollY
        r = self.radius
        cx, cy = mode.getBounds(self.x, self.y)
        canvas.create_oval(cx-r-sx, cy-r-sy, cx+r-sx, cy+r-sy)

    