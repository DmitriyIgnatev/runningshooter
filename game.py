import pygame
import time
import os
import sys
import random


def change():
    f1 = open('data/map.txt', mode='w', encoding='utf-8')
    flag = False
    number_player = random.randint(1, 14)
    number_player_more = random.randint(1, 20)
    zombies = random.randint(2, 7)
    zombies_coords = [(random.randint(1, 14), random.randint(1, 20)) for i in range(zombies)]
    houses = [(random.randint(1, 14), random.randint(1, 20)) for i in range(2)]
    count = 0
    maps = []
    count_more = 0
    for i in range(14):
        a = ''
        if count != number_player:
            for j in range(20):
                g = random.choice(['#', '.'])
                a += g
        else:
            for j in range(20):
                if number_player_more == count_more:
                    g = '@'
                    a += g
                else:
                    g = random.choice(['#', '.'])
                    a += g
                count_more += 1
        count += 1
        maps.append(a + '\n')
    for i in zombies_coords:
        try:
            a = list(maps[i[0]])
            if a[i[1]] == '@':
                continue
            else:
                a[i[1]] = 'z'
                maps[i[0]] = a
        except:
            continue
    for i in houses:
        try:
            a = list(maps[i[0]])
            if a[i[1]] == '@':
                continue
            else:
                a[i[1]] = random.choice(['h', 'c'])
                maps[i[0]] = a
        except:
            continue
    for i in maps:
        f1.write(''.join(i))


change()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def generate_level(level):
    player, x, y, zombie = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('grow', x, y, 0)
            elif level[y][x] == '.':
                Tile('grow', x, y, 1)
            elif level[y][x] == '@':
                Tile('grow', x, y, 0)
                player = Player(y, x)
                all_sprites.add(player)
            elif level[y][x] == 'z':
                Tile('grow', x, y, 1)
                mon.add(Monsters(y, x))
            elif level[y][x] == 'h':
                Tile('grow', x, y, 1)
                ho = Block('house', x, y, 200)
                block_group.add(ho)
            elif level[y][x] == 'c':
                Tile('grow', x, y, 1)
                ho = Block('cfhfq', x, y, 300)
                block_group.add(ho)
    return player, x, y, ho


tile_images = {'grow': [load_image('brick1.jpg'), load_image('brick2.jpg')], 'house': load_image('house.png'), 'cfhfq': load_image('cfhfq.png')}

all_sprites = pygame.sprite.Group()
SIZE = 100
size_monster = 70
tile_width = tile_height = 50
tiles_group = pygame.sprite.Group()
bullet = pygame.sprite.Group()
mon = pygame.sprite.Group()
block_group = pygame.sprite.Group()


