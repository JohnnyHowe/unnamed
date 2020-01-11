import slowEngine
from slowEngine.geometery import *

BLOCK_SIZE = 1


class Block(slowEngine.physics.BoxObject):
    def __init__(self, relative_pos, parent_chunk):
        """ relative_pos is the position inside the chunk where (0, 0) is the bottom left. """
        slowEngine.physics.BoxObject.__init__(self, Rect(relative_pos.x, relative_pos.y, BLOCK_SIZE, BLOCK_SIZE))
        self.parent_chunk = parent_chunk
        self.collider = slowEngine.physics.BoxCollider(self)
        self.collider.mass = float("inf")

    def show(self, engine):
        self.show_block(engine, (50, 50, 50))
        self.show_block(engine, (0, 0, 0), width=2)

    def get_full_rect(self):
        rect = self.rect.copy()
        rect.x -= self.parent_chunk.rect.w // 2 - BLOCK_SIZE // 2
        rect.y -= self.parent_chunk.rect.h // 2 - BLOCK_SIZE // 2
        rect.x += self.parent_chunk.rect.x
        rect.y += self.parent_chunk.rect.y
        return rect

    def get_collision_rect(self):
        return self.get_full_rect()

    def get_display_rect(self):
        return self.get_full_rect()
