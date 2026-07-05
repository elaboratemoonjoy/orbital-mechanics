class GameObjectGroup:
    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def remove(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def update(self):
        for obj in self.objects:
            obj.update()

    def draw(self, screen):
        for obj in self.objects:
            obj.draw(screen)
