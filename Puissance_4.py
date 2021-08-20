    print("Tour n°", tour)
    if tour <= 3:
        DEPTH = 7
    elif tour <= 10:
        DEPTH = 9
    elif tour <= 15:
        DEPTH = 11
    elif tour <= 25:
        DEPTH = 13
    else:
        DEPTH = 15
