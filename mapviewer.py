# -*- coding: utf-8 -*-
"""
author: Simon Heppner
email: simon@heppner.at
contact: see http://simon.heppner.at
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
idea: tile map viewer of generated files by terrain_generator2.py
"""


import pygame 

def draw_examples(background):
    """painting on the background surface"""
    #------- try out some pygame draw functions --------
    # pygame.draw.line(Surface, color, start, end, width) 
    pygame.draw.line(background, (0,255,0), (10,10), (50,100))
    # pygame.draw.rect(Surface, color, Rect, width=0): return Rect
    pygame.draw.rect(background, (0,255,0), (50,50,100,25)) # rect: (x1, y1, width, height)
    # pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
    pygame.draw.circle(background, (0,200,0), (200,50), 35)
    # pygame.draw.polygon(Surface, color, pointlist, width=0): return Rect
    pygame.draw.polygon(background, (0,180,0), ((250,100),(300,0),(350,50)))
    # pygame.draw.arc(Surface, color, Rect, start_angle, stop_angle, width=1): return Rect
    pygame.draw.arc(background, (0,150,0),(400,10,150,100), 0, 3.14) # radiant instead of grad
    #return background # not necessary to return the surface, it's already in the memory

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
  
    def __init__(self, width=640, height=400, fps=30, filename = "level1.txt", tilew = 20, tileh = 20):
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
        self.lines = []
        try:
            lines = 0
            chars = 0
            with open(self.filename) as myfile:
                for line in myfile:
                    self.lines.append(line[:-1])
                    lines += 1
                chars = len(line) - 1
        except:
            print("-- fileReadingError --")
        print(lines, chars) 
        PygView.width = chars * self.tilew
        PygView.height = lines * self.tileh
        self.colourdict = {3:(1, 0, 122), 
                           4:(93, 92, 244),
                           5:(145, 144, 245),
                           6:(246, 252, 84),
                           7:(226, 144, 36),
                           8:(127, 127, 127)}
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()  
        self.background.fill((255,255,255)) # fill background white
        for line in range(lines):
            for char in range(chars):
                pygame.draw.rect(self.background, self.colourdict[int(self.lines[line][char])],
                                 (self.tilew * char, self.tileh * line, tilew, tileh))
        #self.clock = pygame.time.Clock()
        #self.fps = fps
        #self.playtime = 0.0
        #self.font = pygame.font.SysFont('mono', 24, bold=True)
        self.paint() 

    def paint(self):
        """painting on the surface"""
        # make an interesting background 
        #draw_examples(self.background)
        # create (non-pygame) Sprites. 
       #self.ball1 = Ball(x=100, y=100) # creating the Ball object (not a pygame Sprite)
       # self.ball2 = Ball(x=200, y=100) # create another Ball object (not a pygame Sprite)
       # self.ballgroup = [ self.ball1, self.ball2 ] # put all "Sprites" into this list
        


    def run(self):
        """The mainloop"""
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    #if event.key == pygame.K_b:
                      #  self.ballgroup.append(Ball()) # add balls!
            # end of event handler
           # milliseconds = self.clock.tick(self.fps) #
           # seconds = milliseconds / 1000
           # self.playtime += seconds
            # delete everything on screen
            self.screen.blit(self.background, (0, 0)) 
            # write text below sprites
            #write(self.screen, "FPS: {:6.3}  PLAYTIME: {:6.3} SECONDS".format(
            #               self.clock.get_fps(), self.playtime))
            # not-pygame-sprites
            #for myball in self.ballgroup:
            #    myball.update(seconds)
            #for myball in self.ballgroup:
            #    myball.blit(self.screen)
            # write text over everything 
            #write(self.screen, "Press b to add another ball", x=self.width//2, y=250, center=True)
            # next frame
            pygame.display.flip()
            
        pygame.quit()


if __name__ == '__main__':
    PygView().run()
