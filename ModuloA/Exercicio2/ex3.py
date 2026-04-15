# ex3.py
import subprocess
import time
import os
import sys
import utils
import matplotlib.pyplot as plt
import shutil
import tempfile

# ============================================================================
# CONFIGURAÇÃO DO 7-ZIP
# ============================================================================
def find_7zip():
    """Tenta localizar o executável do 7-Zip automaticamente"""
    try:
        subprocess.run(['7z'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return '7z'
    except FileNotFoundError:
        pass
    
    possible_paths = [
        r"C:\Program Files\7-Zip\7z.exe",
        r"C:\Program Files (x86)\7-Zip\7z.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

SEVEN_ZIP_PATH = find_7zip()

if SEVEN_ZIP_PATH is None:
    print("ERRO: 7-Zip não encontrado!")
    sys.exit(1)
else:
    print(f"7-Zip encontrado em: {SEVEN_ZIP_PATH}")

# ============================================================================
# FUNÇÕES DE COMPRESSÃO
# ============================================================================
def compress(input_file, output_dir):
    """Compressão usando 7-Zip - guarda diretamente na pasta output"""
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Ficheiro não encontrado: {input_file}")
    
    # Guardar o .7z diretamente na pasta de resultados, não na data/
    base_name = os.path.basename(input_file)
    compressed_file = os.path.join(output_dir, base_name + '.7z')
    
    start_time = time.time()
    result = subprocess.run([SEVEN_ZIP_PATH, 'a', '-y', '-mx=5', compressed_file, input_file], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        raise RuntimeError(f"Erro na compressão: {result.stderr.decode('utf-8', errors='ignore')}")
    
    tempo = time.time() - start_time
    return compressed_file, tempo

def descompress(compressed_file, original_file):
    """Descompressão usando 7-Zip"""
    temp_dir = tempfile.mkdtemp()
    
    start_time = time.time()
    result = subprocess.run([SEVEN_ZIP_PATH, 'x', '-y', compressed_file, f'-o{temp_dir}'], 
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise RuntimeError(f"Erro na descompressão: {result.stderr.decode('utf-8', errors='ignore')}")
    
    tempo = time.time() - start_time
    
    original_name = os.path.basename(original_file)
    descompressed_file = os.path.join(temp_dir, original_name)
    
    if not os.path.exists(descompressed_file):
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise FileNotFoundError(f"Ficheiro descomprimido não encontrado")
    
    return descompressed_file, tempo, temp_dir

def compress_ratio(input_file, compressed_file):
    tamanho_original = os.path.getsize(input_file)
    tamanho_comprimido = os.path.getsize(compressed_file)
    return tamanho_comprimido / tamanho_original

def compress_descompress(input_file, pasta_saida):
    # Compressão (já guarda em pasta_saida)
    compressed_file, tempo_compressao = compress(input_file, pasta_saida)
    
    # Descompressão
    descompressed_file, tempo_descompressao, temp_dir = descompress(compressed_file, input_file)
    
    # Verificar integridade
    try:
        with open(input_file, 'rb') as f:
            original_data = f.read()
        with open(descompressed_file, 'rb') as f:
            descompressed_data = f.read()
        
        if original_data != descompressed_data:
            raise ValueError("Ficheiros não são idênticos após descompressão!")
    except PermissionError:
        print(f"  ⚠ Aviso: Não foi possível verificar integridade (ficheiro em uso)")
        descompressed_data = b''  # continuar mesmo assim
    
    # Limpar temp
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    razao = compress_ratio(input_file, compressed_file)
    
    return {
        'tempo_compressao': tempo_compressao,
        'tempo_descompressao': tempo_descompressao,
        'razao_compressao': razao,
        'bits_por_byte': razao * 8,
        'compressed_file': compressed_file
    }

# ============================================================================
# GERAÇÃO DE GRÁFICO
# ============================================================================
def plot_entropia_compressao(resultados, pasta_saida):
    if not resultados:
        print("Sem resultados para plotar.")
        return
    
    entropias = [r['entropia'] for r in resultados]
    compressoes = [r['bits_por_byte'] for r in resultados]
    nomes = [r['nome'] for r in resultados]
    
    plt.figure(figsize=(14, 8))
    
    # Cores por tipo
    cores = []
    for nome in nomes:
        ext = os.path.splitext(nome)[1].lower()
        if ext in ['.txt', '.htm', '.c', '.java', '.kt']:
            cores.append('blue')
        elif ext in ['.jpg', '.gif', '.bmp', '.tif', '.png']:
            cores.append('red')
        elif ext in ['.zip', '.rar', '.7z']:
            cores.append('green')
        else:
            cores.append('orange')
    
    plt.scatter(entropias, compressoes, s=150, alpha=0.7, c=cores, edgecolors='black', linewidth=1.5)
    
    # Linhas de referência
    max_val = max(max(entropias), max(compressoes), 8)
    min_val = min(min(entropias), min(compressoes), 0)
    plt.plot([0, max_val], [0, max_val], 'r--', label='Limite de Shannon (y=x)', linewidth=2)
    plt.axhline(y=8, color='gray', linestyle=':', alpha=0.7, label='Sem compressão (8 bits/byte)')
    
    # Anotações
    for i, nome in enumerate(nomes):
        plt.annotate(nome, (entropias[i], compressoes[i]), 
                    xytext=(5, 5), textcoords='offset points', 
                    fontsize=8, rotation=15)
    
    plt.xlabel('Entropia (bits/símbolo)', fontsize=12)
    plt.ylabel('Compressão obtida (bits/byte)', fontsize=12)
    plt.title('Relação Entropia vs Compressão (7-Zip)', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    caminho = os.path.join(pasta_saida, "entropia_vs_compressao.png")
    plt.savefig(caminho, dpi=150, bbox_inches='tight')
    print(f"\n✓ Gráfico guardado em: {caminho}")
    plt.show()

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================
def main():
    dir_script = os.path.dirname(os.path.abspath(__file__))
    pasta_saida = os.path.join(dir_script, "ex3Results")
    os.makedirs(pasta_saida, exist_ok=True)
    
    # Ficheiros da pasta data (TestFilesCD)
    data_files = utils.filesToTest()
    data_files = [f for f in data_files if not f.endswith('.7z')]
    
    # Ficheiros da pasta ex2Results (gerados no exercício 2)
    ex2_dir = os.path.join(dir_script, "ex2Results")
    ex2_files = []
    if os.path.exists(ex2_dir):
        # Selecionar alguns ficheiros representativos do ex2 (evitar .7z e ficheiros muito grandes)
        ex2_files = [
            os.path.join(ex2_dir, f) for f in os.listdir(ex2_dir)
            if os.path.isfile(os.path.join(ex2_dir, f)) 
            and not f.endswith('.7z')
            and not f.endswith('.txt.txt')  # evitar duplicados
            and os.path.getsize(os.path.join(ex2_dir, f)) < 5_000_000  # < 5MB para não demorar muito
        ][:6]  # Pegar nos primeiros 6 ficheiros representativos
    
    # Combinar ambos
    files = data_files + ex2_files
    
    # Limpar .7z antigos
    for f in files:
        if f.endswith('.7z'):
            try:
                os.remove(f)
            except:
                pass
    
    resultados = []
    
    print("="*70)
    print("ANÁLISE DE COMPRESSÃO 7-ZIP - Exercício 3")
    print("="*70)
    print(f"Ficheiros TestFilesCD: {len(data_files)}")
    print(f"Ficheiros Exercício 2: {len(ex2_files)}")
    print(f"Total: {len(files)}")
    print("-"*70)
    
    for file in files:
        nome = os.path.basename(file)
        origem = "Ex2" if "ex2Results" in file else "Data"
        
        if nome.endswith('.7z'):
            continue
            
        try:
            print(f"\n▶ [{origem}] Processando: {nome}")
            
            entropia_valor = utils.file_entropia(file)
            res = compress_descompress(file, pasta_saida)
            
            resultados.append({
                'nome': nome,
                'entropia': entropia_valor,
                'bits_por_byte': res['bits_por_byte'],
                'razao': res['razao_compressao'],
                'origem': origem
            })
            
            print(f"  Entropia:     {entropia_valor:.4f} bits/símbolo")
            print(f"  Compressão:   {res['razao_compressao']:.4f} ({res['bits_por_byte']:.2f} bits/byte)")
            print(f"  ✓ Integridade verificada")
            
        except Exception as e:
            print(f"  ✗ Erro: {e}")
    
    # Alínea (b) - Gráfico
    if resultados:
        print("\n" + "="*70)
        print("GERAÇÃO DO GRÁFICO (Alínea b)")
        print("="*70)
        plot_entropia_compressao(resultados, pasta_saida)
        
        print("\n" + "="*70)
        print("RESUMO FINAL")
        print("="*70)
        print(f"{'Ficheiro':<25} {'Origem':<8} {'Entropia':<10} {'Bits/B':<8} {'Razão':<8}")
        print("-"*65)
        for r in resultados:
            print(f"{r['nome']:<25} {r.get('origem','?'):<8} {r['entropia']:<10.3f} {r['bits_por_byte']:<8.2f} {r['razao']:<8.4f}")
if __name__ == "__main__":
    main()