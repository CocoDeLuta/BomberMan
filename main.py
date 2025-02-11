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
pygame.display.set_caption("Grid com Turnos e Bombas")

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
player_x, player_y = 1, 1
ia_x, ia_y = 1, 4
player_has_bomb = True
bombs = {}
turn = "player"
game_over = False
winner = None
player_moved = False
ia = a_estrela.AEstrela()
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
    bomb_status = "Disponível" if player_has_bomb else "Indisponível"
    hud_text = font.render(f"Bomba: {bomb_status} | Turno: {turn.capitalize()} | Espaço: Passar Turno", True, BLACK)
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
        new_x, new_y = player_x + dx, player_y + dy
        if 0 <= new_x < ROWS and 0 <= new_y < COLS and grid[new_x][new_y] not in [3, 4]:
            grid[player_x][player_y] = 0
            grid[new_x][new_y] = 1
            player_x, player_y = new_x, new_y
            player_moved = True

# Função para colocar bomba
def place_bomb(dx, dy):
    global player_has_bomb
    bx, by = player_x + dx, player_y + dy
    if player_has_bomb and 0 <= bx < ROWS and 0 <= by < COLS and grid[bx][by] == 0:
        grid[bx][by] = 4
        bombs[(bx, by)] = 2  # Explode em 2 turnos
        player_has_bomb = False

# Função para explosão
def process_bombs():
    global player_has_bomb, game_over, winner
    to_explode = []
    for (bx, by) in list(bombs.keys()):
        bombs[(bx, by)] -= 1
        if bombs[(bx, by)] == 0:
            to_explode.append((bx, by))
    for (bx, by) in to_explode:
        del bombs[(bx, by)]
        grid[bx][by] = 0
        for ax, ay in [(bx-1, by), (bx+1, by), (bx, by-1), (bx, by+1)]:
            if 0 <= ax < ROWS and 0 <= ay < COLS:
                if grid[ax][ay] == 1:
                    winner = "IA"
                    game_over = True
                elif grid[ax][ay] == 2:
                    winner = "Jogador"
                    game_over = True
                grid[ax][ay] = 0
        player_has_bomb = True

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
player_x, player_y = random.randint(0, 9), random.randint(0, 9)
ia_x, ia_y = random.randint(0, 9), random.randint(0, 9)
grid[player_x][player_y] = 1
grid[ia_x][ia_y] = 2

max_paredes = random.randint(5, 15)
todas_paredes = False
while not todas_paredes:
    x, y = random.randint(0, 9), random.randint(0, 9)
    if grid[x][y] == 0:
        grid[x][y] = 3
        max_paredes -= 1
    if max_paredes == 0:
        todas_paredes = True
        

while running:
    screen.fill(WHITE)
    draw_hud()
    draw_grid()

    if game_over:
        draw_game_over()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if turn == "player" and event.type == pygame.KEYDOWN:
            if not player_moved:
                if event.key == pygame.K_w:
                    move_player(-1, 0)
                elif event.key == pygame.K_s:
                    move_player(1, 0)
                elif event.key == pygame.K_a:
                    move_player(0, -1)
                elif event.key == pygame.K_d:
                    move_player(0, 1)
            if event.key == pygame.K_UP:
                place_bomb(-1, 0)
            elif event.key == pygame.K_DOWN:
                place_bomb(1, 0)
            elif event.key == pygame.K_LEFT:
                place_bomb(0, -1)
            elif event.key == pygame.K_RIGHT:
                place_bomb(0, 1)
            elif event.key == pygame.K_SPACE:
                if turn == "player":
                    turn = "ia"
                    player_moved = False
                elif turn == "ia":
                    turn = "game"
                elif turn == "game":
                    turn = "player"
                #print("Passar turno: ", turn)
                break
            
        if turn == "ia":
            #print("Turno da IA")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #print("Passar turno: IA -> Game")
                    movimento = ia.a_star_search_avoid_4(grid, (ia_x, ia_y), (player_x, player_y))
                    print(movimento)
                    if movimento is not None:
                        grid[ia_x][ia_y] = 0
                        ia_x, ia_y = movimento
                        if grid[ia_x][ia_y] == 1:
                            winner = "IA"
                            game_over = True
                        grid[ia_x][ia_y] = 2
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
                    process_bombs()
                    #print("Passar turno: Game -> Player")
                    turn = "player"
                    break
    
    pygame.display.flip()
pygame.quit()
