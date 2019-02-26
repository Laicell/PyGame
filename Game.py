import os
import sys
import pygame

pygame.init()

pygame.key.set_repeat(200, 70)

width, height = 800, 600
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("SCP")

# Const
left = right = up = False
animCount = 0
platforms = []
lastJump = False
MOVE_SPEED = 5
GRAVITY = 0.4
JUMP_POWER = 10

# Sound
menu = pygame.mixer.Sound('data/scp.ogg')
step = pygame.mixer.Sound('data/step.ogg')
jump = pygame.mixer.Sound('data/jump.ogg')

# Группы спрайтов
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


# Функция для загрузки изображений
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


# Функция для загрузки уровня
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                pl = Tile(x, y)
                platforms.append(pl)
    # вернем игрока, а также размер поля в клетках
    # return player, x, y

# Стартовый экран


def startScreen():
    introText = ["WELCOME", "",
                "SCP Foundation",
                "Press F to start",
                "Pre-Alpha 0.1"]
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    return  # начинаем игру
        menu.play()
        pygame.display.flip()
        clock.tick(30)


# Функция выхода на кнопку Exit
def terminate():
    pygame.quit()
    sys.exit()


# Разметка
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


# Кнопки
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


# Непосредственно пауза
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
            gui.get_event(event)
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


# Изображения
tile_images = [load_image("#.png", -1)]

bg = [load_image("bg.png")]

playerStand = [load_image("str.png", -1), load_image("stl.png", -1),
load_image("flying.png", -1)]

walkRight = [load_image("r1.png", -1),
load_image("r2.png", -1), load_image("r3.png", -1),
load_image("r4.png", -1), load_image("r5.png", -1),
load_image("r6.png", -1)]

walkLeft = [load_image("l1.png", -1),
load_image("l2.png", -1), load_image("l3.png", -1),
load_image("l4.png", -1), load_image("l5.png", -1),
load_image("l6.png", -1)]


# камера
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


# Класс Героя
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.xvel = 0
        self.yvel = 0
        self.image = playerStand[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.onGround = False

    def update(self, left, right, up, platforms):
        global lastJump
        global animCount
        self.stand = 0
        if animCount + 1 >= 60:
            animCount = 0
        if self.onGround:
            lastJump = False
        if left:
            self.xvel = -MOVE_SPEED

            self.image = walkLeft[animCount//10]
            animCount += 1
            self.stand = 1
            if not up:
                step.play()
            if right:
                step.stop()

        if right:
            self.xvel = MOVE_SPEED
            self.stand = 1
            if not up:
                step.play()
            if left:
                step.stop()
            self.image = walkRight[animCount//10]
            animCount += 1

        if not(left or right):
            self.xvel = 0
            step.stop()
            if not up:
                if self.stand == 0:
                    self.image = playerStand[0]
                else:
                    self.image = playerStand[1]

        if up:
            step.stop()
            if self.onGround:
                self.yvel = -JUMP_POWER

        if lastJump:

            self.image = playerStand[2]

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for pl in platforms:
            if pygame.sprite.collide_rect(self, pl):
                if xvel > 0:
                    self.rect.right = pl.rect.left
                if xvel < 0:
                    self.rect.left = pl.rect.right
                if yvel > 0:
                    self.rect.bottom = pl.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = pl.rect.bottom
                    self.yvel = 0


# Класс блоков
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[0]
        self.rect = self.image.get_rect().move(
            57 * pos_x, 60 * pos_y)


# Инициализация
camera = Camera()
player = Player(120, 340)
generate_level(load_level('map.txt'))


clock = pygame.time.Clock()
running = True
startScreen()
menu.stop()
while running:

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        lastJump = True

    shift_pressed = False
    right_pressed = False
    left_pressed = False

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                left = True
                left_pressed = True

            if e.key == pygame.K_RIGHT:
                right = True
                right_pressed = True

            if e.key == pygame.K_UP:
                up = True

            if e.key == pygame.K_LSHIFT:
                if right_pressed or left_pressed:
                    MOVE_SPEED = 25

            if e.key == pygame.K_ESCAPE:
                pause()

            else:
                shift_pressed = False
                right_pressed = False
                left_pressed = False
                MOVE_SPEED = 5

        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT:
                left = False
            if e.key == pygame.K_RIGHT:
                right = False
            if e.key == pygame.K_UP:
                up = False

    screen.blit(bg[0], (0, 0))
    camera.update(player)
    all_sprites.draw(screen)
    player_group.draw(screen)
    tiles_group.draw(screen)
    player.update(left, right, up, platforms)
    for sprite in all_sprites:
        camera.apply(sprite)
    # player_group.update()
    # all_sprites.update()
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)


pygame.quit()
