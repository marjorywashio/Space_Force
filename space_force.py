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
        
        # Nasça fora da tela com coordenadas iniciais ajustadas
        posicao_x = 960  # Fora da tela à direita
        posicao_y = randint(-30, 570)  # Altura aleatória

        # Velocidades também podem ser aleatórias
        velocidade_x = randint(4, 6)  # Velocidade na direção horizontal (para a esquerda)
        velocidade_y = randint(-1, 3)  # Velocidade na direção vertical (para cima, parado, ou para baixo)

        meteoros_info.append({'posicao': (posicao_x, posicao_y), 'velocidade_x': -velocidade_x, 'velocidade_y': velocidade_y, 'imagem': img_meteoro})

def movimento_meteoros():
    global meteoros_info
    global coracao

    # Percorra a lista de meteoros_info
    meteoros_para_remover = []

    for meteoro_info in meteoros_info:
        meteoro_info['posicao'] = (meteoro_info['posicao'][0] + meteoro_info['velocidade_x'], meteoro_info['posicao'][1] + meteoro_info['velocidade_y'])

        # Remova o meteoro quando ele estiver fora da tela
        if meteoro_info['posicao'][0] < -70 or meteoro_info['posicao'][1] > 600:
            meteoros_para_remover.append(meteoro_info)

        # Verifique a colisão entre a nave e o meteoro
        if nave_rect.colliderect(pygame.Rect(meteoro_info['posicao'], meteoro_info['imagem'].get_size())):
            coracao -= 1  # Remova uma vida quando houver colisão
            meteoros_para_remover.append(meteoro_info)

    # Remova os meteoros que saíram da tela ou colidiram com a nave
    for meteoro_info in meteoros_para_remover:
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
        velocidade_coracao = randint(4,6)
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
            coracao += 1

    for coracao_info in coracoes_coletados:
        coracoes_info.remove(coracao_info)

def disparar_tiro(posicao_nave):
    global tiro_info, tiro_rect, tiro_index, meteoros_info, tiro_superficies, coracoes_coletados, coracao_info, coracao

    # Verifica se a tecla de espaço está pressionada para disparar um tiro
    if disparando_tiro:
        # Obtém a posição atual da nave
        nave_x, nave_y = posicao_nave

        # Define a posição inicial do tiro em relação à nave
        tiro_x = nave_x + 45
        tiro_y = nave_y - 45

        tiro = {
            'surface': tiro_superficies[tiro_index],
            'rect': tiro_rect.copy(),
            'x': tiro_x,
            'y': tiro_y,
            'speed': 5  # Define a velocidade do tiro
        }

        # Adiciona o tiro à lista de tiros
        tiro_info.append(tiro)

        # Atualize o índice para a próxima imagem do tiro
        tiro_index = (tiro_index + 1) % len(tiro_superficies)

def animacao_tiros():
    tiros_para_remover = []

    for tiro in tiro_info:
        tiro['x'] += tiro['speed']
        tiro_rect.topleft = (tiro['x'], tiro['y'])
        tela.blit(tiro['surface'], tiro_rect)

        # Verifica colisão com os meteoros (assumindo que meteoros_info contém informações dos meteoros)
        colidiu_com_meteoro = False

        for meteoro_info in meteoros_info:
            if tiro_rect.colliderect(pygame.Rect(meteoro_info['posicao'], meteoro_info['imagem'].get_size())):
                colidiu_com_meteoro = True
                tiros_para_remover.append(tiro)
                meteoros_info.remove(meteoro_info)
                break
        
        # Verifica colisão com corações e coleta-os
        coracoes_coletados = []

        for coracao_info in coracoes_info:
            if tiro_rect.colliderect(pygame.Rect(coracao_info['posicao'], coracao_info['imagem'].get_size())):
                coracoes_coletados.append(coracao_info)

        for coracao_info in coracoes_coletados:
            coracoes_info.remove(coracao_info)

        # Remova o tiro quando sair da tela
        if tiro_rect.right > 1500:
            tiros_para_remover.append(tiro)

    # Remova os tiros que colidiram ou saíram da tela
    for tiro in tiros_para_remover:
        tiro_info.remove(tiro)

