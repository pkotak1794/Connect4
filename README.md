# CPSC 481 - Artificial Intelligence - Final Project 
### Team Members: Xuan Bui, Priyanka Lee, & Tiffany Tran 

This project is an implementation of Connect4 game that allows the user to play against human or AI opponent. 

## Program Features 
- Larger game board-- 9x7 size
- Uses alpha-beta pruning (with cutoff) for efficiency
- Two gameplay modes: 
  player vs player <br>
  player vs AI opponent
- Command line interface
- AI uses evaluation function for optimality
- Valid moves are shown to player 

## Classes & Functions
- NewConnectFour class: inherits from ConnectFour class and sets up the basis of the game logic
- display: updates the display function and creates the visual of the game board
- evaluate: creates the evaluation function that the alpha_beta_player uses to make optimal move choices
- row_count & dir_count: helper functions used by the evaluate function
- query_player: edits the query_player to take input in a specified manner 
- alpha_beta_player: uses alpha_beta_cutoff_search to play the game
- play_game: creates the game instance and sets up the game to be played by the user 
- time module: gets the execution time per move made by the AI opponent 

## Technical Details 
- Written in Python code 
- All game implementation is done in connect4.py but requires downloading games.py & utils.py in the same directory
- Run command: 
  cd Connect4 <br>
  python3 connect4.py 
  
 ## Acknowledgments
 This project builds upon the original code from AIMA Python Code repository. 
 https://github.com/aimacode/aima-python
