# (f) Determina e imprime os elementos em comum (interseção) entre dois vetores v1 e v2 de inteiros, passados como parâmetro. Caso não existam elementos em comum, retorna vetor vazio.
from test import test

def elementos_intersetados(v1, v2):
    intersecao = []
    for i in v1:
        if i in v2:
            intersecao.append(str(i))
    return ', '.join(intersecao)


def main():
    test(elementos_intersetados([1, 2, 3, 4, 5, 6], [4, 5, 6, 7, 8]), '4, 5, 6')
    test(elementos_intersetados([1, 2, 3], [4, 5, 6]), '')

if __name__ == "__main__":
    main()