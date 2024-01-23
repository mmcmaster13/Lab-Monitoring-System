#the goal of this is to run the lock determination on the camera data from the ULE cavities

import time
import numpy as np

import cv2
from PIL import Image

import statistics as stats

from Cavity import Cavity

#0: 840
#2: 1112
#4:
#6:

def get_ule_status(cavity, image_path):

    t_end = time.time() + cavity.sample_time

    points = []

    cam = cv2.VideoCapture(cavity.address)

    while time.time() < t_end:
        # take pics and process
        # add value at center to a list
        # calculate variance of values
        # compare to variance threshold

        #taking picture and writing it to a file just in case we want it
        #it will be overwritten with each iteration but I'm not sure how else you could even manage this

        result, image = cam.read()
        cv2.imwrite(image_path, image)

        #cam.release()


        #I'm not sure what best practice for this situation is, i.e.
        #I don't know if I should keep cv2 open or close it all the time
        #this needs help

        #waitKey displays an image so I think we can get rid of it altogether

        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        with Image.open(image_path) as im:

            #convert to grayscale for easy indexing
            im = im.convert("L")

        #turn the image into an array of numbers
        image_arr = np.asarray(im)

        intensity = image_arr[cavity.center[0], cavity.center[1]]

        points.append(intensity)

    var = np.var(points)
    average_intensity = np.mean(points)

    if var <= cavity.var_threshold and average_intensity >= cavity.i_threshold:
        is_locked = True
    else:
        is_locked = False
    
    print(is_locked)

    return is_locked

#testing get_ule_status with the 1112

ule_1112 = Cavity(1112, 2, 200, 0.02, [163,256], 10)

get_ule_status(ule_1112, "/home/rbyb/Desktop/test_image.jpg")