import pygame
import time
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана
screen_width = 1600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dino Game")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_COLOR = (83, 83, 83)
DINO_COLOR = (0, 255, 0)  # Зеленый цвет для динозавра
OBSTACLE_COLOR = (255, 0, 0)  # Красный цвет для наземных объектов

# Параметры Дино
dino_width = 40
dino_height = 60
dino_x = 50
dino_y = screen_height - dino_height - 50
dino_velocity = 10
dino_jump_height = 9
is_jumping = False
jump_count = dino_jump_height
is_ducking = False
dino_crouch_height = 30

# Параметры препятствия
obstacle_width = 20
obstacle_height = 40
obstacle_x = screen_width
obstacle_y = screen_height - obstacle_height - 50
obstacle_velocity = 10
initial_obstacle_velocity = 10
obstacles = []

# Основной цикл игры
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)
start_time = time.time()

# Флаги игры
game_over = False

# Счетчики
score = 0
high_score = 0


def draw_dino(x, y, crouching):
    if crouching:
        pygame.draw.rect(screen, DINO_COLOR,
                         (x, y + (dino_height - dino_crouch_height), dino_width, dino_crouch_height))
    else:
        pygame.draw.rect(screen, DINO_COLOR, (x, y, dino_width, dino_height))


def draw_obstacle(x, y):
    pygame.draw.rect(screen, OBSTACLE_COLOR, (x, y, obstacle_width, obstacle_height))


def display_score(score):
    value = font.render(f"Score: {int(score)}", True, BLACK)
    screen.blit(value, [10, 10])


def display_high_score(high_score):
    value = font.render(f"High Score: {int(high_score)}", True, BLACK)
    screen.blit(value, [10, 50])


def show_game_over(score, high_score):
    if score > high_score:
        high_score = score  # Обновляем high_score, если текущий счет превышает предыдущий максимум
    game_over_font = pygame.font.SysFont(None, 70)
    game_over_text = game_over_font.render("Game Over", True, BLACK)
    score_text = font.render(f"Score: {int(score)}", True, BLACK)
    high_score_text = font.render(f"High Score: {int(high_score)}", True, BLACK)
    screen.blit(game_over_text, [screen_width / 2 - 150, screen_height / 2 - 50])
    screen.blit(score_text, [screen_width / 2 - 100, screen_height / 2 + 50])
    screen.blit(high_score_text, [screen_width / 2 - 150, screen_height / 2 + 100])
    restart_text = font.render("Press R to restart", True, BLACK)
    screen.blit(restart_text, [screen_width / 2 - 150, screen_height / 2 + 150])
    pygame.display.update()


collision = False  # Переменная для отслеживания столкновений

# Внутри основного цикла игры
try:
    while running:
        clock.tick(60)  # 60 FPS
        screen.fill(WHITE)  # Заливаем экран белым цветом

        # Рисуем фон и землю
        pygame.draw.rect(screen, GROUND_COLOR, [0, screen_height - 50, screen_width, 50])

        if not game_over:  # Проверяем, активна ли игра
            # Рисуем препятствие и динозавра
            draw_obstacle(obstacle_x, obstacle_y)
            draw_dino(dino_x, dino_y, is_ducking)

            # Рисуем счет и предыдущий рекорд
            display_score(score)
            display_high_score(high_score)
        else:
            # Рисуем сообщение о проигрыше
            show_game_over(score, high_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:  # Перезапуск игры по нажатию клавиши R после завершения игры
                    # Сброс всех значений и переменных
                    game_over = False
                    obstacle_x = screen_width
                    start_time = time.time()
                    dino_y = screen_height - dino_height - 50
                    is_jumping = False
                    is_ducking = False
                    jump_count = dino_jump_height
                    obstacle_velocity = initial_obstacle_velocity
                    score = 0  # Сброс счетчика очков
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if game_over:  # Начать новую игру, если игра завершена и была нажата клавиша прыжка
                        # Сброс всех значений и переменных
                        game_over = False
                        obstacle_x = screen_width
                        start_time = time.time()
                        dino_y = screen_height - dino_height - 50
                        is_jumping = False
                        is_ducking = False
                        jump_count = dino_jump_height
                        obstacle_velocity = initial_obstacle_velocity
                        score = 0  # Сброс счетчика очков
                if event.key == pygame.K_DOWN:
                    is_ducking = True
                else:
                    is_ducking = False

        keys = pygame.key.get_pressed()
        if not is_jumping:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                is_jumping = True
                is_ducking = False
            elif keys[pygame.K_DOWN]:
                is_ducking = True
            else:
                is_ducking = False

        if is_jumping:
            if jump_count >= -dino_jump_height:
                neg = 1
                if jump_count < 0:
                    neg = -1
                dino_y -= (jump_count ** 2) * 0.5 * neg
                jump_count -= 1
            else:
                is_jumping = False
                jump_count = dino_jump_height

        obstacle_x -= obstacle_velocity

        if obstacle_x < -obstacle_width:
            obstacle_x = screen_width

        if not game_over:  # Обновляем счетчик очков только если игра активна
            # Обновление счёта в зависимости от времени
            elapsed_time = time.time() - start_time
            score = elapsed_time * 10  # Коэффициент для увеличения скорости набора очков

            # Ускорение игры со временем
            obstacle_velocity = initial_obstacle_velocity + (elapsed_time // 5)  # Увеличение скорости каждые 5 секунд

        draw_obstacle(obstacle_x, obstacle_y)
        if dino_x + dino_width > obstacle_x and dino_x < obstacle_x + obstacle_width:
            if dino_y + dino_height > obstacle_y:
                if not is_ducking or (is_ducking and dino_y + dino_crouch_height > obstacle_y):
                    game_over = True  # Устанавливаем флаг завершения игры

        draw_dino(dino_x, dino_y, is_ducking)

        # Отображение счета и предыдущего рекорда
        display_score(score)
        display_high_score(high_score)

        # Отображение сообщения о проигрыше, если игра завершена
        if game_over:
            high_score = max(high_score, score)
            show_game_over(score, high_score)

        pygame.display.update()
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    pygame.quit()
