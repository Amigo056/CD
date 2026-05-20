# Escreve a tabela em formato Markdown e tambem a mostra no terminal.
def print_and_save_table(rows, table_file):
    headers = [
        "Ficheiro",
        "p",
        "Configuracao",
        "BER canal",
        "BER apos correcao",
        "Bits transmitidos",
        "Bits informacao",
        "Entrada",
        "Saida",
    ]

    table = []
    table.append("| " + " | ".join(headers) + " |")
    table.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        table.append("| " + " | ".join(row) + " |")

    text = "\n".join(table)
    print(text)

    with open(table_file, "w", encoding="utf-8") as f:
        f.write(text)

# A tabela junta BER do canal, BER depois da correcao e numero de bits.
def create_table_row(input_file, output_file, p, configuration,
                     channel_errors, final_errors, transmitted_bits, information_bits):
    # Cria uma linha com os valores pedidos na alinea b.
    return [
        input_file.name,
        str(p),
        configuration,
        f"{channel_errors / transmitted_bits:.6f}",
        f"{final_errors / information_bits:.6f}",
        str(transmitted_bits),
        str(information_bits),
        input_file.name,
        output_file.name,
    ]