import requests
import time
import random
import json

from util import Queue


#TODO api_key = ""

#Endpoint Url
url = "https://lambda-treasure-hunt.herokuapp.com/api"

headers = {
    "Authorization": "Token " #TODO
}




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Player Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Initialization
def player_initilization():
    time.sleep(6)
    response = requests.get(f'{url}/adv/init/', headers = headers)
    data = response.json()
    print("This is th INIT response--->", data)
    return data

#Player Status
def player_status():
    response = requests.post(f'{url}/adv/status/', headers = headers)
    data = response.json()
    print("This is the STATUS response--->", data)
    return data
    
#Player Movement TODO dynamic cooldown pulled off of init res
def player_move(payload):
    time.sleep(46)
    response = requests.post(f'{url}/adv/move/', data = json.dumps(payload), headers = headers)
    data = response.json()
    
    info = []
    info.append(data)
    # when we move need to print to map.txt
    with open('map.txt', 'a+') as outfile:
        json.dump(info, outfile, indent=2)
   
    print("This is the MOVE response--->", data)
    return data

#Item Looting
def loot_treasure(payload):
    response = requests.post(f'{url}/adv/take/', data= json.dumps(payload), headers = headers)
    data = response.json()
    print("This is the LOOT response--->", data)
    return data
    
    


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Traversal Algorithm WIP~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

traversal_path = []

#Graph dictionary of world map
map_graph = {}

#Gets room ID
def get_room_id():
    init = player_initilization()
    return init['room_id']


#Create a dictionary entry for each room player visits for the first visit
def initial_room_logger():
    init = player_initilization()
    room_id = init['room_id'] 
    unexplored = init['exits']
    room = init
    room['unexplored_exits'] = unexplored
    #print('DIS ROOM', room)
    print("This is the current rooms ID ===", room_id)
    #adds room to map graph
    map_graph[room_id] = room
    visited.add(room_id)
    print("Added this room to visited: ", visited)

#pulls unexplored exits from map graph
def pick_unexplored_direction():
    init = player_initilization()
    room_id = init['room_id']

    unexplored = init['unexplored_exits'] #NOT IN THE INIT RESPONSE TODO NEED TO CHANGE THIS TO PULL OFF OF MAP GRAPH
    print('THESE ARE THE REMAINING UNEXPLORED DIRECTIONS FROM THIS ROOM ', unexplored)
    
    direction = unexplored[0]
    print("This is the functions chosen DIRECTION", direction)
    
    #removes exit chosen from unexplored
    map_graph[room_id]['unexplored_exits'].remove(f'{direction}')
    
    return direction


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Logic~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
visited = set()
print(visited)

initial_room_logger()

while len(map_graph) < 500:
    room_id = get_room_id()
    print("Current ROOM ID ************", room_id) 
    print("TEEEEEST", map_graph[room_id]['room_id'])
    print("TEEEEEST", map_graph[room_id]['unexplored_exits'])
    if map_graph[room_id]['room_id'] in visited:
        if (len(map_graph[room_id]['unexplored_exits']) > 0):
           
            path = pick_unexplored_direction()
            print("The unexplored direction chosen ====> ", path)
            
            player_move({'direction' : f'{path}'})
            print("Moved --------------------> ", path)
            
            traversal_path.append(path)
            print("UPDATED Traversal Path~~~~~", traversal_path)
        else:
            last_move_direction = traversal_path[-1]
            traversal_path.pop(-1)
            print("UPDATED Traversal Path~~~~~", traversal_path)
            
            inverse_direction = { "n": "s", "e": "w", "w": "e", "s": "n" }
            move_back_direction = inverse_direction[last_move_direction]

            
            print("Move BACK DIRECTION CHOSEN -------", move_back_direction)
            player_move({'direction' : f'{move_back_direction}'})
            print("Moved --------------------> ", move_back_direction)
    elif map_graph[room_id]['room_id'] not in visited:
        initial_room_logger()
        if (len(map_graph[room_id]['unexplored_exits']) > 0):
           
            path = pick_unexplored_direction()
            print("The unexplored direction chosen ====> ", path)
            
            player_move({'direction' : f'{path}'})
            print("Moved --------------------> ", path)
            
            traversal_path.append(path)
            print("UPDATED Traversal Path~~~~~", traversal_path)
        else:
            last_move_direction = traversal_path[-1]
            traversal_path.pop(-1)
            print("UPDATED Traversal Path~~~~~", traversal_path)
            
            inverse_direction = { "n": "s", "e": "w", "w": "e", "s": "n" }
            move_back_direction = inverse_direction[last_move_direction]
            
            print("Move BACK DIRECTION CHOSEN -------", move_back_direction)
            player_move({'direction' : f'{move_back_direction}'})
            print("Moved --------------------> ", move_back_direction)



            

    











#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Testing Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# player_init = initilization()
# player_room_id = player_init[room_id]

#Test Functions
#player_initilization()

#player_status()

#player_move({'direction' : 'n'})
#player_move({'direction' : 's'})

# initial_room_logger()
print(map_graph)
# map_graph[0]['unexplored_exits'].remove('w')
# print(map_graph[0]['unexplored_exits'])
# print(len(map_graph[0]['unexplored_exits']))