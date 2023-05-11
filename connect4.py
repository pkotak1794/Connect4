# CPSC 481 - Artificial Intelligence 
# Xuan Bui, Priyanka Lee, & Tiffany Tran

# Connect4 game against an AI player on a 9x7 grid size board
# using alpha-beta pruning algorithm & show player valid moves

#from games import ConnectFour, alpha_beta_player, GameState, Game
import copy
from games import *

# define GameState class to initialize variables
class GameState:
    def __init__(self, player_to_move, utility, board, moves=None): # constructor that takes 4 arguments
        self.player_to_move = player_to_move # tracks turn of player/opponent with a string
        self.utility = utility # keeps score of game (1 = player win, -1 = player loss, 0 = draw)
        self.board = board  # current board state
        self.moves = moves or [] # empty list if no value for moves

    # track whose turn it is    
    def to_move(self):
        return self.player_to_move

# class definition for game play implementation 
class ConnectFour(Game):
    def __init__(self):
        self.cols = 9   # number of rows
        self.rows = 7   # number of columns
        self.win_length = 4 # number of tokens needed in a row to win 
        self.board = {(row, col): "." for row in range(self.rows) for col in range(self.cols)}  # game board initialization
        self.initial = GameState(player_to_move='X', utility=0, board=self.board, moves=[]) # initial game state & player 'X' to move
        self.ai_player = alpha_beta_player  # AI opponent set to alpha_beta_player

    # create new instance with same dimensions + win condition as previous
    def to_game(self, state):
        game = ConnectFour()
        game.cols = self.cols
        game.rows = self.rows
        game.win_length = self.win_length
        game.initial = state
        return game
    
    # keep track of what actions are available 
    def actions(self, state):
        if state is None:
            return []
        # get game board and generate list of possible actions (all empty spots) 
        board = state.board
        actions = [(row, col) for row in range(self.rows) for col in range(self.cols)
            if board[(row, col)] == "." and (row == self.rows - 1 or board[(row+1, col)] != ".")]
        print("Valid actions:", actions)    # prints valid list of actions available 
        return actions

    # analyze current game state and create new game state after token is played 
    def result(self, state, row=None, col=None):
        if state is None:
            return None
        if col is None or col not in range(self.cols):  # if selected column is out of range
            return state
        # traverse column backwards 
        for r in range(self.rows-1, -1, -1):
            if state.board[(r, col)] == ".":    # if column is empty, save row number 
                break
        else: # if no space in selected column 
            return state
        player = state.player_to_move   # check which player 'X' or 'O' has moved 
        new_board = copy.deepcopy(state.board)
        new_board[(r, col)] = player    # update board with token on newly occupied space
        new_moves = state.moves + [(r, col)]    # save move in state 
        new_to_move = 'O' if player == 'X' else 'X' # check which players turn it is now
        new_state = GameState(player_to_move=new_to_move, utility=self.compute_utility(new_board, (r, col), player),
                                  board=new_board, moves=new_moves) # calculate new utility based on recent move 
        if not self.actions(new_state):
            new_state.utility = 0
        return new_state
    
    # computes game results and checks for a win/loss 
    def compute_utility(self, board, move, player):
        if move is None:
            return None
        row, col = move
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # possible direction of win scenarios
        # checks for wins in all directions (vertical/horizontal/diagonal)
        for d in directions:
            count = 1
            # diagonally (bottom-left to top-right)
            for i in range(1, self.win_length):
                r, c = row + d[0]*i, col + d[1]*i
                if r < 0 or r >= self.rows or c < 0 or c >= self.cols or board[(r, c)] != player:
                    break
                count += 1
            # diagonally (top-left to bottom right)
            for i in range(1, self.win_length):
                r, c = row - d[0]*i, col - d[1]*i
                if r < 0 or r >= self.rows or c < 0 or c >= self.cols or board[(r, c)] != player:
                    break
                count += 1
            if count >= self.win_length:
                return 1 if player == 'X' else -1
        if all(board[(r, c)] != '.' for r in range(self.rows) for c in range(self.cols)):   # if the game results in a tie
            return 0
        return 0    # if this line is changed to return None it causes infinite recursion but causes automatic Draw as is

    # checks to see if the game is still in progress or completed 
    def terminal_test(self, state):
        #print(type(state))
        if state is None:   # game isn't over yet 
            return False
        return state.utility is not None    # game is over 

    def display(self, state):
        board = state.board
        for row in range(self.rows):
            print(" | ", end="")
            for col in range(self.cols):
                print(board[(row, col)], end=" | ")
            print("")

if __name__ == "__main__":
    game = ConnectFour()
    print("Welcome to Connect4! Let's get started!")
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
