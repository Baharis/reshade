import argparse as ap
from pathlib import Path


def split_to_list(line):
    return list(filter(None, line.split(' ')))


def add_tens(list_):
    return ['-1' + s[1:] if s[0] == '-' else '1' + s for s in list_]


def cif_order_to_res_order(list_):
    return [list_[0], list_[1], list_[2], list_[5], list_[4], list_[3]]


def get_adp_dictionary_from_constrains(con_path):
    adp_dict = {}
    with open(str(Path(con_path)), 'r') as con:
        for line in con.readlines():
            line_elements = split_to_list(line)
            adp_dict[line_elements[1].upper()] = \
                add_tens(cif_order_to_res_order(line_elements[3:]))
    return adp_dict


def incorporate_constrains_into_line(line, adp_dict):
    line_elements = split_to_list(line)
    if len(line_elements) >= 7:
        k = line_elements[0].upper()
        if line_elements[1].isdigit():
            if k in adp_dict.keys():
                line_elements[6:12] = adp_dict[k]
            if len(line_elements) > 9:
                line_elements = line_elements[:9] + ['=\n'] + line_elements[9:]
            return ' '.join(line_elements)
        return line
    return line


def incorporate_constrains_into_res(res_path, adp_dict):
    with open(str(Path(res_path)), 'r') as res:
        res_data = res.read().replace('=\n', '')
    res_lines = res_data.split('\n')
    with open(str(Path(res_path).stem) + '_constrained.res', 'w+') as res:
        res.writelines([incorporate_constrains_into_line(line, adp_dict) + '\n'
                        for line in res_lines])


def main():
    con_path = ''
    res_path = ''
    help_message_main = 'Incorporate hydrogen constrains into a res file'
    message_blank = ' (leave blank to use alphabetically first)'
    help_message_res = 'Path to the shelx-type res file' + message_blank
    help_message_con = 'Path to the mopro-type CONSTRAINS file ' + message_blank

    p = ap.ArgumentParser(description=help_message_main)
    p.add_argument('Res file',
                   metavar='res_path', type=str, nargs='?', default='',
                   help=help_message_res)
    p.add_argument('Constraints file',
                   metavar='con_path', type=str, nargs='?', default='',
                   help=help_message_con)
    p.parse_args()

    if res_path is '':
        try:
            res_path = list(set(Path.cwd().glob('*.res')) -
                            set(Path.cwd().glob('*_constrained.res')))[0]
        except IndexError:
            raise FileNotFoundError('No unconstrained res file found')
    if con_path is '':
        try:
            con_path = list(Path.cwd().glob('CONSTRAINS.txt'))[0]
        except IndexError:
            raise FileNotFoundError('No constrains file found')

    adp_dict = get_adp_dictionary_from_constrains(con_path=con_path)
    incorporate_constrains_into_res(res_path=res_path, adp_dict=adp_dict)


if __name__ == '__main__':
    main()
