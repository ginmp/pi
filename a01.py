import cv2
import os
import time
import numpy as np

files = os.listdir('./images')
print(files)


transit_slides = 10

min_weight = 0
 
max_weight = 10

def load_img(pathImageRead, resizeWidth, resizeHeight): 	
    
    _img_input = cv2.imread(pathImageRead,cv2.IMREAD_UNCHANGED)
    if _img_input is not None:
        _img_height, _img_width = _img_input.shape[:2]
    
        if _img_width > resizeWidth or _img_height > resizeHeight:
            interpolation = cv2.INTER_AREA
        else:
            interpolation = cv2.INTER_LINEAR
        
        _img_resized = cv2.resize(_img_input, (resizeWidth, resizeHeight), interpolation)
    else:
        _img_resized = _img_input
    return _img_resized

def range_step(start, step, stop):
    range = start
    while range < stop:
        yield range
        range += step

class SlideShow():

    def __init__(self, images, width=500,height=500, exit_key=ord('q'), slideshow_time=2000):
        self.images = images
        self.height = height
        self.width = width
        self.exit_key = exit_key
        self.slideshow_time = slideshow_time
        self.image_id = 0

    def key_pressed(self,wait_time):
        _key_pressed = cv2.waitKey(wait_time)
        if self.exit_key == _key_pressed:        
            cv2.destroyAllWindows()
            return True
        return False

    def get_image(self):
        self.image_id += 1
        self.image_id %= len(self.images)
        return self.images[self.image_id]

    def start(self):
        while True:
            img0 = self.get_image()

            cv2.imshow('Img',img0)

            if self.key_pressed(self.slideshow_time):
                break
            

            #img1 = self.get_image()
        


            #for loop through every weight in range 
            #for weight_two in range_step(min_weight, float (max_weight)/transit_slides, max_weight):
                
            #     weight_one = max_weight - weight_two
                
            #     slide_img = cv2.addWeighted(img0, weight_one, img1, weight_two, 0)

            #     cv2.imshow('Img',slide_img)

            #     key_pressed = cv2.waitKey(wait_slideshow//2)
            #     if exit_key == key_pressed:        
            #         cv2.destroyAllWindows()
            #         break
            # # wait for slide show time to complete and break if Esc key pressed
            # if self.key_pressed(self.slideshow_time):
            #     break
            #copy image two to image one	
            # img0 = img1


width = 500
height = 500
images = [load_img("./images/{}".format(i),width,height) for i in files]

slideshow = SlideShow(images,width,height)
slideshow.start()