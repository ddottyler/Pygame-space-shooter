import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Load images

# PLAYER 1
PLAYER_1 = pygame.image.load(os.path.join("assets", "blue.png"))
PLAYER_1_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_blue.png"))

# PLAYER 2
PLAYER_2 = pygame.image.load(os.path.join("assets", "yellow.png"))
PLAYER_2_LASER = pygame.image.load(
    os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "background.png")), (WIDTH, HEIGHT))

# CONSTANTS
REDUCE_HEALTH = 10


class Player:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.player_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.player_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= REDUCE_HEALTH
                self.lasers.remove(laser)

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.player_img.get_width()

    def get_height(self):
        return self.player_img.get_height()


class Player_1(Player):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.player_img = PLAYER_1
        self.laser_img = PLAYER_1_LASER
        self.mask = pygame.mask.from_surface(self.player_img)
        self.max_health = health

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                         self.player_img.get_height() + 10, self.player_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.player_img.get_height() +
                         10, self.player_img.get_width() * (self.health/self.max_health), 10))


class Player_2(Player):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.player_img = PLAYER_2
        self.laser_img = PLAYER_2_LASER
        self.mask = pygame.mask.from_surface(self.player_img)
        self.max_health = health

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                         self.player_img.get_height() + 10, self.player_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.player_img.get_height() +
                         10, self.player_img.get_width() * (self.health/self.max_health), 10))


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(obj, self)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60

    lost_font = pygame.font.SysFont("bahnschrift", 80)

    PLAYER_VEL = 5
    LASER_VEL = 5

    player_1 = Player_1(320, 600)
    player_2 = Player_2(320, 70)

    clock = pygame.time.Clock()

    p1_lost = False
    p2_lost = False
    p1_lost_count = 0
    p2_lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))

        player_1.draw(WIN)
        player_2.draw(WIN)

        if p1_lost:
            lost_label = lost_font.render(
                "Player 2 won!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        if p2_lost:
            lost_label = lost_font.render(
                "Player 1 won!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if player_1.health <= 0:
            p1_lost = True
            p1_lost_count += 1

        if player_2.health <= 0:
            p2_lost = True
            p2_lost_count += 1

        if p1_lost:
            if p1_lost_count > FPS * 3:
                run = False
            else:
                continue

        if p2_lost:
            if p2_lost_count > FPS * 3:
                run = False
            else:
                continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        # player 1
        if keys[pygame.K_LEFT] and player_1.x - PLAYER_VEL > 0:  # left
            player_1.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player_1.x + PLAYER_VEL + player_1.get_width() < WIDTH:  # right
            player_1.x += PLAYER_VEL
        if keys[pygame.K_UP] and player_1.y - PLAYER_VEL > 0:  # up
            player_1.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player_1.y + PLAYER_VEL + player_1.get_height() + 15 < HEIGHT:  # down
            player_1.y += PLAYER_VEL
        if keys[pygame.K_SPACE]:
            player_1.shoot()
        # player 2
        if keys[pygame.K_a] and player_2.x - PLAYER_VEL > 0:  # left
            player_2.x -= PLAYER_VEL
        if keys[pygame.K_d] and player_2.x + PLAYER_VEL + player_2.get_width() < WIDTH:  # right
            player_2.x += PLAYER_VEL
        if keys[pygame.K_w] and player_2.y - PLAYER_VEL > 0:  # up
            player_2.y -= PLAYER_VEL
        if keys[pygame.K_s] and player_2.y + PLAYER_VEL + player_2.get_height() + 15 < HEIGHT:  # down
            player_2.y += PLAYER_VEL
        if keys[pygame.K_f]:
            player_2.shoot()

        player_1.move_lasers(-LASER_VEL, player_2)
        player_2.move_lasers(LASER_VEL, player_1)


def main_menu():
    title_font = pygame.font.SysFont("bahnschrift", 70)
    instruction_font = pygame.font.SysFont("bahnschrift", 30)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        p1_instruction_label = instruction_font.render(
            "Player 1: Use arrow keys to move and spacebar to shoot", 1, (255, 255, 255))
        p2_instruction_label = instruction_font.render(
            "Player 2: Use a, w, s, d keys to move and f key to shoot", 1, (255, 255, 255))
        title_label = title_font.render(
            "Press the mouse to begin...", 1, (255, 255, 255))
        WIN.blit(p1_instruction_label, (WIDTH/2 -
                 p1_instruction_label.get_width()/2, 670))
        WIN.blit(p2_instruction_label, (WIDTH/2 -
                 p2_instruction_label.get_width()/2, 710))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()
