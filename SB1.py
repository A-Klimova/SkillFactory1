import random
import time


# Клас координат
class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'


# Класс кораблей
class Ship:

    def __init__(self):
        self.sizes = (3, 2, 2, 1, 1, 1, 1)  # Размер кораблей
        self.adjacent_cells = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0),
                               (1, -1)]  # Соседние клетки

    # Метод проверки возможности размещения кораблей
    def can_place_ship(self, field, position, length, orientation):
        x, y = position.x + 1, position.y + 1
        no_adjacent_hits = True
        for i in range(length):
            for dx, dy in self.adjacent_cells:
                if field[x + dx][y + dy] == '■':
                    no_adjacent_hits = False
            if orientation == -1:
                x += 1  # Вниз
            else:
                y += 1  # Вправо
        return no_adjacent_hits


# Класс игры
class BattleShipGame:
    def __init__(self):
        self.vessel = Ship()
        self.board = GameBoard()

    def run(self):
        self.introduction()
        board, machine, human = GameBoard(), AIPlayer(), HumanPlayer()
        machine.board = board.setup_board()
        human.board = board.setup_board()
        while True:
            board.display(machine.board, machine.name)
            board.display(human.board, human.name)
            human.take_shot(machine.board)
            machine.take_shot(human.board)

    # статистический метод
    @staticmethod
    def introduction():
        print("Морской бой" * 1)


# Класс Игроков
class Player:
    def __init__(self):
        self.name = None
        self.board = None


# Класс Компьютера
class AIPlayer(Player):
    def __init__(self):
        super().__init__()
        self.name = 'Компьютер'
        self.position = Position(0, 0)

    health_points = 11

    def take_shot(self, opponents_board):
        while True:
            self.position.x, self.position.y = random.randint(1, 6), random.randint(1, 6)
            if opponents_board[self.position.x][self.position.y] in ['T', 'X']:
                continue
            break
        if opponents_board[self.position.x][self.position.y] == '■':
            opponents_board[self.position.x][self.position.y] = 'X'
            print('Компьютер попал в цель!')
            HumanPlayer.health_points -= 1
            if HumanPlayer.health_points == 0:
                print('Компьютер победил!')
                exit()
        else:
            opponents_board[self.position.x][self.position.y] = 'T'
            print('Компьютер промахнулся!')
        time.sleep(1)


# Класс человека-игрока
class HumanPlayer(Player):
    def __init__(self):
        super().__init__()
        self.name = 'Игрок'
        self.position = Position(0, 0)

    health_points = 11

    def take_shot(self, opponents_board):
        while True:
            try:
                shot_input = input('Введите координаты через пробел (x,y): ')
                self.position.x, self.position.y = map(int, shot_input.split())
                if self.position.x in range(1, 7) and self.position.y in range(1, 7):
                    if opponents_board[self.position.x][self.position.y] in ['T', 'X']:
                        print('Сюда уже стреляли. Повторите попытку!')
                        continue
                    break
            except (ValueError, IndexError):
                print('Неверный ввод, введите координаты повторно!')
        if opponents_board[self.position.x][self.position.y] == '■':
            opponents_board[self.position.x][self.position.y] = 'X'
            print('Игрок попал!')
            AIPlayer.health_points -= 1
            if AIPlayer.health_points == 0:
                print('Игрок победил!')
                exit()
        else:
            opponents_board[self.position.x][self.position.y] = 'T'
            print('Игрок промахнулся')
        time.sleep(0.5)


# Класс игровой доски
class GameBoard:
    def __init__(self, size=8):
        self.field = None
        self.size = size
        self.vessel = Ship()

    def setup_board(self):
        board = None
        while board is None:
            board = self.generate_board(self.vessel)
        return board

    def generate_board(self, vessel):
        self.field = [[0] * 8 for _ in range(8)]
        attempts = 0
        for ship_length in vessel.sizes:
            while True:
                count = 0
                orientation = random.choice([-1, 1])  # Random orientation
                position = Position(random.randint(0, 5), random.randint(0, 5))

                if orientation == -1 and position.x + ship_length <= self.size - 2 and vessel.can_place_ship(self.field,
                                                                                                             position,
                                                                                                             ship_length,
                                                                                                             orientation):
                    count += 2
                if orientation == 1 and position.y + ship_length <= self.size - 2 and vessel.can_place_ship(self.field,
                                                                                                            position,
                                                                                                            ship_length,
                                                                                                            orientation):
                    count += 2

                if self.field[position.x + 1][position.y + 1] == 0:
                    count += 1

                if count == 3:
                    break

                attempts += 1
                if attempts > 99:
                    return None

            for i in range(ship_length):
                self.field[position.x + 1][position.y + 1] = '■'
                if orientation == -1:
                    position.x += 1  # Вниз
                else:
                    position.y += 1  # Вправо

        return self.field

    def display(self, board, player_name):
        print(f'Доска игрока {player_name}')
        print("   | 1 | 2 | 3 | 4 | 5 | 6 |")
        for i in range(self.size - 2):
            print(i + 1, '', end='|')
            for j in range(self.size - 2):
                if player_name == 'Компьютер':
                    print('', board[i + 1][j + 1] if board[i + 1][j + 1] in ['X', 'T'] else '0', '', end='|')
                else:
                    print('', board[i + 1][j + 1], '', end='|')
            print()
        print()


if __name__ == "__main__":
    game_instance = BattleShipGame()
    game_instance.run()
