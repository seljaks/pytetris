import pygame as pg
from random import sample

from pytetris.pieces import PIECES, SHAPES

WIN_W = 960
WIN_H = 1005
WINDOW_SIZE = (WIN_W, WIN_H)
PLAY_W = 400
PLAY_H = 800
PLAY_SIZE = (PLAY_W, PLAY_H)
GRID_W = 10
GRID_H = 20
GRID_SIZE = (GRID_W, GRID_H)

PLAY_W_OFF = (WIN_W - PLAY_W)//2
PLAY_H_OFF = 200

BOX = PLAY_W // GRID_W

GRAVITY_DROP = pg.USEREVENT + 1
PIECE_STOP = pg.USEREVENT + 2


class Stack(pg.sprite.Group):

    def __init__(self):
        self.row_fullness = {i: 0 for i in reversed(range(0, PLAY_H+PLAY_H_OFF, BOX))}
        super().__init__()

    def add(self, *sprites):
        super().add(*sprites)
        for block in sprites:
            if isinstance(block, Block):
                y = block.y
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
                if block.y in lines:
                    block.kill()
                elif block.y < top_line:
                    block.y += no_lines * BOX
                block.update()

            fullness = self.row_fullness
            count = 0
            for row in fullness:
                if row in lines:
                    count += BOX
                elif row in range(0, PLAY_H_OFF, BOX):
                    fullness[row] = 0
                else:
                    fullness[row+count] = fullness[row]

    def draw_background(self, surface, background):
        surface.blits((background, block.rect, block.rect)
                      for block in self if block.y >= PLAY_H_OFF)


class Block(pg.sprite.Sprite):

    def __init__(self, color, x_off, y_off, x=0, y=0):
        super().__init__()
        self.image = pg.Surface((BOX, BOX))
        self.image.fill(pg.color.Color(color))

        self.x_off = x_off
        self.y_off = y_off
        self.x = x + x_off
        self.y = y + y_off

        self.rect = pg.rect.Rect((self.x, self.y,),
                                 (BOX, BOX))

    def update(self):
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


class Piece(pg.sprite.Group):

    def __init__(self, shape, borders, stack, rotation=0, x=0, y=0):
        super().__init__()
        self.shape = shape
        self.color = SHAPES[shape]["color"]
        self.stack = stack

        self.x = x if x else PLAY_W_OFF + SHAPES[shape]["x_offset"] * BOX
        self.y = y if y else PLAY_H_OFF + SHAPES[shape]["y_offset"] * BOX

        self.borders = borders

        self.rotation_dict = {k: tuple((v1*BOX, v2*BOX) for (v1, v2) in v)
                              for k, v in SHAPES[shape]["rot"].items()}
        self.rotation = rotation
        self.rotated = False

        self.stop = False

        for block in self.make_blocks():
            self.add(block)

    def make_blocks(self):
        blocks = (Block(self.color, x_off, y_off, x=self.x, y=self.y)
                  for x_off, y_off in self.rotation_dict[self.rotation])
        return blocks

    def update(self):
        for i, block in enumerate(self):
            if self.rotated:
                x_off, y_off = self.rotation_dict[self.rotation][i]
                block.x_off, block.y_off = x_off, y_off
            block.x = self.x + block.x_off
            block.y = self.y + block.y_off
            block.update()
        self.rotated = False

    def draw(self, surface, vis_borders):
        surface.blits((block.image, block.rect)
                      for block in self if vis_borders.contains(block.rect))

    def draw_background(self, surface, background, vis_borders):
        surface.blits((background, block.rect, block.rect)
                      for block in self if vis_borders.contains(block.rect))

    def draw_preview(self, surface):
        surface.blits((block.image, block.rect)
                      for block in self)

    def valid_move(self, x, y):
        for block in self:
            test_block = pg.sprite.Sprite()
            test_block.rect = block.rect.move(x, y)

            if not self.borders.contains(test_block.rect):
                return False

            if pg.sprite.spritecollide(test_block, self.stack, False):
                return False

        return True

    def down(self):
        y = BOX
        if self.valid_move(0, y):
            print("piece moved down")
            self.y += y
        else:
            print("piece stopped")
            pg.event.clear()
            pg.event.post(pg.event.Event(PIECE_STOP))

    def left(self):
        x = -BOX
        if self.valid_move(x, 0):
            print("piece moved left")
            self.x += x

    def right(self):
        x = BOX
        if self.valid_move(x, 0):
            print("piece moved right")
            self.x += x

    def hard_drop(self):
        y = 0
        while self.valid_move(0, y):
            y += BOX
        y -= BOX
        self.y += y
        pg.event.post(pg.event.Event(PIECE_STOP))

    def hold(self):
        pass

    def valid_rotation(self):
        new_rot = (self.rotation + 1) % 4
        test_piece = Piece(self.shape, self.borders, self.stack, rotation=new_rot,
                           x=self.x, y=self.y)
        for block in test_piece:
            if (
                    not self.borders.contains(block.rect)
                    or pg.sprite.spritecollideany(block, self.stack)
            ):
                return False
        return True

    def rotate(self):
        if self.valid_rotation():
            self.rotated = True
            self.rotation = (self.rotation + 1) % 4


