from random import random
from random import seed
from pathlib import Path

def single_bit_error(input_file, output_file, p, random_seed = False):
    if random_seed:
        seed(42)

    with open(input_file, 'rb') as file_in:
        input = file_in.read()

    output = bytearray()

    for byte in input:
        new_byte = 0
        for bit_pos in range(8):
            bit = (byte >> bit_pos) & 1
                
            if random() < p:
                bit = bit ^ 1  
                
            new_byte |= (bit << bit_pos)
            
        output.append(new_byte)

    with open(output_file, 'wb') as file_out:
        file_out.write(output)
    
    return

def main():
    # Dimensao da rajada usada em todos os testes.
    P = 0,1

    # Testa a funcao nos ficheiros de texto/codigo.
    input_folder = Path("ModuloB/TestFiles")
    output_folder = Path("ModuloB/Part1/SingleBitErrorResults")
    output_folder.mkdir(exist_ok=True)
    single_bit_error(input_folder, output_folder, P)

    output_folder = Path("ModuloB/Part1/SingleBitErrorResultsSeeded")
    output_folder.mkdir(exist_ok=True)
    single_bit_error(input_folder, output_folder, P, True)

    # Testa a funcao nas imagens.
    input_folder = Path("ModuloB/TestImages")
    output_folder = Path("ModuloB/Part1/SingleBitErrorImages")
    output_folder.mkdir(exist_ok=True)
    single_bit_error(input_folder, output_folder, P)

    output_folder = Path("ModuloB/Part1/SingleBitErrorImagesSeeded")
    output_folder.mkdir(exist_ok=True)
    single_bit_error(input_folder, output_folder, P, True)

if __name__ == "__main__":
    main()