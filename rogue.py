# Python Standard Library
from random import randint
from random import choice
import numpy as np
# Third-Party Libraries
import pygame as pg
from itertools import product

# Constants
# ------------------------------------------------------------------------------

X,Y = 30, 40 #taille de la fenêtre de jeu
W,H = 15,15 #taille de nos carrés élémentaires de jeu
DIRECTIONS = {
    "DOWN": (0, +1),
    "UP": (0, -1),
    "RIGHT": (+1, 0),
    "LEFT": (-1, 0),
}
FLOOR = (240, 240, 250)
WALL = (139,69,19)
PATH = (210,180,140)
count_gold = 0
rouge = ( 255, 0,0)
blue = (0, 0, 128)

# Game state
# ------------------------------------------------------------------------------
player = (2,2)

# Helper functions
# ------------------------------------------------------------------------------

def quit(snake, reason):
    print(f"Game over ({reason}) with a score of {len(snake)}")
    pg.quit()
    exit()

def draw_path(départ,arrivée):
    if départ[0]==arrivée[0]:

        t=min(départ[1],arrivée[1])
        for k in range (abs(départ[1]-arrivée[1])):
            draw_tile(départ[0],t+k,PATH)

    if départ[1]==arrivée[1]:
        
        t=min(départ[0],arrivée[0])
        for k in range (abs(départ[0]-arrivée[0])):
            draw_tile(t+k,départ[1],PATH)

def draw_tile(x, y, color):
    """
    x and y in tiles coordinates
    translate into pixel coordinates for painting
    """
    rect = pg.Rect(x * W, y * H, W, H)
    pg.draw.rect(screen, color, rect)

walls = [
    ((1,1),8,8),((1,11),8,8),((1,21),8,8),
    ((11,1),8,8),((11,11),8,8),((11,21),8,8),
    ((21,1),8,8),((21,11),8,8),((21,21),8,8),
] #liste de tuple (coins HG,horizontal,vertical) les longueurs sont en unités de W*H

nombre_salles = 9
salles = []


for k in range(nombre_salles):
    d = dict()
    wall = walls[k]
    d['corner'] = wall[0]
    d['size'] = (wall[1],wall[2]) # horizontal, vertical
    corner = d['corner']
    size = d['size']
    d['doors'] = [(corner[0]+int(size[0]/2),corner[1]+size[1]-1),
                    (corner[0]+int(size[0]/2),corner[1]),
                    (corner[0],corner[1]+int(size[1]/2)),
                    (corner[0]+size[0]-1,corner[1]+int(size[1]/2))
                    ] # liste de tuples des positions des portes
    #if k >=1:
        #dict['neighbors'] = [salles[k-1]]
    salles.append(d)

DOORS = []
PATHS = []

for salle in salles:
    doors = salle['doors']
        
    for door in doors:
        DOORS.append(door)

            

    for (door_1,door_2) in product(DOORS,DOORS):
        x1,y1,x2,y2 = door_1[0],door_1[1],door_2[0],door_2[1]
        if (x1==x2 and abs(y2-y1)==3):
            PATHS.append(((x1,y1),(0,1),3))
            PATHS.append(((x1,y1),(0,-1),3))
        elif (y1==y2 and abs(x2-x1)==3):
            PATHS.append(((x1,y1),(1,0),3))
            PATHS.append(((x1,y1),(-1,0),3))

Case_path = []

for path in PATHS:
    (xp,yp), (dxp,dyp), lenght = path
    for k in range(lenght):
        Case_path.append((xp+dxp*k,yp+dyp*k)) 

def draw_background():
    screen.fill(FLOOR)

    for wall in walls:
        corner,largeur,longueur = wall[0],wall[1]-1,wall[2]-1
        for x in range(largeur+1):
            draw_tile(corner[0]+x,corner[1],WALL)
            draw_tile(corner[0]+x,corner[1]+longueur,WALL)

        for y in range(longueur):
            draw_tile(corner[0],corner[1]+y,WALL)
            draw_tile(corner[0]+largeur,corner[1]+y,WALL)
    
    
    for salle in salles:
        
        doors = salle['doors']
        
        for door in doors:
            if (door[0]>2 and door[0]<28 and door[1]>2 and door[1]<28):
                draw_tile(door[0],door[1],PATH)
        

    for (door_1,door_2) in product(DOORS,DOORS):
        x1,y1,x2,y2 = door_1[0],door_1[1],door_2[0],door_2[1]
        if (x1==x2 and abs(y2-y1)==3):
            draw_path(door_1,door_2)
            
        elif (y1==y2 and abs(x2-x1)==3):
            draw_path(door_1,door_2)

    for i in range(X):
        draw_tile(i,30,(0,0,0))
        
coord_rooms = [product([salle['corner'][0] + k for k in range(1, salle['size'][0]-1)], [salle['corner'][1] + l for l in range(1, salle['size'][1]-1)]) for salle in salles]
coords_vrac = []
for room in coord_rooms:
    coords_vrac += room

empty_cases = coords_vrac + PATHS
gold = choice(empty_cases)
print(gold)
paywall = 5

def move_player(player, direction):
    x, y = player
    dx, dy = direction
    if (x+dx, y+dy) in coords_vrac:
        '''if (x+dx, y+dy) == gold:
            count_gold += 1

            # if new_player in guards:
            #     if count_gold >= paywall:
            #         count_gold -= paywall
            #         new_player = x + dx, y + dy
            #     else:
            #         new_player = player'''
        new_player = x+dx, y+dy
            #gold = []

    elif (x+dx, y+dy) in Case_path:
        new_player = x+dx, y+dy

    elif (x+dx, y+dy) in DOORS:
        new_player = x+dx, y+dy

    else:
        return(player)

    return(new_player)
    



# Game init and main loop
# ------------------------------------------------------------------------------
running = True
pg.init()
screen = pg.display.set_mode((X * W, Y * H))
clock = pg.time.Clock()
pg.display.set_caption('Show Text')
font = pg.font.Font('freesansbold.ttf', 24)
life = font.render('life = ', True, rouge, FLOOR)
money = font.render('money = ', True, blue, FLOOR)
lifeRect = life.get_rect()
lifeRect.center = (2.5*X, 12.2*Y)
moneyRect = money.get_rect()
moneyRect.center = (2.5*X, 12.9*Y)

pg.display.set_caption('Image')
image = pg.image.load(r'images/Couronne.png')
while running:
    direction = (0,0)
    clock.tick(14)
    for event in pg.event.get():
            #print(f"{event=}")
            # chaque évênement à un type qui décrit la nature de l'évênement
            # un type de pg.QUIT signifie que l'on a cliqué sur la "croix" de la fenêtre
            if event.type == pg.QUIT:
                running = False
            # un type de pg.KEYDOWN signifie que l'on a appuyé une touche du clavier
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    direction = DIRECTIONS["DOWN"]
                elif event.key == pg.K_UP:
                    direction = DIRECTIONS["UP"]
                elif event.key == pg.K_RIGHT:
                    direction = DIRECTIONS["RIGHT"]
                elif event.key == pg.K_LEFT:
                    direction = DIRECTIONS["LEFT"]
                # si la touche est "Q" on veut quitter le programme
                elif event.key == pg.K_q:
                    running = False

    
    
    
    
    player = move_player(player, direction)
    draw_background()
    screen.blit(image, (380, 380))
    screen.blit(life, lifeRect)
    screen.blit(money, moneyRect)
    draw_tile(player[0],player[1],(255,0,0))
    pg.display.update()

pg.quit()
