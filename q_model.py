from state import GameState
import random
class QModel:
    def __init__(self, learning_rate=0.9, epsilon=0.1, discount=0.8):
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.discount = discount
        self.features = self.initialize_features()
        self.weights = [2, 1, 1]
        self.is_training = True
    
    def initialize_features(self):
        def shortest_path_feature(state, action):
            next_state = state.get_next_state(action)
            pathA = next_state.fastest_path(turn=0) # shortest player path
            pathB = next_state.fastest_path(turn=1) # shortest computer path

            return len(pathA) - len(pathB)
        # how many ways can you block a players fastest path
        def blockable_paths(state, action):
            n_state = state.get_next_state(action)
            blockableA = n_state.walls_blockable(turn=0)
            blockableB = n_state.walls_blockable(turn=1)
            return blockableA - blockableB
        
        def number_walls(state, action):
            n_state = state.get_next_state(action)
            return n_state.p2.numWalls - n_state.p1.numWalls
        
        features = [shortest_path_feature, blockable_paths, number_walls]
        return features

    def get_q_val(self, state, action):
        s = 0
        for i in range(len(self.weights)):
            s += self.weights[i] * self.features[i](state, action)
        return s
    
    def find_reward(self, state, next_state):
        if next_state.is_game_over():
            if next_state.winner() == 1:
                return 100
            elif next_state.winner() == 0:
                return -100
        return 0
        # origDistance = len(state.fastest_path(turn=1))
        # newDistance = len(next_state.fastest_path(turn=1))

        # origPlayerDistance = len(state.fastest_path(turn=0))
        # newPlayerDistance = len(next_state.fastest_path(turn=0))

        # blockableWalls = state.walls_blockable(turn=1)
        # newBlockableWalls = next_state.walls_blockable(turn=1)

        # playerBlockableWalls = state.walls_blockable(turn=0)
        # newPlayerBlockableWalls = next_state.walls_blockable(turn=0)

        # if newDistance < origDistance:
        #     return 2
        # else:
        #     if newPlayerDistance >= origPlayerDistance:
        #         if newBlockableWalls < blockableWalls:
        #             return 1
        #         if newPlayerBlockableWalls > playerBlockableWalls:
        #             return 1
        # return -1
    
    # Make best move from values
    def make_move(self, state):
        valid_moves = state.get_valid_moves()
        random.shuffle(valid_moves)
        bestAction = None
        bestScore = float('-inf')

        #exploit
        for action in valid_moves:
            if self.get_q_val(state, action) > bestScore:
                bestScore = self.get_q_val(state, action)
                bestAction = action     
           
        if self.is_training:
            # explore
            # if random.randint(0, 100) < self.epsilon * 100:
            #     print("Exploring")
            #     bestAction = random.choice(valid_moves)
            next_state = state.get_next_state(bestAction)
            r = self.find_reward(state, next_state)
            # update with sample
            self.update_weights(state, bestAction, r, next_state)
            
        state.make_move(bestAction)
    
    def update_weights(self, state, action, reward, next_state):
        legalActions = state.get_valid_moves()
        
        maxQval = 0.0
        if len(legalActions) != 0:
            maxQval = max([self.get_q_val(next_state, nextAction) for nextAction in legalActions])
        
        difference = reward + self.discount * maxQval - self.get_q_val(state, action)

        for i in range(len(self.weights)):
            self.weights[i] += self.learning_rate * difference * self.features[i](state, action)
        
        print(self.weights)

    def set_training(self, is_training):
        self.is_training = is_training


        
    

        


