import pygame, math, random, time
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

    Coord1 = [(-0.25,0,0.5),(0.25,0,0.5),(-0.25,0,-0.5),(0.25,0,-0.5),
              (-0.25,0.1,0.5),(0.25,0.1,0.5),(-0.25,0.1,-0.5),(0.25,0.1,-0.5),
              (-0.5,0.05,-0.5),(0.5,0.05,-0.5),(-0.25,0.05,0),(0.25,0.05,0),
               (-0.1,0,1), (0.1,0,1)]

    
    i = 0
    while i < len(Coord1):
        
        Coord1[i] = (ManipulatePoints(Coord1[i],PreCalcRot(rotation),translation))
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

scalez = 15
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

            x += tilesize
    
        z += tilesize
    
    i = 0
    while i != len(Coordinates):

        #print(i)
        if i  + 1< len(Coordinates) and i + 1 != scalex * round(i / scalex):
            
            DrawLine(Coordinates[i],Coordinates[i + 1],(255,0,0))

        if i + scalex < len(Coordinates):
            DrawLine(Coordinates[i],Coordinates[i + scalex],(0,255,0))

        if i + scalex + 1 < len(Coordinates) and i + 1 != scalex * round(i / scalex):
         DrawLine(Coordinates[i],Coordinates[i + scalex + 1],(0,0,255))
        
        i += 1
        


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
    last_time = time.time()
    run = True
    timer = -10
    pygame.mouse.set_visible(False)

    while run:
        
        dt = time.time() - last_time
        last_time = time.time()
        print(dt * 60)
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



