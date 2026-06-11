from random import random
from random import seed
from pathlib import Path

def single_bit_error_bits(bits_data, p, random_seed=False):
    if random_seed:
        seed(42)

    if isinstance(bits_data, (bytes, bytearray)):
        bits_string = bytes(bits_data).decode("utf-8").strip()
    else:
        bits_string = str(bits_data).strip()

    bits = [c for c in bits_string if c in ("0", "1")]

    if not (0 <= p <= 1):
        raise ValueError("p tem de estar entre 0 e 1")

    for i in range(len(bits)):
        if random() < p:
            bits[i] = "1" if bits[i] == "0" else "0"

    return "".join(bits)

def single_bit_error(input_file, output_file, p, random_seed=False):
    # Lê o ficheiro em modo binário.
    with open(input_file, "rb") as file_in:
        data = file_in.read()

    # Aplica erros independentes bit a bit.
    output = single_bit_error_bits(data, p, random_seed=random_seed)

    # Guarda o ficheiro alterado.
    with open(output_file, "wb") as file_out:
        file_out.write(output)

    return output
