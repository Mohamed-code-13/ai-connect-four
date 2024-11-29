class Heuristic:
    def __init__(self, board):
        self.board = board
        self.rows = 6
        self.cols = 7

    def calculate_heuristic(self, player):
        score = 0

        score += self.evaluate_rows(player)
        score += self.evaluate_columns(player)
        score += self.evaluate_positive_diagonal(player)
        score += self.evaluate_negative_diagonal(player)

        return score

    def evaluate_rows(self, player):
        score = 0
        for r in range(self.rows):
            slice = self.board[r * self.cols: (r + 1) * self.cols]
            score += self.evaluate_slice(slice, player)
        return score

    def evaluate_columns(self, player):
        score = 0
        for c in range(self.cols):
            slice = []
            for r in range(self.rows):
                slice.append(self.board[r * self.cols + c])

            slice = ''.join(slice)
            score += self.evaluate_slice(slice, player)

        return score

    def evaluate_positive_diagonal(self, player):
        score = 0
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                slice = []
                for i in range(4):
                    slice.append(self.board[(r + i) * self.cols + (c + i)])

                slice = ''.join(slice)
                score += self.evaluate_slice(slice, player)

        return score

    def evaluate_negative_diagonal(self, player):
        score = 0
        for r in range(self.rows - 3):
            for c in range(3, self.cols):
                slice = []
                for i in range(4):
                    slice.append(self.board[(r + i) * self.cols + (c - i)])

                slice = ''.join(slice)
                score += self.evaluate_slice(slice, player)

        return score

    def evaluate_slice(self, slice, player):
        score = 0
        for i in range(len(slice) - 3):
            sub_slice = slice[i: i + 4]
            score += self.evaluate_four(sub_slice, player)
        return score

    def evaluate_four(self, slice, player):
        opponent = '2' if player == '1' else '1'
        score = 0

        count = {
            '0': 0,
            '1': 0,
            '2': 0
        }

        for p in slice:
            count[p] += 1

        if count[opponent] > 0:
            score = 0
        elif count[player] == 4:
            score = 100000
        elif count[player] == 3:
            score = 1000
        elif count[player] == 2:
            score = 500
        elif count[player] == 1:
            score = 10
        return score


# board = (
#     "0002000"  # Top row
#     "0002000"
#     "0002200"
#     "0111210"  # Tokens start from here
#     "0212110"
#     "0112210"  # Bottom row
# )

# h = Heuristic(board)
# p1 = h.calculate_heuristic('1')
# p2 = h.calculate_heuristic('2')

# print(f"P1 : {p1}")
# print(f"P2 : {p2}")
