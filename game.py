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


# функция для загрузки картинки
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


# класс персонажа игры
class Doodle(pygame.sprite.Sprite):

    size = 33, 30

    def __init__(self, x, y, n_im=0):

        super().__init__(all_sprites)
        self.add(doodle)

        self.k_img = n_im

        self.list_img = doodle_imgs

        self.im1, self.im2 = self.list_img[self.k_img][::-1]
        self.image = self.im1

        self.rect = pygame.Rect((x, y), Doodle.size)
        self.y_jump = self.rect.top

        self.bool_up = False

    def change_img(self, n):
        self.k_img += n

        if self.k_img < 0:
            self.k_img += len(self.list_img)

        if self.k_img >= len(self.list_img):
            self.k_img -= len(self.list_img)

        self.im1, self.im2 = self.list_img[self.k_img][::-1]
        self.image = self.im1

    def update(self, *args):

        global counter, game, running, results

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

                if counter % 5 == 0:
                    platform_array.append(2)

                if counter % 10 == 0:
                    platform_array.append(1)

                self.y_jump = self.rect.top

        if self.rect.left < 0:
            self.rect.left = w

        if self.rect.left > w:
            self.rect.left = 0

        if self.rect.top > h or self.rect.top < -Doodle.size[1] * 0.75:

            game = False

            results.append(counter)
            results = sorted(results, reverse=True)

            with open('data/res.txt', 'w') as res:

                for i in range(len(results) - 1):
                    res.write(str(results[i]) + '\n')

                res.write(str(results[len(results) - 1]))


# класс обыкновенных платформ
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


# класс подвижных платформ
class Platform_Move(pygame.sprite.Sprite):
    def __init__(self, pos, x=100):

        super().__init__(all_sprites)
        self.add(platforms)

        size = x, 10
        self.image = load_image('platf1.png', -1)

        self.rect = pygame.Rect(pos, size)

        self.border = pos[0] - 60
        self.left = True

    def update(self, *args):

        self.rect.top += 1

        if self.left:

            self.rect.left -= 1

            if self.rect.left == self.border:

                self.border += 120
                self.left = False

        else:

            self.rect.left += 1

            if self.rect.left == self.border:

                self.border -= 120
                self.left = True

        if self.rect.top >= h:
            self.kill()


# класс облаков
class Cloud(pygame.sprite.Sprite):

    def __init__(self, im):

        super().__init__(clouds_init)
        self.image = im
        self.size = self.image.get_size()

        self.x, self.y = self.size
        x = random.randrange(0, w)
        y = random.randint(0, h - self.y)

        self.rect = pygame.Rect((x, y), self.size)

    def update(self, *args):

        self.rect.left += 1

        if self.rect.left > w:
            self.rect.left = - self.x


# класс для неподвижной платформы в меню
class Platform_menu(Platform):
    def update(self, *args):
        pass


color = pygame.Color('light blue')
screen.fill(color)
pygame.display.flip()


clock = pygame.time.Clock()
clock.tick(60)
ticks = 60

# загрузка фона в меню игры
menu_img = load_image('fon_doodle.png', -1)

# загрузка видов облаков
clouds_imgs = [load_image('cl1.png', -1), load_image('cl2.png', -1),
          load_image('cl3.png', -1), load_image('cl4.png', -1),
          load_image('cl5.png', -1), load_image('cl6.png', -1)]

start_btn = load_image('start.png')

s1 = 'dle_l'
s2 = 'dle_r'
doodle_imgs = []
i_img = 0

# загрузка всех скинов
for i in range(1, 9):

    a = load_image(s1 + f'{i}' + '.png', -1)
    b = load_image(s2 + f'{i}' + '.png', -1)
    doodle_imgs.append([a, b])

running = True

menu = False
game = True

# логические переменные, отвечающие за направление взгляда главного персонажа
k_left = False
k_right = False

# счетчики
count_pl = 0
counter = 0

# создание списка с номерами видов платформ
# для дальнейшего "рандома" и возможности усложнения игры
platform_array = [1 for _ in range(18)] + [2] + [3]

results = []

