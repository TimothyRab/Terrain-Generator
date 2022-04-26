import pygame, math


# Matricies Multiplication Functions



ma = ((1,0,5),(1,0,5),(1,0,5))
mb = ((1,1),(1,1),(1,1))


def MatriciesMultiply(ma,mb):
    rowa = len(ma)
    cola = len(ma[0]) 
    colb = len(mb[0])

    if cola != len(mb):
        print("Error, columns don't match rows")
        return ["NOT A FUNCTION"]

    mc = []
    
    
    
    i = 0
    while i != rowa:
       
        l = 0
        mc.append([])
        while l != colb:
            mc[i].append(1)
            l += 1
        #mc.append([1,1])


        j = 0
        while j != colb:
            amount = 0
            k = 0
            while k != cola:
                amount += ma[i][k] * mb[k][j]
                print(amount)
                k += 1

            mc[i][j] = amount

            j += 1
        
        i += 1


    return mc


mc = MatriciesMultiply(ma, mb)
print(mc)




















# end


WINDOW = pygame.display.set_mode((800,800))


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

def main():

    run = True
    
    while run:

        
        pygame.display.flip()   




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


main()



