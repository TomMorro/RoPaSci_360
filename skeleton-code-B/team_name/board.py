# Finds a token given its location
def find_token(location, player):
    # Look in Rocks
    for cell in player["R"]:
        if cell == location:
            return "R"
    # Look in Scissors
    for cell in player["S"]:
        if cell == location:
            return "S"
    # Look in Papers
    for cell in player["P"]:
        if cell == location:
            return "P"

    return 0


# Determine if there were any tokens eat as a result a move
def find_eats(token_type, location, our_tokens, opponents_tokens):
    # Rock eats Scissors
    if token_type == "R":
        for cell in our_tokens["S"]:
            if cell == location:
                our_tokens["S"].remove(cell)
        for cell in opponents_tokens["S"]:
            if cell == location:
                opponents_tokens["S"].remove(cell)

    # Scissors eats Paper
    if token_type == "S":
        for cell in our_tokens["P"]:
            if cell == location:
                our_tokens["P"].remove(cell)
        for cell in opponents_tokens["P"]:
            if cell == location:
                opponents_tokens["P"].remove(cell)

    # Paper eats Rock
    if token_type == "P":
        for cell in our_tokens["R"]:
            if cell == location:
                our_tokens["R"].remove(cell)
        for cell in opponents_tokens["R"]:
            if cell == location:
                opponents_tokens["R"].remove(cell)
