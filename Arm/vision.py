import cv2
import numpy as np
from collections import OrderedDict
from parseconfig import parse_config

class TrackSquare():
    def __init__(self, auto_loop=False):
        self.configuration = parse_config("post-it")
        
        self.cap = cv2.VideoCapture(-1)
        self.cap.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, self.configuration['brightness'])
        self.cap.set(cv2.cv.CV_CAP_PROP_CONTRAST, self.configuration['contrast'])
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.configuration['width'])
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.configuration['height'])
        
        if auto_loop:
            self.track_show_loop()
            
    def track_show(self):
        ret, image = self.cap.read()
        
        processed, info = self.find_square(image)
        
        return processed, info
        
    def track_show_loop(self):
        while True:
            ret, image = self.cap.read()
        
            processed, info = self.find_square(image)
            
            cv2.imshow("Live Capture", processed)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        

    def find_square(self, image):
        output = image.copy()
        
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        #threshold image
        lower = np.array(self.configuration['hsv_bounds'][0])
        upper = np.array(self.configuration['hsv_bounds'][1])
        
        mask = cv2.inRange(hsv_image, lower, upper) # filter out all but values in the above range
        result = cv2.bitwise_and(image,image, mask=mask)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))
        emask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=self.configuration['erode_dialate_iterations'])

        erd_dlt_image = cv2.bitwise_and(result,result, mask=mask) #image after errode and dialate
        
        contours, heirarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            return erd_dlt_image, OrderedDict([('x',0), ('y',0), ('w',0), ('h',0), ('angle',0)])

        target_contour = None
        target_rect = None
        target_area = 0
        found_target = False
        stats = []
        rect = []
        #Then sanity checks to find the largest contour that has the correct dimentions, area and side ratio
        for contour in contours:
            area = cv2.contourArea(contour)
            if area>target_area and area>(self.configuration['min_area']*image.shape[1]*image.shape[1]):# ifs are staggered for efficiency reasons
                rect = cv2.minAreaRect(contour)
                stats = get_data(rect, image)
                if stats['w']/stats['h']<self.configuration['ratio']*(1+self.configuration['target_tol']):
                    #print "found one"
                    target_contour = contour
                    target_area = area
                    found_target = True
                    target_rect = rect
                    
        cv2.drawContours(image, contours, -1, (255, 0, 0), 2)
        
        if found_target:
            obb_image = erd_dlt_image
            obb = cv2.cv.BoxPoints(target_rect)
            obb = np.int0(obb)
            cv2.drawContours(obb_image, [obb], -1, (0,0,255), 3)
            return obb_image, stats
        
        return erd_dlt_image, OrderedDict([('x',0), ('y',0), ('w',0), ('h',0), ('angle',0)])
        
def get_data(rect, image):
    img_height, img_width, depth = image.shape
    if rect[1][0]>rect[1][1]:
        w=rect[1][0]/img_width
        h=rect[1][1]/img_width
        angle = rect[2]
        swapped = False # we have not swapped the configuration['width'] and configuration['height']
    else:
        w=rect[1][1]/img_width
        h=rect[1][0]/img_width
        angle = 90+rect[2]
    x = 2*(rect[0][0]/img_width)-1
    y = 2*(rect[0][1]/img_height)-1
    return OrderedDict([('x',x), ('y',y), ('w',w), ('h',h), ('angle',angle)])
        
