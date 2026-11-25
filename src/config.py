# Configurações centrais do jogo (tela, cores e constantes da mecânica).
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

TITULO_JOGO = "IA Verifica - Nem tudo é verdade"

# Cores (R, G, B)
BRANCO = (255, 255, 255)
PRETO = (20, 20, 20)
CINZA_FUNDO = (245, 240, 255)
CINZA_BORDA = (180, 185, 195)
AZUL_ESCURO = (75, 0, 130)
VERDE = (0, 150, 100)
VERMELHO = (210, 40, 60)
AMARELO = (202, 138, 4)

# Regras da proposta
TOTAL_RODADAS = 3
CASOS_POR_RODADA = 3
CREDIBILIDADE_MAX = 20
MORAL_MAX = 15
PRODUTIVIDADE_MAX = 10
PENALIDADE_ERRO = 5
TEMPO_LIMITE_CASO = 20  # segundos por caso antes de perder Produtividade
PONTOS_ACERTO = 10

CAMINHO_RECORDE = "data/recorde.txt"
CAMINHO_CASOS = "data/casos.txt"