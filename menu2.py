# -*- coding: utf-8 -*-
"""
menu system for pygame
"""


import pygame
#import simpledefense
import textscroller_vertical
import random
import sys
import os
import os.path
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,25"

class Settings(object):
    menu = {"root":["Play","Difficulty", "Help", "Credits", "Options","Quit"],

                       "Options":["Turn music off","Turn sound off","Change screen resolution"],
                       "Play":["Campaign", "Training missions"],
                       "Training missions":["Practice Investigate", "Practice Torpedo attack", "Practice Deckgun attack", "Practice Escape", "Practice Navigate"],
                       "Difficulty":["Islands", "Patrol boats", "Patrol planes", "Current", "Reef", "Nautical Intel", "Enemy Intel"],
                       "Change screen resolution":["640x400", "720x480", "720x576", "800x640","1024x800", "1280x720", "1920x1080"],
                       "Credits":["Paolo Perfahl","Simon Heppner", "Horst Jens", "Soundeffects"],
                       "Help":["How to play", "How to win"],
                       "Islands":["One big island", "A few medium islands", "mixed", "A few small islands", "None"],
                       "Patrol boats":["Many agressive", "A few agressive", "Many peaceful", "A few peaceful", "None"],
                       "Patrol planes":["Many agressive", "A few agressive", "Many peaceful", "A few peaceful", "None"],
                       "Current":["Strong", "Medium", "Weak", "None"],
                       "Reef":["Many", "Some", "Few", "None"],
                       "Nautical Intel":["Excellent", "Medium", "Blind"],
                       "Enemy Intel":["Excellent", "Medium", "Blind"]
                       }



class Menu(object):
    """ each menu item name must be unique"""
    def __init__(self, menu={"root":["Play","Help","Quit"]}):
        self.menudict = menu
        self.menuname="root"
        self.oldnames = []
        self.oldnumbers = []
        self.items=self.menudict[self.menuname]
        self.active_itemnumber=0

    def nextitem(self):
        if self.active_itemnumber==len(self.items)-1:
            self.active_itemnumber=0
        else:
            self.active_itemnumber+=1
        return self.active_itemnumber

    def previousitem(self):
        if self.active_itemnumber==0:
            self.active_itemnumber=len(self.items)-1
        else:
            self.active_itemnumber-=1
        return self.active_itemnumber

    def get_text(self):
        """ change into submenu?"""
        try:
            text = self.items[self.active_itemnumber]
        except:
           print("exception!")
           text = "root"
        if text in self.menudict:
            self.oldnames.append(self.menuname)
            self.oldnumbers.append(self.active_itemnumber)
            self.menuname = text
            self.items = self.menudict[text]
            # necessary to add "back to previous menu"?
            if self.menuname != "root":
                self.items.append("back")
            self.active_itemnumber = 0
            return None
        elif text == "back":
            #self.menuname = self.menuname_old[-1]
            #remove last item from old
            self.menuname =  self.oldnames.pop(-1)
            self.active_itemnumber= self.oldnumbers.pop(-1)
            print("back ergibt:", self.menuname)
            self.items = self.menudict[self.menuname]
            return None

        return self.items[self.active_itemnumber]





