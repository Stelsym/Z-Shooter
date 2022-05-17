#Створи власний Шутер!

from pygame import *
from random import randint
from time import time as timer #импортировать под названием таймер

#створи вікно гри
window = display.set_mode((1266,650),flags=FULLSCREEN)
display.set_caption('Нашествие')
#задай фон сцени
background = transform.scale(image.load('mape.jpg'),(1266,650))

win_height = 650
win_width = 1266

mixer.init()
mixer.music.load('footbolMusic.mp3')
mixer.music.play()

music = randint(1,2)
fire_sound = mixer.Sound('fire.ogg') #звук выстрела из пистолета 1
fire_sound2 = mixer.Sound('fire2.ogg') #звук выстрела из пистолета 2
win_sound = mixer.Sound('win.ogg') #музыка при победе
lose_sound1 = mixer.Sound('sad1.ogg') #музыка при поражении 1
lose_sound2 = mixer.Sound('sad2.ogg') #музыка при поражении 2 
boom_sound = mixer.Sound('boom.ogg') #звук выстрела из базуки
damage_sound = mixer.Sound('damage.ogg') #звук получения урона игроком
max_ammo_sound = mixer.Sound('max_ammo.ogg') #звук, после перезарядки пистолета
pusto_pistol_sound = mixer.Sound('pusto_pistol.ogg') #попытка выстрелить с пустым магазином
neprobil_sound = mixer.Sound('neprobil.ogg') #звук непробития брони
boomOGG_sound = mixer.Sound('boomOGG.ogg') #звук взрыва снаряда

fire_sound2.set_volume(0.5)
boom_sound.set_volume(0.5)
damage_sound.set_volume(0.5)
max_ammo_sound.set_volume(0.25)
pusto_pistol_sound.set_volume(0.5)
boomOGG_sound.set_volume(0.5)
neprobil_sound.set_volume(0.5)

clock = time.Clock()
FPS = 60

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.size_x = size_x
        self.size_y = size_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def image_reset(self,new_image,size_x,size_y): 
        self.image = transform.scale(image.load(new_image),(size_x,size_y))
        self.reset()

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if self.rect.y == 55 and keys[K_a] and self.rect.x > 700:
            self.rect.x -= self.speed
        if self.rect.y == 55 and keys[K_d] and self.rect.x < win_width - 330:
            self.rect.x += self.speed

        # 1
        if keys[K_1]:
            self.image_reset('playerP.png',self.size_x,self.size_y)
            self.rect.x = 1266-900
            self.rect.y = 650-200
        # 2
        if keys[K_2]:
            self.image_reset('playerP.png',self.size_x,self.size_y)
            self.rect.x = 1266-870
            self.rect.y = 650-460
        # 3
        if keys[K_3]:
            self.image_reset('playerP2.png',self.size_y,self.size_x) 
            self.rect.x = 800
            self.rect.y = 55

    def fire1B(self):
        bullet = Bullet2('raketa.png',self.rect.x+randint(75,85),self.rect.y+55 ,60,40,randint(4,7))
        rockets.add(bullet)
    def fire1P(self):
        bullet2 = Bullet('pulya2.png',self.rect.x+41,self.rect.y+70,10,20,15)
        bullets.add(bullet2)
    def fire2P(self):
        bullet3  = Bullet2('pulya.png',self.rect.x+80,self.rect.y+27,20,10,15)
        bullets.add(bullet3)
    def fire2B(self):
        bullet4  = Bullet('raketa2.png',self.rect.x-5,self.rect.y+randint(73,80),40,60,randint(4,7))
        rockets.add(bullet4)

