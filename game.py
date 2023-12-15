from state import GameState
from mini_model import MinimaxModel
from q_model import QModel

def play_game(gs, m):
    while not gs.is_game_over():
        print(gs.toString())
        if gs.turn == 0:
            userInp = input("Enter move: ").split()
            if len(userInp) < 2:
                print("\nINVALID MOVE\n")
                continue
            pos = (int(userInp[0]), int(userInp[1]))
            move = [pos]
            if len(userInp) == 3:
                move = [pos, userInp[2]]
            if not gs.is_valid_move(move):
                print("\nINVALID MOVE\n")
                continue
            
            gs.make_move(move)
        else:
            print("Computer's turn")
            m.make_move(gs)
    print(gs.toString())
    winner = gs.winner()
    if winner == 0:
        print("You win!")
    else:
        print("Computer wins!")


gs = GameState()
mm = MinimaxModel(2)
qmodel = QModel()

model_choice = input("Enter model choice (1 for minimax, 2 for q-learning): ")
m = mm if model_choice == "1" else qmodel

train = m == qmodel
if not train:
    print("Playing against minimax model\n")
    play_game(gs, m)
while train:
    gs.reset_game()
    print("NEXT GAME")
    play_game(gs, m)
    train = input("Keep Training? (y/n): ") != "y"