import vision
import robotusb
from collections import OrderedDict
import cv2
from parseconfig import parse_config

configuration = parse_config("arm")

tracker = vision.TrackSquare(False)

while True:
    processed, square = tracker.track_show()
    robotusb.StopArm()
    if square['w'] is not 0:
        if abs(square['x']) > configuration['base_thresh']:
            if square['x'] < 0:
                robotusb.MoveArm("BASE_CL")
            else:
                robotusb.MoveArm("BASE_AC")
        elif abs(square['y']) > configuration['wrist_thresh']:
            up = False
            if square['y'] < 0:
                up = True
            if abs(square['y']) > configuration['shoulder_thresh']:
                if up:
                    robotusb.MoveArm("SLDR_UP")
                else:
                    robotusb.MoveArm("SLDR_DN")
            elif abs(square['y']) > configuration['elbow_thresh']:
                if up:
                    robotusb.MoveArm("ELBW_UP")
                else:
                    robotusb.MoveArm("ELBW_DN")
            elif abs(square['y']) > configuration['wrist_thresh']:
                if up:
                    robotusb.MoveArm("WRST_UP")
                else:
                    robotusb.MoveArm("WRST_DN")
    for key in square:
        print key + " %10f" % square[key]
    cv2.imshow("Live Capture", processed)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        robotusb.StopArm()
        break
