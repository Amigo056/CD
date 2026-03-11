# (b) Determina e imprime na consola o mínimo múltiplo comum entre dois números inteiros a e b.
import math
from test import test

def lcm(a, b): 
    result = math.lcm(a,b)
    return result

def main():
    test(lcm(12, 18), 36)
    test(lcm(20, 30), 60)
    test(lcm(6, 30), 30)

if __name__ == '__main__':
    main()