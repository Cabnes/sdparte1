

# fazer aqui tudo como o prof tem mais ou menos


import random

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
import random
import client.ui.boost as boost


class GameMech:
    def __init__(self, nr_x: int, nr_y: int):
        self.world = {}
        self.players: dict = {}
        self.rastros: dict = {}
        self.new_rastros: dict = {}
        self.boost: dict = {}
        self.x_max: int = nr_x
        self.y_max: int = nr_y
        self.empty = []
        self.nr_players = 0
        self.pos_players = {0: (4, self.y_max // 2), 1: (self.x_max - 5, self.y_max // 2)}
        self.players_ready = [False, False]
        self.game_over = [False, False]
        for x in range(nr_x):
            for y in range(nr_y):
                self.world[(x, y)] = None
                self.empty.append((x, y))

    def reset_gamemech(self):
        self.world = {}
        self.players: dict = {}
        self.rastros: dict = {}
        self.new_rastros: dict = {}
        self.boost: dict = {}
        self.empty = []
        self.nr_players = 0
        self.pos_players = {0: (4, self.y_max // 2), 1: (self.x_max - 5, self.y_max // 2)}
        self.players_ready = [False, False]
        self.game_over = [False, False]
        for x in range(self.x_max):
            for y in range(self.y_max):
                self.world[(x, y)] = None
                self.empty.append((x, y))

    def get_nr_x(self) -> int:
        return self.x_max

    def get_nr_y(self) -> int:
        return self.y_max


    def player_ready(self, id):
        self.players_ready[id] = True

    def get_players_ready(self):
        player1, player2 = self.players_ready
        if player1 and player2:
            return True
        else:
            return False

    def check_boost(self, player, direction):
        x, y = self.players[player.get_id()][1][0], self.players[player.get_id()][1][1]
        x, y = self.execute(x, y, direction)
        if self.world[(x, y)] == ["boost"]:
            player.set_boost(True)
            self.world[(x, y)] = None
            self.empty.append((x, y))

    def player_game_over(self, nr_player):
        self.game_over[nr_player] = True

    def get_game_over(self):
        return self.game_over

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
        if len(self.rastros[nr_player]) <= 100:
            self.new_rastros[nr_player][0] = False
        if self.world[(x, y)] is not None:
            self.player_game_over(nr_player)
            return None
        self.world[old_pos] = ["rastro", nr_player, 0]
        self.world[(x, y)] = ["player", self.players[nr_player][0], nr_player]
        self.empty.remove((x, y))
        self.players[nr_player][1] = (x, y)
        self.players[nr_player][2] = direction
        self.rastros[nr_player].append(old_pos)
        self.new_rastros[nr_player][1] = old_pos
        if len(self.rastros[nr_player]) > 100:
            pos = self.rastros[nr_player].pop(0)
            self.new_rastros[nr_player][0] = True
            self.world[pos] = None
            self.empty.append(pos)
        return x, y

    def get_players(self):
        lst = []
        for i in self.players:
            lst.append(self.players[i])
        return lst

    def posicao_boost(self):
        (x, y) = random.choice(self.empty)
        self.boost["boost"] = [x, y]
        self.world[(x, y)] = ["boost", "", 0]
        self.empty.remove((x, y))
        return x, y

    def get_world(self):
        return [self.players, self.new_rastros]

    def add_player(self, name:str) -> tuple:
        self.players[self.nr_players] = [name, self.pos_players[self.nr_players], self.nr_players + 1]
        self.world[self.pos_players[self.nr_players]] = ["player", name, self.nr_players]
        self.rastros[self.nr_players] = []
        self.new_rastros[self.nr_players] = [False, ()]
        self.empty.remove(self.pos_players[self.nr_players])
        self.nr_players += 1
        return (self.nr_players - 1, self.pos_players[self.nr_players - 1])