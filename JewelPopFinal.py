import pygame
from pygame import *
import random
from random import *
import time

#All tests have been removed to improve performance of game

gridHeight = 10 # amount of balls in a column
gridWidth = 8 # amount of balls in a row

cellSize = 60 # both x and y

windowHeight = cellSize*gridHeight + 20 # y
windowWidth = cellSize*gridWidth + 200 # x

screen = pygame.display.set_mode((windowWidth, windowHeight))


background1 = image.load("Background2.jpg")
background1R = background1.get_rect()
background1R = pygame.Surface(screen.get_size())
background1R = background1.convert()

background2 = image.load("Background3.jpg")
background2R = background2.get_rect()
background2R = pygame.Surface(screen.get_size())
background2R = background2.convert()

background3 = image.load("Background4.jpg")
background3R = background3.get_rect()
background3R = pygame.Surface(screen.get_size())
background3R = background3.convert()

background4 = image.load("Background5.jpg")
background4R = background3.get_rect()
background4R = pygame.Surface(screen.get_size())
background4R = background3.convert()


BackG = background1R

ballRadius = 25

grid = []
ballHeights= []

for x in range(gridHeight):
    ballHeights.append(x*cellSize+40)


gBlue = image.load("gBluePF.png")
gGreen = image.load("gGreenPF.png")
gPurple = image.load("gPurplePF.png")
gRed = image.load("gRedPF.png")
gYellow = image.load("gYellowPF.png")
gSilver = image.load("gSilverPF.png")
gOrange = image.load("gOrangePF.png")
gCube = image.load("gCubePF.png")

size=55

gBlue = transform.scale(gBlue, (size,size))
gGreen = transform.scale(gGreen, (size,size))
gPurple = transform.scale(gPurple, (size,size))
gRed = transform.scale(gRed, (size,size))
gYellow = transform.scale(gYellow, (size,size))
gSilver = transform.scale(gSilver, (size,size))
gOrange = transform.scale(gOrange, (size,size))
gCube = transform.scale(gCube, (size,size))


gems = {"blue":gBlue,"green":gGreen, "purple":gPurple, "red":gRed, "yellow":gYellow, "silver":gSilver, "orange":gOrange, "cube":gCube }

gemsList = gems.keys()
gemsList.remove('silver')
gemsList.remove('orange')


colors = {"blue":[0,0,255], "red":[220,20,60], "yellow":[255,255,0],
          "green":[0,205,0], "orange":[255,165,0], "white":[255,255,255]}

#to switch to gems, every 'color' and 'colorList' is now 'gem' and 'gemsList'

colorList = colors.keys()
##colorList.remove('white')

animate = False 

gameScore = 0 # score on the left side of the screen

def pixelsToGrid((x,y)):
    return (x/cellSize, y/cellSize)



# initially fills the grid with randomly colored balls in each cell
def initialFillGrid():
    for i in range(gridWidth):
        column = []
        for j in range(gridHeight):
            gem = choice(gemsList)
            if gem == "cube":
                gem = choice(gemsList)
                if gem == "cube":
                    gem = choice(gemsList)
            column.append((i*cellSize+35, j*cellSize+35, gem, False))
        grid.append(column)


            
#checks if tuples are next to each other and returns True if they are
def nextTo((a,b),(c,d)):
    if (a-c==1 or a-c==-1) and b==d:
        return True
    if a==c and (b-d==1 or b-d==-1):
        return True
    else:
        return False




# findNeighbors uses this function
# returns a list of all neighbors for input
def generateNeighbors((i,j)):
    neighbors = []
    if -1 < i-1:
        neighbors.append((i-1,j))
    if i+1 < 8:
        neighbors.append((i+1,j))
    if -1 < j-1:
        neighbors.append((i,j-1))
    if j+1 < 10:
        neighbors.append((i,j+1))
    return neighbors


def cubeFunc((i,j), gem):
    if gem == "cube":
        x,y,c,r = grid[i][j]
##        neighbors = generateNeighbors((i,j))
        r = True
        grid[i][j] = x,y,c,r
        for a in range(len(grid)):
            for b in range(len(grid[a])):
                x2,y2,c2,r2 = grid[a][b]
                c,d = pixelsToGrid((x2,y2))
                if d==j:
                    r2=True
                grid[a][b] = x2,y2,c2,r2
##        for a,b in neighbors:
##            x2,y2,c2,r2 = grid[a][b]
##            r2 = True
##            grid[a][b] = x2,y2,c2,r2


def findNeighbors((i,j),gem): # recursive fn to mark ready for removal
    if grid[i][j][-2] == gem and gem != "cube": # first check to make sure its the right color
        tracker = False
        neighbors = generateNeighbors((i,j))
        for a,b in neighbors: # mostly for the first time
            if grid[a][b][-2] == gem:
                tracker = True # this means that it is next to one of its color
        if tracker == True:
            x,y,c,r = grid[i][j]
            r = True
            grid[i][j] = (x,y,c,r)
            for a,b in neighbors:
                if grid[a][b][-2] == gem and grid[a][b][-1] == False:
                    findNeighbors((a,b), gem)
                    
    if grid[i][j][-2] == "cube":
        cubeFunc((i,j), grid[i][j][-2])



