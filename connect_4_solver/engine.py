from connect_4_solver.minimax import MiniMax


class Engine:
    def __init__(self, board, depth=5, use_pruning=True):
        self.board = board
        self.depth = depth
        self.use_pruning = use_pruning
        self.rows = 6
        self.cols = 7
        self.minimax = MiniMax()
        self.score = {
            'Human': 0,
            'Computer': 0
        }

    def move(self, position, player, name):
        self.board = self.board[: position] + \
            player + self.board[position + 1:]
        self.update_score(position, name)

    def computer_move(self, player, name):
        print(self.depth, self.use_pruning)
        _, c = self.minimax.solve(self.board, self.depth, float('-inf'),
                                  float('inf'), self.use_pruning, True, player)
        pos = self.get_position(c)
        self.move(pos, player, name)
        return c

    def get_position(self, c):
        for r in range(self.rows - 1, -1, -1):
            if self.board[r * self.cols + c] == '0':
                return r * self.cols + c

    def update_score(self, position, player):
        self.score[player] += self.calc_score_horizontally(position)
        self.score[player] += self.calc_score_vertically(position)
        self.score[player] += self.calc_score_diagonally(position)
        print(self.score, player)

    def calc_score_horizontally(self, position):
        p = self.board[position]
        dirs = [
            (0, 3),
            (1, 2),
            (2, 1),
            (3, 0)
        ]
        connected = 0

        for dl, dr in dirs:
            c = 1
            for l in range(position - 1, position - dl - 1, -1):
                if position // self.cols != l // self.cols:
                    break
                if self.board[l] == p:
                    c += 1
                else:
                    break

            for r in range(position + 1, position + dr + 1):
                if position // self.cols != r // self.cols:
                    break
                if self.board[r] == p:
                    c += 1
                else:
                    break

            connected += c == 4

        return connected

    def calc_score_vertically(self, position):
        p = self.board[position]
        c = 0
        for i in range(position, min(len(self.board), position + 7 * 4), 7):
            if self.board[i] == p:
                c += 1
            else:
                break
        return c == 4

    def calc_score_diagonally(self, position):
        p = self.board[position]
        dirs = [
            (0, 3),
            (1, 2),
            (2, 1),
            (3, 0)
        ]
        connected = 0

        for dl, dr in dirs:
            c = 1
            for l in range(1, dl + 1):
                ix = position - (8 * l)
                if ix < 0 or position % self.cols != ix % self.cols + l:
                    break
                if self.board[ix] == p:
                    c += 1
                else:
                    break

            for r in range(1, dr + 1):
                ix = position + (8 * r)
                if ix >= len(self.board) or position % self.cols != ix % self.cols - r:
                    break
                if self.board[ix] == p:
                    c += 1
                else:
                    break

            connected += c == 4

        for dl, dr in dirs:
            c = 1
            for l in range(1, dl + 1):
                ix = position + (6 * l)
                if ix >= len(self.board) or position % self.cols != ix % self.cols + l:
                    break
                if self.board[ix] == p:
                    c += 1
                else:
                    break

            for r in range(1, dr + 1):
                ix = position - (6 * r)
                if ix < 0 or position % self.cols != ix % self.cols - r:
                    break
                if self.board[ix] == p:
                    c += 1
                else:
                    break

            connected += c == 4

        return connected

    def check_game_end(self):
        for i in self.board:
            if i == '0':
                return False
        return True

    def get_winner(self):
        if self.score['Human'] > self.score['Computer']:
            return 'Human Won!'
        elif self.score['Human'] < self.score['Computer']:
            return 'Computer Won!'
        return 'It\'s Tie!'
