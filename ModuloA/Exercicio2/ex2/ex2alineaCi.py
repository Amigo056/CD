
import string
from ex2alineaA import symbol_source

def passwordGenerator(strength):

    weakPass = list(string.ascii_lowercase)

    mediumPass = list(string.ascii_letters) + ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    strongPass = list(string.printable)[:-5]

    passalph = []

    if strength == 1:
        passalph = weakPass
    elif strength == 2:
        passalph = mediumPass
    elif strength == 3:
        passalph = strongPass
    else:
        return ""
    
    p = [1/len(passalph)] * len(passalph)

    password = symbol_source(passalph, p, 20, "password.txt")

    return password

passwordGenerator(3)