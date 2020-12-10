from sudokuError import *
import time

class SudokuGame(object):
        """ The game logic. Is in charge of keeping game state and complete testing """
        def __init__(self, board_file, variant):
                self.board_file = board_file
                self.variant = variant
                self.start_puzzle = SudokuBoard(board_file).board

        def start(self):
                """ Will create a puzzle and give it towards the Sudoku Solver"""
                self.puzzle = []
                for i in range(9):
                        self.puzzle.append([])
                        for j in range(9):
                                self.puzzle[i].append(self.start_puzzle[i][j])
                SudokuSolver(self.puzzle, self.variant)

class SudokuSolver(SudokuGame):
        """     The main AI for solving the sudoku puzzle 
                Currently only implements backtracking 
        """
        def __init__(self, puzzle, variant):
                self.puzzle = puzzle
                self.variant = variant
                print(self.print_board())
                self.t0 = time.time()
                self.solve()
        def solve(self):
                empty = self.find_empty()                
                if empty is None:
                        print(self.print_board())
                        t1 = time.time()
                        print("Elapsed time was ", t1 - self.t0)
                        return True
                else:
                        row, col = empty
                for num in range(1,10):
                        if self.is_valid(num, (row, col)):
                                self.puzzle[row][col] = num
                                if self.solve():
                                        return True
                                self.puzzle[row][col] = 0
                return False

        def find_empty(self):
                """ Will find the first empty cell to populate """
                for r in range(9):
                        for c in range(9):
                                if self.puzzle[r][c] == 0:
                                        return(r, c)
                return None
        def is_valid(self, num, pos):
                #* Checks for Classic Sudoku *#
                if not self.check_classic(num, pos):
                        return False

                if self.variant == "diagonal":
                        if not self.check_sudoku_diagonal(num, pos):
                                return False

                if self.variant == "king" or self.variant == "chess":
                        if not self.check_sudoku_anti_king(num, pos):
                                return False

                if self.variant == "knight" or self.variant == "chess":
                        if not self.check_sudoku_anti_knight(num, pos):
                                return False
                return True 
                
        def check_classic(self, num, pos):
                for r in range(9):
                        if self.puzzle[pos[0]][r] == num:
                                return False
                for c in range(9):
                        if self.puzzle[c][pos[1]] == num:
                                return False
                #* This will check for uniqueness within a 3x3 box *#
                box_row = pos[1] // 3
                box_col = pos[0] // 3

                for r in range(box_col*3, box_col*3 + 3):
                        for c in range(box_row*3, box_row*3 + 3):
                                if self.puzzle[r][c] == num:
                                        return False
                return True

        def check_sudoku_diagonal(self, num, pos):
                """ Will solve sudoku-diagonal puzzles.
                For more info on this variant visit: http://sudopedia.enjoysudoku.com/Sudoku-X.html """

                #* The two variables below are meant for filtering out which diagonal the position accounts for *#
                tl_br = [(0,0),(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8)]
                bl_tr = [(0,8),(1,7),(2,6),(3,5),(4,4),(5,3),(6,2),(7,1),(8,0)]
                for r in range(9):
                        if pos in tl_br:
                                if self.puzzle[r][r] == num:
                                        return False
                        if pos in bl_tr:
                                if self.puzzle[8-r][r] == num:
                                        return False
                return True

        def check_sudoku_anti_king(self, num, pos):
                """ Will solve anti-king's sudoku puzzle
                For more info on this variant visit: http://www.cross-plus-a.com/html/cros7sud.htm 
                The only constraint added is on the direct orthogonal cells of the current cell chek"""
                check_kings = [ (pos[0] + 1, pos[1] + 1), #bottom right
                                (pos[0] + 1, pos[1] - 1), #bottom left
                                (pos[0] - 1, pos[1] + 1), #top right
                                (pos[0] - 1, pos[1] - 1) ]#top left
                for orth in check_kings:
                        if orth[0] not in range(9) or orth[1] not in range(9):
                                continue

                        elif self.puzzle[orth[0]][orth[1]] == num:
                                return False
                return True
        def check_sudoku_anti_knight(self, num, pos):
                """ Will solve anti-knight's sudoku puzzle
                For more info on this variant visit: http://www.cross-plus-a.com/html/cros7sud.htm 
                The only constraint added is on the cells a chess knights move away"""
                check_knights = [(pos[0] - 1, pos[1] - 2), # up 1 left 2 
                                 (pos[0] - 2, pos[1] - 1), # up 2 left 1
                                 (pos[0] - 2, pos[1] + 1), # up 2 right 1
                                 (pos[0] - 1, pos[1] + 2), # up 1 right 2
                                 (pos[0] + 1, pos[1] - 2), # down 1 left 2
                                 (pos[0] + 2, pos[1] - 1), # down 2 left 1
                                 (pos[0] + 2, pos[1] + 1), # down 2 right 1
                                 (pos[0] + 1, pos[1] + 2)  # down 1 right 2
                                 ]
                for knight in check_knights:
                        if knight[0] not in range(9) or knight[1] not in range(9):
                                continue
                        elif self.puzzle[knight[0]][knight[1]] == num:
                                return False
                return True
        def print_board(self):
                if self.find_empty() is None:
                        print("Final Board State: ")
                else:
                        print("Initial Board State: ")
                for r in range(9):
                        if r % 3 == 0:
                                print("-------------------")
                        for c in range(9):
                                if c % 3 == 0:
                                        print("\b|", end = "")
                                print(str(self.puzzle[r][c]) + " ", end ="")
                        print("\b|")
                print("-------------------")

class SudokuBoard(object):

        """ Sudoku Board representation"""
        def __init__(self, board_file):
                self.board = self.create_board(board_file)

        def create_board(self, board_file):
                """ Function to create the sudoku board """

                board = []

                """     Will iterate over each line in the board file 
                        Checks for:
                                If each line is 9 characters long (col 0-8)
                                If there are 9 lines (row 0-8)
                                If all that is inputted is an int
                """
                for line in board_file:
                        line = line.strip()
                        if len(line) != 9: #* col *#
                                board = []
                                raise SudokuError("Each line in the sudoku must be 9 chars long!!!")

                        board.append([])
                        for c in line:  #* int *#
                                if not c.isdigit():
                                        raise SudokuError("Valid entries for the board must be 0-9")
                                board[-1].append(int(c))
                if len(board) != 9:     #* row *#
                        raise SudokuError("Each input board must be 9 lines long!")
                return board