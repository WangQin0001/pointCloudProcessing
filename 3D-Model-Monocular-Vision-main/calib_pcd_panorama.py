import os
import subprocess

import cv2
import numpy as np
import math
from pathlib import Path
import open3d as o3d
from scipy import ndimage
import argparse

# Compute edge magnitudes
def edges(d):
    dx = ndimage.sobel(d, 0)  # horizontal derivative
    dy = ndimage.sobel(d, 1)  # vertical derivative
    return np.abs(dx) + np.abs(dy)

def worldCoords(width, height,fx,fy):
    cx, cy = width / 2, height / 2
    xx, yy = np.tile(range(width),(height,1)), np.tile(range(height),(width,1)).T
    xx = (xx - cx) / fx
    yy = (yy - cy) / fy
    return xx, yy

def calib_pcd(args):
    output_directory = args.inout_directory+'/'+args.folder+'/'+args.shift+'/point-cloud'
    Path(output_directory).mkdir(parents=True,exist_ok=True)
    pcd_all = o3d.geometry.PointCloud()
    for index in range(int(args.divide)):
        depth = np.load("{0}/{1}/{3}/{4}/{1}-depth-{2}-{3}.npy".format(args.inout_directory,args.folder,index,args.shift,args.depth_folder))
        img = cv2.imread("{0}/{1}/{3}/img/{1}-{2}-{3}.png".format(args.inout_directory,args.folder,index,args.shift))

        height, width = depth.shape[:2]
        focal = 3.04/2.76*384
        
        xx,yy = worldCoords(width,height,focal,focal)
        # print(xx.shape,yy.shape)

        # depth[edges(depth) > 0.3] = 1e6  # Hide depth edges
        points_3D = np.stack((xx * depth, yy * depth, depth),axis=2).reshape(-1,3)
        print(points_3D.shape)

        # Remove INF values from point cloud
        points_3D[points_3D == float('+inf')] = 0
        points_3D[points_3D == float('-inf')] = 0

        # Mask colors and points
        colors = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).reshape(-1,3)

        delta = 2*math.pi*(index/int(args.divide)+int(args.shift)/(int(args.divide)*width))
        Q = [[np.cos(delta),0,np.sin(delta)],
            [0,1,0],
            [-np.sin(delta),0,np.cos(delta)]]
        points_3D = np.dot(Q,points_3D.T).T
        
        # Get rid of points with value 0 (i.e no depth)
        mask_map =depth.flatten() > depth.flatten().min()
        
        output_points = points_3D[mask_map]
        output_colors = colors[mask_map].astype(np.float64)/255
        
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(output_points.reshape(-1,3))
        pcd.colors = o3d.utility.Vector3dVector(output_colors.reshape(-1,3))
        o3d.io.write_point_cloud(output_directory+'/{0}-{1}-{2}.pcd'.format(args.folder,index,args.shift),pcd)
        pcd_all+=pcd

    o3d.io.write_point_cloud(output_directory+'/{0}-{1}.pcd'.format(args.folder,args.shift), pcd_all)
    return os.path.abspath(output_directory)# 返回这个目录路径
    # o3d.visualization.draw_geometries([pcd_all],window_name="PointCloud")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-io','--inout_directory', help="directory to images", default="output")
    parser.add_argument('-f','--folder', help="folder of input images", default="00000000-1628")
    parser.add_argument('-df','--depth_folder', help="folder of depth", default="calib_param")
    parser.add_argument('-s','--shift', help="shift of input images", default="170")
    parser.add_argument('-d','--divide', help="divide coefficent of input images", default="6")

    args = parser.parse_args()
    output_directory = calib_pcd(args)  # 接收返回的目录路径

    # 生成的文件的完整路径
    output_file_path = os.path.join(output_directory, f'{args.folder}-{args.shift}.pcd')
    # 确保文件存在
    if os.path.exists(output_file_path):
        # 正确的命令应该是 explorer.exe /select,"完整路径"
        subprocess.run(f'explorer /select,"{output_file_path}"', shell=True)
    else:
        print(f'File not found: {output_file_path}')