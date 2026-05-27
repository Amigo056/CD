import csv
from pathlib import Path

def print_and_save_csv(headers, rows, out_path, delimiter=","):
    """
    Grava CSV com BOM UTF-8 e newline='' para compatibilidade com Excel.
    Default delimiter=','; use delimiter=';' para Excel PT local.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # normaliza cada linha ao mesmo número de colunas dos headers
    norm_rows = []
    for r in rows:
        r_list = list(r)
        if len(r_list) < len(headers):
            r_list.extend([''] * (len(headers) - len(r_list)))
        elif len(r_list) > len(headers):
            r_list = r_list[: len(headers)]
        norm_rows.append([str(x) for x in r_list])

    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        writer.writerow([str(h) for h in headers])
        writer.writerows(norm_rows)

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
