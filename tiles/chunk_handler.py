import random

import slowEngine
from slowEngine.geometery import *

from .blocks import *

CHUNK_SIZE = 5


class ChunkHandler:
    def __init__(self):
        self.chunks = {}

    def set_chunk(self, chunk):
        self.chunks[tuple(chunk.chunk_pos)] = chunk

    def show(self, engine, player):
        chunks = self.on_screen_chunks(engine, player)
        # chunks = self.chunks.values()
        for chunk in chunks:
            chunk.show(engine)
        self.draw_chunk_outlines(engine)

    def on_screen_chunks(self, engine, player):
        """ What chunks are on screen? """
        num_chunks = engine.window.size.copy()
        num_chunks /= (CHUNK_SIZE * BLOCK_SIZE)
        num_chunks //= engine.window.game_scale
        num_chunks += Vector(1, 1)

        player_chunk_pos = ((player.rect.pos() / CHUNK_SIZE) + Vector(0.5, 0.5)).floor()
        print(num_chunks)

        chunks = []
        for dx in range(-num_chunks.x // 2, num_chunks.x // 2):
            for dy in range(-num_chunks.y // 2, num_chunks.y // 2):
                pos = player_chunk_pos + Vector(dx, dy)
                if tuple(pos) in self.chunks:
                    chunks.append(self.chunks[tuple(pos)])
        return chunks

    def draw_chunk_outlines(self, engine):
        for chunk in self.chunks.values():
            chunk.show_block(engine, color=(100, 100, 255), width=1)


class Chunk(slowEngine.physics.BoxObject):
    def __init__(self, chunk_pos):
        self.chunk_pos = chunk_pos
        self.rect = Rect(chunk_pos.x, chunk_pos.y, 1, 1) * CHUNK_SIZE * BLOCK_SIZE
        slowEngine.physics.BoxObject.__init__(self, self.rect)
        self.collider = slowEngine.physics.BoxCollider(self)
        self.blocks = {}

    def show(self, engine):
        for block in self.blocks.values():
            block.show(engine)

    def top_layer(self):
        """ Return a list of length CHUNK_SIZE containing the top layer of the chunk.
        if there is no block in that column, None will be at that index. """
        layer = [None, ] * CHUNK_SIZE
        for rx in range(CHUNK_SIZE):
            for ry in range(CHUNK_SIZE, 0, -1):
                rel_tup = (rx, ry)
                if rel_tup in self.blocks:
                    layer[rx] = self.blocks[rel_tup]
                    break
        return layer

    def left_land_piece(self):
        """ Return the left-most block on the top layer, None if it does not exist. """
        for block in self.top_layer():
            if block:
                return block

    def right_land_piece(self):
        """ Return the left-most block on the top layer, None if it does not exist. """
        for block in reversed(self.top_layer()):
            if block:
                return block

