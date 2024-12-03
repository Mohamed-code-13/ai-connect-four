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

        if depth <= 0 or self.check_game_end(state):
            # Calculate heuristic as the evaluation for terminal or leaf nodes
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

                # Initialize weights and track valid moves
                valid_moves = []
                weights = []

                # Main move (current column)
                new_state = self.simulate_move(state, c, player)
                valid_moves.append((new_state, 0.6, 'cur'))

                # Left move (c - 1)
                if c > 0 and state[c - 1] == '0':
                    left_state = self.simulate_move(state, c - 1, player)
                    valid_moves.append((left_state, 0.2, 'left'))

                # Right move (c + 1)
                if c < 6 and state[c + 1] == '0':
                    right_state = self.simulate_move(state, c + 1, player)
                    valid_moves.append((right_state, 0.2, 'right'))

                # Normalize weights based on valid moves
                total_weight = sum(weight for _, weight, _ in valid_moves)
                normalized_moves = [(state, weight / total_weight, dr)
                                    for state, weight, dr in valid_moves]

                # Calculate expected value
                expected_value = 0
                tmp = []
                for move_state, normalized_weight, dr in normalized_moves:
                    cur = normalized_weight * self.solve_single(
                        move_state, depth - 2, alpha, beta, use_pruning, False, '2' if player == '1' else '1'
                    )[0]
                    expected_value += cur
                    tmp.append((dr + ' - ' + str(normalized_weight)
                               [:4], f'{cur:.2f}'))

                if expected_value > maxEval:
                    maxEval = expected_value
                    res = c

                self.tree[state]['children'].append(
                    (new_state, expected_value, tmp))

                alpha = max(alpha, maxEval)
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

                valid_moves = []
                weights = []

                new_state = self.simulate_move(state, c, player)
                valid_moves.append((new_state, 0.6, 'cur'))

                # Left move (c - 1)
                if c > 0 and state[c - 1] == '0':
                    left_state = self.simulate_move(state, c - 1, player)
                    valid_moves.append((left_state, 0.2, 'left'))

                # Right move (c + 1)
                if c < 6 and state[c + 1] == '0':
                    right_state = self.simulate_move(state, c + 1, player)
                    valid_moves.append((right_state, 0.2, 'right'))

                # Normalize weights based on valid moves
                total_weight = sum(weight for _, weight, dr in valid_moves)
                normalized_moves = [(state, weight / total_weight, dr)
                                    for state, weight, dr in valid_moves]

                # Calculate expected value
                expected_value = 0
                tmp = []
                for move_state, normalized_weight, dr in normalized_moves:
                    cur = normalized_weight * self.solve_single(
                        move_state, depth - 2, alpha, beta, use_pruning, True, '2' if player == '1' else '1'
                    )[0]
                    expected_value += cur
                    tmp.append((dr + ' - ' + str(normalized_weight)[:4], cur))

                # Update best score and result
                if expected_value < minEval:
                    minEval = expected_value
                    res = c

                self.tree[state]['children'].append(
                    (new_state, expected_value, tmp))

                # Update beta and prune if needed
                beta = min(beta, minEval)
                if use_pruning and alpha >= beta:
                    break

            self.tree[state]['score'] = minEval
            self.tree[state]['alpha'] = alpha
            self.tree[state]['beta'] = beta
            return minEval, res

    def solve_single(self, state, depth, alpha, beta, use_pruning, maximizing, player):
        return self.solve(state, depth, alpha, beta, use_pruning, maximizing, player)

    def check_game_end(self, state):
        for i in state:
            if i == '0':
                return False
        return True

    def simulate_move(self, state, c, player):
        for r in range(5, -1, -1):
            if state[r * 7 + c] == '0':
                return state[:r * 7 + c] + player + state[r * 7 + c + 1:]
