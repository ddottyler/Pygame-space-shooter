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

    def __init__(self, x, y, health=100)
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


class Laser:
    def __init__(self, x, y, img)
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


def main():
    run = True
    FPS = 60

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


main()
