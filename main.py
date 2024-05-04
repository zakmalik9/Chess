import pygame
import math
import copy
from Board import Board
from Pieces import Rook
from Pieces import Bishop
from Pieces import Queen
from Pieces import Knight
from Pieces import Pawn
from Pieces import King
from GameState import GameState

pygame.init()
# Game Variables
screen_size = 800
row_column_count = 8
cell_size = 100
screen = pygame.display.set_mode((screen_size, screen_size))
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Chess")
images = {
    1: "images/whiterook.png",
    2: "images/blackrook.png",
    3: "images/whiteknight.png",
    4: "images/blackknight.png",
    5: "images/whitebishop.png",
    6: "images/blackbishop.png",
    7: "images/whitequeen.png",
    8: "images/blackqueen.png",
    9: "images/whiteking.png",
    10: "images/blackking.png",
    11: "images/whitepawn.png",
    12: "images/blackpawn.png"
}
b = Board(screen, cell_size, row_column_count)
board = b.create_board()
turn = 0
white_turn = 0
black_turn = 1
winner = None
# White
white_rook1 = Rook("White", board, 7, 0, 1)
white_rook2 = Rook("White", board, 7, 7, 1)
white_knight1 = Knight("White", board, 7, 1, 3)
white_knight2 = Knight("White", board, 7, 6, 3)
white_bishop1 = Bishop("White", board, 7, 2, 5)
white_bishop2 = Bishop("White", board, 7, 5, 5)
white_queen = Queen("White", board, 7, 3, 7)
white_king = King("White", board, 7, 4, 9)
white_pawn1 = Pawn("White", board, 6, 0, 11)
white_pawn2 = Pawn("White", board, 6, 1, 11)
white_pawn3 = Pawn("White", board, 6, 2, 11)
white_pawn4 = Pawn("White", board, 6, 3, 11)
white_pawn5 = Pawn("White", board, 6, 4, 11)
white_pawn6 = Pawn("White", board, 6, 5, 11)
white_pawn7 = Pawn("White", board, 6, 6, 11)
white_pawn8 = Pawn("White", board, 6, 7, 11)
white_pieces = [white_rook1, white_rook2, white_knight1, white_knight2, white_bishop1, white_bishop2, white_queen,
                white_king, white_pawn1, white_pawn2, white_pawn3, white_pawn4, white_pawn5, white_pawn6,
                white_pawn7, white_pawn8]
# Black
black_rook1 = Rook("Black", board, 0, 0, 2)
black_rook2 = Rook("Black", board, 0, 7, 2)
black_knight1 = Knight("Black", board, 0, 1, 4)
black_knight2 = Knight("Black", board, 0, 6, 4)
black_bishop1 = Bishop("Black", board, 0, 2, 6)
black_bishop2 = Bishop("Black", board, 0, 5, 6)
black_queen = Queen("Black", board, 0, 3, 8)
black_king = King("Black", board, 0, 4, 10)
black_pawn1 = Pawn("Black", board, 1, 0, 12)
black_pawn2 = Pawn("Black", board, 1, 1, 12)
black_pawn3 = Pawn("Black", board, 1, 2, 12)
black_pawn4 = Pawn("Black", board, 1, 3, 12)
black_pawn5 = Pawn("Black", board, 1, 4, 12)
black_pawn6 = Pawn("Black", board, 1, 5, 12)
black_pawn7 = Pawn("Black", board, 1, 6, 12)
black_pawn8 = Pawn("Black", board, 1, 7, 12)
black_pieces = [black_rook1, black_rook2, black_knight1, black_knight2, black_bishop1, black_bishop2, black_queen,
                black_king, black_pawn1, black_pawn2, black_pawn3, black_pawn4, black_pawn5, black_pawn6,
                black_pawn7, black_pawn8]


def king_manager(own_king, pieces, oppose_pieces):
    own_pieces = []
    for piece in pieces:
        copy_piece = copy.deepcopy(piece)
        own_pieces.append(copy_piece)
    opposing_pieces = []
    for opp_piece in oppose_pieces:
        copy_opp_piece = copy.deepcopy(opp_piece)
        opposing_pieces.append(copy_opp_piece)
    opposing_positions = GameState.get_pieces_possible_positions(own_pieces, opposing_pieces)
    own_king.unavailable_positions = opposing_positions
    r, c = own_king.get_current_position()
    own_king.check = False
    for pos in opposing_positions:
        if (r, c) == pos:
            own_king.check = True
    own_positions = GameState.get_pieces_possible_positions(opposing_pieces, own_pieces)
    global winner
    if (own_king.check and len(own_positions) == 0) or own_king.captured:
        if own_king.type == "White":
            winner = "Black"
        elif own_king.type == "Black":
            winner = "White"
    elif not own_king.check and len(own_positions) == 0:
        winner = "Draw"


