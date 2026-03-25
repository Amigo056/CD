# 1. Análise de fontes de símbolos.
#   (a) Escreva uma função tal que sobre um ficheiro de entrada, realize as seguintes funcionalidades: (i) determina o símbolo
#       mais frequente, a respetiva probabilidade e a informação própria; (ii) o valor da entropia; (iii) apresente o respetivo
#       histograma.
#   
#   (b) Apresente os resultados obtidos pela função para os ficheiros do conjunto TestFilesCD.zip. Comente os resultados.

import matplotlib.pyplot as plt
import os
import utils

def draw_histogram_matplotlib(frequencias, titulo, total):
    """
    Gera histograma usando matplotlib - salva como imagem.
    Mostra: símbolo, frequência, probabilidade e informação própria.
    """
    simbolos = list(frequencias.keys())
    contagens = list(frequencias.values())
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(simbolos)), contagens, color='skyblue', edgecolor='black')
    
    # Adicionar valores nas barras (probabilidade %)
    for i, (simbolo, freq) in enumerate(zip(simbolos, contagens)):
        prob = freq / total
        plt.text(i, freq + max(contagens)*0.01, f'{prob:.2%}', 
                ha='center', va='bottom', fontsize=8)
    
    plt.xticks(range(len(simbolos)), [repr(s) if len(s) > 1 or not s.isprintable() else s 
                                       for s in simbolos], rotation=45)
    plt.xlabel('Símbolos')
    plt.ylabel('Frequência Absoluta')
    plt.title(titulo)
    plt.tight_layout()
    
    # Criar diretório se não existir
    plt.savefig(os.path.join("Exercicio2", f"{titulo}.png"), dpi=150)
    plt.show()


def file_scanner(file):
    
    with open(file, 'r') as f:
        conteudo = f.read()

    file_name = os.path.basename(file)

    frequencias = utils.calcular_frequencias(conteudo)
    total = len(conteudo)
    simbolo_max, freq_max = utils.simbolo_mais_frequente(conteudo)

    prob_max = utils.prob_max(freq_max, total)

    info_propria_max = utils.info_propria(prob_max)
    entropia_valor = utils.entropia(conteudo)

    print(f'\n{"="*50}')
    print(f'FICHEIRO: {file_name}')
    print(f'{"="*50}')
    print(f'Total de símbolos: {total}')
    print(f'Símbolos únicos: {len(frequencias)}')
    print(f'\n>>> SÍMBOLO MAIS FREQUENTE <<<')
    print(f'  Símbolo: "{simbolo_max}"')
    print(f'  Frequência absoluta: {freq_max}')
    print(f'  Probabilidade: {prob_max:.4f} ({prob_max:.2%})')
    print(f'  Informação própria: {info_propria_max:.4f} bits')
    print(f'\n>>> ENTROPIA DA FONTE <<<')
    print(f'  H = {entropia_valor:.4f} bits/símbolo')
    print(f'  Entropia máxima possível: {utils.max_entropia(frequencias):.4f} bits/símbolo')
    print(f'  Redundância: {utils.entropia_redundancia(entropia_valor, frequencias):.4f} bits/símbolo')
    print(f'{"="*50}\n')
    
    # Tabela completa de todos os símbolos
    print(f'{"Símbolo":<10} {"Freq":<8} {"Prob":<10} {"Info Própria":<12} {"Contribuição H"}')
    print("-" * 60)
    for simbolo, freq in sorted(frequencias.items(), key=lambda x: x[1], reverse=True):
        prob = freq / total
        info = utils.info_propria(prob)
        contrib = prob * info  # Contribuição para a entropia
        simbolo_fmt = repr(simbolo) if simbolo.isspace() or not simbolo.isprintable() else f'"{simbolo}"'
        print(f'{simbolo_fmt:<10} {freq:<8} {prob:<10.4f} {info:<12.4f} {contrib:.4f}')
    
    draw_histogram_matplotlib(frequencias, titulo=f"Symbol_Histogram_{file_name}", total=total)
    
    return {
        'ficheiro': file_name,
        'simbolo_max': simbolo_max,
        'frequencia_max': freq_max,
        'probabilidade_max': prob_max,
        'informacao_propria_max': info_propria_max,
        'entropia': entropia_valor,
        'frequencias': frequencias
    }

def file_path():


def main():
    test_files = [

        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Data', 'input1.txt'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Data', 'a.txt'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Data', 'alice29.txt'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Data', 'arrays.kt')
    ]

    for file in test_files:
        file_scanner(file)

if __name__ == "__main__":
    main()
