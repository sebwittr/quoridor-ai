from player import Player

# Wall -> [(pos), dir]
# walls are defined as (x,y) and "h" or "v" depending if it's horizontal or vertical
# turn -> 0 is player 1, 1 is player 2

class GameState:
    def __init__(self, p1=None, p2=None, walls=[], turn=0):
        self.p1 = Player((8, 4), 10) if p1 is None else p1
        self.p2 = Player((0, 4), 10) if p2 is None else p2
        self.walls = walls
        self.turn = turn
    
    def reset_game(self):
        self = GameState()
    
    def is_game_over(self):
        return self.p1.get_pos()[0] == 8 or self.p2.get_pos()[0] == 0
    
    def get_valid_directions(self, playerPos, newWalls):
        moves = []
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            newPos = (playerPos[0] + move[0], playerPos[1] + move[1])
            if (0 <= newPos[0] <= 8 and 0 <= newPos[1] <= 8) and not self.are_blocked(playerPos, newPos, newWalls):
                moves.append(newPos)
        return moves
    def is_goal_possible(self, player, newWalls):
        goalRow = 0 if player == self.p1 else 8
        visited = set()
        queue = []
        queue.append(player.get_pos())
        while len(queue) > 0:
            curr = queue.pop(0)
            if curr in visited:
                continue
            visited.add(curr)
            if curr[0] == goalRow:
                return True
            for move in self.get_valid_directions(curr, newWalls):
                queue.append(move)
        return False

    # move is of the form [pos] for player moves and [pos, direction]
    def is_valid_move(self, move):
        move_pos = move[0]

        p = self.p1 if self.turn == 0 else self.p2
        otherP = self.p2 if self.turn == 0 else self.p1
        # wall move
        if len(move) == 2:
            move_dir = move[1]
            if p.get_num_walls() == 0:
                return False
            # wall position out of bounds
            if (move_pos[0] < 0 or move_pos[0] > 7) or (move_pos[1] < 0 or move_pos[1] > 7):
                return False 
            
            # overlap with other walls
            for w in self.walls:
                if w[0] == move_pos:
                    return False
                # horizontal wall overlap
                if move_dir == "h" and w[1] == "h" and w[0][0] == move_pos[0] and (w[0][1] == move_pos[1] - 1 or move_pos[1] == w[0][1] - 1):
                    return False
                # vertical wall overlap
                if move_dir == "v" and w[1] == "v" and w[0][1] == move_pos[1] and (w[0][0] == move_pos[0] - 1 or move_pos[0] == w[0][0] - 1):
                    return False

            # check if players can still reach their goal
            newWalls = self.walls.copy()
            newWalls.append([move_pos, move_dir])
            if not self.is_goal_possible(p, newWalls) or not self.is_goal_possible(otherP, newWalls):
                return False

        else:
            newPos = move[0]
            dist = abs(newPos[0] - p.pos[0]) + abs(newPos[1] - p.pos[1])
            # move out of bounds
            if not (0 <= newPos[0] <= 8 and 0 <= newPos[1] <= 8):
                return False
            if newPos == p.pos or newPos == otherP.pos:
                return False
            if dist > 2:
                return False
            # hopping over a player
            if dist == 2:
                # if distance is 2, we hopped over a player in some direction
                # dist from other player to current player
                otherDist = abs(p.pos[0] - otherP.pos[0]) + abs(p.pos[1] - otherP.pos[1])
                
                # dist from other player to new position
                otherNewDist = abs(newPos[0] - otherP.pos[0]) + abs(newPos[1] - otherP.pos[1])
                if otherDist != 1:
                    return False
                if otherNewDist != 1:
                    return False
                #can't hop over a blocked player
                if self.are_blocked(p.pos, otherP.pos, self.walls):
                    return False
                #can't hop over a wall
                if self.are_blocked(newPos, otherP.pos, self.walls):
                    return False
                
                return True
        return True
    
    # are 2 positions blocked by a wall?
    def are_blocked(self, pos1, pos2, walls):
        # horizontal wall
        dist = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        if dist != 1:
            return False
        if pos1[0] == pos2[0]:
            # vertical wall
            for w in walls:
                if w[1] == "v" and (w[0][0] == pos1[0] or w[0][0] == pos1[0] - 1) and (w[0][1] == min(pos1[1], pos2[1])):
                    return True
        else:
            # horizontal wall
            for w in self.walls:
                if w[1] == "h" and (w[0][1] == pos1[1] or w[0][1] == pos1[1] - 1) and (w[0][0] == min(pos1[0], pos2[0])):
                    return True
        return False

    def get_valid_moves(self):
        moves = []
        p = self.p1 if self.turn == 0 else self.p2
        otherP = self.p2 if self.turn == 0 else self.p1
        validDirections = self.get_valid_directions(p.get_pos(), self.walls)
        playerDist = abs(p.get_pos()[0] - otherP.get_pos()[0]) + abs(p.get_pos()[1] - otherP.get_pos()[1])
        if playerDist == 1:
            validDirections += self.get_valid_directions(otherP.get_pos(), self.walls)
        for d in validDirections:
            if self.is_valid_move([d]):
                moves.append([d])
        for row in range(8):
            for col in range(8):
                for d in ["h", "v"]:
                    if self.is_valid_move([(row, col), d]):
                        moves.append([(row, col), d])
        return moves

    def make_move(self, move):
        p = self.p1 if self.turn == 0 else self.p2
        if len(move) == 2:
            self.walls.append(move)
            p.lose_wall()
        else:
            p.update_pos(move[0])
        self.turn = 1 - self.turn

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

gs = GameState()
print(gs.toString())
gs.make_move([(7,4)])
gs.make_move([(1,4)])
print(gs.toString())
gs.make_move([(6,4)])
gs.make_move([(2,4)])
print(gs.toString())
gs.make_move([(5,4)])
gs.make_move([(3,4)])
print(gs.toString())
gs.make_move([(4,4)])
gs.make_move([(4,3)])
print(gs.toString())


    