class Player:
    def __init__(self, pos, numWalls):
        self.pos = pos
        self.numWalls = numWalls
    
    def get_pos(self):
        return self.pos
    
    def get_num_walls(self):
        return self.numWalls

    def lose_wall(self):
        numWalls -= 1
    