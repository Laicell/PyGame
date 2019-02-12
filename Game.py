import pygame
import os

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("SCP")

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
 
    # и подсчитываем максимальную длину    
    max_width = max(map(len, level_map))
 
    # дополняем каждую строку пустыми клетками ('.')    
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

def make_level(level, platform):
    x = 0
    y = 0
    for row in level:
        for col in row:
            if col == '#':
                screen.blit(platform, (x, y))
            x += 57
        y += 60
        x = 0


class Hero(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
 
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
 
    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def render(self, screen, x, y):
        global animCount
        if animCount + 1 >= 30:
            animCount = 0

        if right:
            screen.blit(walkRight[animCount // 5], (x,y))
            animCount += 1

        elif left:
            screen.blit(walkLeft[animCount // 5], (x,y))
            animCount += 1
        
        else:
            if side == 1:
                screen.blit(playerStand[0], (x,y))
            else:
                screen.blit(playerStand[1], (x,y))

        
tile_images = [load_image("#.png",1)]

walkRight = [load_image("r1.png",1),load_image("r2.png",1),
             load_image("r3.png",1),load_image("r4.png",1),
             load_image("r5.png",1),load_image("r6.png",1)]

walkLeft = [load_image("l1.png",1),load_image("l2.png",1),
             load_image("l3.png",1),load_image("l4.png",1),
             load_image("l5.png",1),load_image("l6.png",1)]

playerStand = [load_image("st.png",1), load_image("stl.png",1)]


all_sprites = pygame.sprite.Group()

x = 100
y = 200
speed = 5
left = False
right = False
side = 0
animCount = 0

mapa = load_level('map.txt')
hero = Hero(load_image("ggg.png"), 4, 1, x, y)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > 5:
        x -= speed
        left = True
        right = False
        side = 0

    elif keys[pygame.K_RIGHT]:
        x += speed
        left = False
        right = True
        side = 1

    else:
        left = False
        right = False
        animCount = 0

    make_level(mapa, tile_images[0])
    
    #all_sprites.draw(screen)
    #all_sprites.update()
    hero.render(screen, x, y)
    hero.update()
    pygame.display.flip()
    screen.fill((120,120,120))
    clock.tick(30)

pygame.quit()
    
