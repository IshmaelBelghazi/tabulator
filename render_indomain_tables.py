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

    return parser.parse_args()

def correct_records_types(record):
    record['spectral'] = str(record['spectral'])
    record['k'] = str(record['k'])
    return record

def main(records_file, output_dir, exclude, render_pdf):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    with open(records_file, 'rb') as fp:
        all_records = pickle.load(fp)

    for arch, split_records in all_records.items():
        for split, records in split_records.items():
            records = list(map(correct_records_types, records))
            records = [r for r in records if not (r['algorithm'] in exclude)]
            fname = f'indomain_{arch}_{split}.tex'
            label = f'tab:indomain_{arch}_{split}'
            caption = f'In-domain results for {arch} architecture on the {split} split.'
            fpath = (output_path / fname).absolute()
            tabulatorz.print_table(records, fname=str(fpath),
                                   midrule_column='algorithm',
                                   value_columns=["ACC@1", "ACC@5", "ECE", "NLL"],
                                   columns_scoring=['h', 'h', 'l', 'l'],
                                   caption=caption,
                                   label=label
                                   )
            if render_pdf:
                tabulatorz.render_pdf(fpath)

if __name__ == '__main__':
    args = parse_arguments()
    main(**vars(args))