from random import randrange

class BoardOutException (Exception):
    def __init__(self, text):
        super()
        self.text = text

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Ship:
    def __init__(self, dot, width, horzOrVert):
        self.pos = dot
        self.width = width
        self.horzOrVert = horzOrVert
        self.lives = width

    def hit(self, dot):
        if (self.horzOrVert):
            wx = self.width
        else:
            wx = 1
        if (not self.horzOrVert):
            hy = self.width
        else:
            hy = 1

        if dot.x < self.pos.x or dot.y < self.pos.y:
            return False
        if dot.x >= self.pos.x + wx or dot.y >= self.pos.y + hy:
            return False
        self.lives = self.lives - 1
        return True


class Board:
    # o - nothing
    # T - miss
    # X - hit
    # * - ship
    def __init__(self, width, height, hidden):
        self.width = width
        self.height = height
        self.hidden = hidden

        self.spaces = []
        for i in range(0, height):
            x = []
            for j in range(0, width):
                x.append('o')
            self.spaces.append(x)

        self.ships = []
        self.live_ships = 0

    def print_state(self):
        print ('  0 1 2 3 4 5')
        print ('-------------')
        for i in range(0, self.height):
            x = str(i) + '|'
            for j in range(0, self.width):
                x = x + ' '
                if self.hidden and self.spaces[i][j] == '*':
                    x = x + 'o'
                else:
                    x = x + self.spaces[i][j]
            print (x)



    def add_ship(self, ship):
        if (ship.horzOrVert):
            ship_wx = ship.width
        else:
            ship_wx = 1
        if (not ship.horzOrVert):
            ship_hy = ship.width
        else:
            ship_hy = 1

        # Check if ship inside the board
        if (ship.pos.x < 0 or ship.pos.x + ship_wx >= self.width):
            raise BoardOutException (f'Ship with pos {ship.pos.x}, {ship.pos.y} is out of board')
        if (ship.pos.y < 0 or ship.pos.y + ship_hy >= self.height):
            raise BoardOutException (f'Ship with pos {ship.pos.x}, {ship.pos.y} is out of board')

        # Check ship size
        if ship.width < 1 or ship.width > 3:
            raise BoardOutException(f'Ship has wrong size: {ship.width}')

        # Check if we reached limits for shiup types
        ship_3w = 0
        ship_2w = 0
        ship_1w = 0
        for i in range(0, len(self.ships)):
            if self.ships[i].width == 3:
                ship_3w = ship_3w + 1
            elif self.ships[i].width == 2:
                ship_2w = ship_2w + 1
            else:
                ship_1w = ship_1w + 1

        if (ship.width == 3 and ship_3w > 0):
            raise BoardOutException(f'Ship with size {ship.width} exceeds limit')
        if (ship.width == 2 and ship_2w > 1):
            raise BoardOutException(f'Ship with size {ship.width} exceeds limit')
        if (ship.width == 1 and ship_1w > 3):
            raise BoardOutException(f'Ship with size {ship.width} exceeds limit')

        # Check if requested board popsition is empty
        if (self.spaces[ship.pos.y][ship.pos.x] != 'o'):
            raise BoardOutException(f'Ship with pos {ship.pos.x} {ship.pos.y} crashed with other ship')
        if (ship.pos.x > 0 and self.spaces[ship.pos.y][ship.pos.x - 1] != 'o'):
            raise BoardOutException(f'Ship with pos {ship.pos.x} {ship.pos.y} crashed with other ship')
        if (ship.pos.y > 0 and self.spaces[ship.pos.y - 1][ship.pos.x] != 'o'):
            raise BoardOutException(f'Ship with pos {ship.pos.x} {ship.pos.y} crashed with other ship')

        if (ship.width > 1):
            if ship.horzOrVert:
                if self.spaces[ship.pos.y][ship.pos.x + 1] != 'o':
                    raise BoardOutException(f'Horizontal Ship with pos {ship.pos.x} {ship.pos.y} and size {ship.width} crashed with other ship')
                if ship.width > 2 and self.spaces[ship.pos.y][ship.pos.x + 2] != 'o':
                    raise BoardOutException(f'Horizontal Ship with pos {ship.pos.x} {ship.pos.y} and size {ship.width} crashed with other ship')
            else:
                if self.spaces[ship.pos.y + 1][ship.pos.x] != 'o':
                    raise BoardOutException(f'Vertical Ship with pos {ship.pos.x} {ship.pos.y} and size {ship.width} crashed with other ship')
                if ship.widh > 2 and self.spaces[ship.pos.y + 2][ship.pos.x] != 'o':
                    raise BoardOutException(f'Vertical Ship with pos {ship.pos.x} {ship.pos.y} and size {ship.width} crashed with other ship')


        # Adding new ship
        self.ships.append(ship)
        self.live_ships = self.live_ships + 1

        self.spaces[ship.pos.y][ship.pos.x] = '*'
        if ship.width > 1:
            if ship.horzOrVert:
                self.spaces[ship.pos.y][ship.pos.x + 1] = '*'
            else:
                self.spaces[ship.pos.y + 1][ship.pos.x] = '*'
        if ship.width > 2:
            if ship.horzOrVert:
                self.spaces[ship.pos.y][ship.pos.x + 2] = '*'
            else:
                self.spaces[ship.pos.y + 2][ship.pos.x] = '*'

        #we did it!
        return


    def out(self, dot):
        return dot.x < 0 or dot.x >= self.width or dot.y < 0 or dot.y >= self.height

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException(f'Shoot miosses board: {dot.x} {dot.y}')

        if self.spaces[dot.y][dot.x] == 'o':
            self.spaces[dot.y][dot.x] = 'T'
            return False

        if self.spaces[dot.y][dot.x] != '*':
            raise BoardOutException(f'Shoot should be at unused space: {dot.x} {dot.y}')

        for i in range(0, len(self.ships)):
            self.ships[i].hit(dot)
        self.spaces[dot.y][dot.x] = 'X'
        return True


    def has_alive_ships(self):
        for i in range(0, len(self.ships)):
            if self.ships[i].lives > 0:
                return True
        return False

