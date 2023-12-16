# About
This is an implementation of the game Quoridor with a built in AI player agent.

To learn more about Quoridor, click here: https://en.wikipedia.org/wiki/Quoridor

# Setup
Pull this repository and run 
`python3 game.py`

Then follow the on screen in instructions to configure your agent's model.

# Notes

## Minimax Search
https://en.wikipedia.org/wiki/Minimax
To adjust the search depth, change the constructor argument to your desired depth. Warning, any depth above 3 will likely not be performant.

## Q-Learning with linear approximation
https://en.wikipedia.org/wiki/Q-learning
To add new features, modify the `initialize_features` function in `q_model.py`
The other paramters are set in the constructor of QModel

