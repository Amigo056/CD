import statistics

v = [2, 5, 1, 12, 25, 12, 2, 99, 67]

def data(vector):
    minimum = min(vector)
    maximum = max(vector)
    mean = statistics.mean(vector)
    mode = statistics.mode(vector)
    print(f"In this vector\nThe minimum is {minimum}\nThe maximum is {maximum}\nThe mean is {mean}\nThe mode is {mode}")

data(v)
