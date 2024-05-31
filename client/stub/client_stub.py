from client import stub as client
from middleware.sockets import Socket


class ClientStub:
    def __init__(self, host, port) -> None:
        self._host = host
        self._port = port
        self.socket = Socket.create_client_connection(self._host, self._port)


    # Operação de adição: envia sinal que vai adicionar, envia inteiros, espera resultado
    def get_nr_quad_x(self) -> int:
        self.socket.send_str(client.QUADX_OP) #estou informando o servidor que vou enviar uma mensagem quadx_op
        print("sending")
        return self.socket.receive_int(client.INT_SIZE)

    def get_nr_quad_y(self) -> int:
        self.socket.send_str(client.QUADY_OP)  # estou informando o servidor que vou enviar uma mensagem quadx_op
        return self.socket.receive_int(client.INT_SIZE)

    def get_new_pos(self, nr_player, direction):
        self.socket.send_str(client.CHECK_PATH_OP)
        self.socket.send_int(nr_player, client.INT_SIZE)
        self.socket.send_int(direction, client.INT_SIZE)
        return self.socket.receive_obj(client.INT_SIZE)


# ESTA FUNÇÃO É PARA O PROTOCOLO PLAYER, FOR SETTING PLAYER AND RECEIVING ID
    def set_player(self, name:str) -> tuple:
        self.socket.send_str(client.PLAYER_OP)
        self.socket.send_str(name)
        return self.socket.receive_obj(client.INT_SIZE)

    def get_world(self):
        self.socket.send_str(client.GET_WORLD_OP)
        return self.socket.receive_obj(client.INT_SIZE)

    def exec_stop_client(self):
        self.socket.send_str(client.BYE_OP)
        self.socket.close()

    def exec_stop_server(self):
        self.socket.send_str(client.STOP_SERVER_OP)
        self.socket.close()

    def ready_player(self):
        self.socket.send_str(client.READY_PLAYER)

    def execute_start_game(self) -> int:
        self.socket.send_str(client.START_GAME)
        return self.socket.receive_int(client.INT_SIZE)

    def exec_reset_gamemech(self):
        self.socket.send_str(client.RESET_GAMEMECH)

    def check_game_over(self):
        self.socket.send_str(client.CHECK_GAME_OVER)
        return self.socket.receive_obj(client.INT_SIZE)

    def game_over(self, nr_player):
        self.socket.send_str(client.GAME_OVER)
        self.socket.send_int(nr_player, client.INT_SIZE)

