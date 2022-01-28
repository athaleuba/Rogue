#rogue
#hello

from random import randint
from random import choice
from itertools import product

count_gold = 0



# for salle in salles:

#     corner, width, height = salle['corner'], salle['width'], salle['height']
#     xc, yc = corner
#     coor_walls = []
#     for i in range(width):
#         coor_walls.append((xc + i, yc))
#     for j in range(height):
#         coor_walls.append((xc, yc + j))

coord_rooms = [product([salle['corner'][0] + k for k in range(1, salle['width'])], [salle['corner'][1] + l for l in range(1, salle['height'])]) for salle in salles]
coords_vrac = []
for room in coord_rooms:
    coords_vrac += room
paths = []
doors = []
for salle in salles:
        (xp, yp), (dxp, dyp), length = salle['path']
        path = [(xp + k*dxp, yp + k*dyp) for k in range(length)]
        paths += path
        doors.append(salle['doors'])

empty_cases = coords_vrac + paths
gold = choice(empty_cases)
paywall = 5

def move_player(player, direction):
    x, y = player
    dx, dy = direction
    if (x+dx, y+dy) in coords_vrac:
        if (x+dx, y+dy) == gold:
            count_gold += 1

            # if new_player in guards:
            #     if count_gold >= paywall:
            #         count_gold -= paywall
            #         new_player = x + dx, y + dy
            #     else:
            #         new_player = player
            new_player = x+dx, y+dy
            gold = []

    elif (x+dx, y+dy) in paths:
        new_player = x+dx, y+dy

    elif (x+dx, y+dy) in doors:
        new_player = x+dx, y+dy

    else: 
        new_player = player

    player = new_player