from pathlib import Path
from ex1a import single_bit_error

def calculate_ber(original_file, corrupted_file):

    with open(original_file, 'rb') as f_og:
        orig_data = f_og.read()

    with open(corrupted_file, 'rb') as f_corr:
        corr_data = f_corr.read()

    if len(orig_data) != len(corr_data):
        raise ValueError("Os ficheiros têm tamanhos diferentes.")

    total_bits = len(orig_data) * 8
    bit_errors = 0

    for b_og, b_corr in zip(orig_data, corr_data):
        diff = b_og ^ b_corr
        
        while diff > 0:
            bit_errors += diff & 1
            diff = diff >> 1

    ber = bit_errors / total_bits
    return ber


def calculate_ser(original_file, corrupted_file):

    with open(original_file, 'rb') as f_og:
        orig_data = f_og.read()

    with open(corrupted_file, 'rb') as f_corr:
        corr_data = f_corr.read()

    if len(orig_data) != len(corr_data):
        raise ValueError("Os ficheiros têm tamanhos diferentes.")

    total_bytes = len(orig_data)
    byte_errors = 0

    for b_orig, b_corr in zip(orig_data, corr_data):
        if b_orig != b_corr:
            byte_errors += 1

    ser = byte_errors / total_bytes
    return ser


def main():
    origem = Path("ModuloB/TestFiles/alice29.txt")
    corrompido = Path("ModuloB/Part1/SingleBitErrorResults/alice29.txt")

    single_bit_error(origem, corrompido, 0.01)

    if origem.exists() and corrompido.exists():

        ber_value = calculate_ber(origem, corrompido)
        ser_value = calculate_ser(origem, corrompido)

        print(f"Resultados para o ficheiro {origem.name}:")
        print(f"-> BER (Bit Error Rate):    {ber_value:.6f}")
        print(f"-> SER (Symbol Error Rate): {ser_value:.6f}")

    else:
        print("Os ficheiros de teste não foram encontrados.")

if __name__ == "__main__":
    main()