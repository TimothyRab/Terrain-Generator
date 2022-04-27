import pygame, math


# Matricies Multiplication Functions
import pygame, math, random


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

Projection = ((1,0,0),(0,1,0),(0,0,0))






#Draw window.
Length = 800
WINDOW = pygame.display.set_mode((Length + 10,Length + 10))


# Set up the grid. Depth is not yet added.


# Manipulate the points in 3D space, before projecting them to the Window.

def ManipulatePoints(x,y,z,rotx,roty,rotz):
    XYZ = (x,y,z)
    XYZ = MatriciesMultiply(RotationX(rotx), XYZ)
    XYZ = MatriciesMultiply(RotationY(roty), XYZ)
    XYZ = MatriciesMultiply(RotationZ(rotz), XYZ)
    XYZ = MatriciesMultiply(Projection, XYZ)
    return XYZ

# Draw the Line from the points that have been manipulated.
def DrawLine(Point1,Point2):
    Half = Length / 2

    pygame.draw.line(WINDOW, (255,0,255), (Point1[0] + Half,Point1[1] + Half),(Point2[0] + Half,Point2[1] + Half))


# Draws the grid by getting and manipulating points in 3D space, projecting them into 2D space and then joining them with a line.

def DrawGrid(rotx,roty,rotz):
    pygame.Surface.fill(WINDOW, (0,0,0))
    scale = 40
    HalfLength = (Length / scale) / 2
    x = -1 * HalfLength
    y = -1 * HalfLength
    
    while y < HalfLength:
        x = -1 * HalfLength
        while x < HalfLength:
            # Draw horizontal line
            Point1 = ManipulatePoints((scale * x), (scale * y), 1,rotx,roty,rotz)
            Point2 = ManipulatePoints((scale * (x + 1)), (scale * y), 1,rotx,roty,rotz)
            DrawLine(Point1, Point2)

            # Draw vertical line

            Point1 = ManipulatePoints((scale * x), (scale * y), 1,rotx,roty,rotz)
            Point2 = ManipulatePoints((scale * x), (scale * (y + 1)), 1,rotx,roty,rotz)
            DrawLine(Point1, Point2)
            
            # Create diagonal line

            Point1 = ManipulatePoints((scale * (x + 1)), (scale * (y + 1)), 1,rotx,roty,rotz)
            Point2 = ManipulatePoints((scale * x), (scale * y), 1,rotx,roty,rotz)
            DrawLine(Point1, Point2)

            x += 1

            
        Point1 = ManipulatePoints((scale * x), (scale * y), 1,rotx,roty,rotz)
        Point2 = ManipulatePoints((scale * (x + 1)), (scale * y), 1,rotx,roty,rotz)
        DrawLine(Point1, Point2)


        Point1 = ManipulatePoints((scale * x), (scale * y), 1,rotx,roty,rotz)
        Point2 = ManipulatePoints((scale * x), (scale * (y + 1)), 1,rotx,roty,rotz)
        DrawLine(Point1, Point2)
    
        y += 1
    
        
    
    

    
    

    



    
    

        
    

DrawGrid(math.pi/3,0,0)






# Draw and update window loop
def main():

    run = True
    rotation = 0
    while run:

        
        pygame.display.flip()   
        
        #if rotation != 1:
        #   rotation += 0.01
        #DrawGrid(rotation,0,0)


        #pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


main()




# Test values
ma = ((1,0,1),(1,0,1),(1,0,1))import pygame, math
import pygame, math


# Matricies Multiplication Functions

# Test values

# Multiply Matricies Function. Requires [][] even when there is a sole value in a list.
# Literally walk through the proccess step by step. without music. It's simple, you just have to walk through it yourself
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



def RotationZ(angle):
    rotationZ = ((math.cos(angle),-1 * math.sin(angle),0), (math.sin(angle),math.cos(angle), 0), (0,0,1))
    return rotationZ

def RotationX(angle):
    rotationX = ((1,0,0), (0,math.cos(angle),-1 * math.sin(angle)), (0,math.sin(angle),math.cos(angle)))
    return rotationX

def RotationY(angle):
    rotationY = ((math.cos(angle),0,math.sin(angle)), (0,1,0), (-1 * math.sin(angle),0,math.cos(angle)))
    return rotationY

Projection = ((1,0,0),(0,1,0),(0,0,0))






#Draw window.
Length = 800
WINDOW = pygame.display.set_mode((Length,Length))


# Set up the grid. Perspective and 3D is not yet added.


rotation = 180
def draw(rotation):
    pygame.Surface.fill(WINDOW, (0,0,0))
    scale = 20
    x = -1 * (Length / scale)
    y = -1 * (Length / scale)
    
    while y < Length / scale:
        x = 0
        while x < Length / scale:

         # Draw horizontal line
            Point1 = MatriciesMultiply(RotationY(rotation), (scale * x, scale * y,1))
            Point2 = MatriciesMultiply(RotationY(rotation), (scale * (x + 1), scale * y,1))
        
            Point1 = MatriciesMultiply(Projection, Point1)
            Point2 = MatriciesMultiply(Projection, Point2)

            pygame.draw.line(WINDOW,(255,0,255),(Point1[0] + Length/2,Point1[1] + Length/2),(Point2[0] + Length/2,Point2[1] + Length/2))

            # Draw vertical line
            Point1 = MatriciesMultiply(RotationY(rotation), (scale * x, scale * y,1))
            Point2 = MatriciesMultiply(RotationY(rotation), (scale * x, scale * (y + 1),1))

            Point1 = MatriciesMultiply(Projection, Point1)
            Point2 = MatriciesMultiply(Projection, Point2)

            pygame.draw.line(WINDOW,(255,0,255),(Point1[0] + Length/2,Point1[1] + Length/2),(Point2[0] + Length/2,Point2[1] + Length/2))







            x += 1
        y += 1
    

