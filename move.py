#!/usr/bin/env python
import rospy
from std_msgs.msg import String,int8
import time 
import os
import requests

import dyna
import time





speed = 250
pos_up = 530
pos_right = 500
right_hand = 200
left_hand = 874



def move(data):
    if data.data == 'moveStop':
        mot.stop_motors()
    elif data.data == 'moveLeft':
        mot.move(speed,0,0)
    elif data.data == 'moveRight':
        mot.move(speed,180,0)
    elif data.data == 'moveBack':
        mot.move(speed,270,0)
    elif data.data == 'moveFront':
        mot.move(speed,90,0)
    elif data.data == 'roundRight':
        mot.move(0,0,speed-50)
    elif data.data == 'roundLeft':
        mot.move(0,0,speed+50)
    elif data.data == 'armRightBottom':
        right_hand = mot.constrain(right_hand - 2,10,1020)
        mot.hand(right_hand,0)
    elif data.data == 'armRightTop':
        right_hand = mot.constrain(right_hand + 2,10,1020)
        mot.hand(right_hand,0)
    elif data.data == 'armLeftBottom':
        left_hand = mot.constrain(left_hand + 2,10,1020)
        mot.hand(left_hand,1)
    elif data.data == 'armLeftTop':
        left_hand = mot.constrain(left_hand - 2,10,1020)
        mot.hand(left_hand,1)
    elif data.data == 'neckRight':
        pos_right = mot.constrain(pos_right - 5,220,780)
        mot.head(pos_right,1)
    elif data.data == 'neckLeft':
        pos_right = mot.constrain(pos_right + 5,220,780)
        mot.head(pos_right,1)
    elif data.data == 'neckBottom':
        pos_up = mot.constrain(pos_up - 5,445,600)
        mot.head(pos_up,0)
    elif data.data == 'neckTop':
        pos_up = mot.constrain(pos_up + 5,445,600)
        mot.head(pos_up,0)






if __name__ == "__main__":
    rospy.init_node('hooshang/move', anonymous=True)
    move_command = rospy.Publisher('hooshang/web_client/move_command', String, queue_size=10)
    rospy.Subscriber('hooshang/web_client/move_command', String, move)
    mot = dyna.motors()
    
