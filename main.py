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
    offset_x = obj2.x - obj.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60

    PLAYER_VEL = 5
    LASER_VEL = 5

    player_1 = Player_1(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))

        player_1.draw(WIN)

        if lost:
            lost_label = lost_font.render("You lost!!", 1, (255, 0, 0))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if player_1.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
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


main()
