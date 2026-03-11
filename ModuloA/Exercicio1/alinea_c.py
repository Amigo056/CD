#(c) Apresenta na consola os primeiros N termos da progressão aritmética de primeiro termo u e razão r. Os valores de N,u e r são passados como parâmetro.
from test import test

def progressao_aritmetica(N, u, r):
    result = []
    for i in range(N):
        result.append(str(u))
        u += r
    return ', '.join(result)


def main():
    test(progressao_aritmetica(10, 1, 2), '1, 3, 5, 7, 9, 11, 13, 15, 17, 19')

if __name__ == "__main__":
    main()