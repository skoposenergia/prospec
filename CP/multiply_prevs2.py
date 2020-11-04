import sqlite3
from pathlib import Path
import pandas as pd

SQLITE_FILE = 'configs/sqlite.db'
MLTS = pd.read_excel('configs/MLT.xlsx', index_col=0)
CONFIG = pd.read_csv('configs/config_cp.csv', index_col=0, header=None)

OUT_FILENAME_PATTERN = 'Prevs-{}_{:02d}_{}_{:02d}.rv{}' #Atualizar a entrada das revisões .rvX

LINE_FORMAT = '{:6d}{:5d}{:10d}{:10d}{:10d}{:10d}{:10d}{:10d}'

FIELD_LENGTHS = 6, 5, 10, 10, 10, 10, 10, 10


def multiply_and_write(sub1, k1, sub2, k2, out_filename, in_filename):
    """Lê o arquivo de input, multiplica seus valores e escreve um novo arquivo. Função principal."""
    
    out_file = open(out_filename, 'w')
    
    in_file = open(in_filename)
    cods1 = get_sub_cods(sub1)
    cods2 = get_sub_cods(sub2)
    
    for input_line in in_file:
            input_line = input_line.rstrip()
            
            values = parse_values(input_line)
            line_cod = values[1]
            if line_cod in cods1:
                    new_values = multiply(values, k1)
                    new_line = LINE_FORMAT.format(*new_values)
            elif line_cod in cods2:
                    new_values = multiply(values, k2)
                    new_line = LINE_FORMAT.format(*new_values)
            else:
                    new_line = input_line
            out_file.write(new_line + '\n')
    
    in_file.close()
    out_file.close()
    
    
def parse_values(line):
    """Lê a linha em formato texto e retorna uma lista de números"""
    
    start = 0 # Número da coluna onde o campo começa
    values = [] # Os números serão incluídos nessa coluna
    for length in FIELD_LENGTHS: # Para cada número "comprimento" em FIELD_LENGTHS:,
        next_start = start + length
        # "next_start" não será incluído. Geralmente, minha_lista[a:b] inclui colunas de "a" a "b-1"
        field_str = line[start:next_start]
        field_int = int(field_str)
        values.append(field_int)   # Adiciona os valores à lista
        start = next_start
    return values
    
def get_sub_cods(sub):
    """Procura no DB os códigos pertencentes à cada submercado"""
    conn = sqlite3.connect(SQLITE_FILE)
    cursor = conn.cursor()
    rows = cursor.execute(f'SELECT cod FROM postos WHERE sub = "{sub}"')
    cods = set()
    for row in rows:
        cod=row[0]
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
    for i, col in CONFIG.iteritems():
        REV = col['rev']
        in_dir = Path('entradas/%s/%s' % (col['mes'], REV)).glob('**/*')
        print(col['mes'], REV)
        #in_dir = Path('entradas/%s' % col['mes']).glob('**/*')
        in_filenames = [direc for direc in in_dir if direc.is_file()]
        print(in_filenames)
        SUB1, SUB2 = col['sub_mer1'], col['sub_mer2']
        MLT1, MLT2 = MLTS.loc[SUB1, int(col['mes'])], MLTS.loc[SUB2, int(col['mes'])]
        BASE1, BASE2 = int(round(float(col['base1']) * MLT1)), int(round(float(col['base2']) * MLT2))
        
        PERCS1 = range(int(col['lim_inf1']), int(col['lim_sup1']), int(col['passo1']))
        PERCS2 = range(int(col['lim_inf2']), int(col['lim_sup2']), int(col['passo2']))
        
        for perc1 in PERCS1:
            for perc2 in PERCS2:
                out_filename = OUT_FILENAME_PATTERN.format(SUB1, perc1, SUB2, perc2, REV)
                print(out_filename)
                k1 = (perc1/100) * MLT1 / BASE1
                k2 = (perc2/100) * MLT2 / BASE2
                for files in in_filenames:
                    in_filename = str(files)
                    out_filename = OUT_FILENAME_PATTERN.format(SUB1, perc1, SUB2, perc2, REV)
                    print(out_filename)
                    out_filename = 'saidas/' + col['mes'] + '/' + REV + '/' + out_filename
                    multiply_and_write(SUB1, k1, SUB2, k2, out_filename, in_filename)
                                     