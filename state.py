from player import Player

# Wall -> [(pos), dir]
# walls are defined as (x,y) and "h" or "v" depending if it's horizontal or vertical

class GameState:
    def __init__(self, p1=None, p2=None, walls=[]):
        self.p1 = Player((8, 4), 10) if p1 is None else p1
        self.p2 = Player((0, 4), 10) if p2 is None else p2
        self.walls = walls
    
    def start_state(self):
        p1 = Player((8, 4), 10)
        p2 = Player((0, 4), 10)
        walls = []
        gs = GameState(p1, p2, walls)
        return gs

    def reset_game(self):
        gs = self.start_state()
        self.p1 = gs.p1
        self.p2 = gs.p2
        self.walls = gs.walls
    
    def is_game_over(self):
        return self.p1.get_pos()[0] == 8 or self.p2.get_pos()[0] == 0
    
    # move is of the form [pos] for player moves and [pos, direction]
    # player is 1 for player 1, and 2 for player 2
    def is_valid_move(self, player, move):
        move_pos = move[0]
        if len(move) == 2:
            move_dir = move[1]
            if player.get_num_walls() == 0:
                return False
            # wall position out of bounds
            if (move_pos[0] < 0 or move_pos[0] > 7) or (move_pos[1] < 0 or move_pos[1] > 7):
                return False 
            
            for w in self.walls:
                if w[1] == move_dir:
                    ...
                return 
        return True

    def toString(self):
        res = "Player 2 # Walls: " + str(self.p2.get_num_walls()) + "\n"
        p1pos = self.p1.get_pos()
        p2pos = self.p2.get_pos()

        for row in range(18):
            prevRow = (row - 1) // 2
            for col in range(9):
                if row % 2 == 0:
                    # empty square is "\u25A1"
                    if (row // 2, col) == p1pos:
                        res += "1"
                    elif (row // 2, col) == p2pos:
                        res += "2"
                    else:
                        res += "\u25A1"
                    
                    wallFound = False
                    for wall in self.walls:
                        d = wall[1]
                        wallPos = wall[0]
                        
                        if d == "h":
                            continue

                        if (wallPos[0] == row // 2 or wallPos[0] == (row // 2) - 1) and wallPos[1] == col:
                            res += "|"
                            wallFound = True
                            break
                    if not wallFound:
                        res += " "
                else:
                    wallFound = False
                    for wall in self.walls:
                        d = wall[1]
                        wallPos = wall[0]

                        if d == "v":
                            continue

                        if wallPos[0] == prevRow and (wallPos[1] == col or wallPos[1] == col - 1):
                            res += "- " if wallPos[1] == col - 1 else "--"
                            wallFound = True
                            break
                    if not wallFound:
                        res += "  "
                
            res += "\n"
        res += "Player 1 # Walls: " + str(self.p1.get_num_walls()) + "\n"
        return res

gs = GameState(walls=[[(3, 7), "v"], [(0,0), "h"], [(0,2), "h"], [(0,7), "h"]])
print(gs.toString())



    
    