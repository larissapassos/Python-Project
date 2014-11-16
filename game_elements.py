import pygame,sys
white=(255,255,255)

class Ball(object):
        def __init__(self,i,j,v):
                self.surface=pygame.image.load("resources/fire_ball.png")
                self.rect=self.surface.get_rect()
                self.mask=pygame.mask.from_surface(self.surface)
                self.rect.midbottom=(j,i)
                self.velocity=v ##It is a list, not a number!!
                #(0)->horizontal (1)->vertical
                self.ispower=False
                        

class Paddle(object):
        def __init__(self,i,j,v):
                self.surface=pygame.image.load("resources/paddle.png")
                self.surface.set_colorkey(white)
                self.rect=self.surface.get_rect()
                self.mask=pygame.mask.from_surface(self.surface)
                self.rect.midbottom=(j,i)
                self.size=1
                self.velocity=1

class Brick(object):
        def __init__(self,i,j,r,c):
                self.surface=self.getsurface(c)
                self.surface.set_colorkey(white)
                self.rect=self.surface.get_rect()
                self.mask=pygame.mask.from_surface(self.surface)
                self.rect.left=j
                self.rect.top=i
                self.resistance=r
                self.color=c

        def getsurface(self,c):
                a=pygame.Surface((40,20))
                a.fill((0,0,0))
                if(c=='O'): #ORANGE
                        pygame.draw.rect(a,(255,215,0),pygame.Rect(a.get_rect().top+1,a.get_rect().left+1,38,18))
                elif(c=='W'): #WOOD
                        pygame.draw.rect(a,(184,134,11),pygame.Rect(a.get_rect().top+1,a.get_rect().left+1,38,18))
                elif(c=='M'): #METAL
                        pygame.draw.rect(a,(192,192,192),pygame.Rect(a.get_rect().top+1,a.get_rect().left+1,38,18))
                return a
        

class Level(object):
        def __init__(self,resist,color,v): #resist = matrix 5 rows 16 columns
                self.bricklist=[]
                for i in range(0,5):
                        for j in range(0,16):
                                if(resist[i][j]!=0):
                                        b=Brick(i*20,j*40,resist[i][j],color[i][j])
                                        self.bricklist.append(b)
                self.paddle=Paddle(480,320,1) #HARDCODED                                       
                self.ball=Ball(480-(self.paddle.rect.h),320,v) #HARDCODED


def main():
    resist= [ [0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0 ],\
              [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0 ],\
              [0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0 ],\
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],\
              [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0 ]]
    
    color= [ [0,0,'W','W','O','W','O','W','W',0,0,0,0,0,0,0 ],\
              [0,0,0,'W','M','W','M','W',0,0,0,0,0,0,0,0 ],\
              [0,0,0,0,'W','M','W',0,0,0,0,0,0,0,0,0 ],\
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],\
              [0,0,0,0,0,0,0,0,0,0,0,0,0,'W',0,0 ]]

    lv=Level(resist,color,[1,1])

    screen_width, screen_height = 640, 480
    pygame.init()
    screen = pygame.display.set_mode([screen_width, screen_height])
    white, black = (255, 255, 255), (0, 0, 0)
    screen.fill(white)
    screen.blit(lv.paddle.surface,lv.paddle.rect)
    screen.blit(lv.ball.surface,lv.ball.rect)
    for l in lv.bricklist:
            screen.blit(l.surface,l.rect)
    pygame.display.update()
    

if __name__=="__main__":
    main()
