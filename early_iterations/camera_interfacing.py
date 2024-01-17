import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

cam = cv2.VideoCapture(0)

image_path = ""

def show_image(image, title, path):
    
    cv2.imshow(title, image)
    
    if path == "":
        print("not saving", title, "to file")
    else:
        cv2.imwrite(path, image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_image():
    
    #this method will save a single image-- do we want to store it locally? probably not, let's not save it anywhere
    
    result, image = cam.read()
    cv2.imwrite(image_path, image)
    
    #cv2.imshow("test_image",image)
    
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
    return image

def blur(image):
    
    gray_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)

#now we've ensured the image is in gray scale (precaution)
#it's going to be hard to cross-section if we can't locate the spot very nicely--
#I think it's time to focus on blurring again

    blurred_image = cv2.blur(gray_image,(21,21))
    
    show_image(blurred_image, "blurred","/home/tujuntian/Desktop/lock monitoring/pics/testimage_blurred.jpg") 

    return blurred_image

def do_thresholding(image):
    
    result, thresholded_image = ret, thresh1 = cv2.threshold(image, 0.75*255, 255, cv2.THRESH_BINARY)
    
    show_image(thresholded_image, "thresholded", "/home/tujuntian/Desktop/lock monitoring/pics/testimage_threshd.jpg")
    
    return thresholded_image

def get_contours(image):
    
    image = blur(image)
    
    image = do_thresholding(image)
    
    canny = cv2.Canny(image, 20,30)
    
    show_image(canny, "post-Canny", "/home/tujuntian/Desktop/lock monitoring/pics/post_canny.jpg")
    
    contours, hierarchy= cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(test_image, contours, -1, (0,255,0), 2)
    
    show_image(test_image, "objects found", "/home/tujuntian/Desktop/lock monitoring/pics/objects_found.jpg")
    
    return contours, hierarchy

def plot_profiles(xth, x, yth, y):
        
    x_x = np.arange(480)
    x_y = np.arange(640)
    
    plt.plot(x_x, xth, label="thresholded")
    plt.plot(x_x, x,label = "raw sum")
    plt.title("sum along rows")
    plt.xlabel("row number")
    plt.ylabel("sum of grayscale values")
    plt.legend()
    plt.show()
    
    plt.plot(x_y, yth, label="thresholded")
    plt.plot(x_y, y, label="raw sum")
    plt.title("sum along columns")
    plt.xlabel("column number")
    plt.ylabel("sum of grayscale values")
    plt.legend()
    plt.show()
    
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
            y_indicies.append(j)
        else:
            continue
    
    center_x = x_indices[int(np.round(len(x_indices)/2, 0))]
    center_y = y_indices[int(np.round(len(y_indices)/2, 0))]
    
    center = [center_x, center_y]
    
    return center

def is_locked():

    with Image.open(image_path) as im:
        
        im = im.convert("L")
            
    image_arr = np.asarray(im)
    print(image_arr)
    print(image_arr.shape)
    
    y = np.zeros(640)
    x = np.zeros(480)
    
    #summing
    
    for i in range(640):
        y[i] = np.sum(image_arr[:, i])
        
    for j in range(480):
        x[j] = np.sum(image_arr[j, :])

    avg_x = np.mean(x)
    avg_y = np.mean(y)
    
    print(avg_x)
    print(avg_y)
    
    #now, we have an x array and a y array which are the sums of whichever columns and rows
    #we can think of these as cross-sections
    #you can get the average value of the row or column by dividing by eiher 480 or 640
    
    #we need to figure out how we want to make the diy threshold criterion
    #taking this to be the FWHM,
    
    og_max_x = np.max(x)
    og_max_y = np.max(y)
    
    th_y = 0.5*og_max_y
    th_x = 0.5*og_max_x

    yth = np.zeros(640)
    xth = np.zeros(480)
    
    for i in range(640):
        
        if y[i] < th_y:
            yth[i] = 0
        else:
            yth[i] = og_max_y
    
    for j in range(480):
        
        if x[j] < th_x:
            xth[j] = 0
        else:
            xth[j] = og_max_x
    
    #this certainly didn't yield the results I was expecting (a lot of points remain nonzero)
    #let's plot them for fun
    
    plot_profiles(xth, x, yth, y)
    
    #now let's figure out how to use the thresholded data to get some useful information out of it

    center = find_center(xth, yth)
    
    if xth[center[0]] >= x_threshold & yth[center[1]] >= y_threshold:
        is_locked = 1
        print("laser is locked!")
    else:
        is_locked = 0
        print("laser is unlocked!")
        
    return is_locked

test_image = get_image()

show_image(test_image,"test image", "")

is_locked()

#should save an example test image eventually just so it exists somewhere