class PygView(object):

    def __init__(self, width=640, height=400, fps=30, cursortext="-->", cursorimage=None, backgroundimage = None):
        """Initialize pygame, window, background, font,...
           default arguments
        """

        pygame.mixer.pre_init(44100, -16, 2, 2048)

        pygame.init()
        if cursorimage is not None:
            try:
                self.cursorimage = pygame.image.load(cursorimage)
                self.cursorimage = pygame.transform.smoothscale(self.cursorimage, (128, 32))
            except:
                print("Fehler beim Cursor image load")
                self.cursorimage = None
        else:
            self.cursorimage = cursorimage
        self.cursortext = cursortext
        self.backgroundimage = backgroundimage 
        self.backgrounds = []
   
        self.sound1 = pygame.mixer.Sound(os.path.join('data','select.wav'))
        self.sound2 = pygame.mixer.Sound(os.path.join('data','updown.wav'))
        pygame.display.set_caption("Press ESC to quit")
        self.width = width
        self.height = height
        self.set_resolution()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.font = pygame.font.SysFont('mono', 25, bold=True)

    def set_resolution(self):
        self.screen = pygame.display.set_mode((self.width+5, self.height), pygame.DOUBLEBUF)
        if self.backgroundimage is None:
            self.background = pygame.Surface(self.screen.get_size()).convert()
            self.background.fill((255,255,255)) # fill background white
            
        else:
            self.background = pygame.image.load(self.backgroundimage)
            self.background = pygame.transform.scale(self.background, self.screen.get_size())
            self.background.convert()
            for x in range(10):  # backgroundimage0 - backgroundimage9
                filename = self.backgroundimage[:-4] + str(x) + self.backgroundimage[-4:]
                try:
                    image = pygame.image.load(filename)                 
                    image = pygame.transform.scale(image, self.screen.get_size())
                    image.convert()
                    self.backgrounds.append(image)
                except:
                    print("no backgroundimage found for {}".format(filename))
        self.backgrounds.append(self.background)
        self.background = self.backgrounds[1]
                    
        

    def paint(self):
        """painting on the surface"""
        for i in  m.items:
            n=m.items.index(i)
            if n==m.active_itemnumber:
                if self.cursorimage is not None:
                    self.screen.blit(self.cursorimage, (10, m.items.index(i)*30+60-7))
                    # improve image height position
                    #self.self.draw_text(self.cursortext,50,  m.items.index(i)*30+10,(0,0,255))
                    #self.draw_text(i, 100, m.items.index(i)*30+10,(0,0,255))
                else:
                    # --> draw cursortext
                    self.draw_text(self.cursortext,10,  m.items.index(i)*30+60,(0,0,255))
                    #self.draw_text(i, 100, m.items.index(i)*30+10,(0,0,255))
            #else:
                #self.draw_text(i, 100, m.items.index(i)*30+10)
            self.draw_text(i, 100, m.items.index(i)*30+60)

    def run(self):
        """The mainloop
        """
        #self.paint()
        running = True
        self.sounds = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = True
                        
                    if event.key==pygame.K_DOWN or event.key == pygame.K_KP2:
                        if self.sounds == True:
                            self.sound1.play()
                        if self.sounds == False:
                            try:
                                self.sound5.play()
                            except:
                                print("sound is off!")
                    if event.key==pygame.K_DOWN or event.key == pygame.K_KP2:
                        #print(m.active_itemnumber)
                        m.nextitem()
                        print(m.active_itemnumber)
                        #self.sound2.play()
                    if event.key==pygame.K_UP or event.key == pygame.K_KP8:
                        if self.sounds == True:
                            self.sound1.play()
                        if self.sounds == False:
                            try:
                                self.sound5.play()
                            except:
                                print("sound is off!")
                    if event.key==pygame.K_UP or event.key == pygame.K_KP8:
                        m.previousitem()
                        #self.sound1.play()
                    if event.key==pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if self.sounds == True:
                            self.sound2.play()
                        if self.sounds == False:
                            try:
                                self.sound5.play()
                            except:
                                print("sound is off!")
                    if event.key==pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        result = m.get_text()
                        #print(m.get_text())
                        print(result)
                        if result is None:
                            #print("Bildwechsel")
                            #print(self.backgrounds)
                            self.background = random.choice(self.backgrounds)
                            break
                        
                        if "x" in result:
                            # change screen resolution, menu text is something like "800x600"
                            left = result.split("x")[0]
                            right = result.split("x")[1]
                            if str(int(left))==left and str(int(right))== right:
                                self.width = int(left)
                                self.height = int(right)
                                self.set_resolution()


                        # important: no elif here, instead if, because every menupoint could contain an 'x'
                        if result=="Campaign" or "Practice" in result:
                            print("starting game...")      
                        elif result == "Soundeffects":
                            text="Sonar sound by Argitoth\n URL:\nhttp://freesound.org/people/Argitoth/sounds/38701/"
                            textscroller_vertical.PygView(text, self.width, self.height).run()                          
                        elif result == "Turn music off":
                            # music off
                            Settings.menu["Options"][0] = "Turn music on"
                        elif result == "Turn music on":
                            # music on
                            Settings.menu["Options"][0] = "Turn music off"
                        elif result == "Turn sound off":
                            self.sounds = False
                            Settings.menu["Options"][1] = "Turn sound on"
                        elif result == "Turn sound on":
                            self.sounds = True
                            Settings.menu["Options"][1] = "Turn sound off"
                        elif result == "How to play":
                            text="play this game\n as you like\n and win!"
                            textscroller_vertical.PygView(text, self.width, self.height).run()
                        elif result == "How to win":
                            text="to win the game:\n shoot down enemies\n avoid catching bullets"
                            textscroller_vertical.PygView(text, self.width, self.height).run()
                        elif result == "Simon Heppner":
                            text="-----SIMON HEPPNER-----\nWurde geboren 2006 am 3.5.\n(Also noch nicht gestorben)"
                            textscroller_vertical.PygView(text, self.width, self.height, textcolor=(200,0,200), bg_filename=os.path.join("data","map.png")).run()
                        elif result == "Horst Jens":
                            text="-----Horst Jens-----\nIsst gerne Joghurt! :)"
                            textscroller_vertical.PygView(text, self.width, self.height, textcolor=(200,0,0), bg_filename=os.path.join("data","Ubootdead.png")).run()
                        elif result == "Paolo Perfahl":
                            text="-----Paolo Perfahl-----\n Geboren 2003 1.7.\n (Also noch nicht gestorben)\nEr kann sehr gut am Computer\n und \n auch sonst malen und deshalb\nsind die meisten\nBilder von ihm\ngemalt worden."
                            textscroller_vertical.PygView(text, self.width, self.height, textcolor=(0,200,0), bg_filename=os.path.join("data","reef.png")).run()
                        elif result == "Quit":
                            print("Bye")
                            pygame.quit()
                            sys.exit()
                            
                            
            milliseconds = self.clock.tick(self.fps)
            #self.playtime += milliseconds / 1000.0
            self.draw_text("FPS: {:6.3}".format(self.clock.get_fps()))
                     
            #, self.playtime), color=(30, 120 ,18))
            pygame.draw.line(self.screen,(random.randint(0,255),random.randint(0,255), random.randint(0,255)),(50,self.height - 80),(self.width -50,self.height - 80) ,3)
            self.paint()
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))

        pygame.quit()


    def draw_text(self, text ,x=50 , y=0,color=(255,0,0)):
        if y==0:
            y= self.height - 50

        """Center text in window
        """
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (x,y))


####

if __name__ == '__main__':

    # call with width of window and fps
    m=Menu(Settings.menu)
    PygView(cursortext=">>>", cursorimage=os.path.join("data","scrollimage.png"), backgroundimage = os.path.join("data", "titlescreen.png")).run()