class PiecePreview:

    def __init__(self):
        self.two_bags = list()
        self.add_new_bag()
        self.add_new_bag()

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
        return Piece(shape, borders, stack)

    def update(self):
        if len(self) == len(PIECES):
            self.add_new_bag()


def draw_grid(screen):
    for i in range(0, WIN_W, BOX):
        pg.draw.line(screen, pg.Color(100, 0, 0, 10), (i, 0), (i, WIN_H), 1)
    for i in range(0, WIN_H, BOX):
        pg.draw.line(screen, pg.Color(0, 0, 100, 10), (0, i), (WIN_W, i), 1)


def main():
    pg.init()
    game_screen = pg.display.set_mode(WINDOW_SIZE)
    pg.display.set_caption("basic tetris")

    draw_grid(game_screen)

    black_bg = pg.display.get_surface().convert()
    black_bg.fill((0, 0, 0))

    gray_bg = pg.display.get_surface().convert()
    gray_bg.fill((127, 127, 127))

    play_borders = pg.rect.Rect(PLAY_W_OFF, 0, PLAY_W, PLAY_H+PLAY_H_OFF)
    vis_borders = pg.rect.Rect(PLAY_W_OFF, PLAY_H_OFF, PLAY_W, PLAY_H)

    stack = Stack()

    piece_queue = PiecePreview()
    piece = piece_queue.pop(play_borders, stack)

    piece_queue.draw(game_screen, play_borders, stack, black_bg)
    pg.draw.rect(game_screen, (0, 63, 63), piece_queue.rect.inflate(10, 10), 5)

    game_screen.blit(gray_bg, (PLAY_W_OFF, PLAY_H_OFF), vis_borders)
    pg.draw.rect(game_screen, (0, 127, 127), vis_borders.inflate(10, 10), 5)

    stack.draw(game_screen)
    pg.display.update()

    clock = pg.time.Clock()
    fall_speed = 4.0
    pg.time.set_timer(GRAVITY_DROP, int(1000/fall_speed))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == GRAVITY_DROP:
                piece.down()
            elif event.type == PIECE_STOP:
                stack.add(piece)
                if stack.check_blockout():
                    pg.quit()
                else:
                    piece = piece_queue.pop(play_borders, stack)
                    piece_queue.update()
                    game_screen.blit(black_bg, piece_queue.rect, piece_queue.rect)
                    piece_queue.draw(game_screen, play_borders, stack, black_bg)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                if event.key == pg.K_LEFT:
                    piece.left()
                if event.key == pg.K_RIGHT:
                    piece.right()
                if event.key == pg.K_UP:
                    piece.rotate()
                if event.key == pg.K_DOWN:
                    piece.down()
                if event.key == pg.K_SPACE:
                    piece.hard_drop()
                if event.key == pg.K_LCTRL:
                    piece.hold()


        piece.draw_background(game_screen, gray_bg, vis_borders)
        stack.draw_background(game_screen, gray_bg)
        piece.update()
        stack.update()
        piece.draw(game_screen, vis_borders)
        stack.draw(game_screen)
        pg.display.update()

        clock.tick(10)


if __name__ == '__main__':
    main()
