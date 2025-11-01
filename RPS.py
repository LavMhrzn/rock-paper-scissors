# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
import random

def player(prev_play, opponent_history=[]):
    opponent_history.append(prev_play)

    guess = "R"
    if len(opponent_history) > 2:
        guess = opponent_history[-2]

    return guess


def lm_player(prev_play, opponent_history=[], my_history=[]):
    if prev_play != '':
        opponent_history.append(prev_play)

    # Detect stage
    if len(opponent_history) < 5:
        # Start random for first few rounds
        move = random.choice(["R", "P", "S"])
        my_history.append(move)
        return move