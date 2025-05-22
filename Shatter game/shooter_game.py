from pygame import *
from random import randint

#background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


#fonts and captions
font.init()
font1 = font.Font(None, 36)
win = font1.render('YOU ARE VERY SKIBIDI', True, (255, 255, 255))
lose = font1.render('YOU AINT HIM', True, (180, 0, 0))
font2 = font.SySFont('Arial', 36)


#we need the following images:
img_back = "galaxy.jpg" #game background
img_hero = "rocket.png" #hero
img_bullet = "bullet.png" # bullet
img_enemy = "ufo.png" # enemy


goal = 10
score = 0 #ships destroyed
lost = 0 #ships missed
max_lost = 5 #lose if you miss that many


#parent class for other spirtes
class GameSprite(sprite.Sprite):
#class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Call for the class(Sprite) constructor:
        sprite.Sprite.__init__(self)

        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed


        #every sprite must have the rect property - the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
#method drawing the character on the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#main player class
class Player(GameSprite):
    #method to control the sprite with arrow keys
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        #method to "shoot" (use the player position to create a bullet there)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


#enemy spirte class
class Enemy(GameSprite):
    #enemy movement
    def update(self):
        self.rect.y += self.speed
        global lost
        #disapperas upon reaching the screen edge
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


    #bullet sprite class
class Bullet(GameSprite):
    #enemy movement
    def update(self):
        self.rect.y += self.speed
        #disappears upon reaching the screen edge
        if self.rect.y < 0:
            self.kill()

#create a window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)


bullets = sprite.Group()


#the "game is over" variable: as soon as True is there, sprites stop working in the main loop
finish = False
#Main game loop:
run = True #the flag is reset by the window close button
while run:
    #"Close" button press event
    for e in event.get():
        if e.type == QUIT:
            run = False
        #event of pressing the spacebar - the sprite shoots
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()


    if not finish:
        #update the background
        window.blit(background,(0,0))


        #write text on the screen
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))


        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))


        #launch spirte movements
        ship.update()
        monsters.update()
        bullets.update()



        #update them in a new location in each loop iteration
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        #check for a collision between a bullet and monsters (both monster and bullet disappear upon a touch)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #this loop will repeat as many times as the number of monsters hit
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        #possible lose: missed too many times as the number of monsters hit
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True #lose, set the background and no longer control the sprites.
            window.blit(lose, (200, 200))

        #win checking how many points scored?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    #bonus: automatic restart of the game
    else:
        finsih = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()


        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80,), -40, 80, 50, randint(1, 5))
            monsters.add(monster)



    time.delay(50)