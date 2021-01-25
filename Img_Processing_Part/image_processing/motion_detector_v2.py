import cv2
import numpy as np
import logging
import json
import time

COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (255, 0, 0)

class MotionDetector:
    LAPLACIAN = 1.4
    DETECT_DELAY = 1

    def __init__(self,video,img_bg,coordinates,window,output_file):
        self.video = video
        self.coordinates_data = coordinates
        self.contours = []
        self.bounds = []
        self.mask = []
        self.window = window
        self.output = output_file
        print(img_bg)
        self.bg = cv2.resize(cv2.imread(img_bg),(650,650))

    def detect_motion(self):
        coordinates_data = self.coordinates_data
        logging.debug("coordinates data: %s", coordinates_data)

        handicap_list = [True] * len(coordinates_data)
        statuses = [False] * len(coordinates_data)
        times = [None] * len(coordinates_data)

        while self.video.isOpened():

            result, frame = self.video.read()
            if frame is None:
                break
            frame = cv2.resize(frame, (650, 650))

            self.fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()  
            fgmask_init = self.fgbg.apply(self.bg)
            fgmask_bg_detect = self.fgbg.apply(frame)

            position_in_seconds = self.video.get(cv2.CAP_PROP_POS_MSEC) / 1000.0


            for index, c in enumerate(coordinates_data):
                coord = np.array(c["coordinates"])
                is_handicap = int(c["handicap_list"]) == 0
                top_left = coord[3]
                bottom_right = coord[1]

                if top_left[1] > bottom_right[1]:
                    crop_init = fgmask_init[bottom_right[1]:top_left[1], top_left[0]:bottom_right[0]]
                    crop_detect = fgmask_bg_detect[bottom_right[1]:top_left[1], top_left[0]:bottom_right[0]]
                else:
                    crop_init = fgmask_init[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
                    crop_detect = fgmask_bg_detect[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
                
                res = cv2.absdiff(crop_init, crop_detect)
                res = res.astype(np.uint8)
                
                percentage = (np.count_nonzero(res) * 100)/ res.size
                status = (percentage < 9)
               
                if times[index] is not None and self.status_changed(statuses, index, status):
                    if position_in_seconds - times[index] >= MotionDetector.DETECT_DELAY:
                        statuses[index] = status
                        handicap_list[index] = is_handicap
                        times[index] = None
                        self.json_output = open(self.output,'w+') #to erase it 
                        self.json_output.write("{\n")
                        y = 0
                        for index,val in enumerate(statuses):
                            self.json_output.write('    \"' + str(y+1) + '\"') #str(y+1) == num de place
                            self.json_output.write(": {\n")
                            self.json_output.write('        \"' + str("free") + '\"') 
                            self.json_output.write(": ")
                            self.json_output.write('\"' + str(val) + '\",\n') #str(i) == place prise ou non
                            self.json_output.write('        \"' + str("disabled") + '\"')
                            self.json_output.write(": ")
                            self.json_output.write('\"' + str(handicap_list[index]) + '\"\n  }') #str(False) == place handicapée ou non
                            if y != len(statuses) - 1:
                                self.json_output.write(',\n') 
                            y = y+1
                        self.json_output.write("\n}")
                        self.json_output.close()
                    continue

                if times[index] is None and self.status_changed(statuses, index, status):
                    times[index] = position_in_seconds

                for index, p in enumerate(coordinates_data):
                    coordinates = np.array(p["coordinates"])
                    disable = np.array(p["handicap_list"])
                    color = COLOR_GREEN
                    if statuses[index] == False: #taken
                        color = COLOR_RED
                    if disable ==0:
                        color = COLOR_BLUE
                    cv2.drawContours(frame, [coordinates], -1, color, 3)


            if self.window:
                cv2.imshow(str(self.video), frame)
                k = cv2.waitKey(1)
                if k == ord("q"):
                    break

        self.json_output.close()
        self.video.release()
        cv2.destroyAllWindows()


    @staticmethod
    def same_status(coordinates_status, index, status):
        return status == coordinates_status[index]

    @staticmethod
    def status_changed(coordinates_status, index, status):
        return status != coordinates_status[index]