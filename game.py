import sys

import pygame
import math

from pygame import Vector2
from pygame.locals import *
import pygame.freetype
from pygame_widgets.button import Button
from pygame_widgets.toggle import Toggle
import pygame_widgets
from threading import Timer
import random

pygame.init()


class Target:
    def __init__(self, x, y, radius, surface):
        self.x = x
        self.y = y
        self.radius = radius
        self.surface = surface
        self.color = (255, 0, 0, 160)

    def draw(self):
        pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.radius, width=3)
        pygame.draw.line(self.surface, self.color, (self.x - self.radius - 10, self.y),
                         (self.x + self.radius + 10, self.y), width=3)
        pygame.draw.line(self.surface, self.color, (self.x, self.y - self.radius - 10),
                         (self.x, self.y + self.radius + 10), width=3)


def tim():
    return


def calculate_new_xy(old_xy, speeded, angle_in_degrees):
    move_vec = pygame.math.Vector2()
    move_vec.from_polar((speeded, angle_in_degrees))
    return old_xy + move_vec


size = 800, 500
sizerad = 500, 500
sizeinter = 300, 500
displaysize = 250, 200
displaybase = 280, 230
screener = pygame.display.set_mode(size)
screen = pygame.surface.Surface(sizerad, pygame.SRCALPHA)
clock = pygame.time.Clock()
interface = pygame.Surface(sizeinter, pygame.SRCALPHA)
data = pygame.Surface(displaysize, pygame.SRCALPHA)
datasurf = pygame.Surface(displaybase, pygame.SRCALPHA)
dataoff = pygame.Surface(displaysize, pygame.SRCALPHA)
run = True
radc = (250, 250)
radl = 1000
startpoint = pygame.math.Vector2(250, 250)
endpoint = pygame.math.Vector2(250, 5)
screen.fill(Color("black"))
angle = 0
contactx = 100
contacty = 100
currentx = contactx
currenty = contacty
numcnts = 5
radius = 5
interface.fill((50, 50, 50, 255))
contacts = [(random.randint(200, 300), random.randint(200, 300), random.randint(-180, 180), random.randint(1, 7))]
radsees = []
for i in contacts:
    radsees.append(i[0:2])
hitboxes = []
upds = []
for i in contacts:
    hitboxes.append(pygame.Rect(i[0] - radius, i[1] - radius, radius, radius))
radsurf = pygame.Surface(sizerad, pygame.SRCALPHA)
selected = None
Threads = []
target = None
torpedoes = None
torpedofired = False
inflag = False
radrect = radsurf.get_rect()
pole = pygame.math.Vector2(radrect.center)
pygame.mixer_music.load("res/audio/ambience.mp3")
pygame.mixer_music.set_volume(0.2)
pygame.mixer_music.play()
font0 = pygame.font.Font("res/font/ocra.ttf", 35)


def changetarget():
    if not torpedofired:
        global selected
        maxer = len(radsees)
        if selected is None:
            if maxer == 0:
                selected = None
                return
            selected = 0
        else:
            if maxer - 1 == selected:
                selected = 0
            else:
                selected += 1


def desel():
    if not torpedofired:
        global selected, target
        selected = None
        target = None


def targetship():
    if not torpedofired:
        global selected, target
        if selected is not None:
            target = selected


def firetorpedo():
    global torpedofired, torpedoes, selected, target, cntse
    if not torpedofired and selected is not None and target is not None:
        torpedoes = (250, 250, 0, 90)  # calcangle((xlaunch, ylaunch), (contacts[target][0], contacts[target][1]))
        torpedofired = True


def calcangle(xyaut, xytarg):
    pols = Vector2(xytarg)
    ner, anglers = (pols - xyaut).as_polar()
    return anglers

def genscreen():
    surfer = pygame.Surface(displaysize, pygame.SRCALPHA)
    surfer.fill((255, 255, 255, 0))
    if selected is None and target is None:
        txt = font0.render("[NO TARGET]", True, (0, 150, 0))
        txt2 = font0.render("[SELECTED]", True, (0, 150, 0))
        txtlen = [txt.get_width(), txt.get_height()]
        txt2len = [txt2.get_width(), txt2.get_height()]

        surfer.blit(txt, (displaysize[0]/2 - txtlen[0]/2, displaysize[1]/2 - txtlen[1]))
        surfer.blit(txt2, (displaysize[0]/2 - txt2len[0]/2, displaysize[1]/2))
    return surfer


