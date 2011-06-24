import ants, time, pygame, random


def setup():    
    
    # Starts a colony with 30 ants in it.
    global colonies, trails, foodsource, text, debug
    debug=0
    colonies = []
    colonies.append(ants.Colony([0,0,150],10, 150, 150, WIDTH, HEIGHT, 600))
    colonies.append(ants.Colony([150,0,0],10, 650, 650, WIDTH, HEIGHT, 600))
    trails = []
    foodsource = []
    text = []

def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

def doinput():
    global debug
    for event in pygame.event.get():    #check for keypresses 
        if event.type == pygame.KEYDOWN:
            keys[event.key] = True
        elif event.type == pygame.KEYUP:
            keys[event.key] = False
        if keys[pygame.K_ESCAPE]:
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.music.stop()
            exit(0)
        if keys[pygame.K_d]:
            debug+=1
	    if (debug>1): debug=0


            
def update():
    global colonies, trails, foodsource, text
        
    MainSurf.fill([157,107,64])

    if len(trails) > 0:
        for pheromone in trails:
            pheromone.update()
            pheromone.draw(MainSurf)
            if pheromone.strength < 0.05:
                trails.remove(pheromone)

    for f in foodsource:
        f.draw(MainSurf)
        if (f.size <2): foodsource.remove(f)
        
    if (len(foodsource) < 1):
        for i in range(2):
            x = 50 + random.random()*(WIDTH-100)
            y = 50 + random.random()*(HEIGHT-100)
            s = (random.random()*20)+20
            foodsource.append(ants.Food(x,y,s)) 
  
    text=[]
    for colony in colonies:
        colony.draw(MainSurf)
        for ant in colony:
            ant.update(trails,foodsource)
            ant.draw(MainSurf)
	    
	    if debug==1:
		text.append(ants.Text([0,200,0], 10, (ant.x, ant.y), str((int(ant.x),int(ant.y),int(ant.r)))))
		

    for t in text:
	t.draw(MainSurf)

            
    pygame.display.update()


if __name__ == "__main__":

    pygame.init()
    clock = pygame.time.Clock()

    WIDTH=800
    HEIGHT=800
    MainSurf = pygame.display.set_mode([WIDTH, HEIGHT])

    keys = {pygame.K_ESCAPE : False, pygame.K_d : False} #declare keys we will use

    mfile = "gg.mp3"
    # set up the mixer
    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 2     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment to get right sound)
    pygame.mixer.init(freq, bitsize, channels, buffer)
    #play_music(mfile)
    
    setup()
    
    while 1:
        clock.tick(30)
        #print clock.get_fps()
        doinput()
        update()

    exit(0)
