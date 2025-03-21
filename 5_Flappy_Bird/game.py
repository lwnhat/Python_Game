import pygame, sys, random

# Hàm vẽ sàn
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))

# Hàm tạo ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos - 710))  # Giảm khoảng cách giữa hai ống
    return bottom_pipe, top_pipe

# Hàm di chuyển ống
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 3  # Giảm tốc độ di chuyển của ống
    return pipes

# Hàm vẽ ống
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# Hàm kiểm tra va chạm
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 650:
        return False
    return True

# Hàm xoay chim
def rotate_bird(bird1):
    return pygame.transform.rotozoom(bird1, -bird_movement * 2, 1)  # Giảm độ nghiêng khi bay

# Hàm animation chim
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

# Hiển thị điểm số
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        screen.blit(score_surface, (216, 100))
    if game_state == 'game_over':
        screen.blit(game_font.render(f'Score: {int(score)}', True, (255, 255, 255)), (150, 100))
        screen.blit(game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255)), (150, 630))

# Cập nhật điểm cao
def update_score(score, high_score):
    return max(score, high_score)

pygame.init()
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 35)

gravity = 0.35  # Tăng trọng lực để giảm khoảng cách bay
bird_movement = 0
game_active = True
score = 0
high_score = 0

# Tạo background
bg = pygame.image.load('assests/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

# Tạo sàn
floor = pygame.image.load('assests/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# Tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))

# Tạo timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 150)  # Giảm thời gian để bird thay đổi trạng thái nhanh hơn

# Tạo ống
pipe_surface = pygame.image.load('assests/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# Tạo timer ống
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1300)  # Tạo ống chậm hơn một chút
pipe_height = [250, 300, 350]  # Giảm khoảng cách ống

# Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assests/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216, 384))

# Chèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -8  # Giảm độ cao khi nhấn SPACE
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            bird_index = (bird_index + 1) % 3
            bird, bird_rect = bird_animation()

    screen.blit(bg, (0, 0))

    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(bird)
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

        score += 0.01
        score_display('main game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(100)  # Giữ tốc độ ổn định
