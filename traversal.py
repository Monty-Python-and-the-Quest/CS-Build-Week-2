import requests
import time
import random
import json

from util import Queue


#TODO api_key = ""

#Endpoint Url
url = "https://lambda-treasure-hunt.herokuapp.com/api"

headers = {
    "Authorization": api_key 
}




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Player Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Initialization
def player_initilization():
    response = requests.get(f'{url}/adv/init/', headers=headers)
    data = response.json()
    print("This is th INIT response--->", data)
    return data

#Player Status
def player_status():
    response = requests.post(f'{url}/adv/status/', headers=headers)
    data = response.json()
    print("This is the STATUS response--->", data)
    return data
    
#Player Movement
def player_move(payload):
    response = requests.post(f'{url}/adv/move/', data = json.dumps(payload), headers=headers)
    data = response.json()
   
    print("This is the STATUS response--->", data)
    return data



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Pseudocode~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# player_init = initilization()
# player_room_id = player_init[room_id]

#Test Functions
#player_initilization()

#player_status()

player_move({'direction' : 's'})



"""
#traversal_path = ["n", room_id]
traversal_path = []

#Graph dictionary of world map
map_graph = {}

def player_travel_direction(direction):
    return #direction traveled TODO

#Create a dictionary of each room visited
def current_room_vertex():
    room = {}
    exits = #TODO pull from data possible direction
    for exit in exits:
        room[exit] = "unexplored"
        map_graph[player.current_room.id] = room#room ID TODO]
        #Tie in coordinates to map graph dict TODO

#Logic to find unexplored exit
def current_room_unexplored_exits():
    #Track unexplored exits
    unexplored = []
    #Finds the available exits from the current room and check if they are unexplored
    for exit in player.current_room.id: #TODO
        if map_graph[player.current_room.id][exit] == "unexplored":
            unexplored.append(exit)
    
    #random choice exit to traverse
    return random.choice(unexplored)

"""

