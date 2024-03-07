from random import randint
import time  #для создания спецэффектов в консольной игре

print('------------------------------------------------')
print(' Друзья, давайте поиграем в самую классую игру: ')
print('              Морской Бой!    ')
print('---------------------------------------------------------')
time.sleep(3)   #задержка - эффект "покадрового" вывода информации
print('Пользователь играет с Компьютером - и ходит Первым!')
print('вводим через пробел 2 координаты:')
print('- номер строки и номер столбца.')
print('ПОЕХАЛИ:')

#сразу обозначим исключения при ошибочном вводе пользователя
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):     #отловим выстрел за пределы поля
        return 'Внимание! Вы стреляете за поле!'

class BoardUsedException(BoardException):
    def __str__(self):    #отловим повторный ввод координат
        return 'Вы уже стреляли в эту клетку'

class BoardWrongShipException(BoardException):
    pass

class Board:
    def __init__(self, hid=False, size=6): #исходные параметры поля
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["."] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):  #вывод кораблей на доску
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()  #проверка, чтобы каждая точка корабля:
                #не выходила за границы поля и непопадала в уже занятую точку
                #не выходила за границы поля и непопадала в уже занятую точку
        for d in ship.dots:
            self.field[d.x][d.y] = "■"  #корабли помечаем таким знаком (в видимом поле Пользователя)
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, sp=False): #контуры кораблей, обозначение точками их контуров
        n = [    #комбинация относительных индексов точек рядом с каждой взятой точкой
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]        # (по правилам - их нельзя занимать другому кораблю)
        for d in ship.dots:
            for dx, dy in n:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if sp:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self): #отображаем само игровой поле с помощью "конструктора"
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:  #в скрытом поле игрока ИИ изначально ставим только "."
            res = res.replace("■", ".")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()   #вызываем исключение для возможной отладки игры

        if d in self.busy:
            raise BoardUsedException()  #вызываем исключение для возможной отладки игры

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1    #обратный счётчик количества жизней у корабля
                self.field[d.x][d.y] = "X"   #пока частичное уничтожение корабля - такой знак
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, sp=True)
                    time.sleep(3) #эффект выстрела
                    self.field[d.x][d.y] = "&"  #полное уничтожение корабля - добавление к "Х" ещё такого знака
                    print('Корабль Убит!')
                    return True   #при удачном выстреле - ход НЕ переходит к противнику
                else:
                    time.sleep(3) #эффект выстрела
                    print('Корабль Ранен!')
                    return True  #при удачном выстреле - ход НЕ переходит к противнику

        self.field[d.x][d.y] = "~"  #промах - добавление такого знака на поле
        time.sleep(3)   #эффект выстрела
        print('Промазал!')
        return False  #при неудачном выстреле - ход ПЕРЕХОДИТ к противнику

    def begin(self):
        self.busy = []

class Main:  #установка основных параметров самой игры
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()  #на поле Пользователя - всё происходит по случайному принципу
        co = self.random_board()  #на поле Компьютера - всё происходит по случайному принципу
        co.hid = True   #поле Компьютера скрыто от Пользователя

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):  #расстановка кораблей на поле - случайним методом
        lens = [3, 2, 2, 1, 1, 1, 1]  #размеры всех кораблей
        board = Board(size=self.size)
        attempts_random = 0  #счётчик попыток создать корабли на поле Компьютера
        for L in lens:
            while True:
                attempts_random += 1
                if attempts_random > 1000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), L, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def game(self):  #основной игровой цикл
        num = 0
        while True:
            print('-' * 27)
            print('Доска Пользователя:')
            time.sleep(3)    #эффект выплывания досок - поочерёдно
            print(self.us.board)
            print('-' * 27)
            print('Доска Компьютера:')
            time.sleep(3)    #эффект выплывания досок - поочерёдно
            print(self.ai.board)
            time.sleep(3)
            if num % 2 == 0:
                print('-' * 27)
                time.sleep(1)
                print('Ход Пользователя - введите Ряд и Столбец через пробел')
                time.sleep(3)   #эффект произведённого выстрела
                repeat = self.us.move()
            else:
                print('-' * 27)
                time.sleep(1)
                print('Ход Компьютера:  ')
                time.sleep(3)   #эффект "обдумывания хода" Компьютером
                repeat = self.ai.move()
            if repeat:
                num -= 1  #для того, чтобы не было передачи хода сопернику, когда удачный выстрел

            if self.ai.board.count == 7:
                print('-' * 27)
                time.sleep(3)   #эффект
                print('Пользователь Выиграл!')
                time.sleep(3)   #эффект
                print('Для новой игры нажмите зелёный треугольник вверху')
                break

            if self.us.board.count == 7:
                print('-' * 27)
                time.sleep(3)   #эффект
                print('Компьютер Выиграл!')
                time.sleep(3)   # эффект
                print('Для новой игры нажмите зелёный треугольник вверху')
                break
            num += 1

    def start(self):
        self.game()

class Player:  #основные взаимодействия Пользователя и Компьютера (противника)
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player): #дочерний класс - Игрок ИИ
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        time.sleep(3)
        print(f'Компьютер пошёл так: {d.x + 1} {d.y + 1}')
        return d

class User(Player):  #дочерний класс - Игрок Пользователь
    def ask(self):
        while True:
            cords = input('Ваш ход: ').split()

            if len(cords) != 2:  #проверка ввода на 2 координаты точки
                print(' Внимание! Введите ИМЕННО 2 координаты! ')
                continue

            x, y = cords #обработка ввода координат игрока (как Пользователя, так и Компьютера)

            if not (x.isdigit()) or not (y.isdigit()): #проверка ввода на числовое значение
                print(' Так не пойдёт! Введите числа! ')
                continue

            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)

class Dot: #и снова про точки, их сравнение и отображение координат
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.x}, {self.y})'

class Ship:
    def __init__(self, bow, l, o): #основные параметры корабля: нос, длина, расположение (верт,гориз)
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots

m = Main()
m.start()





