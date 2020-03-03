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
        self.coin_balance = None

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
        
        self.room = json.loads(res.text)
        self.cooldown = self.room['cooldown']  
        print(res.json())
        return res.json()
# Take

    def take(self):
            endpoint = "/adv/take/"
            data = {"name": "treasure"}
            res = requests.post(self.base_url + endpoint,
                                headers=headers,
                                data=json.dumps(data))
            print(f'------- {res.text} TAKING TREASURE')
            
            self.room = json.loads(res.text)
            self.cooldown = self.room['cooldown']  

            if self.room['errors']:
                print(self.room['errors'])
            else:
                print(self.room['messages'])

# Drop

    def drop(self):
            endpoint = "/adv/drop/"
            data = {"name": "treasure"}
            res = requests.post(self.base_url + endpoint,
                                headers=headers,
                                data=json.dumps(data))
            print(f'------- {res.text} DROP TREASURE')

            
            self.room = json.loads(res.text)

            self.cooldown = self.room['cooldown']  

            if self.room['errors']:
                print(self.room['errors'])
            else:
                print(self.room['messages'])
         
# Staus

    def status(self):
        endpoint = "/adv/status/"
        res = requests.post(self.base_url + endpoint, headers=headers)
        print(f'------- {res.text} STATUS')

        self.p_status = json.loads(res.text)  
        self.cd = self.p_status['cooldown']  

# Examine

    def examine(self, item):
        endpoint = "/adv/examine/"
        data = {"name": item,}
        res = requests.post(self.base_url + endpoint,
                            headers=headers,
                            data=json.dumps(data))
        print(f'------- {res.text} WISHING WELL INFO')

# Balance 

    def balance(self):
        endpoint = '/bc/get_balance'
        res = requests.get(self.base_url + endpoint, headers=headers)

        self.coin_balance = json.loads(res.text)
        self.cd = self.coin_balance['cooldown'] 
        return res.json()

# 


# Test 
P = Player("User 20600", 2)
print(P.balance())

