
from ex2alineaA import symbol_source

def diceGame(l):
    dice = [1, 2, 3, 4, 5, 6]

    p = [1/6] * 6

    playerAresultsum = sum(symbol_source(dice, p, l, "playerAdiceHistogram.txt"))
    playerBresultsum = sum(symbol_source(dice, p, l, "playerBdiceHistogram.txt"))

    if playerAresultsum > playerBresultsum:
        print(f"Player A wins!!!! \n{playerAresultsum} to {playerBresultsum}")
    elif playerBresultsum > playerAresultsum:
        print(f"Player B wins!!!! \n{playerBresultsum} to {playerAresultsum}")
    else:
        print(f"it's a draw!!!! \n{playerAresultsum} to {playerBresultsum}")

    return

diceGame(10)