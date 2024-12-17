import pygame, random

from ship import Ship
from obstacle import Obstacle
from obstacle import grid
from alien import Alien, MysteryShip
from laser import Lazer

class Game:
    def __init__(self, screen_width, screen_height, offset):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.ship_group = pygame.sprite.GroupSingle()
        self.ship_group.add(Ship(self.screen_width, self.screen_height, self.offset))
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()
        self.lives = 3
        self.run = True
        self.score = 0
        self.highscore = 0
        self.mystery_ship_boom = pygame.mixer.Sound("sounds/explosion.ogg")
        self.alien_boom = pygame.mixer.Sound("sounds/explosion.ogg")
        self.load_highscore()
        self.victory = False
        pygame.mixer.music.load("music/casinoforest.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def create_obstacles(self):
        obstacle_width = len(grid[0]) * 3
        gap = (self.screen_width + self.offset - (4 * obstacle_width)) / 5
        obstacles = []
        for i in range(4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 150)
            obstacles.append(obstacle)
        return obstacles

    def create_aliens(self):
        for row in range(7):
            for column in range(17):
                x = column * 55 + 200
                y = row * 55 + 100
                if row == 0:
                    alien_type = 3
                elif row in (1, 2):
                    alien_type = 2
                else:
                    alien_type = 1
                alien = Alien(alien_type, x + self.offset / 2, y)
                self.aliens_group.add(alien)

    def move_aliens(self):
        self.aliens_group.update(self.aliens_direction)

        alien_sprites = self.aliens_group.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width + self.offset / 2:
                self.aliens_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= self.offset / 2:
                self.aliens_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    def alien_shoot_laser(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprite = Lazer(random_alien.rect.center, -10, self.screen_height)
            self.alien_lasers_group.add(laser_sprite)

    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(self.screen_width, self.offset))

    def check_victory(self):
        if len(self.aliens_group) == 0:
            self.run = False
            return True
        return False

    def check_for_collisions(self):
        # Ship
        if self.ship_group.sprite.lasers_group:
            for laser_sprite in self.ship_group.sprite.lasers_group:
                aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True)
                if aliens_hit:
                    self.alien_boom.play()
                    for alien in aliens_hit:
                        self.score += alien.type * 100
                        self.check_for_highscore()
                        laser_sprite.kill()

                    if len(self.aliens_group) == 0:
                        self.game_over()


                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):
                    self.score += 500
                    self.mystery_ship_boom.play()
                    self.check_for_highscore()
                    laser_sprite.kill()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        #Alien Lasers
        if self.alien_lasers_group:
            for laser_sprite in self.alien_lasers_group:
                if pygame.sprite.spritecollide(laser_sprite, self.ship_group, False):
                    laser_sprite.kill()
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over()
                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        if self.aliens_group:
            for alien in self.aliens_group:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)

                if pygame.sprite.spritecollide(alien, self.ship_group, False):
                    self.game_over()

    def game_over(self):
        self.run = False
        if len(self.aliens_group) == 0:  # If no aliens left, it's a victory
            self.victory = True
        else:
            self.victory = False

    def reset(self):
        self.run = True
        self.victory = False  # Reset victory state
        self.lives = 3
        self.ship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.obstacles = self.create_obstacles()
        self.score = 0

    def check_for_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score

            with open("highscore.txt", "w") as file:
                file.write(str(self.highscore))

    def load_highscore(self):
        try:
            with open ("highscore.txt", "r") as file:
                self.highscore = int(file.read())
        except FileNotFoundError:
            self.highscore = 0

