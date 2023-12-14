from state import GameState
import random

class MinimaxModel:
    def __init__(self, depth):
        self.depth = depth
        
    # use minimax to find the best move
    def make_move(self, state):
        move, score = self.minimax(state, 1, self.depth, float('-inf'), float('inf'))
        state.make_move(move, 1)
    
    def minimax(self, state, turn, depth, alpha, beta):
        if depth == 0 or state.is_game_over():
            return None, self.evaluate(state)
        
        nextTurn = 1 - turn
        nextDepth = depth - 1

        maxScore = -10000000000
        maxAction = None

        minScore = 10000000000
        minAction = None

        for action in state.get_valid_moves(turn):
            nextAction, curScore = self.minimax(state.get_next_state(action, turn), nextTurn, nextDepth, alpha, beta)
            if curScore < minScore:
                minScore = curScore
                minAction = action

            if curScore > maxScore:
                maxScore = curScore
                maxAction = action
            
            if turn == 1:
                alpha = max(alpha, curScore)
                if beta <= alpha:
                    break
            else:
                beta = min(beta, curScore)
                if beta <= alpha:
                    break
        
        if turn == 1:
            return (maxAction, maxScore)
        else:
            return (minAction, minScore)
    
    # evaluating state for player 2
    def evaluate(self, state):
        if state.is_game_over():
            if state.winner() == 1:
                return 10000000000
            elif state.winner() == 0:
                return -10000000000
        score = 5 * (len(state.fastest_path(0)) - len(state.fastest_path(1)))
        score += 1 * (state.p2.numWalls - state.p1.numWalls)
        return score
        
