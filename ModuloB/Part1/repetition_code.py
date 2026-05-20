from bit_utils import write_bits, read_bits
from ex1a import single_bit_error

# Funcoes do codigo de repeticao.
# A codificacao repete cada bit n vezes; a descodificacao decide por maioria.
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

# Simulacao com codigo de repeticao.
# Fluxo: ficheiro original -> codificacao -> canal -> descodificacao -> saida.
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