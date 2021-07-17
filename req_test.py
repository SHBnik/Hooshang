import requests
import time 
import json

URL = "http://192.168.1.2:3000/checkMovement"
  
while 1:
    r = requests.get(url = URL)
    print(r.text)
    time.sleep(0.2)



# Url = "http://192.168.1.2:3000/"

# face = { 0: 'normal',
#          1: 'laugh',
#          2:'upset',
#          3:'surprise',
#          4:'shy'
# } 


# # sending post request and saving response as response object
# r = requests.get(url = Url+face[4])
  
# print(r.text)