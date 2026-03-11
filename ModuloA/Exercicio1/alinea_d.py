# (d) Cálculo e apresentação das raízes de uma equação de segundo grau ax2 + bx + c = 0, com coeficientes a, b e c passados como parâmetro.
from test import test

def calcular_raizes(a, b, c):
    delta = b**2 - 4*a*c
    if delta < 0:
        return 'A equação não tem raízes reais.'
    elif delta == 0:
        raiz = -b / (2*a)
        return f'A equação tem uma raiz real: {raiz:.2f}.'
    else:
        raiz1 = (-b + delta**0.5) / (2*a)
        raiz2 = (-b - delta**0.5) / (2*a)
        return f'A equação tem duas raízes reais: {raiz1:.2f} e {raiz2:.2f}.'
    
def main():
    test(calcular_raizes(1, -3, 2), 'A equação tem duas raízes reais: 2.00 e 1.00.')
    test(calcular_raizes(1, -2, 1), 'A equação tem uma raiz real: 1.00.')
    test(calcular_raizes(1, 0, 1), 'A equação não tem raízes reais.')

if __name__ == "__main__":
    main()