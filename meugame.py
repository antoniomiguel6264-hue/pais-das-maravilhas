import pygame
import random
import sqlite3
import datetime

# Inicializa o Pygame e o mixer de som
pygame.init()
pygame.mixer.init()

# ---------------------------------------------------------
# CONFIGURAÇÃO DO BANCO DE DADOS (SQLite)
# ---------------------------------------------------------
conexao = sqlite3.connect("ranking_jogo.db")
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS recordes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pontuacao_maxima INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS rankings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_jogador TEXT NOT NULL,
        pontuacao INTEGER NOT NULL,
        data_partida TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS estatisticas_gerais (
        id INTEGER PRIMARY KEY CHECK(id = 1),
        total_partidas_jogadas INTEGER NOT NULL DEFAULT 0,
        tempo_total_jogo REAL NOT NULL DEFAULT 0,
        fase_maxima_desbloqueada INTEGER NOT NULL DEFAULT 0
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS conquistas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        descricao TEXT NOT NULL,
        desbloqueada INTEGER NOT NULL DEFAULT 0,
        data_desbloqueio TEXT
    )
""")

conexao.commit()

# Para não perder a tabela no primeiro uso
cursor.execute("INSERT OR IGNORE INTO estatisticas_gerais (id, total_partidas_jogadas, tempo_total_jogo, fase_maxima_desbloqueada) VALUES (1, 0, 0, 0)")

# Carrega conquistas seed do jogo
cursor.execute("SELECT nome FROM conquistas WHERE nome = 'Primeiros Dez Pontos'")
if cursor.fetchone() is None:
    cursor.executemany("""
        INSERT OR IGNORE INTO conquistas (nome, descricao, desbloqueada, data_desbloqueio)
        VALUES (?, ?, 0, NULL)
    """, [
        ("Primeiros Dez Pontos", "Marque 10 pontos em uma partida.",),
        ("O Mestre da Bola", "Marque 50 pontos em uma partida.",),
        ("Fase Extraterrestre", "Alcance a fase 5.",),
    ])

conexao.commit()

cursor.execute("SELECT MAX(pontuacao_maxima) FROM recordes")
resultado = cursor.fetchone()
recorde_atual = resultado[0] if resultado[0] is not None else 0

# Configurações da tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Não Deixe a Bola Cair! - Com Menu Inicial")

# Cores Base
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AMARELO = (255, 223, 0)

# ---------------------------------------------------------
# CARREGAMENTO DOS SONS
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

# Sistema de Vidas, Pontuação e Fases
pontos = 0
vidas = 3
pontos_consecutivos = 0
fase_atual = 0
dificuldade_fase = 1.0

# Sistema de Estatísticas do Tempo de Jogo
tempo_partida_segundos = 0.0
fase_maxima_desbloqueada = 0

fonte = pygame.font.SysFont(None, 36)
fonte_titulo = pygame.font.SysFont(None, 52)
fonte_game_over = pygame.font.SysFont(None, 64)
fonte_aviso = pygame.font.SysFont(None, 38)

# Controle de Estados do Jogo: 'menu', 'jogando', 'game_over'
estado_jogo = 'menu'

tempo_transicao = 0 
tempo_mensagem = 0
texto_aviso_atual = ""

# Funções auxiliares de persistência

def salvar_ranking(pontuacao_final):
    nome_jogador = "JOG"
    data_partida = datetime.date.today().isoformat()
    cursor.execute("""
        INSERT INTO rankings (nome_jogador, pontuacao, data_partida)
        VALUES (?, ?, ?)
    """, (nome_jogador, pontuacao_final, data_partida))
    conexao.commit()


def listar_top_10():
    cursor.execute("""
        SELECT nome_jogador, pontuacao, data_partida
        FROM rankings
        ORDER BY pontuacao DESC, id DESC
        LIMIT 10
    """)
    return cursor.fetchall()


def atualizar_estatisticas(total_partidas_novas=0, tempo_extra_segundos=0, fase_maxima=0):
    cursor.execute("SELECT total_partidas_jogadas, tempo_total_jogo, fase_maxima_desbloqueada FROM estatisticas_gerais WHERE id = 1")
    estatistica = cursor.fetchone()

    if estatistica is None:
        cursor.execute("INSERT OR IGNORE INTO estatisticas_gerais (id, total_partidas_jogadas, tempo_total_jogo, fase_maxima_desbloqueada) VALUES (1, 0, 0, 0)")
        estatistica = (0, 0, 0)

    total_partidas = estatistica[0] + total_partidas_novas
    tempo_total = estatistica[1] + tempo_extra_segundos
    fase_atual = max(estatistica[2], fase_maxima)

    cursor.execute("""
        UPDATE estatisticas_gerais
        SET total_partidas_jogadas = ?,
            tempo_total_jogo = ?,
            fase_maxima_desbloqueada = ?
        WHERE id = 1
    """, (total_partidas, tempo_total, fase_atual))
    conexao.commit()


def desbloquear_conquistas(pontuacao_final, fase_alcancada):
    # Conquistas por pontuação e fase
    lista_conquistas = []
    if pontuacao_final >= 10:
        lista_conquistas.append("Primeiros Dez Pontos")
    if pontuacao_final >= 50:
        lista_conquistas.append("O Mestre da Bola")
    if fase_alcancada >= 5:
        lista_conquistas.append("Fase Extraterrestre")

    for nome in lista_conquistas:
        cursor.execute("SELECT desbloqueada FROM conquistas WHERE nome = ?", (nome,))
        resultado = cursor.fetchone()
        if resultado is not None and resultado[0] == 0:
            cursor.execute("""
                UPDATE conquistas
                SET desbloqueada = 1,
                    data_desbloqueio = ?
                WHERE nome = ?
            """, (datetime.date.today().isoformat(), nome))
    conexao.commit()


def obter_ranking_texto():
    linhas = []
    top10 = listar_top_10()
    for index, (nome, pontuacao, data_partida) in enumerate(top10, start=1):
        linhas.append(f"{index:02d}. {nome} {pontuacao} pts - {data_partida}")
    return linhas

rodando = True
relogio = pygame.time.Clock()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        if evento.type == pygame.KEYDOWN:
            if estado_jogo == 'menu' and evento.key == pygame.K_SPACE:
                # Inicia a partida a partir do menu
                pontos = 0
                vidas = 3
                pontos_consecutivos = 0
                fase_atual = 0
                dificuldade_fase = 1.0
                tempo_partida_segundos = 0.0
                fase_maxima_desbloqueada = 0
                vel_x_bola = vel_x_inicial
                vel_y_bola = vel_y_inicial
                x_bola = LARGURA // 2
                y_bola = ALTURA // 3
                estado_jogo = 'jogando'
                atualizar_estatisticas(total_partidas_novas=1)
                
            elif estado_jogo == 'game_over' and evento.key == pygame.K_SPACE:
                # Reinicia a partida após o Game Over
                pontos = 0
                vidas = 3
                pontos_consecutivos = 0
                fase_atual = 0
                dificuldade_fase = 1.0
                tempo_partida_segundos = 0.0
                fase_maxima_desbloqueada = 0
                vel_x_bola = vel_x_inicial
                vel_y_bola = vel_y_inicial
                x_bola = LARGURA // 2
                y_bola = ALTURA // 3
                estado_jogo = 'jogando'
                atualizar_estatisticas(total_partidas_novas=1)

    if estado_jogo == 'jogando':
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and x_barra > 0:
            x_barra -= vel_barra
        if teclas[pygame.K_RIGHT] and x_barra < LARGURA - largura_barra:
            x_barra += vel_barra

        # Tempo de jogo e fase máxima alcançada
        tempo_partida_segundos += 1 / 60
        fase_maxima_desbloqueada = max(fase_maxima_desbloqueada, (pontos // 5))

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

            # Colisão da bola com a barra
            if (y_barra <= y_bola + raio_bola <= y_barra + altura_barra) and \
               (x_barra <= x_bola <= x_barra + largura_barra):
                
                fase_anterior = fase_atual
                pontos += 1
                pontos_consecutivos += 1
                fase_atual = pontos // 5

                # Modo de fases: troca a fase a cada 5 pontos
                if fase_atual > fase_anterior:
                    # Nova fase com dificuldade aleatória
                    dificuldade_fase = random.uniform(1.08, 1.35)
                    sinal_x = 1 if vel_x_bola >= 0 else -1
                    sinal_y = -1 if vel_y_bola < 0 else 1
                    vel_x_bola = sinal_x * abs(vel_x_bola) * dificuldade_fase
                    vel_y_bola = sinal_y * abs(vel_y_bola) * dificuldade_fase

                    if som_transicao:
                        som_transicao.play()

                    indice_cenario = fase_atual % len(CENARIOS)
                    tempo_mensagem = 120
                    texto_aviso_atual = f"🚀 FASE {fase_atual + 1} - {CENARIOS[indice_cenario]['nome']} ATIVADA! DIFICULDADE {dificuldade_fase:.2f}x 🚀"
                    
                    tempo_transicao = 90

                vel_y_bola = -vel_y_bola

                if pontos % 10 == 0:
                    fator_aumento = 1.15
                    vel_x_bola *= fator_aumento
                    vel_y_bola *= fator_aumento

                # A cada 8 pontos consecutivos o jogador recebe uma vida extra.
                if pontos_consecutivos >= 8:
                    vidas += 1
                    pontos_consecutivos = 0
                    tempo_mensagem = 120
                    texto_aviso_atual = "⚡ 8 PONTOS CONSECUTIVOS! +1 VIDA EXTRA! ⚡"

                if pontos == 20:
                    vidas += 1
                    tempo_mensagem = 120
                    texto_aviso_atual = "⚡ 20 PONTOS! +1 VIDA EXTRA! ⚡"

            # Se a bola cair no chão
            if y_bola - raio_bola >= ALTURA:
                if som_perda:
                    som_perda.play()

                pontos_consecutivos = 0
                vidas -= 1
                if vidas <= 0:
                    estado_jogo = 'game_over'

                    # Atualiza recorde absoluto
                    if pontos > recorde_atual:
                        recorde_atual = pontos
                        cursor.execute("INSERT INTO recordes (pontuacao_maxima) VALUES (?)", (pontos,))
                        conexao.commit()

                    # Salva o ranking de top 10 com nome / data / pontuação
                    salvar_ranking(pontos)

                    # Salva estatísticas gerais acumuladas do jogador
                    atualizar_estatisticas(tempo_extra_segundos=tempo_partida_segundos, fase_maxima=fase_maxima_desbloqueada)

                    # Salva conquistas da partida
                    desbloquear_conquistas(pontos, fase_maxima_desbloqueada)
                else:
                    x_bola = LARGURA // 2
                    y_bola = ALTURA // 3
                    vel_x_bola = vel_x_inicial if vel_x_bola > 0 else -vel_x_inicial
                    vel_y_bola = -abs(vel_y_inicial)

    # Índice cíclico para os cenários mesmo em modo de fase
    indice_cenario = fase_atual % len(CENARIOS)
    cenario_atual = CENARIOS[indice_cenario]

    tela.fill(cenario_atual["fundo"])

    # Elementos visuais dinâmicos de fundo
    if "ESPAÇO" in cenario_atual["nome"] or "GALÁXIA" in cenario_atual["nome"]:
        for sx, sy in estrelas:
            pygame.draw.circle(tela, BRANCO, (sx, sy), 2)
    elif "SUBAQUÁTICO" in cenario_atual["nome"]:
        for b in bolhas:
            if estado_jogo == 'jogando':
                b["y"] -= b["vel"]
                if b["y"] < 0:
                    b["y"] = ALTURA
                    b["x"] = random.randint(0, LARGURA)
            pygame.draw.circle(tela, (100, 200, 255), (int(b["x"]), int(b["y"])), 3)

    # Renderização visual dependendo do estado do jogo
    if estado_jogo == 'menu':
        texto_titulo = fonte_titulo.render("NÃO DEIXE A BOLA CAIR!", True, AMARELO)
        texto_recorde_menu = fonte.render(f"Recorde Atual: {recorde_atual}", True, BRANCO)
        texto_instrucao = fonte.render("Pressione ESPAÇO para Iniciar a Partida", True, BRANCO)

        # Exibe o top 10 no menu como mini placar arcade
        linhas_top10 = obter_ranking_texto()
        y_ranking = ALTURA // 2 + 80
        for idx, linha in enumerate(linhas_top10[:5]):
            texto_ranking_linha = fonte.render(linha, True, BRANCO)
            tela.blit(texto_ranking_linha, (20, y_ranking + idx * 30))

        # Posicionamento único e centrado
        tela.blit(texto_titulo, (LARGURA // 2 - texto_titulo.get_width() // 2, 80))
        tela.blit(texto_recorde_menu, (LARGURA // 2 - texto_recorde_menu.get_width() // 2, 145))
        tela.blit(texto_instrucao, (LARGURA // 2 - texto_instrucao.get_width() // 2, 190))

    elif estado_jogo == 'jogando':
        pygame.draw.rect(tela, cenario_atual["barra"], (x_barra, y_barra, largura_barra, altura_barra))
        pygame.draw.circle(tela, cenario_atual["bola"], (int(x_bola), int(y_bola)), raio_bola)

        # HUD melhorado com caixa de informações
        painel = pygame.Surface((310, 180), pygame.SRCALPHA)
        pygame.draw.rect(painel, (20, 20, 30, 180), (0, 0, 310, 180), border_radius=12)
        pygame.draw.rect(painel, cenario_atual["barra"], (0, 0, 310, 180), 2, border_radius=12)
        tela.blit(painel, (12, 12))

        nome_cenario_resumido = cenario_atual["nome"].split(".", 1)[-1].strip()
        nome_cenario_resumido = nome_cenario_resumido[:16]

        texto_pontos = fonte.render(f"Pontos: {pontos}", True, BRANCO)
        texto_vidas = fonte.render(f"Vidas: {'♥ ' * vidas}", True, VERMELHO)
        texto_nome_cenario = fonte.render(f"Fase {fase_atual + 1}: {nome_cenario_resumido}", True, cenario_atual["barra"])
        texto_dificuldade = fonte.render(f"Dificuldade: {dificuldade_fase:.2f}x", True, AMARELO)

        # Posicionamento interno do HUD no retângulo
        tela.blit(texto_pontos, (24, 22))
        tela.blit(texto_vidas, (24, 58))
        tela.blit(texto_nome_cenario, (24, 94))
        tela.blit(texto_dificuldade, (24, 132))

        if tempo_mensagem > 0:
            texto_bonus = fonte_aviso.render(texto_aviso_atual, True, BRANCO)
            tela.blit(texto_bonus, (LARGURA // 2 - texto_bonus.get_width() // 2, 140))
            tempo_mensagem -= 1

    elif estado_jogo == 'game_over':
        texto_fim = fonte_game_over.render("GAME OVER", True, VERMELHO)
        texto_pontos_finais = fonte.render(f"Pontuação Final: {pontos}", True, BRANCO)
        texto_recorde = fonte.render(f"Recorde Salvo: {recorde_atual}", True, AMARELO)
        texto_reiniciar = fonte.render("Pressione ESPAÇO para Jogar Novamente", True, BRANCO)

        # Posicionamento centralizado na tela de fim
        tela.blit(texto_fim, (LARGURA // 2 - texto_fim.get_width() // 2, ALTURA // 2 - 110))
        tela.blit(texto_pontos_finais, (LARGURA // 2 - texto_pontos_finais.get_width() // 2, ALTURA // 2 - 40))
        tela.blit(texto_recorde, (LARGURA // 2 - texto_recorde.get_width() // 2, ALTURA // 2 + 10))
        tela.blit(texto_reiniciar, (LARGURA // 2 - texto_reiniciar.get_width() // 2, ALTURA // 2 + 70))

    pygame.display.flip()
    relogio.tick(60)

conexao.close()
pygame.quit()