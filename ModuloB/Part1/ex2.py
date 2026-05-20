# 2. Correcao de erros isolados
# Simulacao com:
#   (i) ausencia de codigos de controlo de erros
#   (ii) codigo de repeticao (3,1)
#   (iii) codigo de repeticao (5,1)

from pathlib import Path
from ex1a import single_bit_error


def bytes_to_bits(data):
    # Converte cada byte do ficheiro numa lista de bits.
    # Exemplo: um ficheiro com N bytes passa a ter N * 8 bits.
    bits = []
    for byte in data:
        for bit_pos in range(8):
            bits.append((byte >> bit_pos) & 1)
    return bits


def bits_to_bytes(bits):
    # Faz a operacao inversa: junta os bits em grupos de 8 para voltar a bytes.
    # Isto permite gravar novamente o resultado como ficheiro.
    data = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for bit_pos, bit in enumerate(bits[i:i + 8]):
            byte |= bit << bit_pos
        data.append(byte)
    return data


def encode_repetition(bits, n):
    # Codigo de repeticao (n,1): cada bit de informacao e repetido n vezes.
    # Para n = 3: 1 -> 111 e 0 -> 000.
    encoded = []
    for bit in bits:
        encoded.extend([bit] * n)
    return encoded


def decode_repetition(bits, n):
    # Descodificacao por maioria.
    # Para n = 3, se pelo menos 2 bits forem 1, o resultado e 1.
    # Para n = 5, se pelo menos 3 bits forem 1, o resultado e 1.
    decoded = []
    for i in range(0, len(bits), n):
        block = bits[i:i + n]
        decoded.append(1 if sum(block) > n // 2 else 0)
    return decoded


def write_bits(filename, bits):
    # Recebe uma lista de bits, converte para bytes e escreve num ficheiro.
    with open(filename, "wb") as f:
        f.write(bits_to_bytes(bits))


def read_bits(filename):
    # Le um ficheiro em binario e devolve o seu conteudo como lista de bits.
    with open(filename, "rb") as f:
        return bytes_to_bits(f.read())


def simulate_without_code(input_file, output_file, p):
    # Configuracao (i): ficheiro original passa diretamente pelo canal.
    # Nao existe codificacao nem correcao.
    single_bit_error(input_file, output_file, p, True)


def simulate_with_repetition(input_file, encoded_file, channel_file, output_file, p, n):
    # Configuracoes (ii) e (iii): primeiro codifica com repeticao.
    bits = read_bits(input_file)
    encoded_bits = encode_repetition(bits, n)
    write_bits(encoded_file, encoded_bits)

    # Depois passa o ficheiro codificado pelo canal single_bit_error.
    single_bit_error(encoded_file, channel_file, p, True)

    # Por fim, descodifica por maioria e grava o ficheiro recuperado.
    received_bits = read_bits(channel_file)
    decoded_bits = decode_repetition(received_bits, n)
    write_bits(output_file, decoded_bits)


def main():
    # Valores escolhidos para testar desde erro baixo ate erro elevado.
    probabilities = [0.001, 0.01, 0.05, 0.1]

    # Caminhos base: assim o script funciona mesmo sendo executado de outra pasta.
    base_dir = Path(__file__).resolve().parent
    modulo_b_dir = base_dir.parent

    # Dois ficheiros de teste escolhidos para a simulacao.
    input_files = [
        modulo_b_dir / "TestFiles" / "a.txt",
        modulo_b_dir / "TestFiles" / "fibonacci.kt",
    ]

    # Pasta onde vao ficar todos os ficheiros produzidos pela simulacao.
    results_dir = base_dir / "Ex2Results"
    results_dir.mkdir(exist_ok=True)

    # Para cada ficheiro e para cada p, testa as tres configuracoes pedidas.
    for input_file in input_files:
        for p in probabilities:
            p_name = str(p).replace(".", "_")

            # (i) Sem codigo de controlo de erros.
            no_code_output = results_dir / f"{input_file.stem}_p{p_name}_sem_codigo{input_file.suffix}"
            simulate_without_code(input_file, no_code_output, p)

            # (ii) Codigo de repeticao (3,1).
            rep3_encoded = results_dir / f"{input_file.stem}_p{p_name}_rep3_codificado.bin"
            rep3_channel = results_dir / f"{input_file.stem}_p{p_name}_rep3_canal.bin"
            rep3_output = results_dir / f"{input_file.stem}_p{p_name}_rep3_saida{input_file.suffix}"
            simulate_with_repetition(input_file, rep3_encoded, rep3_channel, rep3_output, p, 3)

            # (iii) Codigo de repeticao (5,1).
            rep5_encoded = results_dir / f"{input_file.stem}_p{p_name}_rep5_codificado.bin"
            rep5_channel = results_dir / f"{input_file.stem}_p{p_name}_rep5_canal.bin"
            rep5_output = results_dir / f"{input_file.stem}_p{p_name}_rep5_saida{input_file.suffix}"
            simulate_with_repetition(input_file, rep5_encoded, rep5_channel, rep5_output, p, 5)

            # Mostra no terminal quais os ficheiros criados.
            print("Ficheiro:", input_file.name, "| p =", p)
            print("  sem codigo ->", no_code_output.name)
            print("  repeticao (3,1) ->", rep3_output.name)
            print("  repeticao (5,1) ->", rep5_output.name)
            print()


if __name__ == "__main__":
    main()
