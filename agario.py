import pygame
import random
import math

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu i pola gry
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800  # Zwiększenie rozdzielczości ekranu
GAME_WIDTH, GAME_HEIGHT = 1600, 1200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Agar.io Clone - Fixed Consumption")

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Ustawienia graczy
player1 = {"x": GAME_WIDTH // 3, "y": GAME_HEIGHT // 3, "radius": 20, "speed": 5, "score": 0, "color": BLUE, "invincible": 180}
player2 = {"x": 2 * GAME_WIDTH // 3, "y": 2 * GAME_HEIGHT // 3, "radius": 20, "speed": 5, "score": 0, "color": GREEN, "invincible": 180}

# Kulki AI
AI_COUNT = 5
ai_balls = [
    {"x": random.randint(50, GAME_WIDTH - 50), "y": random.randint(50, GAME_HEIGHT - 50),
     "radius": random.randint(10, 40), "color": RED, "speed": random.uniform(1.5, 3), "score": 0}
    for _ in range(AI_COUNT)
]

# Bonusy
BONUS_COUNT = 5
bonuses = [
    {"x": random.randint(50, GAME_WIDTH - 50), "y": random.randint(50, GAME_HEIGHT - 50), "radius": 10, "color": YELLOW}
    for _ in range(BONUS_COUNT)
]

# Funkcja do rysowania okręgu
def draw_circle(x, y, radius, color, offset_x, offset_y):
    pygame.draw.circle(screen, color, (int(x - offset_x), int(y - offset_y)), int(radius))

# Funkcja kolizji
def is_collision(x1, y1, r1, x2, y2, r2):
    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance < r1 + r2

# AI zachowanie
def move_ai(ai):
    # Szukanie najbliższego celu (innej kulki lub bonusu)
    target = find_nearest_target(ai)
    if target:
        dx = target["x"] - ai["x"]
        dy = target["y"] - ai["y"]
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            ai["x"] += ai["speed"] * (dx / distance)
            ai["y"] += ai["speed"] * (dy / distance)

    # Granice pola gry
    ai["x"] = max(ai["radius"], min(ai["x"], GAME_WIDTH - ai["radius"]))
    ai["y"] = max(ai["radius"], min(ai["y"], GAME_HEIGHT - ai["radius"]))

# Znajdź najbliższy cel (AI, bonus, gracz)
def find_nearest_target(ai):
    nearest = None
    min_distance = float('inf')
    targets = ai_balls + bonuses + [player1, player2]
    for target in targets:
        if target is not ai and target["radius"] < ai["radius"]:
            dx = target["x"] - ai["x"]
            dy = target["y"] - ai["y"]
            distance = math.sqrt(dx**2 + dy**2)
            if distance < min_distance:
                min_distance = distance
                nearest = target
    return nearest

# Pochłanianie obiektów
def handle_consumption(player, targets):
    global ai_balls, bonuses
    for target in targets[:]:  # Tworzymy kopię, aby modyfikować listę
        if is_collision(player["x"], player["y"], player["radius"], target["x"], target["y"], target["radius"]):
            if player["radius"] > target["radius"]:  # Gracz większy, pochłania cel
                player["radius"] += target["radius"] // 2
                player["score"] += 10
                if target in ai_balls:
                    ai_balls.remove(target)
                elif target in bonuses:
                    bonuses.remove(target)

# Funkcja rysująca tabelę wyników
def draw_scoreboard():
    font = pygame.font.SysFont(None, 30)
    player1_score = font.render(f"Player 1: {player1['score']}", True, BLACK)
    player2_score = font.render(f"Player 2: {player2['score']}", True, BLACK)
    screen.blit(player1_score, (10, 10))
    screen.blit(player2_score, (10, 40))

    # Wyświetlanie wyników AI
    for i, ai in enumerate(ai_balls):
        ai_score = font.render(f"AI {i+1}: {ai['score']}", True, BLACK)
        screen.blit(ai_score, (10, 80 + i * 30))

# Główna pętla gry
running = True
clock = pygame.time.Clock()
offset_x, offset_y = 0, 0  # Przesunięcie kamery dla gracza 1

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Sterowanie gracza 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1["y"] - player1["radius"] > 0:
        player1["y"] -= player1["speed"]
    if keys[pygame.K_s] and player1["y"] + player1["radius"] < GAME_HEIGHT:
        player1["y"] += player1["speed"]
    if keys[pygame.K_a] and player1["x"] - player1["radius"] > 0:
        player1["x"] -= player1["speed"]
    if keys[pygame.K_d] and player1["x"] + player1["radius"] < GAME_WIDTH:
        player1["x"] += player1["speed"]

    # Sterowanie gracza 2
    if keys[pygame.K_UP] and player2["y"] - player2["radius"] > 0:
        player2["y"] -= player2["speed"]
    if keys[pygame.K_DOWN] and player2["y"] + player2["radius"] < GAME_HEIGHT:
        player2["y"] += player2["speed"]
    if keys[pygame.K_LEFT] and player2["x"] - player2["radius"] > 0:
        player2["x"] -= player2["speed"]
    if keys[pygame.K_RIGHT] and player2["x"] + player2["radius"] < GAME_WIDTH:
        player2["x"] += player2["speed"]

    # Obsługa pochłaniania
    handle_consumption(player1, ai_balls + bonuses)
    handle_consumption(player2, ai_balls + bonuses)

    # Rysowanie graczy
    for player in [player1, player2]:
        draw_circle(player["x"], player["y"], player["radius"], player["color"], offset_x, offset_y)

    # Rysowanie i aktualizacja AI
    for ai in ai_balls[:]:
        draw_circle(ai["x"], ai["y"], ai["radius"], ai["color"], offset_x, offset_y)
        move_ai(ai)

    # Rysowanie bonusów
    for bonus in bonuses:
        draw_circle(bonus["x"], bonus["y"], bonus["radius"], bonus["color"], offset_x, offset_y)

    # Rysowanie tabeli wyników
    draw_scoreboard()

    # Aktualizacja ekranu
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
