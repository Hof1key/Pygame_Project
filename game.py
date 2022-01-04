import random
import pygame
import sys
import os

pygame.init()
size = w, h = 400, 600
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
doodle = pygame.sprite.Group()



def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    try:
        image = pygame.image.load(fullname)
    except pygame.error as msg:
        print('!')
        raise SystemExit(msg)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Doodle(pygame.sprite.Sprite):
    size = 33, 30
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(doodle)
        '''self.image = pygame.Surface(Doodle.size)
        self.image.fill(pygame.Color('yellow'))
        self.rect = pygame.Rect((x, y), Doodle.size)'''
        self.im1 = load_image('dle_r.png')
        self.im2 = load_image('dle_l.png')
        self.image = self.im1
        self.rect = pygame.Rect((x, y), Doodle.size)
        self.y_jump = self.rect.top
        self.bool_up = False

    def update(self, *args):
        global counter
        if self.bool_up:
            self.rect.top -= 2
            if self.rect.top + 80 <= self.y_jump:
                self.bool_up = False
        else:
            if len(pygame.sprite.groupcollide(doodle, platforms, False, False)) == 0:
                self.rect.top += 3
            else:
                self.bool_up = True
                counter += 1
                self.y_jump = self.rect.top
        if self.rect.left < 0:
            self.rect.left += w
        if self.rect.left > w:
            self.rect.left -= w
        if self.rect.top > h:
            game = False
            sys.exit()


class Platform(pygame.sprite.Sprite):

    def __init__(self, pos, x=100):
        super().__init__(all_sprites)
        self.add(platforms)
        size = x, 10
        self.image = load_image('platf.png')
        self.rect = pygame.Rect(pos, size)
        if self.rect.left > w - 100:
            Platform((0, pos[1]), 100 - w + self.rect.left)

    def update(self, *args):
        self.rect.top += 1
        if self.rect.top >= h:
            self.kill()


color = pygame.Color('light blue')
screen.fill(color)
pygame.display.flip()


clock = pygame.time.Clock()
clock.tick(60)

hero = Doodle(w // 2 - 10, 3 * h // 4 - 10)

y_pl = 3 * h // 4 - 21
Platform((w // 2 - 60, 3 * h // 4 + 9))
while y_pl > 0:
    Platform((random.randrange(0, w - 100), y_pl))
    y_pl -= 60
running = True
k_left = False
k_right = False
game = True
count_pl = 0
ticks = 60
counter = 0
while running:
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    hero.rect.left -= 10
                    k_left = True
                    hero.image = hero.im2
                if event.key == pygame.K_RIGHT:
                    hero.rect.left += 10
                    k_right = True
                    hero.image = hero.im1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    k_left = False
                if event.key == pygame.K_RIGHT:
                    k_right = False
        if k_left:
            hero.rect.left -= 2
        if k_right:
            hero.rect.left += 2
        count_pl += 1
        if count_pl == 60:
            Platform((random.randrange(0, w - 100), 0))
            count_pl = 0
        screen.fill(color)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(ticks)

    # завершение работы:
    pygame.quit()
