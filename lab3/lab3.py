# MIT 6.034 Lab 3: Games
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from game_api import *
from boards import *
INF = float('inf')

def is_game_over_connectfour(board) :
    "Returns True if game is over, otherwise False."
    #print sorted(board.get_all_chains(), key=lambda x: len(x))
    num_cells=board.num_rows*board.num_cols
    for chain in board.get_all_chains():
        if len(chain)>=4 or board.count_pieces()==num_cells:
            return True
    return False
    #raise NotImplementedError

def next_boards_connectfour(board) :
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    boards=[]
    for i in range(7):
        if not board.is_column_full(i) and not is_game_over_connectfour(board):
            boards.append(board.add_piece(i))
    return boards
    #raise NotImplementedError

def endgame_score_connectfour(board, is_current_player_maximizer) :
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    chains=sorted(board.get_all_chains(), key=lambda x: len(x))
    if len(chains[-1])>=4:
        if not is_current_player_maximizer:
            return 1000;
        else:
            return -1000;
    return 0;

def endgame_score_connectfour_faster(board, is_current_player_maximizer) :
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""
    chains=sorted(board.get_all_chains(), key=lambda x: len(x))
    if len(chains[-1])>=4:
        score = 1000+23*(42-board.count_pieces());
        if not is_current_player_maximizer:
            return score
        else:

            return -score
    return 0;

def heuristic_connectfour(board, is_current_player_maximizer):
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""
    current_chains = board.get_all_chains(True)
    other_chains = board.get_all_chains(False)
    #print "current_chains: ",current_chains
    #print "other_chains: ", other_chains
    current_score = 0
    other_score = 0
    for chain in current_chains:
        if len(chain)>=1:
            current_score+=len(chain)**2
    for chain in other_chains:
        if len(chain)>=1:
            other_score+=len(chain)**2
    score = 10*(other_score - current_score)
    #if not is_current_player_maximizer
    #raise NotImplementedError
    #print "current_score: ", current_score, "other_score: ", other_score;
    if is_current_player_maximizer:
        return -score
    else:
        return score

# Now we can create AbstractGameState objects for Connect Four, using some of
# the functions you implemented above.  You can use the following examples to
# test your dfs and minimax implementations in Part 2.

# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot = ConnectFourBoard(),
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot = BOARD_UHOH,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)


#### PART 2 ###########################################
# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.
state_evals=0
agenda = []
_path=[];
_score=-INF;
paths=[]
path=[]
level=0
_state=None

def dfs_maximizing(state) :
    """Performs depth-first search to find path with highest endgame score.
    Returns a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations num_evals (a number)"""
    #print state.describe_previous_move()
    global state_evals, path, _path, _score, level, _state;

    level+=1
    path.append(state)
    for stt in state.generate_next_states():
        score=0
        agenda.append((stt, level))
       
        if stt.is_game_over():
            state_evals+=1
            score=stt.get_endgame_score()
            if score>_score:
                _score=score
                _path = path[0:]
                _state = stt
    if not agenda:

        _path.append(_state)
        return [_path, _score, state_evals];
    else:
        new_state, level=agenda.pop()
        path=path[0:level]
        level-=1
        return dfs_maximizing(new_state)


 

depth=0
def get_minimax_score(state, player, path, paths, depth_limit, heuristic_fn):
    global depth;
    _path=path[:]
    _path.append(state)
    
    if state.is_game_over():
        paths.append(_path)
        return _path, state.get_endgame_score(player)
        depth+=1
    
    if player:
        depth+=1
        return max([get_minimax_score(child_state, False, _path, paths,depth_limit, heuristic_fn) for child_state in state.generate_next_states()], key=lambda x: x[1])
    depth+=1
    return min([get_minimax_score(child_state, True, _path,paths,depth_limit, heuristic_fn) for child_state in state.generate_next_states()], key=lambda x: x[1])



def minimax_endgame_search(state, maximize=True) :
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""
    global depth;
    depth=0
    path=[]
    paths=[]
    _path, _score = get_minimax_score(state, maximize, path, paths,INF,always_zero)

    return [_path, _score, len(paths)]


def generic_minmax_search(state, alpha=-INF, beta=INF, heuristic_fn=always_zero, depth_limit=INF, maximize=True):
    num_evals = 0
    _score = 0
    _path = []
    path = [state]

    if state.is_game_over():
        return [[state], state.get_endgame_score(maximize), 1]

    if not (depth_limit):
        return [[state], heuristic_fn(state.snapshot, maximize), 1]

    
    if maximize:
        _score = -INF
        for child in state.generate_next_states():
            [_state, score, evals] = minimax_search_alphabeta(child, alpha, beta, heuristic_fn, depth_limit - 1, False)
            num_evals += evals
            if score > _score:
                _score = score
                _path = path + _state

            
            if alpha!=None:
                if _score > alpha:
                    alpha = _score

                if alpha >= beta:
                    return [_path, alpha, num_evals]

        return [_path, _score, num_evals]
    else:
        _score = +INF

        for child in state.generate_next_states():
            (_state, score, evals) = minimax_search_alphabeta(child, alpha, beta, heuristic_fn, depth_limit - 1, True)
            num_evals += evals
            if score < _score:
                _score = score
                _path = path + _state

            
            if beta!=None:
                if _score < beta:
                    beta = _score

                if alpha >= beta:
                    return [_path, beta, num_evals]

        return [_path, _score, num_evals]

def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :
    "Performs standard minimax search.  Same return type as dfs_maximizing."
    
    
    return generic_minmax_search(state, None, None, heuristic_fn, depth_limit, maximize)
       





def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True) :
    "Performs minimax with alpha-beta pruning.  Same return type as dfs_maximizing."
   
    return generic_minmax_search(state, alpha, beta, heuristic_fn, depth_limit, maximize)



def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    anytime_value = AnytimeValue()   # TA Note: Use this to store values.
    depth = 0
    while depth<=depth_limit-1:
        depth+=1
        best_option=minimax_search_alphabeta(state,-INF,INF, heuristic_fn=heuristic_fn,depth_limit=depth, maximize=True)
        anytime_value.set_value(best_option)
    return anytime_value




##### PART 3: Multiple Choice ##################################################

ANSWER_1 = '4'

ANSWER_2 = '1'

ANSWER_3 = '4'

ANSWER_4 = '5'


#### SURVEY ###################################################

NAME = "Mubarik Mohamoud"
COLLABORATORS = "Izabela Witoszko"
HOW_MANY_HOURS_THIS_LAB_TOOK = 7
WHAT_I_FOUND_INTERESTING = "part two"
WHAT_I_FOUND_BORING = "part one"
SUGGESTIONS = ""
