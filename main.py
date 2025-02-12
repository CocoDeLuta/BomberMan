import pygame
import a_estrela
import random

# Inicializa o pygame
pygame.init()

# Configurações do grid
WIDTH, HEIGHT = 600, 650  # Aumenta altura para a HUD
ROWS, COLS = 10, 10
CELL_SIZE = WIDTH // COLS
HUD_HEIGHT = 50  # Espaço para a HUD

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)

# Criação da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.setCaption("Bomberman")

# Fonte para HUD
font = pygame.font.Font(None, 36)

# Matriz do grid (0 = vazio, 1 = jogador, 2 = IA, 3 = parede, 4 = bomba)
grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# Estado do jogo
player_x, player_y = 1, 1 # Posição inicial do jogador
ia_x, ia_y = 1, 4 # Posição inicial da IA
player_has_bomb = True # Indica se o jogador tem uma bomba
bombs = {} # Dicionário para rastrear as bombas e seus tempos de explosão
turn = "player" # Indica de quem é o turno (player, ia, game)
game_over = False # Indica se o jogo acabou
winner = None # Indica o vencedor
player_moved = False # Indica se o jogador se moveu
ia = a_estrela.AEstrela() # Instância da classe AEstrela
ia_turn_jump = 0 # quando for 5 ia anda 2 casas

# Função para desenhar o grid
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            value = grid[row][col]
            color = WHITE
            if value == 1:
                color = BLUE
            elif value == 2:
                color = RED
            elif value == 3:
                color = GRAY
            elif value == 4:
                color = YELLOW
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE + HUD_HEIGHT, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

# Função para desenhar HUD
def draw_hud():
    screen.fill(WHITE, (0, 0, WIDTH, HUD_HEIGHT))
    bomb_status = "Disp." if player_has_bomb else "Indisp."
    hud_text = font.render(f"Bomba: {bomb_status} | Turno: {turn[0].upper()} | Esp: Passar", True, BLACK)
    screen.blit(hud_text, (20, 10))

