#first we are going to import the libraries we need
#OS library is used for operating system functionalities such as reading a file or using software/hardware products.
#Math library is for math functions such as floor/ceiling
#Sys library gives access to system only functions such as exit()
#Random library allows us to create random number generators
#Pygame library allows us to create game applications along with other types of applications.
import pygame, os, math, sys, random

#We have to initialize the game modules that pygame gives us access to.
pygame.init()

#Lets create a title for our window screen, we have to do pygame.display to access the display of the game.
pygame.display.set_caption("Theta Tau Snek Workshop")


#now lets initialize a random number generator using the random library
random.seed()

#Lets set up some constant variables

#Gonna need the movement speed of the snake, i put caps for constant values but you dont need to. Also you can't have
#any spaces in your variable names
MOVEMENT_SPEED = .4

#Gonna need a block size
SNAKE_BLOCK_SIZE = 10

#Gonna need some food size
FOOD_SIZE = SNAKE_BLOCK_SIZE

#Going to use a no color block to sepearate the blocks
SEPERATION = 10

#Lets set up our screen height and width
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

#Some frames per second
FPS = 25

#Going to set up a dictionary. A dictionary just lets you have keys and assign values to those keys
KEY = {"UP":1, "DOWN": 2, "LEFT": 3, "RIGHT": 4}

#Going to set initialize the screen now with. Remember we have to access the pygames display using the .
#set_mode takes in the resoultion as a pair of width and height, then a surface.
#HWSURFACE uses the video card on the hardware to make it faster.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE)

#Lets create some GUI Constants
text_font = pygame.font.Font(None, 30)
score_number_font = pygame.font.Font(None, 30)

#We're going to make the score text now
#render takes in text, a boolean if you want smooth edges or not, a pygame color, and a background if wanted
score_message = text_font.render("Score", 0, pygame.Color("green"))

#Lets create a background color
background_color = pygame.Color(100,100,100)

#Now lets create a game clock variable
clock = pygame.time.Clock()

#STEP 1
#Lets create our main first so we can start seeing a screen
#we have to call this to get the events on the pygame window or else it doesn't know what to do and crashes
#lets fill the screen we initialized earlier for the window with the color we chose
#we want to update the screen so we call pygame.display.update
#youll notice we can't exit the window, so go into your terminal or command window and push control c
#we have to get the type of events that pygame can take in

