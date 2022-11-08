"""Class Game du jeu Redem en python."""

import pygame
import pytmx
import pyscroll
import animation
from player import Player
from slime import Slime
from boss import Boss
from sounds import SoundManager

#Classe du jeu qui est le coeur principal du programme
class Game:

    def __init__(self):
        #créer la fenêtre du jeu
        self.screen = pygame.display.set_mode((1920, 1080))
        #nom de la fenêtre
        pygame.display.set_caption("Redem")
        #icône de la fenêtre
        icon = pygame.image.load("Assets/Icon/Icon2.png").convert_alpha()
        pygame.display.set_icon(icon)
        #charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame("Assets/TMX/maps/cle_bon.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        #zoom de la carte
        map_layer.zoom = 2

        self.sound_manager = SoundManager()
        #prendre l'information du point player sur Tiled avec le fichier .tmx
        player_position = tmx_data.get_object_by_name("player")
        #générer le joueur et le slime
        self.player = Player(player_position.x, player_position.y, (105, 98))
        self.all_players = pygame.sprite.Group()
        self.all_players.add(self.player)
        slime_position = tmx_data.get_object_by_name("slime")
        self.slime = Slime(slime_position.x, slime_position.y, (60, 60))
        self.all_players.add(self.slime)
        #Définir une liste qui va stocker les rectangles de collision sol
        self.walls = []
        #Définir une liste qui va stocker les rectangles de collision mur de droit
        self.mur = []
        #Définir une liste qui va stocker les rectangles de collision mur de gauche
        self.g = []

        #Boucles qui remplissent les listes citées
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        for mur in tmx_data.objects:
            if mur.type == "mur":
                self.mur.append(pygame.Rect(mur.x, mur.y, mur.width, mur.height))
        for g in tmx_data.objects:
            if g.type == "g":
                self.g.append(pygame.Rect(g.x, g.y, g.width, g.height))

        #générer les mobs
        #dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)
        self.group.add(self.slime)
        #dictionnaire pour les touches entrées par le joueur
        self.pressed = {}

        # prendre l'information du point grotte sur Tiled avec le fichier .tmx
        grotte = tmx_data.get_object_by_name("grotte")
        # prendre l'information du point m1 sur Tiled avec le fichier .tmx
        mort = tmx_data.get_object_by_name("m1")
        #prendre la position du point m1
        self.mort_rect = pygame.Rect(mort.x, mort.y, mort.width, mort.height)
        mort2 = tmx_data.get_object_by_name("m2")
        self.mort2_rect = pygame.Rect(mort2.x, mort2.y, mort2.width, mort2.height)
        mort3 = tmx_data.get_object_by_name("m3")
        self.mort3_rect = pygame.Rect(mort3.x, mort3.y, mort3.width, mort3.height)
        self.grotte_rect = pygame.Rect(grotte.x, grotte.y, grotte.width, grotte.height)
        #nom de la carte actuelle
        self.map = 'world'

    #Définition de switch grotte qui permet de rentrer dans la grotte
    def switch_grotte(self):
        # charger la carte (tmx) ici la grotte
        tmx_data = pytmx.util_pygame.load_pygame("Assets/TMX/maps/suite.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        # zoom de la carte
        map_layer.zoom = 2

        # prendre l'information du point spawn sur Tiled avec le fichier .tmx
        spawn_world_point = tmx_data.get_object_by_name("spawn")
        #générer un joueur et le boss
        self.player = Player(spawn_world_point.x, spawn_world_point.y, (105, 98))
        boss_position = tmx_data.get_object_by_name("boss")
        self.boss = Boss(boss_position.x, boss_position.y, (250, 250))
        self.all_players.add(self.boss)
        # Définir une liste qui va stocker les rectangles de collision sol
        self.walls = []
        # Définir une liste qui va stocker les rectangles de collision mur de droit
        self.mur = []
        # Définir une liste qui va stocker les rectangles de collision mur de gauche
        self.g =[]

        # Boucles qui remplissent les listes citées
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        for mur in tmx_data.objects:
            if mur.type == "mur":
                self.mur.append(pygame.Rect(mur.x, mur.y, mur.width, mur.height))
        for g in tmx_data.objects:
            if g.type == "g":
                self.g.append(pygame.Rect(g.x, g.y, g.width, g.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)
        self.group.add(self.boss)
        # dictionnaire pour les touches entrées par le joueur
        self.pressed = {}

        # prendre l'information du point exit_grotte sur Tiled avec le fichier .tmx
        world = tmx_data.get_object_by_name("exit_grotte")
        # prendre la position du point exit_grotte
        self.world_rect = pygame.Rect(world.x, world.y, world.width, world.height)
        mort = tmx_data.get_object_by_name("m1")
        self.mort_rect = pygame.Rect(mort.x, mort.y, mort.width, mort.height)
        mort2 = tmx_data.get_object_by_name("m2")
        self.mort2_rect = pygame.Rect(mort2.x, mort2.y, mort2.width, mort2.height)
        mort3 = tmx_data.get_object_by_name("m3")
        self.mort3_rect = pygame.Rect(mort3.x, mort3.y, mort3.width, mort3.height)

    #Définition de switch world qui permet de sortir de la grotte
    def switch_world(self):
        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame("Assets/TMX/maps/cle_bon.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        # zoom de la carte
        map_layer.zoom = 2

        # Définir une liste qui va stocker les rectangles de collision sol
        self.walls = []
        # Définir une liste qui va stocker les rectangles de collision mur de droit
        self.mur = []
        # Définir une liste qui va stocker les rectangles de collision mur de gauche
        self.g = []

        # Boucles qui remplissent les listes citées
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        for mur in tmx_data.objects:
            if mur.type == "mur":
                self.mur.append(pygame.Rect(mur.x, mur.y, mur.width, mur.height))
        for g in tmx_data.objects:
            if g.type == "g":
                self.g.append(pygame.Rect(g.x, g.y, g.width, g.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)
        # dictionnaire pour les touches entrées par le joueur
        self.pressed = {}

        # prendre l'information du point grotte sur Tiled avec le fichier .tmx
        grotte = tmx_data.get_object_by_name("grotte")
        # prendre la position du point grotte
        self.grotte_rect = pygame.Rect(grotte.x, grotte.y, grotte.width, grotte.height)
        spawn_grotte_point = tmx_data.get_object_by_name("sortie")
        self.player.position[0] = spawn_grotte_point.x
        self.player.position[1] = spawn_grotte_point.y

    #Définir de switch mort qui permet de retourner au début pour simuler une mort
    def switch_mort(self):
        # charger la carte (tmx)
        tmx_data = pytmx.util_pygame.load_pygame("Assets/TMX/maps/cle_bon.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        # zoom de la carte
        map_layer.zoom = 2

        # prendre l'information du point player sur Tiled avec le fichier .tmx
        spawn_mort_point = tmx_data.get_object_by_name("player")
        # générer un joueur et le slime
        self.player = Player(spawn_mort_point.x, spawn_mort_point.y, (105, 98))
        slime_position = tmx_data.get_object_by_name("slime")
        self.slime = Slime(slime_position.x, slime_position.y, (60, 60))
        self.all_players.add(self.slime)
        # Définir une liste qui va stocker les rectangles de collision sol
        self.walls = []
        # Définir une liste qui va stocker les rectangles de collision mur de droit
        self.mur = []
        # Définir une liste qui va stocker les rectangles de collision mur de gauche
        self.g = []

        # Boucles qui remplissent les listes citées
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        for mur in tmx_data.objects:
            if mur.type == "mur":
                self.mur.append(pygame.Rect(mur.x, mur.y, mur.width, mur.height))
        for g in tmx_data.objects:
            if g.type == "g":
                self.g.append(pygame.Rect(g.x, g.y, g.width, g.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)
        self.group.add(self.slime)
        # dictionnaire pour les touches entrées par le joueur
        self.pressed = {}

        # prendre l'information du point m1 sur Tiled avec le fichier .tmx
        mort = tmx_data.get_object_by_name("m1")
        # prendre la position du point m1
        self.mort_rect = pygame.Rect(mort.x, mort.y, mort.width, mort.height)
        mort2 = tmx_data.get_object_by_name("m2")
        self.mort2_rect = pygame.Rect(mort2.x, mort2.y, mort2.width, mort2.height)
        mort3 = tmx_data.get_object_by_name("m3")
        self.mort3_rect = pygame.Rect(mort3.x, mort3.y, mort3.width, mort3.height)
        grotte = tmx_data.get_object_by_name("grotte")
        self.grotte_rect = pygame.Rect(grotte.x, grotte.y, grotte.width, grotte.height)

    #Définition qui met à jour le jeu tout le temps
    def update(self):
        self.group.update()
        update = False
        #vérification collision switch grotte pour rentrer dans la grotte
        if self.map == 'world' and self.player.feet.colliderect(self.grotte_rect):
            self.switch_grotte()
            self.map = 'grotte'

        #vérification collision switch world pour sortir de la grotte
        if self.map == 'grotte' and self.player.feet.colliderect(self.world_rect):
            self.switch_world()
            self.map = 'world'

        #vérification collision switch mort pour simuler une mort retour au début
        if self.player.feet.colliderect(self.mort_rect):
            self.switch_mort()
            self.map='world'

        #vérification collision switch mort pour simuler une mort retour au début
        if self.player.feet.colliderect(self.mort2_rect):
            self.switch_mort()
            self.map='world'

        #vérification collision switch mort pour simuler une mort retour au début
        if self.player.feet.colliderect(self.mort3_rect):
            self.switch_mort()
            self.map='world'

        #vérification collision sol
        if self.player.feet.collidelist(self.walls) > -1:
            self.player.move_back()
            update = True
        return update

    #Définition vérification collision sol du Slime
    def slime_collision(self):
        update = False
        if self.slime.feet.collidelist(self.walls) > -1:
            self.slime.move_back()
            update = True
        return update


    def slime_mur(self):
        update = False
        # vérification collision mur de droite
        if self.slime.feet.collidelist(self.mur) > -1:
            self.slime.move_back()
            update = True
        return update

    def slime_g(self):
        update = False
        # vérification collision mur de gauche
        if self.slime.feet.collidelist(self.g) > -1:
            self.slime.move_back()
            update = True
        return update

    #Définition vérification collision sol du Boss
    def boss_collision(self):
        update = False
        if self.boss.feet.collidelist(self.walls) > -1:
            self.boss.move_back()
            update = True
        return update

    def boss_mur(self):
        update = False
        # vérification collision mur de droite
        if self.boss.feet.collidelist(self.mur) > -1:
            self.boss.move_back()
            update = True
        return update

    def boss_g(self):
        update = False
        # vérification collision mur de gauche
        if self.boss.feet.collidelist(self.g) > -1:
            self.boss.move_back()
            update = True
        return update


    #Défintion de la màj pour vérifier une collision du mur de droite
    def update_mur(self):
        self.group.update()
        update = False
        #vérification collision mur de droite
        if self.player.feet.collidelist(self.mur) > -1:
                self.player.move_back()
                update = True
        return update

    # Défintion de la màj pour vérifier une collision du mur de gauche
    def update_g(self):
        self.group.update()
        update = False
        # vérification collision mur de gauche
        if self.player.feet.collidelist(self.g) > -1:
            self.player.move_back()
            update = True
        return update

    #Définition des commandes du joueur
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        jump = False
        grav = True

        #Définir le déplacement à gauche
        if pressed[pygame.K_q] and self.update_g() is False:
            self.player.move_left()

        #Définir le déplacement à droite
        elif pressed[pygame.K_d] and self.update_mur() is False:
            self.player.move_right()

        #Définir le jump du personnage
        if jump is False and pressed[pygame.K_SPACE] and self.update() is True:
            jump = True
            grav = False
        if jump is True:
            y = 0
            while jump is True:
                y -= self.player.jump
                self.player.jump -= 5
                if self.player.jump < -30:
                    jump = False
                    grav = True
                    self.player.jump = -5
                pygame.time.delay(5)
                pygame.display.update()
                self.player.move_jump()

        #Définir la gravité pour que le personnage, le slime et le boss retombent
        if grav is True and self.update() is False:
            pygame.time.delay(5)
            pygame.display.update()
            self.player.move_down()

        if grav is True and self.slime_collision() is False:
            pygame.time.delay(5)
            pygame.display.update()
            self.slime.move_down()

        if self.map == "grotte":
            if grav is True and self.boss_collision() is False:
                pygame.time.delay(5)
                pygame.display.update()
                self.boss.move_down()

        #Aggro du slime sur le joueur
        if self.slime.position[0] - self.player.position[0] < 200 and self.slime.position[0] - self.player.position[0] > 0 and self.slime_g() is False:
            self.slime.move_left()

        #Aggro du boss sur le joueur
        if self.map == "grotte":
            if self.boss.position[0] - self.player.position[0] < 500 and self.boss.position[0] - self.player.position[0] > 0 and self.boss_g() is False:
                self.boss.move_left()


        #Définir le lancé de projectile (flèche)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                print("Fermeture du jeu")

            elif event.type == pygame.KEYDOWN:
                self.pressed[event.key] = True
                #Projectile pas fini
                if event.key == pygame.K_a:
                    self.player.launch_projectile()




    #définition de la boucle du jeu
    def run(self):
        #Fixer le nombre de fps
        clock = pygame.time.Clock()
        running = True
        #Mettre la musique du jeu
        self.sound_manager.boucle('music')

        #Boucle du jeu
        while running:
            self.player.save_location()
            self.update()
            self.handle_input()
            self.update_mur()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            #commande pour mettre 60 images par seconde
            clock.tick(60)

        #Fin du jeu
        pygame.quit()