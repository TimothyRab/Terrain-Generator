import pygame, math, random, time
from perlin_noise import PerlinNoise

# +++++++++++ TO DO ++++++++++++
# Smart optimizations for rendering, compute less math, especially math that would otherwise be wasted
# Configure AI to use fixed systems, possibly create more modular and independent functions


noise = PerlinNoise()
distance = 0.9

# Matricies Multiplication Function

def MatriciesMultiply(ma,mb):
    rowa = len(ma[0])
    colb = len(ma)
    mc = [1,1,1]

    i = 0
    while i < colb:
        j = 0
        amount = 0
        while j < rowa:
            amount += mb[j] * ma[i][j]
            j += 1
        mc[i] = amount
        i += 1

    return mc



#Draw window.
Length = 800
Window = pygame.display.set_mode((Length, Length))
Half = (Length / 2)
FOV = 100

# Manipulate the points in 3D space, before projecting them to the Window.

def CalcRot(rotation):
    cosrotX = math.cos(rotation[0])
    sinrotX = math.sin(rotation[0])

    cosrotY = math.cos(rotation[1])
    sinrotY = math.sin(rotation[1])

    cosrotZ = math.cos(rotation[2])
    sinrotZ = math.sin(rotation[2])

    rotlist = [((1,0,0), (0,cosrotX,-1 * sinrotX), (0,sinrotX,cosrotX)),((cosrotY,0,sinrotY), (0,1,0), (sinrotY,0,cosrotY)),((cosrotZ, -1 * sinrotZ,0), (sinrotZ,cosrotZ, 0), (0,0,1))]
    return rotlist


def ManipulatePoints(point,rotation,translation):


    point = MatriciesMultiply(rotation[0], point)
    point = MatriciesMultiply(rotation[1], point)
    point = MatriciesMultiply(rotation[2], point)

    point[0] += translation[0]
    point[1] += translation[1]
    point[2] += translation[2]

    point = MatriciesMultiply(((1 / (distance - point[2]),0,0),(0,1 / (distance - point[2]),0),(0,0,0)),point)

    point[0] = point[0] * FOV + Half
    point[1] = point[1] * FOV + Half
    
    return point






# Draw the Line from the points that have been manipulated.

def DrawLine(Point1,Point2, colour):

    if (Point1[1] < Length or Point2[1] < Length) and( Point1[0] < Length or Point2[0] < Length) and (Point1[0] > 0 or Point2[0] > 0):
        pygame.draw.line(Window, colour, (Point1[0],Point1[1]),(Point2[0],Point2[1]))


# Function for the points of the ship, joining and drawing the ship and representing it on the screen.

def Ship(translation,rotation,colour):

    Coord1 = [(-0.25,0,0.25),(0.25,0,0.25),(-0.25,0,-0.25),(0.25,0,-0.25),
              (-0.25,0.1,0.25),(0.25,0.1,0.25),(-0.25,0.1,-0.25),(0.25,0.1,-0.25),
              (-0.5,0.05,-0.25),(0.5,0.05,-0.25),(-0.25,0.05,0),(0.25,0.05,0),
               (-0.1,0,0.5), (0.1,0,0.5)]

    
    i = 0
    while i < len(Coord1):
        
        Coord1[i] = (ManipulatePoints(Coord1[i],CalcRot(rotation),translation))
        i += 1

    DrawLine(Coord1[1], Coord1[3], colour)
    DrawLine(Coord1[0], Coord1[1], colour)
    DrawLine(Coord1[2], Coord1[0], colour)
    DrawLine(Coord1[2], Coord1[3], colour)
    
    # Top
    DrawLine(Coord1[5], Coord1[7], colour)
    DrawLine(Coord1[7], Coord1[6], colour)
    DrawLine(Coord1[4], Coord1[5], colour)
    DrawLine(Coord1[6], Coord1[4], colour)

    # Corner
    DrawLine(Coord1[3], Coord1[7], colour)
    DrawLine(Coord1[2], Coord1[6], colour)
    DrawLine(Coord1[1], Coord1[5], colour)
    DrawLine(Coord1[0], Coord1[4], colour)

    # Wing
    DrawLine(Coord1[3],Coord1[9],colour)
    DrawLine(Coord1[7],Coord1[9],colour)

    DrawLine(Coord1[6],Coord1[8],colour)
    DrawLine(Coord1[2],Coord1[8],colour)

    DrawLine(Coord1[8],Coord1[10],colour)
    DrawLine(Coord1[9],Coord1[11],colour)

    # Cockpit
    DrawLine(Coord1[0],Coord1[12],colour)
    DrawLine(Coord1[1],Coord1[13],colour)
    DrawLine(Coord1[4],Coord1[12],colour)
    DrawLine(Coord1[5],Coord1[13],colour)
    DrawLine(Coord1[12],Coord1[13],colour)



