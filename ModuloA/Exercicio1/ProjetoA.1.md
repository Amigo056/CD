# Projeto A.1

### Alínea (a)

**Objetivo:** determinar e apresentar todos os múltiplos de 6 no intervalo entre `a` e `a²`.

**Função:** `multiplos_de_seis(a)`

**Casos de teste:**

1. `multiplos_de_seis(6)`  
   **Resultado esperado:** `[6, 12, 18, 24, 30, 36]`

2. `multiplos_de_seis(3)`  
   **Resultado esperado:** `[6]`

3. `multiplos_de_seis(4)`  
   **Resultado esperado:** `[6, 12]`

**Programa de teste:** [`alinea_a.py`](./alinea_a.py) incluído na função `main()`.

---

### Alínea (b)

**Objetivo:** determinar o mínimo múltiplo comum entre dois números inteiros.

**Função:** `lcm(a, b)`

**Casos de teste:**

1. `lcm(12, 18)`  
   **Resultado esperado:** `36`

2. `lcm(20, 30)`  
   **Resultado esperado:** `60`

3. `lcm(6, 30)`  
   **Resultado esperado:** `30`

**Programa de teste:**  [`alinea_b.py`](./alinea_b.py) incluído na função `main()`.

---

### Alínea (c)

**Objetivo:** apresentar os primeiros `N` termos de uma progressão aritmética de primeiro termo `u` e razão `r`.

**Função:** `progressao_aritmetica(N, u, r)`

**Casos de teste:**

1. `progressao_aritmetica(10, 1, 2)`  
   **Resultado esperado:** `1, 3, 5, 7, 9, 11, 13, 15, 17, 19`

2. `progressao_aritmetica(5, 0, 5)`  
   **Resultado esperado:** `0, 5, 10, 15, 20`

3. `progressao_aritmetica(7, 2, 3)`  
   **Resultado esperado:** `2, 5, 8, 11, 14, 17, 20`

**Programa de teste:**  [`alinea_c.py`](./alinea_c.py)incluído na função `main()`.

---

### Alínea (d)

**Objetivo:** calcular e apresentar as raízes reais de uma equação do segundo grau.

**Função:** `calcular_raizes(a, b, c)`

**Casos de teste:**

1. `calcular_raizes(1, -3, 2)`  
   **Resultado esperado:** `A equação tem duas raízes reais: 2.00 e 1.00.`

2. `calcular_raizes(1, -2, 1)`  
   **Resultado esperado:** `A equação tem uma raiz real: 1.00.`

3. `calcular_raizes(1, 0, 1)`  
   **Resultado esperado:** `A equação não tem raízes reais.`

**Programa de teste:** [`alinea_d.py`](./alinea_d.py) incluído na função `main()`.

---

### Alínea (e)

**Objetivo:** determinar o valor mínimo, máximo, médio e a moda de um vetor de valores reais.

**Função:** `data(v)`

**Casos de teste:**

1. `data([2, 5, 1, 12, 25, 12, 2, 99, 67])`  
   **Resultado esperado:** `[1, 99, 25, 2]`

2. `data([1, 1, 1, 1, 1, 1, 1])`  
   **Resultado esperado:** `[1, 1, 1, 1]`

3. `data([1, 2, 3, 4, 5, 6, 7, 8, 9])`  
   **Resultado esperado:** `[1, 9, 5, 1]`

**Programa de teste:** [`alinea_e.py`](./alinea_e.py) incluído na função `main()`.

---

### Alínea (f)

**Objetivo:** determinar os elementos em comum entre dois vetores.

**Função:** `elementos_intersetados(v1, v2)`

**Casos de teste:**

1. `elementos_intersetados([1, 2, 3, 4, 5, 6], [4, 5, 6, 7, 8])`  
   **Resultado esperado:** `4, 5, 6`

2. `elementos_intersetados([1, 2, 3], [4, 5, 6])`  
   **Resultado esperado:** ``

3. `elementos_intersetados([1, 2, 3, 4], [2, 3, 4, 5])`  
   **Resultado esperado:** `2, 3, 4`

**Programa de teste:** [`alinea_f.py`](./alinea_f.py) incluído na função `main()`.

---

### Alínea (g)

**Objetivo:** determinar a união sem repetições entre dois vetores.

**Função:** `vectorUnion(v1, v2)`

**Casos de teste:**

1. `vectorUnion([1, 2, 3, 4, 5], [4, 5, 6, 7, 8])`  
   **Resultado esperado:** `[1, 2, 3, 4, 5, 6, 7, 8]`

