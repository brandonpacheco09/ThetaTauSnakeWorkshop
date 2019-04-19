import pygame, os, math, sys, random

pygame.init()

pygame.display.set_caption("Fuck efrain cause hes hot")

random.seed()

MOVEMENT_SPEED = .5
SNAKE_BLOCK_SIZE = 10
FOOD_SIZE = SNAKE_BLOCK_SIZE
SEPERATION = 10

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

FPS = 25

KEY = {"UP": 1, "DOWN": 2, "LEFT": 3, "RIGHT": 4}

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.HWSURFACE)

text_font = pygame.font.Font(None, 30)
score_number_font = pygame.font.Font(None, 30)

score_message = text_font.render("Score", 0, pygame.Color("green"))

background_color = pygame.Color(100,100,100)

clock = pygame.time.Clock()


def main():
    snake = Snake(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    snake.move()
    end = 0
    count = 0
    startingCells = 2
    eaten_food = 0
    score = 0

    while count < startingCells:
        snake.grow()
        snake.move()
        count += 1

    food = [Food(random.randint(FOOD_SIZE, SCREEN_WIDTH),random.randint(FOOD_SIZE, SCREEN_HEIGHT),1)]
    spawnSingleFood(food, snake.x, snake.y)


    while end != 1:

        #pygame.event.get()
        #pygame.display.update()
        clock.tick(FPS)

        keyPressed = getPressedKey()

        if(keyPressed == "exit"):
            end = 1

        if(snake.checkCrash() == True):
            gameEnd()

        if(crashing(snake.bodyStack[0], SNAKE_BLOCK_SIZE) == True):
            gameEnd()

        for f in food:
            if(f.state == 1):
                if(checkCollision(snake.bodyStack[0], SNAKE_BLOCK_SIZE, f, FOOD_SIZE) == True):
                    snake.grow()
                    f.state = 0
                    score += 5
                    eaten_food = True

        if(eaten_food == True):
            spawnSingleFood(food, snake.x, snake.y)
            eaten_food = False

        if(keyPressed):
            snake.changeDirection(keyPressed)
        snake.move()

        screen.fill(background_color)

        for f in food:
            if(f.state == 1):
                f.draw(screen)

        snake.draw(screen)
        drawScore(score)

        pygame.display.flip()
        pygame.display.update()



def getPressedKey():
    for event in pygame.event.get():
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_UP):
                return KEY["UP"]
            elif(event.key == pygame.K_DOWN):
                return KEY["DOWN"]
            elif(event.key == pygame.K_RIGHT):
                return KEY["RIGHT"]
            elif(event.key == pygame.K_LEFT):
                return KEY["LEFT"]
            elif(event.key == pygame.K_ESCAPE):
                return "exit"
            elif(event.key == pygame.K_y):
                return "yes"
            elif(event.key == pygame.K_n):
                return "no"
        if(event.type == pygame.QUIT):
            sys.exit()

class Cell:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.color = "white"

class Food:
    def __init__(self,x,y,state):
        self.x = x
        self.y = y
        self.state = state
        self.color = pygame.Color("red")

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,(self.x, self.y, FOOD_SIZE, FOOD_SIZE), 0)

