import sys
import time
import game_elements
from game_elements import Level
from game import Movement
from pygame import *

white, black, blue = (255, 255, 255), (0, 0, 0), (0, 0, 255)
screen_width, screen_height = 640, 480
init()
clock = time.Clock()
screen = display.set_mode([screen_width, screen_height])

def blit_all_but_ball(lv):
    # Update screen
    screen.fill(black)
    screen.blit(lv.paddle.surface,lv.paddle.rect)
    for l in lv.bricklist:
        screen.blit(l.surface,l.rect)

def menu(menu, pos='center', font1=None, color1=(128, 128, 128), interline=5, justify=True, light=5):

    class Item(Rect):

        def __init__(self, menu, label):
            Rect.__init__(self, menu)
            self.label = label

    def show():
        i = Rect((0, 0), font1.size(menu[idx].label))
        if justify:
            i.center = menu[idx].center
        else:
            i.midleft = menu[idx].midleft
        display.update(
            (screen.blit(bg, menu[idx], menu[idx]), screen.blit(font1.render(menu[idx].label, 1, (255, 255, 255)), i)))

        time.wait(50)
        screen.blit(bg, r2, r2)
        [screen.blit(font1.render(item.label, 1, color1), item)
         for item in menu if item != menu[idx]]
        r = screen.blit(font1.render(menu[idx].label, 1, color2), i)
        display.update(r2)

        return r

    events = event.get()
    screen = display.get_surface()
    scrrect = screen.get_rect()
    bg = screen.copy()
    color2 = list(map(lambda x: x + (255 - x) * light // 10, color1))
    m = max(menu, key=font1.size)
    r1 = Rect((0, 0), font1.size(m))
    ih = r1.size[1]
    r2 = Rect((0, 0), font1.size(m))
    r2.union_ip(r1)
    w, h = r2.w - r1.w, r2.h - r1.h
    r1.h = (r1.h + interline) * len(menu) - interline
    r2 = r1.inflate(w, h)

    try:
        setattr(r2, pos, getattr(scrrect, pos))
    except:
        r2.topleft = pos
    if justify:
        r1.center = r2.center
    else:
        r1.midleft = r2.midleft

    menu = [Item(((r1.x, r1.y + e * (ih + interline)), font1.size(i)), i)
            for e, i in enumerate(menu)if i]
    if justify:
        for i in menu:
            i.centerx = r1.centerx

    idx = -1
    display.set_caption("BREAKYTHON")
    show()

    while True:
    
        ev = event.wait()
        if ev.type == KEYDOWN:
            try:
                idx = (idx + {K_UP: -1, K_DOWN: 1}[ev.key]) % len(menu)
                r = show()
            except:
                if ev.key in (K_RETURN, K_KP_ENTER):
                    ret = menu[idx].label, idx
                    break
                elif ev.key == K_ESCAPE:
                    ret = None, None
                    break
        elif ev.type == QUIT:
            quit()
            sys.exit()
    screen.blit(bg,r2,r2)
    display.update(r2)

    for ev in events:
        event.post(ev)
    return ret

def start_menu():
    screen.fill(black)
    font.init()
    f = font.Font('resources/airstrip.ttf', 45)
    f1 = font.Font('resources/airstrip.ttf', 25)
    f2 = font.Font('resources/airstrip.ttf', 15)
    mainmenu = f.render('BREAKYTHON', 1, blue)
    r = mainmenu.get_rect()
    r.centerx, r.top = 300, 120
    screen.blit(mainmenu, r)
    display.flip()

    menu1 = {"menu": ['PLAY', 'EXIT'], "font1": f1, "pos": 'center', "color1": blue, "light": 6}

    resp = "re-show"
    while resp == "re-show":
        resp = menu(**menu1)[0]
    if resp == 'PLAY':
        game()

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
    r.centerx, r.top = 300, 120
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

def game():
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
            lv.ball.velocity = [-1,-1]
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
        Movement.move_ball(screen,lv.ball,lv.bricklist,lv.paddle)         
        display.update()
        clock.tick(200)
    
        
if __name__=="__main__":
    start_menu()