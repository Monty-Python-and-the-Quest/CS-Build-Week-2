import requests
import time
import random

from util import Queue

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Pseudocode~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


player = #init import function here TODO

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



