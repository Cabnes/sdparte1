import pygame


# Player is part of the test example 4
# It defines a sprite
class Rastro(pygame.sprite.DirtySprite):

    def __init__(self, pos_x: int, pos_y: int, size: int, imagem: str, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(imagem)
        #initial_size = self.image.get_size()
        #size_rate = size / initial_size[0]
        #self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, (size, size))
        self.pos = (pos_x * size, pos_y * size)
        self.rect = pygame.rect.Rect(self.pos, self.image.get_size())

    def kill(self) -> None:
        super().kill()

    def get_pos(self):
        return self.pos