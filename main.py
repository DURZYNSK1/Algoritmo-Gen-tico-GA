import pygame
import sys
import random

# Configurações
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

### ALGORITMO GENÉTICO ###
def criar_individuo():
    return [random.randint(0, 7) for _ in range(8)]

def fitness(individuo):
    conflitos = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if individuo[i] == individuo[j] or abs(individuo[i] - individuo[j]) == abs(i - j):
                conflitos += 1
    return conflitos

def selecao(populacao):
    return min(random.sample(populacao, 3), key=fitness)

def crossover(pai1, pai2):
    ponto = random.randint(1, 6)
    return pai1[:ponto] + pai2[ponto:]

def mutacao(individuo, taxa=0.2):
    if random.random() < taxa:
        i = random.randint(0, 7)
        individuo[i] = random.randint(0, 7)
    return individuo

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

### NTERFACE GRÁFICA ###
def desenhar_tabuleiro():
    for linha in range(NUM_RAINHAS):
        for coluna in range(NUM_RAINHAS):
            cor = BRANCO if (linha + coluna) % 2 == 0 else PRETO
            rect = pygame.Rect(coluna * TAM_CELULA, linha * TAM_CELULA, TAM_CELULA, TAM_CELULA)
            pygame.draw.rect(screen, cor, rect)

def desenhar_rainhas():
    for coluna, linha in enumerate(solucao):
        center_x = coluna * TAM_CELULA + TAM_CELULA // 2
        center_y = linha * TAM_CELULA + TAM_CELULA // 2
        radius = TAM_CELULA // 3
        pygame.draw.circle(screen, VERMELHO, (center_x, center_y), radius)

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

def main():
    global solucao
    clock = pygame.time.Clock()
    solucao = gerar_solucao_ga()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(event.pos):
                    solucao = gerar_solucao_ga()

        desenhar_tabuleiro()
        desenhar_rainhas()
        botao_rect = desenhar_botao()  # botão atualizado em cada frame
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()