2. `vectorUnion([1, 2, 3, 4, 5], [1, 1, 2, 2, 3])`  
   **Resultado esperado:** `[1, 2, 3, 4, 5]`

3. `vectorUnion([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])`  
   **Resultado esperado:** `[1, 2, 3, 4, 5]`

**Programa de teste:** [`alinea_g.py`](./alinea_g.py) incluído na função `main()`.

---

### Alínea (h)

**Objetivo:** inverter a ordem do conteúdo de um ficheiro, gravar o resultado noutro ficheiro e apresentar o símbolo mais frequente e a entropia de cada ficheiro.

**Função:** `inverter_ficheiro(inputFile, outputFile)`

**Testes realizados:**

Foram preparados **três ficheiros de teste** através de `utils.prepare_test_files()`.

- [`input1.txt`](./Data/input1.txt)
- [`input2.txt`](./Data/input2.txt)
- [`input3.txt`](./Data/input3.txt)

Para cada ficheiro:

1. É feita a inversão do conteúdo;
2. É gerado um ficheiro de saída;
3. São apresentados:
   - o símbolo mais frequente;
   - a frequência desse símbolo;
   - a entropia do ficheiro.

**Resultados:**

1. **Teste 1:**
   - Ficheiro: `input1.txt` → Símbolo mais frequente: `a` (frequência: 4) | Entropia: 1.7500
   - Ficheiro: `output1.txt` → Símbolo mais frequente: `a` (frequência: 4) | Entropia: 1.7500

2. **Teste 2:**
   - Ficheiro: `input2.txt` → Símbolo mais frequente: `a` (frequência: 21) | Entropia: 3.8379
   - Ficheiro: `output2.txt` → Símbolo mais frequente: `a` (frequência: 21) | Entropia: 3.8379

3. **Teste 3:**
   - Ficheiro: `input3.txt` → Símbolo mais frequente: `a` (frequência: 34) | Entropia: 0.1872
   - Ficheiro: `output3.txt` → Símbolo mais frequente: `a` (frequência: 34) | Entropia: 0.1872

**Ficheiros gerados:**


**Programa de teste:** [`alinea_h.py`](./alinea_h.py) incluído na função `main()`.

---

### Alínea (i)

**Objetivo:** determinar o símbolo mais frequente e a entropia de um ficheiro.

**Função:** `analisa_ficheiro(file)`

**Testes realizados:**

Foram analisados **três ficheiros de teste** preparados automaticamente:

- [`input1.txt`](./Data/input1.txt)
- [`input2.txt`](./Data/input2.txt)
- [`input3.txt`](./Data/input3.txt)

Para cada ficheiro são apresentados:

- o símbolo mais frequente;
- a sua frequência;
- a entropia.

**Resultados:**

1. **Teste 1:**
   - Símbolo mais frequente: `a` (frequência: 4)
   - Entropia: 1.7500

2. **Teste 2:**
   - Símbolo mais frequente: `a` (frequência: 21)
   - Entropia: 3.8379

3. **Teste 3:**
   - Símbolo mais frequente: `a` (frequência: 34)
   - Entropia: 0.1872

**Programa de teste:** [`alinea_i.py`](./alinea_i.py) incluído na função `main()`.

---

### Alínea (j)

**Objetivo:** apresentar o histograma dos símbolos de um ficheiro e a respetiva entropia.

**Função principal:** `desenhar_histograma_matplotlib(frequencias, titulo)`

**Testes realizados:**

Foram utilizados **três ficheiros de teste**.

Para cada ficheiro:

1. É calculada a frequência dos símbolos;
2. É apresentada a entropia;
3. É gerado um histograma em imagem (`png`).

Histogramas gerados:
- [`histogram1.png`](./histograma1.png)
- [`histogram2.png`](./histograma2.png)
- [`histogram3.png`](./histograma3.png)

**Programa de teste:** [`alinea_j.py`](./alinea_j.py) incluído na função `main()`.

## Observações

- Em todas as alíneas foram utilizados **três casos de teste distintos**, conforme solicitado.
- Os testes estão integrados nas funções `main()` de cada programa.
- Nas alíneas relacionadas com ficheiros, os ficheiros de teste são criados automaticamente através do módulo `utils`.
- A alínea **j** gera histogramas com recurso à biblioteca `matplotlib`.

## Conclusão

O Projeto A.1 implementa com sucesso todas as funcionalidades pedidas nas alíneas **(a) a (j)**, incluindo os respetivos programas de teste e os resultados experimentais obtidos em três casos distintos para cada situação.