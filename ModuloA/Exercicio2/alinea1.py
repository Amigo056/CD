# 1. Análise de fontes de símbolos.
#   (a) Escreva uma função tal que sobre um ficheiro de entrada, realize as seguintes funcionalidades: (i) determina o símbolo
#       mais frequente, a respetiva probabilidade e a informação própria; (ii) o valor da entropia; (iii) apresente o respetivo
#       histograma.
#   
#   (b) Apresente os resultados obtidos pela função para os ficheiros do conjunto TestFilesCD.zip. Comente os resultados.

import matplotlib.pyplot as plt
import os
import utils

def draw_histogram_matplotlib(frequencias, titulo):
    """
    Gera histograma usando matplotlib - salva como imagem.
    Mostra: símbolo, frequência, probabilidade e informação própria.
    """
    simbolos = list(frequencias.keys())
    contagens = list(frequencias.values())
    
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(simbolos)), contagens, color='skyblue', edgecolor='black')
    
    if simbolos and isinstance(simbolos[0], int):
        # BINÁRIO: Mostrar como hex (0x00, 0x01, etc.)
        labels = [f"0x{s:02x}" for s in simbolos]
        plt.xlabel('Bytes (hexadecimal)')
    else:
        # TEXTO: Lógica original para caracteres
        labels = []
        for s in simbolos:
            if len(s) > 1 or not s.isprintable():
                labels.append(repr(s))
            else:
                labels.append(s)
        plt.xlabel('Caracteres')
    
    plt.xticks(range(len(simbolos)), labels, rotation=90, fontsize=8)
    plt.ylabel('Frequência Absoluta')
    plt.xlabel('Símbolos')
    plt.ylabel('Frequência Absoluta')
    plt.title(titulo)
    plt.tight_layout()

    
    dir_script = os.path.dirname(os.path.abspath(__file__))
    pasta_saida = os.path.join(dir_script, "ex1Results")
    
    file_name = os.path.splitext(titulo)[0]

    caminho_completo = os.path.join(pasta_saida, f"{file_name}.png")
    plt.savefig(caminho_completo, dpi=150)
    plt.show()


def file_scanner(file):
    
    conteudo, modo = utils.ler_ficheiro(file)

    file_name = os.path.basename(file)

    frequencias = utils.calcular_frequencias(conteudo)
    total = len(conteudo)
    simbolo_max, freq_max = utils.simbolo_mais_frequente(conteudo)

    prob_max = utils.prob_max(freq_max, total)

    info_propria_max = utils.info_propria(prob_max)
    entropia_valor = utils.entropia(conteudo)

    print(f'\n{"="*50}')
    print(f'FICHEIRO: {file_name} ({modo.upper()})')
    print(f'{"="*50}')
    print(f'Total de símbolos: {total}')
    print(f'Símbolos únicos: {len(frequencias)}')
    
    if modo == 'binario':
        print(f'Tipo: Ficheiro binário (bytes 0-255)')
        print(f'Byte mais frequente: {simbolo_max} (0x{simbolo_max:02x})')
    else:
        print(f'Caractere mais frequente: "{simbolo_max}"')
    
    print(f'\n>>> SÍMBOLO MAIS FREQUENTE <<<')
    print(f'  Símbolo: {simbolo_max}' + (f' (0x{simbolo_max:02x})' if isinstance(simbolo_max, int) else f' "{simbolo_max}"'))
    print(f'  Frequência absoluta: {freq_max}')
    print(f'  Probabilidade: {prob_max:.4f} ({prob_max:.2%})')
    print(f'  Informação própria: {info_propria_max:.4f} bits')
    print(f'\n>>> ENTROPIA DA FONTE <<<')
    print(f'  H = {entropia_valor:.4f} bits/símbolo')
    print(f'  Entropia máxima possível: {utils.max_entropia(frequencias):.4f} bits/símbolo')
    print(f'  Redundância: {utils.entropia_redundancia(entropia_valor, frequencias):.4f} bits/símbolo')
    print(f'{"="*50}\n')
    
    # Tabela (limitada a top 20 para binários com muitos símbolos)
    print(f'{"Símbolo":<12} {"Freq":<10} {"Prob":<10} {"Info":<10} {"Contrib"}')
    print("-" * 60)
    
    itens = sorted(frequencias.items(), key=lambda x: x[1], reverse=True)
    if modo == 'binario' and len(itens) > 20:
        itens = itens[:20]  # Mostrar só top 20 para binários
        print("(Mostrando top 20 símbolos mais frequentes)")
    
    for simbolo, freq in itens:
        prob = freq / total
        info = utils.info_propria(prob)
        contrib = prob * info
        
        if isinstance(simbolo, int):  # Binário
            simbolo_fmt = f"0x{simbolo:02x} ({simbolo})"
        else:  # Texto
            simbolo_fmt = repr(simbolo) if not str(simbolo).isprintable() else f'"{simbolo}"'
        
        print(f'{simbolo_fmt:<12} {freq:<10} {prob:<10.4f} {info:<10.4f} {contrib:.4f}')
    
    draw_histogram_matplotlib(frequencias, titulo=f"Histogram_{file_name}")
    
    return {
        'ficheiro': file_name,
        'modo': modo,
        'simbolo_max': simbolo_max,
        'frequencia_max': freq_max,
        'probabilidade_max': prob_max,
        'informacao_propria_max': info_propria_max,
        'entropia': entropia_valor,
        'frequencias': frequencias
    }


def main():
    test_files = utils.filesToTest()

    try:
        for file in test_files:
            file_scanner(file)
    except Exception as e:
        print(f"Erro ao processar ficheiro {file}: {e}")
    

if __name__ == "__main__":
    main()
