import os
import random
import sys

from copy import deepcopy

class Board:
    """
        Contains the attributes and functions of a Board.
    """
    def __init__(self, board_size):
        self.BOARD_SIZE = board_size
        self.EFF_BOARD_SIZE = self.BOARD_SIZE + 2
        self.board = self.init_board()
    
    def init_board(self):
        """
            Defines board of a given size
        """
        board = [[0 for x in range(self.EFF_BOARD_SIZE)] for y in range(self.EFF_BOARD_SIZE)]
        for i in range(self.EFF_BOARD_SIZE):
            board[i][0] = 1
        for i in range(self.EFF_BOARD_SIZE):
            board[self.EFF_BOARD_SIZE-1][i] = 1
        for i in range(self.EFF_BOARD_SIZE):
            board[i][self.EFF_BOARD_SIZE-1] = 1
        return board

    def print_board(self, curr_piece, piece_pos, error_message=''):
        """
        Prints the board on the terminal
        """
        os.system('cls' if os.name=='nt' else 'clear')

        board_copy = deepcopy(self.board)
        curr_piece_size_x = len(curr_piece)
        curr_piece_size_y = len(curr_piece[0])
        for i in range(curr_piece_size_x):
            for j in range(curr_piece_size_y):
                board_copy[piece_pos[0]+i][piece_pos[1]+j] = curr_piece[i][j] | self.board[piece_pos[0]+i][piece_pos[1]+j]

        # Print the board to STDOUT
        for i in range(self.EFF_BOARD_SIZE):
            for j in range(self.EFF_BOARD_SIZE):
                if board_copy[i][j] == 1:
                    print("*", end='')
                else:
                    print(" ", end='')
            print("")

        print("Quick play instructions:\n")
        print(" - a (return): move piece left")
        print(" - d (return): move piece right")
        print(" - w (return): rotate piece counter clockwise")
        print(" - s (return): rotate piece clockwise")

        # In case user doesn't want to alter the position of the piece
        # and he doesn't want to rotate the piece either and just wants to move
        # in the downward direction, he can choose 'f'
        print(" -<space> (return): just move the piece downwards as is")
        print(" - q (return): to quit the game anytime")

        if error_message:
            print(error_message)
        print("Your move:",)

    def merge_board_and_piece(self,curr_piece, piece_pos):
        """
            Fixes the position of the passed piece at piece_pos in the board
            This means that the new piece will now come into the play.

            We also remove any filled up rows from the board to continue the gameplay
            as it happends in a tetris game.
        """
        curr_piece_size_x = len(curr_piece)
        curr_piece_size_y = len(curr_piece[0])
        for i in range(curr_piece_size_x):
            for j in range(curr_piece_size_y):
                self.board[piece_pos[0]+i][piece_pos[1]+j] = curr_piece[i][j] | self.board[piece_pos[0]+i][piece_pos[1]+j]

        # After merging the board and piece
        # If there are rows which are completely filled then remove those rows

        # Declare empty row to add later
        empty_row = [0]*self.EFF_BOARD_SIZE
        empty_row[0] = 1
        empty_row[self.EFF_BOARD_SIZE-1] = 1

        # Declare a constant row that is completely filled
        filled_row = [1]*self.EFF_BOARD_SIZE

        # Count the total filled rows in the board
        filled_rows = 0
        for row in self.board:
            if row == filled_row:
                filled_rows += 1

        # The last row is always a filled row because it is the boundary
        # So decrease the count for that one
        filled_rows -= 1

        for i in range(filled_rows):
            self.board.remove(filled_row)

        # Add extra empty rows on the top of the board to compensate for deleted rows
        for i in range(filled_rows):
            self.board.insert(0, empty_row)


