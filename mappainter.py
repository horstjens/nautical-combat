# -*- coding: utf-8 -*-

import pygame 
import random


    

def write(background, text, x=50, y=150, color=(0,0,0),
          fontsize=None, center=False):
        """write text on pygame surface. """
        if fontsize is None:
            fontsize = 24
        font = pygame.font.SysFont('mono', fontsize, bold=True)
        fw, fh = font.size(text)
        surface = font.render(text, True, color)
        if center: # center text around x,y
            background.blit(surface, (x-fw//2, y-fh//2))
        else:      # topleft corner is x,y
            background.blit(surface, (x,y))


class PygView(object):
    width = 0
    height = 0
    maxdelta = 10
  
    def __init__(self, width=640, height=400, fps=30, filename = "level.txt", tilew = 20, tileh = 20):
        """Initialize pygame, window, background, font,...
           default arguments 
        """
        pygame.init()
        pygame.display.set_caption("--- MAP-VIEWER ---")
        PygView.width = width    # make global readable
        PygView.height = height
        self.filename = filename
        self.tilew = tilew
        self.tileh = tileh
        
        self.lines = 32
        self.chars = 64
        self.tiles = []
                
        
        print(self.lines, self.chars) 
        print(self.tiles)
        PygView.width = self.chars * self.tilew
        PygView.height = self.lines * self.tileh
        
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill((255,255,255)) # fill background white
                                          
        #self.clock = pygame.time.Clock()
        #self.fps = fps
        #self.playtime = 0.0
        #self.font = pygame.font.SysFont('mono', 24, bold=True)
        self.paint() 

    def paint(self):
        """painting on the surface"""
        for y in range(self.lines):
            line = []
            for x in range(self.chars):
                line.append(120)
            self.tiles.append(line)

        # blaue kasterln
        for line in range(self.lines):
            for char in range(self.chars):
                value = self.tiles[line][char]
                if value < 128:
                    color = (0,0,value*2)
                elif value < 192:
                    color = (0, value, 0)
                else:
                    color = (value, value, value)
                pygame.draw.rect(self.background,
                                color,
                                (self.tilew * char, 
                                 self.tileh * line, self.tilew, self.tileh))
        # grünes gitter malen
        for line in range(self.lines):
            pygame.draw.line(self.background, (0,255,0),
                             (0, self.tileh * line),
                             (PygView.width, self.tileh * line) )
        for char in range(self.chars):
            pygame.draw.line(self.background, (0,255,0),
                            (self.tilew * char, 0),
                            (self.tilew * char, PygView.height) )
                      

    def get_info(self):
        """returns tile under mouse cursor: x, y, z"""
        x, y = pygame.mouse.get_pos()
        char = x // self.tilew
        line = y // self.tileh
        value = self.tiles[line][char]
        return char, line, value
        
    def check_around(self, char, line ):
        """get z value of surrounding tiles, correct them if necessary"""
        maxdelta = PygView.maxdelta
        value = self.tiles[line][char]
        for y in [-1,0,1]:
            for x in [-1,0,1]:
                if x == 0 and y == 0:
                    continue
                try:
                    v = self.tiles[line+y][char+x]
                except:
                    continue 
                print(x,y,value, v)
                if abs(value-v) > maxdelta:
                    
                    if value > v:
                        self.tiles[line+y][char+x] = value - maxdelta
                    else:
                        self.tiles[line+y][char+x] = value + maxdelta
                    self.check_around(char+x, line+y)
                            
        

    def changeTerrain(self, delta=0):
        """changes terrain under mouse cursor:
           -1 is digging, 1 is building"""
        #x, y = pygame.mouse.get_pos()
        #char = x // self.tilew
        #line = y // self.tileh
        #value = self.tiles[line][char]
        char, line, value = self.get_info()
        
        pygame.draw.rect(self.screen, (random.randint(0,255),0,0),
                        (char * self.tilew, line * self.tileh, 
                         self.tilew, self.tileh), 5)
        
        if delta != 0:
            print("old value:", value)
            value += delta
            value = min(255, value)
            value = max(0, value)
            self.tiles[line][char] = value
            print("new value:", self.tiles[line][char])
            self.paint()
            self.check_around(char, line)
        
            

    def run(self):
        """The mainloop"""
        #self.playtime = 0
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    print(event.key)
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == 93:
                        self.changeTerrain(10)
                    if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS or event.key == 47:
                        self.changeTerrain(-10)
                    if event.key == pygame.K_F4:
                        # save into level.txt
                        linenr = 0
                        with open(self.filename, "w") as f:
                            for line in self.tiles:
                                linenr += 1
                                print(linenr, line)
                                f.write(str(line)+"\n")
                        print("level saved as level.txt")
                        nr = 0
                        for line in self.tiles:
                            nr +=1
                            print(nr, line)

                    
            
            if pygame.mouse.get_pressed()[0]:
                self.changeTerrain(-1)
            if pygame.mouse.get_pressed()[2]:
                self.changeTerrain(1)
            self.screen.blit(self.background, (0, 0)) 
            self.changeTerrain()
         
            pygame.display.flip()
            (x,y,z) = self.get_info()
            pygame.display.set_caption("--- MAP-VIEWER ---x: {} y: {} z: {}  PRESS F4 TO SAVE".format(x,y,z))
            
        pygame.quit()


if __name__ == '__main__':
    PygView().run()
