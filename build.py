import requests
import json
from api_key import API_KEY
import time

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
steps_to_start = []

unexplored = {}
visited = {}

# Set up inverse relationship with directions
inverse_directions = { "n": "s", "e": "w", "w": "e", "s": "n" }

# Working on ALGO

def start():
    starting_room = init()
    room_id = starting_room["room_id"]
    directions = starting_room["exits"]
    print(f"Directions: {directions}")
    cooldown_print(starting_room["cooldown"])
    new_room = move({"direction": directions[0]})
    cooldown_print(new_room["cooldown"])

start()