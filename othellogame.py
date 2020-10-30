import copy
import random #random.randint(a,b) get a rand int from a to b inclusive
import math # for positive an negative inf
WHITE = 1
BLACK = -1
EMPTY = 0
SIZE = 8 # size of the board 
SKIP = "SKIP"
NEG_INFI = -math.inf
INFI = math.inf
class OthelloPlayerTemplate:
    '''Template class for an Othello Player

    An othello player *must* implement the following methods:

    get_color(self) - correctly returns the agent's color

    make_move(self, state) - given the state, returns an action that is the agent's move
    '''
    def __init__(self, mycolor):
        self.color = mycolor

    def get_color(self):
        return self.color

    def make_move(self, state): # Given the state, returns a legal action for the agent to take in the state
        return None
# control current state, color holding, and movement, the game will keep asking for moves until a legal one is given
class HumanPlayer:
    def __init__(self, mycolor): # assign a color
        self.color = mycolor

    def get_color(self): # return the color
        return self.color

    def make_move(self, state):
        curr_move = None # declare the move attribute
        legals = actions(state) # get possible legal moves
        while curr_move == None: # if there are legal moves
            display(state) # show the state
            if self.color == 1: # what color is this player?
                print("White ", end='')
            else:
                print("Black ", end='')
            print(" to play.")
            print("Legal moves are " + str(legals))
            move = input("Enter your move as a r,c pair:")
            if move == "": # if there is no input, take the first step as the default step
                return legals[0]

            if move == SKIP and SKIP in legals: # if it is OK to skip, skip 
                return move

            try: # do the move
                movetup = int(move.split(',')[0]), int(move.split(',')[1])
            except:
                movetup = None
            if movetup in legals:
                curr_move = movetup
            else:
                print("That doesn't look like a legal action to me")
        return curr_move
# A class to represent an othello game state
class OthelloState:
    def __init__(self, currentplayer, otherplayer, board_array = None, num_skips = 0):
        if board_array != None: # if not the initial state, take the array as the state
            self.board_array = board_array
        else: # set up the initial state with 4 chess on the board
            self.board_array = [[EMPTY] * SIZE for i in range(SIZE)]
            self.board_array[3][3] = WHITE
            self.board_array[4][4] = WHITE
            self.board_array[3][4] = BLACK
            self.board_array[4][3] = BLACK
        self.num_skips = num_skips # calculate current skips to see if it is the end
        self.current = currentplayer # who is the current player?
        self.other = otherplayer # the opponent
# the dummy player which takes random move
class RandomPlayer:
    def __init__(self, mycolor): # assign the color to the dummy player
        self.color = mycolor
    def get_color(self): # return the color
        return self.color
    def make_move(self, state):
        curr_move = None
        legals = actions(state) # get all moves
        while curr_move == None:
            display(state)
            rand = random.randint(0,len(legals)-1) #ramdomly pick a move
            move = legals[rand]
            print("Dummy took this step: "+str(move))
            if move == "": # if there is no input, take the first step as the default step
                return legals[0]

            if move == SKIP and SKIP in legals: # if it is OK to skip, skip 
                return move

            try: # do the move
                movetup = int(move[0]), int(move[1])
            except:
                movetup = None
            if movetup in legals:
                curr_move = movetup
        return curr_move
# the minimax player
class MimimaxPlayer:
    def __init__(self, mycolor, depth): # assign the color to the dummy player
        self.color = mycolor
        self.depth = depth
    def get_color(self): # return the color
        return self.color
    def get_depth(self): # return the depth
        return self.depth
    def make_move(self, state):
        curr_move = None
        legals = actions(state) # get all moves
        while curr_move == None:
            display(state)
            final_pos = tuple()
            move_max = NEG_INFI
            for position in legals:
                temp_num = minimax(state,self.depth, True, self.color)
                if temp_num>move_max:
                    final_pos = position
                    move_max = temp_num
            move = final_pos # the random move
            print("minimax_agent moved: "+ str(move))
            if move == "": # if there is no input, take the first step as the default step
                return legals[0]

            if move == SKIP and SKIP in legals: # if it is OK to skip, skip 
                return move

            try: # do the move
                movetup = int(move[0]), int(move[1])
            except:
                movetup = None
            if movetup in legals:
                curr_move = movetup
        return curr_move
