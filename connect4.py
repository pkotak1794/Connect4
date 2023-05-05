# needs to be 9x7 grid size
# add valid moves function
# alpha-beta pruning algorithm 


from games import *
import copy

class GameState:
    def __init__(self, to_move, utility, board, moves=None):
        self.to_move = to_move
        self.utility = utility
        self.board = board
        self.moves = moves or []

class Connect4(Game):
    def __init__(self):
        self.cols = 9
        self.rows = 7
        self.win_length = 4
        self.board = {}
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[(row, col)] = "."
        self.initial = GameState(to_move='X', utility=0, board=self.board, moves=[])

    def to_game(self, state):
        game = Connect4()
        game.cols = self.cols
        game.rows = self.rows
        game.win_length = self.win_length
        game.initial = state
        return game
    
    def actions(self, state):
        return [(row, col) for row in range(self.rows) for col in range(self.cols)
                if state.board[(row, col)] == "."]

    def result(self, state, move):
        if move not in self.actions(state):
            return state
        row, col = move
        player = state.to_move
        new_board = copy.deepcopy(state.board)
        new_board[(row, col)] = player
        new_moves = state.moves + [move]
        new_to_move = 'O' if player == 'X' else 'X'
        new_state = GameState(to_move=new_to_move, utility=self.compute_utility(new_board, move, player),
                              board=new_board, moves=new_moves)
        return new_state

    def compute_utility(self, board, move, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        row, col = move
        for d in directions:
            count = 1
            for i in range(1, self.win_length):
                r, c = vector_add((row, col), (d[0]*i, d[1]*i))
                if (r, c) in board and board[(r, c)] == player:
                    count += 1
                else:
                    break
            for i in range(1, self.win_length):
                r, c = vector_add((row, col), (-d[0]*i, -d[1]*i))
                if (r, c) in board and board[(r, c)] == player:
                    count += 1
                else:
                    break
            if count >= self.win_length:
                return 1 if player == 'X' else -1
        if all(board[(r, c)] != '.' for r in range(self.rows) for c in range(self.cols)):
            return 0
        return None

    def utility(state, player, alpha_beta=None):
        board = state.board
        game = Connect4().to_game(state)
        for row in range(game.rows):
            for col in range(game.cols):
                if board[(row, col)] == '.':
                    continue
                for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                    r, c = row, col
                    seq = ''
                    while (0 <= r < game.rows and 0 <= c < game.cols and board[(r, c)] == board[(row, col)]):
                        seq += board[(r, c)]
                        r, c = r + dr, c + dc
                    if len(seq) >= game.win_length:
                        if seq[0] == player:
                            return 1
                        else:
                            return -1
        return 0


    def terminal_test(self, state):
        return state.utility is not None

    def display(self, state):
        board = state.board
        for row in range(self.rows):
            print(" | ", end="")
            for col in range(self.cols):
                print(board[(row, col)], end=" | ")
            print("")

c4 = Connect4()
# Set the initial state for the game
c4.initial = GameState(to_move='X', utility=0, board={}, moves=[])
for row in range(c4.rows):
    for col in range(c4.cols):
        c4.initial.board[(row, col)] = "."

if __name__ == "__main__":
    c4 = Connect4()
    # Set the initial state for the game
    c4.initial = GameState(to_move='X', utility=0, board={}, moves=[])
    for row in range(c4.rows):
        for col in range(c4.cols):
            c4.initial.board[(row, col)] = "."
    print(c4.initial.board)
    print(c4.initial.moves)
    # play the game using alpha-beta pruning algorithm
    utility = c4.play_game(alpha_beta_player, alpha_beta_player)
    print("Game over. Utility: ", utility)


