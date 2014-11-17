import sys
import time
import game_elements
from game_elements import Level, menu
from game import Movement
from pygame import *

white, black, blue = (255, 255, 255), (0, 0, 0), (0, 0, 255)
screen_width, screen_height = 640, 480
init()
clock = time.Clock()
screen = display.set_mode([screen_width, screen_height])
max_level = 5

def blit_all_but_ball(lv):
    # Update screen
    screen.fill(black)
    screen.blit(lv.paddle.surface,lv.paddle.rect)
    for l in lv.bricklist:
        screen.blit(l.surface,l.rect)

def get_resistance(filename):
    resist = []
    f = open(filename, 'r')
    for line in f:
        row = []
        list_resists = line.split(' ')
        for r in list_resists:
            row.append(int(r))
        resist.append(row)
    return resist

def start_menu():
    screen.fill(black)
    font.init()
    f = font.Font('resources/airstrip.ttf', 45)
    f1 = font.Font('resources/airstrip.ttf', 25)
    f2 = font.Font('resources/airstrip.ttf', 15)
    mainmenu = f.render('BREAKYTHON', 1, blue)
    r = mainmenu.get_rect()
    r.centerx, r.top = 320, 120
    screen.blit(mainmenu, r)
    display.flip()

    menu1 = {"menu": ['PLAY', 'EXIT'], "font1": f1, "pos": 'center', "color1": blue, "light": 6}

    resp = "re-show"
    while resp == "re-show":
        resp = menu(**menu1)[0]
    if resp == 'PLAY':
        game(1)

    if resp == 'EXIT':
        quit()
        sys.exit()

def pause_menu():
    screen.fill(black)
    font.init()
    f = font.Font('resources/airstrip.ttf', 45)
    f1 = font.Font('resources/airstrip.ttf', 25)
    f2 = font.Font('resources/airstrip.ttf', 15)
    mainmenu = f.render('PAUSE', 1, blue)
    r = mainmenu.get_rect()
    r.centerx, r.top = 320, 120
    screen.blit(mainmenu, r)
    display.flip()

    menu1 = {"menu": ['CONTINUE', 'EXIT'], "font1": f1, "pos": 'center', "color1": blue, "light": 6}

    resp = "re-show"
    while resp == "re-show":
        resp = menu(**menu1)[0]
    if resp == 'CONTINUE':
        return
    if resp == 'EXIT':
        quit()
        sys.exit()

def die_menu():
    screen.fill(black)
    font.init()
    f = font.Font('resources/airstrip.ttf', 45)
    f1 = font.Font('resources/airstrip.ttf', 25)
    f2 = font.Font('resources/airstrip.ttf', 15)
    mainmenu = f.render('GAME OVER', 1, blue)
    r = mainmenu.get_rect()
    r.centerx, r.top = 320, 120
    screen.blit(mainmenu, r)
    display.flip()

    menu1 = {"menu": ['NEW GAME', 'EXIT'], "font1": f1, "pos": 'center', "color1": blue, "light": 6}

    resp = "re-show"
    while resp == "re-show":
        resp = menu(**menu1)[0]
    if resp == 'NEW GAME':
        game(1)
    if resp == 'EXIT':
        quit()
        sys.exit()

def won_menu(level):
    screen.fill(black)
    font.init()
    f = font.Font('resources/airstrip.ttf', 45)
    f1 = font.Font('resources/airstrip.ttf', 25)
    f2 = font.Font('resources/airstrip.ttf', 15)
    if level < max_level:
        mainmenu = f.render('LEVEL COMPLETED', 1, blue)
    else:
        mainmenu = f.render('YOU WON!', 1, blue)
    r = mainmenu.get_rect()
    r.centerx, r.top = 320, 120
    screen.blit(mainmenu, r)
    display.flip()

    if level < max_level:
        menu1 = {"menu": ['NEXT LEVEL', 'EXIT'], "font1": f1, "pos": 'center', "color1": blue, "light": 6}
    else:
        menu1 = {"menu": ['NEW GAME', 'EXIT'], "font1": f1, "pos": 'center', "color1": blue, "light": 6}

    resp = "re-show"
    while resp == "re-show":
        resp = menu(**menu1)[0]
    if resp == 'NEXT LEVEL':
        game(level + 1)
    if resp == 'NEW GAME':
        game(1)
    if resp == 'EXIT':
        quit()
        sys.exit()

def game(level_number):
    filename = "resources/level" + str(level_number)
    resist = get_resistance(filename)
    
    lv = Level(resist,[0,0], level_number)

    screen.fill(black)
    screen.blit(lv.paddle.surface,lv.paddle.rect)
    screen.blit(lv.ball.surface,lv.ball.rect)
    for l in lv.bricklist:
        screen.blit(l.surface,l.rect)
    display.update()

    while True:
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
        k = key.get_pressed()
        if k[K_LEFT]:
            Movement.move_paddle_left(screen,lv.paddle)
        elif k[K_RIGHT]:
            Movement.move_paddle_right(screen,lv.paddle)
        elif k[K_SPACE]:
            v = 0.5 + (0.5 * lv.number)
            lv.ball.velocity = [-v,v]
            break;
        lv.ball.rect.bottom = lv.paddle.rect.top
        lv.ball.rect.centerx = lv.paddle.rect.centerx
        blit_all_but_ball(lv)
        screen.blit(lv.ball.surface, lv.ball.rect)
        display.update()
        clock.tick(200)
    
    while True:
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()            
        blit_all_but_ball(lv)
        k = key.get_pressed()
        if k[K_LEFT]:
            Movement.move_paddle_left(screen,lv.paddle)
        elif k[K_RIGHT]:
            Movement.move_paddle_right(screen,lv.paddle)
        elif k[K_ESCAPE]:
            pause_menu()
        elif k[K_m]:
            lv.bricklist = []
        Movement.move_ball(screen,lv.ball,lv.bricklist,lv.paddle)
        if Movement.died(lv.ball):
            die_menu()
        if Movement.won(lv):
            won_menu(lv.number)       
        display.update()
        clock.tick(200)
    
        
if __name__=="__main__":
    start_menu()