# чтение уже имеющихся результатов прошлых игр
with open('data/res.txt', 'r') as res:

    m = list(map(int, res.read().split('\n')))
    results = sorted(m, reverse=True)


font = pygame.font.SysFont('Arial', 25)
font1 = pygame.font.SysFont('Colibri', 50)

while running:

    menu = True

    all_sprites = pygame.sprite.Group()

    platforms = pygame.sprite.Group()
    doodle = pygame.sprite.Group()

    clouds = pygame.sprite.Group()
    clouds_init = pygame.sprite.Group()

    hero = Doodle(w // 2 - 20, 3 * h // 4 - 30, i_img)

    Platform_menu((w // 2 - 60, 3 * h // 4))

    k_clouds = 0

    # заполнение заднего плана облаками
    while k_clouds < 25:

        cl_i = Cloud(random.choice(clouds_imgs))

        while len(pygame.sprite.spritecollide(cl_i, clouds, False)) != 0:
            cl_i = Cloud(random.choice(clouds_imgs))

        clouds.add(cl_i)

        k_clouds += 1

    # цикл отрисовки главного меню игры и ожидания старта игры
    while menu:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                game = False
                running = False
                sys.exit()
            
            # смена картинки персонажа клвишей
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    hero.change_img(-1)
                    i_img = hero.k_img

                elif event.key == pygame.K_RIGHT:
                    hero.change_img(1)
                    i_img = hero.k_img

                else:
                    menu = False

            # смена картинки персонажа кнопкой мыши
            if event.type == pygame.MOUSEBUTTONDOWN:

                x, y = event.pos

                if 350 <= y <= 500 and 0 <= x <= 70:
                    hero.change_img(-1)
                    i_img = hero.k_img

                elif 350 <= y <= 500 and 330 <= x <= 400:
                    hero.change_img(1)
                    i_img = hero.k_img

                elif 200 <= x <= 400 and 0 <= y <= 230:
                    pass

                else:
                    menu = False

        screen.fill(color)

        clouds.draw(screen)
        all_sprites.draw(screen)

        # отрисовываем важные участки фона на первый план
        screen.blit(menu_img, (0, 0))
        screen.blit(start_btn, (w // 2 - 20, h // 2 - 20))

        txt1 = font.render('Score', False, (0, 0, 0))
        txt0 = font.render('№', False, (0, 0, 0))
        
        # номера в списке лидеров
        pos1 = font1.render('1', False, pygame.Color('gold'))
        pos2 = font1.render('2', False, pygame.Color('cornsilk2'))
        pos3 = font1.render('3', False, pygame.Color('darkorange'))
        
        # счет каждого из лидеров
        score1 = font1.render(str(results[0]), False, pygame.Color('gold'))
        score2 = font1.render(str(results[1]), False, pygame.Color('cornsilk2'))
        score3 = font1.render(str(results[2]), False, pygame.Color('darkorange'))

        screen.blit(txt1, (315, 12)) # текст топ-результатов
        screen.blit(txt0, (225, 12))

        screen.blit(pos1, (225, 65))
        screen.blit(pos2, (225, 120))
        screen.blit(pos3, (225, 175))

        screen.blit(score1, (315, 65))
        screen.blit(score2, (315, 120))
        screen.blit(score3, (315, 175))


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

    hero = Doodle(w // 2 - 20, 3 * h // 4 - 30, i_img)

    k_clouds = 0
    while k_clouds < 25:

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

    # цикл отрисовки игры и событий, связанных с ней
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

        # код, с помощью которого добавлена возможность
        # управления персонажен с зажатой клавишей на клавиатуре
        # (в модуль pygame не встроена)
        if k_left:
            hero.rect.left -= 2
        if k_right:
            hero.rect.left += 2

        count_pl += 1

        if count_pl == 60:

            i_pl = random.choice(platform_array)

            if i_pl == 1:
                Platform((random.randrange(0, w - 100), 0))

            else:
                Platform_Move((random.randrange(0, w - 100), 0))

            count_pl = 0

        screen.fill(color)

        clouds.draw(screen)
        all_sprites.draw(screen)

        clouds.update()
        all_sprites.update()

        pygame.display.flip()
        clock.tick(ticks)
