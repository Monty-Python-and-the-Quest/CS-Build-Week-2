import requests
import json
from api_key import API_KEY
import time
import ast
from player import Player

# For O(1) time complexity for append and pop operations
from collections import deque

# Player path
traversal_path = []
room_id = []
room_cd = 0
new_id = []
new_cd = []
direction = {
    "direction": ""
}
inverse_direction = {
    "direction": ""
}
# Inverse player path
inverse_path = []
# Exits are here
unexplored_exits = []
current_room = []
need_to_explore = []
visited = set()
go_back_direction = {
    "direction": ""
}

# Set up inverse relationship with directions
inverse_directions = { "n": "s", "e": "w", "w": "e", "s": "n" }


# URL
url = "https://lambda-treasure-hunt.herokuapp.com/api"

# Header
headers = {
    "Authorization": API_KEY
}

# # Player
player = Player("User 20600", 2)




# INIT FUNCTION
def init():
    r = requests.get(f'{url}/adv/init/', headers=headers)
    data = r.json()
    print('Init:', data)
    return data

# STATUS FUNCTION
def status():
    r = requests.post(f'{url}/adv/status', headers=headers)
    data = r.json()
    print(data["cooldown"])
    return data

# Needs to input the true direction in function
def remove_inverse_direction_from_exits(move_direction):
    if inverse_directions[move_direction] in unexplored_exits:
        unexplored_exits.remove(inverse_directions[move_direction])


# MOVE FUNCTION
def move(payload):
    r_move = requests.post(f'{url}/adv/move', data=json.dumps(payload), headers=headers)
    data = r_move.json()
    cooldown = data["cooldown"]
    room_id = data["room_id"]
    # print('Traversal Path:', traversal_path)
    # print('Inverse path:', inverse_path)
    print('Visited:', visited)
    print('Need to explore:', need_to_explore)
    print('Moved:', payload)
    print('Moved data:', data)
    # print('Cooldown:', cooldown)

    #  Change center room
    if (len(unexplored_exits) == 0) and (room_id not in visited) and (room_id in need_to_explore):
        print('NEW ROOM CENTER 0 NOT IN VISITED (NEED TO EXPLORE):', room_id)
        info = []
        info.append(data)
        need_to_explore.remove(room_id)
        cooldown_print(cooldown)
        setup_current_room()

        # when we move, need to print to map.txt
        with open('map.txt', 'a+') as outfile:
            json.dump        (info, outfile, indent=2)


        remove_inverse_direction_from_exits(direction["direction"])
        step_forward()

    elif (len(unexplored_exits) == 0) and (room_id not in visited):
        print('NEW ROOM CENTER (NOT IN VISITED):', room_id)
        info = []
        info.append(data)
        need_to_explore.append(room_id)
        cooldown_print(cooldown)
        setup_current_room()

        # when we move, need to print to map.txt
        with open('map.txt', 'a+') as outfile:
            json.dump        (info, outfile, indent=2)

            if len(unexplored_exits) == 1:
                move(inverse_direction)
            else:
                remove_inverse_direction_from_exits(direction["direction"])
                step_forward()

    elif (len(unexplored_exits) == 0) and (room_id in visited) and (room_id in need_to_explore):
        print('GO BACK:', room_id)
        info = []
        info.append(data)
        cooldown_print(cooldown)
        setup_current_room()

        # when we move, need to print to map.txt
        with open('map.txt', 'a+') as outfile:
            json.dump        (info, outfile, indent=2)

        remove_inverse_direction_from_exits(direction["direction"])
        step_forward()

    elif (len(unexplored_exits) == 0) and (room_id in visited):
        print('GO BACKWARDS:', room_id)
        info = []
        info.append(data)
        cooldown_print(cooldown)
        setup_current_room()

        # when we move, need to print to map.txt
        with open('map.txt', 'a+') as outfile:
            json.dump        (info, outfile, indent=2)

        remove_inverse_direction_from_exits(direction["direction"])
        # Change move direction to unexplored_exits(0)
        move_direction = unexplored_exits.pop(0)
        direction["direction"] = move_direction
        move(direction)
        step_forward()



    elif (len(unexplored_exits) > 0) and (room_id in visited) and (room_id in need_to_explore):
        print('NEW ROOM CENTER IN VISITED (NEED TO EXPLORE):', room_id)
        info = []
        info.append(data)
        cooldown_print(cooldown)
        setup_current_room()

        # when we move, need to print to map.txt
        with open('map.txt', 'a+') as outfile:
            json.dump        (info, outfile, indent=2)

        remove_inverse_direction_from_exits(direction["direction"])
        step_forward()

    elif (len(unexplored_exits) > 0) and (room_id not in visited) and (room_id in need_to_explore):
        print('NEW ROOM CENTER NOT IN VISITED (NEED TO EXPLORE):', room_id)
        need_to_explore.remove(room_id)
        info = []
        info.append(data)
        cooldown_print(cooldown)
        setup_current_room()

        # when we move, need to print to map.txt
        with open('map.txt', 'a+') as outfile:
            json.dump        (info, outfile, indent=2)

        remove_inverse_direction_from_exits(direction["direction"])
        step_forward()

    # If room_id is in visted and need_to_explore
    elif (len(unexplored_exits) >= 0) and (room_id in visited) and (room_id in need_to_explore):
        print('ROOM IN VISTED AND NEED TO EXPLORE CENTER:', room_id)
        need_to_explore.remove(room_id)
        cooldown_print(cooldown)

        # move_direction = unexplored_exits.pop(0)
        # direction["direction"] = move_direction
        # move(direction)
        # step_forward()

        setup_current_room()

        # when we move, need to print to map.txt
        with open('map.txt', 'a+') as outfile:
            json.dump        (info, outfile, indent=2)

        remove_inverse_direction_from_exits(direction["direction"])
        step_forward()

    elif room_id not in visited and (len(unexplored_exits) > 0):
        print('Adding room:', room_id, ' to map')
        info = []
        info.append(data)
        need_to_explore.append(room_id)

        # when we move, need to print to map.txt
        with open('map.txt', 'a+') as outfile:
            json.dump        (info, outfile, indent=2)

        cooldown_print(cooldown)
        step_back()

    else:
        cooldown_print(cooldown)
        step_forward()



