import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 600, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Esquiva y Sobrevive")

# Cargar imagen del coche y de la bala
car_img = pygame.image.load("car.png")
car_img = pygame.transform.scale(car_img, (50, 50))  
bullet_img = pygame.Surface((5, 10))
bullet_img.fill((255, 0, 0))

# Cargar imagen de la nave enemiga
enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (30, 30))

# Jugador (coche)
car_rect = car_img.get_rect(center=(WIDTH // 2, HEIGHT - 50))
CAR_SPEED = 5

# Enemigos
enemies = []
ENEMY_SPEED = 3
ENEMY_FREQ = 50

# Balas
bullets = []
BULLET_SPEED = 10
MAX_BULLETS = 10  # Número máximo de balas permitidas
bullets_left = MAX_BULLETS  # Balas disponibles para el jugador

# Puntaje
score = 0
font = pygame.font.Font(None, 36)

# Colisiones
collisions = 0
MAX_COLLISIONS = 10  # Número máximo de colisiones permitidas

# Función para generar enemigos
def create_enemy():
    x = random.randint(0, WIDTH - 30)
    y = -30
    enemy_rect = enemy_img.get_rect(topleft=(x, y))
    enemies.append(enemy_rect)

# Función para mover y eliminar enemigos
def move_enemies():
    global score, collisions
    for enemy_rect in enemies:
        enemy_rect.y += ENEMY_SPEED
        if enemy_rect.y > HEIGHT:
            enemies.remove(enemy_rect)
            score += 5
        if enemy_rect.colliderect(car_rect):
            collisions += 1
            if collisions >= MAX_COLLISIONS:
                game_over("¡Haz perdido!")

# Función para crear balas
def create_bullet():
    global bullets_left
    if bullets_left > 0:
        bullet_rect = bullet_img.get_rect(midbottom=(car_rect.centerx, car_rect.top))
        bullets.append(bullet_rect)
        # Reduce las balas disponibles después de disparar
        bullets_left -= 1

# Función para mover y eliminar balas
def move_bullets():
    for bullet_rect in bullets:
        bullet_rect.y -= BULLET_SPEED
        if bullet_rect.bottom <= 0:
            bullets.remove(bullet_rect)

# Función principal del juego
def main_game():
    global score, bullets_left
    clock = pygame.time.Clock()
    enemy_spawn_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    create_bullet()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_rect.left > 0:
            car_rect.x -= CAR_SPEED
        if keys[pygame.K_RIGHT] and car_rect.right < WIDTH:
            car_rect.x += CAR_SPEED

        # Generar enemigos
        enemy_spawn_timer += 1
        if enemy_spawn_timer % ENEMY_FREQ == 0:
            create_enemy()
        
        # Actualizar movimiento de enemigos y balas
        move_enemies()
        move_bullets()

        # Detectar colisiones entre balas y enemigos
        for enemy_rect in enemies:
            for bullet_rect in bullets:
                if enemy_rect.colliderect(bullet_rect):
                    score += 10
                    enemies.remove(enemy_rect)
                    bullets.remove(bullet_rect)
                    bullets_left = min(bullets_left + 1, MAX_BULLETS)  # Recupera una bala después de acertar un enemigo

        # Verificar si se ha alcanzado la puntuación de victoria
        if score >= 1000:
            game_over("¡Has ganado, haz llegado a 1000 puntos!")

        # Dibujar elementos en pantalla
        WIN.fill((0, 0, 0))
        WIN.blit(car_img, car_rect)
        for enemy_rect in enemies:
            WIN.blit(enemy_img, enemy_rect)
        for bullet_rect in bullets:
            WIN.blit(bullet_img, bullet_rect)

        # Mostrar puntaje y balas restantes
        score_text = font.render(f"Puntaje: {score}", True, (255, 255, 255))
        bullets_text = font.render(f"Balas: {bullets_left}/{MAX_BULLETS}", True, (255, 255, 255))
        WIN.blit(score_text, (10, 10))
        WIN.blit(bullets_text, (10, 50))

        pygame.display.update()
        clock.tick(60)  # 60 FPS

# Función para mostrar el mensaje de fin de juego
def game_over(message):
    font_big = pygame.font.Font(None, 72)
    text = font_big.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WIN.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)  # Espera 2 segundos antes de salir
    pygame.quit()
    sys.exit()

# Función principal
def main():
    main_game()

if __name__ == "__main__":
    main()
