import pygame, math, random
from perlin_noise import PerlinNoise


# TO DO ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
# Clean up terrain noise code to remove array function.
# Improve culling method, try learning new python code for once 





noise = PerlinNoise()


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



def XYRotation(array,angle):
    sin = math.sin(angle)
    cos = math.cos(angle)

    x = array[0] * cos - array[1] * sin
    y = array[1] * cos + array[0] * sin

    return (x,y)


#Draw window.
Length = 800
Window = pygame.display.set_mode((Length, Length))
Half = (Length / 2)
FOV = 140

# Set up the grid. Depth is not yet added.


# Manipulate the points in 3D space, before projecting them to the Window.

def ManipulatePoints(x,y,z,rotx,roty,rotz):
    XYZ = (x,y,z)

    XYZ = MatriciesMultiply(RotationX(rotx), XYZ)
    XYZ = MatriciesMultiply(RotationY(roty), XYZ)
    XYZ = MatriciesMultiply(RotationZ(rotz), XYZ)
    XYZ = MatriciesMultiply(Projection(XYZ[2]), XYZ)
    XYZ[0] = XYZ[0] * FOV + Half
    XYZ[1] = XYZ[1] * FOV + Half
    return XYZ

# Draw the Line from the points that have been manipulated.

def DrawLine(Point1,Point2, colour):


    if Point1[1] < Length or Point2[1] < Length:
        if Point1[0] < Length or Point2[0] < Length:
            if Point1[0] > 0 or Point2[0] > 0:
                pygame.draw.line(Window, colour, (Point1[0],Point1[1]),(Point2[0],Point2[1]))

    


# Draws the grid by getting and manipulating points in 3D space, projecting them into 2D space and then joining them with a line.




def Ship(x,y,z,rotx,roty,rotz, colour):
    
    Coord1 = ((-0.2,0,0,2.6,0,0),(0.2,0,0,2.6,0,0),(-0.2,0,-0.5,2.6,0,0),(0.2,0,-0.5,2.6,0,0),
              (-0.2,0.1,0,2.6,0,0),(0.2,0.1,0,2.6,0,0),(-0.2,0.1,-0.5,2.6,0,0),(0.2,0.1,-0.5,2.6,0,0),
              (-0.5,0.05,-0.5,2.6,0,0),(0.5,0.05,-0.5,2.6,0,0),(-0.2,0.05,-0.2,2.6,0,0),(0.2,0.05,-0.2,2.6,0,0),
               (-0.1,0.1,0.1,2.6,0,0), (0.1,0.1,0.1,2.6,0,0))
    Coord2 = []
    i = 0
    while i < len(Coord1):

        Coord2.append(ManipulatePoints(Coord1[i][0] + x,Coord1[i][1] + y,Coord1[i][2] + z,Coord1[i][3] + rotx,Coord1[i][4] + roty,Coord1[i][5] + rotz))
        #print(Coord2[i])
        i += 1
    

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

    # Cockpit
    DrawLine(Coord2[0],Coord2[12],colour)
    DrawLine(Coord2[1],Coord2[13],colour)
    DrawLine(Coord2[4],Coord2[12],colour)
    DrawLine(Coord2[5],Coord2[13],colour)
    DrawLine(Coord2[12],Coord2[13],colour)




def TerrainNoise(x,y,z, perlinz):
    tn = y + (7 * noise([x/10,(z + perlinz) / 10]))
    return tn

scalez = 20
scalex = 20
tilesize = 2

def DrawGrid(x,y,z,rotx,roty,rotz, perlinz):
    pygame.Surface.fill(Window,(50,0,50))
    
    colour = 255
    while z < scalez:

        x = -1 * scalex
        
        colour -= 18
        while x < scalex:
            
            
            # Draw horizontal line
            Point1 = ManipulatePoints(x, TerrainNoise(x,y,z,perlinz), z,rotx,roty,rotz)
            Point2 = ManipulatePoints(x + tilesize, TerrainNoise(x + tilesize,y,z, perlinz), z,rotx,roty,rotz)
            
            DrawLine(Point1, Point2, (colour,0,colour))

            # Draw vertical line

            Point1 = ManipulatePoints(x, TerrainNoise(x,y,z,perlinz), z,rotx,roty,rotz)
            Point2 = ManipulatePoints(x, TerrainNoise(x,y,z + tilesize,perlinz), z + tilesize,rotx,roty,rotz)
            
            DrawLine(Point1, Point2, (colour,0,colour))
            
            # Create diagonal line

            Point1 = ManipulatePoints(x + tilesize, TerrainNoise(x + tilesize,y,z + tilesize,perlinz), z + tilesize,rotx,roty,rotz)
            Point2 = ManipulatePoints(x, TerrainNoise(x,y,z,perlinz), z,rotx,roty,rotz)
            
            DrawLine(Point1, Point2, (colour,0,colour))

            x += tilesize
    
        z += tilesize


# (-1 * (Mouse[1] - (Length/2)) / 4000)

def Reticle(Mouse,angle):

    angle = angle / 10

    x = Mouse[0]
    y = Mouse[1]
    i = 0
    while i < 4:
        Line1 = XYRotation((0, -5),angle + ((math.pi / 2) * i))
        Line2 = XYRotation((0,-20), angle + ((math.pi / 2) * i))
        DrawLine((Line1[0] + x,Line1[1] + y),(Line2[0] + x,Line2[1] + y), (0,170,255))

        Line1 = XYRotation((0, -5),angle + ((math.pi / 2) * i))
        Line2 = XYRotation((+5,-20),angle + ((math.pi / 2) * i))
        DrawLine((Line1[0] + x,Line1[1] + y),(Line2[0] + x,Line2[1] + y), (0,170,255))

        Line1 = XYRotation((0, -20),angle + ((math.pi / 2) * i))
        Line2 = XYRotation((+5,-20), angle + ((math.pi / 2) * i))
        DrawLine((Line1[0] + x,Line1[1] + y),(Line2[0] + x,Line2[1] + y), (0,170,255))
        
        i += 1

    



# Draw and update window loop
def main():

    run = True
    change = 0


    while run:

        Mouse = pygame.mouse.get_pos()
        pygame.mouse.set_visible(False)

        change += 1
        # Terrain
        DrawGrid(0,-5,-1,2.6,0,0, change)
        # Enemy Ship
        Ship(0.5,0,1.5,2.6,math.pi / 2,0,(255,0,0))
        Ship(-0.5,0,1.5,2.6,math.pi / 2,0,(255,0,0))
        # Player Character
        Ship(0 + (-1 * (Mouse[0] - (Length/2)) / 400),0 + (-1 * (Mouse[1] - (Length/2)) / 400),-2,2.6,0,0,(0,170,255))

        Reticle(Mouse,change)

        pygame.display.flip()  

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()




main()



