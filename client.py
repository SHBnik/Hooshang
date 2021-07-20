#!/usr/bin/env python
import rospy
from std_msgs.msg import String,Int8
import time 
import os
import requests





movement_URL = "http://192.168.1.5:3000/checkMovement"
main_URL = "http://192.168.1.5:3000/"
  




face_modes = { 0: 'normal',
         1: 'laugh',
         2:'upset',
         3:'surprise',
         4:'shy'
} 









def face_change(data):
    rospy.loginfo(rospy.get_caller_id() + "current face %s", face_modes[data.data])
    r = requests.get(url = main_URL+face_modes[data.data])



def listen():
    while not rospy.is_shutdown():
        movement_req = requests.get(url = movement_URL)
        new_data = movement_req.text
        data = ''
        move_body_flag = False
        auto_face_flag = False

        if new_data != '':
            if movement_req.text == "moveLeft":
                if not move_body_flag: 
                    move_body_flag = True
                    data = movement_req.text
            elif movement_req.text == "moveRight":
                if not move_body_flag: 
                    move_body_flag = True
                    data = movement_req.text
            elif movement_req.text == "moveBack":
                if not move_body_flag: 
                    move_body_flag = True
                    data = movement_req.text
            elif movement_req.text == "moveFront":
                if not move_body_flag: 
                    move_body_flag = True
                    data = movement_req.text
            elif movement_req.text == "roundLeft":
                if not move_body_flag: 
                    move_body_flag = True
                    data = movement_req.text
            elif movement_req.text == "roundRight":
                if not move_body_flag: 
                    move_body_flag = True
                    data = movement_req.text
            elif movement_req.text == "armRightBottom":
                data = movement_req.text
            elif movement_req.text == "armRightTop":
                data = movement_req.text
            elif movement_req.text == "armLeftTop":
                data = movement_req.text
            elif movement_req.text == "armLeftBottom":
                data = movement_req.text
            elif movement_req.text == "neckRight":
                data = movement_req.text
            elif movement_req.text == "neckLeft":
                data = movement_req.text
            elif movement_req.text == "neckBottom":
                data = movement_req.text
            elif movement_req.text == "neckTop":
                data = movement_req.text

            
            elif movement_req.text == "autoFace":
                if not auto_face_flag:
                    auto_face_flag = True
                    auto_face_command.publish('start/stop')

            else:
                if move_body_flag:
                    move_body_flag = False
                    data = "moveStop"
                if auto_face_command:
                    auto_face_flag = False


            if data:
                move_command.publish(data)
                data = ''
        
        time.sleep(0.01)


if __name__ == "__main__":
    rospy.init_node('hooshang/web_client', anonymous=True)
    move_command = rospy.Publisher('hooshang/web_client/move_command', String, queue_size=10)
    auto_face_command = rospy.Publisher('hooshang/auto_face/start', String, queue_size=10)
    rospy.Subscriber("hooshang/web_client/face", Int8, face_change)
    listen()