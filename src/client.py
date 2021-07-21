#!/usr/bin/env python
import rospy
from std_msgs.msg import String,Int8
import time 
import os
import requests





# movement_URL = "http://192.168.1.5:3000/checkMovement"
# main_URL = "http://192.168.1.5:3000/"
movement_URL = "http://0.0.0.0:3000/checkMovement"
main_URL = "http://0.0.0.0:3000/"
  




face_modes = { 0: 'normal',
         1: 'laugh',
         2:'upset',
         3:'surprise',
         4:'shy'
} 









def face_change(data):
    try:
        rospy.loginfo(rospy.get_caller_id() + "current face %s", face_modes[data.data])
        r = requests.get(url = main_URL+face_modes[data.data])
    except Exception as e:
        rospy.loginfo(rospy.get_caller_id() + "client error %s", e)



def listen():
    rate = rospy.Rate(10)
    move_body_flag = False
    auto_face_flag = False
    while not rospy.is_shutdown():
        try:
            movement_req = requests.get(url = movement_URL)
            new_data = movement_req.text
            data = ''

            if new_data != '':
                print(new_data)
                if new_data == "moveLeft":
                    if not move_body_flag: 
                        move_body_flag = True
                        data = new_data
                elif new_data == "moveRight":
                    if not move_body_flag: 
                        move_body_flag = True
                        data = new_data
                elif new_data == "moveBack":
                    if not move_body_flag: 
                        move_body_flag = True
                        data = new_data
                elif new_data == "moveFront":
                    if not move_body_flag: 
                        move_body_flag = True
                        data = new_data
                elif new_data == "roundLeft":
                    if not move_body_flag: 
                        move_body_flag = True
                        data = new_data
                elif new_data == "roundRight":
                    if not move_body_flag: 
                        move_body_flag = True
                        data = new_data
                elif new_data == "armRightBottom":
                    data = new_data
                elif new_data == "armRightTop":
                    data = new_data
                elif new_data == "armLeftTop":
                    data = new_data
                elif new_data == "armLeftBottom":
                    data = new_data
                elif new_data == "neckRight":
                    data = new_data
                elif new_data == "neckLeft":
                    data = new_data
                elif new_data == "neckBottom":
                    data = new_data
                elif new_data == "neckTop":
                    data = new_data

                
                elif new_data == "autoFace":
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
            
            rate.sleep()
        except Exception as e:
            rospy.loginfo(rospy.get_caller_id() + "client error %s", e)


if __name__ == "__main__":
    rospy.init_node('web_client', anonymous=True)
    move_command = rospy.Publisher('web_client/move_command', String, queue_size=10)
    auto_face_command = rospy.Publisher('auto_face/start', String, queue_size=10)
    rospy.Subscriber("web_client/face", Int8, face_change)
    listen()