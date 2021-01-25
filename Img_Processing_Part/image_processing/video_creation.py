import cv2
import numpy as np
import glob
 
time_in_sec = 60
fps = 12
# 1440 imgs
nb_img = 4

img = cv2.imread("test_input/images/img20.png")

img_voitures = cv2.imread("test_input/images/img20_voitures.png")
img_voitures2 = cv2.imread("test_input/images/img20_voitures2.png")
img_voitures3 = cv2.imread("test_input/images/img20_voitures3.png")

video_file_name = "test_input/test_insa_img20.mp4"

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
height, width, layers = img.shape
size = (width,height)

out = cv2.VideoWriter(video_file_name,fourcc,fps,size)

for i in range(time_in_sec*fps):
    if i < (time_in_sec*fps)/nb_img:
        out.write(img)
    elif i >= (time_in_sec*fps)/nb_img and i < ((time_in_sec*fps)/nb_img)*2:
        out.write(img_voitures)
    elif i >= ((time_in_sec*fps)/nb_img)*2 and i < ((time_in_sec*fps)/nb_img)*3:
        out.write(img_voitures3)
    else:
        out.write(img_voitures2)
