"""
Projet jeu graphique en poo avec Pygame et Tiled se nommant Redem créé par Kevin Espiguinha et Thibaut Bise en 2021.
Jeu de plateforme et troll, attention aux pièges !
Jeu dans lequel où l'on incarne le personnage Redem qui s'aventure dans un territoire dangereux.
N'oubliez pas d'installer pygame (pip install pygame), pytmx (pip install pytmx), pyscroll (pip install pyscroll).
Mettre ces commandes entre parenthèses dans le terminal pour faire fonctionner le jeu.
Veuillez installer Tiled pour ouvrir les fichiers .tmx
Le jeu n'est pas définitivement terminé à cause de plusieurs problèmes rencontrés (collisions, pyscroll).
Mais fonctionne très bien avec une bonne base.
Script Python
Fichiers : main.py, game.py, player.py, animations.py, projectile.py, sounds.py, slime.py, boss.py
"""

import pygame
from game import Game

#Lancement du jeu avec la classe Game()
if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()

