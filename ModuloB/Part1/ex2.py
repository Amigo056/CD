# 2. Correcao de erros isolados
# Simulacao com:
#   (i) ausencia de codigos de controlo de erros
#   (ii) codigo de repeticao (3,1)
#   (iii) codigo de repeticao (5,1)

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))
from ex1a import single_bit_error
from ex1b import count_bit_errors


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


def create_table_row(input_file, output_file, p, configuration,
                     channel_errors, final_errors, transmitted_bits, information_bits):
    # Cria uma linha com os valores pedidos na alinea b.
    return [
        input_file.name,
        str(p),
        configuration,
        f"{channel_errors / transmitted_bits:.6f}",
        f"{final_errors / information_bits:.6f}",
        str(transmitted_bits),
        str(information_bits),
        input_file.name,
        output_file.name,
    ]


def simulate_configuration(input_file, p, results_dir, configuration, repetition):
    # Simula uma das tres configuracoes e devolve a linha da tabela.
    information_bits = input_file.stat().st_size * 8
    p_name = str(p).replace(".", "_")

    if repetition is None:
        output_file = results_dir / f"{input_file.stem}_p{p_name}_sem_codigo{input_file.suffix}"
        simulate_without_code(input_file, output_file, p)

        errors = count_bit_errors(input_file, output_file)
        transmitted_bits = information_bits
        channel_errors = errors
        final_errors = errors
    else:
        prefix = f"rep{repetition}"
        encoded_file = results_dir / f"{input_file.stem}_p{p_name}_{prefix}_codificado.bin"
        channel_file = results_dir / f"{input_file.stem}_p{p_name}_{prefix}_canal.bin"
        output_file = results_dir / f"{input_file.stem}_p{p_name}_{prefix}_saida{input_file.suffix}"

        simulate_with_repetition(input_file, encoded_file, channel_file, output_file, p, repetition)

        transmitted_bits = information_bits * repetition
        channel_errors = count_bit_errors(encoded_file, channel_file)
        final_errors = count_bit_errors(input_file, output_file)

    row = create_table_row(
        input_file,
        output_file,
        p,
        configuration,
        channel_errors,
        final_errors,
        transmitted_bits,
        information_bits,
    )

    return row, output_file


def print_and_save_table(rows, table_file):
    headers = [
        "Ficheiro",
        "p",
        "Configuracao",
        "BER canal",
        "BER apos correcao",
        "Bits transmitidos",
        "Bits informacao",
        "Entrada",
        "Saida",
    ]

    table = []
    table.append("| " + " | ".join(headers) + " |")
    table.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        table.append("| " + " | ".join(row) + " |")

    text = "\n".join(table)
    print(text)

    with open(table_file, "w", encoding="utf-8") as f:
        f.write(text)


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

    configurations = [
        ("Sem codigo", None),
        ("Repeticao (3,1)", 3),
        ("Repeticao (5,1)", 5),
    ]

    table_rows = []

    # Para cada ficheiro e para cada p, testa as tres configuracoes pedidas.
    for input_file in input_files:
        for p in probabilities:
            print("Ficheiro:", input_file.name, "| p =", p)

            for configuration, repetition in configurations:
                row, output_file = simulate_configuration(
                    input_file,
                    p,
                    results_dir,
                    configuration,
                    repetition,
                )
                table_rows.append(row)
                print(" ", configuration, "->", output_file.name)

            print()

    print_and_save_table(table_rows, results_dir / "tabela_ex2b.md")


if __name__ == "__main__":
    main()