# Parameters for the scale of the grid and amount of squares on both axis

scalez = 10
scalex = 20
tilesize = 50

# Draws the grid by getting and manipulating points in 3D space, projecting them into 2D space and then joining them with a line.

def DrawGrid(translation,rotation,timer):
    x = scalex / 2 * -1
    y = translation[1]
    z = 0
    Column = []
    rotation = CalcRot(rotation)

    while z < scalez:
        x = scalex / 2 * -1
        Row = []
        while x != scalex / 2 + 1:

            translation[1] = y + tilesize * noise([x/3,(z + timer / 10) / 3])
            point = ManipulatePoints((x * tilesize, 0, z * tilesize),rotation,translation)
            
            colour =  240 - 200 * (z / scalez)
            
            point[2] = (colour,0,colour)
            
            Row.append(point)

            x += 1

        Column.append(Row)
        z += 1

    
    
    z = scalez - 1
    x = scalex


    while z > -1:
        x = scalex
        while x > -1:
            
            if x > 0:
                DrawLine(Column[z][x],Column[z][x - 1],Column[z][x][2])
            if z > 0:
                DrawLine(Column[z][x],Column[z - 1][x],Column[z][x][2])
            if x > 0 and z > 0:
                DrawLine(Column[z][x],Column[z - 1][x - 1],Column[z][x][2])
            x -= 1
            
        z -= 1



# Draw a rotating reticle on the screen

def Reticle(Mouse,angle):

    angle = angle / 10

    Coord1 = ((0,0.05,0),(0,0.2,0),(0.05, 0.2,0))
    Translation = ((Mouse[0] / Length - 0.5) * 8,(Mouse[1] / Length - 0.5) * 8,0)
    i = 0
    while i < 4:
        Rotation = CalcRot((0,0,i * math.pi / 2 + angle))
        DrawLine(ManipulatePoints(Coord1[0], Rotation, Translation), ManipulatePoints(Coord1[1], Rotation, Translation), (0,170,255))
        DrawLine(ManipulatePoints(Coord1[0], Rotation, Translation), ManipulatePoints(Coord1[2], Rotation, Translation), (0,170,255))
        DrawLine(ManipulatePoints(Coord1[1], Rotation, Translation), ManipulatePoints(Coord1[2], Rotation, Translation), (0,170,255))
        i += 1

class EnemyShip():


    def __init__(self,initx,inity,initz):
        self.x = initx
        self.y = inity
        self.z = initz


    

    def update(self, timer):
        
        Ship((self.x,self.y,self.z),(0,math.pi,0),(255,0,0))


# Class for Playership
class PlayerShip():


    def __init__(self,initx,inity,initz):
        self.x = initx
        self.y = inity
        self.z = initz
        self.t = 0

    

    def update(self, Mouse):
        self.t += 0.01
        Ship(((Mouse[0] - (Length/2)) / 400,(Mouse[1] - (Length/2)) / 400,2),(0,0,math.pi),(0,170,255))


player = PlayerShip(0, 0, 0)
enemy = EnemyShip(0,0,2)


# Draw and update window loop
def main():
    last_time = time.time()
    frame = 0
    second = 0
    run = True
    timer = -10
    pygame.mouse.set_visible(False)
    while run:
        
        dt = time.time() - last_time
        last_time = time.time()


        pygame.Surface.fill(Window,(50,0,50))

        Mouse = pygame.mouse.get_pos()
        
        print('FPS: ' + str(round(1 / dt)) + " Frametime: " + str(dt))

        

        timer += 1 * dt * 60

        #Terrain
        DrawGrid([0,30,0.-2],(math.pi/4 * 5,0,0),timer)

        Reticle(Mouse,timer)
        player.update(Mouse)
        enemy.update(timer)

        pygame.display.flip()  

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()




main()



