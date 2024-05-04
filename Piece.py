class Piece:
    def __init__(self, piece_type, board, row_position, column_position, piece):
        self.type = piece_type
        self.board = board
        self.row_pos = row_position
        self.column_pos = column_position
        self.piece = piece
        self.board[self.row_pos][self.column_pos] = self.piece
        self.has_moved = False
        self.selected = False
        self.capturable = False
        self.captured = False
        self.possible_positions = []
        self.first_turn = True
        self.en_passant = True
        self.ep_position = (None, None)
        self.promote_pos = (None, None)
        self.check = False
        self.unavailable_positions = []
        self.qs_castle = False
        self.qsc_position = (None, None)
        self.ks_castle = False
        self.ksc_position = (None, None)


    def get_current_position(self):
        return self.row_pos, self.column_pos


    def remove_states(self, pieces, opposing_pieces):
        for piece in pieces:
            piece.selected = False
            piece.possible_positions = []
            piece.has_moved = False
        for opposing_piece in opposing_pieces:
            opposing_piece.capturable = False


    def move_piece(self, new_row, new_column):
        self.board[self.row_pos][self.column_pos] = 0
        self.row_pos = new_row
        self.column_pos = new_column
        self.board[self.row_pos][self.column_pos] = self.piece


    def move(self, new_row, new_column):
        if self.selected:
            for position in self.possible_positions:
                if (new_row, new_column) == position:
                    self.move_piece(new_row, new_column)
                    self.selected = False
                    self.has_moved = True
                    self.first_turn = False


    def rook_select(self, opposing_list):
        # left line
        x = 1
        while self.column_pos - x >= 0 and self.board[self.row_pos][self.column_pos - x] == 0:
            self.possible_positions.append((self.row_pos, self.column_pos - x))
            x += 1
        for piece in opposing_list:
            r, c = piece.get_current_position()
            if r == self.row_pos and c == self.column_pos - x:
                piece.capturable = True
                self.possible_positions.append((r, c))
        # right line
        x = 1
        while self.column_pos + x <= 7 and self.board[self.row_pos][self.column_pos + x] == 0:
            self.possible_positions.append((self.row_pos, self.column_pos + x))
            x += 1
        for piece in opposing_list:
            r, c = piece.get_current_position()
            if r == self.row_pos and c == self.column_pos + x:
                piece.capturable = True
                self.possible_positions.append((r, c))
        # forward line
        x = 1
        while self.row_pos - x >= 0 and self.board[self.row_pos - x][self.column_pos] == 0:
            self.possible_positions.append((self.row_pos - x, self.column_pos))
            x += 1
        for piece in opposing_list:
            r, c = piece.get_current_position()
            if r == self.row_pos - x and c == self.column_pos:
                piece.capturable = True
                self.possible_positions.append((r, c))
        # backward line
        x = 1
        while self.row_pos + x <= 7 and self.board[self.row_pos + x][self.column_pos] == 0:
            self.possible_positions.append((self.row_pos + x, self.column_pos))
            x += 1
        for piece in opposing_list:
            r, c = piece.get_current_position()
            if r == self.row_pos + x and c == self.column_pos:
                piece.capturable = True
                self.possible_positions.append((r, c))


    def bishop_select(self, opposing_list):
        # left-forward diagonal
        x = 1
        while self.row_pos - x >= 0 and self.column_pos - x >= 0 \
                and self.board[self.row_pos - x][self.column_pos - x] == 0:
            self.possible_positions.append((self.row_pos - x, self.column_pos - x))
            x += 1
        for piece in opposing_list:
            r, c = piece.get_current_position()
            if r == self.row_pos - x and c == self.column_pos - x:
                piece.capturable = True
                self.possible_positions.append((r, c))
        # right-forward diagonal
        x = 1
        while self.row_pos - x >= 0 and self.column_pos + x <= 7 \
                and self.board[self.row_pos - x][self.column_pos + x] == 0:
            self.possible_positions.append((self.row_pos - x, self.column_pos + x))
            x += 1
        for piece in opposing_list:
            r, c = piece.get_current_position()
            if r == self.row_pos - x and c == self.column_pos + x:
                piece.capturable = True
                self.possible_positions.append((r, c))
        # left-backward diagonal
        x = 1
        while self.row_pos + x <= 7 and self.column_pos - x >= 0 \
                and self.board[self.row_pos + x][self.column_pos - x] == 0:
            self.possible_positions.append((self.row_pos + x, self.column_pos - x))
            x += 1
        for piece in opposing_list:
            r, c = piece.get_current_position()
            if r == self.row_pos + x and c == self.column_pos - x:
                piece.capturable = True
                self.possible_positions.append((r, c))
        # right-backward diagonal
        x = 1
        while self.row_pos + x <= 7 and self.column_pos + x <= 7 \
                and self.board[self.row_pos + x][self.column_pos + x] == 0:
            self.possible_positions.append((self.row_pos + x, self.column_pos + x))
            x += 1
        for piece in opposing_list:
            r, c = piece.get_current_position()
            if r == self.row_pos + x and c == self.column_pos + x:
                piece.capturable = True
                self.possible_positions.append((r, c))


    def knight_select(self, opposing_pieces):
        positions = [
            self.row_pos - 1,
            self.column_pos - 2,
            self.row_pos + 1,
            self.column_pos - 2,
            self.row_pos - 2,
            self.column_pos - 1,
            self.row_pos - 2,
            self.column_pos + 1,
            self.row_pos - 1,
            self.column_pos + 2,
            self.row_pos + 1,
            self.column_pos + 2,
            self.row_pos + 2,
            self.column_pos - 1,
            self.row_pos + 2,
            self.column_pos + 1
        ]
        x = 0
        while x + 2 <= len(positions):
            if 0 <= positions[x] <= 7 and 0 <= positions[x+1] <= 7 \
                    and self.board[positions[x]][positions[x+1]] == 0:
                self.possible_positions.append((positions[x], positions[x+1]))
            for piece in opposing_pieces:
                r, c = piece.get_current_position()
                if r == positions[x] and c == positions[x+1]:
                    piece.capturable = True
                    self.possible_positions.append((r, c))
            x += 2


    def pawn_select(self, opposing_pieces):
        if self.type == "White":
            if self.row_pos - 1 >= 0 and self.board[self.row_pos - 1][self.column_pos] == 0:
                self.possible_positions.append((self.row_pos - 1, self.column_pos))
                if self.row_pos - 1 == 0:
                    self.promote_pos = (self.row_pos - 1, self.column_pos)
                if self.first_turn:
                    if self.board[self.row_pos - 2][self.column_pos] == 0:
                        self.possible_positions.append((self.row_pos - 2, self.column_pos))
            for piece in opposing_pieces:
                r, c = piece.get_current_position()
                if r == self.row_pos - 1 and (c == self.column_pos - 1 or c == self.column_pos + 1):
                    piece.capturable = True
                    self.possible_positions.append((r, c))
        elif self.type == "Black":
            if self.row_pos + 1 <= 7 and self.board[self.row_pos + 1][self.column_pos] == 0:
                self.possible_positions.append((self.row_pos + 1, self.column_pos))
                if self.row_pos + 1 == 7:
                    self.promote_pos = (self.row_pos + 1, self.column_pos)
                if self.first_turn:
                    if self.board[self.row_pos + 2][self.column_pos] == 0:
                        self.possible_positions.append((self.row_pos + 2, self.column_pos))
            for piece in opposing_pieces:
                r, c = piece.get_current_position()
                if r == self.row_pos + 1 and (c == self.column_pos - 1 or c == self.column_pos + 1):
                    piece.capturable = True
                    self.possible_positions.append((r, c))
        for piece in opposing_pieces:
            r, c = piece.get_current_position()
            if piece.en_passant and r == self.row_pos and (c == self.column_pos - 1 or c == self.column_pos + 1):
                if self.type == "White":
                    if self.board[r - 1][c] == 0:
                        self.ep_position = (r - 1, c)
                        self.possible_positions.append((r - 1, c))
                elif self.type == "Black":
                    if self.board[r + 1][c] == 0:
                        self.ep_position = (r + 1, c)
                        self.possible_positions.append((r + 1, c))


    def king_select(self, opposing_pieces):
        positions = [
            self.row_pos,
            self.column_pos - 1,
            self.row_pos - 1,
            self.column_pos - 1,
            self.row_pos - 1,
            self.column_pos,
            self.row_pos - 1,
            self.column_pos + 1,
            self.row_pos,
            self.column_pos + 1,
            self.row_pos + 1,
            self.column_pos + 1,
            self.row_pos + 1,
            self.column_pos,
            self.row_pos + 1,
            self.column_pos - 1
        ]
        x = 0
        attack = False
        while x + 2 <= len(positions):
            if 0 <= positions[x] <= 7 and 0 <= positions[x + 1] <= 7 \
                    and self.board[positions[x]][positions[x + 1]] == 0:
                for pos in self.unavailable_positions:
                    if pos == (positions[x], positions[x + 1]):
                        attack = True
                if not attack:
                    self.possible_positions.append((positions[x], positions[x + 1]))
            attack = False
            for piece in opposing_pieces:
                r, c = piece.get_current_position()
                if r == positions[x] and c == positions[x + 1]:
                    for pos in self.unavailable_positions:
                        if pos == (positions[x], positions[x + 1]):
                            attack = True
                    if not attack:
                        piece.capturable = True
                        self.possible_positions.append((positions[x], positions[x + 1]))
            x += 2
        if self.qs_castle:
            self.qsc_position = (self.row_pos, self.column_pos - 2)
            self.possible_positions.append((self.row_pos, self.column_pos - 2))
        if self.ks_castle:
            self.ksc_position = (self.row_pos, self.column_pos + 2)
            self.possible_positions.append((self.row_pos, self.column_pos + 2))