class Block(pygame.sprite.Sprite):
    def __init__(self, name, y, x, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(tile_images[name], (size, size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x * 55
        self.rect.y = y * 30


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, a):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type][a]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(bullet)
        if pos[2] == 0 or pos[2] == 2:
            self.image = pygame.Surface((25, 5))
        else:
            self.image = pygame.Surface((5, 25))
        self.image.fill('yellow')
        self.rect = self.image.get_rect()
        if pos[2] == 0 or pos[2] == 2:
            self.rect.x = pos[0] + 15
            self.rect.y = pos[1] + 49
        else:
            self.rect.x = pos[0] + 40
            self.rect.y = pos[1] + 49
        self.pos = pos

    def x(self):
        if self.pos[2] == 0:
            self.rect = self.rect.move(20, 0)
        if self.pos[2] == 1:
            self.rect = self.rect.move(0, 20)
        if self.pos[2] == 2:
            self.rect = self.rect.move(-20, 0)
        if self.pos[2] == 3:
            self.rect = self.rect.move(0, -20)

    def dellete(self):
        if self.rect.x >= 1000 or self.rect.x <= 0 or self.rect.y >= 700 or self.rect.y <= 0:
            return True


class Monsters(pygame.sprite.Sprite):
    def __init__(self, y, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(f'data/zom1.png'), (size_monster, size_monster))
        self.rect = self.image.get_rect()
        self.rect.x = x * 50
        self.rect.y = y * 50
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 3
        self.index_animation = 1
        self.flag = False
        self.anim_right = [
            pygame.transform.scale(pygame.image.load(f'data/zombie_dead{i}.png'), (size_monster, size_monster)) for i in
            range(1, 5)]

    def update(self):
        if self.flag == True:
            self.kill()
        else:
            if pygame.sprite.spritecollideany(self, bullet):
                self.health -= 1
                if self.health == 0:
                    self.flag = True
                    bul.kill()
                else:
                    bul.kill()

    def kill(self):
        try:
            self.image = self.anim_right[int(self.index_animation)]
            if self.index_animation == 3.0:
                pass
            else:
                self.index_animation += 0.1
        except:
            pass


class Player(pygame.sprite.Sprite):
    def __init__(self, y, x):
        super().__init__(all_sprites)
        self.anim_right = [pygame.transform.scale(pygame.image.load(f'data/r{i}.png'), (SIZE, SIZE)) for i in
                           range(1, 5)]
        self.image = pygame.transform.scale(pygame.image.load(f'data/r1.png'), (SIZE, SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * 49
        self.rect.y = y * 49
        self.dx = 0
        self.dy = 0
        self.speed_x = 0.1
        self.speed_y = 1
        self.index_animation = 1
        self.direction = 0

    def get(self):
        return self.rect.x, self.rect.y, self.direction

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.dx = 1
            self.direction = 0
        elif keys[pygame.K_LEFT]:
            self.dx = -1
            self.direction = 2
        elif keys[pygame.K_UP]:
            self.dy = -1
            self.direction = 3
        elif keys[pygame.K_DOWN]:
            self.dy = 1
            self.direction = 1
        else:
            self.dx = 0
            self.dy = 0

        self.animation(self.dx, self.dy)
        self.rect.x += self.dx
        # self.collider_x()
        self.rect.y += self.dy
        # self.collider_y()
        # self.golds_up()

    def animation(self, dx, dy):
        try:
            if dx == 1:
                self.image = self.anim_right[int(self.index_animation)]
                if self.index_animation == 3:
                    self.index_animation = 1
                self.index_animation += 0.1
            elif dx == -1:
                self.image = pygame.transform.flip(self.anim_right[int(self.index_animation)], True, False)
                if self.index_animation == 3:
                    self.index_animation = 1
                self.index_animation += 0.1
            elif dy == 1:
                self.image = pygame.transform.rotate(self.anim_right[int(self.index_animation)], -90)
                if self.index_animation == 3:
                    self.index_animation = 1
                self.index_animation += 0.1
            elif dy == -1:
                self.image = pygame.transform.rotate(self.anim_right[int(self.index_animation)], 90)
                if self.index_animation == 3:
                    self.index_animation = 1
                self.index_animation += 0.1
        except:
            self.index_animation = 1


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1000, 700
    screen = pygame.display.set_mode(size)
    running = True
    camera = Camera()
    screen.fill((93, 62, 29))
    pygame.display.flip()
    fps = 120
    clock = pygame.time.Clock()
    player, level_x, level_y, house = generate_level(load_level('map.txt'))
    tiles_group.draw(screen)
    space_group = pygame.sprite.Group()
    a = pygame.sprite.Sprite()
    a.image = load_image('space.jpg')
    a.rect = a.image.get_rect()
    space_group.add(a)
    space_group.draw(screen)

    while running:
        space_group.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if len(bullet.sprites()) == 0:
                        bul = Bullet(player.get())
                        pygame.mixer.init()
                        pygame.mixer.music.load("data/shoot.mp3")
                        pygame.mixer.music.play()

        try:
            bul.x()

        except:
            pass
        try:
            if bul.dellete():
                bul.kill()
        except:
            pass
        mon.update()
        tiles_group.draw(screen)
        all_sprites.draw(screen)
        mon.draw(screen)
        bullet.draw(screen)
        block_group.draw(screen)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in tiles_group:
            camera.apply(sprite)
        for sprite in block_group:
            camera.apply(sprite)
        for sprite in bullet:
            camera.apply(sprite)
        for sprite in mon:
            camera.apply(sprite)
        pygame.display.flip()
        player.update()
        clock.tick(fps)

    pygame.quit()
