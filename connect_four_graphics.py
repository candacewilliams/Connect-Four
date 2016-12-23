from tkinter import *


CANVAS_WIDTH = 700
CANVAS_HEIGHT = 600
CHIP_OFFSET_RATIO = 0.1
CHIP_SPEED = 7
ANIMATION_DELAY = 1

class ConnectFourBoard():
    def __init__(self, num_rows, num_columns, user_clicked_func):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.user_clicked_func = user_clicked_func
        self.animations = []

        self.master = Tk()
        self.canvas = Canvas(
            self.master, 
            width = CANVAS_WIDTH,
            height = CANVAS_HEIGHT)
        self.message = self.canvas.create_text(
            CANVAS_WIDTH / 2, 50, text='', font=('Helvetica', 32),
            anchor=CENTER)
        self.canvas.pack()
        self.master.bind("<Button-1>", self.clicked)
        self.drawBoard()


    def drawBoard(self):
        self.board = self.canvas.create_rectangle(
            50, CANVAS_HEIGHT - 500,
            CANVAS_WIDTH - 50, CANVAS_HEIGHT,
            fill='yellow')

        for row_index in range(self.num_rows):
            for col_index in range(self.num_columns):
                chip_coords = self.get_chip_coords(col_index, row_index)
                self.canvas.create_oval(
                    chip_coords[0], chip_coords[1],
                    chip_coords[2], chip_coords[3],
                    fill='white')

    def clicked(self, event):
        '''
        Calls the student implemented function in connect_four.py if the user
        clicks within the boundaries of a column. Note that this function is
        called automatically when any spot on the canvas is clicked.
        '''
        if len(self.animations) > 0:
            return

        board_coords = self.canvas.coords(self.board)
        col_width = (board_coords[2] - board_coords[0]) / self.num_columns
        if (event.x >= board_coords[0] and event.x <= board_coords[2] and
            event.y >= board_coords[1] and event.y <= board_coords[3]):
            x = event.x - board_coords[0]
            col_index = int(x / col_width)
            col_location = x % col_width
            offset = col_width * CHIP_OFFSET_RATIO
            print('col_location', col_location)
            if col_location >= offset and col_location <= col_width - offset:
                self.user_clicked_func(col_index)

    def get_chip_coords(self, col_index, row_index):
        '''
        Returns the (x1, y1, x2, y2) coordinates for a chip at the given column
        and row index.
        '''

        board_coords = self.canvas.coords(self.board)
        col_width = (board_coords[2] - board_coords[0]) / self.num_columns
        col_offset = col_width * CHIP_OFFSET_RATIO
        row_height = (board_coords[3] - board_coords[1]) / self.num_rows
        row_offset = row_height * CHIP_OFFSET_RATIO
        return (board_coords[0] + col_index * col_width + col_offset / 2,
                board_coords[1] + row_index * row_height + row_offset / 2,
                board_coords[0] + (col_index + 1) * col_width - col_offset / 2,
                board_coords[1] + (row_index + 1) * row_height - row_offset / 2)

    def animate(self):
        '''
        Moves the currently selected chip one unit of distance, schedles this
        function to be called again until the chip is at its final location.
        '''
        if len(self.animations) == 0:
            raise Exception('There are no animations set. '
                'Email Kevin if you see this error')
        cur_animation = self.animations[0]
        chip_coords = self.canvas.coords(cur_animation[0])
        if chip_coords[1] >= cur_animation[1]:
            self.animations.pop(0)
            return
        else:
            y_distance = cur_animation[1] - chip_coords[1]
            self.canvas.move(
                cur_animation[0], 0, 
                CHIP_SPEED if y_distance > CHIP_SPEED else y_distance)
            self.canvas.tag_lower(cur_animation[0], self.board)
            for objectId in self.canvas.find_overlapping(
                chip_coords[0], chip_coords[1], chip_coords[2], chip_coords[3]):
                if objectId != self.board:
                    self.canvas.tag_raise(cur_animation[0], objectId)
            self.master.update()
            self.master.after(ANIMATION_DELAY, self.animate)

    def add_chip(self, col_index, row_index, color):
        '''
        Starts the animation to add a chip at the given column and row indexes.
        This method calls animate, which is called repeatedly until the
        animation completes.
        '''
        if row_index >= self.num_rows:
            raise IndexError(
                'row_index is out of range. row_index is {}. '
                'Available row indexes are 0 to {}.'.format(
                    row_index, self.num_rows - 1))
        elif col_index >= self.num_columns:
            raise IndexError(
                'col_index is out of range. col_index is {}. '
                'Available column indexes are 0 to {}.'.format(
                    col_index, self.num_columns - 1))

        chip_coords = self.get_chip_coords(col_index, row_index)
        self.animations.append((
            self.canvas.create_oval(
                chip_coords[0], 0,
                chip_coords[2], chip_coords[3] - chip_coords[1],
                fill=color),
            chip_coords[1]))
        self.master.after(ANIMATION_DELAY, self.animate)

        self.master.update()

    def display_message(self, string):
        '''
        Displays a message on the board.
        '''
        self.canvas.itemconfig(self.message, text=string)
