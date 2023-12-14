from state import GameState
from mini_model import MinimaxModel

gs = GameState()
mm = MinimaxModel(2)
turn = 0

while not gs.is_game_over():
    print(gs.toString())
    if turn == 0:
        userInp = input("Enter move: ").split()
        pos = (int(userInp[0]), int(userInp[1]))
        move = [pos]
        if len(userInp) == 3:
            move = [pos, userInp[2]]
        gs.make_move(move, turn)
    else:
        print("Computer's turn")
        mm.make_move(gs)
    turn = 1 - turn