draw(0)






# Draw and update window loop
def main():

    run = True
    rotation = 0
    while run:

        
        pygame.display.flip()   
        #if rotation != 360:
        #    rotation += 0.1
        #draw(rotation)

        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


main()





# Matricies Multiplication Functions

# Test values

# Multiply Matricies Function. Requires [][] even when there is a sole value in a list.
# Literally walk through the proccess step by step. without music. It's simple, you just have to walk through it yourself
def MatriciesMultiply(ma,mb):
    rowa = len(ma[0])
    cola = len(ma)
    colb = len(ma)

    mc = [1,1,1]

    i = 0
    while i < colb:
        j = 0
        amount = 0
        while j < rowa:
            amount += mb[i] * ma[i][j]
            j += 1
            print(amount)
        mc[i] = amount
        print(mc[i])
        i += 1


    return mc



def RotationZ(angle):
    rotationZ = ((math.cos(angle),-1 * math.sin(angle),0), (math.sin(angle),math.cos(angle), 0), (0,0,1))
    return rotationZ

def RotationX(angle):
    rotationX = ((1,0,0), (0,math.cos(angle),-1 * math.sin(angle)), (0,math.sin(angle),math.sin(angle)))
    return rotationX

def RotationY(angle):
    rotationY = ((math.cos(angle),0,math.sin(angle), (0,1,0), (-1 * math.sin(angle),0,math.cos(angle))))
    return rotationY()

Projection = ((1,0,0),(0,1,0),(0,0,0))

XYZ = (1,1,1)
# end
mc = MatriciesMultiply(RotationX(54), XYZ)
mc = MatriciesMultiply(Projection, mc)
print(mc)
#Draw window.

WINDOW = pygame.display.set_mode((800,800))


# Set up the grid. Perspective and 3D is not yet added.
x = 0
y = 0
scale = 20
col = 800 / scale
row = 800 / scale
colour = 10
while x < col:
    
    while y < row:
        #horizontal
        pygame.draw.line(WINDOW,(colour,0,colour),(x * scale, y * scale), ((x + 1) * scale, y * scale))
        
        #vertical
        pygame.draw.line(WINDOW,(colour,0,colour),(x * scale, y * scale), (x * scale, (y + 1) * scale))
        
        #diagonal
        pygame.draw.line(WINDOW,(colour,0,colour),((x + 1) * scale, y * scale), (x * scale, (y + 1) * scale))
        colour += 4
       
        y += 1
    colour = 0
    x += 1

    y = 0


# Draw and update window loop
def main():

    run = True
    
    while run:

        
        pygame.display.flip()   




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


main()




mb = ((0.1,1),(1,1),(1,1))

# Multiply Matricies Function. Requires [][] even when there is a sole value in a list.
def MatriciesMultiply(ma,mb):
    rowa = len(ma[0])
    cola = len(ma)
    rowb = len(mb[0])
    colb = len(mb)

    if colb != rowa:
        print("Error, columns don't match rows")
        return ["NOT A FUNCTION"]

    mc = []
    
    i = 0
    while i != cola:
        l = 0
        mc.append([])
        while l != rowb:
            mc[i].append(1)
            l += 1

        j = 0
        while j != rowb:
            amount = 0
            k = 0
            while k != rowa:

                amount += ma[i][k] * mb[k][j]
                print(amount)
                k += 1

            mc[i][j] = amount

            j += 1
        
        i += 1

    return mc

# Test the function
mc = MatriciesMultiply(ma, mb)
print(mc)

# WIP angles. Typing error. Will check tommorrow.
angle = 1
rotationZ = [[math.cos(angle),-1 * math.sin(angle),0],
             [math.sin(angle),math.cos(angle), 0]
             [0,0,1]]

rotationX = ((1,0,0),
             (0,math.cos(angle),-1 * math.sin(angle),)
             (0,math.sin(angle),math.sin(cos)))

rotationY = ((math.cos(angle),0,math.sin(angle),(0,1,0),(-1 * math.sin(angle),0,math.cos(angle))))
# end

#Draw window.

WINDOW = pygame.display.set_mode((800,800))


# Set up the grid. Perspective and 3D is not yet added.
x = 0
y = 0
scale = 20
col = 800 / scale
row = 800 / scale
colour = 10
while x < col:
    
    while y < row:
        #horizontal
        pygame.draw.line(WINDOW,(colour,0,colour),(x * scale, y * scale), ((x + 1) * scale, y * scale))
        
        #vertical
        pygame.draw.line(WINDOW,(colour,0,colour),(x * scale, y * scale), (x * scale, (y + 1) * scale))
        
        #diagonal
        pygame.draw.line(WINDOW,(colour,0,colour),((x + 1) * scale, y * scale), (x * scale, (y + 1) * scale))
        colour += 4
       
        y += 1
    colour = 0
    x += 1

    y = 0


# Draw and update window loop
def main():

    run = True
    
    while run:

        
        pygame.display.flip()   




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


main()



