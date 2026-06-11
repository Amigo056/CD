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
    """Codifica 4 bits de dados em 7 bits (Hamming 7,4)"""
    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4
    return [d1, d2, d3, d4, p1, p2, p3]

def hamming_decode_7bits(bloco):
    """
    Recebe uma lista de 7 bits [d1, d2, d3, d4, p1, p2, p3].
    Deteta se há erro, corrige se for erro de 1 bit, e devolve os 4 bits originais.
    """
    d1, d2, d3, d4, p1, p2, p3 = bloco

    # Calcular os síndromas de erro (XOR entre o que devia ser e o que veio)
    s1 = p1 ^ (d1 ^ d2 ^ d4)
    s2 = p2 ^ (d1 ^ d3 ^ d4)
    s3 = p3 ^ (d2 ^ d3 ^ d4)

    # O valor do síndroma indica a posição do erro (em binário: s3 s2 s1)
    # Convertendo para decimal para saber qual bit falhou:
    posicao_erro = (s3 << 2) | (s2 << 1) | s1
    
    erro_detetado = posicao_erro != 0
    erro_corrigido = False

    if posicao_erro != 0:
        print(f"  [HAMMING] Erro detetado no bit posição (s3s2s1 binário): {posicao_erro}")
        
        # Mapeamento padrão da posição do erro para o bit correspondente na nossa lista:
        # Se alteraste a ordem dos bits na tua aula, ajusta este dicionário!
        mapeamento_posicao = {
            1: 4,  # p1 falhou (índice 4 na lista)
            2: 5,  # p2 falhou (índice 5 na lista)
            4: 6,  # p3 falhou (índice 6 na lista)
            3: 0,  # d1 falhou (índice 0 na lista)
            5: 1,  # d2 falhou (índice 1 na lista)
            6: 2,  # d3 falhou (índice 2 na lista)
            7: 3   # d4 falhou (índice 3 na lista)
        }
        
        if posicao_erro in mapeamento_posicao:
            idx = mapeamento_posicao[posicao_erro]
            erro_corrigido = True
            bloco[idx] ^= 1  # Faz o 'flip' do bit para o corrigir!
            print(f"  [HAMMING] Bit corrigido com sucesso!")
    else:
        print("  [HAMMING] Bloco verificado. Sem erros.")

    # Devolve apenas os 4 bits de dados originais [d1, d2, d3, d4]
    return bloco[0:4], erro_detetado, erro_corrigido

def byte_to_bits(valor):
    return [(valor >> i) & 1 for i in range(7, -1, -1)]

    
def codificar_texto_hamming(texto):
    """
    Recebe uma string e devolve um bytearray com os bits '0' e '1'
    da mensagem codificada em Hamming.
    Cada byte origina 2 blocos Hamming(7,4), totalizando 14 bits por byte.
    """
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


def descodificar_texto_hamming(bits_data):
    """
    Recebe uma sequência codificada em Hamming (bytearray, bytes ou string),
    corrige erros simples e reconstrói o texto original.
    """
    if isinstance(bits_data, str):
        bits_string = bits_data.strip()
    else:
        bits_string = bytes(bits_data).decode("utf-8").strip()

    if len(bits_string) % 14 != 0:
        raise ValueError("A sequência de bits deve ter comprimento múltiplo de 14.")

    lista_bits = [int(b) for b in bits_string]

    bytes_resultado = bytearray()
    erros_detetados = 0
    erros_corrigidos = 0

    for i in range(0, len(lista_bits), 14):
        bloco1 = lista_bits[i:i+7]
        bloco2 = lista_bits[i+7:i+14]

        nibble1_bits, erro1, corrigido1 = hamming_decode_7bits(bloco1)
        nibble2_bits, erro2, corrigido2 = hamming_decode_7bits(bloco2)

        erros_detetados += int(erro1) + int(erro2)
        erros_corrigidos += int(corrigido1) + int(corrigido2)

        nibble_alto = bits_para_nibble(nibble1_bits)
        nibble_baixo = bits_para_nibble(nibble2_bits)

        byte = (nibble_alto << 4) | nibble_baixo
        bytes_resultado.append(byte)

    texto = bytes_resultado.decode("utf-8", errors="replace")

    return texto, erros_detetados, erros_corrigidos

def hamming_decode_file(nome_ficheiro):
   
    with open(nome_ficheiro, "rb") as f:
        dados_codificados = f.read()

    texto_descodificado, erros_detetados, erros_corrigidos = descodificar_texto_hamming(dados_codificados)
   
    with open(nome_ficheiro, "w", encoding="utf-8") as f:
        f.write(texto_descodificado)

    return texto_descodificado, erros_detetados, erros_corrigidos

def main():
    texto_original = "The quick brown fox jumps over the lazy dog!"
    print(f"Texto original: {texto_original}")

    texto_codificado = codificar_texto_hamming(texto_original)
    print(f"Texto codificado (bits): {texto_codificado.decode('utf-8')}")

    # Simular um erro introduzindo um bit errado
    if len(texto_codificado) > 10:
        texto_codificado[10] ^= 1  # Inverte um bit para simular erro

    texto_descodificado, erros_detetados, erros_corrigidos = descodificar_texto_hamming(texto_codificado)
    print(f"Texto descodificado: {texto_descodificado}")
    print(f"Erros detetados: {erros_detetados}, Erros corrigidos: {erros_corrigidos}")
    
    
if __name__ == "__main__":
    main()  