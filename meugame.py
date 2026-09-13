import pygame
import random

# Inicializa o Pygame e o mixer de som
pygame.init()
pygame.mixer.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Não Deixe a Bola Cair! - Sem Som da Bola")

# Cores Base
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

# ---------------------------------------------------------
# CARREGAMENTO DOS SOM (Apenas transição e perda, som da bola removido)
# ---------------------------------------------------------
try:
    som_transicao = pygame.mixer.Sound("transicao.wav")
except:
    som_transicao = None
    print("Aviso: Arquivo 'transicao.wav' não encontrado na pasta.")

try:
    som_perda = pygame.mixer.Sound("perda.wav")
except:
    som_perda = None


# Lista com os 20 Cenários Diferentes (Ciclo Infinito)
CENARIOS = [
    {"nome": "01. NEON", "fundo": (10, 10, 25), "barra": (0, 255, 200), "bola": (255, 0, 127)},
    {"nome": "02. ESPAÇO", "fundo": (5, 5, 15), "barra": (100, 149, 237), "bola": (255, 255, 0)},
    {"nome": "03. VAPORWAVE", "fundo": (30, 10, 40), "barra": (255, 105, 180), "bola": (0, 255, 255)},
    {"nome": "04. SUBAQUÁTICO", "fundo": (0, 30, 60), "barra": (0, 206, 209), "bola": (255, 165, 0)},
    {"nome": "05. VULCÂNICO", "fundo": (40, 10, 5), "barra": (128, 128, 128), "bola": (255, 69, 0)},
    {"nome": "06. CYBERPUNK", "fundo": (20, 0, 30), "barra": (255, 20, 147), "bola": (0, 255, 0)},
    {"nome": "07. FLORESTA MÁGICA", "fundo": (10, 30, 10), "barra": (50, 205, 50), "bola": (255, 215, 0)},
    {"nome": "08. DESERTO", "fundo": (50, 30, 10), "barra": (210, 180, 140), "bola": (255, 140, 0)},
    {"nome": "09. ÁRTICO", "fundo": (20, 30, 50), "barra": (176, 224, 230), "bola": (0, 191, 255)},
    {"nome": "10. RETRO ARCADE", "fundo": (10, 10, 10), "barra": (255, 255, 0), "bola": (255, 0, 0)},
    {"nome": "11. GALÁXIA X", "fundo": (2, 2, 8), "barra": (138, 43, 226), "bola": (0, 255, 255)},
    {"nome": "12. PÂNTANO", "fundo": (15, 25, 15), "barra": (85, 107, 47), "bola": (173, 255, 47)},
    {"nome": "13. CELA ELÉTRICA", "fundo": (5, 25, 25), "barra": (0, 255, 255), "bola": (255, 255, 255)},
    {"nome": "14. INFERNO SOLAR", "fundo": (50, 5, 0), "barra": (255, 69, 0), "bola": (255, 255, 0)},
    {"nome": "15. ABISMO", "fundo": (5, 5, 5), "barra": (70, 130, 180), "bola": (238, 130, 238)},
    {"nome": "16. MATRIX", "fundo": (0, 15, 0), "barra": (0, 255, 0), "bola": (255, 255, 255)},
    {"nome": "17. HALLOWEEN", "fundo": (20, 10, 30), "barra": (255, 140, 0), "bola": (148, 0, 211)},
    {"nome": "18. DOCE", "fundo": (40, 20, 30), "barra": (255, 182, 193), "bola": (255, 105, 180)},
    {"nome": "19. METAL PESADO", "fundo": (25, 25, 25), "barra": (192, 192, 192), "bola": (255, 0, 0)},
    {"nome": "20. FIM DO MUNDO", "fundo": (15, 0, 0), "barra": (255, 0, 0), "bola": (255, 255, 0)}
]

# Elementos visuais de fundo
estrelas = [(random.randint(0, LARGURA), random.randint(0, ALTURA)) for _ in range(50)]
bolhas = [{"x": random.randint(0, LARGURA), "y": random.randint(0, ALTURA), "vel": random.uniform(1, 3)} for _ in range(15)]

# Configurações da Barrinha
largura_barra = 120
altura_barra = 20
x_barra = (LARGURA - largura_barra) // 2
y_barra = ALTURA - 50
vel_barra = 8

# Configurações da Bola
raio_bola = 12
x_bola = LARGURA // 2
y_bola = ALTURA // 3
vel_x_inicial = 4
vel_y_inicial = -4
vel_x_bola = vel_x_inicial
vel_y_bola = vel_y_inicial

# Sistema de Vidas e Pontuação
pontos = 0
vidas = 3

fonte = pygame.font.SysFont(None, 36)
fonte_game_over = pygame.font.SysFont(None, 64)
fonte_aviso = pygame.font.SysFont(None, 38)

# Controle de pausa e transição
tempo_transicao = 0 
tempo_mensagem = 0
texto_aviso_atual = ""

