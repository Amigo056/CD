import random
from pathlib import Path


def burst_bit_error(input_file, output_file, B):
    with open(input_file, "rb") as f:
        data = bytearray(f.read())

    total_bits = len(data) * 8
    start = random.randint(0, total_bits - B)

    for i in range(start, start + B):
        data[i // 8] ^= 1 << (7 - (i % 8))

    with open(output_file, "wb") as f:
        f.write(data)

    return start


def count_bit_errors(file1, file2):
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        data1 = f1.read()
        data2 = f2.read()

    return sum((b1 ^ b2).bit_count() for b1, b2 in zip(data1, data2))


def main():
    B = 10
    input_folder = Path("ModuloB/TestFiles")
    output_folder = Path("ModuloB/Part1/BurstFilesResults")
    output_folder.mkdir(exist_ok=True)

    test_burst_bit_error(input_folder, output_folder, B)

    input_folder = Path("ModuloB/TestImages")
    output_folder = Path("ModuloB/Part1/BurstImagesResults")
    output_folder.mkdir(exist_ok=True)
    test_burst_bit_error(input_folder, output_folder, B)

def test_burst_bit_error(input_folder, output_folder, B):
    for input_file in input_folder.iterdir():
        if not input_file.is_file():
            continue

        output_file = output_folder / f"{input_file.stem}_burst{input_file.suffix}"
        start = burst_bit_error(input_file, output_file, B)
        errors = count_bit_errors(input_file, output_file)

        print("Ficheiro:", input_file.name)
        print("Inicio da rajada:", start)
        print("Bits alterados:", errors)
        print("Esperado:", str(B)+"\n")

if __name__ == "__main__":
    main()
