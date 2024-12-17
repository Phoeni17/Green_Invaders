import pygame, sys, random
from game import Game

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
OFFSET = 100
screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + OFFSET * 2))

grey = ((32,32,32))
yellow = ((238, 210, 2))

background = pygame.image.load("images/space.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + OFFSET * 2))
font = pygame.font.Font("fonts/monogram.ttf", 80)
level_surface = font.render("LEVEL 01", False, yellow)
game_over_surface = font.render("GAME OVER", False, yellow)
score_text_surface = font.render("SCORE", False, yellow)
highscore_text_surface = font.render("HIGHSCORE", False, yellow)
victory_surface = font.render("VICTORY!", False, yellow)

pygame.display.set_caption("Green Invaders")

clock = pygame.time.Clock()

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

shoot_laser = pygame.USEREVENT
pygame.time.set_timer(shoot_laser, 300)

MysteryShip = pygame.USEREVENT + 1
pygame.time.set_timer(MysteryShip, random.randint(8000, 16000))

while True:
    #check event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == shoot_laser and game.run:
            game.alien_shoot_laser()
        if event.type == MysteryShip and game.run:
            game.create_mystery_ship()
            pygame.time.set_timer(MysteryShip, random.randint(8000, 16000))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and game.run == False:
            game.reset()

    #updating
    if game.run:
        game.ship_group.update()
        game.move_aliens()
        game.alien_lasers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collisions()

    #Drawing
    screen.blit(background, (0, 0))

    #UI
    pygame.draw.rect(screen, yellow, (10, 10, 1280, 1180), 2, 0, 60, 60, 60, 60)
    pygame.draw.line(screen, yellow, (25, 1000), (1275, 1000), 3)

    if game.run:
        screen.blit(level_surface, (950, 1050, 50, 50))
    else:
        if game.victory:
            screen.blit(victory_surface, (950, 1050, 50, 50))
        else:
            screen.blit(game_over_surface, (950, 1050, 50, 50))

    x = 100
    for life in range(game.lives):
        screen.blit(game.ship_group.sprite.image, (x, 1050))
        x += 100

    screen.blit(score_text_surface, (525, 1050, 50, 50))
    formatted_score = str(game.score).zfill(5)
    score_surface = font.render(str(formatted_score), False, yellow)
    screen.blit(score_surface, (750, 1050, 50, 50))
    screen.blit(highscore_text_surface, (450, 1100, 50, 50))
    formatted_highscore = str(game.highscore).zfill(5)
    highscore_surface = font.render(str(formatted_highscore), False, yellow)
    screen.blit(highscore_surface, (750, 1100, 50 , 50))


    game.ship_group.draw(screen)
    game.ship_group.sprite.lasers_group.draw(screen)
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(screen)
    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.mystery_ship_group.draw(screen)

    pygame.display.update()
    clock.tick(60)
