# tag 068
# 192.168.33.39 12000
import pygame, time, os, sys, random
from pygame.locals import *
from menu import *

#define boundry walls
TILE_WALLS = ["tl2", "tr", "bl", "br", "tm", "bm", "lm", "rm",
              "chest", "wall", "stonewall","wall2","w2r"] # 1
TILE_PUSH = [] # 2 --- unused because rock = object
TILE_TREASURE = ["chest"] # 4

# all images to be used
imagesToLoad = ["character.png", "tl2.png", "tr.png", "bl.png", "br.png", "grass.png", "bg.png",
                "lm.png", "rm.png", "tm.png", "bm.png", "grass2.png", "grass3.png", "wallsm.png",
                "chest.png", "rock.png", "wall.png", "stone1.png","stone2.png","stone3.png", "stonewall.png","wall2.png","w2r.png"]

# define movement keys here assigning them to names so methods for movement can be used
P_CONTROLS = [
    {"up": K_UP, "down": K_DOWN, "left": K_LEFT, "right": K_RIGHT},
    {"up": K_w, "down": K_s, "left": K_a, "right": K_d}
]


class Level(object):
    def __init__(self, levelFile):
        self.players = [Player(x, 0, 0) for x in range(2)]
        self.chests = 0

        self.load(levelFile)
    def load(self, level):

	#this is used to set the level creation its quite handy as those letters correspond to certain objects
        tileMap = {
            "+": ["grass", "grass", "grass", "grass", "grass2", "grass2", "grass3"],
            " ": ["stone2","stone1","stone3"],
			"$": "chest", "#": "wall", ".": "wallsm",
            "<": "tl2", ">": "tr", "v": "bl", "V": "br",
            ",": "lm", "^": "tm", "/": "rm", "_": "bm", "s":"stonewall", "l":"wall2", "R":"w2r"
        }

        lsrc = [x.strip() for x in open(os.path.join("Levels", level), "r").readlines()]
        self.name = lsrc[0]
        pygame.display.set_caption("Escape from Cera " + self.name)
        self.xdim, self.ydim = lsrc[1].split()
        self.xdim = int(self.xdim)
        self.ydim = int(self.ydim)
        levLines = []
        for y in range(self.ydim):
            levLines.append(lsrc[2 + y])

        self.array = []

        y = 0
        for line in levLines:
            levTiles = []
            x = 0
            for unit in line:
                if unit in tileMap:
                    levTiles.append(Tile(tileMap[unit]))
                    if unit == "$":
                        self.chests += 1
                if unit == "1":
                    levTiles.append(Tile(tileMap[" "]))
                    self.players[0].x, self.players[0].y = x, y
                if unit == "2":
                    levTiles.append(Tile(tileMap[" "]))
                    self.players[1].x, self.players[1].y = x, y
                if unit == "o":
                    levTiles.append(Tile(tileMap[" "]))
                    levTiles[-1].obj = Rock()
                x += 1
            y += 1
            self.array.append(levTiles)

    def tick(self):
        for player in self.players:
            player.tick(self)
    def blit(self, surf):
        surf.blit(images["bg.png"], (0, 0))
        ys = 240 - (32 * self.ydim) / 2
        xs = 320 - (32 * self.xdim) / 2
        y = ys
        for row in self.array:
            x = xs
            for cell in row:
                subrect = Rect(cell.fr[0] * 32, cell.fr[1] * 32, 32, 32)
                surf.blit(images[cell.sprite], (x, y), subrect)
                x += 32
            y += 32

        # Objects over tiles
        y = ys
        for row in self.array:
            x = xs
            for cell in row:
                if cell.obj:
                    dx = cell.obj.dx
                    dy = cell.obj.dy
                    surf.blit(images[cell.obj.sprite], (x + dx, y + dy))
                x += 32
            y += 32

        for player in self.players:
            subrect = Rect(0, 0, 32, 32)
            if player.uid == 1:
                subrect.move_ip(96, 0)
            subrect.move_ip(32 * player.frame, 0)
            subrect.move_ip(0, 32 * player.dir)
            surf.blit(images["character.png"], (player.x * 32 + player.dx + xs, player.y * 32 + player.dy + ys), subrect)

#----------------------------------------------------------------------------------------------------------------------------------
class Player(object):

