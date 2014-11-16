import pygame,sys
import time
import game_elements
from game_elements import Level

width, height = 640, 480

class Movement(object):
        def move_paddle_left(s,p):
                if(p.rect.left-p.velocity>=0):
                        p.rect.left=p.rect.left-p.velocity
                else:
                        p.rect.left=0
                # Draw paddle after movement
                s.blit(p.surface,p.rect)
                                        
        def move_paddle_right(s,p):
                if(p.rect.right+p.velocity<=640):
                        p.rect.right=p.rect.right+p.velocity
                else:
                        p.rect.right=640
                s.blit(p.surface,p.rect)                
        touch_paddle=False

        @classmethod
        def move_ball(cls,s,b,bricklist,p):                        
                        b.rect=b.rect.move(b.velocity)
                        #Collision with wall
                        #Next 2 ifs: Error in case the ball is very fast (probably not going to happen)
                        if b.rect.left < 0 or b.rect.right > width:
                            b.velocity[0] = -b.velocity[0]
                            s.blit(b.surface,b.rect)
                            return
                        if b.rect.top  < 0:
                            b.velocity[1] = -b.velocity[1]
                            s.blit(b.surface,b.rect)
                            return
                                
                        #Collision with paddle
                        offset_x = (b.rect.left - p.rect.left)
                        offset_y = (b.rect.top - p.rect.top)
                        if (p.mask.overlap(b.mask, (offset_x, offset_y)) != None):
                                #Test to see if horizontal or vertical collision
                                velocity_test=(b.velocity[0],-b.velocity[1])
                                test_rect=b.rect.move(velocity_test)
                                test_offset_x, test_offset_y = (test_rect.left - p.rect.left), (test_rect.top - p.rect.top)
                                if (p.mask.overlap(b.mask, (test_offset_x, test_offset_y)) != None):
                                #horizontal collision
                                        if(cls.touch_paddle==False):
                                                b.velocity[0] = -b.velocity[0]
                                                cls.touch_paddle=True
                                        b.velocity[1] = -1*abs(b.velocity[1])
                                else:
                                #vertical collision
                                        b.velocity[1] = -1*abs(b.velocity[1])
                                s.blit(b.surface,b.rect)
                                return
                        elif(abs(b.rect.left-p.rect.left)>100):
                                cls.touch_paddle=False

                        #Collision with bricks
                        for (ind,l) in enumerate(bricklist):
                                offset_x, offset_y = (b.rect.left - l.rect.left), (b.rect.top - l.rect.top)
                                if (l.mask.overlap(b.mask, (offset_x, offset_y)) != None):
                                        velocity_test=(b.velocity[0],-b.velocity[1])
                                        test_rect=b.rect.move(velocity_test)
                                        test_offset_x, test_offset_y = (test_rect.left - l.rect.left), (test_rect.top - l.rect.top)
                                        if (l.mask.overlap(b.mask, (test_offset_x, test_offset_y)) != None):
                                                b.velocity[0] = -b.velocity[0]
                                        else:
                                                b.velocity[1] = -b.velocity[1]
                                        l.resistance=l.resistance-1                                        
                                        if(l.resistance==0):
                                                del bricklist[ind]    
                        s.blit(b.surface,b.rect)

def main():
    resist= [ [0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0 ],\
              [0,0,0,1,2,2,2,2,2,2,2,2,1,0,0,0 ],\
              [0,0,0,0,1,3,3,3,3,3,3,1,0,0,0,0 ],\
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],\
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ]]
    
    color= [ [0,0,'O','O','O','O','O','O','O','O','O','O','O','O',0,0 ],\
              [0,0,0,'O','W','W','W','W','W','W','W','W','O',0,0,0 ],\
              [0,0,0,0,'O','M','M','M','M','M','M','O',0,0,0,0 ],\
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],\
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ]]

    lv=Level(resist,color,[-1,-1])

    screen_width, screen_height = 640, 480
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([screen_width, screen_height])
    white, black = (255, 255, 255), (0, 0, 0)
    screen.fill(white)
    screen.blit(lv.paddle.surface,lv.paddle.rect)
    lv.ball.rect.top=100
    lv.ball.rect.left=270
    screen.blit(lv.ball.surface,lv.ball.rect)
    for l in lv.bricklist:
            screen.blit(l.surface,l.rect)
    pygame.display.update()
    
    def blit_all_but_ball():
            screen.fill(white)
            screen.blit(lv.paddle.surface,lv.paddle.rect)
            for l in lv.bricklist:
               screen.blit(l.surface,l.rect)
    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()            
            blit_all_but_ball()
            key=pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                    Movement.move_paddle_left(screen,lv.paddle)
            elif key[pygame.K_RIGHT]:
                    Movement.move_paddle_right(screen,lv.paddle)
            Movement.move_ball(screen,lv.ball,lv.bricklist,lv.paddle)         
            pygame.display.update()
            clock.tick(200)
    
        

if __name__=="__main__":
    main()
