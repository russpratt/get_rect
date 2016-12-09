import random
import pygame
from pygame.locals import *



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("art/jet.png").convert()
        self.image.set_colorkey((255,255,255), RLEACCEL)
        #self.surf = pygame.Surface((75,25))
        #self.surf.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.surf = self.image
        self.score = 0
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)
        #screen logic
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > s_x:
            self.rect.right = s_x
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= s_y:
            self.rect.bottom = s_y
        #print(self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        #self.image = pygame.image.load("art/missile.png").convert()
        bad_food = ["art/bad/gb.png", "art/bad/h.png"
            , "art/bad/ic.png"]
        self.image = pygame.image.load(bad_food[random.randint(0,2)]).convert()
        self.image.set_colorkey((0,0,0), RLEACCEL)
        #self.surf = pygame.Surface((20,10))
        #self.surf.fill((255,255,255))
        self.rect = self.image.get_rect(
            center=(random.randint(s_x+20,s_x+100), random.randint(0,s_y)))
        self.speed = random.randint(2,10)
        self.surf = self.image

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right<0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.image = pygame.image.load("art/cloud.png").convert()
        self.image.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.image.get_rect(
            center = (random.randint(s_x+20,s_x+100), random.randint(0,s_y))
        )
        self.surf = self.image
    def update(self):
        self.rect.move_ip(-1,0)
        if self.rect.right < 0:
            self.kill

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super(Food, self).__init__()
        good_food = ["art/good/b.png", "art/good/bp.png"
            ,"art/good/w.png", "art/good/c.png"]
        self.image = pygame.image.load(good_food[random.randint(0,len(good_food)-1)])
        self.image.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.image.get_rect(
            center = (random.randint(s_x+20,s_x+100), random.randint(0,s_y))
        )
        self.surf = self.image
        self.speed = random.randint(2,10)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill

pygame.init()

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 522)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)
ADDFOOD = pygame.USEREVENT + 3
pygame.time.set_timer(ADDFOOD, 327)
ADDBANG = pygame.USEREVENT + 4


running = True
s_x = 1200
s_y = 800
screen = pygame.display.set_mode((s_x,s_y))

background = pygame.Surface(screen.get_size())
background.fill((137,205,250))

#score
myfont = pygame.font.SysFont("monospace", 30)

#music
pygame.mixer.music.load("sounds/songs/Can't eat right.mp3")
pygame.mixer.music.play(-1)
death_sound = pygame.mixer.Sound("sounds/Celebrate.wav")
bite_sound = pygame.mixer.Sound("sounds/bite/bite1.aiff")

#surfs
bang_i = pygame.sprite.Sprite()
bang_i.image = pygame.image.load("art/explosion.png").convert()
bang_i.image.set_colorkey((0,0,0), RLEACCEL)
bang_time = 0

#custom surf classes
player = Player()
#enemy = Enemy()

enemies = pygame.sprite.Group()
foods = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
clouds = pygame.sprite.Group()



while running:
    #making events?
    #getting events
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif (event.type == ADDENEMY):
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            all_sprites.add(new_cloud)
            clouds.add(new_cloud)
        elif event.type == ADDFOOD:
            new_food = Food()
            foods.add(new_food)
            all_sprites.add(new_food)
        elif event.type == ADDBANG:
            all_sprites.add(bang_i)
            bang_time = pygame.time.get_ticks()

    pressed_keys = pygame.key.get_pressed()

    #cleanup and maintenance
    if pygame.sprite.spritecollideany(player, enemies) and player.alive():
        player.kill()
        print("OH NOE!")
        death_sound.play()
        bang_i.rect = player.rect
        all_sprites.add(bang_i)
        bang_time = pygame.time.get_ticks()
        #pygame.event.post(pygame.event.Event(ADDBANG))
    if pygame.sprite.spritecollideany(player, foods) and player.alive():
        pygame.sprite.spritecollideany(player, foods).kill()
        print("yum")
        bite_sound.play()
        if player.alive():
            player.score +=1
    screen.blit(background,(0,0))
    label = myfont.render(str(player.score), 1, (255,255,255))
    screen.blit(label, (10, s_y-30))
    if bang_time + 2000 <pygame.time.get_ticks():
        bang_i.kill()

    #doing stuff with events

    if player in all_sprites:
        player.update(pressed_keys)
        screen.blit(player.surf, player.rect)
    for e in enemies:
        e.update()
        screen.blit(e.surf, e.rect)
    for f in foods:
        f.update()
        screen.blit(f.surf, f.rect)
    for c in clouds:
        c.update()
        screen.blit(c.surf, c.rect)    #for entity in all_sprites:
    if bang_i in all_sprites:
        screen.blit(bang_i.image, bang_i.rect)
    #    screen.blit(entity.surf, entity.rect)
    #screen.blit(enemy.surf, enemy.rect)
    pygame.display.flip()
    #print(len(all_sprites))
