import cv2
import numpy as np
import glob
import argparse
  
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

def match_image(args):
    images_path = sorted(glob.glob(args.input_directory+'/'+args.folder+"/*/l.jpg", recursive=True))
    
    angle_list =[]
    for path_elem in images_path:
        print("正在从以下路径读取图片：",path_elem)
        angle = path_elem.split('\\')[-2]
        if not angle.isnumeric():
            angle = path_elem.split('/')[-2]
        angle_list.append(int(angle))
    angle_list.sort()

    image_list = []
    for i in angle_list:
        image_path = args.input_directory + "/" + args.folder + '/' + str(i) + "/l.jpg"
        image = cv2.imread(image_path)
        if image is None:
            print("Failed to load image:", image_path)
        else:
            print("Loaded image:", image_path)

        image = cv2.imread(args.input_directory+"/"+args.folder+'/'+str(i)+"/l.jpg")
        image = cv2.resize(image,(512,384),interpolation = cv2.INTER_AREA)
        image_list.append(image)
    print("Starting match "+str(len(angle_list))+" images")
    stitcher = cv2.Stitcher.create()
    status,result = stitcher.stitch(image_list)
    if (status == cv2.STITCHER_OK):
        cv2.imwrite(args.output_directory+'/'+args.folder+"-original.png",result)        
        panorama = calculate_dark(result)
        width = int(3280/2464*384/62.2*360)
        panorama = cv2.resize(panorama,(width,384),cv2.INTER_AREA)
        
        cv2.imwrite(args.output_directory+'/'+args.folder+".png",panorama)
        # cv2.imshow("img",panorama)
        cv2.waitKey(0)
    else:
        print("False")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input_directory', help="directory to input images", default="input")
    parser.add_argument('-f','--folder', help="folder of input images", default="09112023-1407")
    parser.add_argument('-o','--output_directory', help="directory to input images", default="output/panorama")

    args = parser.parse_args()
    print("Received arguments:", args)
    match_image(args)