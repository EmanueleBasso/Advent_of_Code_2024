class PositionVisitedWithDirection:
    def __init__(self, x: int, y: int, direction: str):
        self.x = x
        self.y = y
        self.direction = direction

    def __lt__(self, other):
        if self.x < other.x:
            return True
        elif self.x > other.x:
            return False
        else:
            if self.y < other.y:
                return True
            elif self.y > other.y:
                return False
            else:
                return self.direction < other.direction

    def __eq__(self, other):
        if isinstance(other, PositionVisitedWithDirection):
            return (
                self.x == other.x
                and self.y == other.y
                and self.direction == other.direction
            )
        return False
