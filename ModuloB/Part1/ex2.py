# 2. Correcao de erros isolados
# Simulacao com:
#   (i) ausencia de codigos de controlo de erros
#   (ii) codigo de repeticao (3,1)
#   (iii) codigo de repeticao (5,1)

# Imports e preparacao do caminho para conseguir reutilizar funcoes do ex1.
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))
from ex1a import single_bit_error
from repetition_code import simulate_with_repetition
from bit_utils import remove_file
from metrics import calculate_final_ber, count_bit_errors
from table_utils import print_and_save_table, create_table_row


# Simulacao sem codigo de controlo de erros.
# Aqui o ficheiro passa diretamente pelo canal single_bit_error.
def simulate_without_code(input_file, output_file, p):
    # Configuracao (i): ficheiro original passa diretamente pelo canal.
    # Nao existe codificacao nem correcao.
    single_bit_error(input_file, output_file, p, True)


def simulate_configuration(input_file, p, results_dir, configuration, repetition):
    # Simula uma das tres configuracoes e devolve a linha da tabela.
    information_bits = input_file.stat().st_size * 8
    p_name = str(p).replace(".", "_")

    if repetition is None:
        output_file = results_dir / f"{input_file.stem}_p{p_name}_sem_codigo{input_file.suffix}"
        simulate_without_code(input_file, output_file, p)

        errors = count_bit_errors(input_file, output_file)
        transmitted_bits = information_bits
        channel_errors = errors
        final_errors = errors
    else:
        prefix = f"rep{repetition}"
        encoded_file = results_dir / f"{input_file.stem}_p{p_name}_{prefix}_codificado.bin"
        channel_file = results_dir / f"{input_file.stem}_p{p_name}_{prefix}_canal.bin"
        output_file = results_dir / f"{input_file.stem}_p{p_name}_{prefix}_saida{input_file.suffix}"

        simulate_with_repetition(input_file, encoded_file, channel_file, output_file, p, repetition)

        transmitted_bits = information_bits * repetition
        channel_errors = count_bit_errors(encoded_file, channel_file)
        final_errors = count_bit_errors(input_file, output_file)
        remove_file(encoded_file)
        remove_file(channel_file)

    row = create_table_row(
        input_file,
        output_file,
        p,
        configuration,
        channel_errors,
        final_errors,
        transmitted_bits,
        information_bits,
    )

    return row, output_file


# Funcoes da alinea 2.c.

def test_zero_ber_range(input_files, probabilities, results_dir, repetition):
    # Testa varios valores de p e verifica quando BER' fica igual a zero.
    rows = []
    zero_ber_ps = []

    for p in probabilities:
        all_files_zero = True

        for input_file in input_files:
            p_name = str(p).replace(".", "_")
            prefix = f"rep{repetition}"

            encoded_file = results_dir / f"{input_file.stem}_p{p_name}_{prefix}_2c_codificado.bin"
            channel_file = results_dir / f"{input_file.stem}_p{p_name}_{prefix}_2c_canal.bin"
            output_file = results_dir / f"{input_file.stem}_p{p_name}_{prefix}_2c_saida{input_file.suffix}"

            simulate_with_repetition(input_file, encoded_file, channel_file, output_file, p, repetition)
            final_ber = calculate_final_ber(input_file, output_file)
            remove_file(encoded_file)
            remove_file(channel_file)
            remove_file(output_file)

            if final_ber != 0:
                all_files_zero = False

            rows.append([
                f"Repeticao ({repetition},1)",
                str(p),
                input_file.name,
                f"{final_ber:.6f}",
                "Sim" if final_ber == 0 else "Nao",
            ])

        if all_files_zero:
            zero_ber_ps.append(p)

    return rows, zero_ber_ps


def run_ex2c(input_files, results_dir):
    # Grelha de valores usada para estimar experimentalmente a gama de p.
    probabilities = [0.001, 0.002, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1]

    rows = []
    summary = []

    for repetition in [3, 5]:
        repetition_rows, zero_ber_ps = test_zero_ber_range(
            input_files,
            probabilities,
            results_dir,
            repetition,
        )

        rows.extend(repetition_rows)

        if zero_ber_ps:
            summary.append(f"Repeticao ({repetition},1): BER'=0 ate p={max(zero_ber_ps)} nos valores testados.")
        else:
            summary.append(f"Repeticao ({repetition},1): nenhum valor testado obteve BER'=0 em todos os ficheiros.")

    table = [
        "| Codigo | p | Ficheiro | BER apos correcao | BER'=0 |",
        "| --- | --- | --- | --- | --- |",
    ]

    for row in rows:
        table.append("| " + " | ".join(row) + " |")

    table.append("")
    table.extend(summary)

    text = "\n".join(table)
    print("\nResultados da alinea 2.c")
    print(text)

    with open(results_dir / "tabela_ex2c.md", "w", encoding="utf-8") as f:
        f.write(text)


# Funcao principal: define ficheiros, probabilidades e configuracoes,
# executa os testes da alinea 2.b e depois a pesquisa experimental da 2.c.
def main():
    # Valores escolhidos para testar desde erro baixo ate erro elevado.
    probabilities = [0.001, 0.01, 0.05, 0.1]

    # Caminhos base: assim o script funciona mesmo sendo executado de outra pasta.
    base_dir = Path(__file__).resolve().parent
    modulo_b_dir = base_dir.parent

    # Dois ficheiros de teste escolhidos para a simulacao.
    input_files = [
        modulo_b_dir / "TestFiles" / "a.txt",
        modulo_b_dir / "TestFiles" / "fibonacci.kt",
    ]

    # Pasta onde vao ficar todos os ficheiros produzidos pela simulacao.
    results_dir = base_dir / "Ex2Results"
    results_dir.mkdir(exist_ok=True)

    configurations = [
        ("Sem codigo", None),
        ("Repeticao (3,1)", 3),
        ("Repeticao (5,1)", 5),
    ]

    table_rows = []

    # Para cada ficheiro e para cada p, testa as tres configuracoes pedidas.
    for input_file in input_files:
        for p in probabilities:
            print("Ficheiro:", input_file.name, "| p =", p)

            for configuration, repetition in configurations:
                row, output_file = simulate_configuration(
                    input_file,
                    p,
                    results_dir,
                    configuration,
                    repetition,
                )
                table_rows.append(row)
                print(" ", configuration, "->", output_file.name)

            print()

    print_and_save_table(table_rows, results_dir / "tabela_ex2.md")
    run_ex2c(input_files, results_dir)


if __name__ == "__main__":
    main()