def check_for_pawn_promotion(piece_type, promote_row, piece_list, board_piece):
    for piece in piece_list:
        if isinstance(piece, Pawn):
            if piece.type == piece_type and piece.row_pos == promote_row:
                piece.piece = 0
                piece_list.remove(piece)
                new_piece = Queen(piece_type, board, piece.row_pos, piece.column_pos, board_piece)
                piece_list.append(new_piece)


def check_for_castling(brd, queenside_rook, king, kingside_rook, own_pieces, opposing_pieces):
    positions = GameState.get_pieces_possible_positions(own_pieces, opposing_pieces)
    r, c = king.get_current_position()
    king.qs_castle = False
    king.ks_castle = False
    attack_qs = False
    attack_ks = False
    # Queenside Check
    if king.first_turn and queenside_rook.first_turn:
        for position in positions:
            if (r, c) == position or (r, c - 1) == position or (r, c - 2) == position:
                attack_qs = True
        if not attack_qs and brd[r][c - 1] == 0 and brd[r][c - 2] == 0:
            king.qs_castle = True
    # Kingside Check
    if king.first_turn and kingside_rook.first_turn:
        for position in positions:
            if (r, c) == position or (r, c + 1) == position or (r, c + 2) == position:
                attack_ks = True
        if not attack_ks and brd[r][c + 1] == 0 and brd[r][c + 2] == 0:
            king.ks_castle = True


def game_manager(pieces, opposing_pieces, row, column, queenside_rook, kingside_rook, king):
    for piece in pieces:
        if piece.selected:
            for opposing_piece in opposing_pieces:
                if opposing_piece.en_passant:
                    if piece.ep_position == (row, column):
                        opposing_piece.captured = True
                        opposing_piece.piece = 0
                        opposing_pieces.remove(opposing_piece)
                        if piece.type == "White":
                            piece.move_piece(row + 1, column)
                        elif piece.type == "Black":
                            piece.move_piece(row - 1, column)
                        break
                if opposing_piece.capturable:
                    if opposing_piece.row_pos == row and opposing_piece.column_pos == column:
                        opposing_piece.captured = True
                        opposing_piece.piece = 0
                        opposing_pieces.remove(opposing_piece)
                        break
                opposing_piece.en_passant = False
            if isinstance(piece, King):
                if piece.qs_castle and (row, column) == piece.qsc_position:
                    queenside_rook.move_piece(row, column + 1)
                    piece.qsc_position = (None, None)
                elif piece.ks_castle and (row, column) == piece.ksc_position:
                    kingside_rook.move_piece(row, column - 1)
                    piece.ksc_position = (None, None)
            piece.move(row, column)
            if piece.has_moved:
                piece.remove_states(pieces, opposing_pieces)
                global turn
                turn += 1
                turn %= 2
                break
        if piece.row_pos == row and piece.column_pos == column:
            piece.select(pieces, opposing_pieces, False)
            break


def update_board(brd, image_list, pieces, opposing_pieces):
    b.draw_board()
    b.draw_states(pieces, opposing_pieces)
    b.draw_pieces(brd, image_list)


# Main Game Loop
game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_column = math.floor(event.pos[0] / 100)
            clicked_row = math.floor(event.pos[1] / 100)
            if game_running and turn == white_turn:
                check_for_castling(board, white_rook1, white_king, white_rook2, white_pieces, black_pieces)
                game_manager(white_pieces, black_pieces, clicked_row, clicked_column, white_rook1, white_rook2, white_king)
                check_for_pawn_promotion("White", 0, white_pieces, 7)
            elif game_running and turn == black_turn:
                check_for_castling(board, black_rook1, black_king, black_rook2, black_pieces, white_pieces)
                game_manager(black_pieces, white_pieces, clicked_row, clicked_column, black_rook1, black_rook2, black_king)
                check_for_pawn_promotion("Black", 7, black_pieces, 8)
    king_manager(white_king, white_pieces, black_pieces)
    king_manager(black_king, black_pieces, white_pieces)
    if turn == white_turn:
        update_board(board, images, white_pieces, black_pieces)
    elif turn == black_turn:
        update_board(board, images, black_pieces, white_pieces)
    if winner is not None:
        game_running = False
    pygame.display.update()


def display_win_text():
    white = (255, 255, 255)
    black = (0, 0, 0)
    grey = (128, 128, 128)
    font = pygame.font.SysFont("monospace", 100)
    label = font.render("", 1, white)
    if winner == "White":
        label = font.render("White Wins", 1, white)
    elif winner == "Black":
        label = font.render("Black Wins", 1, black)
    elif winner == "Draw":
        label = font.render("Game Drawn", 1, grey)
    screen.blit(label, (85, 315))


over_running = True
while over_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            over_running = False
    display_win_text()
    pygame.display.update()
