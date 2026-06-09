import random
from pathlib import Path


def burst_bit_error(input_file, output_file, B):
    # Le o ficheiro em modo binario para funcionar com texto, imagens, codigo, etc.
    with open(input_file, "rb") as f:
        data = bytearray(f.read())

    # Calcula o numero total de bits e escolhe onde a rajada vai comecar.
    total_bits = len(data) * 8
    start = random.randint(0, total_bits - B)

    # Inverte os B bits consecutivos da rajada.
    for i in range(start, start + B):
        data[i // 8] ^= 1 << (7 - (i % 8))

    # Guarda o ficheiro resultante depois da introducao dos erros.
    with open(output_file, "wb") as f:
        f.write(data)

    # Devolve a posicao inicial para ser possivel confirmar o teste.
    return start


