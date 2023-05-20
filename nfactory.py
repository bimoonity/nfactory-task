import tkinter as tk
from random import shuffle


class MyButton(tk.Button):

    def __init__(self, master, x, y, number, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False

    def __repr__(self):
        return f'MyButton {self.x} {self.y} {self.number} {self.is_mine}'


class NFactory:
    window = tk.Tk()
    row = 10
    columns = 10
    mines = 15

    def __init__(self):
        self.buttons = []
        count = 1
        for i in range(NFactory.row):
            temp = []
            for j in range(NFactory.columns):
                btn = MyButton(NFactory.window, x=i, y=j, number=count, )
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)
                count += 1
            self.buttons.append(temp)

    def click(self, clicked_button: MyButton):
        if clicked_button.is_mine:
            clicked_button.config(text="*", background='red')
        else:
            clicked_button.config(text=clicked_button.number)

    def create_widgets(self):
        for i in range(NFactory.row):
            for j in range(NFactory.columns):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def start(self):
        self.create_widgets()
        self.insert_mines()
        self.print_buttons()

        NFactory.window.mainloop()

    def print_buttons(self):
        for row_btn in self.buttons:
            print(row_btn)

    def insert_mines(self):
        indexes_mines = self.get_mines_places()
        print(indexes_mines)
        for row_btn in self.buttons:
            for btn in row_btn:
                if btn.number in indexes_mines:
                    btn.is_mine = True

    @staticmethod
    def get_mines_places():
        indexes = list(range(1, NFactory.columns * NFactory.row + 1))
        shuffle(indexes)
        return indexes[:NFactory.mines]


game = NFactory()
game.start()