class Enemy(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        global lost
        if self.rect.x < 0:
            self.rect.x = 1266
            self.rect.y = randint(150,535)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Bullet2(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        global lost
        if self.rect.x < 0:
            self.rect.x = 1266
            self.rect.y = randint(150,535)
            lost += 2

font.init()
font1 = font.SysFont('Verdana',26)
font2 = font.SysFont('Verdana',46)

game = True
Finish = False

lost = 0
score = 0
life = 3

bullets = sprite.Group()
rockets = sprite.Group()

Gun = GameSprite('pistolet.png',135,35,80,60,0)
patrons_pistolet = 5

Bazuka = GameSprite('bazuka.png',135,90,100,60,0)
patrons_bazuka = 0

player = Player('playerP.png',1266-900,650-200,100,80,10)
rel_time = False
num_fire = 0
rel_time2 = False
num_fire2 = 0
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('enemy.png',win_width-80,randint(150,530),70,50,randint(1,5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Asteroid('enemy2.png',win_width-80,randint(150,530),80,80,randint(1,3))
    asteroids.add(asteroid)

while game:
    if not Finish:
        window.blit(background, (0,0))
        Gun.update()
        Gun.reset()
        Bazuka.update()
        Bazuka.reset()
        player.update()
        player.reset() 
        monsters.update()
        monsters.draw(window) 
        bullets.update()
        bullets.draw(window) 
        rockets.update()
        rockets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render('Перезарядка пистолета...',1,(150,0,0))
                window.blit(reload,(player.rect.x,player.rect.y-30))
            else:
                num_fire = 0
                rel_time = False
                patrons_pistolet = 5
                max_ammo_sound.play()
        
        if rel_time2 == True:
            now_time2 = timer()
            if now_time2 - last_time2 < 5:
                if patrons_bazuka != 0:
                    reload1 = font1.render('Перезарядка базуки...',1,(200,100,0))
                    window.blit(reload1,(player.rect.x,player.rect.y-50))
            else:
                num_fire2 = 0
                rel_time2 = False

        text = font1.render('Счёт:' + str(score),1,(255,255,255))
        text_lose = font1.render('Пропущено:' + str(lost),1,(255,255,255))
        text_life = font1.render('Жизни:'+ str(life),1,(150,0,0))
        text_patrons_pistolet = font2.render(str(patrons_pistolet),1,(53,185,0))
        text_patrons_bazuka = font2.render(str(patrons_bazuka),1,(53,185,0))
        window.blit(text,(280,10))
        window.blit(text_lose,(390,10))
        window.blit(text_life,(150,10))
        window.blit(text_patrons_pistolet,(215,35))
        window.blit(text_patrons_bazuka,(240,90))

        if sprite.spritecollide(player,monsters,False) or sprite.spritecollide(player,asteroids,False):
            sprite.spritecollide(player,monsters,True)
            sprite.spritecollide(player,asteroids,True)
            life -= 1
            damage_sound.play()


        collides = sprite.groupcollide(monsters,bullets,True,True)
        collidesB = sprite.groupcollide(monsters,rockets,True,True)
        for c in collides or collidesB:
            score = score + 1
            if patrons_bazuka != 2:
                patrons_bazuka += 1
            monster = Enemy('enemy.png',win_width-80,randint(150,530),70,50,randint(1,5))
            monsters.add(monster)
        if score >= 12:
            Finish = True
            mixer.music.pause()
            win_sound.play()
            win = font1.render('YOU WIN!',True,(0,150,0))
            window.blit(win,(400,40))
        if life == 0 or lost >= 5:
            Finish = True
            mixer.music.pause()
            lose = font1.render('YOU LOSE!',True,(180,0,0))
            window.blit(lose,(395,40))
            if music == 1:
                lose_sound1.play()
            if music == 2:
                lose_sound2.play()
            lose = font1.render('YOU LOSE!',True,(180,0,0))
            window.blit(lose,(395,40))

        collides2 = sprite.groupcollide(asteroids,rockets,True,True)
        for a in collides2:
            boomOGG_sound.play()
            asteroid = Asteroid('enemy2.png',win_width-80,randint(150,530),80,80,randint(1,3))
            asteroids.add(asteroid)

        collides2B = sprite.groupcollide(asteroids,bullets,False,True)
        for o in collides2B:
            neprobil_sound.play()
            

        display.update()

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:

            #Базука
            if e.key == K_LEFT and player.rect.y != 55:
                if player.rect.y == 55:
                    player.image_reset('playerB2.png',player.size_y+3,player.size_x+9)
                else:
                    player.image_reset('playerB.png',player.size_x+3,player.size_y+9)
                if num_fire2 < 1 and rel_time2 == False:
                    num_fire2 += 1
                    if patrons_bazuka > 0:
                        boom_sound.play()
                        player.fire1B()
                        patrons_bazuka -= 1
                if num_fire2 == 1 and rel_time2 == False:
                    last_time2 = timer()
                    rel_time2 = True



            #Пистолет
            if e.key == K_DOWN and player.rect.y == 55:
                if player.rect.y == 55:
                    player.image_reset('playerP2.png',player.size_y,player.size_x)
                else:
                    player.image_reset('playerP.png',player.size_x,player.size_y)
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound2.play()
                    player.fire1P()
                    if patrons_pistolet != 0:
                        patrons_pistolet -= 1
                if num_fire >=5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                if num_fire >= 5 and rel_time == True:
                    pusto_pistol_sound.play()

            #Пистолет
            if e.key == K_RIGHT and player.rect.y != 55:
                if player.rect.y == 55:
                    player.image_reset('playerP2.png',player.size_y,player.size_x)
                else:
                    player.image_reset('playerP.png',player.size_x,player.size_y)
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound2.play()
                    player.fire2P()
                    if patrons_pistolet != 0:
                        patrons_pistolet -= 1
                if num_fire >=5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                if num_fire >= 5 and rel_time == True:
                    pusto_pistol_sound.play()

            #Базука         
            if e.key == K_UP and player.rect.y == 55:
                if player.rect.y == 55:
                    player.image_reset('playerB2.png',player.size_y+10,player.size_x)
                else:
                    player.image_reset('playerB.png',player.size_x+10,player.size_y)
                if num_fire2 < 1 and rel_time2 == False:
                    num_fire2 += 1
                    if patrons_bazuka > 0:
                        boom_sound.play()
                        player.fire2B()
                        patrons_bazuka -= 1
                if num_fire2 == 1 and rel_time2 == False:
                    last_time2 = timer()
                    rel_time2 = True
            
        elif e.type == KEYUP:
            if e.key == K_8: #pausa music
                mixer.music.pause()

            elif e.key == K_9:
                mixer.music.unpause()
                mixer.music.set_volume(0.5) #тише в 2 раза
                
            elif e.key == K_0:
                mixer.music.unpause()
                mixer.music.set_volume(1) #стандартный звук
                
            elif e.key == K_6: #сделать звук эффектов громче в 2 раза
                fire_sound2.set_volume(1)
                boom_sound.set_volume(1)
                damage_sound.set_volume(1)
                pusto_pistol_sound.set_volume(1)
                boomOGG_sound.set_volume(1)
                neprobil_sound.set_volume(1)

            elif e.key == K_7: #сделать звук эффектов стандартным
                fire_sound2.set_volume(0.5)
                boom_sound.set_volume(0.5)
                damage_sound.set_volume(0.5)
                pusto_pistol_sound.set_volume(0.5)
                boomOGG_sound.set_volume(0.5)
                neprobil_sound.set_volume(0.5)

            elif e.key == K_r: #перезарядка пистолета при нажатии на R
                if num_fire > 0:
                    num_fire = 5
                    last_time = timer()
                    rel_time = True
            elif e.key == K_ESCAPE:
                game = False

    time.delay(10)    


 
