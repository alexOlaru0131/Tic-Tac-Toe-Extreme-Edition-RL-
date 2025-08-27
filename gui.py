###### gui.py ######
# ->

###### IMPORTS ######
from imports import *
###### END IMPORTS ######

###### GUI ######
class GUI:
        def __init__(self, pygame):
                self.WHITE = (255, 255, 255)
                self.GRAY = (255, 255, 255, 0)
                self.BLACK = (0, 0, 0)
                self.pygame = pygame
                self.display = pygame.display.set_mode((300, 400))
                self.pygame.init()

                self.p1_moves = []
                self.p2_moves = []

                self._action = {
                        0: [0, 0],
                        1: [0, 1],
                        2: [0, 2],
                        3: [1, 0],
                        4: [1, 1],
                        5: [1, 2],
                        6: [2, 0],
                        7: [2, 1],
                        8: [2, 2],
                }

                self._winner_lines = {
                        "l0": [0, 0, 2, 0],
                        "l1": [0, 1, 2, 1],
                        "l2": [0, 2, 2, 2],
                        "c0": [0, 0, 0, 2],
                        "c1": [1, 0, 1, 2],
                        "c2": [2, 0, 2, 2],
                        "dp": [0, 0, 2, 2],
                        "ds": [0, 2, 2, 0],
                }

        def draw_x(self, x, y):
                self.pygame.draw.line(self.display, self.WHITE, (20 + x*100, 120 + y*100), (80 + x*100, 180 + y*100), 5)
                self.pygame.draw.line(self.display, self.WHITE, (80 + x*100, 120 + y*100), (20 + x*100, 180 + y*100), 5)
                self.pygame.display.update()
                        
        def draw_o(self, x, y):
                self.pygame.draw.circle(self.display, self.WHITE, (50 + x*100, 150 + y*100), 35, 5)
                self.pygame.display.update()

        def update(self, draw, move):
                self.pygame.display.set_caption('Tic Tac Toe')
                for event in self.pygame.event.get():
                        if event.type == QUIT:
                                self.pygame.quit()
                                sys.exit()
                        self.pygame.display.update()

                self.p1_moves.append(move) if draw == 'X' else self.p2_moves.append(move)
                for move_x_i, move_x_j in self.p1_moves:
                        self.draw_x(move_x_i, move_x_j)
                for move_o_i, move_o_j in self.p2_moves:
                        self.draw_o(move_o_i, move_o_j)

                self.pygame.display.update()

        def winner(self, coordinates, winner):
                x1, y1, x2, y2 = coordinates
                self.pygame.draw.line(self.display, self.GRAY, (50 + y1 * 100, 150 + x1 * 100), (50 + y2 * 100, 150 + x2 * 100), 5)
                self.pygame.draw.line(self.display, self.WHITE, (55 + y1 * 100, 150 + x1 * 100), (55 + y2 * 100, 150 + x2 * 100), 5)

                pygame.font.init()

                font = pygame.font.SysFont('Comic Sans MS', 20)
                if winner == 1:
                        text_surface = font.render('P1 won', False, self.WHITE)
                        self.display.blit(text_surface, (120,50))
                elif winner == -1:
                        text_surface = font.render('P2 won', False, self.WHITE)
                        self.display.blit(text_surface, (120,50))
                else:
                        text_surface = font.render('Draw', False, self.WHITE)
                        self.display.blit(text_surface, (120,50))

                self.pygame.display.update()

        def reset(self, p1_score, p2_score, round):
                self.display.fill(self.BLACK)
                self.p1_moves = []
                self.p2_moves = []

                self.pygame.draw.line(self.display, self.WHITE, (0, 100), (0, 400), 5)
                self.pygame.draw.line(self.display, self.WHITE, (100, 100), (100, 400), 5)
                self.pygame.draw.line(self.display, self.WHITE, (200, 100), (200, 400), 5)
                self.pygame.draw.line(self.display, self.WHITE, (298, 100), (298, 400), 5)
                self.pygame.draw.line(self.display, self.WHITE, (0, 100), (300, 100), 5)
                self.pygame.draw.line(self.display, self.WHITE, (0, 200), (300, 200), 5)
                self.pygame.draw.line(self.display, self.WHITE, (0, 300), (300, 300), 5)
                self.pygame.draw.line(self.display, self.WHITE, (0, 398), (300, 398), 5)

                pygame.font.init()

                font = pygame.font.SysFont('Comic Sans MS', 20)
                text_surface = font.render(f'P1: {p1_score}', False, self.WHITE)
                self.display.blit(text_surface, (20,0))
                text_surface = font.render(f'P2: {p2_score}', False, self.WHITE)
                self.display.blit(text_surface, (230,0))
                text_surface = font.render(f'R: {round}', False, self.WHITE)
                self.display.blit(text_surface, (120,0))

                self.pygame.display.update()
