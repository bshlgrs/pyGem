# draggable rectangle:

class Draggable():
    def __init__(self):
        self.beingDragged = False
        self.offsetX = None
        self.offsetY = None

    def reactToClickOn(self):
        pos = pygame.mouse.get_pos()
        hitbox = self.rect.inflate(0,0)
        if pos is inside hitbox: ?????
            self.beingDragged = True
            self.offsetX = self.x - pos[0]
            self.offsetY = self.y - pos[1]

    def reactToClickOff(self):
        self.beingDragged = False

    def update(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        if self.beingDragged:
            self.x = mouseX + self.offsetX
            self.y = mouseY + self.offsetY

