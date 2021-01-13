import pygame

pygame.init()
win = pygame.display.set_mode((500, 480))
pygame.display.set_caption("DINOKILL")

walkRight = [pygame.image.load('Knight\\KR1.png'), pygame.image.load('Knight\\KR2.png'), pygame.image.load('Knight\\KR3.png'), pygame.image.load('Knight\\KR4.png'), pygame.image.load(
    'Knight\\KR5.png'), pygame.image.load('Knight\\KR6.png'), pygame.image.load('Knight\\KR7.png'), pygame.image.load('Knight\\KR8.png'), pygame.image.load('Knight\\KR9.png')]
walkLeft = [pygame.image.load('Knight\\KL1.png'), pygame.image.load('Knight\\KL2.png'), pygame.image.load('Knight\\KL3.png'), pygame.image.load('Knight\\KL4.png'), pygame.image.load(
    'Knight\\KL5.png'), pygame.image.load('Knight\\KL6.png'), pygame.image.load('Knight\\KL7.png'), pygame.image.load('Knight\\KL8.png'), pygame.image.load('Knight\\KL9.png')]
bg = pygame.image.load('jungle.jpg')

clock = pygame.time.Clock()

spearsound = pygame.mixer.Sound("Knight.wav")
dinosound = pygame.mixer.Sound("TRex.wav")

music = pygame.mixer.music.load("POCarribean.mp3")
pygame.mixer.music.play(-1)

score = 0


class player(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 55, self.y + 11, 29, 52)

    def draw(self, win):

        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 55, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-10', 5, (15, 143, 255))
        win.blit(text, (250 - int(text.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class projectile(object):

    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('Dinosaur\\DR1.png'), pygame.image.load('Dinosaur\\DR2.png'), pygame.image.load('Dinosaur\\DR3.png'), pygame.image.load(
        'Dinosaur\\DR4.png'), pygame.image.load('Dinosaur\\DR5.png'), pygame.image.load('Dinosaur\\DR6.png'), pygame.image.load('Dinosaur\\DR7.png'), pygame.image.load('Dinosaur\\DR8.png')]
    walkLeft = [pygame.image.load('Dinosaur\\DL1.png'), pygame.image.load('Dinosaur\\DL2.png'), pygame.image.load('Dinosaur\\DL3.png'), pygame.image.load(
        'Dinosaur\\DL4.png'), pygame.image.load('Dinosaur\\DL5.png'), pygame.image.load('Dinosaur\\DL6.png'), pygame.image.load('Dinosaur\\DL7.png'), pygame.image.load('Dinosaur\\DL8.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 38, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()

        if self.visible:
            if self.walkCount + 1 >= 24:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0),
                             (self.hitbox[0], self.hitbox[1]-20, 50, 10))
            pygame.draw.rect(
                win, (0, 128, 0), (self.hitbox[0], self.hitbox[1]-20, 50 - (int(50/10) * (10 - self.health)), 10))
            self.hitbox = (self.x + 38, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print(f"Hit! {(score+1)}")


def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (380, 15))
    man.draw(win)
    dino.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    if dino.visible == False:
        result = pygame.font.SysFont('comicsans', 500, True)
        end_score = font.render("You Win!  Score : " +
                                str(score), 1, (255, 72, 36))
        win.blit(end_score, (130, 200))
    pygame.display.update()


font = pygame.font.SysFont('comicsans', 30, True)
man = player(300, 400, 64, 64)
dino = enemy(100, 400, 66, 66, 300)
shootLoop = 0
bullets = []
run = True

while run:
    clock.tick(27)

    if dino.visible == True:
        if man.hitbox[1] < dino.hitbox[1] + dino.hitbox[3] and man.hitbox[1] + man.hitbox[3] > dino.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > dino.hitbox[0] and man.hitbox[0] < dino.hitbox[0] + dino.hitbox[2]:
                man.hit()
                score -= 10

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < dino.hitbox[1] + dino.hitbox[3] and bullet.y + bullet.radius > dino.hitbox[1]:
            if bullet.x + bullet.radius > dino.hitbox[0] and bullet.x - bullet.radius < dino.hitbox[0] + dino.hitbox[2]:
                dinosound.play()
                dino.hit()
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        spearsound.play()
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width // 2),
                                      round(man.y + man.height // 2), 6, (255, 230, 0), facing))
        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not (man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0

    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= int((man.jumpCount ** 2)*0.50 * neg)
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.quit()