btt = Button(win=screener, x=573, y=30, text="Next", width=70, height=70, onClick=changetarget,
             pressedColour=(0, 200, 20), radius=10, fontSize=18, shadowDistance=1)
bttdes = Button(win=screener, x=659, y=30, text="Deselect", width=70, height=70, onClick=desel,
                pressedColour=(0, 200, 20), radius=10, fontSize=18, shadowDistance=1)
btttar = Button(win=screener, x=573, y=110, text="Target", width=70, height=70, onClick=targetship,  # 15
                pressedColour=(0, 200, 20), radius=10, fontSize=18, shadowDistance=1)
bttfire = Button(win=screener, x=659, y=110, text="FIRE", width=70, height=70, onClick=firetorpedo,
                 pressedColour=(255, 0, 0), radius=10, colour=Color("red"), fontSize=18, shadowDistance=1)
displaybtt = Toggle(win=screener, x=680, y=200, width=20, height=20, handleOnColour=Color("green"), handleOffColour=Color("red"))
radbtt = Toggle(win=screener, x=600, y=200, width=20, height=20, handleOnColour=Color("green"), handleOffColour=Color("red"))
pygame.mixer.init()
offlayer = pygame.Surface(sizerad, pygame.SRCALPHA)
radbase = pygame.Surface(sizerad)
while run:
    ondis = displaybtt.getValue()
    onrad = radbtt.getValue()
    events = pygame.event.get()
    collisions = []
    hitboxes = []
    offlayer.fill((100, 100, 100, 60))
    radbase.fill((0, 0, 0))
    if not contacts:
        choice = random.randint(1, 50)
    else:
        choice = random.randint(1, 1200)
    datasurf.fill(color=Color("black"))
    if selected is not None:
        xsel = radsees[selected][0] - 10
        ysel = radsees[selected][1] - 10
    else:
        xsel = None
        ysel = None
    if choice == 50:
        contacts.append(
            (random.randint(100, 400), random.randint(100, 400), random.randint(-180, 180), random.randint(1, 7)))
        lastcnt = len(contacts) - 1
        nowlist = contacts[lastcnt]
        radsees.append(nowlist[0:2])
    for i in contacts:
        index = contacts.index(i)
        hdg = i[2] + (random.randint(-2, 5) / 10)
        coords = calculate_new_xy((i[0], i[1]), i[3] / 90, hdg)  # i2 + 90 true nav heading
        contacts[index] = (coords[0], coords[1], hdg, i[3])
        speed = i[3]
        if 7 >= speed >= -7:
            speed = i[3] + (random.randint(-1, 1) / 10)
        elif speed > 7:
            speed -= 0.1
        else:
            speed += 0.1
        nowi = contacts[index]
        contacts[index] = (nowi[0], nowi[1], nowi[2], speed)
    for i in contacts:
        hitboxes.append(pygame.Rect(i[0] - radius, i[1] - radius, radius * 2, radius * 2))
    screen.fill((0, 0, 0))
    radsurf.fill((255, 255, 255, 0))
    radsurf.fill((0, 255, 0, 60))
    screener.fill((50, 50, 50))
    pygame_widgets.update(events)
    dataoff.fill((100, 100, 100, 60))
    data.fill((0, 255, 0, 60))
    for e in events:
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            run = False
            break
    circle = pygame.draw.circle(screen, Color("green"), (250, 250), 250, 4)
    for i in range(200, 0, -50):
        pygame.draw.circle(screen, Color("green"), (250, 250), i, 4)
    if torpedofired:
        torpedoonwater = pygame.Rect(torpedoes[0] - 2.5, torpedoes[1] - 5, 5, 10)
        if torpedofired:
            if torpedoonwater.colliderect(hitboxes[target]):
                torpedofired = False
                contacts.pop(target)
                radsees.pop(target)
                hitboxes.pop(target)
                target = None
                torpedoes = None
                selected = None
                screen.fill((0, 0, 0))
                radsurf.fill((255, 255, 255, 0))
                radsurf.fill((0, 255, 0, 60))
                screener.fill((50, 50, 50))
                splash = pygame.mixer.Channel(0)
                splashsound = pygame.mixer.Sound("res/audio/splash.mp3")
                splash.play(splashsound)

                continue
            coords = (torpedoes[0], torpedoes[1])
            heading = torpedoes[3]
            destroytarget = contacts[target]
            targethdg = calcangle(coords, (destroytarget[0], destroytarget[1]))
            speed = torpedoes[2]
            if speed < 0.12:
                speed += 0.01
            oldxy = (torpedoes[0], torpedoes[1])
            newxy = calculate_new_xy(oldxy, speed, heading)
            coords = newxy
            if pygame.math.Vector2(newxy).distance_to((destroytarget[0], destroytarget[1])) > 0:
                if abs(targethdg - heading) < 1:
                    if heading < targethdg:
                        heading += abs(targethdg - heading)
                        rot = (heading + abs(targethdg - heading)) % 360
                    else:
                        heading -= abs(targethdg - heading)
                        rot = (heading - abs(targethdg - heading)) % 360
                else:
                    if heading < targethdg:
                        heading = (heading + 3)
                        rot = (heading + 3) % 360
                    else:
                        heading = heading - 3
                        rot = (heading - 3) % 360
            torpedoes = (newxy[0], newxy[1], speed, heading)
            torpedoonwater = pygame.Rect(torpedoes[0] - 5, torpedoes[1] - 12.5, 10, 25)
            vectx = destroytarget[0] - torpedoes[0]
            vecty = destroytarget[1] - torpedoes[1]
            rads = math.atan2(vecty, vectx) - math.pi / 2
            rads %= 2 * math.pi
            direr = math.degrees(rads)
            surf = radsurf.subsurface(torpedoonwater)
            surf = surf.copy()
            surf.fill(Color("black"))
            surf = pygame.transform.rotozoom(surf, direr, 1)
            print(f"{targethdg};{heading};{direr}")
            radsurf.blit(surf, torpedoonwater.center)
            # pygame.draw.rect(radsurf, color=(0, 0, 0), rect=torpedoonwater)

    angle = (angle + 1) % 360
    x = radc[0] + math.cos(math.radians(angle)) * radl
    y = radc[1] + math.sin(math.radians(angle)) * radl
    xdraw = radc[0] + math.cos(math.radians(angle)) * 250
    ydraw = radc[1] + math.sin(math.radians(angle)) * 250
    pygame.draw.circle(screen, Color("green"), (250, 250), 10, 0)
    check = False
    if xsel is not None and ysel is not None:
        rectselec = pygame.Rect(xsel, ysel, 20, 20)
        check = True
    for i in hitboxes:
        if i.clipline(radc, (x, y)):
            collisions.append(True)
            if len(upds) != len(contacts):
                upds.append(Timer(1, tim))
        else:
            collisions.append(False)
            if len(upds) != len(contacts):
                upds.append(Timer(1, tim))
        if collisions[hitboxes.index(i)]:
            if not upds[hitboxes.index(i)].is_alive():
                upds[hitboxes.index(i)] = Timer(1, tim)
                upds[hitboxes.index(i)].start()
                radsees[hitboxes.index(i)] = tuple(list(contacts[hitboxes.index(i)][0:2]))
        if circle.contains(i):
            if target == hitboxes.index(i) or selected == hitboxes.index(i):
                if check == True and target is None:
                    pygame.draw.rect(screen, Color("blue"), rectselec, width=2)
                if target is not None:
                    targx = radsees[target][0]
                    targy = radsees[target][1]
                    targ = Target(targx, targy, radius + 10, radsurf)
                    targ.draw()
            pygame.draw.circle(radsurf, Color("red"), radsees[hitboxes.index(i)], 5, 0)
    pygame.draw.line(screen, Color("green"), radc, (xdraw, ydraw), width=4)
    """for i in hitboxes:
        pygame.draw.rect(radsurf, Color("blue"), i)"""
    line = pygame.draw.line(screen, Color("green"), radc, (x, y), width=0)
    """for i in hitboxes:
        pygame.draw.rect(screen, Color("blue"), i)"""
    screener.blit(radbase, (0, 0))
    if onrad:
        screen.blit(radsurf, (0, 0))
        screener.blit(screen, (0, 0))
    else:
        screener.blit(offlayer, (0, 0))
    if ondis:
        surftext = genscreen()
        data.blit(surftext, (0, 0))
        datasurf.blit(data, (15, 15))
    else:
        datasurf.blit(dataoff, (15, 15))
    screener.blit(datasurf, (510, 250))
    pygame.display.flip()
    clock.tick(140)

for i in range(len(upds)):
    upds[i].cancel()
pygame.quit()
sys.exit(0)
