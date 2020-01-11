import slowEngine
from slowEngine.geometery import *
from tiles.chunk_handler import CHUNK_SIZE


class Player(slowEngine.physics.BoxObject):
    def __init__(self, rect=Rect(0, 6, 1, 2) * 0.9):
        slowEngine.physics.BoxObject.__init__(self, rect)

        self.collider = slowEngine.physics.BoxCollider(self)

        self.sides_touching = {}
        self.set_sides_touching()

        controls = {"A": Vector(-1, 0), "D": Vector(1, 0)}
        self.controller = slowEngine.controllers.KeyBoardControllerSmooth(self, controls)
        self.max_velocity = Vector(4, 10)
        self.jump_power = 5

        self.current_chunks = []

    def update(self, engine, chunk_handler):
        self.apply_gravity(engine)
        self.movement(engine)
        self.apply_velocity(engine)
        self.update_sides_touching(chunk_handler)
        self.block_collisions(chunk_handler)

    def block_collisions(self, chunk_handler):
        self.current_chunks = []
        for chunk in chunk_handler.chunks.values():
            if self.collider.is_collided_box(chunk.collider):
                self.current_chunks.append(chunk)
        for chunk in self.current_chunks:
            self.collider.run_collisions(objects=chunk.blocks.values())

    def set_sides_touching(self):
        self.sides_touching = {
            (1, 0): [],
            (-1, 0): [],
            (0, 1): [],
            (0, -1): [],
        }

    def update_sides_touching(self, chunk_handler):
        self.set_sides_touching()
        player_chunk = ((self.rect.pos() / CHUNK_SIZE) + Vector(0.5, 0.5)).floor()

        neighbor_chunks = []
        for chunk_change in [Vector(1, 0), Vector(-1, 0), Vector(0, 1), Vector(0, -1), Vector(0, 0)]:
            chunk_pos = player_chunk + chunk_change
            if tuple(chunk_pos) in chunk_handler.chunks:
                neighbor_chunks.append(chunk_pos)

        touching_chunks = []
        for chunk_pos in neighbor_chunks:
            chunk = chunk_handler.chunks[tuple(chunk_pos)]
            if self.collider.is_collided_box(chunk.collider):
                touching_chunks.append(chunk)

        for chunk in touching_chunks:
            for block in chunk.blocks.values():
                collision_side = self.collider.box_collision_side(block.collider)
                if collision_side.x or collision_side.y:
                    self.sides_touching[tuple(collision_side)] = block

    def show(self, engine):
        self.show_block(engine, (0, 200, 0))
        for chunk in self.current_chunks:
            chunk.show_block(engine, (255, 0, 0), 2)

    def movement(self, engine):
        if self.sides_touching[(0, -1)]:
            self.controller.acceleration = 100
            if engine.keyboard.tapped["SPACE"] == 1:
                self.velocity.y = self.jump_power
        else:
            self.controller.acceleration = 52

        self.controller.update(engine)
