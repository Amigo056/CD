from pathlib import Path

# Funcoes auxiliares para trabalhar ao nivel dos bits.
# Como os codigos de repeticao repetem bits, e mais simples converter
# primeiro o conteudo dos ficheiros para listas de 0s e 1s.
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

# Funcoes simples de leitura/escrita de ficheiros quando o conteudo esta
# representado como lista de bits.
def write_bits(filename, bits):
    # Recebe uma lista de bits, converte para bytes e escreve num ficheiro.
    with open(filename, "wb") as f:
        f.write(bits_to_bytes(bits))


def read_bits(filename):
    # Le um ficheiro em binario e devolve o seu conteudo como lista de bits.
    with open(filename, "rb") as f:
        return bytes_to_bits(f.read())
    
def remove_file(filename):
    # Remove ficheiros temporarios usados apenas durante os calculos.
    Path(filename).unlink(missing_ok=True)