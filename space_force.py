import pygame
from random import randint, choice
import random
from sys import exit
import time
import math

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
    global meteoros_info
    global max_meteoros

    if len(meteoros_info) < max_meteoros:
        img_meteoro = random.choice(meteoros)
        posicao = (randint(950, 990), randint(20, 480))
        velocidade_meteoros = randint(1, 3)
        meteoros_info.append({'posicao': posicao, 'velocidade': -velocidade_meteoros, 'imagem': img_meteoro})

def movimento_meteoros():
    global meteoros_info
    global coracao

    # Percorra a lista de meteoros_info
    for meteoro_info in meteoros_info:
        meteoro_info['posicao'] = (meteoro_info['posicao'][0] + meteoro_info['velocidade'], meteoro_info['posicao'][1])

        # Remova o meteoro quando ele estiver fora da tela à esquerda
        if meteoro_info['posicao'][0] < -70:
            meteoros_info.remove(meteoro_info)

        # Verifique a colisão entre a nave e o meteoro
        if nave_rect.colliderect(pygame.Rect(meteoro_info['posicao'], meteoro_info['imagem'].get_size())):
            coracao -= 1  # Remova uma vida quando houver colisão
            meteoros_info.remove(meteoro_info)

    # Desenhe os meteoros na tela
    for meteoro_info in meteoros_info:
        tela.blit(meteoro_info['imagem'], meteoro_info['posicao'])

    pygame.display.update()

def adicionar_coracoes():
    global coracoes_info, max_coracoes

    if len(coracoes_info) < max_coracoes:
        img_coracao = pygame.image.load('Objects/Coracao/Heart1.png').convert_alpha()

        tamanho_novo = (60, 60)  # Tamanho desejado
        img_coracao = pygame.transform.scale(img_coracao, tamanho_novo)

        posicao = (randint(950, 990), randint(20, 480))
        velocidade_coracao = randint(1, 2)
        coracoes_info.append({'posicao': posicao, 'velocidade': -velocidade_coracao, 'imagem': img_coracao})

def movimento_coracoes():
    global coracoes_info, coracao

    coracoes_coletados = []

    for coracao_info in coracoes_info:
        tela.blit(coracao_info['imagem'], coracao_info['posicao'])
        coracao_info['posicao'] = (coracao_info['posicao'][0] + coracao_info['velocidade'], coracao_info['posicao'][1])

        if coracao_info['posicao'][0] < -70:
            coracoes_coletados.append(coracao_info)

        if nave_rect.colliderect(pygame.Rect(coracao_info['posicao'], coracao_info['imagem'].get_size())):
            coracoes_coletados.append(coracao_info)

    for coracao_info in coracoes_coletados:
        coracoes_info.remove(coracao_info)
        coracao += 1

def mostra_textos():
    global coracao

    texto_coracoes = fonte_pixel.render(f"{coracao}", True, '#FFFFFF')

    logo_coracao = pygame.transform.scale(coracao_superficies[0], (40, 40))

    tela.blit(texto_coracoes, (908, 28))
    tela.blit(logo_coracao, (865, 22))

pygame.init()

coracao = 3

# Tamanho da tela
tamanho = (960, 540)
tela = pygame.display.set_mode(tamanho)

# Título da janela
pygame.display.set_caption("ChuvaMortal")

# Cria um relógio para controlar os FPS
relogio = pygame.time.Clock()

# Carrega a fonte
fonte_pixel = pygame.font.Font('Objects/Font/space age.ttf', 30) 

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
meteoros = []
velocidade = []
meteoros_rect = []
meteoros_info = []
max_meteoros = 7

for imagem in range (1,11):
    img = pygame.image.load(f'Objects/Items/Meteors/Meteor_{imagem}.png').convert_alpha()
    img = pygame.transform.scale(img, (60, 60))
    meteoros.append(img)
    print(f'Objects/Items/Meteors/Meteor_{imagem}.png')

movimento_y_nave = 0
movimento_x_nave = 0

### Coração
coracao_superficies = []
coracao_index = 0
coracoes_info = []
max_coracoes = 1

for imagem in range(1, 4):
    img = pygame.image.load(f'Objects/Coracao/Heart{imagem}.png').convert_alpha()
    img = pygame.transform.scale(img, (40, 40))
    coracao_superficies.append(img)

# Cria um evento para adicionar um objeto na tela
novo_objeto_timer = pygame.USEREVENT + 1 # userevento = 0 é reservado, por isso começa com 1.
pygame.time.set_timer(novo_objeto_timer, 500) # cronômetro: a cada 500ms dispara o novo_objeto_timer

novo_coracao_timer = pygame.USEREVENT + 2
pygame.time.set_timer(novo_coracao_timer, 5000)  # A cada 5 segundos dispara o evento

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
    mostra_textos()

    adicionar_coracoes()
    movimento_coracoes()

    adicionar_meteoros()
    movimento_meteoros()
    

    # Atualiza a tela com o conteúdo
    pygame.display.update()

    # Define a quantidade de frames por segundo
    relogio.tick(60)