# goes through every ball, checks to see if it is True (ready to be removed)
# and then removes it and puts an extra ball at the beginning of that list
def replace():
    global gameScore
    for i in range(len(grid)):
        newRow = []
        removed = 0
        for j in range(len(grid[i])):
            if grid[i][j][-1] == True: # skip over if True
                removed += 1
            else: # otherwise, add to the new row
                newRow.append(grid[i][j])
        for n in range(removed): # add in extras for all of the deleted ones
            gem = choice(gemsList)
            if gem == "cube":
                gem = choice(gemsList)
            lastJ = newRow[0][1] # so that they start a cell up from the past ones
            newRow.insert(0,(i*cellSize+35,lastJ-60,gem,False))

        grid[i] = newRow
        gameScore += removed*50

def anyToReplace(): # returns True if any balls are waiting to be replaced
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j][-1] == True:
                return True
    return False


def slideDownNicely(): # the animation!!
    keepGoing = False
    for row in grid:
        for j in range(gridHeight-1,-1,-1): # going backwards through the list
            x,y,gem,r = row[j]
            if y < ballHeights[j]: # if its higher up than it should be...
                y += 2 # bring it down a little
                row[j] = (x,y,gem,r)
                keepGoing = True
    return keepGoing # for animate


# retuns False if there are no adjacent balls of the same color left (game over)
def anyLeft():
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            x,y,gem,r = grid[i][j]
            neighbors = generateNeighbors((i,j))
            for a,b in neighbors:
                if grid[a][b][-2] == gem:
                    return True
    return False


levelChange2=True
levelChange3=True

def levelFunc():
    backG = 1
    level = 1
    if gameScore<5000:
        level = 1
        backG = background1R
    if gameScore>5000 and levelChange2:
        level = 2
        gemsList.append('silver')
        levelChange2 = False
    if gameScore>=5000:
        level = 2
        backG = background2R
    if gameScore>8000 and levelChange3:
        level = 3
        levelChange3 = False
        gemsList.append('orange')
    if gameScore>8000:
        level = 3
        backG = background3R
    screen.blit(backG, (0,0))


#creates opening effect
def startEffect():
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            x,y,gem,r = grid[i][j]
            r = True
            grid[i][j]= x,y,gem,r

            
# do all of this only once
init()
mixer.init()
font.init()
screen = display.set_mode((windowWidth, windowHeight))
screen.fill(colors['white'])
initialFillGrid()
#startEffect() #need to fix error when running

mixer.music.load("Music1EX.mp3") # load and play the game's music
mixer.music.play(-1,10.0)

# keep doing this forever
while True:
    backG = 1
    level = 1

    if gameScore<2500:
        level = 1
        backG = background1R
    if gameScore>=2500:
        backG = background4R
    if gameScore>5000 and levelChange2:
        level = 2
        gemsList.append('orange')
        levelChange2 = False
        # need to add sound "LevelComplete.mp3"
    if gameScore>=5000:
        level = 2
        backG = background2R
    if gameScore>8000 and levelChange3:
        level = 3
        levelChange3 = False
        gemsList.append('silver')
    if gameScore>=8000:
        level = 3
        backG = background3R
    screen.blit(backG, (0,0))

    if animate == True: # if the balls are sliding don't let the user click
        animate = slideDownNicely()
        
    else: # the user is looking for balls to click
        if anyLeft(): # before the game is over.....
            event.get()
            if True in mouse.get_pressed():
                x,y = mouse.get_pos()
                a,b = pixelsToGrid((x,y))
                if a > (gridWidth - 1) or b > (gridHeight - 1): # so there are no out of range issues
                    continue
                findNeighbors((a,b), grid[a][b][-2])
                if anyToReplace() == True:
                    replace()
                    mixer.Sound("Pop.mp3").play #need to make it play and work
                    animate = True # because the replacing is done
        

        else: # if the game is over
            overFont = font.Font(None, 80)
            over = overFont.render("Over", True, colors['red'])
            overRect = over.get_rect(centerx = 560, centery = 250)
            screen.blit(over, overRect)
            game = overFont.render("Game", True, colors['red'])
            gameRect = game.get_rect(centerx = 560, centery = 200)
            screen.blit(game, gameRect)
            time.sleep(3)
            quit()


    # draws all the balls on the screen
    for row in grid:
        for ball in row:
            x,y,gem,b = ball
            if b == True:
                print gem
       #        gem = 'white'
      #      if gem == 'white':
                while size>0:
                #draw.circle(screen, colors[gem], [x,y], ballRadius)
                    gem = transform.scale(gem[gems], (size,size))
                    screen.blit(gems[gem],(x-30,y-30))
                    display.flip()
                    size -= 1
              #  draw.circle(screen, colors[color], [x,y], ballRadius)
            if gem != 'white':
                size = 55
                screen.blit(gems[gem],(x-30,y-30))
        
    # draws the score on the screen
    scoreFont = font.Font(None, 50)
    score = scoreFont.render(str(gameScore), True, colors['white'])
    scoreRect = score.get_rect(centerx = 580, centery = 150)
    levelFont = font.Font(None, 50)
    level = levelFont.render("Level " +str(level), True, colors['white'])
    levelRect = score.get_rect(centerx = 545, centery = 190)
    
    screen.blit(score, scoreRect)
    screen.blit(level, levelRect)
    display.flip()