#STEP 3
#lets change the line of code of pygame.event.get we had to call our function.
#lets make a variable to keep track of the key pressed. Now you can exit the window formally.
def main():
    #STEP 17
    #lets create a new snake object and remember we pass in the starting location. You can put any values in there as long
    #as there within the screen size
    snake = Snake(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
    #Lets get the snake to move right away
    snake.move()
    #This is going to be our variable to end the game
    end = 0;
    #Create a variable to to have your snake start out with this many body cells. Im going to choose two.
    startingCells = 2
    #Create a variable to count how many cells we create
    count = 0

    #Create a variable to keep track if the food has beene eaten
    eaten_food = 0
    #Create a variable to keep track of the score
    score = 0

    #Lets create a while loop to let the snake grow and have it move
    #we're going to use the cells variable we made as the condition
    while(count < startingCells):
        snake.grow()
        snake.move()
        count += 1

    #Lets create a list of food that takes in a food object with random coordinates and state equal to 1
    food = [Food(random.randint(FOOD_SIZE,SCREEN_WIDTH), random.randint(FOOD_SIZE, SCREEN_HEIGHT), 1)]

    #lets spawn a food by passing in the food list and snake coordinates
    spawnSingleFood(food, snake.x, snake.y)

    while end != 1:
        #Lets comment these out now and start from the beginning now for the loop that will run endlessly
        #keyPressed = getPressedKey()
        #screen.fill(background_color)
        #pygame.display.update()

        #Going to have the pygame clock tick as fast as the FPS
        clock.tick(FPS)

        #Create the keypressed variable again and call the function getPressedKey
        keyPressed = getPressedKey()
        #We check if the keypresed is equal to exit we make end equal to 1
        if(keyPressed == "exit"):
            end = 1

        #lets check if the snake is crashing into itself and if it is end the game
        if(snake.checkCrash() == True):
            gameEnd()

        #lets check if the snake is crashing into the edges and if its true end the game
        if(crashing(snake.bodyStack[0], SNAKE_BLOCK_SIZE) == True):
            gameEnd()

        #we're going to check for all the food and if the food is not eaten then check for the snake colliding with food
        #if the snake does collide then we make the snake grow make sure the food is set to state 0 for eaten
        #and we add to the score and make eaten food equal to true
        for f in food:
            if(f.state == 1):
                if(checkCollision(snake.bodyStack[0],SNAKE_BLOCK_SIZE, f, FOOD_SIZE) == True):
                    snake.grow()
                    f.state = 0
                    score += 5
                    eaten_food = True

        #if the snake has eaten then we spawn another food and changed eaten food to false
        if(eaten_food == True):
            spawnSingleFood(food, snake.bodyStack[0].x, snake.bodyStack[0].y)
            eaten_food = False

        #If a key was pressed we try to change the direction of the snake then we move again
        if(keyPressed):
            snake.changeDirection(keyPressed)
        snake.move()

        #We fill the screen in again with the color
        screen.fill(background_color)

        #we check for all the food and if the food has not been eaten then we draw it on the screen
        for f in food:
            if(f.state == 1):
                f.draw(screen)

        #lets draw the snake on the screen
        snake.draw(screen)
        #lets draw the score
        drawScore(score)

        #We call pygame.display.flip to layer the screen
        pygame.display.flip()
        #we update the display
        pygame.display.update()

#STEP 2
#lets create a function to access these events
#we're going to write a for loop to check all the events that can happen in the window
#We're going to create a bunch of if statements and else if statements
#We're going to check the event type and  if that event type is equal to either
#key up, key down, key right, key left, key escape, key y, key n, or quit then we are going to return
#either the value of the respective key we defined earlier, a string of what to do, or exit the system
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

#STEP 4
#Alright lets create the class for the basic snake cell which the snake will be composed of
#We have to create an init function as this will be called when we want to create a new cell.
#It has two underscores on each side and this is necessary.
#The parameters are going to be self, an x value, and a y value
#Then we set the self.x and self.y to the respective x and y values.
#Then we are going to set the direction to up by using the dictionary value of up
#Then we can set the color of the cell, this doesn't matter because we will be changing the color later
#But we do need to create a color for it so go wild with whatever color you want.
class Cell:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.color = "white"

#STEP 5
#Now lets create the food class so we can create food for the snake to eat
#Again the parameters will be the the self, x value, y value, and a state which is just an integer
#We're going to set the values like we did in the cell class, but now we don't have a direction
#We have a state and we need a color, you can choose any color you want your food to be, but this color will not change later
class Food:
    def __init__(self,x,y,state):
        self.x = x
        self.y = y
        self.state = state
        self.color = pygame.Color("red")

    #STEP 14
    #We're going to write a function to draw the food
    #parameters are going to be self and a screen
    #lets draw a rect using the screen the self.color and the x, y coordinates and the food size and a 0 width
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, FOOD_SIZE, FOOD_SIZE), 0)


