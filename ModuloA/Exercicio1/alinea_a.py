#(a) Determina e imprime na consola todos os números múltiplos de seis, contidos no intervalo definido por a e a2, inclusivamente
from test import test


def multiplos_de_seis(a, a2):
    result = []
    for i in range(a, a2 + 1):
        if i % 6 == 0:
            result.append(str(i))
    return ', '.join(result)

def main():
    test(multiplos_de_seis(1, 20), '6, 12, 18')

if __name__ == "__main__":
    main()