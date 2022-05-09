import pygame, math, random
from perlin_noise import PerlinNoise

# +++++++++++ TO DO ++++++++++++
# Smart optimizations for rendering, compute less math, especially math that would otherwise be wasted
# == Check tile sizes and scale. Possible optimization opportunity?
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


# Rotation and Projection Matricies
def RotationZ(rotation):
    rotationZ = ((math.cos(rotation), -1 * math.sin( rotation),0), (math.sin(rotation),math.cos(rotation), 0), (0,0,1))
    return rotationZ

def RotationX(rotation):
    rotationX = ((1,0,0), (0,math.cos(rotation),-1 * math.sin(rotation)), (0,math.sin(rotation),math.cos(rotation)))
    return rotationX

def RotationY(rotation):
    rotationY = ((math.cos(rotation),0,math.sin(rotation)), (0,1,0), (math.sin(rotation),0,math.cos(rotation)))
    return rotationY

def Projection(point):

    Projection = ((1 / (distance - point[2]),0,0),(0,1 / (distance - point[2]),0),(0,0,0))
    return Projection


def PreCalcRot(rotation):
    rotlist = []
    rotlist.append(RotationX(rotation[0]))
    rotlist.append(RotationY(rotation[1]))
    rotlist.append(RotationZ(rotation[2]))
    return rotlist

#Draw window.
Length = 800
Window = pygame.display.set_mode((Length, Length))
Half = (Length / 2)
FOV = 100

# Manipulate the points in 3D space, before projecting them to the Window.

def ManipulatePoints(point,rotation,translation):


    point = MatriciesMultiply(rotation[0], point)
    point = MatriciesMultiply(rotation[1], point)
    point = MatriciesMultiply(rotation[2], point)

    point[0] += translation[0]
    point[1] += translation[1]
    point[2] += translation[2]

    point = MatriciesMultiply(Projection(point),point)

    point[0] = point[0] * FOV + Half
    point[1] = point[1] * FOV + Half
    
    return point

# Draw the Line from the points that have been manipulated.

def DrawLine(Point1,Point2, colour):

    if (Point1[1] < Length or Point2[1] < Length) and( Point1[0] < Length or Point2[0] < Length) and (Point1[0] > 0 or Point2[0] > 0):
        pygame.draw.line(Window, colour, (Point1[0],Point1[1]),(Point2[0],Point2[1]))


# Function for the points of the ship, joining and drawing the ship and representing it on the screen.

def Ship(translation,rotation,colour):

    Coord1 = ((-0.25,0,0.5),(0.25,0,0.5),(-0.25,0,-0.5),(0.25,0,-0.5),
              (-0.25,0.1,0.5),(0.25,0.1,0.5),(-0.25,0.1,-0.5),(0.25,0.1,-0.5),
              (-0.5,0.05,-0.5),(0.5,0.05,-0.5),(-0.25,0.05,0),(0.25,0.05,0),
               (-0.1,0,1), (0.1,0,1))
    
    Coord2 = []
    i = 0
    while i < len(Coord1):
        
        Coord2.append(ManipulatePoints(Coord1[i],PreCalcRot(rotation),translation))
        i += 1

    DrawLine(Coord2[1], Coord2[3], colour)
    DrawLine(Coord2[0], Coord2[1], colour)
    DrawLine(Coord2[2], Coord2[0], colour)
    DrawLine(Coord2[2], Coord2[3], colour)
    
        # Top
    DrawLine(Coord2[5], Coord2[7], colour)
    DrawLine(Coord2[7], Coord2[6], colour)
    DrawLine(Coord2[4], Coord2[5], colour)
    DrawLine(Coord2[6], Coord2[4], colour)

        # Corner
    DrawLine(Coord2[3], Coord2[7], colour)
    DrawLine(Coord2[2], Coord2[6], colour)
    DrawLine(Coord2[1], Coord2[5], colour)
    DrawLine(Coord2[0], Coord2[4], colour)

        # Wing
    DrawLine(Coord2[3],Coord2[9],colour)
    DrawLine(Coord2[7],Coord2[9],colour)

    DrawLine(Coord2[6],Coord2[8],colour)
    DrawLine(Coord2[2],Coord2[8],colour)

    DrawLine(Coord2[8],Coord2[10],colour)
    DrawLine(Coord2[9],Coord2[11],colour)

        # Cockpit
    DrawLine(Coord2[0],Coord2[12],colour)
    DrawLine(Coord2[1],Coord2[13],colour)
    DrawLine(Coord2[4],Coord2[12],colour)
    DrawLine(Coord2[5],Coord2[13],colour)
    DrawLine(Coord2[12],Coord2[13],colour)
    
   # return XYHitbox


# Parameters for the scale of the grid and amount of squares on both axis

scalez = 20
scalex = 20
tilesize = 2

# Draws the grid by getting and manipulating points in 3D space, projecting them into 2D space and then joining them with a line.

def DrawGrid(translation,rotation):
    x = 0
    y = translation[1]
    z = 0
    Coordinates = []
    rotation = PreCalcRot(rotation)
    while z < scalez:

        x = -1 * scalex

        while x < scalex:

            zcornerplus = z + tilesize
            xcornerplus = x + tilesize

            translation[1] = y + 7 * noise([x/10,z / 10])
            Coordinates.append(ManipulatePoints((x, 0, z),rotation,translation))
            
            translation[1] = y + 7 * noise([xcornerplus/10,z / 10])
            Coordinates.append(ManipulatePoints((xcornerplus, 0, z),rotation,translation))

            translation[1] = y + 7 * noise([x/10,zcornerplus / 10])
            Coordinates.append(ManipulatePoints((x, 0, zcornerplus),rotation,translation))

            x += tilesize
    
        z += tilesize
    
    i = 0
    while i != len(Coordinates):
        DrawLine(Coordinates[i],Coordinates[i + 1],(255,0,255))
        DrawLine(Coordinates[i],Coordinates[i + 2],(255,0,255))
        if i < len(Coordinates) - (scalex * 3):
            #540
            DrawLine(Coordinates[i],Coordinates[i + (scalex * 3) + 1],(255,0,255))
        i += 3


# Draw a rotating reticle on the screen

def Reticle(Mouse,angle):

    angle = angle / 10

    Coord1 = ((0,0.05,0),(0,0.2,0),(0.05, 0.2,0))
    Translation = ((Mouse[0] / Length - 0.5) * 7,(Mouse[1] / Length - 0.5) * 7,0)
    i = 0
    while i < 4:
        Rotation = PreCalcRot((0,0,i * math.pi / 2 + angle))
        DrawLine(ManipulatePoints(Coord1[0], Rotation, Translation), ManipulatePoints(Coord1[1], Rotation, Translation), (0,170,255))
        DrawLine(ManipulatePoints(Coord1[0], Rotation, Translation), ManipulatePoints(Coord1[2], Rotation, Translation), (0,170,255))
        DrawLine(ManipulatePoints(Coord1[1], Rotation, Translation), ManipulatePoints(Coord1[2], Rotation, Translation), (0,170,255))
        i += 1
        
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

# Draw and update window loop
def main():

    run = True
    timer = -10
    pygame.mouse.set_visible(False)

    while run:
        pygame.Surface.fill(Window,(50,0,50))

        Mouse = pygame.mouse.get_pos()
        

        timer += 1

        #Terrain
        DrawGrid([0,3,0],(2.6,0,0))

        Reticle(Mouse,timer)
        player.update(Mouse)

        pygame.display.flip()  

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()




main()