# Função para desenhar tela de game over
def draw_game_over():
    screen.fill(WHITE)
    text = font.render(f"{winner} venceu!", True, BLACK)
    screen.blit(text, (WIDTH // 3, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    exit()

# Função para movimentação
def move_player(dx, dy):
    global player_x, player_y, player_moved
    if not player_moved:
        # Calcula a nova posição do jogador
        new_x, new_y = player_x + dx, player_y + dy
        # Verifica se a nova posição está dentro dos limites do grid e não é uma parede ou bomba
        if 0 <= new_x < ROWS and 0 <= new_y < COLS and grid[new_x][new_y] not in [3, 4]:
            # Atualiza a posição anterior do jogador para vazio
            grid[player_x][player_y] = 0
            # Define a nova posição do jogador
            grid[new_x][new_y] = 1
            # Atualiza as coordenadas do jogador
            player_x, player_y = new_x, new_y
            # Marca que o jogador se moveu
            player_moved = True

# Função para colocar bomba
def place_bomb(dx, dy):
    global player_has_bomb
    # Calcula a posição onde a bomba será colocada
    bx, by = player_x + dx, player_y + dy
    # Verifica se o jogador tem uma bomba e se a posição é válida (dentro dos limites do grid e vazia)
    if player_has_bomb and 0 <= bx < ROWS and 0 <= by < COLS and grid[bx][by] == 0:
        # Coloca a bomba na posição calculada
        grid[bx][by] = 4
        # Define o tempo para a bomba explodir (2 turnos)
        bombs[(bx, by)] = 2
        # Marca que o jogador não tem mais bomba
        player_has_bomb = False

# Função para processar explosão das bombas
def process_bombs():
    global player_has_bomb, game_over, winner
    to_explode = []  # Lista de bombas que irão explodir
    # Atualiza o tempo de explosão de cada bomba
    for (bx, by) in list(bombs.keys()):
        bombs[(bx, by)] -= 1
        if bombs[(bx, by)] == 0:
            to_explode.append((bx, by))
    # Processa a explosão das bombas
    for (bx, by) in to_explode:
        del bombs[(bx, by)]
        grid[bx][by] = 0  # Remove a bomba do grid
        # Verifica as posições adjacentes à bomba
        for ax, ay in [(bx-1, by), (bx+1, by), (bx, by-1), (bx, by+1)]:
            if 0 <= ax < ROWS and 0 <= ay < COLS:
                # Se a explosão atingir o jogador, a IA vence
                if grid[ax][ay] == 1:
                    winner = "IA"
                    game_over = True
                # Se a explosão atingir a IA, o jogador vence
                elif grid[ax][ay] == 2:
                    winner = "Jogador"
                    game_over = True
                grid[ax][ay] = 0  # Remove qualquer objeto atingido pela explosão
        player_has_bomb = True  # Permite que o jogador coloque outra bomba

# Usar depois talvez
def search_player(x, y):
    # Funcao que procura o player nas casas adjacentes cima, baixo, esquerda e direita
    # Se encontrar a IA coloca uma bomba
    distancia = 2
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ROWS and 0 <= ny < COLS:
            if grid[nx][ny] == 1:
                return True
    return False

# Loop principal
running = True
player_x, player_y = random.randint(0, 9), random.randint(0, 9)  # Posição inicial aleatória do jogador
ia_x, ia_y = random.randint(0, 9), random.randint(0, 9)  # Posição inicial aleatória da IA
grid[player_x][player_y] = 1  # Marca a posição inicial do jogador no grid
grid[ia_x][ia_y] = 2  # Marca a posição inicial da IA no grid

# Gera paredes aleatórias no grid
max_paredes = random.randint(5, 15)
todas_paredes = False
while not todas_paredes:
    x, y = random.randint(0, 9), random.randint(0, 9)
    if grid[x][y] == 0:
        grid[x][y] = 3  # Coloca uma parede no grid
        max_paredes -= 1
    if max_paredes == 0:
        todas_paredes = True

# Loop principal do jogo
while running:
    screen.fill(WHITE)  # Limpa a tela
    draw_hud()  # Desenha a HUD
    draw_grid()  # Desenha o grid

    if game_over:
        draw_game_over()  # Desenha a tela de game over

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Sai do loop principal se o evento for de saída

        if turn == "player" and event.type == pygame.KEYDOWN:
            if not player_moved:
                # Movimenta o jogador com as teclas W, A, S, D
                if event.key == pygame.K_w:
                    move_player(-1, 0)
                elif event.key == pygame.K_s:
                    move_player(1, 0)
                elif event.key == pygame.K_a:
                    move_player(0, -1)
                elif event.key == pygame.K_d:
                    move_player(0, 1)
            # Coloca uma bomba com as setas direcionais
            if event.key == pygame.K_UP:
                place_bomb(-1, 0)
            elif event.key == pygame.K_DOWN:
                place_bomb(1, 0)
            elif event.key == pygame.K_LEFT:
                place_bomb(0, -1)
            elif event.key == pygame.K_RIGHT:
                place_bomb(0, 1)
            # Passa o turno com a tecla espaço
            elif event.key == pygame.K_SPACE:
                if turn == "player":
                    turn = "ia"
                    player_moved = False
                elif turn == "ia":
                    turn = "game"
                elif turn == "game":
                    turn = "player"
                break

        if turn == "ia":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # IA realiza um movimento usando o algoritmo A*
                    movimento = ia.a_star_search_avoid_4(grid, (ia_x, ia_y), (player_x, player_y))
                    print(movimento)
                    if movimento is not None:
                        grid[ia_x][ia_y] = 0  # Limpa a posição anterior da IA
                        ia_x, ia_y = movimento  # Atualiza a posição da IA
                        if grid[ia_x][ia_y] == 1:
                            winner = "IA"
                            game_over = True
                        grid[ia_x][ia_y] = 2  # Marca a nova posição da IA no grid
                        ia_turn_jump += 1
                        if ia_turn_jump == 5:
                            turn = "ia"
                            ia_turn_jump = 0
                            break
                    turn = "game"
                    break

        if turn == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    process_bombs()  # Processa as explosões das bombas
                    turn = "player"
                    break

    pygame.display.flip()  # Atualiza a tela
pygame.quit()  # Encerra o pygame
