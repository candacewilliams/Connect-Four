from connect_four_graphics import *

def BoardClicked(col_index):
        global endgame
        global chip_color

        if endgame == False:
                row_index = FindNextRowIndex(col_index)
                print('BoardClicked col_index:', col_index)
                print('board click', col_index, row_index)
                
                AlternatePlayers(col_index, row_index)
                print(board_values)

                CheckWinner()

def CheckWinner():
        if CheckHorizontal('red'):
                endgame = True
                board.display_message('Player Red won')
        elif CheckHorizontal('blue'):
                endgame = True
                board.display_message('Player Blue won')
                
        elif CheckVertical('red'):
                endgame = True
                board.display_message('Player Red won')
        elif CheckVertical('blue'):
                endgame = True
                board.display_message('Player Blue won')
                
        if CheckDiagonal('red'):
                endgame = True
                board.display_message('Player Red won')
        elif CheckDiagonal('blue'):
                endgame = True
                board.display_message('Player Blue won')

def FindNextRowIndex(col_index):
        lowest_row_index = len(board_values)-1
        lowest_row_value = board_values[lowest_row_index][col_index]
                        
        if lowest_row_value == None:
                return lowest_row_index
        else:
                while lowest_row_value!= None:
                        lowest_row_index = lowest_row_index - 1
                        if lowest_row_index == 0 and lowest_row_value != None:
                               board.display_message('This column is out of room!')
                        lowest_row_value = board_values[lowest_row_index][col_index]
                return lowest_row_index      

        
def AlternatePlayers(col_index, row_index):
        global chip_color
        global endgame
        global player

        if player % 2 == 0:
                board.add_chip(col_index, row_index , chip_color )
                board_values[row_index][col_index] = chip_color
                board.display_message('Player Blue turn')
                player += 1
                chip_color = 'blue'
        else:
                board.add_chip(col_index, row_index , chip_color )
                board_values[row_index][col_index] = chip_color
                board.display_message('Player Red turn')
                player += 1
                chip_color = 'red'
                
        if player == rows * cols:
                endgame = True
                board.display_message('Draw!')
                


def CheckHorizontal(chip_color):
        global endgame
        global target_chips
        count = 0
        for i in range(rows):
                count = 0
                for j in range(cols):
                        if board_values[i][j] == chip_color:
                                count+=1
                        else:
                                count = 0
                        if count == target_chips:
                                endgame = True
                                return True
        return False

def CheckVertical(chip_color):
        global endgame
        global target_chips
        count = 0
        for i in range(cols):
                count = 0
                for j in range(rows):
                        if board_values[j][i] == chip_color:
                                count+=1
                        else:
                                count = 0
                        if count == target_chips:
                                endgame = True
                                return True
        return False
                                    
def CheckDiagonal(chip_color):
        global endgame
        global target_chips
        count = 0
        for i in range(rows):
                count = 0
                for j in range(cols):
                        count = 0
                        for h in range(target_chips):
                                if IsInBounds(i-h, j+h):
                                        if board_values[i - h][j + h] == chip_color:
                                                count+=1
                                        else:
                                                count = 0
                                        if count == target_chips:
                                                endgame = True
                                                return True
                        count = 0              
                        for k in range(target_chips):
                                if IsInBounds(i-k, j-k):
                                        if board_values[i - k][j - k] == chip_color:
                                                count+=1
                                        else:
                                                count = 0
                                        if count == target_chips:
                                                endgame = True
                                                return True
                        count = 0              
                        for  l in range(target_chips):
                                if IsInBounds(i+l, j+l):
                                        if board_values[i + l][j + l] == chip_color:
                                                count+=1
                                        else:
                                                count = 0
                                        if count == target_chips:
                                                endgame = True
                                                return True
                        count = 0              
                        for m in range(target_chips):
                                if IsInBounds(i+m, j-m):
                                        if board_values[i + m][j - m] == chip_color:
                                                count+=1
                                        else:
                                                count = 0
                                        if count == target_chips:
                                                endgame = True
                                                return True
        return False
                
def IsInBounds(row_index, col_index):
        if (rows > row_index and row_index >= 0
            and cols > col_index  and col_index >= 0):
                return True
        return False
                      
chip_color = 'red'
endgame = False
rows = int(input('Enter num of rows: '))
cols = int(input('Enter num of cols: '))
target_chips = int(input('num of chips to win: '))
board = ConnectFourBoard(rows, cols, BoardClicked)
player = 0

board_values =[[None] * cols for i in range(rows)]

                       

# Make sure mainloop() is the last line of code in this program!
mainloop()

