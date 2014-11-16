import pygame,sys
import time
import game_elements
from game_elements import Level

width, height = 640, 480

class Movement(object):

        def move_paddle_left(surface, paddle):
                if(paddle.rect.left - paddle.velocity >= 0):
                        paddle.rect.left = paddle.rect.left - paddle.velocity
                else:
                        paddle.rect.left = 0
                # Draw paddle after movement
                surface.blit(paddle.surface, paddle.rect)
                                        
        def move_paddle_right(surface, paddle):
                if(paddle.rect.right + paddle.velocity <= 640):
                        paddle.rect.right = paddle.rect.right + paddle.velocity
                else:
                        paddle.rect.right = 640
                # Draw paddle after movement
                surface.blit(paddle.surface, paddle.rect)

        touch_paddle=False

        @classmethod
        def move_ball(cls, surface, ball, bricklist, paddle):                        
                        ball.rect = ball.rect.move(ball.velocity)
                        #Collision with wall
                        #Next 2 ifs: Error in case the ball is very fast (probably not going to happen)
                        if ball.rect.left < 0 or ball.rect.right > width:
                            print("collision with side walls")
                            print("velocity before: " + str(ball.velocity))
                            ball.velocity[0] = - ball.velocity[0]
                            print("velocity after: " + str(ball.velocity))
                            surface.blit(ball.surface,ball.rect)
                            return
                        if ball.rect.top  < 0:
                            print("collision with top wall")
                            print("velocity before: " + str(ball.velocity))
                            ball.velocity[1] = - ball.velocity[1]
                            print("velocity after: " + str(ball.velocity))
                            surface.blit(ball.surface, ball.rect)
                            return
                                
                        #Collision with paddle
                        offset_x = (ball.rect.left - paddle.rect.left)
                        offset_y = (ball.rect.top - paddle.rect.top)
                        if (paddle.mask.overlap(ball.mask, (offset_x, offset_y)) != None):
                                #Test to see if horizontal or vertical collision
                                print("collision with paddle")
                                print("velocity before: " + str(ball.velocity))
                                velocity_test = (ball.velocity[0],-ball.velocity[1])
                                test_rect = ball.rect.move(velocity_test)
                                test_offset_x, test_offset_y = (test_rect.left - paddle.rect.left), (test_rect.top - paddle.rect.top)
                                if (paddle.mask.overlap(ball.mask, (test_offset_x, test_offset_y)) != None):
                                #horizontal collision
                                        if(cls.touch_paddle==False):
                                                ball.velocity[0] = -ball.velocity[0]
                                                cls.touch_paddle=True
                                        ball.velocity[1] = -1*abs(ball.velocity[1])
                                print("velocity after: " + str(ball.velocity))
                                else:
                                #vertical collision
                                        ball.velocity[1] = -1*abs(ball.velocity[1])
                                print("velocity after: " + str(ball.velocity))
                                surface.blit(ball.surface, ball.rect)
                                return
                        elif(abs(ball.rect.left - paddle.rect.left) > 100):
                                cls.touch_paddle = False

                        #Collision with bricks
                        for (ind,l) in enumerate(bricklist):
                                offset_x, offset_y = (ball.rect.left - l.rect.left), (ball.rect.top - l.rect.top)
                                if (l.mask.overlap(ball.mask, (offset_x, offset_y)) != None):
                                        print("collision with brick")
                                        print("velocity before: " + str(ball.velocity))
                                        velocity_test = (ball.velocity[0],-ball.velocity[1])
                                        test_rect = ball.rect.move(velocity_test)
                                        test_offset_x, test_offset_y = (test_rect.left - l.rect.left), (test_rect.top - l.rect.top)
                                        if (l.mask.overlap(ball.mask, (test_offset_x, test_offset_y)) != None):
                                                ball.velocity[0] = -ball.velocity[0]
                                            print("velocity after: " + str(ball.velocity))
                                        else:
                                                ball.velocity[1] = -ball.velocity[1]
                                                print("velocity after: " + str(ball.velocity))
                                        l.resistance = l.resistance-1                                        
                                        if(l.resistance==0):
                                                del bricklist[ind]    
                        surface.blit(ball.surface, ball.rect)

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
