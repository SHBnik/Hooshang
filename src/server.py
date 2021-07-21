#!/usr/bin/env python
import rospy
import time 
import os
import subprocess








if __name__ == "__main__":
    rospy.init_node('server', anonymous=True)
    process = subprocess.Popen(['node', 'server'],cwd = "/home/hooshang/catkin_ws/src/hooshang/Smile_Server")

    rospy.spin()
    print('server going down')
    process.terminate()
    
