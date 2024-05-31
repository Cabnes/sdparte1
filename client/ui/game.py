import pygame
import player7
from client.stub.client_stub import ClientStub
import boost
from rastro import Rastro
import time
from button import Button
import threading

# ----------------------------------------------------------------------------
# A grid is added to the world. Now, sprites move step by step
# on the grid. This will allow us to discretise the world
# It is used the DirtySprite concept. It allows to update only the part of
# the screen that changes.
# We need to align objects position to the grid. How?
# ----------------------------------------------------------------------------



class Game(object):
    # def __init__(self, width:int = 640, height:int = 480):
    #def __init__(self, nr_x: int = 20, nr_y: int = 20, size: int = 20):
    def __init__(self, cs: ClientStub, size: int):
        self.cs = cs
        self.id = ""

        self.nr_x = self.cs.get_nr_quad_x()
        self.nr_y = self.cs.get_nr_quad_y()
        self.width, self.height = self.nr_x * size, self.nr_y * size # isto está no video 3 minuto 2:10
        self.max_x, self.max_y = self.nr_x, self.nr_y
        self.screen = pygame.display.set_mode((self.width, self.height))
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
        self.players = pygame.sprite.LayeredDirty()
        self.rastro_verde = pygame.sprite.LayeredDirty()
        self.rastro_laranja = pygame.sprite.LayeredDirty()
        pygame.display.update()
        self.create_players(self.grid_size)

    def draw_grid(self, width: int, height: int, size: int, colour: tuple):
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
            pygame.draw.line(self.screen, colour, (0, pos), (width, pos))
        # Desenhar as linhas verticais
        for pos in range(0, width, size):
            pygame.draw.line(self.screen, colour, (pos, 0), (pos, height))

    def create_players(self, size:int) -> None:
        #name = str(input("What is ur name? "))
        name = "ggfbd"
        (self.id, pos) = self.cs.set_player(name)  # A POSIÇÃO VAI SER USADA
        print("Player", name, "created with id:", self.id, "pos: ", pos)
        pygame.display.set_caption(f"grid game id{self.id}")
        if self.id == 0:
            self.playerA = player7.Player(pos[0], pos[1], "pixel_racecar_green.png", size, self.id, self.cs, 1,
                                          self.players)  # PARA COLOCAR O OBJETO NA POSIÇÃO DEFINIDA PELO LADO DO SERVIDOR
            self.players.add(self.playerA)
        elif self.id == 1:
            self.playerB = player7.Player(pos[0], pos[1], "pixel_racecar_orange.png", size, self.id, self.cs, 3
                                          , self.players) # PARA COLOCAR O OBJETO NA POSIÇÃO DEFINIDA PELO LADO DO SERVIDOR
            self.players.add(self.playerB)

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
        pygame.draw.rect(self.screen, color,
                         pygame.Rect((self.width / 12) * 2 - rec_w / 2, self.height / 14 - rec_h / 2, 50, 25))
        if self.pontuacao[0] == 2:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)
        pygame.draw.rect(self.screen, color,
                         pygame.Rect((self.width / 12) * 2 - rec_w / 2 + rec_w + 10, self.height / 14 - rec_h / 2, 50,
                                     25))
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

    def main_menu(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid(self.width, self.height, self.grid_size, (17, 41, 173))
        while True:
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(self.width / 2, self.height / 6))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(self.width / 2,
                                                                                       self.height * 3/6),
                                 text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(self.width / 2,
                                                                                       self.height * 4/6 +
                                                                                       self.height / 16),
                                 text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.change_color(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.check_for_input(MENU_MOUSE_POS):
                        self.waiting_room()
                        return
                    if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                        pygame.quit()
                        return

            pygame.display.update()

    def start_game(self):
        self.cs.execute_start_game()
        print("going to start game")
        global waiting_end
        waiting_end = True

    def waiting_room(self):
        self.cs.ready_player()
        global waiting_end
        waiting_end = False
        thread = threading.Thread(target=self.start_game)
        thread.start()
        while not waiting_end:

            self.screen.fill("black")

            PLAY_TEXT = get_font(20).render("This is the Waiting Room. "
                                            "Wait for other player.", True, "White")
            PLAY_RECT = PLAY_TEXT.get_rect(center=(self.width / 2, self.height / 2))
            self.screen.blit(PLAY_TEXT, PLAY_RECT)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

            pygame.display.update()
        time.sleep(1)
        self.run()

    def update_world(self):
        (players, rastros) = self.cs.get_world()
        self.players.empty()
        for id_player in players:
            pos = players[id_player][1]
            direction = players[id_player][2]
            id_player = int(id_player)
            if id_player == 0:
                playerA = player7.Player(pos[0], pos[1], "pixel_racecar_green.png", self.grid_size, id_player, self.cs, direction,
                                         self.players)  # PARA COLOCAR O OBJETO NA POSIÇÃO DEFINIDA PELO LADO DO SERVIDOR
                self.players.add(playerA)
            elif id_player == 1:
                playerB = player7.Player(pos[0], pos[1], "pixel_racecar_orange.png", self.grid_size, id_player, self.cs, direction,
                                         self.players)  # PARA COLOCAR O OBJETO NA POSIÇÃO DEFINIDA PELO LADO DO SERVIDOR
                self.players.add(playerB)

        color = None
        group = None
        for i in rastros:
            if i == "0":
                color = "verde.png"
                group = self.rastro_verde
            elif i == "1":
                color = "laranja.png"
                group = self.rastro_laranja
            if rastros[i][0]:
                sprites = group.sprites()
                if sprites:
                    group.remove(sprites[0])
            if len(rastros[i][1]) > 0:
                group.add(Rastro(rastros[i][1][0], rastros[i][1][1], self.grid_size, color, group))

    def run(self):
        end = False
        inicio = time.time()
        self.screen.fill((0, 0, 0))
        self.draw_grid(self.width, self.height, self.grid_size, (17, 41, 173))
        while end == False:
            # dt = self.clock.tick(10)
            self.clock.tick(20)
            while self.game_over:
                # self.screen.fill((0, 0, 0))
                fonte = pygame.font.SysFont(None, 60)
                mensagem = fonte.render("Fim de Jogo! Para voltar para o menu, pressione Espaço.",
                                        True, ((255, 255, 255)))
                mensagem_rect = mensagem.get_rect(center=(self.width / 2, self.height / 8))
                self.screen.blit(mensagem, mensagem_rect)
                if self.pontuacao[0] == 2 and self.pontuacao[1] == 2:
                    self.screen.blit(self.background, (0, 0))
                    self.draw_grid(self.width, self.height, self.grid_size, (17, 41, 173))
                    fonte = pygame.font.SysFont(None, 60)
                    mensagem = fonte.render(f"Foi um empate",
                                            True, ((255, 255, 255)))
                    mensagem_rect = mensagem.get_rect(center=(self.width / 2, self.height / 2))
                    self.screen.blit(mensagem, mensagem_rect)
                    self.tabela_pontuacao()
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.game_over = False
                            end = True
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            self.game_over = False
                            end = True
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            self.cs.exec_stop_client()
                            return
                else:
                    for i in self.pontuacao:
                        if self.pontuacao[i] == 2:
                            self.screen.blit(self.background, (0, 0))
                            self.draw_grid(self.width, self.height, self.grid_size, (17, 41, 173))
                            fonte = pygame.font.SysFont(None, 60)
                            mensagem = fonte.render(f"O jogador {i + 1} foi vencedor",
                                                    True, ((255, 255, 255)))
                            mensagem_rect = mensagem.get_rect(center=(self.width / 2, self.height / 2))
                            self.screen.blit(mensagem, mensagem_rect)
                            self.tabela_pontuacao()
                            pygame.display.update()
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    self.game_over = False
                                    end = True
                                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                    self.game_over = False
                                    end = True
                                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                    self.cs.exec_stop_client()
                                    return
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game_over = False
                        end = True
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.game_over = False
                        end = True
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.screen.blit(self.background, (0, 0))
                        self.draw_grid(self.width, self.height, self.grid_size, (17, 41, 173))
                        fonte = pygame.font.SysFont(None, 60)
                        mensagem = fonte.render("Espere o outro jogador reiniciar.",
                                                True, ((255, 255, 255)))
                        mensagem_rect = mensagem.get_rect(center=(self.width / 2, self.height / 2))
                        self.screen.blit(mensagem, mensagem_rect)
                        self.tabela_pontuacao()
                        pygame.display.update()
                        self.cs.exec_reset_gamemech()
                        self.cs.ready_player()
                        self.cs.execute_start_game()
                        self.players.empty()
                        self.game_over = False
                        self.tabela_pontuacao()
                        self.create_players(self.grid_size)
                        self.cs.ready_player()
                        self.cs.execute_start_game()
                        return self.run()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    end = True
                    pygame.quit()
                    return

            for i in self.players:
                if i.get_id() == self.id:
                    i.update(self)
            self.cs.ready_player()
            self.cs.execute_start_game()
            lst = self.cs.check_game_over()
            if True in lst:
                self.game_over = True
                for index, b in enumerate(lst):
                    if b:
                        self.pontuacao[not index] += 1
            self.update_world()
            pygame.display.update()
            rects = self.players.draw(self.screen)
            rastro_verde = self.rastro_verde.draw(self.screen)
            rastro_laranja = self.rastro_laranja.draw(self.screen)
            self.draw_grid(self.width, self.height, self.grid_size, (17, 41, 173))
            self.tabela_pontuacao()

            # We call update to pygame display
            pygame.display.update(rects)
            pygame.display.update(rastro_verde)
            pygame.display.update(rastro_laranja)

            # Why do we clear screen and background?
            self.players.clear(self.screen, self.background)
            self.rastro_verde.clear(self.screen, self.background)
            self.rastro_laranja.clear(self.screen, self.background)

        pygame.display.update()
        return

    def sair(self):
        self.cs.exec_stop_server()

    # Press the green button in the gutter to run the script.


def get_font(size):     # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