#set up co-ordinate types and other variables
    def __init__(self, uid, x, y):
        self.uid = uid
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.gox = x
        self.goy = y
        self.goint = 0
        self.dir = 0
        self.controls = P_CONTROLS[self.uid] # load up array of control buttons this is to change to motion sensor stuff
        self.frame = 1
        self.mov = False
    def tick(self, level):

        pygame.event.pump()
        keystate = pygame.key.get_pressed()

        tmove = abs(self.x-self.gox) + abs(self.y-self.goy)

        if tmove == 0:
            for key in self.controls:
                if keystate[self.controls[key]]:
                    if key == "up":
                        self.dir = 3
                        if level.array[self.y - 1][self.x].bits & 1 == 0:
                            if not (level.array[self.y - 2][self.x].bits & 1 and level.array[self.y - 1][self.x].obj):
                                if not (level.array[self.y - 2][self.x].obj and level.array[self.y - 1][self.x].obj):
                                    if not (level.players[not self.uid].y == self.y - 2 and level.players[not self.uid].x == self.x and level.array[self.y - 1][self.x].obj):
                                        self.goy -= 1
                    elif key == "down":
                        self.dir= 0
                        if level.array[self.y + 1][self.x].bits & 1 == 0:
                            if not (level.array[self.y + 2][self.x].bits & 1 and level.array[self.y + 1][self.x].obj):
                                if not (level.array[self.y + 2][self.x].obj and level.array[self.y + 1][self.x].obj):
                                    if not (level.players[not self.uid].y == self.y + 2 and level.players[not self.uid].x == self.x and level.array[self.y + 1][self.x].obj):
                                        self.goy += 1
                    elif key == "left":
                        self.dir = 1
                        if level.array[self.y][self.x - 1].bits & 1 == 0:
                            if not (level.array[self.y][self.x - 2].bits & 1 and level.array[self.y][self.x - 1].obj):
                                if not (level.array[self.y][self.x - 2].obj and level.array[self.y][self.x - 1].obj):
                                    if not (level.players[not self.uid].y == self.y and level.players[not self.uid].x == self.x - 2 and level.array[self.y][self.x - 1].obj):
                                        self.gox -= 1
                    elif key == "right":
                        self.dir = 2
                        if level.array[self.y][self.x + 1].bits & 1 == 0:
                            if not (level.array[self.y][self.x + 2].bits & 1 and level.array[self.y][self.x + 1].obj):
                                if not (level.array[self.y][self.x + 2].obj and level.array[self.y][self.x + 1].obj):
                                    if not (level.players[not self.uid].y == self.y and level.players[not self.uid].x == self.x + 2 and level.array[self.y][self.x + 1].obj):
                                        self.gox += 1
                    break

        tmove = abs(self.x-self.gox) + abs(self.y-self.goy)

        if tmove > 1:
            self.gox = self.x
            self.goy = self.y
        elif tmove == 1:
            self.frame = abs((((int(self.goint / 5.0) + 1) % 4) - 1))
            tdx = (self.gox - self.x)
            tdy = (self.goy - self.y)
            self.dx = tdx * 32 * (self.goint / 19.0)
            self.dy = tdy * 32 * (self.goint / 19.0)
            self.goint += 1
            if self.goint == 20:
                self.mov = False
                self.goint = 0
                if level.array[self.goy][self.gox].sprite == "wallsm.png":
                    level.array[self.goy][self.gox].sprite = "wall.png"
                    level.array[self.goy][self.gox].bits |= 1
                if level.array[self.goy][self.gox].obj:
                    level.array[self.goy][self.gox].obj.dx = 0
                    level.array[self.goy][self.gox].obj.dy = 0
                    level.array[self.goy+tdy][self.gox+tdx].obj = level.array[self.goy][self.gox].obj
                    level.array[self.goy][self.gox].obj = None
                self.x = self.gox
                self.y = self.goy
                self.dx = 0
                self.dy = 0
                self.tmove = 0


            else:
                if level.array[self.goy][self.gox].obj:
                    if not self.mov:
                        self.mov = True
                        PUSHSOUND.play()
                    level.array[self.goy][self.gox].obj.dx = self.dx
                    level.array[self.goy][self.gox].obj.dy = self.dy
        else:
            self.frame = 1

        gotTreasure = False

        if self.dir == 0 and level.array[self.y + 1][self.x].bits & 4:
            level.array[self.y + 1][self.x].fr = (1, 0)
            level.array[self.y + 1][self.x].bits ^= 4
            gotTreasure = True
        if self.dir == 1 and level.array[self.y][self.x - 1].bits & 4:
            level.array[self.y][self.x - 1].fr = (1, 0)
            level.array[self.y][self.x - 1].bits ^= 4
            gotTreasure = True
        if self.dir == 2 and level.array[self.y][self.x + 1].bits & 4:
            level.array[self.y][self.x + 1].fr = (1, 0)
            level.array[self.y][self.x + 1].bits ^= 4
            gotTreasure = True
        if self.dir == 3 and level.array[self.y - 1][self.x].bits & 4:
            level.array[self.y - 1][self.x].fr = (1, 0)
            level.array[self.y - 1][self.x].bits ^= 4
            gotTreasure = True

        if gotTreasure:
            TREASURESOUND.play()
            level.chests -= 1
#----------------------------------------------------------------------------------------------------------------------------------
class Tile(object):
    def __init__(self, sprite):
        global TILE_WALLS, TILE_PUSH, TILE_TREASURE
        if type(sprite) == list: sprite = random.choice(sprite)
        self.sprite = sprite + ".png"
        self.bits = 0
        if sprite in TILE_WALLS: self.bits |= 1
        if sprite in TILE_PUSH: self.bits |= 2
        if sprite in TILE_TREASURE: self.bits |= 4
        self.fr = (0, 0)
        self.obj = None
