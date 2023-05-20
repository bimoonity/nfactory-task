import tkinter as tk
from random import shuffle

colors = {
    0: 'white',
    1: '#577590',
    2: '#4d908e',
    3: '#43aa8b',
    4: '#90be6d',
    5: '#f9c74f',
    6: '#f8961e',
    7: '#f3722c',
    8: '#f94144',
}

class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0

    def __repr__(self):
        return f'MyButton {self.x} {self.y} {self.number} {self.is_mine}'


class NFactory:
    window = tk.Tk()
    row = 10
    columns = 10
    mines = 22

    def __init__(self):
        self.buttons = []
        for i in range(NFactory.row + 2):
            temp = []
            for j in range(NFactory.columns + 2):
                btn = MyButton(NFactory.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)
            self.buttons.append(temp)

    def click(self, clicked_button: MyButton):
        if clicked_button.is_mine:
            clicked_button.config(text="*", background='red', disabledforeground='black')
        else:
            color = colors.get(clicked_button.count_bomb, 'black')
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
            else:
                clicked_button.config(text=' ', disabledforeground=color)

        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)

    def create_widgets(self):
        for i in range(1, NFactory.row + 1):
            for j in range(1, NFactory.columns + 1):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def open_all_buttons(self):
        for i in range(NFactory.row + 2):
            for j in range(NFactory.columns + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text="*", background='red', disabledforeground='black')

                elif btn.count_bomb in  colors:
                    color = colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, fg=color)

    def start(self):
        self.create_widgets()
        self.insert_mines()
        self.count_mines_in_cells()
        self.print_buttons()
        #self.open_all_buttons()
        NFactory.window.mainloop()

    def print_buttons(self):
        for i in range(1, NFactory.row + 1):
            for j in range(1, NFactory.columns + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end=' ')
                else:
                    print(btn.count_bomb, end=' ')
            print()

    def insert_mines(self):
        indexes_mines = self.get_mines_places()
        print(indexes_mines)
        count=1
        for i in range(1, NFactory.row + 1):
            for j in range(1, NFactory.columns + 1):
                btn = self.buttons[i][j]
                btn.number = count

                if btn.number in indexes_mines:
                    btn.is_mine = True
                count +=1

    def count_mines_in_cells(self):
        for i in range(1, NFactory.row + 1):
            for j in range(1, NFactory.columns + 1):
                btn = self.buttons[i][j]
                count_bomb=0
                if not btn.is_mine:
                    for row_dx in [-1,0,1]:
                        for col_dx in [-1, 0, 1]:
                            neighbor = self.buttons[i+row_dx][j+col_dx]
                            if neighbor.is_mine:
                                count_bomb+=1
                btn.count_bomb = count_bomb



    @staticmethod
    def get_mines_places():
        indexes = list(range(1, NFactory.columns * NFactory.row + 1))
        shuffle(indexes)
        return indexes[:NFactory.mines]


game = NFactory()
game.start()
