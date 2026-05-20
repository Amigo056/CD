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
    P = 0.01

    output_folder = Path("ModuloB/Part1/SingleBitErrorResults")
    output_folder.mkdir(parents=True, exist_ok=True)
    input_folder = Path("ModuloB/TestFiles")
    for file_path in input_folder.glob("*"):
        if file_path.is_file(): # Garante que processa apenas ficheiros e ignora subpastas
            single_bit_error(file_path, output_folder / file_path.name, P)

    # Com semente
    output_folder_seeded = Path("ModuloB/Part1/SingleBitErrorResultsSeeded")
    output_folder_seeded.mkdir(parents=True, exist_ok=True)
    for file_path in input_folder.glob("*"):
        if file_path.is_file():
            single_bit_error(file_path, output_folder_seeded / file_path.name, P, random_seed=True)


    # ---- TESTE 2: Imagens ----
    input_images = Path("ModuloB/TestImages")
    
    # Sem semente
    output_images = Path("ModuloB/Part1/SingleBitErrorImages")
    output_images.mkdir(parents=True, exist_ok=True)
    for img_path in input_images.glob("*"):
        if img_path.is_file():
            single_bit_error(img_path, output_images / img_path.name, P)

    # Com semente
    output_images_seeded = Path("ModuloB/Part1/SingleBitErrorImagesSeeded")
    output_images_seeded.mkdir(parents=True, exist_ok=True)
    for img_path in input_images.glob("*"):
        if img_path.is_file():
            single_bit_error(img_path, output_images_seeded / img_path.name, P, random_seed=True)

if __name__ == "__main__":
    main()