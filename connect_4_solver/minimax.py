from connect_4_solver.heuristic import Heuristic


class MiniMax:
    def __init__(self):
        self.expanded_nodes = 0
        self.tree = {}

    def solve(self, state, depth, alpha, beta, use_pruning, maximizing, player):
        self.expanded_nodes += 1
        self.tree[state] = {
            'score': 0,
            'alpha': alpha,
            'beta': beta,
            'children': []
        }

        if depth == 0 or self.check_game_end(state):
            score = Heuristic(state).calculate_heuristic(player)
            score -= Heuristic(state).calculate_heuristic('2' if player ==
                                                          '1' else '1')
            if not maximizing:
                score *= -1
            self.tree[state]['score'] = score
            return score, 0

        res = 0
        if maximizing:
            maxEval = float('-inf')
            for c in range(7):
                if state[c] != '0':
                    continue
                if depth == 5 and c == 6:
                    pass
                new_state = self.simulate_move(state, c, player)
                eval, _ = self.solve(new_state, depth - 1, alpha, beta,
                                     use_pruning, False, '2' if player == '1' else '1')
                if eval > maxEval:
                    maxEval = eval
                    res = c

                alpha = max(alpha, eval)
                self.tree[state]['children'].append(
                    (new_state, eval, alpha, beta))

                if use_pruning and alpha >= beta:
                    break

            self.tree[state]['score'] = maxEval
            self.tree[state]['alpha'] = alpha
            self.tree[state]['beta'] = beta
            return maxEval, res
        else:
            minEval = float('inf')
            for c in range(7):
                if state[c] != '0':
                    continue
                new_state = self.simulate_move(state, c, player)
                eval, _ = self.solve(new_state, depth - 1, alpha, beta,
                                     use_pruning, True, '2' if player == '1' else '1')
                if eval < minEval:
                    minEval = eval
                    res = c

                beta = min(beta, eval)
                self.tree[state]['children'].append(
                    (new_state, eval, alpha, beta))

                if use_pruning and alpha >= beta:
                    break

            self.tree[state]['score'] = minEval
            self.tree[state]['alpha'] = alpha
            self.tree[state]['beta'] = beta
            return minEval, res

    def check_game_end(self, state):
        for i in state:
            if i == '0':
                return False
        return True

    def simulate_move(self, state, c, player):
        for r in range(5, -1, -1):
            if state[r * 7 + c] == '0':
                return state[:r * 7 + c] + player + state[r * 7 + c + 1:]
