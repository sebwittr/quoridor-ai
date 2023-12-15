from state import GameState
from mini_model import MinimaxModel
from q_model import QModel

gs = GameState()
mm = MinimaxModel(2)
qmodel = QModel()

model_choice = input("Enter model choice (1 for minimax, 2 for q-learning): ")
m = mm if model_choice == "1" else qmodel

while not gs.is_game_over():
    print(gs.toString())
    if gs.turn == 0:
        userInp = input("Enter move: ").split()
        pos = (int(userInp[0]), int(userInp[1]))
        move = [pos]
        if len(userInp) == 3:
            move = [pos, userInp[2]]
        gs.make_move(move)
    else:
        print("Computer's turn")
        m.make_move(gs)

winner = gs.winner()
if winner == 0:
    print("You win!")
else:
    print("Computer wins!")