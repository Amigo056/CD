
import string
import random
import os
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

    password = "".join(symbol_source(passalph, p, 20,))
    

    return password

passwordGenerator(3)

def main():
    N = 2500

    dir_script = os.path.dirname(os.path.abspath(__file__))
    pasta_saida = os.path.join(dir_script, "ex2Results")
    caminho_log = os.path.join(pasta_saida, "passwords3.txt")

    with open(caminho_log, "w", encoding="utf-8") as log_file:
        for i in range(N):
            strength = random.randint(1, 3)
            
            password = passwordGenerator(strength)
            print(f"Generated password: {password} with strength {strength}")
            log_file.write(password + "\n")


if __name__ == "__main__":
    main()