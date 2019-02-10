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


class Hero(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        #super().__init__(all_sprites)
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
        if animCount + 1 >= 15:
            animCount = 0

        if right:
            screen.blit(self.frames[animCount // 5], (x,y))
            animCount += 1
        else:
            screen.blit(self.frames[0], (x,y))
        #screen.blit(self.image, (x,y))
        


#all_sprites = pygame.sprite.Group()
x = 100
y = 200
speed = 10
left = False
right = False
animCount = 0
hero = Hero(load_image("ggg.png"), 4, 1, x, y)
clock = pygame.time.Clock()
running = True
while running:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > 5:
        x -= speed
        left = True
        right = False
    elif keys[pygame.K_RIGHT]:
        x += speed
        left = False
        right = True
    else:
        left = False
        right = False
        animCount = 0
    #all_sprites.draw(screen)
    #all_sprites.update()
    hero.render(screen, x, y)
    hero.update()
    pygame.display.flip()
    screen.fill((0,0,0))
    clock.tick(30)
pygame.quit()
    
