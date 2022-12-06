from pytetris.objects import *
from pytetris.settings import *

# TODO:
# add ghost piece
# refactor to more oop


class Game:

    def __init__(self):
        pg.init()
        pg.font.init()
        pg.display.set_caption("basic tetris")

        self.font = pg.font.SysFont(FONT, 100)
        self.title_text = self.font.render('TETRIS', True, pg.Color(0, 127, 127))
        self.score_text = self.font.render('Score', True, pg.Color(0, 63, 63))

        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.black_background = pg.display.get_surface().convert()
        self.black_background.fill((0, 0, 0))
        self.gray_background = pg.display.get_surface().convert()
        self.gray_background.fill((127, 127, 127))

        self.game_borders = pg.rect.Rect(PLAY_W_OFF, 0, PLAY_W, PLAY_H + PLAY_H_OFF)
        self.visible_borders = pg.rect.Rect(PLAY_W_OFF, PLAY_H_OFF, PLAY_W, PLAY_H)

        self.clock = pg.time.Clock()
        self.fall_speed = 4.0
        pg.time.set_timer(DROP, int(1000/self.fall_speed))

        self.new_game()

    def new_game(self):
        self.stack = Stack()
        self.hold = Hold()
        self.piece_queue = PiecePreview()
        self.piece = self.piece_queue.pop(self.game_borders, self.stack)

    def initial_draw(self):
        self.screen.blit(self.black_background, (0, 0))
        self.screen.blit(self.gray_background, (PLAY_W_OFF, PLAY_H_OFF), self.visible_borders)

        self.screen.blit(self.title_text, (480-self.title_text.get_size()[0]//2, 40))
        self.screen.blit(self.score_text, (40, 400))

        pg.draw.rect(self.screen, (0, 63, 63), self.hold.rect.inflate(10, 10), 5)
        pg.draw.rect(self.screen, (0, 63, 63), self.piece_queue.rect.inflate(10, 10), 5)
        pg.draw.rect(self.screen, (0, 127, 127), self.visible_borders.inflate(10, 10), 5)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == DROP:
                self.piece.drop()
                if self.piece.stop:
                    self.stack.add(self.piece)
                    if self.stack.check_blockout():
                        pg.quit()
                    else:
                        self.piece = self.piece_queue.pop(self.game_borders, self.stack)
                        self.piece_queue.draw(self.screen, self.game_borders, self.stack, self.black_background)
                        pg.time.set_timer(DROP, int(1000 / self.fall_speed))
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                if event.key == pg.K_LEFT:
                    self.piece.left()
                if event.key == pg.K_RIGHT:
                    self.piece.right()
                if event.key == pg.K_UP:
                    self.piece.rotate()
                if event.key == pg.K_DOWN:
                    self.piece.down()
                if event.key == pg.K_r:
                    self.new_game()
                    self.initial_draw()
                if event.key == pg.K_SPACE:
                    self.piece.hard_drop()
                if event.key == pg.K_LCTRL:
                    if not self.piece.held:
                        if not self.hold.has_piece:
                            self.piece.draw_background(self.screen, self.gray_background)
                            self.hold.set_hold(self.piece)
                            self.hold.draw_background(self.screen, self.black_background)
                            self.hold.draw(self.screen)
                            self.piece = self.piece_queue.pop(self.game_borders, self.stack)
                        else:
                            self.piece.draw_background(self.screen, self.gray_background)
                            new_piece = self.hold.get_hold(self.game_borders, self.stack)
                            self.hold.set_hold(self.piece)
                            self.hold.draw_background(self.screen, self.black_background)
                            self.hold.draw(self.screen)
                            self.piece = new_piece

    def update(self):
        self.piece_queue.update()

        self.piece.update()
        self.stack.update()

    def draw_backgrounds(self):
        self.piece.draw_background(self.screen, self.gray_background)
        self.stack.draw_background(self.screen, self.gray_background)
        if self.piece.held:
            self.hold.draw_background(self.screen, self.black_background)

        if self.piece_queue.new_piece:
            self.screen.blit(self.black_background, self.piece_queue.rect, self.piece_queue.rect)

    def draw(self):
        self.piece.draw(self.screen)
        self.hold.draw(self.screen)
        self.stack.draw(self.screen)
        if self.piece_queue.new_piece:
            self.piece_queue.draw(self.screen, self.game_borders, self.stack,
                                  self.black_background)
            self.piece_queue.new_piece = False

        self.screen.blit(self.black_background, self.stack.score_rect, self.stack.score_rect)
        self.screen.blit(self.font.render(str(self.stack.score), True, pg.Color(0, 63, 63)), (40, 480))

    def run(self):
        self.initial_draw()
        while True:
            self.check_events()
            self.draw_backgrounds()
            self.update()
            self.draw()
            pg.display.update()
            self.clock.tick(60)


def main():
    pg.init()

    pg.font.init()
    font = pg.font.SysFont(FONT, 100)

    game_screen = pg.display.set_mode(WINDOW_SIZE)

    title = font.render('TETRIS', True, pg.Color(0, 127, 127))
    score_str = font.render('Score', True, pg.Color(0, 63, 63))

    game_screen.blit(title, (480-title.get_size()[0]//2, 40))
    game_screen.blit(score_str, (40, 400))

    black_bg = pg.display.get_surface().convert()
    black_bg.fill((0, 0, 0))

    gray_bg = pg.display.get_surface().convert()
    gray_bg.fill((127, 127, 127))

    play_borders = pg.rect.Rect(PLAY_W_OFF, 0, PLAY_W, PLAY_H + PLAY_H_OFF)
    vis_borders = pg.rect.Rect(PLAY_W_OFF, PLAY_H_OFF, PLAY_W, PLAY_H)

    stack = Stack()
    hold = Hold()
    hold.draw_outline(game_screen, black_bg)

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
                    if not piece.held:
                        if not hold.has_piece:
                            piece.draw_background(game_screen, gray_bg)
                            hold.set_hold(piece)
                            hold.draw_background(game_screen, black_bg)
                            hold.draw(game_screen)
                            piece = piece_queue.pop(play_borders, stack)
                        else:
                            piece.draw_background(game_screen, gray_bg)
                            new_piece = hold.get_hold(play_borders, stack)
                            hold.set_hold(piece)
                            hold.draw_background(game_screen, black_bg)
                            hold.draw(game_screen)
                            piece = new_piece

        piece.draw_background(game_screen, gray_bg)
        stack.draw_background(game_screen, gray_bg)
        piece.update()
        stack.update()
        piece.draw(game_screen)
        stack.draw(game_screen)

        game_screen.blit(black_bg, stack.score_rect, stack.score_rect)
        game_screen.blit(font.render(str(stack.score), True, pg.Color(0, 63, 63)), (40, 480))

        pg.display.update()

        clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()
