#we need to set an intensity threshold and a threshold on the variance

import numpy as np
import time

import cv2
from PIL import Image

import statistics as stats

def find_center(xth, yth):
    
    #to find the center, we first need to find where xth/yth are nonzero
    
    x_indices = []
    y_indices = []
    
    for i in range(480):
        
        if xth[i] != 0:
            x_indices.append(i)
        else:
            continue
    
    for j in range(640):
        
        if yth[j] != 0:
            y_indices.append(j)
        else:
            continue
    
    center_x = x_indices[int(np.round(len(x_indices)/2, 0))]
    center_y = y_indices[int(np.round(len(y_indices)/2, 0))]
    
    center = [center_x, center_y]

    #print(center)
    
    return center

#calculate the center position for some amount of time,
#then average the values to estimate the center

#after calculating the center once, we can store it in a Cavity object for each cavity

def time_averaged_center(sample_time, image_path):

    t_end = time.time() + sample_time

    centers = []

    cam = cv2.VideoCapture(2)

    while time.time() < t_end:

        result, image = cam.read()
        cv2.imwrite(image_path, image)

        #cam.release()

        with Image.open(image_path) as im:

            #convert to grayscale for easy indexing
            im = im.convert("L")

        #turn the image into an array of numbers
        image_arr = np.asarray(im)

        y = np.zeros(640)
        x = np.zeros(480)
        
        #summing

        #summing across columns (y)
        for i in range(640):
            y[i] = np.sum(image_arr[:, i])

        #summing across rows (x)
        for j in range(480):
            x[j] = np.sum(image_arr[j, :])

        #taking maxima of 1D sums
        og_max_x = np.max(x)
        og_max_y = np.max(y)

        #calculating FWHM threshold
        th_y = 0.8*og_max_y
        th_x = 0.8*og_max_x

        #arrays for thresholded data
        yth = np.zeros(640)
        xth = np.zeros(480)

        #thresholding over y
        for i in range(640):
            
            if y[i] < th_y:
                yth[i] = 0
            else:
                yth[i] = og_max_y

        #thresholding over x
        for j in range(480):
            
            if x[j] < th_x:
                xth[j] = 0
            else:
                xth[j] = og_max_x

        center = find_center(xth, yth)

        centers.append(center)
    
    x_centers = []
    y_centers = []
    
    for center in centers:
        x_centers.append(center[0])
        y_centers.append(center[1])
    
    center = [int(np.round(np.mean(x_centers), 0)), int(np.round(np.mean(y_centers), 0))]

    print("final: " + str(center))

    return center

def calculate_thresholds(sample_time, image_path, center):

    t_end = time.time() + sample_time

    cam = cv2.VideoCapture(2)

    intensities = []

    while time.time() < t_end:

        result, image = cam.read()
        cv2.imwrite(image_path, image)

        #cam.release()

        with Image.open(image_path) as im:

            #convert to grayscale for easy indexing
            im = im.convert("L")

        #turn the image into an array of numbers
        image_arr = np.asarray(im)

        to_append = image_arr[center[0], center[1]]
        intensities.append(to_append)

    average_intensity = np.mean(intensities)
    variance = np.var(intensities)

    print("average intensity: " + str(average_intensity))
    print("variance: " + str(variance))

    return average_intensity, variance


#time_averaged_center(10, "/home/rbyb/Desktop/test_image.jpg")

center = [163, 256]

average_intensity, variance = calculate_thresholds(60, "/home/rbyb/Desktop/test_image.jpg", center)