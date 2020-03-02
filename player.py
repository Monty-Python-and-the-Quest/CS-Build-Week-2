import requests
import hashlib
import json
import time
from api_key import API_KEY

auth_key = API_KEY

headers = {'Authorization': auth_key, 'Content-Type': 'application/json'}

class Player:
    def __init__(self, name, starting_room):
        self.name = name
        self.current_room = starting_room
        self.base_url = "https://lambda-treasure-hunt.herokuapp.com/api"


        self.cooldown = None  
        self.room = None 
        

# Init
    def init(self):
        endpoint = "/adv/init/"
        res = requests.get(self.base_url + endpoint, headers=headers)

        self.room = json.loads(res.text)  
        self.cooldown = self.room['cooldown']  


# move
    def move(self, direction):
        endpoint = "/adv/move/"
        data = {"direction": direction}

        res = requests.post(self.base_url + endpoint,
                            headers=headers,
                            data=json.dumps(data))
       
        self.room = json.loads(res.text)
<<<<<<< HEAD
=======

>>>>>>> 381164c575d99551903d34a5485489c4a5523e1d
        self.cooldown = self.room['cooldown']  
        return res.json()

# wise move
    def wise_move(self, direction, room):
        print(f'Direction: {direction} Room: {room}')
        endpoint = "/adv/move/"
        data = {"direction": direction, "next_room": room}
        res = requests.post(self.base_url + endpoint,
                            headers=headers,
                            data=json.dumps(data))
<<<<<<< HEAD
        
=======

>>>>>>> 381164c575d99551903d34a5485489c4a5523e1d
        self.room = json.loads(res.text)
        self.cooldown = self.room['cooldown']  
        print(res.json())
        return res.json()
<<<<<<< HEAD
=======

>>>>>>> 381164c575d99551903d34a5485489c4a5523e1d
# Take

    def take(self):
            endpoint = "/adv/take/"
            data = {"name": "treasure"}
            res = requests.post(self.base_url + endpoint,
                                headers=headers,
                                data=json.dumps(data))
            print(f'------- {res.text} TAKING TREASURE')
<<<<<<< HEAD
            
            self.room = json.loads(res.text)
=======

            
            self.room = json.loads(res.text)

>>>>>>> 381164c575d99551903d34a5485489c4a5523e1d
            self.cooldown = self.room['cooldown']  

            if self.room['errors']:
                print(self.room['errors'])
            else:
                print(self.room['messages'])



P = Player("User 20600", 2)

print(P.move("s"))