# needs to be 9x7 grid size
# add valid moves function
# alpha-beta pruning algorithm 

#from games import ConnectFour, alpha_beta_player, GameState, Game
import copy
from games import *

class GameState:
    def __init__(self, player_to_move, utility, board, moves=None):
        self.player_to_move = player_to_move
        self.utility = utility
        self.board = board
        self.moves = moves or []

    def to_move(self):
        return self.player_to_move

class ConnectFour(Game):
    def __init__(self):
        self.cols = 9
        self.rows = 7
        self.win_length = 4
        self.board = {(row, col): "." for row in range(self.rows) for col in range(self.cols)}
        self.initial = GameState(player_to_move='X', utility=0, board=self.board, moves=[])
        self.ai_player = alpha_beta_player

    def to_game(self, state):
        game = ConnectFour()
        game.cols = self.cols
        game.rows = self.rows
        game.win_length = self.win_length
        game.initial = state
        return game
    
    def actions(self, state):
        if state is None:
            return []
        return [(row, col) for row in range(self.rows) for col in range(self.cols)
            if state.board[(row, col)] == "." and (row == self.rows - 1 or state.board[(row+1, col)] != ".")]

    def result(self, state, row=None, col=None):
        if state is None:
            return None
        if col is None or col not in range(self.cols):
            return state
        for r in range(self.rows-1, -1, -1):
            if state.board[(r, col)] == ".":
                break
        else: # column is full
            return state
        player = state.player_to_move
        new_board = copy.deepcopy(state.board)
        new_board[(r, col)] = player
        new_moves = state.moves + [(r, col)]
        new_to_move = 'O' if player == 'X' else 'X'
        new_state = GameState(player_to_move=new_to_move, utility=self.compute_utility(new_board, (r, col), player),
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
                return 0

    def terminal_test(self, state):
        #print(type(state))
        if state is None:
            return False
        return state.utility is not None

    def display(self, state):
        board = state.board
        for row in range(self.rows):
            print(" | ", end="")
            for col in range(self.cols):
                print(board[(row, col)], end=" | ")
            print("")

if __name__ == "__main__":
    game = ConnectFour()
    print(game)
    board = {(row, col): "." for row in range(game.rows) for col in range(game.cols)}
    game.initial = GameState(player_to_move='X', utility=game.compute_utility(board, None, 'X'), board=board, moves=[])
    state = game.initial
    while not game.terminal_test(state):
        game.display(state)
        if state.to_move() == 'X':
            col = int(input("Enter a column number: "))
            state = game.result(state, row=None,col=col)
        else:
            state = alpha_beta_player(game, state)
    game.display(state)
    utility = game.compute_utility(state.board, None, state.to_move)
    if utility == 1:
        print("Congratulations! You won!")
    elif utility == -1:
        print("Awww, you lost...")
    else:
        print("It's a Draw.")
