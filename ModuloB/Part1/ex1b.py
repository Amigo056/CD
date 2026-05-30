import random
from pathlib import Path



def burst_bit_error_bytes(data, B):
    # Aplica a rajada diretamente sobre bytes e devolve uma nova copia alterada.
    output = bytearray(data)

    # Calcula o numero total de bits e escolhe onde a rajada vai comecar.
    total_bits = len(output) * 8
    if B < 0 or B > total_bits:
        raise ValueError("B tem de estar entre 0 e o numero total de bits dos dados")

    start = random.randint(0, total_bits - B) if B > 0 else 0

    # Inverte os B bits consecutivos da rajada.
    for i in range(start, start + B):
        output[i // 8] ^= 1 << (7 - (i % 8))

    return bytes(output)


def burst_bit_error(input_file, output_file, B):
    # Le o ficheiro em modo binario para funcionar com texto, imagens, codigo, etc.
    with open(input_file, "rb") as f:
        data = f.read()

    # Reutiliza a funcao pura sobre bytes.
    output = burst_bit_error_bytes(data, B)

    # Guarda o ficheiro resultante depois da introducao dos erros.
    with open(output_file, "wb") as f:
        f.write(output)

    # Devolve os bytes alterados para permitir reutilizacao.
    return output


def count_bit_errors(file1, file2):
    # Le os dois ficheiros em binario para comparar byte a byte.
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        data1 = f1.read()
        data2 = f2.read()

    # XOR mostra os bits diferentes; bit_count conta quantos bits mudaram.
    return sum((b1 ^ b2).bit_count() for b1, b2 in zip(data1, data2))


def main():
    # Dimensao da rajada usada em todos os testes.
    B = 10

    # Testa a funcao nos ficheiros de texto/codigo.
    input_folder = Path("ModuloB/TestFiles")
    output_folder = Path("ModuloB/Part1/BurstFilesResults")
    output_folder.mkdir(exist_ok=True)
    test_burst_bit_error(input_folder, output_folder, B)

    # Testa a funcao nas imagens.
    input_folder = Path("ModuloB/TestImages")
    output_folder = Path("ModuloB/Part1/BurstImagesResults")
    output_folder.mkdir(exist_ok=True)
    test_burst_bit_error(input_folder, output_folder, B)


def test_burst_bit_error(input_folder, output_folder, B):
    # Percorre todos os ficheiros da pasta de entrada.
    for input_file in input_folder.iterdir():
        if not input_file.is_file():
            continue

        # Cria o nome do ficheiro de saida mantendo a mesma extensao.
        output_file = output_folder / f"{input_file.stem}_burst{input_file.suffix}"

        # Aplica a rajada e confirma quantos bits foram alterados.
        with open(input_file, "rb") as f:
            input_data = f.read()

        output_data = burst_bit_error_bytes(input_data, B)
        with open(output_file, "wb") as f:
            f.write(output_data)

        errors = sum((b1 ^ b2).bit_count() for b1, b2 in zip(input_data, output_data))

        # Apresenta os resultados do teste para este ficheiro.
        print("Ficheiro:", input_file.name)
        print("Bits alterados:", errors)
        print("Esperado:", str(B)+"\n")


if __name__ == "__main__":
    main()
