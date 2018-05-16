#!/usr/bin/env python
import sys, os, time, subprocess, commands, pygame
from pygame.locals import *
from subprocess import *
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

# Initialize pygame modules individually (to avoid ALSA errors) and hide mouse
pygame.init()
pygame.font.init()
pygame.display.init()

# pygame.mouse.set_visible(0)

# define function for printing text in a specific place with a specific width and height with a specific colour and border
def make_button(text, xpo, ypo, height, width, colour):
    pygame.draw.rect(screen, tron_regular, (xpo-10,ypo-10,width,height),3)
    pygame.draw.rect(screen, tron_light, (xpo-9,ypo-9,width-1,height-1),1)
    pygame.draw.rect(screen, tron_regular, (xpo-8,ypo-8,width-2,height-2),1)
    font=pygame.font.Font(None,42)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo))


# define function for printing text in a specific place with a specific colour
def make_label(text, xpo, ypo, fontsize, colour):
    font=pygame.font.Font(None,fontsize)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo))

# define function that checks for touch location
def on_touch():
    # get the position that was touched
    touch_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
    #  x_min                 x_max   y_min                y_max
    # button 1 event
    if 30 <= touch_pos[0] <= 240 and 105 <= touch_pos[1] <=160:
            button(1)
    # button 2 event
    if 260 <= touch_pos[0] <= 470 and 105 <= touch_pos[1] <=160:
            button(2)
    # button 3 event
    if 30 <= touch_pos[0] <= 240 and 180 <= touch_pos[1] <=235:
            button(3)
    # button 4 event
    if 260 <= touch_pos[0] <= 470 and 180 <= touch_pos[1] <=235:
            button(4)
    # button 5 event
    if 30 <= touch_pos[0] <= 240 and 255 <= touch_pos[1] <=310:
            button(5)
    # button 6 event
    if 260 <= touch_pos[0] <= 470 and 255 <= touch_pos[1] <=310:
            button(6)

