import argparse
from sudokuError import *
from sudokuGame import *

def parse_arguments():
    """Will parse arguments and check for valid boards"""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--board",
                            help = "Enter fileName.txt",
                            type = str,
                            required=True)
                            #!  python3 main.py --board BOARD_NAME.txt !#
    arg_parser.add_argument("--variant",
                            help = "Enter variant name",
                            type = str,
                            required=False,
                            default = "classic")
                            #!  python3 main.py --board BOARD_NAME.txt --variant VARIANT_NAME  !#
    args = vars(arg_parser.parse_args())
    return args

if __name__ == "__main__":
    args = parse_arguments() #* Makes sure that there is valid CL input *#
    board_name = args['board']
    board_variants = args['variant']

    with open(board_name, 'r') as boards_file:  #* Opens board file as boards_file *#
        game = SudokuGame(boards_file, board_variants)
        game.start()