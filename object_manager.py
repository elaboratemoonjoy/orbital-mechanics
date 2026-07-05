from game_object import GameObject


class ObjectManager:
    def __init__(self, screen, game_objects: list[GameObject] = []):
        self.screen = screen
        self.objects: list[GameObject] = game_objects

    def add(self, obj):
        self.objects.append(obj)

    def remove(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def update(self, dt):
        for obj in self.objects:
            obj.update(dt)

    def draw(self, screen):
        for obj in self.objects:
            obj.draw(screen)
