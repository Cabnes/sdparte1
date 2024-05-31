import pygame
from client.stub.client_stub import ClientStub
from client.stub import SQUARE_SIZE, PORT, SERVER_ADDRESS
from game import Game

def main():
    pygame.init()
    # PRIMEIRA ALTERACAO: Queremos definir o número células no mundo
    cs = ClientStub(SERVER_ADDRESS, PORT)
    gm = Game(cs, SQUARE_SIZE)
    gm.main_menu()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
