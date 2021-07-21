#!/usr/bin/env python3
import rospy
from std_msgs.msg import String,Int8
import time 
import os
import cv2
from fer import FER



start_stop_flag = False
cap = None

last_face_mode = ''
faces = []
num = 0

def start_stop(data):
    global start_stop_flag
    if not start_stop_flag:
        start_stop_flag = True
    else:
        start_stop_flag = False



def most_frequent(List):
    return max(set(List), key = List.count)

def loop():
    global faces,last_face_mode,num

    rate = rospy.Rate(1000)
    while not rospy.is_shutdown():
        if start_stop_flag:
            try:
                ret, image = cap.read()
                image = cv2.rotate(image, cv2.ROTATE_180)
                
                faces.append(detector.top_emotion(image)[0])
                num += 1

                if num == 10:
                    new_face = most_frequent(faces)
                    faces = []
                    num = 0

                    if new_face != last_face_mode:
                        last_face_mode = new_face
                        if new_face == 'happy':
                            face_modes.publish(1)
                        elif new_face == 'sad':
                            face_modes.publish(2)
                        elif new_face == 'surprise':
                            face_modes.publish(3)
                        elif new_face == 'neutral':
                            face_modes.publish(0)

            except Exception as e:
                rospy.loginfo(rospy.get_caller_id() + "some error in FER \n%s", e)


        rate.sleep()

if __name__ == "__main__":
    rospy.init_node('auto_face', anonymous=True)
    face_modes = rospy.Publisher('web_client/face', Int8, queue_size=10)
    rospy.Subscriber("auto_face/start", String, start_stop)
    detector = FER()
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    loop()

