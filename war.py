import math
import time
from random import randint

import pygame

pygame.mixer.init()


soundObj = pygame.mixer.Sound('music/sakano.wav')
soundObj.play(-1)

# 00 Show panel
pygame.init()
screen = pygame.display.set_mode(
    (900, 900))  # pygame.display.set_mode((Width, Height))
pygame.display.set_caption(
    "Tsushima Battle 0.0")  # Set up a caption for the screen
icon = pygame.image.load("images/lShield.png")
pygame.display.set_icon(icon)

# Set up player and enermy
player = pygame.image.load("images/warshipMikasa.jpg.png").convert_alpha()
playerX = 425  # location of player
playerY = 700
enemy = pygame.image.load("images/enermy.jpg.png").convert_alpha()
transit = 0
step = 0
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

def show_score():
    text = "This is your score: " + str(score)
    score_render = font.render(text, True, (234, 200, 2))
    screen.blit(score_render, (0, 0))


Max_enemies = 6
game_over = False
isWin = False



# Create a class of enermy, which has method move
class Enermy:
    def __init__(self, x, y, estep):
        self.x = x
        self.y = y
        self.step = estep
        self.img = pygame.image.load("images/enermy.jpg.png").convert_alpha()
        self.hp = 300

    def move_enemy(self):
        self.x += self.step
        if self.x > 850. or self.x < 0.:
            self.step *= -1
            self.y += 30

    def reset(self):
        self.y = 0
        self.x = 0

    def beattacked(self):
        self.hp -= 100
        if self.hp == 0:
            self.reset()


class Shell:
    def __init__(self):
        self.x = playerX + 12
        self.y = playerY
        self.step = -2
        self.img = pygame.image.load("images/shellShell.png")

    def move_shell(self):
        self.y += self.step

    def distance(self, ex, ey):
        side1 = self.x - ex
        side2 = self.y - ey
        d = math.sqrt(pow(side1, 2) + pow(side2, 2))
        return d

    def attack(self):
        global score
        for e in enemies:
            d = self.distance(e.x + 25, e.y + 100)
            if d < 30:
                shells.remove(self)
                e.beattacked()
                boom = pygame.mixer.Sound("music/bomb.mp3")
                boom.play()
                score += 1


def greatSkill():
    global playerX

    shell = Shell()
    shells.append(shell)
    for shell in shells:
        shell.x = randint(1, 800)
    shell.attack()



shells = []

# Get a list of enemies created
enemies = []
for i in range(Max_enemies):
    enemies.append(Enermy(randint(0, 850), randint(0, 100), 0.5))


def move_enemies():
    for e in enemies:
        screen.blit(e.img, (e.x, e.y))
        e.move_enemy()


def get_end():
    global game_over
    global isWin
    for e in enemies:
        if e.y > 900 - 200 - 200:
            game_over = True
            isWin = False
    if score > 100:
        game_over = True
        isWin = True


def move_player():
    global playerX, playerY
    global step
    global running
    global shells
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:  # Use event.key to check which button you press
                step = 2
            if event.key == pygame.K_LEFT:
                step = -2
            if event.key == pygame.K_SPACE:
                shells.append(Shell())

        if event.type == pygame.KEYUP:  # Use pygame.KEYUP to end the event
            step = 0
    for shell in shells:
        shell.move_shell()
        screen.blit(shell.img, (shell.x, shell.y))
        shell.attack()

    # # The player should not out of bound
    playerX += step

    if playerX > 850:
        playerX = 850
    elif playerX < 0:
        playerX = 0

getSkill = False
getCount = 0

win_text = pygame.font.Font('freesansbold.ttf', 60)
win_render = win_text.render("Game End! You win!", True, (255, 210, 12))
lose_text = pygame.font.Font('freesansbold.ttf', 60)
lose_render = win_text.render("Game End! You Lose!", True, (255, 210, 12))

# 01 Maintain the screen by using while loop
background = pygame.image.load("images/LogoLocky.png")  # load the background image
running = True
while running:
    screen.blit(background, (0, 0))
    # Use screen.blit(backgroundImage, startingPosition) to draw the image
    move_player()

    # if int(playerX) >= 850:
    #     transit = 1 # transit == 1 means warship should turn left
    # if int(playerX) <= 0:
    #     transit = 0 # transit == 0 means warship should turn right
    #
    # if not transit:
    #     playerX += 0.1
    # else:
    #     playerX -= 0.1
    move_enemies()
    show_score()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                getSkill = True
                for i in range(10):
                    greatSkill()
                getCount += 1
                skillimg = pygame.image.load("images/LogoLocky.png")
                pygame.display.set_icon(skillimg)
                if getCount > 100000000:
                    getCount = 0
                    break


    pygame.display.set_icon(background)







    get_end()
    if game_over and isWin:
        screen.blit(win_render, (100, 100))
    elif game_over and not isWin:
        screen.blit(lose_render, (100, 100))

    screen.blit(player, (int(playerX), int(playerY)))
    pygame.display.update()
    # No matter what yo  u have done on screen, pygame.display.update is needed.
