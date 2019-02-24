import pygame
import os
import sys

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("SCP")

#Константы
pos_x = 100
pos_y = 200
speed = 5
left = False
right = False
side = 0
animCount = 0


#Группы спрайтов
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


#Функция для загрузки изображений
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


#Функция для загрузки уровня
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
 
    # и подсчитываем максимальную длину    
    max_width = max(map(len, level_map))
 
    # дополняем каждую строку пустыми клетками ('.')    
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

#Стартовый экран
def startScreen():
    introText = ["WELCOME", "",
                 "SCP Foundation",
                "Смэртб,",
                 "Ты умрёшь в конце"]
    
    fon = pygame.transform.scale(load_image('fon.jpg'), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    textCoord = 50

    for line in introText:
        stringRendered = font.render(line, 1, pygame.Color('white'))
        introRect = stringRendered.get_rect()
        textCoord += 10
        introRect.top = textCoord
        introRect.x = 10
        textCoord += introRect.height
        screen.blit(stringRendered, introRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(30)

#Функция выхода на кнопку Exit
def terminate():
    pygame.quit()
    sys.exit()

#Разметка
class Label:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bgcolor = pygame.Color("white")
        self.font_color = pygame.Color("gray")
        # Рассчитываем размер шрифта в зависимости от высоты
        self.font = pygame.font.Font("freesansbold.ttf", self.rect.height - 4)
        self.rendered_text = None
        self.rendered_rect = None


    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)


class GUI:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def render(self, surface):
        for element in self.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(surface)

    def update(self):
        for element in self.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                element.get_event(event)

#Кнопки
class Button(Label):
    def __init__(self, rect, text):
        super().__init__(rect, text)
        self.bgcolor = pygame.Color("black")
        # при создании кнопка не нажата
        self.pressed = False

    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        if not self.pressed:
            color1 = pygame.Color("white")
            color2 = pygame.Color("black")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 5, centery=self.rect.centery)
        else:
            color1 = pygame.Color("black")
            color2 = pygame.Color("white")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 7, centery=self.rect.centery + 2)

        # рисуем границу
        pygame.draw.rect(surface, color1, self.rect, 2)
        pygame.draw.line(surface, color2, (self.rect.right - 1, self.rect.top), (self.rect.right - 1, self.rect.bottom), 2)
        pygame.draw.line(surface, color2, (self.rect.left, self.rect.bottom - 1),
                         (self.rect.right, self.rect.bottom - 1), 2)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False

#Непосредственно пауза
def pause():
    gui = GUI()
    b1 = Button((300, 300, 200, 80), "EXIT")
    b2 = Button((270, 250, 260, 50), "CONTINUE")
    gui.add_element(b1)
    gui.add_element(b2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            gui.get_event(event);
        if b1.pressed:
            while b1.pressed:
                for event in pygame.event.get():
                    gui.get_event(event)
                gui.render(screen)
                gui.update()
                pygame.display.flip()
            terminate()
        if b2.pressed:
            while b2.pressed:
                for event in pygame.event.get():
                    gui.get_event(event)
                gui.render(screen)
                gui.update()
                pygame.display.flip()
            return
        gui.render(screen)
        gui.update()
        pygame.display.flip()


#Изображения    
tile_images = [load_image("#.png",1)]

walkRight = [load_image("r1.png",1),load_image("r2.png",1),
             load_image("r3.png",1),load_image("r4.png",1),
             load_image("r5.png",1),load_image("r6.png",1)]

walkLeft = [load_image("l1.png",1),load_image("l2.png",1),
             load_image("l3.png",1),load_image("l4.png",1),
             load_image("l5.png",1),load_image("l6.png",1)]

playerStand = [load_image("st.png",1), load_image("stl.png",1)]


#Класс Героя
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = playerStand[0]
        self.rect = self.image.get_rect().move(
            89 * pos_x + 15, 200 * pos_y + 5)
 
 
    def update(self, screen, x, y):
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

#Класс блоков
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[0]
        self.rect = self.image.get_rect().move(
            57 * pos_x, 60 * pos_y)


#Инициализация
player = Player(pos_x, pos_y)
mapa = load_level('map.txt')


def generate_level(level):
    player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile( x, y)
            elif level[y][x] == '@':
                player = Player( x, y)
    # вернем игрока, а также размер поля в клетках
    return player, x, y


clock = pygame.time.Clock()
running = True
generate_level(mapa)
startScreen()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause()


    keys = pygame.key.get_pressed()

    
    if keys[pygame.K_LEFT] and pos_x > 5:
        pos_x -= speed
        left = True
        right = False
        side = 0

    elif keys[pygame.K_RIGHT]:
        pos_x += speed
        left = False
        right = True
        side = 1

    else:
        left = False
        right = False
        animCount = 0
    
    screen.fill((120,120,120))
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    all_sprites.update(screen, pos_x, pos_y)
    pygame.display.flip()
    clock.tick(30)


pygame.quit()
    