# COOLDOWN PRINTS
def cooldown_print(seconds):
    # seconds = seconds + 10
    print('Must wait', seconds, ' seconds!')
    while seconds > 0:
        time.sleep(1)
        seconds = seconds - 1
    if seconds == 0:
        print('Done waiting')


def take_treasure(self):
    if len(player.room['items']) > 0:
        player.status()
        time.sleep(player.cooldown)
        # cooldown_print(player.cooldown)
        if len(player.p_status['inventory']) < player.p_status['strength']:
            player.take()
            time.sleep(player.cooldown)
        else:
            print('Inventory is full')

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


# Working on ALGO

def setup_current_room():
    current_room = init()
    current_room_id = current_room["room_id"]
    current_room_exits = current_room["exits"]
    current_room_cd = current_room["cooldown"]

    # Add current room to visited
    visited.add(current_room_id)
    print(f"Visited: {visited}")

    for exit in current_room_exits:
        unexplored_exits.append(exit)
    print(f"Room Exits: {current_room_exits}")

    if len(room_id) == 1:
        room_id.pop(0)
        room_id.append(current_room_id)
    else:
        room_id.append(current_room_id)
    print(f"Room id: {room_id}")

    room_cd = int(round(current_room_cd))

    # print(f"Current room cd: {current_room_cd}")
    #
    # print(f"Room cd: {room_cd}")

    # Prints cool down
    cooldown_print(current_room_cd)

def step_forward():
    # Get the first available direction
    move_direction = unexplored_exits.pop(0)
    # Once we go through all exits, go back to first exit
    inverse_direction["direction"] = inverse_directions[move_direction]
    direction["direction"] = move_direction

    # print(f"Direction: {move_direction}")
    # print(f"Inverse direction: {inverse_direction}")

    if len(unexplored_exits) == 0:
        print(f"Unexplored Exits: {unexplored_exits}")
        # Remove the inverse direction since we don't need to go back
        # inverse_path.remove(inverse_directions[move_direction])
        move(direction)

    else:
        print(f"Unexplored Exits: {unexplored_exits}")

        # Prints cool down
        cooldown_print(room_cd)

        # Add the direction to traversal path
        traversal_path.append(move_direction)

        # Add the inverse direction so we can retrace our path
        inverse_path.append(inverse_directions[move_direction])

        # Travel there (NEED TO FIX FORMAT ITS BEING SENT--- MAIN PROBLEM)
        move(direction)

        # # Reinit new room to explore
        # if room_id in need_to_explore:
        #     unexplored_exits.remove(inverse_directions[move_direction])
        #     setup_current_room()
        #     step_forward()

        # # Prints cool down
        # cooldown_print(upcoming_room["cooldown"])


def step_back():
    if len(inverse_path) == 0:
        move_direction = inverse_directions[traversal_path.pop(-1)]
    # Go back one room and check again
    # move_direction = inverse_path.pop()
    # traversal_path.append(move_direction)
    else:
        move_direction = inverse_directions[traversal_path.pop(-1)]

    inverse_direction["direction"] = move_direction
    # print(f"Inverse Direction: {move_direction}")
    move(inverse_direction)

def algo():
    while len(visited) < 500:
        if len(unexplored_exits) > 0:
            take_treasure()
            step_forward()
        else:
            step_back()

# Uncomment to initialize and run algo
setup_current_room()
algo()

# Uncomment to move manually
# move(({"direction":"n"}))
# move(({"direction":"s", "next_room_id": "259"}))