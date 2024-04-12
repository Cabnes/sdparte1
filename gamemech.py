import random

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
import random
import boost

class GameMech:
    def __init__(self, nr_x: int, nr_y: int):
        self.world = {}
        self.players: dict = {}
        self.rastros: dict = {}
        self.boost: dict = {}
        self.x_max: int = nr_x
        self.y_max: int = nr_y
        self.empty = []
        for x in range(nr_x):
            for y in range(nr_y):
                self.world[(x, y)] = None
                self.empty.append((x, y))
        self.players[0] = ["jose", (self.x_max - 5, self.y_max // 2)]
        self.world[(self.x_max - 5, self.y_max // 2)] = ["player", "jose", 0]
        self.empty.remove((x, y))
        self.rastros[0] = []

        self.players[1] = ["manuel", (4, self.y_max // 2)]
        self.world[(4, self.y_max // 2)] = ["player", "manuel", 1]
        self.rastros[1] = []


    def check_boost(self, player, direction):
        x, y = self.players[player.get_id()][1][0], self.players[player.get_id()][1][1]
        x, y = self.execute(x, y, direction)
        if self.world[(x, y)] == ["boost"]:
            player.set_boost(True)
            self.world[(x, y)] = None
            self.empty.append((x, y))



    def execute(self, x, y, direction: int):
        if direction == UP:
            y -= 1
        elif direction == RIGHT:
            x += 1
        elif direction == DOWN:
            y += 1
        elif direction == LEFT:
            x -= 1
        if x >= self.x_max:
            print(x)
            x = 0
        if x < 0:
            x = self.x_max - 1
        if y >= self.y_max:
            y = 0
        if y < 0:
            y = self.y_max - 1

        return x, y




    def check_caminho(self, nr_player, direction):
        old_pos = self.players[nr_player][1]
        x, y = self.players[nr_player][1][0], self.players[nr_player][1][1]
        x,y = self.execute(x, y, direction)
        if self.world[(x, y)] is not None:
            return None, None
        self.world[old_pos] = ["rastro", nr_player, 0]
        self.world[(x, y)] = ["player", self.players[nr_player][0], nr_player]
        self.empty.remove((x, y))
        self.players[nr_player][1] = (x, y)
        self.rastros[nr_player].append(old_pos)
        if len(self.rastros[nr_player]) > 100:
            pos = self.rastros[nr_player].pop(0)
            self.world[pos] = None
            self.empty.append(pos)
        return x, y


    def posicao_boost(self):
        (x, y) = random.choice(self.empty)
        self.boost[boost] = [x, y]
        self.world[(x, y)] = ["boost"]
        self.empty.remove((x, y))
        return x, y



