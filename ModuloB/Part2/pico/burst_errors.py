import random
from pathlib import Path


def burst_bit_error_bits(bits_data, B):
    if isinstance(bits_data, (bytes, bytearray)):
        bits_string = bytes(bits_data).decode("utf-8").strip()
    else:
        bits_string = str(bits_data).strip()

    bits = [c for c in bits_string if c in ("0", "1")]

    total_bits = len(bits)
    if B < 0 or B > total_bits:
        raise ValueError("B tem de estar entre 0 e o número total de bits")

    start = random.randint(0, total_bits - B) if B > 0 else 0

    for i in range(start, start + B):
        bits[i] = "1" if bits[i] == "0" else "0"

    return "".join(bits)

def burst_bit_error(input_file, output_file, B):
    # Le o ficheiro em modo binario para funcionar com texto, imagens, codigo, etc.
    with open(input_file, "rb") as f:
        data = f.read()

    # Reutiliza a funcao pura sobre bytes.
    output = burst_bit_error_bits(data, B)

    # Guarda o ficheiro resultante depois da introducao dos erros.
    with open(output_file, "wb") as f:
        f.write(output)

    # Devolve os bytes alterados para permitir reutilizacao.
    return output


