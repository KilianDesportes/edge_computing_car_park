from places_detection_v3 import getContours
import cv2
import numpy as np
class CoordinatesDetector: 

    def __init__(self, img_in, file_out):
        self.image_input = img_in
        self.output_file = file_out

    def test_detect(self):
        input_file = "output/yml_output.yml"
        
        with open(input_file, 'r') as in_file:
            for line in in_file:
                self.output_file.write(line)

        return self.output_file

    def detect(self,areamax,areamin,whitetreshold):
        out = self.output_file
        img = cv2.imread(self.image_input)
        AREAMAX = int(areamax)
        AREAMIN = int(areamin)
        white_treshold_detection = int(whitetreshold)
        getContours(img,AREAMIN,AREAMAX,out,white_treshold_detection)