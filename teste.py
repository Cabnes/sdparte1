import pygame
import player7
import player8
import gamemech
import boost
import time
from random import randint


class Menu(object):
    def __init__(self, tela, size):
        self.tela = tela
        self.grid_size = size
        self.width, self.height = tela.get_size()
        self.background = pygame.Surface(self.tela.get_size())
        self.background.fill((0, 0, 0))
        self.fonte_grande = pygame.font.Font(None, 60)
        self.fonte_pequena = pygame.font.Font(None, 36)

    def mostrar_menu(self):
        self.tela.blit(self.background, (0, 0))
        titulo = self.fonte_grande.render("Jogo da Cobra", True, (255, 255, 255))
        instrucoes = self.fonte_pequena.render("Pressione qualquer tecla para começar", True, (255, 255, 255))
        self.tela.blit(titulo, ((self.width - titulo.get_width()) / 2, self.height / 3))
        self.tela.blit(instrucoes, ((self.width - instrucoes.get_width()) / 2, self.height / 2))
        pygame.display.flip()

        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    esperando = False
                    self.tela.blit(self.background, (0, 0))
                    self.draw_grid(self.width, self.height, self.grid_size, (17, 41, 173))

    def draw_grid(self,width:int, height:int, size: int, colour:tuple):
        '''
        Desenha uma grelha, assumindo que o mundo é quadrado. Como fazer se o mundo não é quadrado?
        :param width: dimensão no eixo dos xx da janela
        :param height: dimensão no eixo dos yy da janela
        :param size: the size of the grid
        :param colour:
        :return:
        '''

        # Desenhar as linhas horizontais
        for pos in range(0, height, size):
            pygame.draw.line(self.tela, colour, (0, pos), (width,pos))
        # Desenhar as linhas verticais
        for pos in range(0, width, size):
            pygame.draw.line(self.tela, colour, (pos, 0), (pos,height))


