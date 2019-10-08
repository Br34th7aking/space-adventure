# Escape - A Python Space Adventure
# Abhijit Raj
# Original Author: Sean McManus

import time, random, math

##############################
##        variables         ##
##############################
WIDTH = 800
HEIGHT = 600

# Player variables 
PLAYER_NAME = 'Abhijit'
FRIEND1_NAME = 'Siddhant'
FRIEND2_NAME = 'Neha'

current_room = 31 # starting room = 31

top_left_x = 100
top_left_y = 150

DEMO_OBJECTS = [images.floor, images.pillar, images.soil]

##############################
##          MAP             ##
##############################
MAP_WIDTH = 5
MAP_HEIGHT = 10
MAP_SIZE = MAP_WIDTH * MAP_HEIGHT

GAME_MAP = [ ["Room 0 - where unused objects are kept", 0, 0, False, False] ]

outdoor_rooms = range(1, 26)
for planetsectors in range(1, 26):
    GAME_MAP.append(["The dusty planet surface", 13, 13, True, True])

# add the other rooms 
GAME_MAP += [
        #["Room description", height, width, exit top?, exit right?]
        ["The airlock", 13, 5, True, False],
        ["The engineering lab", 13, 13, False, False],
        ["Poodle Mission Control", 9, 13, False, True],
        ["The viewing gallery", 9, 15, False, False],
        ["The crew's bathroom", 5, 5, False, False],
        ["The airlock entry bay", 7, 11, True, True],
        ["Left Elbow room", 9, 7, True, False],
        ["Right Elbow room", 7, 13, True, True],
        ["The science lab", 13, 13, False, True],
        ["The greenhouse", 13, 13, True, False],
        [PLAYER_NAME + "'s sleeping quarters", 9, 11, False, False],
        ["West Corridor", 15, 5, True, True],
        ["The briefing room", 7, 13, False, True],
        ["The crew's community room", 11, 13, True, False],
        ["Main Mission Control", 14, 14, False, False],
        ["The sick bay", 12, 7, True, False],
        ["West Corridor", 9, 7, True, False],
        ["Utilities Control room", 9, 9, False, True],
        ["System engineering bay", 9, 11, False, False],
        ["Security portal to Mission Control", 7, 7, True, False],
        [FRIEND1_NAME + "'s sleeping quarters", 9, 11, True, True],
        [FRIEND2_NAME + "'s sleeping quarters", 9, 11, True, True],
        ["The pipeworks", 13, 11, True, False],
        ["The chief scientist's office", 9, 7, True, True],
        ["The robot workshop", 9, 11, True, False]
    ]

# simple sanity check on map above to check data entry 
assert len(GAME_MAP) - 1 == MAP_SIZE, "Map size and GAME_MAP don't match"

##############################
##        make map          ##
##############################

def get_floor_type():
    if current_room in outdoor_rooms:
        return 2 # soil 
    else:
        return 0 # floor


def generate_map():
# this function makes the map for the current room, 
# using room data, scenery data and prop data 
    global room_map, room_width, room_height, room_name, hazard_map
    global top_left_x, top_left_y, wall_transparency_frame

    room_data = GAME_MAP[current_room]
    room_name = room_data[0]
    room_height = room_data[1]
    room_width = room_data[2]

    floor_type = get_floor_type()
    if current_room in range(1, 21):
        bottom_edge = 2 # soil 
        side_edge = 2 # soil 
    if current_room in range(21, 26):
        bottom_edge = 1 # wall
        side_edge = 2 # soil 
    if current_room > 25:
        bottom_edge = 1 # wall 
        side_edge = 1 # wall 

    # Create top line of the room map. 
    room_map = [[side_edge] * room_width]
    # Add middle lines of the room map (wall, floor to fill width, wall)
    for y in range(room_height - 2):
        room_map.append([side_edge] + [floor_type] * (room_width - 2) + [side_edge])
    # add the bottom line of the room map
    room_map.append([bottom_edge] * room_width)

    # add doorways 
    middle_row = int(room_height / 2)
    middle_column = int(room_width / 2)

    if room_data[4]: # if exit at right of this room 
        room_map[middle_row][room_width - 1] = floor_type
        room_map[middle_row + 1][room_width - 1] = floor_type
        room_map[middle_row - 1][room_width - 1] = floor_type

    if current_room % MAP_WIDTH != 1: # If room is not on the left of the map
        room_to_left = GAME_MAP[current_room - 1]
        # If room_to_left has a right exit, add left exit in this room 
        if room_to_left[4]:
            room_map[middle_row][0] = floor_type
            room_map[middle_row + 1][0] = floor_type
            room_map[middle_row - 1][0] = floor_type

    if room_data[3]: # if exit at top of this room 
        room_map[0][middle_column] = floor_type
        room_map[0][middle_column + 1] = floor_type
        room_map[0][middle_column - 1] = floor_type

    if current_room <= MAP_SIZE - MAP_WIDTH: # If room is not on the bottom of the map
        room_below = GAME_MAP[current_room + MAP_WIDTH]
        # If room_below has a top exit, add exit at the bottom of this one
        if room_below[3]:
            room_map[room_height - 1][middle_column] = floor_type
            room_map[room_height - 1][middle_column + 1] = floor_type
            room_map[room_height - 1][middle_column - 1] = floor_type


##############################
##        explorer          ##
##############################
def draw():
    global room_height, room_width, room_map
    generate_map()
    screen.clear()

    for y in range(room_height):
        for x in range(room_width):
            image_to_draw = DEMO_OBJECTS[room_map[y][x]]
            screen.blit(image_to_draw, (top_left_x + (x * 30), top_left_y + (y * 30) - image_to_draw.get_height()))

def movement():
    global current_room
    old_room  = current_room

    if keyboard.left:
        current_room -= 1
    if keyboard.right:
        current_room += 1
    if keyboard.up:
        current_room -= MAP_WIDTH
    if keyboard.down:
        current_room += MAP_WIDTH

    if current_room > 50:
        current_room = 50
    if current_room < 1:
        current_room = 1

    if current_room != old_room:
        print(f'Entering room: {current_room}')

clock.schedule_interval(movement, 0.1)
