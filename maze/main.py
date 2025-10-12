from pygame import *


mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')


font.init()
font = font.SysFont('Arial', 40)
win = font.render('YOU WIN!', True, (224, 217, 180))
lose = font.render('YOU LOSE!', True, (116, 183, 211))



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x < 850:
            self.rect.x += self.speed

        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed

        if keys[K_DOWN] and self.rect.y < 850:
            self.rect.y += self.speed


class Enemy(GameSprite):
    direction = 'left'
    def update(self):
        if self.rect.x <= 570:
            self.direction = 'right'
        if self.rect.x >= 850:
            self.direction = 'left'
        
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Kill(GameSprite):
    direction = 'left'
    def update(self):
        if self.rect.x <= 10:
            self.direction = 'right'
        if self.rect.x >= 200:
            self.direction = 'left'
        
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


win_width = 900
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption('Maze')
background = transform.scale(image.load('ajy.jpg'), (win_width, win_height))


player = Player('hero.png', 5, win_height - 700, 4)
cyborg = Enemy('cyborg.png', 800, win_height - 600, 3)
treasure = GameSprite('treasure.png', 800, win_height - 100, 2)
knife = Kill('knife.png', 5, win_height - 100, 4)


w1 = Wall(201,234,205, 90, 10, 550, 10)
w2 = Wall(201,234,205, 100, 650, 650, 10)
w3 = Wall(201,234,205, 300, 10, 10, 550)
w4 = Wall(201,234,205, 90, 20, 10, 500)
w5 = Wall(201,234,205, 500, 100, 10, 550)


clock = time.Clock()


game = True

finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))
        knife.update()
        cyborg.update()
        player.update()
        treasure.reset()
        cyborg.reset()
        player.reset()
        knife.reset()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()

        if sprite.collide_rect(player, cyborg) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or \
            sprite.collide_rect(player, w3) or sprite.collide_rect(player, w4) or sprite.collide_rect(player, w5) or sprite.collide_rect(player, knife):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()
        if sprite.collide_rect(player, treasure):
            finish = True
            window.blit(win, (200, 200))
            money.play()



    display.update()
    clock.tick(60)