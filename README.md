# Pacman-Bot
Used AI for modeling the decision-making task as an adversarial search problem that allows the Pacman to decide actions while taking into account the behaviour of ghosts.
It uses min-max game tree search with alpha-beta pruning to determine optimal moves for pacman in the maze.
Next, we observed that ghosts in pacman don't take all optimal moves due to some randomization. To take advantage of this, expectimax tree search was implemented. 

Both bots performed very well compared to human performance. However, expectimax was a better performer than alpha-beta pruning in all our experiments.

### Declaration
This project was created by me with Swaraj in the Artificial Intelligence course at IIT Delhi. 
