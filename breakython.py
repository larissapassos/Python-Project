import pygame,sys
import time
import game_elements
from game_elements import Level
from game import Movement


def main():
    resist = [ [0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0 ],\
              [0,0,0,1,2,2,2,2,2,2,2,2,1,0,0,0 ],\
              [0,0,0,0,1,3,3,3,3,3,3,1,0,0,0,0 ],\
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],\
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ]]
    
    color = [ [0,0,'O','O','O','O','O','O','O','O','O','O','O','O',0,0 ],\
              [0,0,0,'O','W','W','W','W','W','W','W','W','O',0,0,0 ],\
              [0,0,0,0,'O','M','M','M','M','M','M','O',0,0,0,0 ],\
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],\
              [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ]]

    lv = Level(resist,color,[0,0])

    screen_width, screen_height = 640, 480
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([screen_width, screen_height])
    white, black = (255, 255, 255), (0, 0, 0)
    screen.fill(white)
    screen.blit(lv.paddle.surface,lv.paddle.rect)
    screen.blit(lv.ball.surface,lv.ball.rect)
    for l in lv.bricklist:
        screen.blit(l.surface,l.rect)
    pygame.display.update()
    
    def blit_all_but_ball():
        screen.fill(white)
        screen.blit(lv.paddle.surface,lv.paddle.rect)
        for l in lv.bricklist:
            screen.blit(l.surface,l.rect)
        screen.blit(lv.ball.surface, lv.ball.rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()            
        blit_all_but_ball()
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            Movement.move_paddle_left(screen,lv.paddle)
        elif key[pygame.K_RIGHT]:
            Movement.move_paddle_right(screen,lv.paddle)
        elif key[pygame.K_SPACE]:
            lv.ball.velocity = [-1,-1]
        Movement.move_ball(screen,lv.ball,lv.bricklist,lv.paddle)         
        pygame.display.update()
        clock.tick(200)
    
        
if __name__=="__main__":
    main()