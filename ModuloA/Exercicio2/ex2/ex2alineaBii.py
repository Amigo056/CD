
from ex2alineaA import symbol_source

def lottery(n):
    numbers = list(range(1, 51)) 
    np = [1/50] * 50
    stars = list(range(1, 13))
    sp = [1/12] * 12

    output = "This weeks key: "

    winnerNumbers = symbol_source(numbers, np, 5, "winnerNumbers.txt")
    winnerStars = symbol_source(stars, sp, 2, "winnerStars.txt")
    winnerstatus = False
    winnerBet = []

    output += f"Numbers: {winnerNumbers} Stars: {winnerStars}\n\n"
    output += "And this weeks bets were:\n"

    for i in range(n):
        betN = symbol_source(numbers, np, 5)
        betS = symbol_source(stars, sp, 2)
        output += f"\nBet {i+1}: Numbers: {betN} Stars: {betS} "
        if sorted(betN) == sorted(winnerNumbers) and sorted(betS) == sorted(winnerStars):
            print("We have a winner!!!!")
            output += "Winner------------------"
            winnerstatus = True
            winnerBet = winnerBet.append(i + 1)
        else:
             print("Not a winner")
             output += ("Not a winner")
    
    if winnerstatus == False:
        output += "\n\nUnfortunatly there was no winner this week."
    elif winnerBet.__sizeof__ == 1:
        output += f"\n\nThe winner bet this week was number {winnerBet[0]}"
    else:
        output += f"\n\nThis weeks winners were bets number: {winnerBet}"

    with open("2Bii_output.txt", 'w', encoding='utf-8') as f:
            f.write(output)

    return


lottery(20000)