def mostra_textos():
    global coracao

    texto_coracoes = fonte_pixel.render(f"{coracao}", True, '#FFFFFF')

    logo_coracao = pygame.transform.scale(coracao_superficies[0], (40, 40))

    tela.blit(texto_coracoes, (708, 28))
    tela.blit(logo_coracao, (665, 22))

pygame.init()

coracao = 3

# Tamanho da tela
tamanho = (760, 540)
tela = pygame.display.set_mode(tamanho)

# Título da janela
pygame.display.set_caption("SpaceForce")

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
max_meteoros = 10

for imagem in range (1,11):
    img = pygame.image.load(f'Objects/Items/Meteors/Meteor_{imagem}.png').convert_alpha()
    img = pygame.transform.scale(img, (60, 60))
    meteoros.append(img)
    print(f'Objects/Items/Meteors/Meteor_{imagem}.png')

movimento_y_nave = 0
movimento_x_nave = 0

# Carrega o coração
coracao_superficies = []
coracao_index = 0
coracoes_info = []
max_coracoes = 1

for imagem in range(1, 4):
    img = pygame.image.load(f'Objects/Coracao/Heart{imagem}.png').convert_alpha()
    img = pygame.transform.scale(img, (40, 40))
    coracao_superficies.append(img)

# Carrega o tiro
tiro_superficies = []
tiro_index = 0
tiro_info = []

for imagem in range(1, 5):
    img = pygame.image.load(f'Objects/Spaceships/PNG_Parts&Spriter_Animation/Shots/Shot6/shot6_{imagem}.png').convert_alpha()
    img = pygame.transform.scale(img, (90, 90))
    tiro_superficies.append(img)

# Carrega o tiroparado
tiro = pygame.image.load('Objects/Spaceships/PNG_Parts&Spriter_Animation/Shots/Shot6/shot6_asset.png').convert_alpha()
tiro_rect = nave.get_rect(center = (5, 5))

# Carrega o tiroexp
tiroexp_superficies = []
tiroexp_index = 0
tiroexp_info = []

for imagem in range(1, 11):
    img = pygame.image.load(f'Objects/Spaceships/PNG_Parts&Spriter_Animation/Shots/Shot6/shot6_exp{imagem}.png').convert_alpha()
    img = pygame.transform.scale(img, (40, 40))
    tiroexp_superficies.append(img)

# Cria um evento para adicionar um objeto na tela
novo_objeto_timer = pygame.USEREVENT + 1 # userevento = 0 é reservado, por isso começa com 1.
pygame.time.set_timer(novo_objeto_timer, 500) # cronômetro: a cada 500ms dispara o novo_objeto_timer

novo_coracao_timer = pygame.USEREVENT + 2
pygame.time.set_timer(novo_coracao_timer, 5000)  # A cada 5 segundos dispara o evento

tiro_timer = pygame.USEREVENT + 3
pygame.time.set_timer(tiro_timer, 200)  # A cada 1 segundo dispara o evento

################################################################################
############################ LOOP PRINCIPAL DO JOGO ############################
################################################################################

jogo_ativo = True
tempo_ultimo_disparo = 0
intervalo_entre_disparos = 1000
disparando_tiro = False

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
            if evento.key == pygame.K_SPACE:
                if not disparando_tiro:
                    disparando_tiro = True

        if(evento.type) == pygame.KEYUP:
            movimento_x_nave = 0
            movimento_y_nave = 0
            if evento.key == pygame.K_SPACE:
                disparando_tiro = False
                tempo_ultimo_disparo = 0

        if evento.type == tiro_timer:
            print("tiro")
            if disparando_tiro:
                disparar_tiro(nave_rect.center)
                # tempo_atual = pygame.time.get_ticks()
                # if tempo_atual - tempo_ultimo_disparo >= intervalo_entre_disparos:
                #     tempo_ultimo_disparo = tempo_atual


        
        if(evento.type) == novo_coracao_timer:
            adicionar_coracoes()

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

    # disparar_tiro(nave_rect.center)
    animacao_tiros()
    
    # Atualiza a tela com o conteúdo
    pygame.display.update()

    # Define a quantidade de frames por segundo
    relogio.tick(60)