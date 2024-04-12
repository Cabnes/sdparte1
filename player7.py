import pygame
import gamemech
from rastros import Rastros
from rastro import Rastro

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# Player 7 is part of the test example 7
# It defines a sprite with size rate
class Player(pygame.sprite.DirtySprite):
    # Já não precisamos da acelaração. As posições são as posições dos quadrados... size é a dimensão do quadrado
    def __init__(self,pos_x:int, pos_y:int, size:int, my_id: int, *groups):

    #def __init__(self,pos_x:int, pos_y:int, acc:int, size:int, *groups ):
        super().__init__(*groups)
        self.my_id = my_id
        self.size = size
        self.boost = False
        self.contador = 0
        self.boost_ativo = False
        self.image = pygame.image.load('pixel_racecar_orange.png')
        initial_size = self.image.get_size()
        size_rate = size / initial_size[0]
        #self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))

        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        #self.image = pygame.transform.scale(self.image, self.new_size)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.image_inicial = self.image

        #self.rect = pygame.rect.Rect((pos_x,pos_y), self.image.get_size())
        self.rect = pygame.rect.Rect((pos_x * size ,pos_y * size), self.image.get_size())
        #self.acc = acc
        self.pos:list = [pos_x, pos_y]
        self.direcao = LEFT
        self.rastros = Rastros()

    def get_size(self):
        return self.new_size

    def get_id(self):
        return self.my_id

    def set_boost(self, boost: bool):
        self.boost = boost
#    def update(self, dt:float, game:object):
    # Já não definimos a velocidade. Eles irão deslocar-se todos à mesma velocidade...
    def update(self, game: object, gm: gamemech.GameMech, *groups) -> bool:
        key = pygame.key.get_pressed()
        new_pos = self.pos
        if key[pygame.K_LEFT] and self.direcao != RIGHT:
            self.direcao = LEFT
        elif key[pygame.K_RIGHT] and self.direcao != LEFT:
            self.direcao = RIGHT
        elif key[pygame.K_UP] and self.direcao != DOWN:
            self.direcao = UP
        elif key[pygame.K_DOWN] and self.direcao != UP:
            self.direcao = DOWN
        elif key[pygame.K_SPACE]:
            if self.boost:
                self.boost_ativo = True
                self.contador += 1
        if self.direcao == RIGHT:
            # self.rect.x += self.acc * dt
            if self.boost_ativo and self.contador < 10:
                self.contador += 1
                contador = 2

            elif self.boost_ativo and self.contador >= 10:
                self.contador = 0
                contador = 1
                self.boost = False
                self.boost_ativo = False
            else:
                contador = 1
            for i in range(contador):
                gm.check_boost(self, self.direcao)
                new_pos = gm.check_caminho(self.my_id, self.direcao)
                if None in new_pos:
                    return True
                # new_pos = [self.pos[0] + 1, self.pos[1]]
                self.rect.x = new_pos[0] * self.size
                self.rect.y = new_pos[1] * self.size
                rastro = Rastro(self.pos[0], self.pos[1], self.size, "laranja.png", *groups)
                self.rastros.adicionar_rastro(rastro)
                self.rastros.remover_rastro()
                self.pos = new_pos
                self.image = pygame.transform.rotate(self.image_inicial, 90)
        elif self.direcao == LEFT:
            if self.boost_ativo and self.contador < 10:
                self.contador += 1
                contador = 2
            elif self.boost_ativo and self.contador >= 10:
                self.contador = 0
                contador = 1
                self.boost = False
                self.boost_ativo = False
            else:
                contador = 1
            for i in range(contador):
                gm.check_boost(self, self.direcao)
                new_pos = gm.check_caminho(self.my_id, self.direcao)
                if None in new_pos:
                    return True
                # new_pos = [self.pos[0] - 1, self.pos[1]]
                self.rect.x = new_pos[0] * self.size
                self.rect.y = new_pos[1] * self.size
                rastro = Rastro(self.pos[0], self.pos[1], self.size, "laranja.png", *groups)
                self.rastros.adicionar_rastro(rastro)
                self.rastros.remover_rastro()
                self.pos = new_pos
                self.image = pygame.transform.rotate(self.image_inicial, 270)
        elif self.direcao == UP:
            if self.boost_ativo and self.contador < 10:
                self.contador += 1
                contador = 2
            elif self.boost_ativo and self.contador >= 10:
                self.contador = 0
                contador = 1
                self.boost = False
                self.boost_ativo = False
            else:
                contador = 1
            for i in range(contador):
                # self.rect.y -= self.acc * dt
                gm.check_boost(self, self.direcao)
                new_pos = gm.check_caminho(self.my_id, self.direcao)
                if None in new_pos:
                    return True
                # new_pos = [self.pos[0], self.pos[1] - 1]
                self.rect.x = new_pos[0] * self.size
                self.rect.y = new_pos[1] * self.size
                rastro = Rastro(self.pos[0], self.pos[1], self.size, "laranja.png", *groups)
                self.rastros.adicionar_rastro(rastro)
                self.rastros.remover_rastro()
                self.pos = new_pos
                self.image = pygame.transform.rotate(self.image_inicial, 0)
        elif self.direcao == DOWN:
            if self.boost_ativo and self.contador < 10:
                self.contador += 1
                contador = 2
            elif self.boost_ativo and self.contador >= 10:
                self.contador = 0
                contador = 1
                self.boost = False
                self.boost_ativo = False
            else:
                contador = 1
            for i in range(contador):
                gm.check_boost(self, self.direcao)
                new_pos = gm.check_caminho(self.my_id, self.direcao)
                if None in new_pos:
                    return True
                # new_pos = [self.pos[0], self.pos[1] + 1]
                self.rect.x = new_pos[0] * self.size
                self.rect.y = new_pos[1] * self.size
                rastro = Rastro(self.pos[0], self.pos[1], self.size, "laranja.png", *groups)
                self.rastros.adicionar_rastro(rastro)
                self.rastros.remover_rastro()
                self.pos = new_pos
                self.image = pygame.transform.rotate(self.image_inicial, 180)
        self.pos = new_pos
        # Keep visible
        self.dirty = 1
        return False

    def kill(self):
        for i in self.rastros.get_rastros():
            i.kill()
        super().kill()