class Snake:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.direction = KEY["RIGHT"]

        self.bodyStack = []
        self.bodyStack.append(self)

        endCell = Cell(x - SEPERATION, y)
        endCell.color = "NULL"
        endCell.direction = KEY["RIGHT"]
        self.bodyStack.append(endCell)

    def move(self):

        lastCell = len(self.bodyStack) - 1

        while lastCell != 0:
            self.bodyStack[lastCell].direction = self.bodyStack[lastCell-1].direction
            self.bodyStack[lastCell].x = self.bodyStack[lastCell-1].x
            self.bodyStack[lastCell].y = self.bodyStack[lastCell-1].y
            lastCell -= 1

        if(len(self.bodyStack) < 2):
            headCell = self
        else:
            headCell = self.bodyStack.pop(lastCell)

        if(self.bodyStack[0].direction == KEY["UP"]):
            headCell.y = self.bodyStack[0].y - (FPS * MOVEMENT_SPEED)
        elif(self.bodyStack[0].direction == KEY["RIGHT"]):
            headCell.x = self.bodyStack[0].x + (FPS * MOVEMENT_SPEED)
        elif(self.bodyStack[0].direction == KEY["DOWN"]):
            headCell.y = self.bodyStack[0].y + (FPS * MOVEMENT_SPEED)
        elif(self.bodyStack[0].direction == KEY["LEFT"]):
            headCell.x = self.bodyStack[0].x - (FPS * MOVEMENT_SPEED)

        self.bodyStack.insert(0, headCell)

    def grow(self):
        lastCell = len(self.bodyStack) - 1

        if(self.bodyStack[lastCell].direction == KEY["UP"]):
            newCell = Cell(self.bodyStack[lastCell].x, self.bodyStack[lastCell].y + SNAKE_BLOCK_SIZE)
            endCell = Cell(newCell.x, newCell.y + SEPERATION)
        if(self.bodyStack[lastCell].direction == KEY["DOWN"]):
            newCell = Cell(self.bodyStack[lastCell].x, self.bodyStack[lastCell].y - SNAKE_BLOCK_SIZE)
            endCell = Cell(newCell.x, newCell.y - SEPERATION)
        if(self.bodyStack[lastCell].direction == KEY["RIGHT"]):
            newCell = Cell(self.bodyStack[lastCell].x - SNAKE_BLOCK_SIZE, self.bodyStack[lastCell].y)
            endCell = Cell(newCell.x - SEPERATION, newCell.y)
        if(self.bodyStack[lastCell].direction == KEY["LEFT"]):
            newCell = Cell(self.bodyStack[lastCell].x + SNAKE_BLOCK_SIZE, self.bodyStack[lastCell].y)
            endCell = Cell(newCell.x + SEPERATION, newCell.y)

        endCell.color = "NULL"
        self.bodyStack.append(newCell)
        self.bodyStack.append(endCell)

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color("gold"),(self.bodyStack[0].x,self.bodyStack[0].y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE), 0)

        cellCount = 1

        while cellCount < len(self.bodyStack):
            if(self.bodyStack[cellCount].color == "NULL"):
                cellCount += 1
                continue
            pygame.draw.rect(screen, pygame.Color("orange"),(self.bodyStack[cellCount].x, self.bodyStack[cellCount].y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE), 0)
            cellCount += 1

    def checkCrash(self):
        cellCount = 1

        while cellCount < len(self.bodyStack):
            if checkCollision(self.bodyStack[0], SNAKE_BLOCK_SIZE, self.bodyStack[cellCount], SNAKE_BLOCK_SIZE) == True and self.bodyStack[cellCount].color != "NULL":
                return True
            cellCount += 1
        return False

    def changeDirection(self, direction):
        if(self.direction == KEY["RIGHT"] and direction == KEY["LEFT"] or self.direction == KEY["LEFT"] and direction == KEY["RIGHT"]):
            pass
        if(self.direction == KEY["DOWN"] and direction == KEY["UP"] or self.direction == KEY["UP"] and direction == KEY["DOWN"]):
            pass
        self.direction = direction

def checkCollision(positionA,sizeA, positionB, sizeB):
    if(positionA.x < positionB.x + sizeB and positionA.x + sizeA > positionB.x and positionA.y < positionB.y + sizeB and positionA.y + sizeA > positionB.y):
        return True
    return False

def crashing(positionA, sizeA):
    if(positionA.x - sizeA < 0 or positionA.x + sizeA > SCREEN_WIDTH or positionA.y - sizeA < 0 or positionA.y + sizeA > SCREEN_HEIGHT):
        return True
    return False

def spawnSingleFood(food, sx, sy):
    del food[:]

    x = random.uniform(FOOD_SIZE + 5, SCREEN_WIDTH - FOOD_SIZE - 5)
    y = random.uniform(FOOD_SIZE + 5, SCREEN_HEIGHT - FOOD_SIZE - 5)

    while(x-FOOD_SIZE == sx or x+FOOD_SIZE == sx and y-FOOD_SIZE ==sy or y+FOOD_SIZE==sy):
        x = random.uniform(FOOD_SIZE + 5, SCREEN_WIDTH - FOOD_SIZE - 5)
        y = random.uniform(FOOD_SIZE + 5, SCREEN_HEIGHT - FOOD_SIZE - 5)

    food.append(Food(x,y,1))

def drawScore(score):
    msg_score = score_number_font.render(str(score), 1, pygame.Color("green"))
    screen.blit(score_message, (SCREEN_WIDTH - text_font.size("Score")[0] - 60,10))
    screen.blit(msg_score, (SCREEN_WIDTH - 40, 10))

def gameEnd():
    msg = text_font.render("Game Over",1,pygame.Color("White"))
    play_again = text_font.render("Play Again Y/N?", 1, pygame.Color("green"))
    screen.blit(msg,(SCREEN_WIDTH/2 - text_font.size("Game Over")[0]/2,SCREEN_HEIGHT/2))
    screen.blit(play_again,(SCREEN_WIDTH/2 - text_font.size("Play Again Y/N?")[0]/2, SCREEN_HEIGHT/2 + 40))

    pygame.display.flip()
    pygame.display.update()

    myKey = getPressedKey()
    while myKey != "exit":
        if(myKey == "yes"):
            main()
        elif(myKey == "no"):
            break
        myKey = getPressedKey()
        clock.tick(FPS)
    sys.exit()















main()
