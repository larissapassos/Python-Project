import pygame,sys
white  =  (255,255,255)

class Ball(object):
        def __init__(self,i,j,v):
                self.surface = pygame.image.load("resources/fire_ball.png")
                self.rect = self.surface.get_rect()
                self.mask = pygame.mask.from_surface(self.surface)
                self.rect.midbottom = (j,i)
                # The ball velocity is defined as a list
                #(0)->horizontal (1)->vertical
                self.velocity = v
                self.ispower = False
                        

class Paddle(object):
        def __init__(self,i,j,v):
                self.surface = pygame.image.load("resources/paddle.png")
                self.rect = self.surface.get_rect()
                self.mask = pygame.mask.from_surface(self.surface)
                self.rect.midbottom = (j,i)
                self.size = 1
                self.velocity = v

class Brick(object):
        def __init__(self,i,j,r,c):
                self.surface = self.getsurface(c)
                self.surface.set_colorkey(white)
                self.rect = self.surface.get_rect()
                self.mask = pygame.mask.from_surface(self.surface)
                self.rect.left = j
                self.rect.top = i
                self.resistance = r
                self.color = c

        def getsurface(self,c):
                # Create the brick surface
                a = pygame.Surface((40,20))
                a.fill((0,0,0))
                if(c == 'O'): #ORANGE
                        pygame.draw.rect(a,(255,215,0),pygame.Rect(a.get_rect().top+1,a.get_rect().left+1,38,18))
                elif(c == 'W'): #WOOD
                        pygame.draw.rect(a,(184,134,11),pygame.Rect(a.get_rect().top+1,a.get_rect().left+1,38,18))
                elif(c == 'M'): #METAL
                        pygame.draw.rect(a,(192,192,192),pygame.Rect(a.get_rect().top+1,a.get_rect().left+1,38,18))
                return a
        

class Level(object):
        def __init__(self,resist,color,v): #resist  =  matrix 5 rows 16 columns
                self.bricklist = []
                for i in range(0,5):
                        for j in range(0,16):
                                if(resist[i][j] != 0):
                                        b = Brick(i * 20, j * 40, resist[i][j], color[i][j])
                                        self.bricklist.append(b)
                self.paddle = Paddle(460,320,2) #HARDCODED                                       
                self.ball = Ball(460-(self.paddle.rect.h),320,v) #HARDCODED