class Player:
    def __init__(self, my_board, enemy_board):
        self.my_board = my_board
        self.enemy_board = enemy_board

    def ask(self):
        return Dot(-1, -1)

    def move(self):
        dot = self.ask()
        try:
            return self.enemy_board.shot(dot)
        except BoardOutException as exception:
            print (exception.text)
            return self.move()


class AI (Player):
    def __init__(self, my_board, enemy_board):
        super().__init__(my_board, enemy_board)


    def ask(self):
        return Dot(randrange(0, self.my_board.width), randrange(0, self.my_board.height))



class User (Player):
    def __init__(self, my_board, enemy_board):
        super().__init__(my_board, enemy_board)


    def ask(self):
        print('Your board:')
        self.my_board.print_state()
        print('Enemy board:')
        self.enemy_board.print_state()

        ask = input('Ваш ход (x,y)')
        (xc, yc) = ask.split(',')
        return Dot(int(xc), int(yc))


class Game:
    def __init__(self):
        self.board_player = Board(6, 6, False)
        self.board_computer = Board(6, 6, True)
        self.player = User(my_board=self.board_player, enemy_board=self.board_computer)
        self.computer = AI(my_board=self.board_computer, enemy_board=self.board_player)
        self.random_board(self.board_player)
        self.random_board(self.board_computer)


    def greet(self):
        print('Hello! This is well-known ship battle game.')
        print('Enter your coordinates in form x,y')

    def loop(self):
        while (self.board_player.has_alive_ships()):
            while self.player.move():
                if not self.board_computer.has_alive_ships():
                    print ('You have won!')
                    return
            while self.computer.move():
                if not self.board_player.has_alive_ships():
                    print ('You loose!')
                    return
        print('You have no ships!')


    def start(self):
        self.greet()
        self.loop()


    def try_add_ship(self, board, width):
        dot = Dot(randrange(0, board.width), randrange(0, board.height))
        ship = Ship(dot, width, randrange(0, 1) == 0)
        board.add_ship(ship)

    # 1 3-ship
    # 2 2-ships
    # 4 1-ships
    def random_board(self, board):

        # First we trying biggest ship
        attempts = 0
        not_added = True
        while not_added:
            try:
                self.try_add_ship(board, 3)
                not_added = False

            except BoardOutException:
                not_added = True

        added = 0
        while added < 2:
            try:
                self.try_add_ship(board, 2)
                added = added + 1

            except BoardOutException:
                attempts = attempts + 1
                if attempts > 10000:
                    raise BoardOutException('Bad board')


        added = 0
        while added < 4:
            try:
                self.try_add_ship(board, 1)
                added = added + 1

            except BoardOutException:
                attempts = attempts + 1
                if attempts > 10000:
                    raise BoardOutException('Bad board')
        return



def main():
    good_board = False
    while not good_board:
        try:
            game = Game()
            good_board = True
            game.start()
        except BoardOutException:
            pass

main()
