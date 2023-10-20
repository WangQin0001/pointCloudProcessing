import numpy as np
from matplotlib import pyplot as plt
import cv2
import glob
import math
from pathlib import Path

input_path = "input/"
folder = "25072023-1610"


with open(input_path+folder+"/distance.txt",'r') as file:
    for line in file:
        angle,distance = line.split('-')
        
        image = cv2.imread(input_path+folder+"/"+str(angle)+"/l.jpg")
        image = cv2.resize(image,(511,384),interpolation = cv2.INTER_AREA)
        
        xk = round(3.04/2.76*384*3.75/float(distance)+image.shape[1]/2)
        yk = round(3.04/2.76*384*0.9/float(distance)+image.shape[0]/2)

        # draw circle
        cv2.circle(image, (xk,yk), 5, (0, 0, 255), thickness=2)

        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.show()