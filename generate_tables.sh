#!/bin/bash
python3.8 render_indomain_tables.py -r tabulator_indomain_records.pkl -o tables --exclude RBF $1
python3.8 render_outdomain_tables.py -r tabulator_outdomain_records.pkl -o tables --exclude RBF $1
find -s tables -name "*.tex" -exec cp {} $HOME/projects/uimnet-paper/tables \;
