import tkinter as tk
from tkinter import simpledialog

# Исходный размер сетки
INITIAL_SIZE = 10
SQUARE_SIZE = 30
ITER_TIME = 300


class GridApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Game of Life")

        # Начальная установка размеров сетки
        self.grid_size = INITIAL_SIZE
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        self.is_paused = True

        # Создаем виджеты
        self.canvas = tk.Canvas(master, width=self.grid_size * SQUARE_SIZE, height=self.grid_size * SQUARE_SIZE)
        self.canvas.pack()

        self.button_frame = tk.Frame(master)
        self.button_frame.pack()

        self.resize_button = tk.Button(self.button_frame, text="Resize Grid", command=self.prompt_resize)
        self.resize_button.pack(side=tk.LEFT)

        self.toggle_button = tk.Button(self.button_frame, text="Toggle All", command=self.toggle_all)
        self.toggle_button.pack(side=tk.LEFT)

        self.start_pause_button = tk.Button(self.button_frame, text="Start", command=self.toggle_pause)
        self.start_pause_button.pack(side=tk.LEFT)

        # Привязка событий
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Рисуем начальную сетку
        self.canvas_items = []
        self.draw_grid()

        # Запускаем цикл для перекраски первой клетки
        self.toggle_first_cell()

    def draw_grid(self):
        # Очистка холста и перерисовка
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
        j = event.x // SQUARE_SIZE
        i = event.y // SQUARE_SIZE
        if 0 <= i < self.grid_size and 0 <= j < self.grid_size:
            self.grid[i][j] = 1 - self.grid[i][j]
            self.update_square(i, j)

    def update_square(self, i, j):
        color = "green" if self.grid[i][j] == 1 else "white"
        self.canvas.itemconfig(self.canvas_items[i][j], fill=color)

    def toggle_all(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.grid[i][j] = 1 - self.grid[i][j]
                self.update_square(i, j)

    def prompt_resize(self):
        # Запрашиваем новый размер сетки у пользователя
        new_size = simpledialog.askinteger("Resize Grid", "Enter new grid size:", initialvalue=self.grid_size)

        if new_size is not None:
            self.grid_size = new_size
            self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
            self.canvas.config(width=self.grid_size * SQUARE_SIZE, height=self.grid_size * SQUARE_SIZE)
            self.draw_grid()

    def toggle_first_cell(self):
        if not self.is_paused:
            # Перекрасить первую клетку
            self.grid[0][0] = 1 - self.grid[0][0]
            self.update_square(0, 0)

        # Запланировать следующий вызов этой функции через ITER_TIME миллисекунд
        self.master.after(ITER_TIME, self.toggle_first_cell)

    def toggle_pause(self):
        # Меняем состояние на "пауза/возобновление"
        self.is_paused = not self.is_paused
        # Обновляем текст кнопки
        if self.is_paused:
            self.start_pause_button.config(text="Start")
        else:
            self.start_pause_button.config(text="Pause")


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root)
    root.mainloop()
