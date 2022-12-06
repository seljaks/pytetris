from random import sample
from pytetris.settings import *


class Piece(pg.sprite.Group):

    def __init__(self, shape, borders, stack, rot=0, x=0, y=0):
        super().__init__()
        self.shape = shape
        self.color = SHAPES[shape]["color"]
        self.stack = stack

        self.x = x if x else PLAY_W_OFF + SHAPES[shape]["x_offset"] * BOX
        self.y = y if y else PLAY_H_OFF + SHAPES[shape]["y_offset"] * BOX

        self.borders = borders
        self.rotation_dict = {k: tuple((v1 * BOX, v2 * BOX) for (v1, v2) in v)
                              for k, v in SHAPES[shape]["rot"].items()}
        self.rot = rot
        self.stop = False
        self.held = False

        for block in self.make_blocks(self.x, self.y):
            self.add(block)

    def make_blocks(self, x, y):
        blocks = (Block(self.color, x_off, y_off, x=x, y=y)
                  for x_off, y_off in self.rotation_dict[self.rot])
        return blocks

    def update(self):
        for i, block in enumerate(self):
            x_off, y_off = self.rotation_dict[self.rot][i]
            x = self.x + x_off
            y = self.y + y_off
            block.update(x, y)

    def draw(self, surface):
        surface.blits((block.image, block.rect)
                      for block in self if block.rect.y >= PLAY_H_OFF)

    def draw_background(self, surface, background):
        surface.blits((background, block.rect, block.rect)
                      for block in self if block.rect.y >= PLAY_H_OFF)

    def draw_preview(self, surface):
        surface.blits((block.image, block.rect)
                      for block in self)

    def drop(self):
        dy = BOX
        if self.valid_move(0, dy):
            self.y += BOX
        else:
            self.stop = True

    def left(self):
        dx = -BOX
        if self.valid_move(dx, 0):
            self.x += dx

    def right(self):
        dx = BOX
        if self.valid_move(dx, 0):
            self.x += dx

    def rotate(self):
        if self.valid_rotation():
            self.rot = (self.rot + 1) % 4

    @staticmethod
    def down():
        pg.event.post(pg.event.Event(DROP))

    @staticmethod
    def hard_drop():
        pg.time.set_timer(DROP, 20)

    def valid_rotation(self):
        new_rot = (self.rot + 1) % 4
        test_piece = Piece(self.shape, self.borders, self.stack, rot=new_rot,
                           x=self.x, y=self.y)
        for block in test_piece:
            if (
                    not self.borders.contains(block.rect)
                    or pg.sprite.spritecollideany(block, self.stack)
            ):
                return False
        return True

    def valid_move(self, x, y):
        for block in self:
            test_block = pg.sprite.Sprite()
            test_block.rect = block.rect.move(x, y)

            if not self.borders.contains(test_block.rect):
                return False

            if pg.sprite.spritecollide(test_block, self.stack, False):
                return False
        return True


class Block(pg.sprite.Sprite):

    def __init__(self, color, x_off, y_off, x=0, y=0):
        super().__init__()
        self.image = pg.Surface((BOX, BOX))
        self.image.fill(pg.color.Color(color))

        x = x + x_off
        y = y + y_off
        self.rect = pg.rect.Rect((x, y), (BOX, BOX))

    def update(self, x, y):
        self.rect.update((x, y), (BOX, BOX))


class PiecePreview:

    def __init__(self):
        self.two_bags = list()
        self.add_new_bag()
        self.add_new_bag()

        self.new_piece = False

        self.rect = pg.rect.Rect((PLAY_W + PLAY_W_OFF + 80, PLAY_H_OFF - 40),
                                 (160, PLAY_H))

    def __len__(self):
        return len(self.two_bags)

    def add_new_bag(self):
        new_bag = sample(PIECES, k=len(PIECES))
        self.two_bags.extend(new_bag)

    def draw(self, surface, borders, stack, background):
        surface.blit(background, self.rect, self.rect)

        x_pos = self.rect.x
        y_pos = self.rect.y
        for shape in self.two_bags[:len(PIECES)]:
            x_inc = 20
            y_inc = 3

            if shape == "I":
                x_inc = 0
                y_inc = 2
            elif shape == "O":
                x_inc = 40

            x = x_pos + x_inc
            piece = Piece(shape, borders, stack, x=x, y=y_pos)
            piece.draw_preview(surface)
            y_pos += y_inc * BOX

    def pop(self, borders, stack):
        shape = self.two_bags.pop(0)
        self.new_piece = True
        return Piece(shape, borders, stack)

    def update(self):
        if len(self) == len(PIECES):
            self.add_new_bag()


class Stack(pg.sprite.Group):

    def __init__(self):
        self.row_fullness = {i: 0 for i in reversed(range(0, PLAY_H + PLAY_H_OFF, BOX))}
        super().__init__()
        self.score = 0
        self.score_rect = pg.rect.Rect((40, 480), (200, 100))

    def add(self, *sprites):
        super().add(*sprites)
        for block in sprites:
            if isinstance(block, Block):
                y = block.rect.y
                self.row_fullness[y] += 1

    def check_full_lines(self):
        full_lines = list()
        for row in self.row_fullness:
            if self.row_fullness[row] == 10:
                full_lines.append(row)
        return full_lines

    def check_blockout(self):
        for row in range(0, PLAY_H_OFF, BOX):
            if self.row_fullness[row]:
                return True
        return False

    def update(self):
        lines = self.check_full_lines()
        if lines:
            no_lines = len(lines)
            top_line = min(lines)
            for block in self:
                if block.rect.y in lines:
                    block.kill()
                elif block.rect.y < top_line:
                    block.rect.y += no_lines * BOX

            fullness = self.row_fullness
            count = 0
            for row in fullness:
                if row in lines:
                    count += BOX
                elif row in range(0, PLAY_H_OFF, BOX):
                    fullness[row] = 0
                else:
                    fullness[row+count] = fullness[row]

            self.score += SCORE_MULT[no_lines]

    def draw_background(self, surface, background):
        surface.blits((background, block.rect, block.rect)
                      for block in self if block.rect.y >= PLAY_H_OFF)


class Hold(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = pg.rect.Rect((HOLD_X, HOLD_Y), (4*BOX, 4*BOX))

        self.piece = None
        self.has_piece = False

    def draw_outline(self, surface, background):
        self.draw_background(surface, background)
        pg.draw.rect(surface, (0, 63, 63), self.rect.inflate(10, 10), 5)

    def draw_background(self, surface, background):
        surface.blit(background, self.rect, self.rect)

    def draw(self, surface):
        if self.has_piece:
            self.piece.draw(surface)

    def set_hold(self, piece):
        self.has_piece = True
        self.piece = piece
        self.piece.rot = 0
        x_off, y_off = 20, 40
        if piece.shape == "I":
            x_off, y_off = 0, 60
        elif piece.shape == "O":
            x_off, y_off = 40, 40

        self.piece.x = HOLD_X + x_off
        self.piece.y = HOLD_Y + y_off
        self.piece.update()

    def get_hold(self, borders, stack):
        if self.has_piece:
            piece = Piece(self.piece.shape, borders, stack)
            piece.held = True
            return piece
