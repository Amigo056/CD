from PIL import Image
import secrets
import os;


def cifra_vernam(plain_bytes, key_bytes):
    resultado = bytearray()
    for p, k in zip(plain_bytes, key_bytes):
        resultado.append(p ^ k)
    return bytes(resultado)


def decifra_vernam(cipher_bytes, key_bytes):
    resultado = bytearray()
    for c, k in zip(cipher_bytes, key_bytes):
        resultado.append(c ^ k)
    return bytes(resultado)


def selecionar_retangulo(img, rect):
    if rect is None:
        return (0, 0, img.width, img.height)

    x, y, w, h = rect

    if w <= 0 or h <= 0:
        print("A largura e a altura têm de ser positivas.")

    left = max(0, x)
    upper = max(0, y)
    right = min(img.width, x + w)
    lower = min(img.height, y + h)

    if left >= right or upper >= lower:
        print("Retângulo inválido.")

    return (left, upper, right, lower)


def processar_imagem(plain_text, ficheiro_saida, ficheiro_chave,
                     modo="cifrar", rect=None):
    img = Image.open(plain_text).convert("RGB")

    box = selecionar_retangulo(img, rect)
    regiao = img.crop(box)

    dados = regiao.tobytes()

    if modo == "cifrar":
        chave = secrets.token_bytes(len(dados))
        novos_dados = cifra_vernam(dados, chave)
        with open(ficheiro_chave, "wb") as f:
            f.write(chave)

    elif modo == "decifrar":
        with open(ficheiro_chave, "rb") as f:
            chave = f.read()

        if len(chave) != len(dados):
            print("A chave não tem o tamanho correto para esta região.")

        novos_dados = decifra_vernam(dados, chave)

    else:
        print("Modo deve ser 'cifrar' ou 'decifrar'.")

    nova_regiao = Image.frombytes("RGB", regiao.size, novos_dados)

    resultado = img.copy()
    resultado.paste(nova_regiao, box)
    resultado.save(ficheiro_saida)



def main():
    files = ["barb.tif", "bird.png","bubbles.png" ,"goldhill.tif" ,"lena1.tif","lena3.tif", "mandrill.tif", "monarch.tif", "tulips.tif" ]
    rects = [(100, 50, 200, 120), (50, 50, 150, 150), (0, 0, 100, 100), (150, 150, 300, 300), (200, 200, 400, 400), (250, 250, 500, 500), (300, 300, 600, 600), (350, 350, 700, 700), (400, 400, 800, 800)]
    dir_script = os.path.dirname(os.path.abspath(__file__))
    pasta_entrada = os.path.join(dir_script, "Test Images")
    pasta_cifra = os.path.join(dir_script, "imagens_cifradas")
    pasta_decifra = os.path.join(dir_script, "imagens_decifradas")
    pasta_chaves = os.path.join(dir_script, "chaves")
    for file in files:
            file_entrada = os.path.join(pasta_entrada,file)
            file_cifra = os.path.join(pasta_cifra,f"cifrado_{file}")
            file_chave = os.path.join(pasta_chaves,f"{file}_key.key")
            file_decifra = os.path.join(pasta_decifra,f"decifrado_{file}")
            processar_imagem(
                plain_text=file_entrada,
                ficheiro_saida=file_cifra,
                ficheiro_chave=file_chave,
                modo="cifrar",
                rect=rects[files.index(file)]
            )
            
            processar_imagem(
                plain_text=file_cifra,
                ficheiro_saida=file_decifra,
                ficheiro_chave=file_chave,
                modo="decifrar",
                rect=rects[files.index(file)]
            )
            



if __name__ == "__main__":
    main()