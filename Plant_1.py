from pygame import *
from random import *
from time import time as timer

win_widh = 1000
win_hight = 400

win = display.set_mode((win_widh, win_hight))
display.set_caption('Plants')

ImegHero = 'Woodman.png'
ImeBack = 'Forest.png'
ImeAnemi = 'BigCliz.png'
img_bullet = 'Ball.png'

TimeNow = timer()
TimeHit = timer()

# clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, PLimage, playX, playY, sizeX, sizeY, speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(PLimage), (sizeX, sizeY))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = playX
        self.rect.y = playY
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Plaer(GameSprite):
    def Went(self):
        global LastWent
        global TimeNow
        went = key.get_pressed()
        if went[K_UP]:
            self.rect.y -= self.speed
        if went[K_DOWN]:
            self.rect.y += self.speed
        if went[K_LEFT]:
            self.rect.x -= self.speed
            LastWent = 'Left'
        if went[K_RIGHT]:
            self.rect.x += self.speed
            LastWent = 'Right'
        if (timer() - TimeNow) > 2:
            if went[K_SPACE]:
                TimeNow = timer()
                if LastWent == 'Left':
                    self.rect.x -= 10*self.speed
                else:
                    self.rect.x += 10*self.speed
    def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.centery, 15, 20, 15)
       bullets.add(bullet)

class PlantsAnami(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = win_widh
            self.rect.y = randint(150, 340)

class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_widh:
            self.kill()

fps = 30
LastWent = 'Left'
HeroGad = Plaer(ImegHero, 50, 50, 60, 60, 10)

GameRun = True
bacgraund = transform.scale(image.load(ImeBack), (win_widh, win_hight))

monsters = sprite.Group()
ds = [50, win_widh-100]
for i in range(1,7):
    monster = PlantsAnami(ImeAnemi, win_widh, randint(150, 400-90), 72, 72, randint(-5,-1))
    monsters.add(monster)

bullets = sprite.Group()

def DrawAll():
    win.blit(bacgraund, (0,0))
    # draw.rect(win, (0,255,0), (0, 350, 1000, 50))
    HeroGad.reset()
    HeroGad.Went()

    monsters.update()
    monsters.draw(win)

    bullets.update()
    bullets.draw(win)

    display.update()

while GameRun:
    for e in event.get():
        if e.type == QUIT:
            GameRun = False
        elif e.type == KEYDOWN:
            if e.key == K_q:
                HeroGad.fire()

    collide = sprite.groupcollide(bullets, monsters, True, True)
    for c in collide:
        while len(monsters) < 6:
            monster = PlantsAnami(ImeAnemi, win_widh, randint(150, 340), 72, 72, randint(-5,-1))
            monsters.add(monster)
    # tap = key.get_pressed()

    # if sprite.spritecollide(HeroGad, monsters, True):
    #     print('AAAAAAAAAAAAAA')
    #     # monster = PlantsAnami(ImeAnemi, win_widh, randint(150, 340), 72, 72, randint(-5,-1))
    #     # monsters.add(monster)
    #     while len(monsters)<6:
    #         monster = PlantsAnami(ImeAnemi, win_widh, randint(150, 340), 72, 72, randint(-5,-1))
    #         monsters.add(monster)

    DrawAll()
    time.delay(fps)