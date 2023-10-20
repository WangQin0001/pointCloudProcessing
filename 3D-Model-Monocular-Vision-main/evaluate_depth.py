import numpy as np
from matplotlib import pyplot as plt
import cv2
import glob
import math
from pathlib import Path
import pandas as pd
import argparse

def solve_paras(args):
    depths = []
    for index in range(int(args.divide)):
        # depth = np.load("output/{0}/{2}/match_diff/{0}-depth-{1}-{2}.npy".format(folder,index,shift))
        depth = np.load("{0}/{1}/{3}/{4}/{1}-depth-{2}-{3}.npy".format(args.inout_directory,args.folder,index,args.shift,args.depth_folder))
        depths.append(depth)
    width = sum(depths[i].shape[1] for i in range(int(args.divide)))
    # print(width)

    data=[]
    point_distance_file = pd.read_csv(args.inout_directory+'/'+args.folder+'/distance.csv')
    # print(point_distance_file)
    for _,row in point_distance_file.iterrows():
        # if int(row['Angle']) in {164,736,322}:
        #     continue
        x_delta = row['xp']-int(args.shift) if row['xp']-int(args.shift)>=0 else row['xp']-int(args.shift)+width
        part_number = int(x_delta/(width/int(args.divide)))
        col_part = int(x_delta-part_number*width/int(args.divide))
        depth_in_map = row['Distance']/100*math.cos(math.atan(
            (col_part-depths[index].shape[1]/2)/(depths[index].shape[1]/2)*math.tan(math.pi/int(args.divide))))
        # if not (int(row['Angle']) > 513 or int(row['Angle']) <38):
        print(row['Angle'],row['xp'],depths[part_number][int(row['yp']),col_part],depth_in_map)
        data.append([depths[part_number][int(row['yp']),col_part],depth_in_map])
        
    data = np.array(data)
    data = data[data[:,0].argsort()]
    coeff = np.polyfit(data[:,0],data[:,1],1)
    print(coeff)
    y_new = np.polyval(coeff,data[:,0])
    dis = abs(y_new - data[:,1])
    delta = abs(data[:,0]-data[:,1])
    delta_ab = delta/data[:,1]


    # print(dis)
    # print(data[:,1]-data[:,0])
    # print(y_new-data[:,0])
    print(delta.mean(),delta.max(),delta.min())
    print(delta_ab.mean(),delta_ab.max(),delta_ab.min())    
    print(dis.mean(),dis.max(),dis.min())
    # plt.scatter(data[0],abs(data[1]-data[0]))
    # plt.scatter(data[0],abs(y_new-data[0]))
    plt.scatter(data[:,0],data[:,1])
    plt.plot(data[:,0],y_new)
    plt.xlabel('Predict depth (m)')
    plt.ylabel('Measured depth (m)')
    plt.show()
       

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-io','--inout_directory', help="directory to images", default="output")
    parser.add_argument('-f','--folder', help="folder of input images", default="27072023-1628")
    parser.add_argument('-df','--depth_folder', help="folder of depth", default="match_diff")
    parser.add_argument('-s','--shift', help="shift of input images", default="170")
    parser.add_argument('-d','--divide', help="divide coefficent of input images", default="6")
    
    args = parser.parse_args()
    solve_paras(args)