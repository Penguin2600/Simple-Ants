import pygame
from pygame.locals import *
import random
import sys
import os

PATH=str(os.path.abspath(os.path.dirname(sys.argv[0])))

class GameSamples():
    def __init__(self):
        pygame.mixer.init(44100, -16, 2, 2048)
        self.music=pygame.mixer.Sound(PATH+'/resources/gg.ogg')# music makes things better!
        self.music.set_volume(.5)
    
    def playsound(self, clip):
        #if not pygame.mixer.get_busy():
        if clip=='music':
            self.music.play()
                
class MenuSamples():
    def __init__(self):
        
        pygame.mixer.init(44100, -16, 2, 2048)
        self.over = pygame.mixer.Sound(PATH +"/resources/beep4.wav")
        self.click = pygame.mixer.Sound(PATH +"/resources/beep5.wav")      
            
    def playsound(self, clip):
        #if not pygame.mixer.get_busy():
        if clip=='over':
            self.over.play()
        if clip=='click':
            self.click.play()

class AntSamples():
    def __init__(self):
        
        pygame.mixer.init(44100, -16, 2, 2048)
        self.get=pygame.mixer.Sound(PATH+'/resources/beep1.wav')
        self.drop=pygame.mixer.Sound(PATH+'/resources/beep2.wav')
        self.fight=pygame.mixer.Sound(PATH+'/resources/beep3.wav')

    def playsound(self, clip, stop=0):
        #if not pygame.mixer.get_busy():
                
        if clip=='get':
            self.get.play()
                    
        if clip=='drop':
                self.drop.play()
                
        if clip=='fight':
                self.fight.play()
