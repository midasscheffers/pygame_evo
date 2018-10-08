import pygame
import random
import math
import numpy as np

pygame.init();
print(pygame.init())

seed = random.randrange(0, 999999)
random.seed(seed)

# variables
height = 1080
width = 1920

clock = pygame.time.Clock()
FPS = 60
getTicksLastFrame = 0

fontL = pygame.font.SysFont(None, 100)
fontS = pygame.font.SysFont(None, 30)

white = (255, 255, 255)
black = (0, 0, 0)
red = (170, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
dark_purple = (25, 0, 25)

maxOrbSpeed = 2
orbs = []
amountOfOrbs = 50

fruits = []
amountOfFruits = 50
fruitGameTicks = 0

gameExit = False

MouseXY = ()
selected = ""

#make game display
gameDisplay = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("evo")

pygame.display.update()

# classes
class Fruit:
    def __init__(self, size, color, posX, posY):
        self.size = size
        self.color = color
        self.posX = posX
        self.posY = posY

    def draw(self):
        pygame.draw.circle(gameDisplay, self.color, (self.posX, self.posY), self.size, 0)

class Orb:

    def __init__(self, size, color, posX, posY, Xspd, Yspd, aOFTS, numOfOffspring, food_los, food_max, gen):
        self.size = size
        self.color = color
        self.posX = posX
        self.posY = posY
        self.Xspd = Xspd
        self.Yspd = Yspd
        self.aOFTS = aOFTS
        self.numOfOffspring = numOfOffspring
        self.gen = gen
        self.food_los = food_los
        self.food_max = food_max
        self.food_timer = self.food_max
        self.food = 3
        self.kill = False

    def move(self):
        if self.size > 40:
            self.posX += (self.Xspd / (self.size / 40))
            self.posY += (self.Yspd / (self.size / 40))
        else:
            self.posX += self.Xspd
            self.posY += self.Yspd
        if self.posX > width - self.size or self.posX < 0 + self.size:
            self.Xspd = -self.Xspd
        if  self.posY > height - self.size or self.posY < 0 + self.size:
            self.Yspd = -self.Yspd

    def checkForFruit(self):
        eat = False
        FruitToKill = 0
        for i in range(len(fruits)):
            fruit = fruits[i]
            if math.sqrt(math.pow(self.posX - fruit.posX, 2) + math.pow(self.posY - fruit.posY, 2)) <= self.size + fruit.size:
                self.food += 1
                FruitToKill = i
                eat = True
        if eat == True:
            del fruits[FruitToKill]
            self.food_timer = self.food_max
            self.food += self.food_los

        if self.size > 40:
            self.food_timer -= 1 * (self.size / 40)
        else:
            self.food_timer -= 1
        if self.food_timer < 0:
            self.food_timer = self.food_max
            self.food -= self.food_los
        if self.food < 0:
            self.kill = True



    def draw(self):
        pygame.draw.circle(gameDisplay, self.color, (int(self.posX), int(self.posY)), self.size, 0)

    def ChekSplit(self):
        if self.food >= self.aOFTS + 5:
            for i in range(self.numOfOffspring):
                doMutation = bool(random.getrandbits(1))
                if doMutation == True:
                    newcolor = (random.randint(self.color[0]-50, self.color[0]+50), random.randint(self.color[1]-50, self.color[1]+50), random.randint(self.color[2]-50, self.color[2]+50))
                    if newcolor[0] > 255:
                        newcolor = replace_at_index1(newcolor, 0, 255)
                    if newcolor[1] > 255:
                        newcolor = replace_at_index1(newcolor, 1, 255)
                    if newcolor[2] > 255:
                        newcolor = replace_at_index1(newcolor, 2, 255)
                    if newcolor[0] < 0:
                        newcolor = replace_at_index1(newcolor, 0, 0)
                    if newcolor[1] < 0:
                        newcolor = replace_at_index1(newcolor, 1, 0)
                    if newcolor[2] < 0:
                        newcolor = replace_at_index1(newcolor, 2, 0)
                    size = random.randint(self.size-5, self.size+5)
                    if size < 5:
                        size = 5
                    orb = Orb(size, newcolor, self.posX - i*20, self.posY - i*20, random.randint(self.Xspd-1, self.Xspd+1), random.randint(self.Yspd-1, self.Yspd+1), random.randint(1, self.aOFTS+2), random.randint(1, 3), random.randint(1, 3), random.randint(self.food_max - 20, self.food_max + 20), self.gen + 1)
                else:
                    orb = Orb(self.size, self.color, int(self.posX - i*20), int(self.posY - i*20), self.Xspd, self.Yspd, self.aOFTS, self.numOfOffspring, self.food_los, self.food_max, self.gen + 1)
                orbs.append(orb)
            self.kill = True
            self.food = 0

# functoins
def message_toscreen(msg, color, x, y, size):
    if (size == "l"):
        screenText = fontL.render(msg, True, color)
        gameDisplay.blit(screenText, [x, y])
    if (size == "s"):
        screenText = fontS.render(msg, True, color)
        gameDisplay.blit(screenText, [x, y])


def replace_at_index1(tup, ix, val):
    lst = list(tup)
    lst[ix] = val
    return tuple(lst)

def randColor(min, max):
    return(int(random.randint(min, max)), int(random.randint(min, max)), int(random.randint(min, max)))

def start():
    # make orbs
    for i in range(amountOfOrbs):
        orb = Orb(random.randint(10, 20), randColor(0, 255), random.randint(50, width - 50), random.randint(50, height - 50), random.randint(-maxOrbSpeed, maxOrbSpeed), random.randint(-maxOrbSpeed, maxOrbSpeed), random.randint(1, 5), random.randint(1, 3), random.randint(1, 3), random.randint(120, 240), 0)
        orbs.append(orb)
    # make Fruit
    for i in range(amountOfFruits):
        fruit = Fruit(5, green, random.randint(50, width - 50), random.randint(50, height - 50))
        fruits.append(fruit)

start()


# game
while not gameExit:

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            gameExit = True


    t = pygame.time.get_ticks()
    # deltaTime in seconds.
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    print(deltaTime)

    gameDisplay.fill(dark_purple)

    for i in range(len(fruits)):
        fruit = fruits[i]
        fruit.draw()

    fruitGameTicks += 1

    if fruitGameTicks > FPS/4 - 1:
        fruit = Fruit(5, green, random.randint(50, width - 50), random.randint(50, height - 50))
        fruits.append(fruit)
        fruitGameTicks = 0

    numberToKill = []
    for i in range(len(orbs)):
        orb = orbs[i]
        orb.move()
        orb.draw()
        orb.checkForFruit()
        if orb.kill == True:
            numberToKill.append(i)
        orb.ChekSplit()

    orbs = list(np.delete(orbs, numberToKill))

    MouseXY = pygame.mouse.get_pos()

    pygame.event.get()
    mouseDown = pygame.mouse.get_pressed()
    if mouseDown[2] == True:
        selected = ""

    for i in range(len(orbs)):
        orb = orbs[i]
        if math.sqrt(math.pow(orb.posX - MouseXY[0], 2) + math.pow(orb.posY - MouseXY[1], 2)) <= 2 + orb.size or str(orb) == selected:
            pygame.event.get()
            mouseDown = pygame.mouse.get_pressed()
            if mouseDown[0] == True:
                selected = str(orb)
            pygame.draw.circle(gameDisplay, white, (int(orb.posX), int(orb.posY)), orb.size + 5, 0)
            orb.draw()
            pygame.draw.rect(gameDisplay, (50, 0, 100), [width - 500, 0, 500, 50])
            message_toscreen(("cell: " + str(orb)), white, width-450, 15, "s")
            pygame.draw.rect(gameDisplay, (0, 0, 50), [width - 500, 50, 500, 300])
            message_toscreen(("cell pos: " + str(orb.posX) + ", " + str(orb.posY)), white, width-450, 100, "s")
            message_toscreen(("cell spd: " + str(orb.Xspd) + ", " + str(orb.Yspd)), white, width-450, 150, "s")
            message_toscreen(("cell gen: " + str(orb.gen)), white, width-450, 200, "s")
            message_toscreen(("cell food: " + str(orb.food)), white, width-450, 250, "s")
            message_toscreen(("cell size: " + str(orb.size)), white, width-450, 300, "s")


    message_toscreen(("N.O.O: " + str(len(orbs))), white, 10, 10, "l")
    message_toscreen(("Seed: " + str(seed)), white, 10, 80, "s")


    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
quit()
