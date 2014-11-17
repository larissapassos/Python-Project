import pygame,sys
from pygame import *

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
        self.paddle = Paddle(460,320,2)                                      
        self.ball = Ball(460 - self.paddle.rect.h,320,v)

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