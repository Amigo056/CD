def nibble_para_bits(n):
    return [
        (n >> 3) & 1,
        (n >> 2) & 1,
        (n >> 1) & 1,
        n & 1
    ]


def bits_para_nibble(bits4):
    return (bits4[0] << 3) | (bits4[1] << 2) | (bits4[2] << 1) | bits4[3]

def hamming_encode_nibble(d1, d2, d3, d4):
    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4
    return [d1, d2, d3, d4, p1, p2, p3]


def byte_to_bits(valor):
    return [(valor >> i) & 1 for i in range(7, -1, -1)]

    
def codificar_texto_hamming(texto):
    resultado = bytearray()

    for byte in texto.encode("utf-8"):
        nibble_alto = (byte >> 4) & 0x0F
        nibble_baixo = byte & 0x0F

        bits_alto = nibble_para_bits(nibble_alto)
        bits_baixo = nibble_para_bits(nibble_baixo)

        bloco1 = hamming_encode_nibble(*bits_alto)
        bloco2 = hamming_encode_nibble(*bits_baixo)

        for bit in bloco1:
            resultado.append(ord('0') + bit)

        for bit in bloco2:
            resultado.append(ord('0') + bit)

    return resultado


