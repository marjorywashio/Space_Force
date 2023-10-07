import pygame
from random import randint, choice
import random
from sys import exit

def animacao_nave():

    global normal_flight
    global normal_flight_index

    if nave_rect.right >= 960:
        nave_rect.right = 960
    elif nave_rect.left <= 30:
        nave_rect.left = 30

    if nave_rect.top <= 0:
        nave_rect.top = 0
    elif nave_rect.bottom >= 540:
        nave_rect.bottom = 540

    nave_rect.y += movimento_y_nave
    nave_rect.x += movimento_x_nave

    normal_flight_rect.y += movimento_y_nave
    normal_flight_rect.x += movimento_x_nave

    if normal_flight_rect.right >= 857:
        normal_flight_rect.right = 857
    elif normal_flight_rect.left <= -10:
        normal_flight_rect.left = -10

    if normal_flight_rect.top <= 30:
        normal_flight_rect.top = 30
    elif normal_flight_rect.bottom >= 510:
        normal_flight_rect.bottom = 510

    tela.blit(nave, nave_rect)
    tela.blit(normal_flight[int(normal_flight_index)], (normal_flight_rect))

    normal_flight_index += 0.2
    if normal_flight_index > len(normal_flight):
        normal_flight_index = 0

def adicionar_meteoros():
    global meteoros
    global velocidade
    global meteoros_rect

    posicao = (randint(960, 1000), randint(-100, 0))
    velocidade_meteoros = randint(5, 7)

    meteoro = pygame.Surface((30, 30))
   # meteoros_rect = meteoros.get_rect(center=posicao)
    meteoros.append(meteoro)
    velocidade.append(velocidade_meteoros)
    meteoros_rect.append(meteoros_rect)

def movimento_meteoros():
    global meteoros
    global meteoros_rect
    global velocidade

    for i in range(len(meteoros)):
        meteoros_rect[i].x -= velocidade[i]

    for i in range(len(meteoros)):
        tela.blit(meteoros[i], meteoros_rect[i])

    tela.blit(meteoros[meteoro_index], meteoros_rect)

pygame.init()

# Tamanho da tela
tamanho = (960, 540)
tela = pygame.display.set_mode(tamanho)

# Título da janela
pygame.display.set_caption("ChuvaMortal")

# Cria um relógio para controlar os FPS
relogio = pygame.time.Clock()

# Carrega a fonte
fonte_pixel = pygame.font.Font('Objects/Font/space age.ttf', 50) 

# Carrega os planos de fundo
fundo_escuro = pygame.image.load('Objects/Clouds/1.png').convert_alpha()
lua = pygame.image.load('Objects/Clouds/2.png').convert_alpha()
nuvem1 = pygame.image.load('Objects/Clouds/3.png').convert_alpha()
nuvem2 = pygame.image.load('Objects/Clouds/4.png').convert_alpha()

# Transforma o tamanho da imagem de fundo
fundo_escuro = pygame.transform.scale(fundo_escuro, tamanho)
lua = pygame.transform.scale(lua, tamanho)
nuvem1 = pygame.transform.scale(nuvem1, tamanho)
nuvem2 = pygame.transform.scale(nuvem2, tamanho)

# Carrega a nave
nave = pygame.image.load('Objects/Spaceships/PNG_Parts&Spriter_Animation/Ship6/Ship6.png').convert_alpha()
nave_rect = nave.get_rect(center = (100, 270))

# Carrega o fogo normal
normal_flight_index = 0
normal_flight = []

for imagem in range (1,5):
    img = pygame.image.load(f'Objects/Spaceships/PNG_Animations/Exhaust/Ship6/Normal_flight/normal{imagem}.png').convert_alpha()
    normal_flight.append(img)
normal_flight_rect = normal_flight[normal_flight_index].get_rect(center = (nave_rect.center))
normal_flight_rect.x -= 74

# Carrega os meteoros
meteoro_index = 0
meteoros = []
velocidade = []
meteoros_rect = []

for imagem in range (1,11):
    img = pygame.image.load(f'Objects/Items/Meteors/Meteor_{imagem}.png').convert_alpha()
    img = pygame.transform.scale(img, (70, 70))
    meteoros.append(img)

# Carrega os itens bônus
itens = []

item_escudo = pygame.image.load('Objects/Items/Bonus_Items/Armor_Bonus.png').convert_alpha()
item_dano = pygame.image.load('Objects/Items/Bonus_Items/Damage_Bonus.png').convert_alpha()
item_speed_enemy = pygame.image.load('Objects/Items/Bonus_Items/Enemy_Speed_Debuff.png').convert_alpha()
item_hero_speed = pygame.image.load('Objects/Items/Bonus_Items/Hero_Speed_Debuff.png').convert_alpha()
item_hp = pygame.image.load('Objects/Items/Bonus_Items/HP_Bonus.png').convert_alpha()

itens.append(item_escudo)
itens.append(item_dano)
itens.append(item_speed_enemy)
itens.append(item_hero_speed)
itens.append(item_hp)

movimento_y_nave = 0
movimento_x_nave = 0

# Cria um evento para adicionar um objeto na tela
novo_objeto_timer = pygame.USEREVENT + 1 # userevento = 0 é reservado, por isso começa com 1.
pygame.time.set_timer(novo_objeto_timer, 500) # cronômetro: a cada 500ms dispara o novo_objeto_timer

################################################################################
############################ LOOP PRINCIPAL DO JOGO ############################
################################################################################

jogo_ativo = True

while jogo_ativo:

    #EVENTOS: mostra todos os eventos que acontecem no jogo
    for evento in pygame.event.get():
        if(evento.type) == pygame.QUIT:
            pygame.quit()
            exit()

        if(evento.type) == pygame.KEYDOWN:
            if evento.key == pygame.K_DOWN:
                movimento_y_nave = 5
                direcao = 'cima'
            if evento.key == pygame.K_UP:
                movimento_y_nave = -5
                direcao = 'baixo'
            if evento.key == pygame.K_RIGHT:
                movimento_x_nave = 5
                direcao = 'direita'
            if evento.key == pygame.K_LEFT:
                movimento_x_nave = -5
                direcao = 'esquerda'
            if evento.key == pygame.K_ESCAPE:
                jogo_ativo = False

        if(evento.type) == pygame.KEYUP:
            movimento_x_nave = 0
            movimento_y_nave = 0
    
    # Desenha o fundo na tela
    tela.blit(fundo_escuro, (0, 0))
    tela.blit(lua, (0, 0))
    tela.blit(nuvem1, (0, 0))
    tela.blit(nuvem2, (0, 0))

    animacao_nave()

    adicionar_meteoros()

    movimento_meteoros()

    # Atualiza a tela com o conteúdo
    pygame.display.update()

    # Define a quantidade de frames por segundo
    relogio.tick(60)