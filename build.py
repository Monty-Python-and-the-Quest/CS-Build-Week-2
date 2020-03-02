import requests
import json
from api_key import API_KEY
import time

# For O(1) time complexity for append and pop operations
from collections import deque

# URL
url = "https://lambda-treasure-hunt.herokuapp.com/api"

# Header
headers = {
    "Authorization": API_KEY
}

# INIT FUNCTION
def init():
    r = requests.get(f'{url}/adv/init/', headers=headers)
    data = r.json()
    print(data)
    return data

# STATUS FUNCTION
def status():
    r = requests.post(f'{url}/adv/status', headers=headers)
    data = r.json()
    print(data["cooldown"])
    return data

# MOVE FUNCTION
def move(payload):
    r_move = requests.post(f'{url}/adv/move', data=json.dumps(payload), headers=headers)
    data = r_move.json()
    cooldown = data["cooldown"]
    
    info = []
    info.append(data)
    # when we move, need to print to map.txt
    with open('map.txt', 'a+') as outfile:
          json.dump(info, outfile, indent=2)

    print(data)
    return data

# COOLDOWN PRINTS
def cooldown_print(seconds):
    while seconds > 0:
        print('Must wait', seconds, ' seconds!')
        time.sleep(1)
        seconds = seconds - 1


# To run type - python build.py, uncomment each function to use

# init()

# Testing - moving
# move(({"direction":"w"}))

# Testing - if moving south from room 10 (back to room 0)
# move(({"direction":"s", "next_room_id": "0"}))

# Testing - if moving north from room 0 (initial room)
# move(({"direction":"n", "next_room_id": "10"}))

# status()

# cooldown_print()

# Player path
traversal_path = []

# Inverse player path
inverse_path = []
# Exits are here
unexplored = []
visited = set()

# Set up inverse relationship with directions
inverse_directions = { "n": "s", "e": "w", "w": "e", "s": "n" }

# Working on ALGO

# def start():
#     starting_room = init()
#     room_id = starting_room["room_id"]
#     directions = starting_room["exits"]
#     print(f"Directions: {directions}")
#     cooldown_print(starting_room["cooldown"])
#
#     if directions[0] == "w" and not visited:
#         enque()
#
#     new_room = move({"direction": directions[0]})
#     cooldown_print(new_room["cooldown"])

def setup_current_room():
    current_room = init()
    current_room_id = current_room["room_id"]
    current_room_exits = current_room["exits"]
    visited.add(current_room_id)
    print(f"Visited: , {visited}")
    for exit in current_room_exits:
        unexplored.append(exit)
    print(f"Room Exits: , {current_room_exits}")

    # Prints cool down
    cooldown_print(current_room["cooldown"])

def step_forward():
    # new_room = init()
    # print(f"New room: , {new_room}")
    # cooldown_print(new_room["cooldown"])
    # newer_room = init()
    # print(f"Newer room: , {newer_room}")
    # new_room_id = new_room['room_id']

    if len(unexplored) == 0:
        step_back()
    else:
        print(f"Unexplored: , {unexplored}")

        # Get the first available direction
        direction = unexplored.pop(0)

        print(f"Direction: , {direction}")

        # Add the inverse direction so we can retrace our path
        inverse_path.append(inverse_directions[direction])

        # Travel there (NEED TO FIX FORMAT ITS BEING SENT--- MAIN PROBLEM)
        move((f'{"direction":"{direction}"}'))

        # Reinit new room
        upcoming_room = init()
        print(f"Upcoming room: , {upcoming_room}")
        cooldown_print(upcoming_room["cooldown"])

        upcoming_room_id = upcoming_room["room_id"]

        if upcoming_room_id not in visited:
            # Add current room to visited
            setup_current_room()
            # Remove the inverse direction since we don't need to go back
            unexplored.remove(inverse_directions[direction])

        # Add the direction we traveled to traversal_path
        traversal_path.append(direction)

        # Prints cool down
        cooldown_print(upcoming_room["cooldown"])


def step_back():
    back_room = init()

    # Go back one room and check again
    direction = inverse_path.pop()
    traversal_path.append(direction)
    move({"direction": direction})

    # Prints cool down
    cooldown_print(back_room["cooldown"])


def algo():
    room = init()
    room_id = room["room_id"]

    while len(visited) < 5:
        if len(unexplored) > 0:
            step_forward()
        else:
            step_back()

setup_current_room()
algo()