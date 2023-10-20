import numpy as np
import cv2

folder = '27072023-1628'
width = int(3280/2464*384/62.2*360)
panorama = cv2.imread("output/panorama/"+folder+"-panorama.png")
print(panorama.shape)

def calculate_dark(image):
    for j in range(0,image.shape[1]):
        check = False
        for i in range(100,image.shape[0]-100):
            if np.array_equal(image[i,j],[0,0,0]):
                check = True
                break
        if i == image.shape[0]-101 and check == False:
            break
    left = j
    print(left)
    
    for j in range(image.shape[1]-1,image.shape[1]-100,-1):
        check = False
        for i in range(100,image.shape[0]-100):
            if np.array_equal(image[i,j],[0,0,0]):
                check = True
                break
        if i == image.shape[0]-101 and check == False:
            break
    right = j+1
    print(right)
        
    for i in range(0,100):
        check = False
        for j in range(left,right):
            if np.array_equal(image[i,j],[0,0,0]):
                check = True
                break
        if j == right-1 and check == False:
            break
    top = i  
    print(top) 

    for i in range(image.shape[0]-1,image.shape[0]-101,-1):
        check = False
        for j in range(left,right):
            if np.array_equal(image[i,j],[0,0,0]):
                break
        if j == right-1 and check == False:
            break
    bottom = i
    print(bottom)
    return image[top:bottom,left:right]

panorama = calculate_dark(panorama)
panorama = cv2.resize(panorama,(width,384),cv2.INTER_AREA)
cv2.imwrite("output/panorama/"+folder+".png",panorama)
cv2.imshow("img",panorama)
cv2.waitKey(0)