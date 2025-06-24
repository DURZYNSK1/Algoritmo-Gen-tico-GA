import pygame
import sys
import random

# Configurações do tabuleiro e da tela
TAM_CELULA = 60
NUM_RAINHAS = 8
LARGURA = TAM_CELULA * NUM_RAINHAS
ALTURA = TAM_CELULA * NUM_RAINHAS + 50

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Problema das 8 Rainhas - Algoritmo Genético")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Fonte
font = pygame.font.SysFont(None, 36)

# Variável que armazena a solução atual
solucao = []

# ALGORITMO GENÉTICO #

# cria um indivíduo aleatório, representado por uma lista onde cada elemento
# indica a linha da rainha em cada coluna do tabuleiro
def criar_individuo():
    return [random.randint(0, 7) for _ in range(8)]

# calcula o "fitness" de um indivíduo, ou seja, o número de conflitos entre rainhas
# quanto menor o valor, melhor a solução; zero significa sem conflitos
def fitness(individuo):
    conflitos = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if individuo[i] == individuo[j] or abs(individuo[i] - individuo[j]) == abs(i - j):
                conflitos += 1
    return conflitos

# seleção por torneio: escolhe 3 indivíduos aleatórios e retorna o melhor entre eles
def selecao(populacao):
    return min(random.sample(populacao, 3), key=fitness)

# crossover simples: combina os genes dos pais em um ponto de corte aleatório
def crossover(pai1, pai2):
    ponto = random.randint(1, 6)
    return pai1[:ponto] + pai2[ponto:]

# aplica mutação em um indivíduo com certa probabilidade (taxa)
# a mutação consiste em alterar a posição de uma rainha aleatoriamente
def mutacao(individuo, taxa=0.2):
    if random.random() < taxa:
        i = random.randint(0, 7)
        individuo[i] = random.randint(0, 7)
    return individuo

# executa o algoritmo genético para encontrar uma solução para o problema
def gerar_solucao_ga():
    populacao = [criar_individuo() for _ in range(100)]
    for _ in range(1000):
        nova_pop = []
        for _ in range(100):
            pai1, pai2 = selecao(populacao), selecao(populacao)
            filho = crossover(pai1, pai2)
            filho = mutacao(filho)
            nova_pop.append(filho)
        populacao = nova_pop
        melhor = min(populacao, key=fitness)
        if fitness(melhor) == 0:
            return melhor
    return melhor  # retorna o melhor mesmo que não seja perfeito

# NTERFACE GRÁFICA #

# desenha o tabuleiro 8x8, com cores alternadas para as células
def desenhar_tabuleiro():
    for linha in range(NUM_RAINHAS):
        for coluna in range(NUM_RAINHAS):
            cor = BRANCO if (linha + coluna) % 2 == 0 else PRETO
            rect = pygame.Rect(coluna * TAM_CELULA, linha * TAM_CELULA, TAM_CELULA, TAM_CELULA)
            pygame.draw.rect(screen, cor, rect)

# desenha as rainhas na tela, baseando-se na solução atual
def desenhar_rainhas():
    for coluna, linha in enumerate(solucao):
        center_x = coluna * TAM_CELULA + TAM_CELULA // 2
        center_y = linha * TAM_CELULA + TAM_CELULA // 2
        radius = TAM_CELULA // 3
        pygame.draw.circle(screen, VERMELHO, (center_x, center_y), radius)

# desenha o botão para gerar uma nova solução usando o Algoritmo Genético
def desenhar_botao():
    botao_largura = 250
    botao_altura = 40
    botao_x = 10
    botao_y = ALTURA - 50
    botao_rect = pygame.Rect(botao_x, botao_y, botao_largura, botao_altura)
    pygame.draw.rect(screen, AZUL, botao_rect)
    texto = font.render("Gerar Nova Solução (GA)", True, BRANCO)
    texto_rect = texto.get_rect(center=botao_rect.center)
    screen.blit(texto, texto_rect)
    return botao_rect

# função principal que gerencia o loop de eventos e atualização da tela
def main():
    global solucao
    clock = pygame.time.Clock()
    solucao = gerar_solucao_ga()  # gera a primeira solução ao iniciar o programa

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(event.pos):
                    solucao = gerar_solucao_ga()

        # desenha o tabuleiro, as rainhas e o botão a cada frame
        desenhar_tabuleiro()
        desenhar_rainhas()
        botao_rect = desenhar_botao()
        pygame.display.flip()
        clock.tick(60)

# executa o programa chamando a função principal
if __name__ == "__main__":
    main()
