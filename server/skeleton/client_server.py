from threading import Thread
from server.server_impl.gamemech import GameMech
import logging
import server.server_impl as server
from server_shared_state import ServerSharedState
import numpy as np
import ast

class ClientThread(Thread):
    def __init__(self, shared_state: ServerSharedState, current_connection, address):
        self.current_connection = current_connection
        self.shared_state = shared_state
        self.gamemech = self.shared_state.gamemech()
        self.address = address
        Thread.__init__(self)

    def process_update(self):
        pass

    def process_add_player(self):
        name = self.current_connection.receive_str(server.MAX_STR_SIZE)
        res: tuple = self.gamemech.add_player(name)
        self.current_connection.send_obj(res, server.INT_SIZE)

    def process_get_world(self):
        res = self.gamemech.get_world()
        self.current_connection.send_obj(res, server.INT_SIZE)

    def process_nr_x_quad_value(self):
        nr_x_quad = self.gamemech.get_nr_x()
        print(nr_x_quad)
        self.current_connection.send_int(nr_x_quad, server.INT_SIZE)

    def process_nr_y_quad_value(self):
        nr_y_quad = self.gamemech.get_nr_y()
        self.current_connection.send_int(nr_y_quad, server.INT_SIZE)

    def process_check_path_value(self):
        nr_player = self.current_connection.receive_int(server.INT_SIZE)
        direction = self.current_connection.receive_int(server.INT_SIZE)
        new_pos = self.gamemech.check_caminho(nr_player, direction)
        self.current_connection.send_obj(new_pos, server.INT_SIZE)

    def process_ready_player(self):
        self.shared_state.add_client()

    def process_start_game(self):
        # val: bool = False
        # while val == False:
        #    val = self.shared_state.start_game()
        self.shared_state.start_game_sem().acquire()
        self.shared_state.finished()
        if self.shared_state.get_finished() == 2:
            self.shared_state.reset()
        val = True
        self.current_connection.send_int(int(val), server.INT_SIZE)

    def process_game_over(self):
        nr_player = self.current_connection.receive_int(server.INT_SIZE)
        self.gamemech.player_game_over(nr_player)

    def check_game_over(self):
        game_over = self.gamemech.get_game_over()
        self.current_connection.send_obj(game_over, server.INT_SIZE)

    def reset_gamemech(self):
        self.gamemech.reset_gamemech()

    def dispatch_request(self) -> (bool, bool):
        """
        Calls process functions based on type of request.
        """
        request_type = self.current_connection.receive_str(server.COMMAND_SIZE)
        print(request_type)
        keep_running = True
        last_request = False
        if request_type == server.UPDATE_OP: ###############
            logging.info("Update operation requested " + str(self.address)) ###################
            self.process_update()

        elif request_type == server.QUADX_OP:
            logging.info("Ask for a number of x quad operation requested")
            self.process_nr_x_quad_value()

        elif request_type == server.QUADY_OP:
            logging.info("Ask for a number of y quad operation requested")
            self.process_nr_y_quad_value()
        elif request_type == server.PLAYER_OP:
            logging.info("Adding player "+str(self.address))
            self.process_add_player()
        elif request_type == server.CHECK_PATH_OP:
            logging.info("Moving player "+str(self.address))
            self.process_check_path_value()
        elif request_type == server.GET_WORLD_OP:
            logging.info("Getting players"+str(self.address))
            self.process_get_world()
        elif request_type == server.START_GAME:
            logging.info("Asking for starting the game:" + str(self.address))
            self.process_start_game()
        elif request_type == server.READY_PLAYER:
            logging.info("Player Ready:" + str(self.address))
            self.process_ready_player()
        elif request_type == server.GAME_OVER:
            logging.info("Player gamed over:" + str(self.address))
            self.process_game_over()
        elif request_type == server.CHECK_GAME_OVER:
            logging.info("Game Over:" + str(self.address))
            self.check_game_over()
        elif request_type == server.RESET_GAMEMECH:
            logging.info("Resetting Gamemech:" + str(self.address))
            self.reset_gamemech()
        elif request_type == server.BYE_OP:
            self.shared_state.finished()
            last_request = True
            print(self.shared_state.get_finished())
            if self.shared_state.get_finished() == 2:
                keep_running = False
        elif request_type == server.STOP_SERVER_OP:
            last_request = True
            keep_running = False
        return keep_running, last_request


    def run(self):
        # While client connected, wait for its demmands and dispatch the requests
        #with self.current_connection:
        last_request = False
        #If it is not the last request receive the request
        while not last_request:
            keep_running, last_request = self.dispatch_request()
        #If it is the last request, client is disconnecting...
        logging.debug("Client " + str(self.current_connection.get_address()) + " disconnected")

