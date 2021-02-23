import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img_')
snd_dir = path.join(path.dirname(__file__), 'snd')
WIDTH = 480
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
spawn = 0
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot em up!")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('comic sans ms')
HP = 160


def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def get_shield(center):
    sh = ShieldBuff(center)
    all_sprites.add(sh)
    buffs.add(sh)


def get_mg(center):
    mgb = MGBuff(center)
    all_sprites.add(mgb)
    buffs.add(mgb)


class MGBuff(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = mg_buff_image
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = -5
        self.speedx = random.randint(-1, 1)

    def update(self):
        global HP, running
        self.rect.y -= self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom > 600:
            self.kill()
        hitss = pygame.sprite.spritecollide(player, buffs, False, pygame.sprite.collide_circle)
        if hitss:
            player.mgtime += 75
            self.kill()


class ShieldBuff(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = sheild_buff_image
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = -5
        self.speedx = random.randint(-1, 1)

    def update(self):
        global HP, running
        self.rect.y -= self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom > 600:
            self.kill()
        hitss = pygame.sprite.spritecollide(player, buffs, False, pygame.sprite.collide_circle)
        if hitss:
            player.sheild += 1
            self.kill()


def newmob():
    global spawn
    m_ = Mob()
    spawn += 1
    all_sprites.add(m_)
    mobs.add(m_)
    if spawn % 5 == 0:
        all_sprites.add(m_)
        mobs.add(m_)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speedy = 8
        self.image = pygame.transform.scale(player_img, (50, 55))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.sheild = False
        self.mgtime = 0
        self.mgcounter = 0
        self.sheild = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.mgtime > 0:
            if self.mgcounter == 0:
                self.mgcounter = 1
            else:
                self.shoot()
                self.mgcounter = 0
                self.mgtime -= 1

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        global enemy_image
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = enemy_image
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -50)
        self.speedy = random.randrange(1, 2)
        self.speedx = random.randrange(-3, 3)
        self.last_update = pygame.time.get_ticks()
        self.counter = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.counter += 1
        if self.counter % 75 == 0:
            self.shoot()
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        ebullets.add(bullet)
        shoot_sound.play()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img2
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.top = y + 50
        self.rect.centerx = x
        self.speedy = -8

    def update(self):
        global HP, running, ebullets
        self.rect.y -= self.speedy
        if self.rect.bottom > 600:
            self.kill()
        hitss = pygame.sprite.spritecollide(player, ebullets, False, pygame.sprite.collide_circle)
        if hitss:
            if player.sheild > 0:
                player.sheild -= 1
            else:
                HP -= 40
            self.kill()
            if HP <= 0:
                running = False
            for hitt in hitss:
                all_sprites.add(Explosion(hitt.rect.center, 'sm'))


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


background = pygame.image.load(path.join(img_dir, "starfield.jpg")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "Player.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "PB.png")).convert()
bullet_img2 = pygame.image.load(path.join(img_dir, "EB.png")).convert()
enemy_image = pygame.image.load(path.join(img_dir, 'Enemy.png')).convert()
mg_buff_image = pygame.image.load(path.join(img_dir, 'mg_buff.png')).convert()
sheild_buff_image = pygame.image.load(path.join(img_dir, 'shield_buff.png')).convert()

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
expl_sounds = []
explosion_anim = {'lg': [], 'sm': []}
for i in range(9):
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'LMR.ogg'))
pygame.mixer.music.set_volume(0.9)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
ebullets = pygame.sprite.Group()
buffs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
mobcounter = 4
for i in range(mobcounter):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
score = 0
running = False
nexit = False
record = 0
pygame.mixer.music.play(loops=-1)

while not nexit:
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                nexit = True
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
        if not nexit:
            all_sprites.update()
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 50 - hit.radius
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            newmob()
            chance = random.randint(1, 17)
            if chance == 1:
                newmob()
            chance = random.randint(1, 60)
            if chance == 1:
                get_shield(hit.rect.center)
            elif chance == 2:
                get_mg(hit.rect.center)
        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if hits:
            for hit in hits:
                if HP <= hit.radius:
                    running = False
                else:
                    newmob()
                    HP -= hit.radius
                    random.choice(expl_sounds).play()
                    expl = Explosion(hit.rect.center, 'lg')
                    all_sprites.add(expl)
        if not nexit:
            screen.fill(BLACK)
            screen.blit(background, background_rect)
            all_sprites.draw(screen)
            draw_text(screen, ('Счёт: ' + str(score) + '  Здоровье: ' + str(HP) + '    Щит: ' +
                               str(player.sheild)), 18, WIDTH // 2, 10, GREEN)
            pygame.display.flip()
    while not running:
        if nexit:
            pygame.quit()
        clock.tick(FPS)
        if score > record:
            record = score
        if not nexit and not running:
            screen.fill(BLACK)
            screen.blit(background, background_rect)
            draw_text(screen, 'Игра Shoot em up!', 56, WIDTH // 2, 100, WHITE)
            draw_text(screen, 'Стрелки - передвижение', 20, WIDTH // 2, 200, WHITE)
            draw_text(screen, 'Пробел - стрельба', 20, WIDTH // 2, 250, WHITE)
            draw_text(screen, ('Ваш счёт: ' + str(score)), 20, WIDTH // 2, 300, WHITE)
            draw_text(screen, ('Ваш рекорд: ' + str(record)), 20, WIDTH // 2, 350, WHITE)
            draw_text(screen, 'Нажмите "P", чтобы начать', 20, WIDTH // 2, 400, WHITE)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    nexit = True
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        running = True
                        nexit = False
                        score = 0
                        HP = 160
                        all_sprites = pygame.sprite.Group()
                        mobs = pygame.sprite.Group()
                        bullets = pygame.sprite.Group()
                        player = Player()
                        all_sprites.add(player)
                        mobcounter = 4
                        for i in ebullets:
                            i.kill()
                        for i in range(mobcounter):
                            m = Mob()
                            all_sprites.add(m)
                            mobs.add(m)
if nexit:
    pygame.quit()
