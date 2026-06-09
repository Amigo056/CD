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
