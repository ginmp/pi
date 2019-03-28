import cv2
import os
import time
import numpy as np

def load_img(image_path, width, height): 	
    
    image_input = cv2.imread(image_path) #,cv2.IMREAD_UNCHANGED)
    
    return cv2.resize(image_input, (width, height))

def range_step(start, step, stop):
    range = start
    while range < stop:
        yield range
        range += step

class SlideShow():

    def __init__(self, images, watermark=None,  
                width=500,height=500, 
                border_thickness=20, border_color=(222,222,222),
                exit_key=ord('q'), 
                slideshow_time=200,transaction_time=100):
        self.__images = images
        self.__watermark = watermark
        self.__height = height
        self.__width = width
        self.border_thickness = border_thickness
        self.border_color = border_color
        self.exit_key = exit_key
        self.slideshow_time = slideshow_time
        self.transaction_time = transaction_time
        self.__image_id = 0

    def key_pressed(self,wait_time):
        _key_pressed = cv2.waitKey(wait_time)
        if self.exit_key == _key_pressed:        
            cv2.destroyAllWindows()
            return True
        return False

    def next(self):
        self.__image_id += 1
        self.__image_id %= len(self.__images)
    
    def previous(self):
        self.__image_id -= 1
        self.__image_id %= len(self.__images)

    def get_image(self):
        self.next()
        return self.__images[self.__image_id]
    
    def get_second_image(self):
        image = self.get_image()
        self.previous()
        return image

    def add_watermark(self,image,opacity=.5):
        
        return cv2.addWeighted(image.copy(),1, self.__watermark,opacity, 1)

    def add_border(self,image):
        cv2.rectangle(image, (0, 0), (self.__width, self.__height), self.border_color, self.border_thickness)

    def start(self):
        opacity = .3
        weight_count = self.transaction_time//10 # 100
        weight = 1/weight_count # 0.01

        while True:
            image0 = self.get_image()
            image1 = self.get_second_image()          
            
            image_wm = self.add_watermark(image0, opacity)
            self.add_border(image_wm)

            cv2.imshow('slideshow',image_wm)

            if self.key_pressed(self.slideshow_time):
                return True
            
            for i in range(weight_count):
                weight0 = weight*(weight_count-i) # 0.01 * 0,1,2,...,99
                weight1 = 1 - weight0

                new_image = cv2.addWeighted(image0,weight0, image1,weight1, 1)
                
                new_image = self.add_watermark(new_image, opacity)
                self.add_border(new_image)

                cv2.imshow('slideshow',new_image)

                if self.key_pressed(self.transaction_time//weight_count):
                    return True     
            
        return False           


def get_size(size0, size1, divider):
   
    if size0 > size1:
        bigger = size0
        smaller = size1
        
    else:
        bigger = size1
        smaller = size0

    ratio = smaller / bigger
    size = ratio * bigger
    return int(size//divider)

def get_watermark(path_watermark, image, border_thickness):
    zeros_watermark = np.zeros_like(image)

    image_watermark = cv2.imread(path_watermark, cv2.IMREAD_UNCHANGED)

    wm_height = get_size(image_watermark.shape[0],zeros_watermark.shape[0], 2)
    wm_width = get_size(image_watermark.shape[1],zeros_watermark.shape[1], 2)

    image_watermark = load_img(path_watermark, wm_width,wm_height)

    offset = border_thickness//2

    zeros_watermark[ 
                zeros_watermark.shape[0] - (wm_height + offset) : zeros_watermark.shape[0] - offset,
                offset: wm_width + offset
                    ] = image_watermark

    return zeros_watermark

def main():
      
    slideshow_time=2000
    transaction_time=1000
    exit_key=ord('q')

    border_thickness = 20
    border_color = (88,88,88)


    width = 500
    height = 500
    files = os.listdir('./images')
    images = [load_img("./images/{}".format(i),width,height) for i in files]

    image_watermark = get_watermark('./watermarks/wm.jpg', images[0], border_thickness)

    slideshow = SlideShow(images,image_watermark, 
                    width,height, border_thickness, 
                    border_color,
                    exit_key=exit_key, 
                    slideshow_time=slideshow_time,transaction_time=transaction_time)
    
    slideshow.start()

if __name__ == "__main__":
    main()