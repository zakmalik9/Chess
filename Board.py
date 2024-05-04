import pygame
import numpy as np


class Board:
    def __init__(self, screen, cell_size, row_column_count):
        self.screen = screen
        self.cell = cell_size
        self.rc_count = row_column_count


    def create_board(self):
        board = np.zeros((self.rc_count, self.rc_count))
        return board


    def draw_board(self):
        dark_square = (209, 139, 71)
        light_square = (255, 206, 158)
        x = 0
        for c in range(self.rc_count):
            for r in range(self.rc_count):
                if r % 2 == 0:
                    x = 0
                elif r % 2 == 1:
                    x = 1
                if c % 2 == x:
                    pygame.draw.rect(self.screen, light_square, (c * self.cell, r * self.cell, self.cell, self.cell))
                elif c % 2 != x:
                    pygame.draw.rect(self.screen, dark_square, (c * self.cell, r * self.cell, self.cell, self.cell))


    def draw_states(self, pieces, opposing_pieces):
        for piece in pieces:
            if piece.selected:
                row, column = piece.get_current_position()
                x = column * self.cell
                y = row * self.cell
                black = (0, 0, 0)
                pygame.draw.rect(self.screen, black, (x, y, self.cell, self.cell), 5)
                for c in range(self.rc_count):
                    for r in range(self.rc_count):
                        for position in piece.possible_positions:
                            if (r, c) == position:
                                x = c * self.cell
                                y = r * self.cell
                                yellow = (255, 255, 0)
                                purple = (128, 0, 128)
                                pygame.draw.rect(self.screen, yellow, (x, y, self.cell, self.cell))
                                if position == piece.ep_position or position == piece.promote_pos \
                                        or position == piece.qsc_position or position == piece.ksc_position:
                                    pygame.draw.rect(self.screen, purple, (x, y, self.cell, self.cell))
            if piece.check:
                r, c = piece.get_current_position()
                offset = self.cell // 2
                x = c * self.cell + offset
                y = r * self.cell + offset
                radius = offset - 5
                red = (255, 0, 0)
                pygame.draw.circle(self.screen, red, (x, y), radius)
        for opposing_piece in opposing_pieces:
            if opposing_piece.capturable:
                row, column = opposing_piece.get_current_position()
                x = column * self.cell
                y = row * self.cell
                red = (255, 0, 0)
                pygame.draw.rect(self.screen, red, (x, y, self.cell, self.cell))


    def draw_pieces(self, board, image_dictionary):
        for c in range(self.rc_count):
            for r in range(self.rc_count):
                for x in range(1, len(image_dictionary) + 1):
                    if board[r][c] == x:
                        image = pygame.image.load(image_dictionary[x])
                        self.screen.blit(image, (c * self.cell, r * self.cell))
