import argparse
import yaml
from coordinates_generator import CoordinatesGenerator
from motion_detector import MotionDetector
from colors import *
import logging
import cv2
import os
from CSI_camera_pipeline import CameraClass

# video + coordinates file
# python main.py --data ../coordinates_files/places.yml --video ../videos/parking_lot_1.mp4

# video + handmade detection of coordinates
# python main.py --h --data ../coordinates_files/coordinates_output.yml --video ../videos/parking_lot_1.mp4

# camera stream + coordinates file
# python main.py --data ../coordinates_files/places.yml

# camera stream + handmade detection of coordinates
# python main.py --h --data ../coordinates_files/coordinates_output.yml

def main():
    logging.basicConfig(level=logging.INFO)

    args = parse_args()

    window = args.w

    if args.video_file is None:
        video = cv2.VideoCapture(CameraClass.gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    else:
        video = cv2.VideoCapture(args.video_file)

    if args.h is False:
        data_file = args.data_file
    else:
        data_file = args.data_file

        success,image = video.read()
        cv2.imwrite("temp_places_detection.png", image)

        with open(data_file, "w+") as points:
            generator = CoordinatesGenerator("temp_places_detection.png", points, COLOR_RED)
            generator.generate()

        os.remove("temp_places_detection.png")
       
    with open(data_file, "r") as data:
        points = yaml.load(data)
        detector = MotionDetector(video, points,window)
        detector.detect_motion()

def parse_args():
    parser = argparse.ArgumentParser(description='Generates Coordinates File')


    parser.add_argument("--h",
                        action='store_true',
                        help="Mode where places coordinates will be written on --data file after handmade detection of places")

    parser.add_argument("--w",
                        action='store_true',
                        help="Window showing the video")

    parser.add_argument("--data",
                        dest="data_file",
                        required=True,
                        help="Data file to describe places coordinates")

    parser.add_argument("--video",
                        dest="video_file",
                        required=False,
                        help="Video file to detect motion on")


    return parser.parse_args()

if __name__ == '__main__':
    main()


