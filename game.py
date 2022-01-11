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
clouds = pygame.sprite.Group()



def load_image(name, colorkey=None):
    fullname = os.path.join('data/' + name)
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
        self.k_img = 0
        list_img = doodle_imgs[self.k_img]
        self.im1, self.im2 = list_img[::-1]
        self.image = self.im1
        self.rect = pygame.Rect((x, y), Doodle.size)
        self.y_jump = self.rect.top
        self.bool_up = False

    def update(self, *args):
        global counter, game, running
        if self.bool_up:
            self.rect.top -= 2
            if self.rect.top + 90 <= self.y_jump:
                self.bool_up = False
        else:
            if len(pygame.sprite.groupcollide(doodle, platforms, False, False)) == 0:
                self.rect.top += 3
            else:
                self.rect.top += 3
                self.bool_up = True
                counter += 1
                self.y_jump = self.rect.top
        if self.rect.left < 0:
            self.rect.left += w
        if self.rect.left > w:
            self.rect.left -= w

        if self.rect.top > h or self.rect.top < -Doodle.size[1] * 0.75:
            game = False


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


class Cloud(pygame.sprite.Sprite):

    def __init__(self, im):

        super().__init__(clouds_init)
        self.image = im
        self.size = self.image.get_size()

        self.x, self.y = self.size
        x = random.randrange(0, w - self.x)
        y = random.randint(0, h - self.y)

        self.rect = pygame.Rect((x, y), self.size)

    def update(self, *args):

        self.rect.left += 1
        if self.rect.left > w - self.x // 2:
            self.rect.left = - self.x // 2


class Platform_menu(Platform):
    def update(self, *args):
        pass


color = pygame.Color('light blue')
screen.fill(color)
pygame.display.flip()


clock = pygame.time.Clock()
clock.tick(60)
ticks = 60

menu_img = load_image('fon_doodle.png', -1)
clouds_imgs = [load_image('cl1.png', -1), load_image('cl2.png', -1),
          load_image('cl3.png', -1), load_image('cl4.png', -1),
          load_image('cl5.png', -1), load_image('cl6.png', -1)]
start_btn = load_image('start.png')

s1 = 'dle_l'
s2 = 'dle_r'
doodle_imgs = []
for i in range(1, 9):
    a = load_image(s1 + f'{i}' + '.png', -1)
    b = load_image(s2 + f'{i}' + '.png', -1)
    doodle_imgs.append([a, b])
running = True
menu = False
game = True

k_left = False
k_right = False

count_pl = 0
counter = 0

while running:

    menu = True

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    doodle = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    clouds_init = pygame.sprite.Group()

    hero = Doodle(w // 2 - 20, 3 * h // 4 - 30)

    Platform_menu((w // 2 - 60, 3 * h // 4))

    k_clouds = 0
    while k_clouds < 20:
        cl_i = Cloud(random.choice(clouds_imgs))
        while len(pygame.sprite.spritecollide(cl_i, clouds, False)) != 0:
            cl_i = Cloud(random.choice(clouds_imgs))
        clouds.add(cl_i)
        k_clouds += 1

    while menu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                running = False
                sys.exit()

            if event.type == pygame.KEYDOWN:
                menu = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                menu = False

        screen.fill(color)

        clouds.draw(screen)
        all_sprites.draw(screen)


        screen.blit(menu_img, (0, 0))
        screen.blit(start_btn, (w // 2 - 20, h // 2 - 20))

        clouds.update()
        all_sprites.update()

        pygame.display.flip()
        clock.tick(ticks)

    game = True

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    doodle = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    clouds_init = pygame.sprite.Group()

    hero = Doodle(w // 2 - 20, 3 * h // 4 - 30)

    k_clouds = 0
    while k_clouds < 20:
        cl_i = Cloud(random.choice(clouds_imgs))
        while len(pygame.sprite.spritecollide(cl_i, clouds, False)) != 0:
            cl_i = Cloud(random.choice(clouds_imgs))
        clouds.add(cl_i)
        k_clouds += 1

    y_pl = 3 * h // 4 - 60

    Platform((w // 2 - 60, y_pl + 60))

    while y_pl > 0:
        Platform((random.randrange(0, w - 100), y_pl))
        y_pl -= 60

    while game:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game = False
                running = False
                sys.exit()

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

        clouds.draw(screen)
        all_sprites.draw(screen)

        clouds.update()
        all_sprites.update()

        pygame.display.flip()
        clock.tick(ticks)
