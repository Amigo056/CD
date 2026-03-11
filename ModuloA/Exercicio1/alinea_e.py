# (e) Cálculo e listagem na consola dos valores mínimo, máximo, médio e a moda, de um vetor v de valores reais, passado como parâmetro.
import statistics
from test import test

def data(v):
    minimum = min(v)
    maximum = max(v)
    mean = statistics.mean(v)
    mode = statistics.mode(v)
    return [minimum, maximum, mean, mode]

v1 = [2, 5, 1, 12, 25, 12, 2, 99, 67]
v2 = [1, 1, 1, 1, 1, 1, 1]
v3 = [1, 2, 3, 4, 5, 6, 7, 8, 9]

test(data(v1), [1, 99, 25, 2])
test(data(v2), [1, 1, 1, 1])
test(data(v3), [1, 9, 5, 1])