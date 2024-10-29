class CellularAutomaton:
    """ Класс для функций клеточного автомата """

    def __init__(self, binary_func: str) -> None:
        """
        Создание автомата с конкретной булевой функцией

        :param binary_func: булева функция пяти переменных
        """
        self.binary_func = binary_func

    def bin_func(self, x0, x1, x2, x3, x4) -> int:
        """ Функция для получения значения бинарной функции"""

        # Вычисляем индекс как сумму произведений
        index = (x0 * 16) + (x1 * 8) + (x2 * 4) + (x3 * 2) + x4

        # Достаем значение функции из двоичной строки по индексу
        return int(self.binary_func[index])

    @staticmethod
    def neighbors(i: int, j: int):
        """ Функция для вычисления координат соседей клетки """

        s1 = (i-1, j)
        s2 = (i+1, j)
        s3 = (i, j-1)
        s4 = (i, j+1)
        return s1, s2, s3, s4
