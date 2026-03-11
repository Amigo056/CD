# (g) Determina e imprime os elementos sem repetições (reunião) entre dois vetores v1 e v2 de inteiros, passados como parâmetro.
from test import test

def vectorUnion(v1, v2):
    result = list(set(v1) | set(v2))
    
    return result
def main():
    vector_a = [1, 2, 3, 4, 5]
    vector_b = [4, 5, 6, 7, 8]
    vector_c = [1, 1, 2, 2, 3]

    test(vectorUnion(vector_a, vector_b), [1, 2, 3, 4, 5, 6, 7, 8])
    test(vectorUnion(vector_a, vector_c), vector_a)
    test(vectorUnion(vector_a, vector_a), vector_a)

if __name__ == '__main__':
    main()