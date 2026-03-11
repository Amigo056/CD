
vetor_a = [1, 2, 3, 4, 5]
vetor_b = [4, 5, 6, 7, 8]

def vectorUnion(v1, v2):
    result = list(set(v1) | set(v2))

    print(f"The vector with no repetitions is: {result}")
    
    return result

vectorUnion(vetor_a, vetor_b)
