
import random

def symbol_source(alphabet, probabilities, n_symbols, filename = ""):
    
    if abs(sum(probabilities) - 1.0) > 1e-9:
        print("The sum of the probabilities don't equal 1.")
        return

    if len(alphabet) != len(probabilities):
        print("Alphabet size is not the same as the ammout of probabilities given.")
        return

    seq = random.choices(alphabet, weights = probabilities, k = n_symbols)
    
    output = "".join(map(str, seq))
    
    if filename != "":
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(output)
    
    return seq


X = ['A', 'B', 'C']
P = [0.1, 0.7, 0.2]  
N = 1000

symbol_source(X, P, N, "ex2alineaA_Output.txt")

