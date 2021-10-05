#!/bin/bash
python3.8 render_tables.py -r tabulator_records.pkl -o tables --exclude RBF $1
find -s tables -name "*.tex" -exec cp {} $HOME/projects/uimnet-paper/tables \;
