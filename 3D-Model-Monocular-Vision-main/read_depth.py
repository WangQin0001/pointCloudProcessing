import cv2
import numpy as np
from matplotlib import pyplot as plt
import glob 
from pathlib import Path
import matplotlib.cm as cm
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import argparse

def draw_depth(args):
    path = f"{args.inout_directory}/{args.folder}/{args.shift}/{args.depth_folder}"
    depth_path = sorted(glob.glob(path+"/*.npy", recursive=True))  
    depths=[]
    for path_elem in depth_path:
        depth = np.load(path_elem)   
        if depths == []:
            depths = depth
        else:
            depths = np.concatenate((depths,depth),axis=1)     
        try:
            file_stem = path_elem.split('\\')[-1]
        except:
            file_stem = path_elem.split('/')[-1]
            pass
        file_stem = file_stem[:-4]
        
        plt.imsave(path+"/gray.png",depth,cmap='gray')
        image_gray = cv2.imread(path+'/gray.png',cv2.IMREAD_GRAYSCALE)
        
        # print(np.unravel_index(np.argmin(image_gray),image_gray.shape))
        fig = plt.figure()
        ax = fig.add_subplot()
        # ax.set_title(file_stem)
        ax.imshow(depth,cmap='jet_r')
        divider = make_axes_locatable(ax)
        norm_color = plt.Normalize(vmin=0,vmax=255) 
        print(depth.min(),depth.max(),depth.min(),depth.max(),image_gray.min(),image_gray.max())
        cmap = colors.ListedColormap(cm.jet(norm_color(np.linspace(image_gray.min(), image_gray.max(), 256))))
        cmap = cmap.reversed()       
        # v = np.linspace(dis.min(), dis.max(), 20, endpoint=True)
        # plt.contourf(depth,v,cmap = cmap)
        norm_range = plt.Normalize(vmin=depth.min(),vmax=depth.max()) 
        sm = cm.ScalarMappable(cmap=cmap,norm=norm_range)
        cbar = plt.colorbar(sm,cax=ax.inset_axes((0.02,0.125,0.03,0.75)))
        cbar.locator = plt.MaxNLocator(nbins=20)
        cbar.update_ticks()
        ax.axis('off')  
        fig.savefig(path+"/"+file_stem+'_d.png',bbox_inches='tight',pad_inches=0)
        plt.imsave(path+"/"+file_stem+'_dn.png',depth,cmap='jet_r')
        # fig.tight_layout()
        plt.show()
        plt.close()
    plt.imshow(depths,cmap='jet_r')
    plt.show()
    plt.imsave(path+"/"+file_stem+'_all.png',depths,cmap='jet_r')
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-io','--inout_directory', help="directory to images", default="output")
    parser.add_argument('-f','--folder', help="folder of input images", default="00000000-1628")
    parser.add_argument('-df','--depth_folder', help="folder of depth", default="match_diff")
    parser.add_argument('-s','--shift', help="shift of input images", default="170")
    parser.add_argument('-d','--divide', help="divide coefficent of input images", default="6")
    
    args = parser.parse_args()
    draw_depth(args)

