"""Read Prevs_VE.prv and save another file with multiplied values."""
import sqlite3
from pathlib import Path
import pandas as pd


SQLITE_FILE = 'configs/sqlite.db'
MLTS = pd.read_excel('configs/MLT.xlsx', index_col=0)
CONFIG = pd.read_csv('configs/config.csv', index_col=0)

# New files will be named, for example, Prevs_VE_05.rv0.
# {:02d} will write a given number using 2 digits (e.g. 3 -> 03).
OUT_FILENAME_PATTERN = 'Prevs-{}_{:02d}_{}_{:02d}.rv0'

# {:6d} means: write a number (d) and complete with spaces on the left up to 6
# columns.
LINE_FORMAT = '{:6d}{:5d}{:10d}{:10d}{:10d}{:10d}{:10d}{:10d}'

# Field lengths will be used to read the file. Same numbers as in LINE_FORMAT
FIELD_LENGTHS = 6, 5, 10, 10, 10, 10, 10, 10


def multiply_and_write(sub1, k1, sub2, k2, out_filename, in_filename):
    """Read input file, multiply values and write a new one. Main function."""
        
    out_file = open(out_filename, 'w')  # 'w' means "create or overwrite"
        
    in_file = open(in_filename)     # default is read-only ('r')
    cods1 = get_sub_cods(sub1)
    cods2 = get_sub_cods(sub2)


    for input_line in in_file:
        input_line = input_line.rstrip()  # remove trailing white spaces

        values = parse_values(input_line)  # text becomes numbers (see below)
        line_cod = values[1]
        if line_cod in cods1:
            new_values = multiply(values, k1)  # multiply some columns by k1
            new_line = LINE_FORMAT.format(*new_values)  # numbers -> text
        elif line_cod in cods2:
            new_values = multiply(values, k2)  # multiply some columns by k2
            new_line = LINE_FORMAT.format(*new_values)  # numbers -> text
        else:
            new_line = input_line
        out_file.write(new_line + '\n')

    # Resources such as files should be closed.
    in_file.close()
    out_file.close()


def parse_values(line):
    """Read a line in text format and return a list of numbers.

    Use FIELD_LENGTH to read a line field by field and covert them from `str`
    (string) to `int` (integer) type.
    """
    start = 0    # column number where the field starts
    values = []  # numbers will be included in this list
    for length in FIELD_LENGTHS:  # for each "length" number in FIELD_LENGTHS:
        # Next field will start after "length" columns from current "start"
        next_start = start + length
        # Field is from "start" column to "next_start - 1".
        # "next_start" will not be included. Generally speaking, my_list[a:b]
        # includes columns from a to b-1.
        field_str = line[start:next_start]
        field_int = int(field_str)  # convert `str` to `int`
        values.append(field_int)    # add the int value to the list
        start = next_start          # update start to read the next field
    return values


def get_sub_cods(sub):
    """Search the DB for the CODs belonging to the given sub."""
    conn = sqlite3.connect(SQLITE_FILE)
    cursor = conn.cursor()
    rows = cursor.execute(f'SELECT cod FROM postos WHERE sub = "{sub}"')
    cods = set()
    for row in rows:
        cod = row[0]
        cods.add(cod)
    return cods


def multiply(values, k):
    """Multiply columns 3, 4, ... by "k"."""
    # Get the CODs for the given sub
    # First, we copy columns 0 and 1 that won't be multiplied
    multiplied = values[:2]   # same as values[0:2]
    # For all the other values, we multiply each one by "k"
    for value in values[2:]:  # same as value[2:<total number of columns>]
        int_value = int(round(value * k))
        multiplied.append(int_value)
    return multiplied


if __name__ == '__main__':
    # Generate two files. We will improve the code below according to your
    # needs.
    for i, col in CONFIG.iteritems():
        in_dir = Path('entradas/%s' % col.name).glob('**/*')
        in_filenames = [direc for direc in in_dir if direc.is_file()]
        SUB1, SUB2 = col['sub_mer1'], col['sub_mer2']
        MLT1, MLT2 = MLTS.loc[SUB1, int(col.name)], MLTS.loc[SUB2, int(col.name)] 
        BASE1, BASE2 = int(round(float(col['base1']) * MLT1)), int(round(float(col['base2']) * MLT2))
        
        #PERCS1 = [78, 84] # from 50 to 100
        #PERCS2 = [93, 113]   # from 60 to 90
        PERCS1 = range(int(col['lim_inf1']), int(col['lim_sup1']), int(col['passo1'])) # from 50 to 100
        PERCS2 = range(int(col['lim_inf2']), int(col['lim_sup2']), int(col['passo2']))   # from 60 to 90

        for perc1 in PERCS1:
            for perc2 in PERCS2:
                out_filename = OUT_FILENAME_PATTERN.format(SUB1, perc1, SUB2, perc2)
                k1 = (perc1/100) * MLT1 / BASE1
                k2 = (perc2/100) * MLT2 / BASE2
                for files in in_filenames:
                    in_filename = str(files)
                    out_filename = OUT_FILENAME_PATTERN.format(SUB1, perc1, SUB2, perc2)
                    out_filename = 'saídas/' + col.name + '/' + out_filename
                    multiply_and_write(SUB1, k1, SUB2, k2, out_filename, in_filename)
