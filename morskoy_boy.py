from random import randint

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return 'Вы вышли за границу поля('

class BoardUsedException(BoardException):
    def __str__(self):
        return 'В этой клетке вы уже были'

class BoardWrongShipException(BoardException):
    pass


def hello():
    print()
    print('           Приветствуем вас в         ')
    print('               Морской Бой!           ')
    print()
    print('Вы играете с Искусственным Интелектом.')
    print('   В вашем распоряжении 7 кораблей:   ')
    print('      1 четырехпалубный корабль,      ')
    print('    2 двухпалубных и 4 однопалубных   ')
    print()
    print('Между кораблями должна быть минимум 1 клетка!')
    print('        Да победит сильнейший!        ')

class Board:
    def __init__(self, hid=False, size=6):
      self.size = size
      self.hid = hid

      self.count = 0

      self.field = [["."] * size for _ in range(size)]

      self.busy = []
      self.ships = []

    def add_ship(self, ship):
      for d in ship.dots:
        if self.out(d) or d in self.busy:
            raise BoardWrongShipException()

      for d in ship.dots:
         self.field[d.x][d.y] = "■"
         self.busy.append(d)

      self.ships.append(ship)

    def __str__(self):
      res = ""
      res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
      for i, row in enumerate(self.field):
        res += f"\n{i + 1} | " + " | ".join(row) + " |"

      if self.hid:
        res = res.replace("■", '.')
      return res

    def out(self, d):
      return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
       if self.out(d):
         raise BoardOutException()

       if d in self.busy:
         raise BoardUsedException()

       self.busy.append(d)

       for ship in self.ships:
         if d in ship.dots:
            ship.lives -= 1
            self.field[d.x][d.y] = "X"
            if ship.lives == 0:
              self.count += 1
              self.field[d.x][d.y] = "&"
              print('Корабль Убит!')
              return True
            else:
              print('Корабль Ранен!')
              return True

       self.field[d.x][d.y] = "~"
       print('Промазал!')
       return False

    def begin(self):
      self.busy = []

class Main:
  def __init__(self, size=6):
    self.size = size
    pl = self.random_board()
    co = self.random_board()
    co.hid = True

    self.ai = AI(co, pl)
    self.us = User(pl, co)

  def random_board(self):
    board = None
    while board is None:
      board = self.random_place()
    return board

  def random_place(self):  # расстановка кораблей на поле - случайним методом
    lens = [3, 2, 2, 1, 1, 1, 1]  # размеры всех кораблей
    board = Board(size=self.size)
    attempts_random = 0  # счётчик попыток создать корабли на поле Компьютера
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

  def game(self):  # основной игровой цикл
    num = 0
    while True:
      print('-' * 27)
      print('Доска Пользователя:')
      print(self.us.board)
      print('-' * 27)
      print('Доска Компьютера:')
      print(self.ai.board)
      if num % 2 == 0:
        print('-' * 27)
        print('Ход Пользователя - введите Ряд и Столбец через пробел')

        repeat = self.us.move()
      else:
        print('-' * 27)

        print('Ход Компьютера:  ')
        repeat = self.ai.move()
      if repeat:
         num -= 1  # для того, чтобы не было передачи хода сопернику, когда удачный выстрел

      if self.ai.board.count == 7:
          print('-' * 27)

          print('Пользователь Выиграл!')

          print('Для новой игры нажмите зелёный треугольник вверху')
          break

      if self.us.board.count == 7:
          print('-' * 27)
          print('Компьютер Выиграл!')

          print('Для новой игры нажмите зелёный треугольник вверху')
          break

      num += 1

  def start(self):
      self.game()
class Player:  # основные взаимодействия Пользователя и Компьютера (противника)
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

class AI(Player):  # дочерний класс - Игрок ИИ
  def ask(self):
    d = Dot(randint(0, 5), randint(0, 5))

    print(f'Компьютер пошёл так: {d.x + 1} {d.y + 1}')
    return d

class User(Player):  # дочерний класс - Игрок Пользователь
  def ask(self):
    while True:
      cords = input('Ваш ход: ').split()

      if len(cords) != 2:  # проверка ввода на 2 координаты точки
        print(' Внимание! Введите ИМЕННО 2 координаты! ')
        continue
      x, y = cords  # обработка ввода координат игрока (как Пользователя, так и Компьютера)

      if not (x.isdigit()) or not (y.isdigit()):  # проверка ввода на числовое значение
        print(' Так не пойдёт! Введите числа! ')
        continue

      x, y = int(x), int(y)
      return Dot(x - 1, y - 1)

class Dot:  # и снова про точки, их сравнение и отображение координат
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

  def __repr__(self):
    return f'({self.x}, {self.y})'

class Ship:
  def __init__(self, bow, l, o):  # основные параметры корабля: нос, длина, расположение (верт,гориз)
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






hello()