class Game(object):
    #def __init__(self, width:int = 640, height:int = 480):
    def __init__(self, screen, nr_x: int = 20, nr_y: int = 20, size: int = 20):
        self.width, self.height = nr_x * size, nr_y * size
        self.nrx, self.nry = nr_x, nr_y
        self.gm = gamemech.GameMech(nr_x, nr_y)
        #self.width, self.height = width, height
        self.screen = screen
        pygame.display.set_caption("grid game")
        self.clock = pygame.time.Clock()
        # Grid
        self.grid_size = size
        # Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        # Convert the image to a better format to blit
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.draw_grid(self.width, self.height, self.grid_size, (17, 41, 173))
        self.game_over = False
        self.pontuacao = {0: 0, 1: 0}
        pygame.display.update()

    def draw_grid(self,width:int, height:int, size: int, colour:tuple):
        '''
        Desenha uma grelha, assumindo que o mundo é quadrado. Como fazer se o mundo não é quadrado?
        :param width: dimensão no eixo dos xx da janela
        :param height: dimensão no eixo dos yy da janela
        :param size: the size of the grid
        :param colour:
        :return:
        '''

        # Desenhar as linhas horizontais
        for pos in range(0, height, size):
            pygame.draw.line(self.screen, colour, (0, pos), (width,pos))
        # Desenhar as linhas verticais
        for pos in range(0, width, size):
            pygame.draw.line(self.screen, colour, (pos, 0), (pos,height))

    def create_players(self,size:int) -> None:
        '''

        :param self:
        :param size:
        :return:
        '''
        #self.players = pygame.sprite.Group()
        self.players = pygame.sprite.LayeredDirty()
        # Vamos querer identificar a posição dos jogadores de acordo com a grelha...
        self.playerA = player7.Player(self.nrx - 5, self.nry // 2, size, 0, self.players)
        self.playerB = player8.Player(4, self.nry // 2, size, 1, self.players)

        #self.playerA = player7.Player(15,120,300,size,self.players)
        #self.playerB = player7.Player(50,55,150,size,self.players)
        self.players.add(self.playerA)
        self.players.add(self.playerB)

    '''def create_walls(self, wall_size:int):
        # Create Wall (sprites) around world
        self.walls = pygame.sprite.Group()
        for x in range(0,self.width,wall_size):
            for y in range(0,self.height,wall_size):
                if x in (0,self.width - wall_size) or y in (0, self.height - wall_size):
                    w = wall.Wall(x,y,0,wall_size,self.walls)
                    self.walls.add(w)
        # Additional walls
        w = wall.Wall(200,200,0,wall_size,self.walls)
        self.walls.add(w)'''

    def tabela_pontuacao(self):
        fonte = pygame.font.SysFont(None, 40)
        pontuacao_0 = fonte.render("Jogador 1:",
                                True, ((255, 255, 255)))
        pontuacao_0_rect = pontuacao_0.get_rect(center=(self.width / 12, self.height / 14))
        self.screen.blit(pontuacao_0, pontuacao_0_rect)
        if self.pontuacao[0] >= 1:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)
        rec_w = 50
        rec_h = 25
        pygame.draw.rect(self.screen, color, pygame.Rect((self.width / 12) * 2 - rec_w / 2, self.height / 14 - rec_h / 2, 50, 25))
        if self.pontuacao[0] == 2:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)
        pygame.draw.rect(self.screen, color,
                         pygame.Rect((self.width / 12) * 2 - rec_w / 2 + rec_w + 10, self.height / 14 - rec_h / 2, 50, 25))
        pontuacao_1 = fonte.render("Jogador 2:",
                                   True, ((255, 255, 255)))
        pontuacao_1_rect = pontuacao_1.get_rect(center=((self.width / 12) * 9, self.height / 14))
        if self.pontuacao[1] >= 1:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)
        pygame.draw.rect(self.screen, color,
                         pygame.Rect((self.width / 12) * 10 - rec_w / 2, self.height / 14 - rec_h / 2, 50,
                                     25))
        if self.pontuacao[1] == 2:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)
        pygame.draw.rect(self.screen, color,
                         pygame.Rect((self.width / 12) * 10 - rec_w / 2 + rec_w + 10, self.height / 14 - rec_h / 2, 50,
                                     25))
        self.screen.blit(pontuacao_1, pontuacao_1_rect)


    def run(self):
        #Create Sprites
        #self.create_walls(self.grid_size)
        #self.walls.draw(self.screen)
        self.create_players(self.grid_size)
        self.tabela_pontuacao()
        end = False
        inicio = time.time()
        while end == False:
            #dt = self.clock.tick(10)
            self.clock.tick(10)
            while self.game_over:
                #self.screen.fill((0, 0, 0))
                fonte = pygame.font.SysFont(None, 60)
                mensagem = fonte.render("Fim de Jogo! Para jogar novamente, pressione Espaço.",
                                        True, ((255, 255, 255)))
                mensagem_rect = mensagem.get_rect(center=(self.width / 2, self.height / 8))
                self.screen.blit(mensagem, mensagem_rect)
                for i in self.pontuacao:
                    if self.pontuacao[i] == 3:
                        self.game_over = False
                        end = True
                        self.game_over = False

                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game_over = False
                        end = True
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.game_over = False
                        end = True
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.players.empty()
                        self.screen.blit(self.background, (0, 0))
                        self.draw_grid(self.width, self.height, self.grid_size, (17, 41, 173))
                        self.game_over = False
                        self.gm = gamemech.GameMech(self.nrx, self.nry)
                        self.tabela_pontuacao()
                        return self.run()
            fim = time.time()
            if round(fim - inicio, 0) % 6 == 0 and randint(1, 15) == 1:
                self.create_boost(self.players)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    end = True
             # Update the position of players...
            #self.players.update(dt / 1000.,self)
            for i in self.players:
                if i.update(self, self.gm, self.players):
                    self.game_over = True
                    self.pontuacao[i.get_id()] += 1
            # We are not going to print all the screen again...
            #self.screen.fill((200,200,200))
            # We keep only rectangles we need to render
            rects = self.players.draw(self.screen)
            # We don't touch the walls, at least we don't
            #self.walls.draw(self.screen)
            #pygame.display.flip()
            # We draw the grid: Why? Try to remove the command...
            self.draw_grid(self.width, self.height, self.grid_size, (17, 41, 173))
            self.tabela_pontuacao()

            # We call update to pygame display
            pygame.display.update(rects)
            # Why do we clear screen and background?
            self.players.clear(self.screen, self.background)

        pygame.display.update()

        return

    def create_boost(self, *groups):
        pos_x, pos_y = self.gm.posicao_boost()
        new_boost = boost.Boost(pos_x, pos_y, self.grid_size, "verde.png", *groups)
        return new_boost

def main():
    pygame.init()
    nr_x, nr_y, size = 90, 40, 15
    width, height = nr_x * size, nr_y * size
    tela = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Jogo da Cobra')
    menu = Menu(tela, size)
    game = Game(tela, nr_x, nr_y, size)

    while True:
        menu.mostrar_menu()
        game.run()

if __name__ == '__main__':
    main()
