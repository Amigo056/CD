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
    origem_texto = Path("ModuloB/TestFiles/alice29.txt")
    corrompido_texto = Path("ModuloB/Part1/SingleBitErrorResults/alice29.txt")
    origem_imagem= Path("ModuloB/TestImages/bird.png")
    corrompido_imagem = Path("ModuloB/Part1/SingleBitErrorImages/bird.png")

    P = 0.01
    single_bit_error(origem_texto, corrompido_texto, P)
    single_bit_error(origem_imagem, corrompido_imagem, P)

    if origem_texto.exists() and corrompido_texto.exists():

        ber_value = calculate_ber(origem_texto, corrompido_texto)
        ser_value = calculate_ser(origem_texto, corrompido_texto)

        print(f"Resultados para o ficheiro {origem_texto.name}:")
        print(f"-> BER (Bit Error Rate):    {ber_value:.6f}")
        print(f"-> SER (Symbol Error Rate): {ser_value:.6f}")

    else:
        print("Os ficheiros de texto de teste não foram encontrados.")

    if origem_imagem.exists() and corrompido_imagem.exists():

        ber_value = calculate_ber(origem_imagem, corrompido_imagem)
        ser_value = calculate_ser(origem_imagem, corrompido_imagem)

        print(f"Resultados para o ficheiro {origem_imagem.name}:")
        print(f"-> BER (Bit Error Rate):    {ber_value:.6f}")
        print(f"-> SER (Symbol Error Rate): {ser_value:.6f}")

    else:
        print("Os ficheiros de imagem de teste não foram encontrados.")

if __name__ == "__main__":
    main()