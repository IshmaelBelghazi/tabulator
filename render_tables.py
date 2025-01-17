#!/usr/bin/env python3
import pickle
import argparse
from pathlib import Path
from tabulatorz import tabulatorz

def parse_arguments():
    parser = argparse.ArgumentParser(description='Renders uimnet records')
    parser.add_argument('-r', '--records_file', type=str, required=True, help='Input record')
    parser.add_argument('-o', '--output_dir', type=str, required=True, help='Output folder')
    parser.add_argument('--exclude', type=str, nargs='*', default=[], help='algorithm to exclude')
    parser.add_argument('--render_pdf', action='store_true')
    parser.add_argument('--with_counts', action='store_true', help='Add value counts')

    return parser.parse_args()


def sort_algorithms(
        records, 
        algorithms=["ERM", "Mixup", "SoftLabeler", "DeepAE", "RND",
                    "OC", "MIMO", "MCDropout", "DUE", "RBF"]):
    new_records = []
    for algorithm in algorithms:
        for record in records:
            if record["algorithm"] == algorithm:
                new_records.append(record)

    return new_records


def correct_records_types(record):
    record['spectral'] = str(record['spectral'])
    record['k'] = str(record['k'])
    record['calibration'] = str(record['calibration'])
    if "arch" in record:
        del record["arch"]
    return record

def main(**kwargs):
    render_indomain(**kwargs)
    render_outdomain(**kwargs)

def render_indomain(records_file, output_dir, exclude, render_pdf, with_counts):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    with open(records_file, 'rb') as fp:
        all_records = pickle.load(fp)['indomain']

    values_columns_str_foo = tabulatorz.mean_std
    if with_counts:
        values_columns_str_foo = tabulatorz.mean_std_with_counts

    for arch, split_records in all_records.items():
        for split, records in split_records.items():
            if split != 'val':
                continue
            records = list(map(correct_records_types, records))
            records = [r for r in records if not (r['algorithm'] in exclude)]
            fname = f'indomain_{arch}_{split}.tex'
            label = f'tab:indomain_{arch}_{split}'
            caption = 'In-domain results for {}.'.format("ResNet18" if arch == "resnet18" else "ResNet50")
            fpath = (output_path / fname).absolute()
            tabulatorz.print_table(records, fname=str(fpath),
                                   midrule_column='algorithm',
                                   value_columns_str_foo=values_columns_str_foo,
                                   value_columns=["ACC@1", "ACC@5", "ECE", "NLL"],
                                   columns_scoring=['h', 'h', 'l', 'l'],
                                   num_white=70 if arch == "resnet18" else 90,
                                   caption=caption,
                                   standalone=render_pdf,
                                   label=label
                                   )
            if render_pdf:
                tabulatorz.render_pdf(fpath)

def render_outdomain(records_file, output_dir, exclude, render_pdf, with_counts):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    with open(records_file, 'rb') as fp:
        all_records = pickle.load(fp)['outdomain']
    values_columns_str_foo = tabulatorz.mean_std
    if with_counts:
        values_columns_str_foo = tabulatorz.mean_std_with_counts


    for arch, split_records in all_records.items():
        for measure, records in split_records.items():
            records = list(map(correct_records_types, records))
            records = [r for r in records if not (r['algorithm'] in exclude)]
            records = sort_algorithms(records)
            fname = f'outdomain_{arch}_{measure}.tex'
            label = f'tab:outdomain_{arch}_{measure}'
            caption = "Out-domain results for {} using measure ``{}''".format("ResNet18" if arch == "resnet18" else "ResNet50", measure)
            fpath = (output_path / fname).absolute()
            tabulatorz.print_table(records, fname=str(fpath),
                                   midrule_column='algorithm',
                                   value_columns_str_foo=values_columns_str_foo,
                                   value_columns=['AUC', 'InAsIn', 'OutAsOut'],
                                   columns_scoring=['h', 'h', 'h'],
                                   num_white=70 if measure != "Entropy" else 40,
                                   caption=caption,
                                   label=label,
                                   standalone=render_pdf
                                   )
            if render_pdf:
                tabulatorz.render_pdf(fpath)

if __name__ == '__main__':
    args = parse_arguments()
    main(**vars(args))
