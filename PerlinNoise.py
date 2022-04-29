import pygame, math, random
from perlin_noise import PerlinNoise


noise = PerlinNoise()
array = [0]
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
            amount += mb[i] * ma[i][j]
            j += 1
        mc[i] = amount
        i += 1

    return mc


# Rotation and Projection Matricies
def RotationZ(rotz):
    rotationZ = ((math.cos(rotz),-1 * math.sin(rotz),0), (math.sin(rotz),math.cos(rotz), 0), (0,0,1))
    return rotationZ

def RotationX(rotx):
    rotationX = ((1,0,0), (0,math.cos(rotx),-1 * math.sin(rotx)), (0,math.sin(rotx),math.cos(rotx)))
    return rotationX

def RotationY(roty):
    rotationY = ((math.cos(roty),0,math.sin(roty)), (0,1,0), (-1 * math.sin(roty),0,math.cos(roty)))
    return rotationY


distance = 1.7

def Projection(z):

    Projection = ((1 / (distance - z),0,0),(0,1 / (distance - z),0),(0,0,0))
    return Projection






#Draw window.
Length = 800
Window = pygame.display.set_mode((Length , Length + 300))
Half = (Length / 2)
Zoom = 160

# Set up the grid. Depth is not yet added.


# Manipulate the points in 3D space, before projecting them to the Window.

def ManipulatePoints(x,y,z,rotx,roty,rotz):
    XYZ = (x,y,z)

    XYZ = MatriciesMultiply(RotationX(rotx), XYZ)
    XYZ = MatriciesMultiply(RotationY(roty), XYZ)
    XYZ = MatriciesMultiply(RotationZ(rotz), XYZ)
    XYZ = MatriciesMultiply(Projection(XYZ[2]), XYZ)
    XYZ[0] = XYZ[0] * Zoom + Half
    XYZ[1] = XYZ[1] * Zoom + Half
    return XYZ

# Draw the Line from the points that have been manipulated.

def DrawLine(Point1,Point2, colour):

    if Point1[0]< Length + 100:
        if Point2[0] < Length + 100:
            if Point1[0] > - 80:
                if Point2[0] > - 80:
                    if Point1[1] < Length + 350:
                        if Point2[1] < Length + 350:
                            pygame.draw.line(Window, colour, (Point1[0],Point1[1]),(Point2[0],Point2[1]))

    


# Draws the grid by getting and manipulating points in 3D space, projecting them into 2D space and then joining them with a line.


scalez = 24
scalex = 22
tilesize = 2

def Ship(x,y,z,rotx,roty,rotz):
    
    Coord1 = ((-0.2,0,0,2.6,0,0),(0.2,0,0,2.6,0,0),(-0.2,0,-2,2.6,0,0),(0.2,0,-2,2.6,0,0),
              (-0.2,0.1,0,2.6,0,0),(0.2,0.1,0,2.6,0,0),(-0.2,0.1,-2,2.6,0,0),(0.2,0.1,-2,2.6,0,0),
              (-0.5,0.05,-2,2.6,0,0),(0.5,0.05,-2,2.6,0,0),(-0.2,0.05,0,2.6,0,0),(0.2,0.05,0,2.6,0,0))
    Coord2 = []
    i = 0
    while i < len(Coord1):

        Coord2.append(ManipulatePoints(Coord1[i][0] + x,Coord1[i][1] + y,Coord1[i][2] + z,Coord1[i][3] + rotx,Coord1[i][4] + roty,Coord1[i][5] + rotz))
        #print(Coord2[i])
        i += 1
    
    colour = (0,170,255)

    # Base
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



def TerrainNoise(x,y,z):
    tn = y + (7 * noise([x/10,(z + array[0]) / 10]))
    return tn

def DrawGrid(x,y,z,rotx,roty,rotz):
    pygame.Surface.fill(Window,(50,0,50))
    
    colour = 255
    while z < scalez:

        x = -1 * scalex
        
        colour -= 15
        while x < scalex:
            
            
            # Draw horizontal line
            Point1 = ManipulatePoints(x, TerrainNoise(x,y,z), z,rotx,roty,rotz)
            Point2 = ManipulatePoints(x + tilesize, TerrainNoise(x + tilesize,y,z), z,rotx,roty,rotz)
            
            DrawLine(Point1, Point2, (colour,0,colour))

            # Draw vertical line

            Point1 = ManipulatePoints(x, TerrainNoise(x,y,z), z,rotx,roty,rotz)
            Point2 = ManipulatePoints(x, TerrainNoise(x,y,z + tilesize), z + tilesize,rotx,roty,rotz)
            
            DrawLine(Point1, Point2, (colour,0,colour))
            
            # Create diagonal line

            Point1 = ManipulatePoints(x + tilesize, TerrainNoise(x + tilesize,y,z + tilesize), z + tilesize,rotx,roty,rotz)
            Point2 = ManipulatePoints(x, TerrainNoise(x,y,z), z,rotx,roty,rotz)
            
            DrawLine(Point1, Point2, (colour,0,colour))

            x += tilesize
    
        z += tilesize



# Draw and update window loop
def main():

    run = True
    change = 0
    while run:
        
        pygame.display.flip()   
        
        change += 0.1
        
        DrawGrid(0,-5,-1,2.6,0,0)
        Ship(1,-0.5,change,0,0,0)
        pygame.draw.line(Window,(155,155,155),(0,800),(800,800))
        pygame.draw.line(Window,(155,155,155),(800,0),(800,800))

        array[0] += 0.1

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()




main()



