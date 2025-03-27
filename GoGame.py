class GoGame:
    def __init__(self, board_size=19):
        self.board_size = board_size
        self.board = [['.' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'B'  # 'B' for black, 'W' for white

    def get_group(self, row, col):
        """Return the group of connected stones of the same color starting at (row, col) and their liberties."""
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

    def apply_move(self, move):
        if move == 'pass':
            # Pass move; you might want to handle passes separately.
            self.current_player = 'W' if self.current_player == 'B' else 'B'
            return

        row, col = move
        if self.board[row][col] != '.':
            raise ValueError("Invalid move: spot taken")

        # Place the stone.
        self.board[row][col] = self.current_player

        # Identify opponent color.
        opponent = 'B' if self.current_player == 'W' else 'W'

        # For each neighbor, if it's an opponent stone, check if its group has any liberties.
        for nr, nc in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
            if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                if self.board[nr][nc] == opponent:
                    group, liberties = self.get_group(nr, nc)
                    if not liberties:
                        # Remove all captured stones.
                        for r, c in group:
                            self.board[r][c] = '.'

        # Optionally, check for suicide: if the new stone's group now has no liberties (should not happen in legal play),
        # you might want to revert the move. For now, we'll assume moves are legal.
        self.current_player = opponent