rodando = True
game_over = False
relogio = pygame.time.Clock()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN and game_over:
            if evento.key == pygame.K_SPACE:
                pontos = 0
                vidas = 3
                vel_x_bola = vel_x_inicial
                vel_y_bola = vel_y_inicial
                x_bola = LARGURA // 2
                y_bola = ALTURA // 3
                game_over = False

    if not game_over:
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and x_barra > 0:
            x_barra -= vel_barra
        if teclas[pygame.K_RIGHT] and x_barra < LARGURA - largura_barra:
            x_barra += vel_barra

        # Pausa a bola durante a transição de cenário
        if tempo_transicao > 0:
            tempo_transicao -= 1
        else:
            x_bola += vel_x_bola
            y_bola += vel_y_bola

            if x_bola - raio_bola <= 0 or x_bola + raio_bola >= LARGURA:
                vel_x_bola = -vel_x_bola

            if y_bola - raio_bola <= 0:
                vel_y_bola = -vel_y_bola

            # Colisão da bola com a barra (sem tocar som de bola)
            if (y_barra <= y_bola + raio_bola <= y_barra + altura_barra) and \
               (x_barra <= x_bola <= x_barra + largura_barra):
                
                nivel_antigo = pontos // 5
                pontos += 1
                nivel_novo = pontos // 5

                # Mudança de cenário a cada 5 pontos (com som e pausa)
                if nivel_novo > nivel_antigo:
                    if som_transicao:
                        som_transicao.play()

                    indice_cenario = nivel_novo % len(CENARIOS)
                    tempo_mensagem = 120
                    texto_aviso_atual = f"🚀 {CENARIOS[indice_cenario]['nome']} ATIVADO! 🚀"
                    
                    # Congela a bola por 90 frames (~1.5 segundos)
                    tempo_transicao = 90

                vel_y_bola = -vel_y_bola

                if pontos % 10 == 0:
                    fator_aumento = 1.15
                    vel_x_bola *= fator_aumento
                    vel_y_bola *= fator_aumento

                if pontos == 20:
                    vidas += 1
                    tempo_mensagem = 120
                    texto_aviso_atual = "⚡ 20 PONTOS! +1 VIDA EXTRA! ⚡"

            # Se a bola cair no chão
            if y_bola - raio_bola >= ALTURA:
                if som_perda:
                    som_perda.play()

                vidas -= 1
                if vidas <= 0:
                    game_over = True
                else:
                    x_bola = LARGURA // 2
                    y_bola = ALTURA // 3
                    vel_x_bola = vel_x_inicial if vel_x_bola > 0 else -vel_x_inicial
                    vel_y_bola = -abs(vel_y_inicial)

    # Índice cíclico para os cenários
    indice_cenario = (pontos // 5) % len(CENARIOS)
    cenario_atual = CENARIOS[indice_cenario]

    tela.fill(cenario_atual["fundo"])

    # Elementos visuais dinâmicos de fundo
    if "ESPAÇO" in cenario_atual["nome"] or "GALÁXIA" in cenario_atual["nome"]:
        for sx, sy in estrelas:
            pygame.draw.circle(tela, BRANCO, (sx, sy), 2)
    elif "SUBAQUÁTICO" in cenario_atual["nome"]:
        for b in bolhas:
            if not game_over:
                b["y"] -= b["vel"]
                if b["y"] < 0:
                    b["y"] = ALTURA
                    b["x"] = random.randint(0, LARGURA)
            pygame.draw.circle(tela, (100, 200, 255), (int(b["x"]), int(b["y"])), 3)

    if not game_over:
        pygame.draw.rect(tela, cenario_atual["barra"], (x_barra, y_barra, largura_barra, altura_barra))
        pygame.draw.circle(tela, cenario_atual["bola"], (int(x_bola), int(y_bola)), raio_bola)

        texto_pontos = fonte.render(f"Pontos: {pontos}", True, BRANCO)
        texto_vidas = fonte.render(f"Vidas: {vidas}", True, VERMELHO)
        texto_nome_cenario = fonte.render(f"Fase: {cenario_atual['nome']}", True, cenario_atual["barra"])
        
        tela.blit(texto_pontos, (20, 20))
        tela.blit(texto_vidas, (20, 60))
        tela.blit(texto_nome_cenario, (20, 100))

        if tempo_mensagem > 0:
            texto_bonus = fonte_aviso.render(texto_aviso_atual, True, BRANCO)
            tela.blit(texto_bonus, (LARGURA // 2 - texto_bonus.get_width() // 2, 140))
            tempo_mensagem -= 1
    else:
        texto_fim = fonte_game_over.render("GAME OVER", True, VERMELHO)
        texto_reiniciar = fonte.render("Pressione ESPAÇO para Jogar Novamente", True, BRANCO)
        
        tela.blit(texto_fim, (LARGURA // 2 - texto_fim.get_width() // 2, ALTURA // 2 - 50))
        tela.blit(texto_reiniciar, (LARGURA // 2 - texto_reiniciar.get_width() // 2, ALTURA // 2 + 20))

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()