class Piece:
    """
        Contains the attributes and function of Pieces.
    """
    def __init__(self, EFF_BOARD_SIZE):
        self.PIECES = [

            [[1], [1], [1], [1]],

            [[1, 0],
             [1, 0],
             [1, 1]],

            [[0, 1],
             [0, 1],
             [1, 1]],

            [[0, 1],
             [1, 1],
             [1, 0]],

            [[1, 1],
             [1, 1]]

        ]
        self.EFF_BOARD_SIZE = EFF_BOARD_SIZE
    
    def get_random_piece(self):
        """
            a random piece from the PIECES constant declared above
        """
        i = random.randrange(len(self.PIECES))
        return self.PIECES[i]


    def get_random_position(self,curr_piece):
        """
            a randomly (along x-axis) chosen position for this piece
        """
        curr_piece_size = len(curr_piece)

        # This x refers to rows, rows go along y-axis
        x = 0
        # This y refers to columns, columns go along x-axis
        y = random.randrange(1, self.EFF_BOARD_SIZE-curr_piece_size)
        return [x, y]
    
    def get_left_move(self,piece_pos):
        """
            position of the piece shifted to the left.
        """
        # Shift the piece left by 1 unit
        new_piece_pos = [piece_pos[0], piece_pos[1] - 1]
        return new_piece_pos


    def get_right_move(self,piece_pos):
        """
            new position of the piece shifted to the right
        """
        # Shift the piece right by 1 unit
        new_piece_pos = [piece_pos[0], piece_pos[1] + 1]
        return new_piece_pos


    def get_down_move(self,piece_pos):
        """
            new position of the piece shifted downward
        """
        # Shift the piece down by 1 unit
        new_piece_pos = [piece_pos[0] + 1, piece_pos[1]]
        return new_piece_pos


    def rotate_clockwise(self,piece):
        """
            Clockwise rotated piece
        """
        piece_copy = deepcopy(piece)
        reverse_piece = piece_copy[::-1]
        return list(list(elem) for elem in zip(*reverse_piece))


    def rotate_anticlockwise(self,piece):
        """
            Anti-clockwise rotated piece
        """
        piece_copy = deepcopy(piece)
        # Rotating clockwise thrice will be same as rotating anticlockwise :)
        piece_1 = self.rotate_clockwise(piece_copy)
        piece_2 = self.rotate_clockwise(piece_1)
        return self.rotate_clockwise(piece_2)
    
    def overlap_check(self, board, curr_piece, piece_pos):
        """
            Check if the peices overlap
        """
        curr_piece_size_x = len(curr_piece)
        curr_piece_size_y = len(curr_piece[0])
        for i in range(curr_piece_size_x):
            for j in range(curr_piece_size_y):
                if board[piece_pos[0]+i][piece_pos[1]+j] == 1 and curr_piece[i][j] == 1:
                    return False
        return True

    def can_move_left(self, board, curr_piece, piece_pos):
        """
            Check if the peice can be moved to left
        """
        piece_pos = self.get_left_move(piece_pos)
        return self.overlap_check(board, curr_piece, piece_pos)


    def can_move_right(self, board, curr_piece, piece_pos):
        """
        Check if the peice can be moved to right
        """
        piece_pos = self.get_right_move(piece_pos)
        return self.overlap_check(board, curr_piece, piece_pos)


    def can_move_down(self, board, curr_piece, piece_pos):
        """
            Check if the peice can be moved to down
        """
        piece_pos = self.get_down_move(piece_pos)
        return self.overlap_check(board, curr_piece, piece_pos)


    def can_rotate_anticlockwise(self, board, curr_piece, piece_pos):
        """
            Check if the peice can be rotated anticlockwise
        """
        curr_piece = self.rotate_anticlockwise(curr_piece)
        return self.overlap_check(board, curr_piece, piece_pos)


    def can_rotate_clockwise(self, board, curr_piece, piece_pos):
        """
            Check if the peice can be rotated clockwise
        """
        curr_piece = self.rotate_clockwise(curr_piece)
        return self.overlap_check(board, curr_piece, piece_pos)


class Game:
    def __init__(self):
        # Constants for user input
        self.MOVE_LEFT = 'a'
        self.MOVE_RIGHT = 'd'
        self.ROTATE_ANTICLOCKWISE = 'w'
        self.ROTATE_CLOCKWISE = 's'
        self.NO_MOVE = ' '
        self.QUIT_GAME = 'q'


    def is_game_over(self, board, curr_piece, piece_pos, peices):
        """
            Check if game is over.
        """
        # If the piece cannot move down and the position is still the first row
        # of the board then the game has ended
        if not peices.can_move_down(board, curr_piece, piece_pos) and piece_pos[0] == 0:
            return True
        return False


    def play_game(self):
        board = Board(board_size=12)
        peices = Piece(board.EFF_BOARD_SIZE)
        curr_piece = peices.get_random_piece()
        piece_pos = peices.get_random_position(curr_piece)
        board.print_board(curr_piece, piece_pos)

        # Get player move from STDIN
        player_move = input()
        while (not self.is_game_over(board.board, curr_piece, piece_pos, peices)):
            ERR_MSG = ""
            do_move_down = False
            if player_move == self.MOVE_LEFT:
                if peices.can_move_left(board.board, curr_piece, piece_pos):
                    piece_pos = peices.get_left_move(piece_pos)
                    do_move_down = True
                else:
                    ERR_MSG = "Cannot move left!"
            elif player_move == self.MOVE_RIGHT:
                if peices.can_move_right(board.board, curr_piece, piece_pos):
                    piece_pos = peices.get_right_move(piece_pos)
                    do_move_down = True
                else:
                    ERR_MSG = "Cannot move right!"
            elif player_move == self.ROTATE_ANTICLOCKWISE:
                if peices.can_rotate_anticlockwise(board.board, curr_piece, piece_pos):
                    curr_piece = peices.rotate_anticlockwise(curr_piece)
                    do_move_down = True
                else:
                    ERR_MSG = "Cannot rotate anti-clockwise !"
            elif player_move == self.ROTATE_CLOCKWISE:
                if peices.can_rotate_clockwise(board.board, curr_piece, piece_pos):
                    curr_piece = peices.rotate_clockwise(curr_piece)
                    do_move_down = True
                else:
                    ERR_MSG = "Cannot rotate clockwise!"
            elif player_move == self.NO_MOVE:
                do_move_down = True
            elif player_move == self.QUIT_GAME:
                print("Bye. Thank you for playing!")
                sys.exit(0)
            else:
                ERR_MSG = "That is not a valid move!"

            if do_move_down and peices.can_move_down(board.board, curr_piece, piece_pos):
                piece_pos = peices.get_down_move(piece_pos)

            # This means the current piece in the game cannot be moved
            # We have to fix this piece in the board and generate a new piece
            if not peices.can_move_down(board.board, curr_piece, piece_pos):
                board.merge_board_and_piece(curr_piece, piece_pos)
                curr_piece = peices.get_random_piece()
                piece_pos = peices.get_random_position(curr_piece)

            os.system('cls' if os.name=='nt' else 'clear')
            # Redraw board
            board.print_board(curr_piece, piece_pos, error_message=ERR_MSG)

            # Get player move from STDIN
            player_move = input()

        print("GAME OVER!")
    
if __name__ == "__main__":
    game = Game()
    game.play_game()