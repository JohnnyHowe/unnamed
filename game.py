import slowEngine
from slowEngine.geometery import *

import tiles
import player as player_mod


class Game:
    def __init__(self):
        self.engine = slowEngine.Engine()
        self.engine.set_window(Vector(600, 600), 20)

        self.chunk_handler = tiles.chunk_handler.ChunkHandler()

        gr = 3
        for x in range(-gr, gr + 1):
            # self.chunk_handler.chunks[(x, -2)] = tiles.chunk_generator.solid_chunk(Vector(x, -2), tiles.blocks.Block, self.chunk_handler)
            self.chunk_handler.chunks[(x, -1)] = tiles.chunk_generator.solid_chunk(Vector(x, -1), tiles.blocks.Block, self.chunk_handler)
            self.chunk_handler.chunks[(x, 0)] = tiles.chunk_generator.surface_chunk(Vector(x, 0), tiles.blocks.Block, self.chunk_handler)

        self.player = player_mod.Player()

    def show(self):
        self.engine.window.fill()
        self.engine.window.draw_grid(xy_max=15)

        self.chunk_handler.show(self.engine, self.player)
        self.player.show(self.engine)

        self.engine.window.update_display()

    def update(self):
        self.engine.update()
        self.player.update(self.engine, self.chunk_handler)
        self.engine.window.set_caption(round(self.engine.clock.get_fps()))
