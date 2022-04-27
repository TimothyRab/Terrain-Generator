import pygame, math


# Matricies Multiplication Functions

# Test values
ma = ((1,0,1),(1,0,1),(1,0,1))import pygame, math


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



