import tkinter as tk
from tkinter import simpledialog
from constants import *


class GridApp:
    """ Класс, отвечающий за всю графику в окне master """
    def __init__(self, master):
        """
        Создание и подготовка сетки и кнопки

        :param master: окно, в котором будет отрисовка
        """
        self.master = master
        self.master.title("Game of Life")

        # Начальная установка размеров сетки
        self.grid_size = INITIAL_SIZE
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Изначально игра на паузе
        self.is_paused = True

        # Создаем виджеты:
        # 1. холст для отрисовки поля
        self.canvas = tk.Canvas(master, width=self.grid_size * SQUARE_SIZE, height=self.grid_size * SQUARE_SIZE)
        self.canvas.pack()

        # 2. рамка для кнопок
        self.button_frame = tk.Frame(master)
        self.button_frame.pack()

        # 3. кнопка для изменения размеров сетки
        self.resize_button = tk.Button(self.button_frame, text="Resize Grid", command=self.prompt_resize)
        self.resize_button.pack(side=tk.LEFT)

        # 4. кнопка инверсии поля
        self.inversion_button = tk.Button(self.button_frame, text="Inverse All", command=self.inverse_all)
        self.inversion_button.pack(side=tk.LEFT)

        # 5. кнопка паузы
        self.start_pause_button = tk.Button(self.button_frame, text="Start", command=self.toggle_pause)
        self.start_pause_button.pack(side=tk.LEFT)

        # Привязка клика ЛКМ по холсту
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Рисуем начальную сетку
        self.canvas_items = []
        self.draw_grid()

        # Запускаем цикл для перекраски первой клетки
        self.inverse_first_cell()

    def draw_grid(self):
        """ Функция перерисовки всего холста """
        self.canvas.delete("all")
        self.canvas_items.clear()
        for i in range(self.grid_size):
            row_items = []
            for j in range(self.grid_size):
                x1 = j * SQUARE_SIZE
                y1 = i * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                color = "green" if self.grid[i][j] == 1 else "white"
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                row_items.append(rect)
            self.canvas_items.append(row_items)

    def on_canvas_click(self, event):
        """
        Функция обработки клика по холсту

        :param event: Событие клика
        """
        j = event.x // SQUARE_SIZE
        i = event.y // SQUARE_SIZE
        if 0 <= i < self.grid_size and 0 <= j < self.grid_size:
            self.grid[i][j] = 1 - self.grid[i][j]
            self.update_square(i, j)

    def update_square(self, i, j):
        """
        Функция обновления одной клетки на холсте

        :param i: Координата строки
        :param j: Координата столбца
        """
        color = "green" if self.grid[i][j] == 1 else "white"
        self.canvas.itemconfig(self.canvas_items[i][j], fill=color)

    def inverse_all(self):
        """ Функция инверсии состояния всех клеток """
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.grid[i][j] = 1 - self.grid[i][j]
                self.update_square(i, j)

    def prompt_resize(self):
        """ Функция изменения размера сетки """
        new_size = simpledialog.askinteger("Resize Grid", "Enter new grid size:", initialvalue=self.grid_size)

        if new_size is not None:
            self.grid_size = new_size
            self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
            self.canvas.config(width=self.grid_size * SQUARE_SIZE, height=self.grid_size * SQUARE_SIZE)
            self.draw_grid()

    def inverse_first_cell(self):
        """ Функция перекраски первой клетки """
        if not self.is_paused:
            # Перекрасить первую клетку
            self.grid[0][0] = 1 - self.grid[0][0]
            self.update_square(0, 0)

        # Запланировать следующий вызов этой функции через ITER_TIME миллисекунд
        self.master.after(ITER_TIME, self.inverse_first_cell)

    def toggle_pause(self):
        """ Функция, которая приостанавливает и возобновляет игру """
        # Меняем состояние на "пауза/возобновление"
        self.is_paused = not self.is_paused
        # Обновляем текст кнопки
        if self.is_paused:
            self.start_pause_button.config(text="Start")
        else:
            self.start_pause_button.config(text="Pause")
