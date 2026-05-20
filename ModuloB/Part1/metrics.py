def count_bit_errors(file1, file2):
    # Le os dois ficheiros em binario para comparar byte a byte.
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        data1 = f1.read()
        data2 = f2.read()

    # XOR mostra os bits diferentes; bit_count conta quantos bits mudaram.
    return sum((b1 ^ b2).bit_count() for b1, b2 in zip(data1, data2))

# O objetivo e procurar, experimentalmente, para que valores de p o BER'
# fica igual a zero depois da descodificacao por repeticao.
def calculate_final_ber(input_file, output_file):
    # Calcula o BER' entre o ficheiro original e o ficheiro final descodificado.
    information_bits = input_file.stat().st_size * 8
    return count_bit_errors(input_file, output_file) / information_bits