from coordinates_generator import CoordinatesGenerator
from motion_detector_v2 import MotionDetector
from csi_camera_pipeline import CameraClass
from places_coordinates_detector import CoordinatesDetector

import argparse
import yaml
import logging
import cv2
import os
import shutil

COLOR_RED = (255, 0, 0)

# test with video files :
# python main.py --video ./test_input/test_insa_img20.mp4 --window --bg ./test_input/images/img20.png
# python main.py --video ./test_input/test_insa_img21.mp4 --window --bg ./test_input/images/img21.png

def main():

    if os.path.exists("temp") is False:
        os.makedirs("temp")

    logging.basicConfig(level=logging.INFO)

    args = parse_args()

    # video stream 
    if args.video_input_file is None:
        video = cv2.VideoCapture(CameraClass.gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    else:
        video = cv2.VideoCapture(args.video_input_file)

    # places coordinates, detected or handly generated
    coordinates_file = "temp/places_detection_output.yml"

    output_file = "output/json_output.json"

    img = cv2.imread(args.bg_img_file)
    img = cv2.resize(img,(650,650))

    success,image = video.read()
    image = cv2.resize(image,(650,650))
    image_path = "temp/places_detection_image.png"
    cv2.imwrite(image_path, image) #first image of the video stream, used to detect places

    if args.hand is False:
        with open(coordinates_file,"w+") as coord_file:
            AREAMAX = 280
            AREAMIN = 115
            WHITE_TRESHOLD = 216
            detector = CoordinatesDetector(image_path,coord_file)
            detector.detect(AREAMAX,AREAMIN,WHITE_TRESHOLD)
    else:
        with open(coordinates_file,"w+") as points:
            generator = CoordinatesGenerator(image_path,points,COLOR_RED)
            generator.generate()
    
    with open(coordinates_file, "r") as data:
        points = yaml.load(data)
        detector = MotionDetector(video,args.bg_img_file,points,args.window,output_file)
        detector.detect_motion()

    if args.keep is False:
        shutil.rmtree("temp")

def parse_args():
    parser = argparse.ArgumentParser(description='Image Processing Args')
    parser.add_argument("--hand",
                        action='store_true',
                        help="Hand detection of places coordinates")
    parser.add_argument("--keep",
                        action='store_true',
                        help="Keep temporary files")
    parser.add_argument("--window",
                        action='store_true',
                        help="Window Output")
    parser.add_argument("--video",
                        dest="video_input_file",
                        help="Input video stream")
    parser.add_argument("--bg",
                        dest="bg_img_file",
                        help="Image of video stream when all places are free")
    return parser.parse_args()

if __name__ == '__main__':
    main()


