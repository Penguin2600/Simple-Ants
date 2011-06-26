import ants, time, pygame, random, os, sys, audio

def setup():                #Setup all our lists and establish two ant colonies (RED vs BLU)
    global colonies, trails, foods, text, debug, showtrail, dirty
    colonies = []
    trails = []
    foods = []
    text = []
    colonies.append(ants.Colony("black", 3, 100, 150, 150, WIDTH, HEIGHT, 300))
    colonies.append(ants.Colony("red", 3, 100, 650, 650, WIDTH, HEIGHT, 300))
    debug=False
    showtrail=False

def doinput():                              #Handle input
    global debug, showtrail
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            keys[event.key] = True
        elif event.type == pygame.KEYUP:
            keys[event.key] = False
            
        if keys[pygame.K_ESCAPE]:           # ESC = Quit
            exit(0)
            
        if keys[pygame.K_d]:                # d = Debug text
            debug = not debug

        if keys[pygame.K_t]:                # t = Show Trails 
            showtrail = not showtrail


def update():              #Update all our ants, trails, and foods.
    global colonies, trails, foods, text, debug, showtrail, dirty

    MainSurf.fill([64,157,80])     #blank our background with a pleasant brown.

    if len(trails) > 0:
        for pheromone in trails:        #If there are any trails we need to degrade them over time
            pheromone.update()
            if showtrail:
                pheromone.draw(MainSurf)
            if pheromone.strength < 0.05:   #Trails that grow weak should be removed.
                trails.remove(pheromone)


    for f in foods:      #Update and draw our food blobs.
        f.draw(MainSurf)
        if (f.size <2): foods.remove(f)

    if (len(foods) < 1):    #Place new ones if the current ones are mined out.
        for i in range(2):
            x = 100 + random.random()*(WIDTH-100)
            y = 100 + random.random()*(HEIGHT-100)
            s = (random.random()*20)+20
            foods.append(ants.Food(x,y,s))

    text=[]          #text method only used for debug mode at this point.


    for colony in colonies:  #for each colony we need to go through and update and draw the ants.
        colony.drawhill(MainSurf)
        colony.draw(MainSurf)
        text.append(ants.Text([150,150,150], 10, (colony.x-5, colony.y+30), str(len(colony))))
        colony.update(trails,foods,colonies)
        colony.draw(MainSurf)

        #rough colision for fighting
        pygame.sprite.groupcollide(colonies[0], colonies[1], True, True)
                                   
    for t in text:        #draw any text we have.
        t.draw(MainSurf)

    pygame.display.update()  #draw our new frame


if __name__ == "__main__":

    pygame.init()          #initialize pygame
    clock = pygame.time.Clock()     #start our FPS clock

    #global constants here
    WIDTH=800
    HEIGHT=800
    MainSurf = pygame.display.set_mode([WIDTH, HEIGHT])

    sounds=audio.GameSamples()
    sounds.playsound('music')

    keys = {pygame.K_ESCAPE : False, pygame.K_d : False, pygame.K_t : False} #Declare keys we will use

    setup()             #run our init function

    while 1:                #main loop
        clock.tick(32)      #Limit FPS to 30
        print clock.get_fps()
        doinput()           #Do input functions
        update()            #Do main update routene

    exit(0)
