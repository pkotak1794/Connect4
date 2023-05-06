# needs to be 9x7 grid size
# add valid moves function
# alpha-beta pruning algorithm 


from games import GameState
from games import alpha_beta_player
from games import ConnectFour
from games import Game
import copy


class GameState:
    def __init__(self, to_move, utility, board, moves=None):
        self.to_move = to_move
        self.utility = utility
        self.board = board
        self.moves = moves or []

class ConnectFour(Game):
    def __init__(self):
        self.cols = 9
        self.rows = 7
        self.win_length = 4
        self.board = {(row, col): "." for row in range(self.rows) for col in range(self.cols)}
        self.initial = GameState(to_move='X', utility=0, board=self.board, moves=[])

    def to_game(self, state):
        game = ConnectFour()
        game.cols = self.cols
        game.rows = self.rows
        game.win_length = self.win_length
        game.initial = state
        return game
    
    def actions(self, state):
        return [(row, col) for row in range(self.rows) for col in range(self.cols)
            if state.board[(row, col)] == "." and (row == self.rows - 1 or state.board[(row+1, col)] != ".")]

    def result(self, state, row=None, col=None):
        if col not in range(self.cols):
            return state
        # find the lowest unoccupied row in the given column
        for r in range(self.rows-1, -1, -1):
            if state.board[(r, col)] == ".":
                break
        else: # column is full
            return state
        player = state.to_move
        new_board = copy.deepcopy(state.board)
        new_board[(r, col)] = player
        new_moves = state.moves + [(r, col)]
        new_to_move = 'O' if player == 'X' else 'X'
        new_state = GameState(to_move=new_to_move, utility=self.compute_utility(new_board, (r, col), player),
                              board=new_board, moves=new_moves)
        return new_state

    def compute_utility(self, board, move, player):
        if move is None:
            return None
        print(f"move: {move}")
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        row, col = move
        for d in directions:
            count = 1
            for i in range(1, self.win_length):
                r, c = row + d[0]*i, col + d[1]*i
                if r < 0 or r >= self.rows or c < 0 or c >= self.cols or board[(r, c)] != player:
                    break
                count += 1
            for i in range(1, self.win_length):
                r, c = row - d[0]*i, col - d[1]*i
                if r < 0 or r >= self.rows or c < 0 or c >= self.cols or board[(r, c)] != player:
                    break
                count += 1
            if count >= self.win_length:
                return 1 if player == 'X' else -1
            if all(board[(r, c)] != '.' for r in range(self.rows) for c in range(self.cols)):
                return 0
            else:
                return None

    def terminal_test(self, state):
        return state.utility is not None

    def to_move(self, state):
        return state.to_move

    def display(self, state):
        board = state.board
        for row in range(self.rows):
            print(" | ", end="")
            for col in range(self.cols):
                print(board[(row, col)], end=" | ")
            print("")


if __name__ == "__main__":
    c4 = ConnectFour()
    print(c4)
    board = {(row, col): "." for row in range(c4.rows) for col in range(c4.cols)}
    c4.initial = GameState(to_move='X', utility=c4.compute_utility(board, None, 'X'), board=board, moves=[])
    state = c4.initial
    while not c4.terminal_test(state):
        c4.display(state)
        if state.to_move == 'X':
            col = int(input("Enter column: "))
            state = c4.result(state, row=None,col=col)
        else:
            state = alpha_beta_player(state, c4)
    c4.display(state)
    utility = c4.compute_utility(state.board, None, state.to_move)
    if utility == 1:
        print("You won!")
    elif utility == -1:
        print("You lost!")
    else:
        print("Draw!")
