class GoGame:
    def __init__(self, board_size=19):
        self.board_size = board_size
        self.board = [['.' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'B'
        self.moves = []  # Track moves in GTP format, e.g. ["B", "Q16"]

    def apply_move(self, move):
        # move is either 'pass' or a tuple (row, col)
        if move == 'pass':
            self.moves.append([self.current_player, "pass"])
            self.current_player = 'W' if self.current_player == 'B' else 'B'
            return

        row, col = move
        if self.board[row][col] != '.':
            raise ValueError("Invalid move: spot taken")
        self.board[row][col] = self.current_player
        # Convert the move from index to a GTP coordinate string.
        move_str = index_to_gtp(move, self.board_size)
        self.moves.append([self.current_player, move_str])
        # Check for captures here...
        opponent = 'W' if self.current_player == 'B' else 'B'
        for nr, nc in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            if 0 <= nr < self.board_size and 0 <= nc < self.board_size and self.board[nr][nc] == opponent:
                group, liberties = self.get_group(nr, nc)
                if not liberties:
                    for r, c in group:
                        self.board[r][c] = '.'
        self.current_player = opponent

    def get_group(self, row, col):
        color = self.board[row][col]
        group = set()
        liberties = set()
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            if (r, c) in group:
                continue
            group.add((r, c))
            for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
                if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                    if self.board[nr][nc] == '.':
                        liberties.add((nr, nc))
                    elif self.board[nr][nc] == color and (nr, nc) not in group:
                        stack.append((nr, nc))
        return group, liberties


def index_to_gtp(move, board_size=19):
    """
    Converts a move from (row, col) indices to a GTP coordinate string.
    For a 19x19 board, row 0 is the top row.
    """
    if move == 'pass':
        return 'pass'
    row, col = move
    number = board_size - row
    # Skip letter "I"
    if col >= 8:
        letter = chr(ord('A') + col + 1)
    else:
        letter = chr(ord('A') + col)
    return f"{letter}{number}"