#----------------------------------------------------------------------------------------------------------------------------------
class Rock(object):
    def __init__(self):
        self.sprite = "rock.png"
        self.dx = 0
        self.dy = 0
#----------------------------------------------------------------------------------------------------------------------------------


#-----------------------------Define main parameters of the system------------------------------------------------------------
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)
screen = pygame.display.set_mode((640, 480))#, FULLSCREEN)
#screen = pygame.display.set_mode((640, 480), FULLSCREEN)
pygame.mouse.set_visible(0)
# define sounds ingame
PUSHSOUND = pygame.mixer.Sound("push.wav")
TREASURESOUND = pygame.mixer.Sound("Treasure.ogg")
WINSOUND = pygame.mixer.Sound("Orb.ogg")

images = {}
for im in imagesToLoad:
    images[im] = pygame.image.load(im).convert_alpha()

pygame.display.set_caption("Escape from Cera")

bkg = pygame.image.load('bg.png')
screen.blit(bkg, (0, 0))
pygame.display.flip()
#-----------------levels-------
levels = os.listdir("Levels")
levels.sort()
i = len(levels)
L = 0
#------------------------menu-----------------------------------------------
menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
               [('Start Game',5, None),
                ('Load Level',1, None),
                ('Instructions',2, None),
                ('Exit',4, None)])
				
menu1 = cMenu(50, 50, 20, 5, 'vertical', 4, screen,
                [('Previous Menu', 0, None),
                 ('Choose level',3, None),
                 ('Exit',4, None)])		
levelMenu = []

levelMenu.append(('Previous Menu', 0, None)	)

for j in range(0, i):
	p = j+6
	levelMenu.append(('Level%d '%j,p, None))
		
levelMenu.append(('Exit',4, None))
menu2 = cMenu(50, 50, 20, 5, 'vertical', 4, screen, levelMenu)	

menu3 = cMenu(50, 50, 20, 5, 'vertical', 4, screen,
                [('Previous Menu', 0, None),
                 ('Exit',4, None)])			
				 
#----------------------set the positions of menus on screen----------------------------------------
menu.set_center(True, True)
menu.set_alignment('center', 'center')
menu1.set_center(True, True)
menu1.set_alignment('center', 'center')
menu2.set_center(True, True)
menu2.set_alignment('center', 'center')
menu3.set_center(True, True)
menu3.set_alignment('center', 'center')
state = 0
prev_state = 1
rect_list = []

# Ignore mouse motion (greatly reduces resources when not needed)
pygame.event.set_blocked(pygame.MOUSEMOTION)

while 1:
  # Check if the states changed
  # the queue to force the menu to be shown at least once
	if prev_state != state:
		pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
		prev_state = state

		if state in [0,1,2,3]:
			# Reset the screen before going to the next menu,  caption at the bottom 
			screen.blit(bkg, (0, 0))
			screen.blit(TEXT[state][0], (15, 430))
			screen.blit(TEXT[state][1], (15, 410))
			screen.blit(TEXT[state][2], (15, 390))
			screen.blit(TEXT[state][2], (15, 390))
			pygame.display.flip()
	# Get the next event
	e = pygame.event.wait()

	if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
		if state == 0:
			rect_list, state = menu.update(e, state)
		elif state == 1:
			rect_list, state = menu1.update(e, state)
		elif state == 5:
	#--------------------------------start game-----------------------------------------------------------------------------
			print 'Start Game!'
			levels = os.listdir("Levels")
			levels.sort()
			levels = levels[L:]

			for level in levels:
			    curLev = Level(level)
			    inLev = True
			    while inLev:
			        curLev.tick()
			        curLev.blit(screen)
					# check if chests in current level are still active if not progress, add here some sort of differenciation for the two players i think
			        if curLev.players[0].x == curLev.players[1].x and curLev.players[0].y == curLev.players[1].y and curLev.chests == 0:
			            inLev = False
			            for player in curLev.players:
			                player.dx = 0; player.dy = 0; player.goint = 0; player.dir = 0
			        pygame.display.flip()
			        pygame.event.pump()
			        time.sleep(0.01)
			        for ev in pygame.event.get():
			            if ev.type == QUIT:
			                pygame.quit()
			                sys.exit(0)
			            if ev.type == KEYDOWN:
			                if ev.key == K_r:
			                    curLev = Level(level)
			                if ev.key == K_ESCAPE:
			                    pygame.quit()
			                    sys.exit(0)
	    # Level complete
			WINSOUND.play()
	#----------------------------------end of start game----------------------------------------------------------------------	
		elif state == 2:
			rect_list, state = menu3.update(e, state)
		elif state == 3:
			rect_list, state = menu2.update(e, state)
		elif state == 4 :
			print 'Exit!'
			pygame.quit()
			sys.exit()
	#-----------------------------------------player level choice-----------------------------------------------------------------	
		else:	
			for j in range(i):
				p = j+6
				if state == p:
					L = j
					state = 5


  # Quit if the user presses the exit button
	if e.type == pygame.QUIT:
		pygame.quit()
		sys.exit()

  # Update the screen
	pygame.display.update(rect_list)

#-----------------------------------------------------------------------