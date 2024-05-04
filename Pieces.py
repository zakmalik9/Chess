from Piece import Piece


class Rook(Piece):
    def select(self, pieces, opposing_pieces, do_return):
        self.remove_states(pieces, opposing_pieces)
        self.selected = True
        self.rook_select(opposing_pieces)
        if do_return:
            return self.possible_positions


class Bishop(Piece):
    def select(self, pieces, opposing_pieces, do_return):
        self.remove_states(pieces, opposing_pieces)
        self.selected = True
        self.bishop_select(opposing_pieces)
        if do_return:
            return self.possible_positions


class Queen(Piece):
    def select(self, pieces, opposing_pieces, do_return):
        self.remove_states(pieces, opposing_pieces)
        self.selected = True
        self.rook_select(opposing_pieces)
        self.bishop_select(opposing_pieces)
        if do_return:
            return self.possible_positions


class Knight(Piece):
    def select(self, pieces, opposing_pieces, do_return):
        self.remove_states(pieces, opposing_pieces)
        self.selected = True
        self.knight_select(opposing_pieces)
        if do_return:
            return self.possible_positions


class Pawn(Piece):
    def select(self, pieces, opposing_pieces, do_return):
        self.remove_states(pieces, opposing_pieces)
        self.selected = True
        self.pawn_select(opposing_pieces)
        if do_return:
            return self.possible_positions


    def move(self, new_row, new_column):
        if self.selected:
            for position in self.possible_positions:
                if (new_row, new_column) == position:
                    if self.first_turn:
                        if self.type == "White" and new_row == 4:
                            self.en_passant = True
                        elif self.type == "Black" and new_row == 3:
                            self.en_passant = True
                    else:
                        self.en_passant = False
                    self.move_piece(new_row, new_column)
                    self.selected = False
                    self.has_moved = True
                    self.first_turn = False


class King(Piece):
    def select(self, pieces, opposing_pieces, do_return):
        self.remove_states(pieces, opposing_pieces)
        self.selected = True
        self.king_select(opposing_pieces)
        if do_return:
            return self.possible_positions
