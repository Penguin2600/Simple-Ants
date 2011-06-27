import ants, time, pygame, random, os, sys, audio

def setup():                #Setup all our lists and establish two ant colonies
    global colonies, trails, foods, text, showtrail, mousevars
    mousevars = [0,0,0,0,0,0,0]
    colonies = []
    trails = []
    foods = []
    text = []
    colonies.append(ants.Colony("black", 3, random.random()*SWIDTH, random.random()*SHEIGHT, 150, SWIDTH, SHEIGHT, 900))
    colonies.append(ants.Colony("red", 3, 100, random.random()*SWIDTH, random.random()*SHEIGHT, SWIDTH, SHEIGHT, 900))
    debug=False
    showtrail=False

def doinput():                              #Handle input
    global showtrail, mousevars
    mousevars[5]=0
    mousevars[6]=0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button < 4:
                mousevars[event.button+1]=0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousevars[event.button+1]=1
            if event.button==4:
                mousevars[5]=1
            if event.button==5:
                mousevars[6]=1
        elif event.type == pygame.MOUSEMOTION:
            mousevars[0]=event.pos[0]
            mousevars[1]=event.pos[1]  
        elif event.type == pygame.KEYDOWN:
            keys[event.key] = True
        elif event.type == pygame.KEYUP:
            keys[event.key] = False
            
        if keys[pygame.K_ESCAPE]:           # ESC = Quit
            exit(0)

        if keys[pygame.K_t]:                # t = Show Trails 
            showtrail = not showtrail



def update():              #Update all our ants, trails, and foods.
    global colonies, trails, foods, text, showtrail
    
    #GameSurface.fill([0,0,0])     #blank our background with a pleasant brown.
    SpriteSurface.fill([64,157,80])     #blank our background with a pleasant brown.
 
    
    if len(trails) > 0:
        for pheromone in trails:        #If there are any trails we need to degrade them over time
            pheromone.update()
            if showtrail:
                pheromone.draw(SpriteSurface)
            if pheromone.strength < 0.05:   #Trails that grow weak should be removed.
                trails.remove(pheromone)


    for f in foods:      #Update and draw our food blobs.
        f.draw(SpriteSurface)
        if (f.size <2): foods.remove(f)

    if (len(foods) < 1):    #Place new ones if the current ones are mined out.
        for i in range(2):
            x = 100 + random.random()*(SWIDTH-200)
            y = 100 + random.random()*(SHEIGHT-200)
            s = (random.random()*20)+20
            foods.append(ants.Food(x,y,s))

    text=[]          #text method only used for debug mode at this point.


    for colony in colonies:  #for each colony we need to go through and update and draw the ants.
        colony.drawhill(SpriteSurface)
        colony.draw(SpriteSurface)
        text.append(ants.Text([150,150,150], 10, (colony.x-5, colony.y+30), str(len(colony))))
        colony.update(trails,foods,colonies)
        colony.draw(SpriteSurface)


                                   
    for t in text:        #draw any text we have.
        t.draw(SpriteSurface)

    pygame.display.update()  #draw our new frame


def doview():
    global mousevars, ScrollX, ScrollY, HEIGHT, WIDTH, SHEIGHT, SWIDTH, Zoom

    print mousevars
    if (mousevars[0] < WIDTH/10):
        ScrollX+=10
            
    if (mousevars[0] > 9*(WIDTH/10)):
        ScrollX-=10

    if (mousevars[1] < HEIGHT/10):
        ScrollY+=10

    if (mousevars[1] > 9*(HEIGHT/10)):
        ScrollY-=10

    if mousevars[5]:
        Zoom+=0.05
        if Zoom >1: Zoom=1
        
    if mousevars[6]:
        Zoom-=0.05
        if Zoom <0.5: Zoom=0.5

    if ScrollX >0: ScrollX=0
    if ScrollX < WIDTH-SWIDTH*Zoom: ScrollX= WIDTH-SWIDTH*Zoom
    if ScrollY >0: ScrollY=0
    if ScrollY < HEIGHT-SHEIGHT*Zoom: ScrollY= HEIGHT-SHEIGHT*Zoom
        
    GameSurface.blit(pygame.transform.smoothscale(SpriteSurface, (int(SWIDTH*Zoom),int(SHEIGHT*Zoom))), (ScrollX,ScrollY))


if __name__ == "__main__":

    pygame.init()          #initialize pygame
    clock = pygame.time.Clock()     #start our FPS clock

    #global constants here
    pygame.display.set_caption('Simple Ants')
    WIDTH=640
    HEIGHT=480
    SWIDTH=WIDTH*2
    SHEIGHT=HEIGHT*2
    Zoom=0.5
    ScrollX=0
    ScrollY=0
    
    pygame.transform.set_smoothscale_backend('SSE')
    
    GameSurface = pygame.display.set_mode([WIDTH, HEIGHT])
    SpriteSurface = pygame.Surface([SWIDTH,SHEIGHT])
    sounds=audio.GameSamples()
    #sounds.playsound('music')

    keys = {pygame.K_ESCAPE : False, pygame.K_d : False, pygame.K_t : False} #Declare keys we will use

    setup()             #run our init function

    while 1:                #main loop
        clock.tick(30)      #Limit FPS to 30
        #print clock.get_fps()
        doinput()           #Do input functions
        update()            #Do main update routene
        doview()            #handle transforms to main view screen
        
    exit(0)
