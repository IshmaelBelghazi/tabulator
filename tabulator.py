import numpy as np
from colour import Color


def row(values, bold=False):
    row_str = ""
    for value in values:
        if bold:
            row_str += "\\textbf{{{}}} & ".format(value)
        else:
            row_str += "{} & ".format(value)

    return row_str[:-3] + "\\\\\n"


def min_max_column(records, column, foo):
    min_, max_ = 1e10, -1e10
    for record in records:
        min_ = min(min_, foo(record[column]))
        max_ = max(max_, foo(record[column]))
    return min_, max_


def colorize(
        v,
        v_min=0,
        v_max=1,
        c_min=(255, 150, 138),
        c_max=(151, 193, 169)):
    colors = list(Color("#FF968A").range_to(Color("#FFFFFF"), 20)) +\
             list(Color("#FFFFFF").range_to(Color("#FFFFFF"), 60)) +\
             list(Color("#FFFFFF").range_to(Color("#97C1A9"), 20))

    p = int((v - v_min) / (v_max - v_min) * 99)

    return "\\cellcolor[RGB]{{{}, {}, {}}}".format(
        colors[p].rgb[0] * 255,
        colors[p].rgb[1] * 255,
        colors[p].rgb[2] * 255)


def count(records, columns, values):
    the_count = 0
    for record in records:
        valid_record = True
        for column, value in zip(columns, values):
            if record[column] != value:
                valid_record = False
                break

        if valid_record:
            the_count += 1

    return the_count


def print_table(
        records,
        fname="test.tex",
        standalone=True,
        multirow=True,
        midrule_column=None,
        value_columns=[],
        value_columns_val_foo=lambda x: sum(x) / len(x),
        value_columns_str_foo=lambda x: "${:.3f} \\pm {:.3f}$".format(
            np.mean(x), np.std(x)),
        caption="table",
        label="tab:table"):
    f = open(fname, "w")

    if standalone:
        f.write("\\documentclass{article}\n")
        f.write("\\usepackage{booktabs, multirow, graphicx, adjustbox}\n")
        f.write("\\usepackage[table]{xcolor}\n\n")
        f.write("\\begin{document}\n\n")
        f.write("\\renewcommand{\\aboverulesep}{0pt}\n")
        f.write("\\renewcommand{\\belowrulesep}{0pt}\n")
        f.write("\\renewcommand{\\arraystretch}{1.15}\n")

    columns = list(records[0].keys())

    f.write("\\begin{table}\n")
    f.write("\\begin{center}\n")
    f.write("\\adjustbox{max width=\\linewidth, "
            "max totalheight=0.95\\textheight}{\n")
    f.write("\\begin{tabular}{" + "l" * len(columns) + "}\n")

    f.write("\\toprule\n")
    f.write(row(columns, bold=True))
    f.write("\\midrule\n")

    # compute column minimums and maximums for coloring purporses
    column_min, column_max = {}, {}
    for column in value_columns:
        column_min[column], column_max[column] = min_max_column(
            records, column, value_columns_val_foo)

    if midrule_column is not None:
        place_midrule = records[0][midrule_column]

    for r, record in enumerate(records):
        if midrule_column is not None and\
           place_midrule != record[midrule_column]:
            f.write("\\midrule\n")
            place_midrule = record[midrule_column]

        observed_columns, observed_values, row_values = [], [], []
        for column in columns:
            value = record[column]

            observed_columns.append(column)
            observed_values.append(value)

            if column in value_columns:
                color_str = colorize(
                    value_columns_val_foo(value),
                    column_min[column],
                    column_max[column])
                row_values.append(color_str + value_columns_str_foo(value))
            else:
                multirow_count = count(
                    records, observed_columns, observed_values)

                if not multirow or multirow_count == 1:
                    row_values.append(value)
                elif multirow:
                    if r % multirow_count == 0:
                        row_values.append(
                            "\\multirow{" +
                            str(multirow_count) +
                            "}{*}{" + value + "}")
                    else:
                        row_values.append(" ")
        f.write(row(row_values))

    f.write("\\bottomrule\n")
    f.write("\\end{tabular}}\n")
    f.write("\\end{center}\n")
    f.write("\\caption{{{}}}\n".format(caption))
    f.write("\\label{{{}}}\n".format(label))
    f.write("\\end{table}\n\n")

    if standalone:
        f.write("\\end{document}\n")

    f.close()


def dummy_test():
    records = []

    for algorithm in ["ERM", "MCDropout", "MIMO",
                      "Mixup", "OC", "RND", "SoftLabeler"]:
        for spectral in ["False", "True"]:
            for calibration in ["initial", "learned"]:
                for k in ["1", "5"]:
                    records.append({
                        "algorithm": algorithm,
                        "spectral": spectral,
                        "calibration": calibration,
                        "k": k,
                        "ACC@1": np.random.rand(10).tolist(),
                        "ACC@5": np.random.rand(10).tolist(),
                        "ECE": np.random.rand(10).tolist(),
                        "NLL": np.random.rand(10).tolist()})

    print_table(
        records,
        midrule_column="algorithm",
        value_columns=["ACC@1", "ACC@5", "ECE", "NLL"])

    import subprocess
    subprocess.run(["latexmk", "--shell-escape", "--pdf", "test.tex"])
    subprocess.run(["open", "test.pdf"])


if __name__ == "__main__":
    dummy_test()
