# -*- coding: utf-8 -*-
"""
author: Horst JeNS,
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
idea: submarine game from my students Paolo P. and Simon H.
this example is tested using python 3.5 and pygame
needs: several files  in subfolder 'data'
what works now: scrollwheel for map zoom
"""

#the next line is only needed for python2.x and not necessary for python3.x
from __future__ import print_function, division

import pygame 
import math
import random
import os
import sys

GRAD = math.pi / 180 # 2 * pi / 360   # math module needs Radiant instead of Grad

import operator
import math
 
class Vec2d(object):
    """2d vector class, supports vector and scalar operators,
       and also provides a bunch of high level functions
       """
    __slots__ = ['x', 'y']
 
    def __init__(self, x_or_pair, y = None):
        if y == None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y
 
    def __len__(self):
        return 2
 
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")
 
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")
 
    # String representaion (for debugging)
    def __repr__(self):
        return 'Vec2d(%s, %s)' % (self.x, self.y)
 
    # Comparison
    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False
 
    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x != other[0] or self.y != other[1]
        else:
            return True
 
    def __nonzero__(self):
        return bool(self.x or self.y)
 
    # Generic operator handlers
    def _o2(self, other, f):
        "Any two-operator operation where the left operand is a Vec2d"
        if isinstance(other, Vec2d):
            return Vec2d(f(self.x, other.x),
                         f(self.y, other.y))
        elif (hasattr(other, "__getitem__")):
            return Vec2d(f(self.x, other[0]),
                         f(self.y, other[1]))
        else:
            return Vec2d(f(self.x, other),
                         f(self.y, other))
 
    def _r_o2(self, other, f):
        "Any two-operator operation where the right operand is a Vec2d"
        if (hasattr(other, "__getitem__")):
            return Vec2d(f(other[0], self.x),
                         f(other[1], self.y))
        else:
            return Vec2d(f(other, self.x),
                         f(other, self.y))
 
    def _io(self, other, f):
        "inplace operator"
        if (hasattr(other, "__getitem__")):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
        return self
 
    # Addition
    def __add__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x + other.x, self.y + other.y)
        elif hasattr(other, "__getitem__"):
            return Vec2d(self.x + other[0], self.y + other[1])
        else:
            return Vec2d(self.x + other, self.y + other)
    __radd__ = __add__
 
    def __iadd__(self, other):
        if isinstance(other, Vec2d):
            self.x += other.x
            self.y += other.y
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self
 
    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x - other.x, self.y - other.y)
        elif (hasattr(other, "__getitem__")):
            return Vec2d(self.x - other[0], self.y - other[1])
        else:
            return Vec2d(self.x - other, self.y - other)
    def __rsub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(other.x - self.x, other.y - self.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(other[0] - self.x, other[1] - self.y)
        else:
            return Vec2d(other - self.x, other - self.y)
    def __isub__(self, other):
        if isinstance(other, Vec2d):
            self.x -= other.x
            self.y -= other.y
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self
 
    # Multiplication
    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x*other.x, self.y*other.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(self.x*other[0], self.y*other[1])
        else:
            return Vec2d(self.x*other, self.y*other)
    __rmul__ = __mul__
 
    def __imul__(self, other):
        if isinstance(other, Vec2d):
            self.x *= other.x
            self.y *= other.y
        elif (hasattr(other, "__getitem__")):
            self.x *= other[0]
            self.y *= other[1]
        else:
            self.x *= other
            self.y *= other
        return self
 
    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)
    def __idiv__(self, other):
        return self._io(other, operator.div)
 
    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)
    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)
 
    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)
    def __itruediv__(self, other):
        return self._io(other, operator.floordiv)
 
    # Modulo
    def __mod__(self, other):
        return self._o2(other, operator.mod)
    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)
 
    def __divmod__(self, other):
        return self._o2(other, operator.divmod)
    def __rdivmod__(self, other):
        return self._r_o2(other, operator.divmod)
 
    # Exponentation
    def __pow__(self, other):
        return self._o2(other, operator.pow)
    def __rpow__(self, other):
        return self._r_o2(other, operator.pow)
 
    # Bitwise operators
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)
 
    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)
 
    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__
 
    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__
 
    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__
 
    # Unary operations
    def __neg__(self):
        return Vec2d(operator.neg(self.x), operator.neg(self.y))
 
    def __pos__(self):
        return Vec2d(operator.pos(self.x), operator.pos(self.y))
 
    def __abs__(self):
        return Vec2d(abs(self.x), abs(self.y))
 
    def __invert__(self):
        return Vec2d(-self.x, -self.y)
 
    # vectory functions
    def get_length_sqrd(self):
        return self.x**2 + self.y**2
 
    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2)
    def __setlength(self, value):
        length = self.get_length()
        self.x *= value/length
        self.y *= value/length
    length = property(get_length, __setlength, None, "gets or sets the magnitude of the vector")
 
    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        self.x = x
        self.y = y
 
    def rotated(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        return Vec2d(x, y)
 
    def get_angle(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.degrees(math.atan2(self.y, self.x))
    def __setangle(self, angle_degrees):
        self.x = self.length
        self.y = 0
        self.rotate(angle_degrees)
    angle = property(get_angle, __setangle, None, "gets or sets the angle of a vector")
 
    def get_angle_between(self, other):
        cross = self.x*other[1] - self.y*other[0]
        dot = self.x*other[0] + self.y*other[1]
        return math.degrees(math.atan2(cross, dot))
 
    def normalized(self):
        length = self.length
        if length != 0:
            return self/length
        return Vec2d(self)
 
    def normalize_return_length(self):
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
        return length
 
    def perpendicular(self):
        return Vec2d(-self.y, self.x)
 
    def perpendicular_normal(self):
        length = self.length
        if length != 0:
            return Vec2d(-self.y/length, self.x/length)
        return Vec2d(self)
 
    def dot(self, other):
        return float(self.x*other[0] + self.y*other[1])
 
    def get_distance(self, other):
        return math.sqrt((self.x - other[0])**2 + (self.y - other[1])**2)
 
    def get_dist_sqrd(self, other):
        return (self.x - other[0])**2 + (self.y - other[1])**2
 
    def projection(self, other):
        other_length_sqrd = other[0]*other[0] + other[1]*other[1]
        projected_length_times_other_length = self.dot(other)
        return other*(projected_length_times_other_length/other_length_sqrd)
 
    def cross(self, other):
        return self.x*other[1] - self.y*other[0]
 
    def interpolate_to(self, other, range):
        return Vec2d(self.x + (other[0] - self.x)*range, self.y + (other[1] - self.y)*range)
 
    def convert_to_basis(self, x_vector, y_vector):
        return Vec2d(self.dot(x_vector)/x_vector.get_length_sqrd(), self.dot(y_vector)/y_vector.get_length_sqrd())
 
    def __getstate__(self):
        return [self.x, self.y]
 
    def __setstate__(self, dict):
        self.x, self.y = dict   

#a = Vec2d(5,1)
#b = Vec2d(0,9)
#print("a",a)
#print("a*5", a*5)
#print("a90", a.rotated(90))

    
class FlyingObject(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0 # current number for new Sprite
    numbers = {} # {number: Sprite}
  
    
    def __init__(self, radius = 50,speed = 20, color=None, x=320, y=240,
                 dx=0, dy=0, layer=4, friction=1.0, mass=10,
                 hitpoints=100, damage=10, bossnumber = None, imagenr = None):
        """create a (black) surface and paint a blue ball on it"""
        self._layer = layer   #self.layer = layer
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        # self groups is set in PygView.paint()
        self.number = FlyingObject.number # unique number for each sprite
        FlyingObject.number += 1 
        FlyingObject.numbers[self.number] = self
        self.radius = radius
        self.mass = mass
        self.damage = damage
        self.imagenr = imagenr
        self.bossnumber = bossnumber
        self.hitpoints = hitpoints
        self.hitpointsfull = hitpoints
        self.width = 2 * self.radius
        self.height = 2 * self.radius
        self.turnspeed = 5   # only important for rotating
        self.speed = speed      # only important for ddx and ddy
        self.angle = 0
        self.X = 0
        self.Y = 0
        self.heading = Vec2d(0,1) # north
        
        self.x = x           # position
        self.y = y
        self.dx = dx         # movement
        self.dy = dy
        self.ddx = 0 # acceleration and slowing down. set dx and dy to 0 first!
        self.ddy = 0
        self.friction = friction # 1.0 means no friction at all
        if color is None: # create random color if no color is given
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        else:
            self.color = color
        self.create_image()
        self.rect= self.image.get_rect()
        self.init2()
        
    def init2(self):
        pass # for specific init stuff of subclasses, overwrite init2
        
    def kill(self):
        del self.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)
            
    def create_image(self):
        self.image = pygame.Surface((self.width,self.height))    
        self.image.fill((self.color))
        self.image = self.image.convert()
        
    def turnleft(self):
        self.angle += self.turnspeed
        
    def turnright(self):
        self.angle -= self.turnspeed
        
    def forward(self):
        self.ddx = -math.sin(self.angle*GRAD) 
        self.ddy = -math.cos(self.angle*GRAD) 
        
    def backward(self):
        self.ddx = +math.sin(self.angle*GRAD) 
        self.ddy = +math.cos(self.angle*GRAD)  
        
    def straferight(self):
        self.ddx = +math.cos(self.angle*GRAD)
        self.ddy = -math.sin(self.angle*GRAD)
    
    def strafeleft(self):
        self.ddx = -math.cos(self.angle*GRAD) 
        self.ddy = +math.sin(self.angle*GRAD) 
        
    def turn2heading(self):
        """rotate into direction of movement (dx,dy)"""
        self.angle = math.atan2(-self.dx, -self.dy)/math.pi*180.0 
        self.image = pygame.transform.rotozoom(self.image0,self.angle,1.0)
    
    def rotate(self):
          """rotate because changes in self.angle"""
          self.oldcenter = self.rect.center
          self.image = pygame.transform.rotate(self.image0, self.angle)
          self.rect = self.image.get_rect()
          self.rect.center = self.oldcenter

    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        self.dx += self.ddx * self.speed
        self.dy += self.ddy * self.speed
        if abs(self.dx) > 0 : 
            self.dx *= self.friction  # make the Sprite slower over time
        if abs(self.dy) > 0 :
            self.dy *= self.friction
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        # alive?
        if self.hitpoints < 1:
            self.kill()



class Plane(FlyingObject):
    images = []
    
    """A plane that patrols the skies"""
    def init2(self):
        self.hitpointsfull = 75
        self.hitpoints = 75
        self.speed = 130
        self.turnspeed = 11
        self.damage = 10
        self.dx = 10
        self.dy = 10
        self.x = 50
        self.y = 50
        self.path = [(50,50),(150,150),(300,50),(400,100),(200,200),(50,400)]
        self.newpoint = 1
        self.oldpoint = 0
        
    def create_image(self):
        self.image = self.images[0]
        self.image0 = self.images[0]
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        
    def update(self, seconds):
        self.dx += self.ddx * self.speed
        self.dy += self.ddy * self.speed
        if abs(self.dx) > 0 : 
            self.dx *= self.friction  # make the Sprite slower over time
        if abs(self.dy) > 0 :
            self.dy *= self.friction
        self.x += self.dx * seconds
        self.y += self.dy * seconds
        self.rect.centerx = round(self.x, 0)
        self.rect.centery = round(self.y, 0)
        #if self.point == 1:
        #    if self.x>150:
        #        self.point = 2
        #        (self.x,self.y) = self.path[1]
        #        self.dy = -10
        # x
        if self.path[self.oldpoint][0] < self.path[self.newpoint][0]:
            dirx = 1
        elif self.path[self.oldpoint][0] > self.path[self.newpoint][0]:
            dirx = -1
        else:
            dirx = 0
        # y
        if self.path[self.oldpoint][1] < self.path[self.newpoint][1]:
            diry = 1
        elif self.path[self.oldpoint][1] > self.path[self.newpoint][1]:
            diry = -1
        else:
            diry = 0
        pointwechsel = False            
        if dirx != 0:
            if dirx == 1:
                if self.x > self.path[self.newpoint][0]:
                    pointwechsel = True
            else:
                if self.x < self.path[self.newpoint][0]:
                    pointwechsel = True
        if diry != 0:
            if diry == 1:
                if self.y > self.path[self.newpoint][1]:
                    pointwechsel = True
            else:
                if self.y < self.path[self.newpoint][1]:
                    pointwechsel = True
        if pointwechsel:
            # letzter in der liste?
            if self.newpoint == len(self.path)-1:
                self.oldpoint = self.newpoint
                self.newpoint = 0
            else:
                tmp = self.newpoint
                self.newpoint += 1
                self.oldpoint = tmp
            (self.x, self.y) = self.path[self.oldpoint]
            pointwechsel = False
            #print("oldpoint, newpoint", self.oldpoint, self.newpoint)
            self.dx = self.path[self.newpoint][0] - self.path[self.oldpoint][0]
            self.dy = self.path[self.newpoint][1] - self.path[self.oldpoint][1]
            tmpvec = Vec2d(self.dx,self.dy).normalized()
            self.dx = tmpvec.x * self.speed
            self.dy = tmpvec.y * self.speed             

        
        
        
        # alive?
        if self.hitpoints < 1:
            self.kill()

class Fighter(Plane):
    """Fast but fragile Plane armed with machine guns"""
    def init2(self):
        self.hitpointsfull = 75
        self.hitpoints = 75
        self.speed = 130
        self.turnspeed = 11
        self.damage = 10
        self.dx = 10
        self.dy = 10
        self.x = 50
        self.y = 50
        self.path = [(50,50),(300,300),(750,50)]
        self.newpoint = 1
        self.oldpoint = 0
        Hitpointbar(self.number)
        
class Bomber(Plane):
    """Plane that drops explosive bombs"""
    def init2(self):
        self.hitpointsfull = 90
        self.hitpoints = 90
        self.speed = 120
        self.turnspeed = 11
        self.damage = 50
        self.dx = 0
        self.dy = 40
        self.x = 50
        self.y = 50
        self.path = [(100,100),(100,400),(400,400),(400,100)]
        self.newpoint = 1
        self.oldpoint = 0
        Hitpointbar(self.number)
        
    def create_image(self):
        self.image = self.images[2]
        self.image0 = self.images[2]
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height    
        
class SwimmingObject(FlyingObject):
    
    def __init2(self):  
        self.hitpoints = 150
        self.hitpointsfull = 150
        self.damage = 10
        self.speed = 50
        self.turnspeed = 5
        
class Hitpointbar(pygame.sprite.Sprite):
        """shows a bar with the hitpoints of a Boss sprite
        Boss needs a unique number in FlyingObject.numbers,
        self.hitpoints and self.hitpointsfull"""
    
        def __init__(self, bossnumber, height=7, color = (0,255,0), ydistance=10):
            pygame.sprite.Sprite.__init__(self,self.groups)
            self.bossnumber = bossnumber # lookup in Flyingobject.numbers
            self.boss = FlyingObject.numbers[self.bossnumber]
            self.height = height
            self.color = color
            self.ydistance = ydistance
            self.image = pygame.Surface((self.boss.rect.width,self.height))
            self.image.set_colorkey((0,0,0)) # black transparent
            pygame.draw.rect(self.image, self.color, (0,0,self.boss.rect.width,self.height),1)
            self.rect = self.image.get_rect()
            self.oldpercent = 0
            
            
        def update(self, time):
            self.rect.centerx = self.boss.rect.centerx
            self.rect.centery = self.boss.rect.centery - self.boss.rect.height //2 - self.ydistance
            self.percent = self.boss.hitpoints / self.boss.hitpointsfull * 1.0
            if self.percent != self.oldpercent:
                pygame.draw.rect(self.image, (0,0,0), (1,1,self.boss.rect.width-2,self.height-2)) # fill black
                pygame.draw.rect(self.image, (0,255,0), (1,1,
                    int(self.boss.rect.width * self.percent),self.height-2),0) # fill green
            self.oldpercent = self.percent
            #check if boss is still alive
            if self.bossnumber not in FlyingObject.numbers:
                self.kill() # kill the hitbar

class Explosion(FlyingObject):
    """a big pygame Sprite with high mass"""
        
    def init2(self):
        self.mass = 150
        checked = False
        self.dx = random.random() * 100 - 50
        self.dy = random.random() * 100 - 50
        Hitpointbar(self.number)
        
    def create_image(self):
        self.image = pygame.Surface((self.width,self.height))    
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius) # draw blue filled circle on ball surface
        pygame.draw.circle (self.image, (0,0,200) , (self.radius //2 , self.radius //2), self.radius// 3)         # left blue eye
        pygame.draw.circle (self.image, (255,255,0) , (3 * self.radius //2  , self.radius //2), self.radius// 3)  # right yellow yey
        pygame.draw.arc(self.image, (32,32,32), (self.radius //2, self.radius, self.radius, self.radius//2), math.pi, 2*math.pi, 1) # grey mouth
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert_alpha() # faster blitting with transparent color
        self.rect= self.image.get_rect()        

class EnemySub(SwimmingObject):
    """a big pygame Sprite with high mass"""
        
    def init2(self):
        self.hitpointsfull = 150
        self.hitpoints = 150
        self.mass = 150
        checked = False
        self.dx = 0#random.random() * 10 - 50
        self.dy = 0#random.random() * 10 - 50
        Hitpointbar(self.number)
        
    def create_image(self):
        self.image = PygView.images[self.imagenr]
        self.image0 = PygView.images[self.imagenr]
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height

class Torpedoexplosion(FlyingObject):
    """exploding torpedo"""
    images = []

    def init2(self):
        #self.mass = 5
        self.lifetime = 1.5 # seconds
        #self.color = (255,5,210)
        self.speed = 0.0
        self.angle = FlyingObject.numbers[self.bossnumber].angle
        self.rotate()
        self.picturetime = 0.2 # how long one picture is visible
        self.age = 0

    def update(self, seconds):
        super(Torpedoexplosion, self).update(seconds)
        self.lifetime -= seconds # aging
        self.age += seconds
        try:
            self.image0 = Torpedoexplosion.images[int(self.age / self.picturetime)]
            self.image = Torpedoexplosion.images[int(self.age / self.picturetime)]
        except:
            self.kill()
            print("Torpedoexplosion lifetime is too low or too few images for Torpedoexplosion")
        if self.lifetime < 0:
            self.kill()
        
    def create_image(self):
        self.image = Torpedoexplosion.images[0]
        self.image0 = Torpedoexplosion.images[0]
        self.rect = self.image.get_rect()

class Torpedo(FlyingObject):
    """a small Sprite with mass"""
    images = []

    def init2(self):
        self.mass = 5
        self.damage = 100
        self.lifetime = 8.5 # seconds
        self.color = (255,5,210)
        self.speed = 5.0
        self.angle = FlyingObject.numbers[self.bossnumber].angle
        self.rotate()

    def update(self, seconds):
        super(Torpedo,self).update(seconds)
        self.lifetime -= seconds # aging
        if self.lifetime < 0:
            Torpedoexplosion(radius=5, x=self.x, y=self.y, bossnumber=self.number) 
            self.kill()
        
    def create_image(self):
        #self.image = pygame.Surface((self.width,self.height))    
        #pygame.draw.rect(self.image, self.color, (0,0,5,10))
        #self.image.set_colorkey((0,0,0))
        #self.image = self.image.convert_alpha() # faster blitting with transparent color
        #self.rect= self.image.get_rect()
        #self.image0 = self.image.copy()
        self.image = Torpedo.images[0]
        self.image0 = Torpedo.images[0]
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        
        
class Player(SwimmingObject):
    """player-controlled character with relative movement"""
        
    def init2(self):
        self.friction = 0.922#992 # slow down self-movement over time
        self.turnspeed = 1
        self.speed = 3
        self.hitpoints = 200
        self.mass = 100
        self.damage = 100
        self.radius = 16 # image is 32x36 pixel
        self.cooldown = 0.0
        self.cooldowntime = 1.0
        Hitpointbar(self.number)
        
    def create_image(self):
        self.image = PygView.images[self.imagenr]
        self.image0 = PygView.images[self.imagenr]
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
                
    def update(self, seconds):
          super(Player,self).update(seconds)
          self.rotate()        # use for player-controlled objects
          if self.cooldown > 0.0:
              self.cooldown -= seconds
          
    def checkfire(self):
        if self.cooldown > 0.0:
            return False
        return True       


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
    
def elastic_collision(sprite1, sprite2):
        """elasitc collision between 2 sprites (calculated as disc's).
           The function alters the dx and dy movement vectors of both sprites.
           The sprites need the property .mass, .radius, .x .y, .dx, dy
           by Leonard Michlmayr"""
        dirx = sprite1.x - sprite2.x
        diry = sprite1.y - sprite2.y
        sumofmasses = sprite1.mass + sprite2.mass
        sx = (sprite1.dx * sprite1.mass + sprite2.dx * sprite2.mass) / sumofmasses
        sy = (sprite1.dy * sprite1.mass + sprite2.dy * sprite2.mass) / sumofmasses
        bdxs = sprite2.dx - sx
        bdys = sprite2.dy - sy
        cbdxs = sprite1.dx - sx
        cbdys = sprite1.dy - sy
        distancesquare = dirx * dirx + diry * diry
        if distancesquare == 0:
            dirx = random.randint(0,11) - 5.5
            diry = random.randint(0,11) - 5.5
            distancesquare = dirx * dirx + diry * diry
        dp = (bdxs * dirx + bdys * diry) # scalar product
        dp /= distancesquare # divide by distance * distance.
        cdp = (cbdxs * dirx + cbdys * diry)
        cdp /= distancesquare
        if dp > 0:
            sprite2.dx -= 2 * dirx * dp 
            sprite2.dy -= 2 * diry * dp
            sprite1.dx -= 2 * dirx * cdp 
            sprite1.dy -= 2 * diry * cdp
            
class PygView(object):
    width = 0
    height = 0
    images = []
    
  
    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,..."""
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        PygView.width = width    # make global readable
        PygView.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.loadresources()
        self.background = pygame.Surface(PygView.images[0].get_size())
        self.background.blit(PygView.images[0], (0,0))
        #self.background = pygame.Surface(self.screen.get_size()).convert()  
        #self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        #self.loadresources()
        self.mapzoom = 5
        
        
    def zoom_in(self):
        if self.mapzoom < 3:
            self.mapzoom += 1
            self.background.blit(PygView.images[self.mapzoom], (0,0))
         
        
    def zoom_out(self):
        if self.mapzoom > 0:
            self.mapzoom -= 1
            self.background.blit(PygView.images[self.mapzoom], (0,0))
            
           
      
        
    def loadresources(self):
        """painting on the surface (once) and create sprites"""
        # make an interesting background 
        #draw_examples(self.background) # background artwork
        try:  # ----------- load sprite images -----------
            PygView.images.append(pygame.image.load(os.path.join("data", "map.png")).convert())     # index 0
            PygView.images.append(pygame.image.load(os.path.join("data", "map.png")).convert())     # index 1
            PygView.images.append(pygame.image.load(os.path.join("data", "map.png")).convert())     # index 2
            PygView.images.append(pygame.image.load(os.path.join("data", "map.png")).convert())     # index 3
            PygView.images.append(pygame.image.load(os.path.join("data", "Uboot.png")).convert_alpha()) # index 4
            PygView.images.append(pygame.image.load(os.path.join("data", "Ubootrot.png")).convert_alpha()) # index 5
            Torpedoexplosion.images.append(pygame.image.load(os.path.join("data","torpedoexplosion0.png")).convert_alpha())
            Torpedoexplosion.images.append(pygame.image.load(os.path.join("data","torpedoexplosion1.png")).convert_alpha())
            Torpedoexplosion.images.append(pygame.image.load(os.path.join("data","torpedoexplosion2.png")).convert_alpha())
            Torpedoexplosion.images.append(pygame.image.load(os.path.join("data","torpedoexplosion3.png")).convert_alpha())
            Torpedoexplosion.images.append(pygame.image.load(os.path.join("data","torpedoexplosion4.png")).convert_alpha())
            Torpedoexplosion.images.append(pygame.image.load(os.path.join("data","torpedoexplosion5.png")).convert_alpha())
            Torpedo.images.append(pygame.image.load(os.path.join("data","torpedo.png")))
            Plane.images.append(pygame.image.load(os.path.join("data", "fighter1.png")))            
            Plane.images.append(pygame.image.load(os.path.join("data", "fighter2.png")))
            Plane.images.append(pygame.image.load(os.path.join("data", "bomber1.png")))
            rosa = Plane.images[1].get_at((0,0))
            andresrosa = Torpedo.images[0].get_at((0,0))
            Plane.images[0].set_colorkey(rosa)            
            Plane.images[1].set_colorkey(rosa)
            Plane.images[2].set_colorkey(rosa)
            Torpedo.images[0].set_colorkey(andresrosa)      
        
            # load other resources here
        except:
            print("pygame error:", pygame.get_error())
            print("please make sure there is a subfolder 'data' and in it the missing file(s)")
            pygame.quit()
            sys.exit()
        # ------- create background
        
        PygView.images[1] = pygame.transform.scale(PygView.images[0], (self.width, self.height))
        PygView.images[2] = pygame.transform.scale(PygView.images[0], (self.width*2, self.height*2))
        PygView.images[3] = pygame.transform.scale(PygView.images[0], (self.width*4, self.height*4))
        
        # ----- draw grids ----
        
        for x in range(0,6401,100):
            pygame.draw.line(PygView.images[1], (0,255,0), (x, 0), (x, self.height) )
        for y in range(0,4801,100):
            pygame.draw.line(PygView.images[1], (0,255,0), (0, y), (self.width, y))
        for x in range(0,6401,200):
            pygame.draw.line(PygView.images[2], (0,255,0), (x, 0), (x, self.height*2) )
        for y in range(0,4801,200):
            pygame.draw.line(PygView.images[2], (0,255,0), (0, y), (self.width*2, y))
        for x in range(0,6401,400):
            pygame.draw.line(PygView.images[3], (0,255,0), (x, 0), (x, self.height*4) )
        for y in range(0,4801,400):
            pygame.draw.line(PygView.images[3], (0,255,0), (0, y), (self.width*4, y))
            
        
        
        
        
        
        # -------  create (pygame) Sprites Groups and Sprites -------------
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        self.hitpointbargroup = pygame.sprite.Group()
        self.torpedogroup = pygame.sprite.Group()
        self.playergroup = pygame.sprite.Group()
        self.enemysubgroup = pygame.sprite.Group()
        self.planegroup = pygame.sprite.Group()
        # ----- assign Sprite class to sprite Groups ------- 
        Player.groups = self.allgroup, self.playergroup
        Hitpointbar.groups = self.hitpointbargroup
        Plane.groups = self.allgroup, self.planegroup
        Bomber.groups = self.allgroup, self.planegroup
        Fighter.groups = self.allgroup, self.planegroup
        Torpedo.groups = self.allgroup, self.torpedogroup
        Torpedoexplosion.groups = self.allgroup,
        EnemySub.groups = self.allgroup, self.enemysubgroup
        self.enemysub1 = EnemySub(x=150, y=150, imagenr = 5)
        self.enemysub2 = EnemySub(x=350, y=250, imagenr = 5)
        self.player1 = Player(x=400, y=200, dx=0, dy=0, layer=5, imagenr = 4) # over balls layer
        self.fighter1 = Fighter(x=50, y=50)
        self.bomber1 = Bomber(x=100, y=100)
        

    def run(self):
        """The mainloop"""
        self.mapdx, self.mapdy = 0, 0
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                # ------- press and release key handler -------
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE: # fire forward from player1 with 300 speed
                        if self.player1.checkfire():
                            Torpedo(radius=5, x=self.player1.x, y=self.player1.y,
                                   dx=-math.sin((self.player1.angle)*GRAD)*50,
                                   dy=-math.cos((self.player1.angle)*GRAD)*50,
                                   bossnumber=self.player1.number,
                                   color = (255,0,210))   
                            self.player1.cooldown = self.player1.cooldowntime       
                # ------ mouse wheel handler ----      
                elif event.type == pygame.MOUSEBUTTONDOWN: # or event.type == pygame.JOYBUTTONDOWN:
                     if event.button == 4: # scrollwheel up
                          #key_to_function[pygame.K_PLUS](universe_screen)
                          self.zoom_in()
                     elif event.button == 5: # scrollweeel down
                          self.zoom_out()
            # ------ pressed keys key handler ------------
            pressedkeys = pygame.key.get_pressed()
            self.player1.ddx = 0 # reset movement
            self.player1.ddy = 0 
            if pressedkeys[pygame.K_w]: # forward
                 self.player1.forward()
            if pressedkeys[pygame.K_s]: # backward
                 self.player1.backward()
            if pressedkeys[pygame.K_a]: # turn left
                self.player1.turnleft()
            if pressedkeys[pygame.K_d]: # turn right
                self.player1.turnright()
            if pressedkeys[pygame.K_e]: # strafe right
                self.player1.straferight()
            if pressedkeys[pygame.K_q]: # strafe left
                self.player1.strafeleft()
            # ---- map scrolling -----
            if pressedkeys[pygame.K_LEFT]:
                self.mapdx += 1
                #if self.mapdx > 15:
                #    self.mapdx = 15
            if pressedkeys[pygame.K_RIGHT]:
                self.mapdx -= 1
                #if self.mapdx < -15:
                #    self.mapdx = -15
            if pressedkeys[pygame.K_UP]:
                self.mapdy += 1
                #if self.mapdy > 15:
                #    self.mapdy = 15
            if pressedkeys[pygame.K_DOWN]:
                self.mapdy -= 1
                #if self.mapdy < -15:
                #    self.mapdy = -15

            # ------ clock ----------
            milliseconds = self.clock.tick(self.fps) 
            seconds = milliseconds / 1000
            self.playtime += seconds
            self.screen.blit(self.background, (0 + self.mapdx, 0 + self.mapdy))  # clear screen
            # write text below sprites
            write(self.screen, "FPS: {:6.3}  PLAYTIME: {:6.3} SECONDS".format(
                           self.clock.get_fps(), self.playtime))
            # ----------- collision detection between enemysub and torpedo --------
            for ship in self.enemysubgroup:
                crashgroup = pygame.sprite.spritecollide(ship, self.torpedogroup, True, pygame.sprite.collide_mask)
                for torpedo in crashgroup:
                    ship.hitpoints -= torpedo.damage
            
            
            
            # ---------- collision detection between torpedo and other torpedos
            for torpedo in self.torpedogroup:
                crashgroup = pygame.sprite.spritecollide(torpedo, self.torpedogroup, False, pygame.sprite.collide_circle)
                for othertorpedo in crashgroup:
                    if torpedo.number > othertorpedo.number:
                #         elastic_collision(torpedo, othertorpedo) # change dx and dy of both sprites
                          torpedo.kill()
            
            # ------------ collision detection between Player and torpedos
            for player in self.playergroup:
                crashgroup = pygame.sprite.spritecollide(player, self.torpedogroup, False, pygame.sprite.collide_circle)
                for othertorpedo in crashgroup:
                    # player is not damaged by his own torpedos
                    if othertorpedo.bossnumber != player.number:
                        elastic_collision(player, othertorpedo)
                        player.hitpoints -= othertorpedo.damage
                        othertorpedo.kill()
                        
            # 
            # ----------- clear, draw , update, flip -----------------  
            #self.allgroup.clear(screen, background)
            self.allgroup.update(seconds) # would also work with ballgroup
            self.hitpointbargroup.update(seconds) # to avoid "bouncing" hitpointbars
            self.allgroup.draw(self.screen)      
            self.hitpointbargroup.draw(self.screen)     
            # -------  write text over everything  -----------------
            #write(self.screen, "Press b to add another ball", x=self.width//2, y=250, center=True)
            # --------- next frame ---------------
            pygame.display.flip()
            # update status text 
            pygame.display.set_caption("Press ESC to quit"+"mapzoom: {}".format(self.mapzoom))
        pygame.quit()

if __name__ == '__main__':
    abba = Vec2d(5,5)
    #print(abba)
    #print(abba.normalized())
    #print(abba.x, abba.y)
    # try PygView(800,600).run()
    PygView().run() 
