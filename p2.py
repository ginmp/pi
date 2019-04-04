import cv2
import os
import numpy as np

class Rectangle():
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y

    def __repr__(self):
        return "\t x:{} \t y:{} \n".format(self.__x, self.__y)
    
    def __str__(self):
        return self.__repr__()

def get_all_rectangles(data, kernel):
    rectangles = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if i <= data.shape[0] - kernel.shape[0]:
                i_final = i + kernel.shape[0]
            else:
                i_final = 0
            if j <= data.shape[1] - kernel.shape[1]:
                j_final = j + kernel.shape[1]
            else:
                j_final = 0
            
            if i_final == 0 or j_final == 0:
                break
            mult = data[i:i_final, j:j_final] * kernel
            mean = np.mean(mult)

            if mean == 1.0:
                x = [i,i_final]
                y = [j,j_final]
                rectangles.append(Rectangle(x , y))
    return rectangles

def collision(values0, values1):
    for v0 in range(values0[0], values0[1]):
            if v0 in range(values1[0], values1[1]):
                return True
    return False

def get_unique_rectangles(rectangles):
    unique_rectangles = []
    for rect0 in rectangles:
        col = False
        for rect1 in unique_rectangles:
            x0inx1 = collision(rect0.get_x(), rect1.get_x())
            y0iny1 = collision(rect0.get_y(), rect1.get_y())

            col = x0inx1 and y0iny1

            if col:
                break        

        if not col:
            unique_rectangles.append(rect0)
    return unique_rectangles

def show(data, unique_rectangles, width=500, height=500):
    if len(unique_rectangles) == 0:
        print("quadrados nao encontrados")
        exit()
    
    print(unique_rectangles)
    print("%d" % len(unique_rectangles))

    img = cv2.resize(data, (width, height))
    img = img * 255
    cv2.imshow('data',img)

    color = 255
    color_step = color // len(unique_rectangles)

    rectangles_data = data.copy()
    for rect in unique_rectangles:
        x0,x1 = rect.get_x()
        y0,y1 = rect.get_y()
        rectangles_data[x0:x1, y0:y1] = rectangles_data[x0:x1, y0:y1] * color
        color -= color_step

    img = cv2.resize(rectangles_data, (width, height))
    cv2.imshow('found',img)

    cv2.waitKey()
    cv2.destroyAllWindows()

def get_data(x,y, kx,ky, new_data=True):

    kernel_shape = (kx,ky)
    kernel = np.ones(shape=kernel_shape)

    if new_data:         
        from random import randint
        
        data_shape = (x,y)
        TOTAL_PIXELS = x * y

        O = randint(TOTAL_PIXELS//2, TOTAL_PIXELS)
        Z = TOTAL_PIXELS - O
        data = np.array([0] * Z + [1] * O, dtype = np.uint8)
        np.random.shuffle(data)

        data = data.reshape(data_shape)

    else:
        data = np.array([
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1, 0, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 0]
        ], dtype = np.uint8
        )
    
    return data, kernel

def main():
    # dimensoes da nova imagem
    x, y = 100, 100
    
    # dimensoes da kernel
    kx, ky = 3, 3

    # True para gerar uma nova imagem
    new_data = False

    # dimensoes da imagem de exibicao
    width, height = 500, 500

    data,kernel = get_data(x,y, kx,ky, new_data)
    rectangles = get_all_rectangles(data,kernel)
    unique_rectangles = get_unique_rectangles(rectangles)
    show(data,unique_rectangles, width, height)

if __name__ == "__main__":
    main()
