import zlib
import ex1b


def crc32_value(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF


def encode_crc32(data: bytes) -> bytes:
    crc = crc32_value(data)
    crc_bytes = crc.to_bytes(4, byteorder="big")
    return data + crc_bytes


def check_crc32(data: bytes) -> bool:
    if len(data) < 4:
        return False

    payload = data[:-4]
    received_crc = int.from_bytes(data[-4:], byteorder="big")
    calculated_crc = crc32_value(payload)
    return payload,calculated_crc == received_crc



def main():
    msg = b"teste de mensagem para CRC32"
    frame = encode_crc32(msg)
    print(f"Frame: {frame.hex()}")
    new_frame = ex1b.burst_bit_error_bytes(frame, 0)  
    payload, is_valid = check_crc32(new_frame)
    print(f"Frame válido: {is_valid}")
    print(f"Novo frame: {new_frame.hex()}")
    
    




if __name__ == "__main__":
    main()    
    
