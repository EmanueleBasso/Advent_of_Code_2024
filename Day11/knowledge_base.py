class KnowledgeBase:
    def __init__(self, stone: int, expansion_after_twentyfive_blinks: list[str]):
        self.stone = stone
        self.expansion_after_twentyfive_blinks = expansion_after_twentyfive_blinks

    def __lt__(self, other):
        return self.stone < other.stone

    def __eq__(self, other):
        if isinstance(other, KnowledgeBase):
            return self.stone == other.stone

        return False
