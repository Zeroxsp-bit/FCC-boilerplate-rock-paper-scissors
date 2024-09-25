import random

# Mapeo de los movimientos ganadores
winning_moves = {"R": "P", "P": "S", "S": "R"}

# Estrategia de frecuencia
def most_frequent_move(opponent_history):
    if not opponent_history or opponent_history[-1] == '':  # Verifica si el historial está vacío
        return random.choice(["R", "P", "S"])  # Si no hay jugadas anteriores, juega aleatoriamente
    most_frequent = max(set(opponent_history), key=opponent_history.count)
    return winning_moves[most_frequent]

# Estrategia adaptativa basada en patrones
def pattern_based_strategy(history):
    if len(history) < 3:
        return random.choice(["R", "P", "S"])

    pattern_dict = {
        ("R", "R"): {"R": 0, "P": 0, "S": 0},
        ("R", "P"): {"R": 0, "P": 0, "S": 0},
        ("R", "S"): {"R": 0, "P": 0, "S": 0},
        ("P", "R"): {"R": 0, "P": 0, "S": 0},
        ("P", "P"): {"R": 0, "P": 0, "S": 0},
        ("P", "S"): {"R": 0, "P": 0, "S": 0},
        ("S", "R"): {"R": 0, "P": 0, "S": 0},
        ("S", "P"): {"R": 0, "P": 0, "S": 0},
        ("S", "S"): {"R": 0, "P": 0, "S": 0}
    }

    for i in range(len(history) - 2):
        seq = tuple(history[i:i+2])  # Convertir la lista a una tupla para usarla como clave
        next_move = history[i+2]
        if seq in pattern_dict:
            pattern_dict[seq][next_move] += 1

    last_two = tuple(history[-2:])  # Convertir la lista a tupla
    if last_two in pattern_dict:
        next_move_prediction = max(pattern_dict[last_two], key=pattern_dict[last_two].get)
        return winning_moves[next_move_prediction]

    return random.choice(["R", "P", "S"])

# Estrategia principal adaptativa
def player(prev_play, opponent_history=[], strategy_state={"wins": 0, "games": 0, "strategy": "frequency"}):
    # Si es la primera jugada, devuelve una jugada aleatoria
    if prev_play == "":
        return random.choice(["R", "P", "S"])

    opponent_history.append(prev_play)

    # Cambiar de estrategia si es necesario
    strategy_state["games"] += 1

    # Control de victorias
    if strategy_state["games"] > 10:  # Cambiar estrategia si no ganamos al menos el 60% en 10 juegos
        if strategy_state["wins"] / strategy_state["games"] < 0.6:
            if strategy_state["strategy"] == "frequency":
                strategy_state["strategy"] = "pattern"
            else:
                strategy_state["strategy"] = "frequency"
        strategy_state["games"] = 0
        strategy_state["wins"] = 0

    # Elegir estrategia actual
    if strategy_state["strategy"] == "frequency":
        next_move = most_frequent_move(opponent_history)
    else:
        next_move = pattern_based_strategy(opponent_history)

    # Determinar si la estrategia está funcionando (si ganamos el último juego)
    if winning_moves[prev_play] == next_move:
        strategy_state["wins"] += 1

    return next_move