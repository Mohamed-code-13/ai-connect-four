from connect_4_solver.heuristic import Heuristic


class Expectiminimax:
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
            score -= Heuristic(state).calculate_heuristic('2' if player == '1' else '1')
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

                expected_score = 0
                # Simulate the move and calculate probabilities for the chosen column and neighbors
                neighbors = [c - 1, c + 1]
                for column, prob in [(c, 0.6)] + [(n, 0.2) for n in neighbors if 0 <= n < 7]:
                    new_state = self.simulate_move(state, column, player)
                    if new_state is None:  # Invalid move, skip it
                        continue
                    eval, _ = self.solve(new_state, depth - 1, alpha, beta,
                                         use_pruning, False, '2' if player == '1' else '1')
                    expected_score += prob * eval

                if expected_score > maxEval:
                    maxEval = expected_score
                    res = c

                self.tree[state]['children'].append((state, expected_score))

                alpha = max(alpha, expected_score)
                if use_pruning and alpha >= beta:
                    break

            self.tree[state]['score'] = maxEval
            return maxEval, res
        else:
            minEval = float('inf')
            for c in range(7):
                if state[c] != '0':
                    continue

                expected_score = 0
                neighbors = [c - 1, c + 1]
                for column, prob in [(c, 0.6)] + [(n, 0.2) for n in neighbors if 0 <= n < 7]:
                    new_state = self.simulate_move(state, column, player)
                    if new_state is None:
                        continue
                    eval, _ = self.solve(new_state, depth - 1, alpha, beta,
                                         use_pruning, True, '2' if player == '1' else '1')
                    expected_score += prob * eval

                if expected_score < minEval:
                    minEval = expected_score
                    res = c

                self.tree[state]['children'].append((state, expected_score))

                beta = min(beta, expected_score)
                if use_pruning and alpha >= beta:
                    break

            self.tree[state]['score'] = minEval
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
        return None
