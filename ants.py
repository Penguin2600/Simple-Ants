import random, pygame

from math import *

class Colony(list):
    
    def __init__(self,c, n, x, y, w, h, r):
        
        self.food = 10
        self.color=c
        for i in range(n):
            self.append(Ant(self, x, y))
                             
        self.x = x
        self.y = y
        self.w = w
        self.h = h
	self.r = r
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 10)
        pygame.draw.circle(surface, [0,0,0], (int(self.x), int(self.y)), 4)

class Food:
    
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self, surface):
            pygame.draw.circle(surface, [0,150,0], (int(self.x), int(self.y)), int(self.size))

class Pheromone:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.strength = 1.0
        
    def update(self, d=0.005):
        self.strength -= d

    def draw(self, surface):
        pygame.draw.circle(surface, [self.strength*255,self.strength*255,self.strength*255], (int(self.x),int(self.y)), 6, 1)

class Ant:

    def __init__(self, colony, x, y):
    
        self.colony = colony
    
        self.x = x
        self.y = y
	self.r = int(random.random()*359)
	self.s = 2.0
        self.has_food = False
        self.wandering = random.random()*300
    
    def near(self, obj, radius=12):

        d = (((obj.x-self.x)**2 ) + ((obj.y-self.y)**2))**0.5

        if d < radius:
		return True
        return False
        
    def goal(self, obj):
        
        """Set a goal to move towards.
        Sets the object, which has x and y properties, as goal.
        The ant starts moving towards it.
        """
   
        dx = (obj.x-self.x) 
        dy = (obj.y-self.y) 

	angle_rad = atan2(dy,dx)
	self.r= degrees(angle_rad)
        
        self.wandering = 0

    
    def wander(self, d=10.0):
        
        """Wander around randomly.
        Ants wander around randomly until they find food.
        The d parameter controls the chaos with which the ant moves:
        a higher d means a more erratic ant,
        but too high is inefficient as the ant becomes indecisive.
        Eventually, ants that have been doing nothing to long,
        return to the colony.
        """

        self.wandering+=5
        self.r+=((random.random() * d*2)-(d))

        if self.x > self.colony.w: self.goal(self.colony)
        if self.x < 0: self.goal(self.colony)
        if self.y > self.colony.h: self.goal(self.colony)
        if self.y < 0: self.goal(self.colony)

	if self.wandering > self.colony.r: self.goal(self.colony)
        if self.near(self.colony): self.wandering = 0
    
    def follow(self, trails):
        
        """Follow a nearby pheromone trail.
        If the ant is not carrying food to the colony,
        follow any nearby trail.
        If the pheromone has evaporated to much,
        the ant might lose interest in the trail,
        this ensures it doesn't get "stuck" on a useless trail.
        """

        if self.has_food == False:
            for pheromone in trails:
                if self.near(pheromone):
                    if random.random()*.5 > pheromone.strength: return
                    self.goal(pheromone)	
                    if pheromone.strength < 0.4: return
                    else: break
    
    def harvest(self, foodsource):
        
        """Collect nearby food.
        If the ant is not carrying anything,
        and it is near a source of food,
        pick up food and start marking the trail home.
        """

        for food in foodsource:
            if self.near(food, radius=food.size) and self.has_food == False: 
                food.size -= 1
                if food.size < 1: foodsource.remove(food)
                #self.trail = [Pheromone(food.x, food.y)]
                #trails.append(Pheromone(self.x, self.y))
                self.has_food = True
        
    def hoard(self, trails, trail=0.2):
        
        """Return straight home with food.
        Leave a trail of pheromone markers,
        which the other ants smell and follow to the food.
        """
        
        if self.has_food:
            self.goal(self.colony)
            if random.random() < trail:
                trails.append(Pheromone(self.x, self.y))
        
        #Drop food and start wandering again
        if self.near(self.colony) and self.has_food:
            #self.trail.append(Pheromone(self.colony.x, self.colony.y))
            self.has_food = False
            self.colony.food += 1
    
    def update(self, trails, foodsource, speed=3):
        
        self.follow(trails) #follow nearby trails to food.
        self.harvest(foodsource)      #harvest nearby food source
        self.hoard(trails)  #bring food directly to colony
        self.wander()       #some random wandering is more efficient

        self.y += self.s*sin(radians(self.r))
        self.x += self.s*cos(radians(self.r)) 
        
    def draw(self, surface):
	y=int(self.y+2*sin(radians(self.r)))
	x=int(self.x+2*cos(radians(self.r)))
        pygame.draw.line(surface, self.colony.color, (int(self.x), int(self.y)),(x,y), 2)


class Text:

    def __init__(self, color, size, pos, text):
        self.font = pygame.font.Font('freesansbold.ttf', size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.topleft=pos

    def draw(self, surface):
		surface.blit(self.image,self.rect.topleft)
	