def run_cmd(cmd):
    process = Popen(cmd.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

class GlobalIndex(object):
    _index = 0
    def setIndex(self, val):
        self._index = val
    def index(self):
        return self._index

index = GlobalIndex()  

# Define each button press action
def button(number):
    if number == 1:
        # X TFT
        pygame.quit()
        ## Requires "Anybody" in dpkg-reconfigure x11-common if we have scrolled pages previously
        run_cmd("/usr/bin/sudo -u pi FRAMEBUFFER=/dev/fb1 startx")
        os.execv(__file__, sys.argv)        

    if number == 2:
        # X HDMI
        pygame.quit()
        ## Requires "Anybody" in dpkg-reconfigure x11-common if we have scrolled pages previously
        run_cmd("/usr/bin/sudo -u pi FRAMEBUFFER=/dev/fb0 startx")
        os.execv(__file__, sys.argv)        


    if number == 3:
        # exit
        pygame.quit()
        sys.exit()

    if number == 4:
        # htop
        pygame.quit()
        process = subprocess.call("/usr/bin/htop", shell=True)
        os.execv(__file__, sys.argv)        

    if number == 5:
        # next page
        pygame.quit()
        ##startx only works when we don't use subprocess here, don't know why
        page=os.environ["MENUDIR"] + "menu_screenoff.py"
        os.execvp("python", ["python", page])
        sys.exit()

    if number == 6:
        # next page
        # screen.blit(bif,(0-20,0))
        # s1.move(-20,0)
        index.setIndex(1)
        #pygame.quit()
        # ##startx only works when we don't use subprocess here, don't know why
        # page=os.environ["MENUDIR"] + "menu_kali-2.py"
        # os.execvp("python", ["python", page])
        # sys.exit()



# colors    R    G    B
white    = (255, 255, 255)
tron_whi = (189, 254, 255)
red      = (255,   0,   0)
green    = (  0, 255,   0)
blue     = (  0,   0, 255)
tron_blu = (  0, 219, 232)
black    = (  0,   0,   0)
cyan     = ( 50, 255, 255)
magenta  = (255,   0, 255)
yellow   = (255, 255,   0)
tron_yel = (255, 218,  10)
orange   = (255, 127,   0)
tron_ora = (255, 202,   0)

# Tron theme orange
tron_regular = tron_ora
tron_light   = tron_yel
tron_inverse = tron_whi

# Tron theme blue
##tron_regular = tron_blu
##tron_light   = tron_whi
##tron_inverse = tron_yel 

# Set up the base menu you can customize your menu with the colors above

#set size of the screen
size = width, height = 800, 480
screen = pygame.display.set_mode(size)


class Button(object):
    def __init__(self, label, rect):
        self._label = label
        self.x, self.y, self.h, self.w = rect
        
    def render(self):
        make_button(self._label, self.x, self.y, self.h, self.w, tron_light)

    def move(self, deltax, deltay):
        self.x += deltax
        self.y += deltay
        self.h += deltay
        self.w += deltax

    def click(self):
        pass

    def __contains__(self, touch_pos):
        return (self.x <= touch_pos[0] <= 240 and self.y <= touch_pos[1] <=160)
        # if 30 <= touch_pos[0] <= 240 and 105 <= touch_pos[1] <=160:


class Screen(object):
    def __init__(self):
        self._objects = []

    def attach(self, *objs):
        for obj in objs:
            self._objects += [obj]

    def move(self, deltax, deltay):
        for n in self._objects:
            n.move(deltax, deltay)

    def render(self):
        for n in self._objects:
            n.render()

    def on_touch(self, touch_pos):
        # id = (touch_pos in a1) * 1 + \
            # (touch_pos in a2) * 2 + \
            # (touch_pos in a3) * 3 + \
            # (touch_pos in a4) * 4 + 
        #  x_min                 x_max   y_min                y_max
        # button 1 event
        if 30 <= touch_pos[0] <= 240 and 105 <= touch_pos[1] <=160:
                button(1)
        # button 2 event
        if 260 <= touch_pos[0] <= 470 and 105 <= touch_pos[1] <=160:
                button(2)
        # button 3 event
        if 30 <= touch_pos[0] <= 240 and 180 <= touch_pos[1] <=235:
                button(3)
        # button 4 event
        if 260 <= touch_pos[0] <= 470 and 180 <= touch_pos[1] <=235:
                button(4)
        # button 5 event
        if 30 <= touch_pos[0] <= 240 and 255 <= touch_pos[1] <=310:
                button(5)
        # button 6 event
        if 260 <= touch_pos[0] <= 470 and 255 <= touch_pos[1] <=310:
                button(6)


# Background Color


# Outer Border
pygame.draw.rect(screen, tron_regular, (0,0,width-1,height-1),8)
pygame.draw.rect(screen, tron_light, (2,2,width-5,height-5),2)

pi_hostname = run_cmd("hostname")
pi_hostname = "  " + pi_hostname[:-1]
# Buttons and labels
# First Row Label
make_label(pi_hostname, 32, 30, 48, tron_inverse)
# Second Row buttons 3 and 4
a1 = Button("    X on TFT", (30, 105, 55, 210))
a2 = Button("   X on HDMI", (260, 105, 55, 210))
# Third Row buttons 5 and 6
a3 = Button("    Terminal", (30, 180, 55, 210))
a4 = Button("        hTop", (260, 180, 55, 210))
# Fourth Row Buttons
a5 = Button("          <<<", (30, 255, 55, 210))
a6 = Button("          >>>", (260, 255, 55, 210))

a7 = Button("         Koko", (30, 105, 55, 210))



s1 = Screen()
s1.attach(a1,a2,a3,a4,a5,a6)

s2 = Screen()
s2.attach(a7)

screens = [s1,s2]



#While loop to manage touch screen inputs
while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
            screens[index.index()].on_touch(pos)

        #ensure there is always a safe way to end the program if the touch screen fails
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
    screen.fill(black)
    screens[index.index()].render()
    pygame.display.update()
    pygame.display.flip()
    ## Reduce CPU utilisation
    time.sleep(0.1)
