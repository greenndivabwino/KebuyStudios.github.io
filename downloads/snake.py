import pygame
import random
import time
import sys
import os 

# -----------------------------------------------------------
# 1. INIZIALIZZAZIONE GLOBALE E VARIABILI
# -----------------------------------------------------------
pygame.init()
pygame.mixer.init() 

# Definizione dei colori (RGB)
NERO = (0, 0, 0)
GRIGIO_SCURO = (100, 100, 100)
ROSSO_SANGUE = (150, 0, 0)
VERDE_BRILLANTE = (0, 200, 0)
ORO = (255, 215, 0)
BIANCO = (255, 255, 255)

# Dimensioni totali della finestra
win_larghezza = 1024
win_altezza = 768
dis = pygame.display.set_mode((win_larghezza, win_altezza), pygame.RESIZABLE)
pygame.display.set_caption('Mega Snake Game - WASD e Freccette')

# Variabili dei file (percorso delle risorse in PyInstaller)
SFONDO_FILE = 'snake-game.png'
MUSIC_FILE = 'music.mp3'

# Funzione per ottenere il percorso delle risorse in ambiente PyInstaller
def resource_path(relative_path):
    """ Ottiene il percorso assoluto della risorsa, funziona sia in sviluppo che in PyInstaller. """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Caricamento dello sfondo
try:
    sfondo_img = pygame.image.load(resource_path(SFONDO_FILE)).convert()
    sfondo_img = pygame.transform.scale(sfondo_img, (win_larghezza, win_altezza))
except pygame.error:
    sfondo_img = None 

# Caricamento della musica
try:
    pygame.mixer.music.load(resource_path(MUSIC_FILE))
except pygame.error:
    pass

# Variabili del gioco
snake_block = 10 
snake_speed = 12 # NUOVA VELOCITÀ: Leggermente più lenta
game_larghezza = 800 
game_altezza = 600
game_x_offset = (win_larghezza - game_larghezza) // 2
game_y_offset = (win_altezza - game_altezza) // 2

clock = pygame.time.Clock()
font_stile = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 30)

# -----------------------------------------------------------
# 2. FUNZIONI AUSILIARIE (Lasciate invariate)
# -----------------------------------------------------------

def IlTuoPunteggio(score):
    value = score_font.render("PUNTEGGIO: " + str(score), True, BIANCO)
    dis.blit(value, [game_x_offset, 10]) 

def il_serpente(snake_block, snake_list):
    pygame.draw.rect(dis, (0, 100, 0), [snake_list[-1][0], snake_list[-1][1], snake_block, snake_block])
    for x in snake_list[:-1]:
        pygame.draw.rect(dis, VERDE_BRILLANTE, [x[0], x[1], snake_block, snake_block])

def messaggio(msg, color):
    mesg = font_stile.render(msg, True, color)
    test_rect = mesg.get_rect(center=(win_larghezza / 2, win_altezza / 2))
    dis.blit(mesg, test_rect)

def disegna_bordo_gioco():
    rect_gioco = pygame.Rect(game_x_offset, game_y_offset, game_larghezza, game_altezza)
    pygame.draw.rect(dis, GRIGIO_SCURO, rect_gioco, 5)

def genera_cibo(snake_list):
    while True:
        foodx = round(random.randrange(game_x_offset, game_x_offset + game_larghezza - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(game_y_offset, game_y_offset + game_altezza - snake_block) / snake_block) * snake_block
        if [foodx, foody] not in snake_list:
            return foodx, foody

# -----------------------------------------------------------
# 3. CICLO DI GIOCO PRINCIPALE
# -----------------------------------------------------------

def gameLoop():
    global dis, win_larghezza, win_altezza, game_x_offset, game_y_offset, sfondo_img 

    # Avvia la musica all'inizio del gioco
    if pygame.mixer.music.get_busy() == False and MUSIC_FILE:
         pygame.mixer.music.play(-1)
         
    game_over = False
    game_close = False

    x1 = round((game_x_offset + game_larghezza / 2) / snake_block) * snake_block
    y1 = round((game_y_offset + game_altezza / 2) / snake_block) * snake_block

    x1_change = 0
    y1_change = -snake_block 

    snake_List = []
    lunghezza_serpente = 4 

    for i in range(lunghezza_serpente):
        snake_List.append([x1, y1 + (i * snake_block)])

    foodx, foody = genera_cibo(snake_List)

    while not game_over:

        # --- Ciclo Game Over ---
        while game_close == True:
            pygame.mixer.music.stop() 
            
            dis.blit(sfondo_img, (0, 0)) 
            s = pygame.Surface((game_larghezza, game_altezza), pygame.SRCALPHA)
            s.fill((0, 51, 102, 180)) 
            dis.blit(s, (game_x_offset, game_y_offset)) 
            
            disegna_bordo_gioco()
            
            IlTuoPunteggio(lunghezza_serpente - 4)
            messaggio("GAME OVER! Premi C per Riprovare o Q per Uscire", ROSSO_SANGUE)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop() 

        # 1. Gestione degli Eventi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            
            if event.type == pygame.VIDEORESIZE:
                win_larghezza, win_altezza = event.size
                dis = pygame.display.set_mode((win_larghezza, win_altezza), pygame.RESIZABLE)
                
                try:
                    sfondo_img = pygame.image.load(resource_path(SFONDO_FILE)).convert()
                    sfondo_img = pygame.transform.scale(sfondo_img, (win_larghezza, win_altezza))
                except:
                    pass
                    
                game_x_offset = (win_larghezza - game_larghezza) // 2
                game_y_offset = (win_altezza - game_altezza) // 2

            if event.type == pygame.KEYDOWN:
                # --- SUPPORTO WASD e FRECCETTE ---
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
        
        # 2. Logica di Gioco e Collisioni
        if (x1 < game_x_offset or x1 >= game_x_offset + game_larghezza or 
            y1 < game_y_offset or y1 >= game_y_offset + game_altezza):
            game_close = True

        x1 += x1_change
        y1 += y1_change
        
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        
        if len(snake_List) > lunghezza_serpente:
            del snake_List[0] 

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        if x1 == foodx and y1 == foody:
            foodx, foody = genera_cibo(snake_List)
            lunghezza_serpente += 1

        # 3. Disegno
        dis.blit(sfondo_img, (0, 0)) 
        
        s = pygame.Surface((game_larghezza, game_altezza), pygame.SRCALPHA)
        s.fill((0, 51, 102, 180)) 
        dis.blit(s, (game_x_offset, game_y_offset)) 

        disegna_bordo_gioco()
        pygame.draw.rect(dis, ORO, [foodx, foody, snake_block, snake_block])

        il_serpente(snake_block, snake_List)
        IlTuoPunteggio(lunghezza_serpente - 4) 

        pygame.display.update()
        clock.tick(snake_speed) # Usa la nuova velocità (12 FPS)

    pygame.quit()
    sys.exit()

# Avvia il gioco!
gameLoop()