import random
from slowEngine.geometery import *
from .chunk_handler import Chunk, CHUNK_SIZE
from .blocks import BLOCK_SIZE


def solid_chunk(pos, block, chunk_handler):
    chunk = Chunk(pos)
    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            relative_pos = Vector(x, y) * BLOCK_SIZE
            block_obj = block(relative_pos, chunk)
            chunk.blocks[tuple(relative_pos)] = block_obj
    return chunk


def surface_chunk(pos, block, chunk_handler):
    chunk = Chunk(pos)
    top_ys = surface_layer(pos, chunk_handler)
    for x in range(CHUNK_SIZE):
        for y in range(0, top_ys[x]):
            relative_pos = Vector(x, y)
            block_obj = block(relative_pos, chunk)
            chunk.blocks[tuple(relative_pos)] = block_obj
    return chunk


def last_surface_ys(pos, chunk_handler):
    left_chunk_pos = Vector(pos.x - 1, pos.y)
    right_chunk_pos = Vector(pos.x + 1, pos.y)

    left_y = None
    right_y = None

    if tuple(left_chunk_pos) in chunk_handler.chunks:
        chunk = chunk_handler.chunks[tuple(left_chunk_pos)]
        left_chunk = chunk.right_land_piece()
        if left_chunk:
            left_y = left_chunk.rect.y
    if tuple(right_chunk_pos) in chunk_handler.chunks:
        chunk = chunk_handler.chunks[tuple(right_chunk_pos)]
        right_chunk = chunk.left_land_piece()
        if right_chunk:
            right_y = right_chunk.rect.y

    return left_y, right_y


def surface_layer(pos, chunk_handler):
    left, right = last_surface_ys(pos, chunk_handler)
    if left:
        layer = surface_ys(left)
    elif right:
        layer = list(reversed(surface_ys(right)))
    else:
        layer = surface_ys(CHUNK_SIZE // 2)
    return layer


def surface_ys(start):
    surface = [start, ]
    for x in range(CHUNK_SIZE - 1):
        surface.append(next_surface_y(surface[-1]))
    return surface


def next_surface_y(last):
    change = random.choice([0, ] * 3 + [1, -1])
    return max(min(last + change, CHUNK_SIZE), 0)


