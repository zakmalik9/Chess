class GameState:
    @staticmethod
    def get_pieces_possible_positions(pieces, opposing_pieces):
        possible_positions = []
        for opposing_piece in opposing_pieces:
            temp_list = opposing_piece.select(opposing_pieces, pieces, True)
            for item in temp_list:
                possible_positions.append(item)
            opposing_piece.remove_states(opposing_pieces, pieces)
        new_list = list(dict.fromkeys(possible_positions))
        return new_list



