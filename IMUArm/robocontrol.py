import udp
import robotusb
import math

#note: this code designed to be used with the mpu-6050 with the wires facing
#left from your hand and uses the DropBoneImu code
#http://58.162.140.188/mediawiki-1.23.2/index.php/DropBone_IMU
#when I do angle/180*pi, I am converting from degrees to radians
#as euler angles are given in degrees
STOP_THRESH = 5/180*math.pi
STOP_VERT_THRESH = 10/180*math.pi
SHOLDER_THRESH = 20/180*math.pi
ELBOW_THRESH = 30/180*math.pi
WRIST_THRESH = 40/180*math.pi
listen_port = 4774

def main():
    global listen_port, STOP_THRESH, ELBOW_THRESH, SHOULDER_THRESH, WRIST_THRESH
    last_5_pitch = [0, 0, 0, 0, 0] #the differences between each of the last 5 measurements for pitch
    euler = [0,0,0]
    while True: #main control loo
        values = udp.get_data(listen_port)
        last_euler = euler
        euler = values[:3]
        euler_diff = list_diff(euler, last_euler)
        last_5_pitch = last_5_pitch[1:]+euler_diff[2]
        avg = average(last_5_pitch) #average of the last 5 values for pitch
        if (abs(avg) < STOP_VERT_THRESH) or (abs(euler_diff[1])<STOP_THRESH) or (abs(euler_diff[2])<STOP_THRESH):
            robotusb.StopArm()
        #vertical movements (pitch)
        if avg >= STOP_VERT_THRESH:
            if avg < SHOULDER_THRESH:
                robotusb.MoveArm('SLDR_UP')
            elif avg < ELBOW_THRESH:
                robotusb.MoveArm('ELBW_UP')
            elif avg < WRIST_THRESH:
                robotusb.MoveArm('WRST_UP')
        elif avg <= -STOP_VERT_THRESH:
            if avg > -SHOULDER_THERSH:
                robotusb.MoveArm('SLDR_DN')
            elif avg > -ELBOW_THRESH:
                robotusb.MoveArm('ELBW_DN')
            elif avg > -WRIST_THESH:
                robotusb.MoveArm('WRST_DN')
        #base rotations (roll)
        if STOP_THESH<euler_diff[0]<=BASE_THRESH:
            robotusb.MoveArm('BASE_CL')
        elif -STOP_THESH>euler_diff[0]>=-BASE_THRESH:
            robotusb.MoveArm('BASE_AC')

#find the average of the values in list values
def average(values):
    total = 0
    for value in values:
        total += values
    return total/len(values)

#find the difference between each of the values in list one to each of the values in list 2
def list_diff(list1, list2):
    diff = []
    for value1 in list1:
        for value2 in list2:
            diff.append(value1-value2)
    return diff
