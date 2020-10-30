# FILES #
- Run game.py to play the game, user can choose the type of agent/player by following the prompt

# Algorithms Used #
- RandomPlayer: a class that move randomly every step
- MimimaxPlayer: player implemented minimax, take color and depth
- ABMimimaxPlayer: minimax player with alpha-beta pruning
- play_game: modified so user can pick the type of player they want
- util: calculate utility, with 3 sub-functions:
    - coin_diff: difference between 2 colors
    - corner_diff: if corner can be captured
    - move_diff: how many next-move avaliable
- minimax: the minimax algorithm
- minimax_ab: minimax with alpha-beta