import numpy as np
from matplotlib import pyplot as plt
import cv2
import glob
import math
from pathlib import Path
import argparse
DEFAULT_INPUT_DIRECTORY = "F:/repo/point_cloud_processing/raspberryPi/input"

def search_point(args):
    # images_path = sorted(glob.glob(input_path+folder+"/*/l.jpg", recursive=True))

    distance_table = []
    with open(args.input_directory+'/'+args.folder+"/distance.txt",'r') as file:
        for line in file:
            angle,distance = line.split('-')
            distance_table.append([int(angle),float(distance)+4])
    distance_table = np.array(distance_table)
    distance_table = distance_table[distance_table[:,0].argsort()]

    panorama_i = cv2.imread(args.output_directory+'/panorama/'+args.folder+".png")
    panorama = cv2.cvtColor(panorama_i,cv2.COLOR_BGR2GRAY)

    Path(args.output_directory+'/'+args.folder).mkdir(parents=True,exist_ok=True)

    point_distance_file = open(args.output_directory+'/'+args.folder+'/distance.csv','w')
    point_distance_file.write("Angle,x,y,xp,yp,Distance\n")
    
    output_directory = Path(args.output_directory+'/'+args.folder+'/point')
    output_directory.mkdir(parents=True,exist_ok=True)

    for index,(angle,distance) in enumerate(distance_table):
        angle = int(angle)
        # if angle not in {937}:
        #     continue
        image_i = cv2.imread(args.input_directory+'/'+args.folder+"/"+str(angle)+"/l.jpg")
        image_i = cv2.resize(image_i,(511,384),interpolation = cv2.INTER_AREA)
        image = cv2.cvtColor(image_i,cv2.COLOR_BGR2GRAY)
        
        # SIFT algorithm
        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(panorama, None) 
        kp2, des2 = sift.detectAndCompute(image, None) 

        bf = cv2.BFMatcher(cv2.NORM_L1,crossCheck=True) 
        matches = bf.match(des1,des2)
        
        matches = sorted(matches, key = lambda x:x.distance) 
        
        # Coordinate of point
        xk = round(3.04/2.76*384*3.75/distance+image.shape[1]/2)
        yk = round(3.04/2.76*384*0.9/distance+image.shape[0]/2)
        
        # Average delta
        sum_x=0
        sum_y=0
        denominator = 0
        for i in range(0,20):
            x1,y1 = np.round(kp1[matches[i].queryIdx].pt)
            x2, y2 = np.round(kp2[matches[i].trainIdx].pt)
            dx = x1-x2 if x1-x2>0 else panorama.shape[1]+x1-x2
            dy = y1-y2 
            if i<5 or (abs(dx-delta_x)<30 and abs(y1-y2-delta_y)<15):
                sum_x+=dx/matches[i].distance
                sum_y+=(y1-y2)/matches[i].distance
                denominator+=abs(1/matches[i].distance)
                delta_x = sum_x/denominator
                delta_y = sum_y/denominator
                # print(i,y1,y2,x1,x2,dx,y1-y2,delta_x,delta_y)
        delta_x = round(sum_x/denominator)
        delta_y = round(sum_y/denominator)
        # print(delta_x,delta_y)
        
        
        dmin = 1e+10
        index=0
        for i in range(0,int(len(matches))):
            x1,y1 = np.round(kp1[matches[i].queryIdx].pt)
            x2, y2 = np.round(kp2[matches[i].trainIdx].pt)
            dx = x1-x2 if x1-x2>0 else panorama.shape[1]+x1-x2
            d = math.sqrt(math.pow(x2-xk,2)+math.pow(y2-yk,2))
            if d<dmin and abs(dx-delta_x)<50 and abs(y1-y2-delta_y)<20:
                dmin = d
                index = i
        x1,y1 = np.round(kp1[matches[index].queryIdx].pt)
        x2, y2 = np.round(kp2[matches[index].trainIdx].pt)
        dx_min = int(x1-x2 if x1-x2>0 else panorama.shape[1]+x1-x2)
        dy_min = int(y1-y2)
        # print(index,y1,y2,x1,y2,dx_min,dy_min)
        
        xk_panorama = xk+dx_min if xk+dx_min<panorama.shape[1] else xk+dx_min-panorama.shape[1]
        yk_panorama = yk+dy_min
        
        print(angle,distance)
        point_distance_file.write("{},{},{},{},{},{}\n".format(angle,xk,yk,xk_panorama,yk_panorama,distance))
        
        if dx_min<panorama.shape[1]-image.shape[1]:
            img_new = panorama_i[:,dx_min:dx_min+image.shape[1]].copy()
        else:
            img_new = np.zeros((panorama.shape[0],image.shape[1],3)).astype(np.uint8)
            img_new[:,:panorama.shape[1]-dx_min] = panorama_i[:,dx_min:]
            img_new[:,panorama.shape[1]-dx_min:] = panorama_i[:,:image.shape[1]-panorama.shape[1]+dx_min]
        
        # draw circle
        cv2.circle(img_new, (xk,yk+dy_min), 5, (0, 0, 255), thickness=2)
        cv2.circle(image_i, (xk,yk), 5, (0, 0, 255), thickness=2)
        
        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(1, 2, 1)
        ax.imshow(cv2.cvtColor(image_i, cv2.COLOR_BGR2RGB))
        ax.set_title(str(angle)+' original',fontsize=10)
        
        ax = fig.add_subplot(1, 2, 2)
        ax.imshow(cv2.cvtColor(img_new, cv2.COLOR_BGR2RGB))
        ax.set_title(str(angle)+' panorama',fontsize=10)
        
        fig.tight_layout()
        fig.savefig(f'{args.output_directory}/{args.folder}/point/{angle}.png')
        # plt.show()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input_directory', help="directory to input images", default=DEFAULT_INPUT_DIRECTORY)
    # parser.add_argument('-i','--input_directory', help="directory to input images", default="input")

    parser.add_argument('-f','--folder', help="folder of input images", default="00000000-1628")
    parser.add_argument('-o','--output_directory', help="directory to input images", default="output")
    args = parser.parse_args()
    search_point(args) 