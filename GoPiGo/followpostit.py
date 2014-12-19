import vision
import cv2
import gopigo
from parseconfig import parse_config

tracker = vision.TrackSquare(False)

configuration = parse_config('follow')

while True:
    processed, square = tracker.track_show()
    
    if square['w'] != 0:
        area = square['u_width'] * square['u_height']
        if abs(square['x']) > configuration['rotate_tol']:
            if square['x'] > configuration['rotate_tol']:
                gopigo.right()
                print "right"
            else:
                gopigo.left()
                print "left"
        elif configuration['target_area']*(1-configuration['area_tol']) > area or configuration['target_area']*(1+configuration['area_tol']) < area:
            if configuration['target_area']*(1+configuration['area_tol']) < area:
                gopigo.bwd()
                print "bwd"
            else:
                gopigo.fwd()
                print "fwd"
        else:
            gopigo.stop()
    print str(square)
    #cv2.imshow("Live Capture", processed)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break
