import random

def player(prev_play, opponent_history=[], my_history=[], strategy=['']):
    # Track opponent and self history
    if prev_play != '':
        opponent_history.append(prev_play)
    else:
        opponent_history.clear()
        my_history.clear()

    # Detect stage
    if len(opponent_history) < 5:
        # Start random for first few rounds
        my_move = random.choice(["R", "P", "S"])
        my_history.append(my_move)
        return my_move
    
    #Strategy for Quincy
    if IsBotQuincy(opponent_history):
        quincy_pattern = ["R", "P", "P", "S", "R"]
        rem = len(opponent_history) % len(quincy_pattern)
        my_move = counter_move(quincy_pattern[rem])
        my_history.append(my_move)
        return my_move

    #Strategy for kris
    if IsBotKris(opponent_history, my_history):
        my_move = counter_move(counter_move(my_history[-1]))
        my_history.append(my_move)
        return my_move

    #Strategy for Mrugesh
    if IsBotMrugesh(opponent_history, my_history):        
        my_last_ten = my_history[-10:]
        my_most_frequent = max(set(my_last_ten), key=my_last_ten.count)
        my_move = counter_move(counter_move(my_most_frequent))
        my_history.append(my_move)
        return my_move
    
    #Strategy for Abbey
    ThisIsAbbey, AbbeyPrediction = IsBotAbbey(opponent_history,my_history)
    if ThisIsAbbey:
        my_move = counter_move(AbbeyPrediction)
        my_history.append(my_move)
        return my_move

    # Fallback random
    my_move = random_move()
    my_history.append(my_move)
    return my_move

def IsBotQuincy(opponent_history):
    quincy_pattern = ["R", "P", "P", "S", "R"]
    ohl = len(opponent_history)
    qpl = len(quincy_pattern)
    rem = ohl % qpl
    for i in range(0, ohl-rem, qpl):
        if opponent_history[i:i+qpl] != quincy_pattern:
            return False
    return True

def IsBotAbbey(opponent_history, my_history) :
    play_order=[{"RR": 0,"RP": 0,"RS": 0,"PR": 0,"PP": 0,"PS": 0,"SR": 0,"SP": 0,"SS": 0,}]
    correct_predictions = 0
    total_checks = 0
    for i in range(1, len(my_history)):
        if i == 1:
            last_two = "R" + my_history[i-1]
        else :
            last_two = my_history[i-2] + my_history[i-1]
        play_order[0][last_two] += 1

        potential_plays = [
            my_history[i-1] + "R",
            my_history[i-1] + "P",
            my_history[i-1] + "S",
        ]
        sub_order = { k: play_order[0][k] for k in potential_plays if k in play_order[0] }
        prediction = max(sub_order, key=sub_order.get)[-1:]
        if opponent_history[i] == counter_move(prediction) :
            correct_predictions += 1
        
        total_checks += 1

    if total_checks == 0:
        return False, random_move()
    
    accuracy = correct_predictions / total_checks
    if accuracy < 0.6 :
        return False, random_move()
    
    last_two = "".join(my_history[-2:])
    play_order[0][last_two] += 1
    potential_plays = [
        my_history[-1] + "R",
        my_history[-1] + "P",
        my_history[-1] + "S",
    ]
    sub_order = { k: play_order[0][k] for k in potential_plays if k in play_order[0] }
    prediction = max(sub_order, key=sub_order.get)[-1:]
    return True, counter_move(prediction)

def IsBotKris(opponent_history, my_history):
    for i in range(1, len(opponent_history)):
        if opponent_history[i] != counter_move(my_history[i-1]):
            return False
    return True

def IsBotMrugesh(opponent_history, my_history):
    if len(my_history) < 10:
        return False
    ohl = len(opponent_history)
    for i in range(10, ohl):
        current_ten = my_history[i-10:i]
        most_frequent = max(set(current_ten), key=current_ten.count)
        if opponent_history[i] != counter_move(most_frequent):
            return False
    return True        

def random_move():
    return random.choice(["R", "P", "S"])

def counter_move(move):
    counter = {'R':'P','P':'S','S':'R'}
    countermove = counter[move]
    return countermove