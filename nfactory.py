# Для старта игры запустите программу в PyCharm, нажав Run. Появится новое окно с полем для игры. Вы можете начать нажав на любую ячейку.
# Для начала новой игры нажмите на "Файл" в левом верхнем углу окна и выберите "Play"
# Для изменения параметров поля и количества мин нажмите на "Файл" в левом верхнем углу окна и выберите "Settings"
# При введении букв выйдет окно об ошибке, закройте его нажав на Х в правом верхнем углу
# Для выхода нажмите на "Файл" в левом верхнем углу окна и выберите "Exit"
# При растягивании окна количество ячеек не меняется, только их размер
# Багов быть не должно
# Спасибо и хорошего дня/вечера!



import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror

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
        self.is_open = False

    def __repr__(self):
        return f'MyButton {self.x} {self.y} {self.number} {self.is_mine}'


class NFactory:
    window = tk.Tk()
    row = 10
    columns = 10
    mines = 20
    is_game_over = False
    is_first_click = True

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

        if NFactory.is_game_over:
            return

        if NFactory.is_first_click:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_cells()
            self.print_buttons()
            NFactory.is_first_click = False

        if clicked_button.is_mine:
            clicked_button.config(text="*", background='red', disabledforeground='black')
            clicked_button.is_open = True
            NFactory.is_game_over = True
            showinfo('Game over', 'You lose (')
            for i in range(1, NFactory.row +1):
                for j in range (1, NFactory.columns+1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
        else:
            color = colors.get(clicked_button.count_bomb, 'black')
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)

    def breadth_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:

            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text=' ', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)
            
            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        # if not abs(dx-dy) == 1:
                        #     continue

                        next_btn =  self.buttons[x+dx][y+dy]
                        if not next_btn.is_open and 1<=next_btn.x<=NFactory.row and \
                                1<=next_btn.y<=NFactory.columns and next_btn not in queue:
                            queue.append(next_btn)

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        NFactory.is_first_click = True
        NFactory.is_game_over = False

    def create_settings(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Settings')
        tk.Label(win_settings, text='Number of rows').grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, NFactory.row)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Number of columns').grid(row=1, column=0)
        column_entry = tk.Entry(win_settings)
        column_entry.insert(0, NFactory.columns)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Number of mines').grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, NFactory.mines)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        save_btn = tk.Button(win_settings, text='Apply', command=lambda :self.change_settings(row_entry, column_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror('Error','You entered an incorrect value')
            return
        NFactory.row = int(row.get())
        NFactory.columns = int(column.get())
        NFactory.mines = int(mines.get())
        self.reload()

    def create_widgets(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        settings = tk.Menu(menubar, tearoff=0)
        settings.add_command(label='Play', command=self.reload)
        settings.add_command(label='Settings', command =self.create_settings)
        settings.add_command(label='Exit', command=self.window.destroy)
        menubar.add_cascade(label='File', menu=settings)

        count = 1
        for i in range(1, NFactory.row + 1):
            for j in range(1, NFactory.columns + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick='NWES')
                count +=1
        for i in range(1, NFactory.row + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)

        for i in range(1, NFactory.columns + 1):
            tk.Grid.columnconfigure(self.window, i, weight=1)



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

    def insert_mines(self, number: int):
        indexes_mines = self.get_mines_places(number)
        print(indexes_mines)
        for i in range(1, NFactory.row + 1):
            for j in range(1, NFactory.columns + 1):
                btn = self.buttons[i][j]
                if btn.number in indexes_mines:
                    btn.is_mine = True

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
    def get_mines_places(exclude_number:int):
        indexes = list(range(1, NFactory.columns * NFactory.row + 1))
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:NFactory.mines]


game = NFactory()
game.start()