#STEP 6
#Lets create the snake class
#Remember to initialize it we have to create this init function.
#We have to have the parameters of self, an x value, and a y value
class Snake:
    def __init__(self,x,y):
        #So we initalize the snakes x and y location to the x and y passed in and
        #set the direction of the snake to right
        self.x = x
        self.y = y
        self.direction = KEY["RIGHT"]

        #We're going to create a list to hold all the snakes body
        self.bodyStack = []
        #adding the first snake cell to the list of cells
        self.bodyStack.append(self)

        #We're going to create an end cell to separate the body cells, we create the end cell to the left of the head
        endCell = Cell(x - SEPERATION,y)
        #We dont want a color so we don't show it on the graph
        endCell.color = "NULL"
        #Make the end cell the same direction as the head.
        endCell.direction = KEY["RIGHT"]
        #Then we add the cell to body list
        self.bodyStack.append(endCell)

    #STEP 7
    #Lets create a function to move the snake
    def move(self):
        #So we're going to calculate the length of the snake - 1, since arrays start from 0 the last index will be
        #the length of the snake - 1
        lastCell = len(self.bodyStack) - 1

        #We're going to write  a while loop to iterate through all the snakes body cells from the end to the front of the snake.
        #While we are not at the head of the snake lets go through every cell and make sure it is going in the direction of the
        #previous cells and move that cell to the location of the cell in front of it. Then we decrease the cell index we are on.
        while(lastCell != 0):
            self.bodyStack[lastCell].direction = self.bodyStack[lastCell - 1].direction
            self.bodyStack[lastCell].x = self.bodyStack[lastCell - 1].x
            self.bodyStack[lastCell].y = self.bodyStack[lastCell - 1].y
            lastCell -= 1
        #we check if the body is less than 2 so we know its just the head, but if not
        #then we pop out the head of the list
        if(len(self.bodyStack) < 2):
            headCell = self
        else:
            headCell = self.bodyStack.pop(lastCell)

        #Now lets create some if-else statements to check if a new direction was inputted.
        #We have to access the snakes bodystack and check the new direction
        #If the direction is up then we set the y coordinate of the head above the second cell
        #If the direction is right then we set the x coordinate of the head to the right of the second cell
        #If the direction is down then we set the y coordinate of the head below the second cell
        #If the direction is left then we set the y coordinate of the head to the left of the second cell
        #I used fps * movement speed to make it relative to how fast you want your snake to go
        if(self.bodyStack[0].direction == KEY["UP"]):
            headCell.y = self.bodyStack[0].y - (FPS * MOVEMENT_SPEED)
        elif(self.bodyStack[0].direction == KEY["RIGHT"]):
             headCell.x = self.bodyStack[0].x + (FPS * MOVEMENT_SPEED)
        elif(self.bodyStack[0].direction == KEY["DOWN"]):
            headCell.y = self.bodyStack[0].y + (FPS * MOVEMENT_SPEED)
        elif(self.bodyStack[0].direction == KEY["LEFT"]):
            headCell.x = self.bodyStack[0].x - (FPS * MOVEMENT_SPEED)

        #We then insert the head back into the front of the snakes list
        self.bodyStack.insert(0, headCell)

    #STEP 8
    #So we can create a grow function so when your snake eats food it can grow
    def grow(self):
        #Again we're going to get the length of the snake and substract 1 so we can access the array
        lastCell = len(self.bodyStack) - 1
        #Lets check the last cells direction and create a newcell, but also a endcell to add sepration.
        #We check if the direction is up,down,right, or left and depending on which direction it is we
        #create the new cell and end cell in the right place.
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

        #We're going to set the color to NULL for endcells so we dont see it in the window
        endCell.color = "NULL"
        #We then append the cells to the body list of the snake
        self.bodyStack.append(newCell)
        self.bodyStack.append(endCell)

    #STEP 9
    #We're going to define a draw function to draw our snake.
    #We're going to have the parameters as self and a screen we can draw on
    def draw(self, screen):
        #We're going to call pygame.draw.rect which takes in a screen, a color for what we want our cell to be
        #then a tuple of (an x position, a y position, a size, and a size) and then a width
        #We're going to call this first for our head cell
        pygame.draw.rect(screen, pygame.Color("gold"), (self.bodyStack[0].x, self.bodyStack[0].y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE), 0)
        #starting with our first cell
        cellCount = 1

        #while loop to go through all the cells in the body
        while(cellCount < len(self.bodyStack)):
            #We're going to check if the cells color is null and if it is we're going to increase the count and continue
            #to the next iteration
            if(self.bodyStack[cellCount].color == "NULL"):
                cellCount += 1
                continue
            #if the color is not null we're going to draw a rectangle again using the cells positions, the screen, and any color you want
            #Then increase the cell count.
            pygame.draw.rect(screen, pygame.Color("green"), (self.bodyStack[cellCount].x, self.bodyStack[cellCount].y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE), 0)
            cellCount += 1

    #STEP 11
    #Now we're going to write a function to check for self crashing
    def checkCrash(self):
        #Going to start the count at 1 so we can go through the snakes body cells again
        cellCount = 1

        #Lets write a while loop to go through the snakes body cells
        while(cellCount < len(self.bodyStack)-1):

            #Lets write an If statement which uses the collision method we created earlier to check if the head is crashing with any of the cells
            #However we ony want to check if the head is crashing with the cells that are colored and not the separation cells.
            #If they are colliding then we return True
            #lets increease the cellcount by 1 everytime
            if(checkCollision(self.bodyStack[0], SNAKE_BLOCK_SIZE, self.bodyStack[cellCount], SNAKE_BLOCK_SIZE) == True and self.bodyStack[cellCount].color != "NULL"):
                return True
            cellCount += 1
        #if we get out of the while loop this means we should return false and that the snake is not crashing into itself
        return False

    #STEP 12
    #We're going to create a function to change directions
    #The parameters are going to be self and a direction
    def changeDirection(self, direction):
        #We're going to check if the current direction is up or down and the new direction is opposite we aren't going to change directions
        if(self.direction == KEY["UP"] and direction == KEY["DOWN"] or self.direction == KEY["DOWN"] and direction == KEY["UP"]):
            pass
        #going to do the same for right and left
        if(self.direction == KEY["RIGHT"] and direction == KEY["LEFT"] or self.direction == KEY["LEFT"] and direction == KEY["RIGHT"]):
            pass
        #if the new direction isn't opposite of the current direction then we change the direction
        self.direction = direction

