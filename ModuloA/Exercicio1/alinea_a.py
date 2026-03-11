#(a) Determina e imprime na consola todos os números múltiplos de seis, contidos no intervalo definido por a e a2, inclusivamente
from test import test

def multiplos_de_seis(a):
    multiplos = []
    for num in range(a, a*a):
        if num % 6 == 0:
            multiplos.append(num)
    return multiplos

def main():
    test(multiplos_de_seis(6), [6, 12, 18, 24, 30, 36])
    test(multiplos_de_seis(3), [6])
    test(multiplos_de_seis(4), [6, 12])

if __name__ == "__main__":
    main()