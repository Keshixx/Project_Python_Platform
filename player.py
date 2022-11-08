"""Class Player du jeu Redem en python."""

import pygame
from projectile import Projectile
import animation
from sounds import SoundManager

#classe du personnage que l'on incarne dans le jeu
class Player(animation.AnimateSprite):

    def __init__(self, x, y, size = (200, 200)):
        super().__init__('Ggdqc3-', (150, 111))
        self.image = pygame.image.load("Assets/plat.png")
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.sound_manager = SoundManager()
        #self.image.set_colorkey([0, 0, 0])
        self.position = [x, y]
        self.speed = 3.5
        self.feet = pygame.Rect(0, 0, self.rect.width*0.5, self.rect.height*0.5)
        self.old_position = self.position.copy()
        self.speed = 3
        self.jump = -5
        self.mort = 5
        self.all_projectiles = pygame.sprite.Group()

    #Définition de l'ancienne position du personnage
    def save_location(self): self.old_position = self.position.copy()

    #Définition du saut
    def move_jump(self): self.position[1] += self.jump

    #Définition de tomber
    def move_down(self): self.position[1] += self.mort

    #Définition du mouvement de droite
    def move_right(self): self.position[0] += self.speed

    #Définition du mouvement de gauche
    def move_left(self): self.position[0] -= self.speed

    #Définition de la maj
    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    #Définition du retour arrière
    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    #Définition pour que le personnage soit animé mais pas fini à cause des collisions
    def update_animation(self):
        self.animate(0.4)

    #Définition pour afficher la barre de pv mais idem
    def update_health_bar(self, surface):
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 30, self.rect.y + 10, self.max_health, 7])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 30, self.rect.y + 10, self.health, 7])

    #Définition pour lancer un projectile mais idem
    def launch_projectile(self):
        self.start_animation()
        self.update_animation()
        self.sound_manager.play('arc')
        self.all_projectiles.add(Projectile(self))