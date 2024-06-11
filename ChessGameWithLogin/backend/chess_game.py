class ChessPiece:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __str__(self):
        return f"{self.color[0]}{self.name[0]}"

class ChessGame:
    def __init__(self):
        self.board = self.initialize_board()
        self.turn = 'white'  # White goes first
        self.move_log = []
        self.kings = {'white': (7, 4), 'black': (0, 4)}  # Initial positions of kings
        self.en_passant_target = None  # Target for en passant capture

    def initialize_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]

        # Add pawns
        for i in range(8):
            board[1][i] = ChessPiece('Pawn', 'black')
            board[6][i] = ChessPiece('Pawn', 'white')

        # Add other pieces
        placement = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook']
        for i, piece in enumerate(placement):
            board[0][i] = ChessPiece(piece, 'black')
            board[7][i] = ChessPiece(piece, 'white')

        return board

    def print_board(self):
        for row in self.board:
            print(' '.join([str(piece) if piece else '.' for piece in row]))

    def move_piece(self, start_pos, end_pos):
        start_x, start_y = start_pos
        end_x, end_y = end_pos

        piece = self.board[start_x][start_y]
        target_piece = self.board[end_x][end_y]

        if not piece:
            raise ValueError("No piece at start position")
        if piece.color != self.turn:
            raise ValueError(f"It is {self.turn}'s turn")

        if self.is_valid_move(piece, start_pos, end_pos):
            # Make the move
            self.board[end_x][end_y] = piece
            self.board[start_x][start_y] = None
            self.move_log.append((start_pos, end_pos, str(piece)))

            # Update king's position if moved
            if piece.name == 'King':
                self.kings[piece.color] = (end_x, end_y)

            # Handle en passant capture
            if piece.name == 'Pawn' and self.en_passant_target and (end_x, end_y) == self.en_passant_target:
                self.board[start_x][end_y] = None  # Remove the captured pawn
                self.en_passant_target = None

            # Handle pawn promotion
            if piece.name == 'Pawn' and end_x in (0, 7):
                self.board[end_x][end_y] = ChessPiece('Queen', piece.color)  # Promote to Queen for simplicity

            # Set en passant target
            if piece.name == 'Pawn' and abs(end_x - start_x) == 2:
                self.en_passant_target = (start_x + (end_x - start_x) // 2, start_y)
            else:
                self.en_passant_target = None

            # Switch turn
            self.turn = 'black' if self.turn == 'white' else 'white'

            # Check for checkmate
            if self.is_in_checkmate('black' if self.turn == 'white' else 'white'):
                print(f"Checkmate! {self.turn.capitalize()} wins the game.")
        else:
            raise ValueError("Invalid move")

    def is_valid_move(self, piece, start_pos, end_pos):
        if piece.name == 'Pawn':
            return self.is_valid_pawn_move(piece, start_pos, end_pos)
        elif piece.name == 'Knight':
            return self.is_valid_knight_move(piece, start_pos, end_pos)
        elif piece.name == 'Bishop':
            return self.is_valid_bishop_move(piece, start_pos, end_pos)
        elif piece.name == 'Rook':
            return self.is_valid_rook_move(piece, start_pos, end_pos)
        elif piece.name == 'Queen':
            return self.is_valid_queen_move(piece, start_pos, end_pos)
        elif piece.name == 'King':
            return self.is_valid_king_move(piece, start_pos, end_pos) or self.is_valid_castling(piece, start_pos, end_pos)

        return False

    def is_valid_pawn_move(self, piece, start_pos, end_pos):
        start_x, start_y = start_pos
        end_x, end_y = end_pos

        # Basic forward moves
        if piece.color == 'white':
            if start_x == 6 and end_x == 4 and start_y == end_y and not self.board[end_x][end_y]:
                return True
            if end_x == start_x - 1 and start_y == end_y and not self.board[end_x][end_y]:
                return True
        elif piece.color == 'black':
            if start_x == 1 and end_x == 3 and start_y == end_y and not self.board[end_x][end_y]:
                return True
            if end_x == start_x + 1 and start_y == end_y and not self.board[end_x][end_y]:
                return True

        # Capturing
        if piece.color == 'white' and end_x == start_x - 1 and abs(end_y - start_y) == 1 and self.board[end_x][end_y] and self.board[end_x][end_y].color == 'black':
            return True
        if piece.color == 'black' and end_x == start_x + 1 and abs(end_y - start_y) == 1 and self.board[end_x][end_y] and self.board[end_x][end_y].color == 'white':
            return True

        # En Passant
        if piece.color == 'white' and (end_x, end_y) == self.en_passant_target and abs(end_y - start_y) == 1 and end_x == start_x - 1:
            return True
        if piece.color == 'black' and (end_x, end_y) == self.en_passant_target and abs(end_y - start_y) == 1 and end_x == start_x + 1:
            return True

        return False

    def is_valid_knight_move(self, piece, start_pos, end_pos):
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)
        return (dx, dy) in [(2, 1), (1, 2)]

    def is_valid_bishop_move(self, piece, start_pos, end_pos):
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)
        if dx == dy:
            return self.is_path_clear(start_pos, end_pos)
        return False

    def is_valid_rook_move(self, piece, start_pos, end_pos):
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        if start_x == end_x or start_y == end_y:
            return self.is_path_clear(start_pos, end_pos)
        return False

    def is_valid_queen_move(self, piece, start_pos, end_pos):
        return self.is_valid_rook_move(piece, start_pos, end_pos) or self.is_valid_bishop_move(piece, start_pos, end_pos)

    def is_valid_king_move(self, piece, start_pos, end_pos):
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)
        return max(dx, dy) == 1

    def is_valid_castling(self, piece, start_pos, end_pos):
        start_x, start_y = start_pos
        end_x, end_y = end_pos

        if piece.name != 'King' or start_y != 4 or start_x not in (0, 7):
            return False

        if abs(end_y - start_y) == 2 and start_x == end_x:
            rook_start_y = 7 if end_y > start_y else 0
            rook = self.board[start_x][rook_start_y]
            if rook and rook.name == 'Rook' and rook.color == piece.color:
                if all(not self.board[start_x][y] for y in range(min(start_y, end_y) + 1, max(start_y, end_y))):
                    if not self.is_in_check(piece.color) and not self.is_castle_through_check(start_pos, end_pos):
                        # Move the rook as well
                        self.board[start_x][(start_y + end_y) // 2] = rook
                        self.board[start_x][rook_start_y] = None
                        return True
        return False

    def is_castle_through_check(self, start_pos, end_pos):
        start_x, start_y = start_pos
        end_x, end_y = end_pos

        mid_y = (start_y + end_y) // 2
        return self.is_attacked((start_x, mid_y), 'black' if self.turn == 'white' else 'white') or self.is_attacked(end_pos, 'black' if self.turn == 'white' else 'white')

    def is_path_clear(self, start_pos, end_pos):
        start_x, start_y = start_pos
        end_x, end_y = end_pos

        if start_x == end_x:
            step_y = 1 if start_y < end_y else -1
            for y in range(start_y + step_y, end_y, step_y):
                if self.board[start_x][y]:
                    return False

        elif start_y == end_y:
            step_x = 1 if start_x < end_x else -1
            for x in range(start_x + step_x, end_x, step_x):
                if self.board[x][start_y]:
                    return False

        else:
            step_x = 1 if start_x < end_x else -1
            step_y = 1 if start_y < end_y else -1
            x, y = start_x + step_x, start_y + step_y
            while x != end_x and y != end_y:
                if self.board[x][y]:
                    return False
                x += step_x
                y += step_y

        return not self.board[end_x][end_y] or self.board[end_x][end_y].color != self.board[start_x][start_y].color

    def is_in_check(self, color):
        king_position = self.kings[color]
        opponent_color = 'black' if color == 'white' else 'white'
        return self.is_attacked(king_position, opponent_color)

    def find_king(self, color):
        for x in range(8):
            for y in range(8):
                if self.board[x][y] and self.board[x][y].name == 'King' and self.board[x][y].color == color:
                    return (x, y)
        raise ValueError("King not found")

    def is_attacked(self, position, attacker_color):
        end_x, end_y = position
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece and piece.color == attacker_color:
                    if self.is_valid_move(piece, (x, y), position):
                        return True
        return False

    def is_in_checkmate(self, color):
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece and piece.color == color:
                    for end_x in range(8):
                        for end_y in range(8):
                            if self.is_valid_move(piece, (x, y), (end_x, end_y)):
                                # Temporarily make the move to check for check
                                target_piece = self.board[end_x][end_y]
                                self.board[end_x][end_y] = piece
                                self.board[x][y] = None
                                if not self.is_in_check(color):
                                    # Undo the move
                                    self.board[x][y] = piece
                                    self.board[end_x][end_y] = target_piece
                                    return False
                                # Undo the move
                                self.board[x][y] = piece
                                self.board[end_x][end_y] = target_piece
        return True