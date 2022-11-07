from pytetris.objects import Stack, PiecePreview
from pytetris.settings import *


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

    play_borders = pg.rect.Rect(PLAY_W_OFF, 0, PLAY_W, PLAY_H + PLAY_H_OFF)
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
    pg.time.set_timer(DROP, int(1000 / fall_speed))

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == DROP:
                piece.drop()
                if piece.stop:
                    stack.add(piece)
                    if stack.check_blockout():
                        pg.quit()
                    else:
                        piece = piece_queue.pop(play_borders, stack)
                        piece_queue.update()
                        game_screen.blit(black_bg, piece_queue.rect, piece_queue.rect)
                        piece_queue.draw(game_screen, play_borders, stack, black_bg)
                        pg.time.set_timer(DROP, int(1000 / fall_speed))
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

        piece.draw_background(game_screen, gray_bg)
        stack.draw_background(game_screen, gray_bg)
        piece.update()
        stack.update()
        piece.draw(game_screen)
        stack.draw(game_screen)
        pg.display.update()

        clock.tick(60)


if __name__ == '__main__':
    main()
