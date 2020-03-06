import requests
import time
import random
import json

from util import Queue


#Endpoint Url
url = "https://lambda-treasure-hunt.herokuapp.com/api"

#Needed with all requests
headers = {
    "Authorization": "Token" 
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Player Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Initialization
def player_initilization():
    time.sleep(6)
    response = requests.get(f'{url}/adv/init/', headers = headers)
    data = response.json()
    print("                                                                                                                   ") 
    print("This is th INIT response--->", data)
    print("                                                                                                                   ") 

    return data

#Player Status
def player_status():
    response = requests.post(f'{url}/adv/status/', headers = headers)
    data = response.json()
    print("This is the STATUS response--->", data)
    return data
    
#Player Movement TODO dynamic cooldown pulled off of init res
def player_move(payload):
    time.sleep(6)
    response = requests.post(f'{url}/adv/move/', data = json.dumps(payload), headers = headers)
    data = response.json()
    
    info = []
    info.append(data)
    # when we move need to print to map.txt
    with open('map.txt', 'a+') as outfile:
        json.dump(info, outfile, indent=2)
   
    print("This is the MOVE response--->", data)
    print("                                                                                                                   ") 

    return data

#Item Looting
def loot_treasure(payload):
    response = requests.post(f'{url}/adv/take/', data= json.dumps(payload), headers = headers)
    data = response.json()
    print("This is the LOOT response--->", data)
    return data

# TAKE FUNCTION
def take(payload):
    r = requests.post(f'{url}/adv/take', data=json.dumps(payload), headers=headers)
    data = r.json()
    info = []
    info.append(data)

    # 
    with open('player_status.txt', 'w') as outfile:
        json.dump(info, outfile, indent=2)

    print(data)
    return data
    
    


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DFT like Traversal Algorithm WIP~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

traversal_path = []

#Graph dictionary of world map
map_graph = {}

#Gets room ID
def get_room_id(cooldown):
    print("The older cooldown PREINIT time in seconds:", cooldown)
    print("                                                                                                                   ")
    time.sleep(cooldown + 6)
    init = player_initilization()
    new_cooldown = init['cooldown']
    print("The  new cooldown time in seconds:", new_cooldown)
    print("                                                                                                                   ")
    #get cooldown and wait here TODO
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
    return unexplored

#pulls unexplored exits from map graph
def pick_unexplored_direction():
    init = player_initilization()
    room_id = init['room_id']


    unexplored = map_graph[room_id]['unexplored_exits'] #NOT IN THE INIT RESPONSE TODO NEED TO CHANGE THIS TO PULL OFF OF MAP GRAPH
    print('THESE ARE THE REMAINING UNEXPLORED DIRECTIONS FROM THIS ROOM ', unexplored)
    
    direction = unexplored[0]
    print("This is the functions chosen DIRECTION", direction)
    
    #removes exit chosen from unexplored
    map_graph[room_id]['unexplored_exits'].remove(f'{direction}')
    
    return direction


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Logic~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
visited = set()
print(visited)
current_cooldown = 5
initial_room_logger()
most_recent_direction = None
inverse_direction = { "n": "s", "e": "w", "w": "e", "s": "n" }

while len(map_graph) < 500:
    print("                                                                                                                   ") 
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&-----VISITED Beginning of LOOP", visited)
    print("                                                                                                                   ") 
    
    room_id = get_room_id(current_cooldown)
    
    print("Current ROOM ID ************", room_id)
    print("                                                                                                                   ") 
    #print("TEEEEEST", map_graph[room_id]['room_id']) #returns key error if you hit unvisited
    print("                                                                                                                   ") 
    #print("************************UNEXPLORED EXITS REMAINING********************", map_graph[room_id]['unexplored_exits']) #returns key error if you hit unvisited
    print("                                                                                                                   ") 
    print("THE Most recent direction TAKEN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", most_recent_direction)
    print("                                                                                                                   ") 

    if room_id in visited:#stable
        print("VISITED INSIDE LOOP", visited)
        if (len(map_graph[room_id]['unexplored_exits']) > 0):
           
            path = pick_unexplored_direction()
            print("<==================================================================The unexplored direction chosen =======================> ", path)
            print("                                                                                                                   ") 
            
            data = player_move({'direction' : f'{path}'})
            most_recent_direction = path
            new_cooldown = data['cooldown']
            current_cooldown = new_cooldown
            print("-----------------------------------------------Moved --------------------> ", path)
            print("                                                                                                                   ") 
            
            traversal_path.append(path)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~UPDATED Traversal Path~~~~~", traversal_path)
            print("                                                                                                                   ") 
        else:
            last_move_direction = traversal_path[-1]
            traversal_path.pop(-1)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~UPDATED Traversal Path~~~~~", traversal_path)
            print("                                                                                                                   ") 
            
            move_back_direction = inverse_direction[last_move_direction]

            
            print("----------------------------------------------------------Move BACK DIRECTION CHOSEN -------", move_back_direction)
            print("                                                                                                                   ") 
            data = player_move({'direction' : f'{move_back_direction}'})
            most_recent_direction = move_back_direction
            new_cooldown = data['cooldown']
            current_cooldown = new_cooldown
            print("----------------------------------------------------------------Moved --------------------> ", move_back_direction)
            print("                                                                                                                   ") 
    elif room_id not in visited:
        unexplored = initial_room_logger()
        to_be_removed = inverse_direction[most_recent_direction]
        unexplored.remove(to_be_removed)
        print("                                                                                                                   ")
        print("                                                                                                                   ")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^CURRENT rooms GRAPH", map_graph[room_id])
        print('UPDATED UNEXPLORED CIRCUMSTANCE---------------------------------------------------------------->', to_be_removed)
        print("                                                                                                                   ")
        print("                                                                                                                   ")
        
        if (len(map_graph[room_id]['unexplored_exits']) > 0):
           
            path = unexplored[0]#---FIX NOT REMOVING PATH see line 112 ----fixed below
            map_graph[room_id]['unexplored_exits'].remove(f'{path}')
            print("<=========================================================The unexplored direction chosen =======================> ", path)
            print("                                                                                                                   ") 
            
            data = player_move({'direction' : f'{path}'})
            most_recent_direction = path
            new_cooldown = data['cooldown']
            current_cooldown = new_cooldown
            print("--------------------------------------Moved --------------------> ", path)
            print("                                                                                                                   ") 
            
            traversal_path.append(path)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~UPDATED Traversal Path~~~~~", traversal_path)
            print("                                                                                                                   ") 
        else:
            last_move_direction = traversal_path[-1]
            traversal_path.pop(-1)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~UPDATED Traversal Path~~~~~", traversal_path)
            print("                                                                                                                   ") 
            
            move_back_direction = inverse_direction[last_move_direction]
            
            print("--------------------------------------Move BACK DIRECTION CHOSEN -------", move_back_direction)
            print("                                                                                                                   ") 
            data = player_move({'direction' : f'{move_back_direction}'})
            most_recent_direction = move_back_direction
            new_cooldown = data['cooldown']
            current_cooldown = new_cooldown
            print("--------------------------------------Moved -----------------------------------> ", move_back_direction)
            print("                                                                                                                   ") 


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Testing Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# player_init = initilization()
# player_room_id = player_init[room_id]

#Test Functions
#player_initilization()

#player_status()

# data = player_move({'direction' : 's'})
# new_cooldown = data['cooldown']
# print("CURRENT CC", current_cooldown)
# print("NEW CC", new_cooldown)
# current_cooldown = new_cooldown
# print("current AGAIN", current_cooldown)



#player_move({'direction' : 'n'})
#player_move({'direction' : 's'})

# initial_room_logger()
print(map_graph)
# map_graph[0]['unexplored_exits'].remove('w')
# print(map_graph[0]['unexplored_exits'])
# print(len(map_graph[0]['unexplored_exits']))


#TODO ideas to improve alfo 1. save move response so you dont have to init