#STEP 10
#Next we're going to check for collisions with the food
#So lets create a function that takes in postionA, a size, positionB, and a size.
def checkCollision(positionA, sizeA, positionB,sizeB):
    #We're going to check if positionA's x is less than positionB's.x + size of B
    #and is positonAs x + sizeA is greater than positionBs x
    #and if positionA y is less than positionBs y + size B
    #and if positionA y is + size A is greater than position B y
    #If all those are true then return true if not then return false
    if(positionA.x < positionB.x+sizeB and positionA.x + sizeA > positionB.x and positionA.y < positionB.y + sizeB and positionA.y + sizeA > positionB.y):
        return True
    return False

#STEP 13
#Lets write a function to check for the snake crashing into the sides of the screen
#we're going to have the prarameters of positionA and a size A
def crashing(positionA, sizeA):

    #We're going to check if positionAs x - the size a is less than 0
    #or if the positionAs x + size a is greater than the screen width
    #or if the positionAs y - size A is less than 0
    #or if the positionAs y + size A is greater than the screen height
    #if any of these are true then we return true
    #if not then return false
    if(positionA.x - sizeA < 0 or positionA.x + sizeA > SCREEN_WIDTH or positionA.y - sizeA < 0 or positionA.y + sizeA > SCREEN_HEIGHT):
        return True
    return False

#STEP 15
#We're now going to create the function to spawn a single food
#The parameters are going to be the food list, and the snakes x and y coordinates
def spawnSingleFood(food, sx, sy):
    #We're going to delete the list of food since we don't want to add more food to list, we only want one.
    del food[:]

    #We're going to get a random x and y by using random uniform
    #we're going to pass in the food size plus a constant 5 and the screen height/width - food size - 5
    x = random.uniform(FOOD_SIZE + 5,SCREEN_WIDTH - FOOD_SIZE - 5)
    y = random.uniform(FOOD_SIZE + 5, SCREEN_HEIGHT - FOOD_SIZE - 5)

    #We're going to check that the food has not spawned on top of the snake already
    #If the x and y coordinates are on the snakes head then we create new x and y coordinates
    while(x-FOOD_SIZE == sx or x+FOOD_SIZE == sx and y-FOOD_SIZE == sy or y + FOOD_SIZE == sy):
            x = random.uniform(20,SCREEN_WIDTH - 20)
            y = random.uniform(20, SCREEN_HEIGHT - 20)

    #we then add the food to the list by creating a new food with the state as 1 to show that its not eaten.
    #We also pass in the x and y coordinates into the food constructor
    food.append(Food(x,y,1))

#STEP 16
#Next lets draw the function to draw the score where we pass in a score
def drawScore(score):
    #set up some variables to use the fonts we made earlier and render them
    #we have to use the variable str(score) to make the score a string, remember you can make whatever color you want it
    #you can also change that 1 to a 0 if you want
    msg_score = score_number_font.render(str(score),1,pygame.Color("green"))
    #we have to use screen.blit() to add a screen onto the window
    screen.blit(score_message, (SCREEN_WIDTH - text_font.size("Score")[0] - 60, 10))
    screen.blit(msg_score, (SCREEN_WIDTH - 40, 10))

#STEP 18
def gameEnd():
    msg = text_font.render("Game Over",1,pygame.Color("white"))
    play_again = text_font.render("Play Again? Y/N",1,pygame.Color("green"))
    screen.blit(msg,(SCREEN_WIDTH/2 - text_font.size("Game Over")[0]/2,SCREEN_HEIGHT/2))
    screen.blit(play_again,(SCREEN_WIDTH/2 - text_font.size('Play Again? Y/N')[0]/2,SCREEN_HEIGHT/2+40))

    pygame.display.flip()
    pygame.display.update()

    myKey = getPressedKey()
    while(myKey != "exit"):
        if(myKey == "yes"):
            main()
        elif(myKey == "no"):
            break
        myKey = getPressedKey()
        clock.tick(FPS)
    sys.exit()
main()
