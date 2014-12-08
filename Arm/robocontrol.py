import udp
import robotusb
import math

#note: this code designed to be used with the mpu-6050 with the wires facing
#left from your hand and uses the DropBoneImu code
#http://58.162.140.188/mediawiki-1.23.2/index.php/DropBone_IMU
#when I do angle/180*pi, I am converting from degrees to radians
#as euler angles are given in radians
listen_port = 4774
MOVE_BASE = 45.0/180*math.pi
GRIP = 30.0/180*math.pi
MOVE_SHOULDER = 55.0/180*math.pi
MOVE_ELBOW = 40.0/180*math.pi
MOVE_WRIST = 25.0/180*math.pi


def main():
    euler = [0,0,0]
    euler_offset = None
    while True: #main control loop
        values = udp.get_data(listen_port)
        euler = values[:3]
        if not euler_offset:
            euler_offset = euler
        else:
            for angle, offset in zip(euler, euler_offset):
                angle -= offset
        robotusb.StopArm()
        if abs(euler[0]) > MOVE_BASE: # move base with yaw
            if euler[0] > 0:
                robotusb.MoveArm("BASE_CL")
            else:
                robotusb.MoveArm("BASE_AC")
        elif abs(euler[1]) > MOVE_WRIST:
            up = False
            if euler[1] < 0:
                up=True
            if abs(euler[1]) > MOVE_SHOULDER:
                if up:
                    robotusb.MoveArm("SLDR_UP")
                else:
                    robotusb.MoveArm("SLDR_DN")
            elif abs(euler[1]) > MOVE_ELBOW:
                if up:
                    robotusb.MoveArm("ELBW_UP")
                else:
                    robotusb.MoveArm("ELBW_DN")
            elif abs(euler[1]) > MOVE_WRIST:
                if up:
                    robotusb.MoveArm("WRST_UP")
                else:
                    robotusb.MoveArm("WRST_DN")
                
        elif abs(euler[2]) > GRIP: # grip with roll
            if euler[2] > 0:
                robotusb.MoveArm("GRIP_OP")
            else:
                robotusb.MoveArm("GRIP_CS")
    
if __name__ == "__main__":
	main()
