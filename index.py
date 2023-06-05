import random
import pygame

pygame.init()

x = 1280
y = 720

screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("SpaceDead")

bg = pygame.image.load("image/Fundo.jpg").convert_alpha()
bg = pygame.transform.scale(bg, (x, y))

alien = pygame.image.load("image/alien.png").convert_alpha()
alien = pygame.transform.scale(alien, (50, 50))

playerImg = pygame.image.load("image/nave.png").convert_alpha()
playerImg = pygame.transform.scale(playerImg, (50, 50))
playerImg = pygame.transform.rotate(playerImg, -90)

missil = pygame.image.load("image/missil.png").convert_alpha()
missil = pygame.transform.scale(missil,(25,25))
missil = pygame.transform.rotate(missil, -45)

pos_alien_x = 500
pos_alien_y = 360

pos_player_x = 200
pos_player_y = 300

vel_x_missil = 0
pos_x_missil = 200
pos_y_missil = 300

triggered = False

rodando = True

player_rect = playerImg.get_rect()
alien_rect = alien.get_rect()
missil_rect = missil.get_rect()

pontos = 4

font = pygame.font.SysFont("fonts/Gloock-Regular.ttf", 50)

# Funções

def respawn():
    x = 1350
    y = random.randint(1,640)
    return [x,y]

def respawn_missil():
    triggered = False
    respawn_missil_x = pos_player_x
    respawn_missil_y = pos_player_y
    vel_x_missil = 0
    return [respawn_missil_x, respawn_missil_y, triggered, vel_x_missil]

def colisions():
    global pontos
    if player_rect.colliderect(alien_rect) or alien_rect.x == 60:
        pontos -=1
        return True
    elif missil_rect.colliderect(alien_rect):
        pontos +=1
        return True
    else:
        return False
    

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    screen.blit(bg, (0, 0))

    rel_x = x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    if rel_x < 1280:
        screen.blit(bg, (rel_x, 0))

    # teclas
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and pos_player_y > 1:
        pos_player_y -= 1
        
        if not triggered:
            pos_y_missil -=1

    if tecla[pygame.K_DOWN] and pos_player_y < 665:
        pos_player_y += 1

        if not triggered:
            pos_y_missil += 1

    if tecla[pygame.K_SPACE]:
        triggered = True
        vel_x_missil = 2
    
    if pontos == 0:
        rodando = False

    # respawn
    if pos_alien_x == 50:
        pos_alien_x, pos_alien_y = respawn()

    if pos_x_missil == 1300:
        pos_x_missil, pos_y_missil, triggered, vel_x_missil = respawn_missil()

    if pos_alien_x == 50 or colisions():
        pos_alien_x = respawn()[0]
        pos_alien_y = respawn()[1]
    # Posições do Rect

    player_rect.x = pos_player_x
    player_rect.y = pos_player_y

    missil_rect.x = pos_x_missil
    missil_rect.y = pos_y_missil

    alien_rect.x = pos_alien_x
    alien_rect.y = pos_alien_y

    # movimento
    x -= 2
    pos_alien_x -= 1
    pos_x_missil += vel_x_missil

    pygame.draw.rect(screen,(255,0,0), player_rect, 4)
    pygame.draw.rect(screen,(255,0,0), missil_rect, 4)
    pygame.draw.rect(screen,(255,0,0), alien_rect, 4)

    score = font.render(f"Pontos: {int(pontos)}",True,(0,0,0))
    screen.blit(score,(50,50))

    # Criar imagens
    screen.blit(alien, (pos_alien_x, pos_alien_y))
    screen.blit(missil,(pos_x_missil,pos_y_missil))
    screen.blit(playerImg, (pos_player_x, pos_player_y))

    print(pontos)

    pygame.display.update()
