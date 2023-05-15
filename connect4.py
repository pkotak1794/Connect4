# CPSC 481 - Artificial Intelligence 
# Xuan Bui, Priyanka Lee, & Tiffany Tran

# Connect4 game against an AI or human player on a 9x7 grid size board
# using alpha-beta pruning (cutoff) algorithm & show player valid moves

import copy
import time
from games import *

# create new class that inherits from ConnectFour class 
class NewConnectFour(ConnectFour):
    def __init__(self):
        ConnectFour.__init__(self, h=9, v=7, k=4)   # set board size to 9x7 and 4 in a row to win

    # update display format for game board 
    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print('| {} '.format(board.get((x, y), '.')), end='')
            print('|')
        print('-' * (self.h * 4 + 1))

    # evaluation function that counts pieces in a row and returns difference
    def evaluate(self, state):
        score = 0   # initialize score to 0
        # iterate over board height/width 
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                piece = state.board.get((x, y), None)   # check if there is a piece at current position
                if piece is None:
                    continue    # if no piece, pass over
                # if piece belongs to current player, add to score 
                if piece == state.to_move:
                    score += self.row_count(state, (x, y))
                # if score belongs to opponent, subtract from player score 
                else:
                    score -= self.row_count(state, (x, y))
        return score

    # count number of pieces players have in a row 
    def row_count(self, state, pos):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)] # list of possible directions for counting pieces
        counts = [self.dir_count(state, pos, d) for d in directions] # save result in list 
        return max(counts)  # return max form the counts list 

    # count number of pieces players have in specific position from given position
    def dir_count(self, state, pos, direction):
        player = state.board[pos]   # stores piece at given position
        count = 0   # initialize count to 0
        x, y = pos  # tuple split in x and y variables
        dx, dy = direction  # direction split into dx, dy variables
        # while dx+x and dy+y = piece stored in player variable
        while state.board.get((x+dx, y+dy)) == player:
            count += 1  # increment count
            x, y = x+dx, y+dy   # update x & y 
        return count

    # lets user enter moves 
    def query_player(game, state):
        print("Current board state:")
        game.display(state) # displays current game state 
        print("Available valid moves: {}".format(game.actions(state)))  # shows valid list of moves 
        print("")
        move = None # initialize move to None
        # if there are valid moves for current board 
        if game.actions(state):
            move_string = input('Your move? ')  # take user input for move 
            try:
                row, col = move_string.split(',')
                move = (int(row), int(col))
               # if input entered by user is invalid  
            except ValueError:
                move = move_string
        else:
            print('no valid moves: passing turn to next player')
        return move
    
# function that sets up the game between players 
def play_game():
    play_again = True  # initialize play_again to True

    while play_again:  # loop until user does not want to play again 
        game = NewConnectFour() # create new game instance 
        state = game.initial

        # user picks whether to play against AI or human player 
        print("Welcome to ConnectFour! Let's get started!")
        players = {'X': 'human', 'O': 'human'}
        game_option = input("Enter 'A' to play against the AI opponent or 'H' to play against another human: ")
        if game_option.lower() == 'a':
            players['O'] = 'ai'
            print("You are playing against an AI!")
        else:
            print("You are playing against another human.")

        while True:
            current_player = game.to_move(state)
            print("Current player: {}".format(current_player))  # shows which player has to move
            game.display(state)
            print("Available moves: {}".format(game.actions(state)))    # shows valid mvoes 
            print("")
            if players[current_player] == 'human':
                move = query_player(game, state)    # calls query_player function for human player 
            else:
                start_time = time.time()
                move = alpha_beta_player(game, state)   # calls alpha_beta_player function w/ alpha beta cutoff search
                end_time = time.time()
                print("Time taken by AI player: {:.3f} seconds".format(end_time - start_time))  # prints AI execution time per move
            if move is None:
                break
            state = game.result(state, move)
            print("Score:", game.evaluate(state))   # prints score from evaluate function
            if game.terminal_test(state):   # game is over 
                break

        # calculate final score and print result
        score = game.utility(state, game.to_move(game.initial)) # uses utility function to calculate who won 
        if score == 1:
            print("Player X has won the game!")
        elif score == -1:
            print("Player O has won the game!")
        else:
            print("Aww...it's a draw")

        # ask the user if they want to play again
        play_again = input("Do you want to play again? (y/n)").lower() in ('y')
        print("")

    print("Thanks for playing ConnectFour!")


if __name__ == "__main__":
    #game = NewConnectFour()
    play_game()


