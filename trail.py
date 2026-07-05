from pygame import Vector2, draw

class Trail():
    def __init__(self):
        self.points = []
        self.length = 2000

    def create_segments(self):
        segments = []

        if len(self.points) > 120:
            self.points.pop(0)

        if len(self.points) > 0:
            from_point = self.points[0]
            for point in self.points[1:]:
                segments.append((from_point, point))
                from_point = point

            return segments
        return []