from dynamixel_sdk import *
import math
import time

class motors:
    def __init__(self):
        # Control table address
        self.ADDR_MX_TORQUE_ENABLE      = 24               # Control table address is different in Dynamixel model
        self.ADDR_MX_MOVE_SPEED         = 32
        self.ADDR_MX_CW_ANGLE_LIMIT     = 6
        self.ADDR_MX_CCW_ANGLE_LIMIT    = 8 

        # Data Byte Length
        self.LEN_MX_MOVE_SPEED          = 2

        # Protocol version
        self.PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

        # Default setting
        self.DXL1_ID                     = 1                 
        self.DXL2_ID                     = 16                  
        self.DXL3_ID                     = 28                 
        self.BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
        self.DEVICENAME                  = 'COM5'    # Check which port is being used on your controller
                                                        # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

        self.TORQUE_ENABLE               = 1                 # Value for enabling the torque
        self.TORQUE_DISABLE              = 0                 # Value for disabling the torque
        self.DXL_MINIMUM_POSITION_VALUE  = 100           # Dynamixel will rotate between this value
        self.DXL_MAXIMUM_POSITION_VALUE  = 1023            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
        self.DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold
        
        # Initialize PortHandler instance
        # Set the port path
        # Get methods and members of PortHandlerLinux or PortHandlerWindows
        self.portHandler = PortHandler(self.DEVICENAME)

        # Initialize PacketHandler instance
        # Set the protocol version
        # Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
        self.packetHandler = PacketHandler(self.PROTOCOL_VERSION)

        # Initialize GroupSyncWrite instance
        self.groupSyncWrite = GroupSyncWrite(self.portHandler, self.packetHandler, self.ADDR_MX_MOVE_SPEED, self.LEN_MX_MOVE_SPEED)

        # Open port
        self.portHandler.openPort()


        # Set port baudrate
        self.portHandler.setBaudRate(self.BAUDRATE)

        self.set_wheel_mode(self.DXL1_ID)
        self.set_wheel_mode(self.DXL2_ID)
        self.set_wheel_mode(self.DXL3_ID)

        
        self.enable_torque(self.DXL1_ID)
        self.enable_torque(self.DXL2_ID)
        self.enable_torque(self.DXL3_ID)



        zero = self.prepare_packet(0)
        self.groupSyncWrite.addParam(self.DXL3_ID, zero)
        self.groupSyncWrite.addParam(self.DXL2_ID, zero)
        self.groupSyncWrite.addParam(self.DXL1_ID, zero)
        self.groupSyncWrite.txPacket()
        self.groupSyncWrite.clearParam()



    def set_wheel_mode(self, ID):
        self.packetHandler.write2ByteTxRx(self.portHandler, ID, self.ADDR_MX_CW_ANGLE_LIMIT, 0)
        self.packetHandler.write2ByteTxRx(self.portHandler, ID, self.ADDR_MX_CCW_ANGLE_LIMIT, 0)

    def enable_torque(self, ID):
        self.packetHandler.write1ByteTxRx(self.portHandler, ID, self.ADDR_MX_TORQUE_ENABLE, self.TORQUE_ENABLE)

    def disable_torque(self, ID):
        self.packetHandler.write1ByteTxRx(self.portHandler, ID, self.ADDR_MX_TORQUE_ENABLE, self.TORQUE_DISABLE)

    def prepare_packet(self, speed):
        return [DXL_LOBYTE(int(speed)), DXL_HIBYTE(int(speed))]

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def constrain(self, value, min, max):
        if value >= max:    return max
        elif value <= min:  return min
        else:               return value

    def map_dyna(self, value):
        if value >= 0:  return value + 1024
        elif value < 0: return -1 * value

    def stop_motors(self):
        self.disable_torque(self.DXL1_ID)
        self.disable_torque(self.DXL2_ID)
        self.disable_torque(self.DXL3_ID)


    def move(self, speed, theta, yaw, t):

        Vx = speed * math.cos(theta * math.pi / 180)
        Vy = speed * math.sin(theta * math.pi / 180)

        A = -Vx
        B = 0.5 * Vx - 0.866 * Vy
        C = 0.5 * Vx + 0.866 * Vy
        


        A = self.constrain(A + yaw, -500, 500)
        B = self.constrain(B + yaw, -500, 500)
        C = self.constrain(C + yaw, -500, 500)

        A = self.map(A, -500, 500, -1023, 1023)
        B = self.map(B, -500, 500, -1023, 1023)
        C = self.map(C, -500, 500, -1023, 1023)

        A = self.map_dyna(A)
        B = self.map_dyna(B)
        C = self.map_dyna(C)
        
        A = self.prepare_packet(A)
        B = self.prepare_packet(B)
        C = self.prepare_packet(C)

        self.groupSyncWrite.addParam(self.DXL3_ID, A)
        self.groupSyncWrite.addParam(self.DXL2_ID, B)
        self.groupSyncWrite.addParam(self.DXL1_ID, C)

        self.groupSyncWrite.txPacket()


        self.groupSyncWrite.clearParam()

        time.sleep(t)
        self.stop_motors()



        

        

    

    

