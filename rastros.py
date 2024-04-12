import pygame
import rastro


class Rastros:
    def __init__(self):
        self.rastros: list[rastro.Rastro] = []

    def get_rastros(self):
        return self.rastros

    def adicionar_rastro(self, r: rastro.Rastro):
        self.rastros.append(r)

    def remover_rastro(self):
        if len(self.rastros) > 100:
            rastro = self.rastros.pop(0)
            rastro.kill()

