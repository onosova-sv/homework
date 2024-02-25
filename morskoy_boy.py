#class mistake:
 #   if x<0 or x>9 or y<0 or y>9:
  #      print('BoardOutException')

def show():
    print()
    print("     0 | 1 | 2 | 3 | 4 | 5 | 6 | ")
    for i, row in enumerate(field):
        row_str = f"  {i}  {' | '.join(row)} "
        print(row_str)
        #корабли должны быть
    print()


def ask():
    while True:
        hod = input("Ваш ход: ").split()

        x, y = hod

        if not (x.isdigit()) or not (y.isdigit()):
            print(" Введите числа! ")
            continue

        x, y = int(x), int(y)

        if 0 > x or x > 6 or 0 > y or y > 6:
            print(" Координаты вне диапазона! ")
            continue

        if field[x][y] != "O":
            print(" Клетка занята! ")
            continue

        return x, y

field = [[" "] * 7 for i in range(7)]

class Dot():
    def __eq__(self, x, y):
        self.x=x
        self.y=y


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

hello()