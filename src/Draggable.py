class Draggable (object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

        self.dragX = 0
        self.dragY = 0
        self.beingDragged = False
        self.beingEqualled = False