# the alpha-beta minimax player
class ABMimimaxPlayer:
    def __init__(self, mycolor, depth): # assign the color to the dummy player
        self.color = mycolor
        self.depth = depth
    def get_color(self): # return the color
        return self.color
    def get_depth(self): # return the depth
        return self.depth
    def make_move(self, state):
        curr_move = None
        legals = actions(state) # get all moves
        while curr_move == None:
            display(state)
            final_pos = tuple()
            move_max = NEG_INFI
            for position in legals:
                temp_num = minimax_ab(state,self.depth, NEG_INFI, INFI, True, self.color)
                if temp_num>move_max:
                    final_pos = position
                    move_max = temp_num
            move = final_pos # the random move
            print("AB_minimax_agent moved: "+ str(move))
            if move == "": # if there is no input, take the first step as the default step
                return legals[0]

            if move == SKIP and SKIP in legals: # if it is OK to skip, skip 
                return move

            try: # do the move
                movetup = int(move[0]), int(move[1])
            except:
                movetup = None
            if movetup in legals:
                curr_move = movetup
        return curr_move
#---------------------------------------------------------
#-----------------^^ CLASS vv FUNCTIONS-------------------
#---------------------------------------------------------
# will return current state of the board
def player(state):
    return state.current
# given the current state, return a list of legal actions, append "SKIP" for action if there is no legal actions
def actions(state):
    legal_actions = []
    for i in range(SIZE):
        for j in range(SIZE):
            if result(state, (i,j)) != None:
                legal_actions.append((i,j))
    if len(legal_actions) == 0:
        legal_actions.append(SKIP)
    return legal_actions
# return the result based on the action taken, if action is skip return the current state. Note this function will flip the chess automatically, and if the action is not legal return None
def result(state, action):
    if action == SKIP: # if the action is skip, return the current board
        newstate = OthelloState(state.other, state.current, copy.deepcopy(state.board_array), state.num_skips + 1)
        return newstate

    if state.board_array[action[0]][action[1]] != EMPTY: # if the input is not a legal action(in the list), return None
        return None

    color = state.current.get_color()
    newstate = OthelloState(state.other, state.current, copy.deepcopy(state.board_array))# create new state with players swapped and a copy of the current board
    newstate.board_array[action[0]][action[1]] = color # set the new state to the chosen color
    
    flipped = False # check if this move is leagal
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    for d in directions:
        i = 1
        count = 0
        while i <= SIZE:
            x = action[0] + i * d[0]
            y = action[1] + i * d[1]
            if x < 0 or x >= SIZE or y < 0 or y >= SIZE:
                count = 0
                break
            elif newstate.board_array[x][y] == -1 * color:
                count += 1
            elif newstate.board_array[x][y] == color:
                break
            else:
                count = 0
                break
            i += 1

        if count > 0: # see if there is anything on the way, if so, make flip
            flipped = True

        for i in range(count): # flip the coin
            x = action[0] + (i+1) * d[0]
            y = action[1] + (i+1) * d[1]
            newstate.board_array[x][y] = color

    if flipped: # if there is flip, return the new state
        return newstate
    else: # if no pieces are flipped, it's not a legal move
        return None
# check if the state reaches the final state
def terminal_test(state):
    if state.num_skips == 2: # if both players have skipped, 2 skipps in a row
        return True # then there is no action to take for both of them, return the state
    # if there are no empty spaces
    empty_count = 0
    for i in range(SIZE): # check if there is still space on the board, if there is no empty spaces, return None
        for j in range(SIZE):
            if state.board_array[i][j] == EMPTY:
                empty_count += 1
    if empty_count == 0:
        return True
    return False
# display the current state
def display(state):
    print('  ', end='')
    for i in range(SIZE):
        print(i,end='')
    print()
    for i in range(SIZE):
        print(i, '', end='')
        for j in range(SIZE):
            if state.board_array[j][i] == WHITE:
                print('W', end='')
            elif state.board_array[j][i] == BLACK:
                print('B', end='')
            else:
                print('-', end='')
        print()
# print out the final state, score and the winner
def display_final(state):
    wcount = 0
    bcount = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[i][j] == WHITE:
                wcount += 1
            elif state.board_array[i][j] == BLACK:
                bcount += 1

    print("Black: " + str(bcount))
    print("White: " + str(wcount))
    if wcount > bcount:
        print("White wins")
    elif wcount < bcount:
        print("Black wins")
    else:
        print("Tie")
