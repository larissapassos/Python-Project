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
        
        if ball.rect.left < 0 or ball.rect.right > width:
            ball.velocity[0] = - ball.velocity[0]
            surface.blit(ball.surface,ball.rect)
        if ball.rect.top  < 0:
            ball.velocity[1] = - ball.velocity[1]
            surface.blit(ball.surface, ball.rect)
                                
        #Collision with paddle
        offset_x = (ball.rect.left - paddle.rect.left)
        offset_y = (ball.rect.top - paddle.rect.top)
        if (paddle.mask.overlap(ball.mask, (offset_x, offset_y)) != None):
            #Test to see if horizontal or vertical collision
            velocity_test = (ball.velocity[0],-ball.velocity[1])
            test_rect = ball.rect.move(velocity_test)
            test_offset_x, test_offset_y = (test_rect.left - paddle.rect.left), (test_rect.top - paddle.rect.top)
            if (paddle.mask.overlap(ball.mask, (test_offset_x, test_offset_y)) != None):
                #horizontal collision
                if(cls.touch_paddle==False):
                    ball.velocity[0] = -ball.velocity[0]
                    cls.touch_paddle=True
                ball.velocity[1] = -1*abs(ball.velocity[1])
            else:
                #vertical collision
                ball.velocity[1] = -1*abs(ball.velocity[1])
            surface.blit(ball.surface, ball.rect)
        elif (abs(ball.rect.left - paddle.rect.left) > 100):
            cls.touch_paddle = False

        #Collision with bricks
        for (ind,l) in enumerate(bricklist):
            offset_x, offset_y = (ball.rect.left - l.rect.left), (ball.rect.top - l.rect.top)
            if (l.mask.overlap(ball.mask, (offset_x, offset_y)) != None):
                velocity_test = (ball.velocity[0],-ball.velocity[1])
                test_rect = ball.rect.move(velocity_test)
                test_offset_x, test_offset_y = (test_rect.left - l.rect.left), (test_rect.top - l.rect.top)
                if (l.mask.overlap(ball.mask, (test_offset_x, test_offset_y)) != None):
                    ball.velocity[0] = -ball.velocity[0]
                else:
                    ball.velocity[1] = -ball.velocity[1]
                l.resistance = l.resistance-1                                        
                if(l.resistance==0):
                    del bricklist[ind]    
            surface.blit(ball.surface, ball.rect)
