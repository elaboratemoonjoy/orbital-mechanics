class GameObject:
    def __init__(self):
        ...

    def update(self, dt):
        raise NotImplementedError("Subclasses must implement the update method!")


    def draw(self, screen):
        ...