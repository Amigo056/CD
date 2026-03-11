import math

val1 = 12

val2 = 18

def lcm(a, b): 
    result = math.lcm(a,b)
    return result

def main():
    result = lcm(val1, val2)
    print(f"the least common multiple of {val1} and {val2} is {result}")

main()
