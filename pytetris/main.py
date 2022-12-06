from pytetris.objects import *
from pytetris.settings import *

# TODO:
# add ghost piece


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


if __name__ == '__main__':
    game = Game()
    game.run()
