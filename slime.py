"""Class Slime du jeu Redem en python."""

import pygame
import sounds
import animation

#classe du slime
class Slime(animation.AnimateSprite):

    def __init__(self, x, y, size = (200, 200), largeur = 5):
        super().__init__("iOOF6t-", size)
        self.image = pygame.image.load("Assets/slime.png")
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.sound_manager = sounds.SoundManager()
        # self.image.set_colorkey([0, 0, 0])
        self.position = [x, y]
        self.speed = 3.5
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, self.rect.height * 0.5)
        self.old_position = self.position.copy()
        self.speed = 1
        self.mort = 5

    # Définition de l'ancienne position du slime
    def save_location(self): self.old_position = self.position.copy()

    # Définition de tomber
    def move_down(self): self.position[1] += self.mort

    # Définition du mouvement de droite
    def move_right(self): self.position[0] += self.speed

    # Définition du mouvement de gauche
    def move_left(self): self.position[0] -= self.speed

    # Définition de la maj
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    # Définition du retour arrière
    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