# the play game method, modify this
def play_game(p1 = None, p2 = None,deep1 = 2,deep2 = 2):
    if p1 == None or p1 =="1"or p1 == "":
        p1 = HumanPlayer(BLACK) # change this to a random player
    if p2 == None or p2 =="1" or p2 == "":
        p2 = HumanPlayer(WHITE) # change this to the agent player
    if p1 == "2":
        p1 = RandomPlayer(BLACK) # change this to a random player
    if p2 == "2":
        p2 = RandomPlayer(WHITE)
    if p1 == "3":
        p1 = MimimaxPlayer(BLACK,deep1) # change this to a random player
    if p2 == "3":
        p2 = MimimaxPlayer(WHITE,deep2)
    if p1 == "4":
        p1 = ABMimimaxPlayer(BLACK,deep1) # change this to a random player
    if p2 == "4":
        p2 = ABMimimaxPlayer(WHITE,deep2)

    s = OthelloState(p1, p2) # set the state
    while True: # start the game
        # Note: make_move is a part of the human class, which needs to be rewrite
        action = p1.make_move(s) # player 1 move first
        if action not in actions(s): # if it take an illegal move, end game
            print("Illegal move made by Black")
            print("White wins!")
            return
        s = result(s, action) # get the result action after the move
        if terminal_test(s): # if it is a legal terminal state, display the end
            print("Game Over")
            display(s)
            display_final(s)
            return False
        action = p2.make_move(s) # turn for player 2 to take the move
        if action not in actions(s): # if illegal end
            print("Illegal move made by White")
            print("Black wins!")
            return
        s = result(s, action) # of leagal take the move
        if terminal_test(s):
            print("Game Over")
            display(s)
            display_final(s)
            return True
# the evalution/utility function
def util(state, color): #use xx.color, dont use.get_color, util(s,xx.color)
    cd = coin_diff(state,color)
    md = move_diff(state)
    cap = corner_diff(state,color)
    return 0.1*cd+0.4*md+1.5*cap
# calc the coin diff for state, as a partial of utility score
def coin_diff(state,color):
    up_score = 0 # return the utility score
    down_score = 0
    if color == WHITE:
        other = BLACK
    else:
        other = WHITE
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board_array[j][i] == color:
                up_score+=1
            if state.board_array[j][i] == other:
                down_score+=1
    if up_score == down_score:
        return 0
    else:
        return (abs(up_score-down_score)/(up_score+down_score))
# calc the number of legal moves at the point, a part of utility score
def move_diff(state):
    num_actions = actions(state)
    return len(num_actions)
# calc the 4 corners captured by the color
def corner_diff(state,color):
    the_corner = [state.board_array[0][0],state.board_array[0][7],state.board_array[7][0],state.board_array[7][7]]
    captured = the_corner.count(color)
    return captured
# the minimax function
def minimax(state, depth, minimax_player: bool, player_color):
    if depth == 0 or terminal_test(state):
        return util(state,player_color)
    if minimax_player:
        max_eval = NEG_INFI
        pos_actions =  actions(state)
        for items in pos_actions:
            new_state = result(state, items)
            evalu = minimax(new_state,depth-1,False,player_color)
            max_eval = max(evalu, max_eval)
        return max_eval
    else: # for min_player's round
        min_eval = INFI
        pos_actions =  actions(state)
        for items in pos_actions:
            new_state = result(state, items)
            evalu = minimax(new_state,depth-1,True,player_color)
            min_eval = min(evalu, min_eval)
        return min_eval
# the alpha-beta prune
def minimax_ab(state, depth, alpha, beta, minimax_player: bool, player_color):
    if depth == 0 or terminal_test(state):
        return util(state,player_color)
    if minimax_player:
        max_eval = NEG_INFI
        pos_actions =  actions(state)
        for items in pos_actions:
            new_state = result(state, items)
            evalu = minimax_ab(new_state,depth-1, alpha, beta,False,player_color)
            max_eval = max(evalu, max_eval)
            alpha = max(alpha, evalu)
            if beta<=alpha:
                break
        return max_eval
    else: # for min_player's round
        min_eval = INFI
        pos_actions =  actions(state)
        for items in pos_actions:
            new_state = result(state, items)
            evalu = minimax_ab(new_state,depth-1, alpha, beta,True,player_color)
            min_eval = min(evalu, min_eval)
            beta = min(beta,evalu)
            if beta<=alpha:
                break
        return min_eval