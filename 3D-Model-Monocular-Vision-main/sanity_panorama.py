import numpy as np
from torchvision.transforms import ToTensor
from PIL import Image
from zoedepth.utils.misc import get_image_from_url, colorize
import torch

import argparse
from tqdm import tqdm
from pathlib import Path
import glob

from zoedepth.models.builder import build_model
from zoedepth.utils.config import get_config

from pprint import pprint

from matplotlib import pyplot as plt

def sanity(args):
    torch.hub._validate_not_a_forked_repo=lambda a,b,c: True
    torch.hub.help("intel-isl/MiDaS", args.model_midas, force_reload=True) 
    # torch.hub.help("intel-isl/MiDaS", "DPT_Large", force_reload=True) 

    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    # DEVICE = "cpu"
    if DEVICE == "cpu":
        print("WARNING: Running on CPU. This will be slow. Check your CUDA installation.")

    print("*" * 20 + " Testing zoedepth " + "*" * 20)
    conf = get_config("zoedepth", "infer")

    print("Config:")
    pprint(conf)

    model = build_model(conf).to(DEVICE)
    model.eval()
       
    print("-"*20 + " Processing indoor scene " + "-"*20)
    
    # print(folder_name)
    
    with torch.no_grad():
        panorama = Image.open(args.input_directory+'/'+args.folder+'.png').convert("RGB")
        width, height = panorama.size
        # print(panorama.size)
        
        new_output_img = args.output_directory+"/"+args.folder+'/'+args.shift+'/'+'img'
        new_output_depth = args.output_directory+"/"+args.folder+'/'+args.shift+'/'+'first_depth'
        Path(new_output_img).mkdir(parents=True,exist_ok=True)    
        Path(new_output_depth).mkdir(parents=True,exist_ok=True)
        
        # print(f"Found {len(images_path)} images. Saving files to {output_directory}/")
        depths = []
        for index in tqdm(range(int(args.divide))):
            left = int(index*width/int(args.divide))+int(args.shift)
            right = int((index+1)*width/int(args.divide))+int(args.shift)
            if right<=width:
                img = panorama.crop((left,0,right,height))
            else:
                imgr = panorama.crop((left,0,width,height))
                imgl = panorama.crop((0,0,int(args.shift),height))
                img = Image.new("RGB",(right-left,height))
                img.paste(imgr,(0,0))
                img.paste(imgl,(width-left,0))
            # print(img.size)
            # img = image.resize((512,384),Image.LANCZOS)
            # print("???")
            file_stem = "/"+args.folder+"-depth-"+str(index)   
            # print(file_stem)         
            X = ToTensor()(img)
            X = X.unsqueeze(0).to(DEVICE)
            # print("start")
            depth = model.infer(X).cpu().numpy().squeeze()
            # print("done")
            if len(depths) == 0:
                depths = depth
            else:
                depths = np.concatenate((depths,depth),axis=1)
            img.save(new_output_img +"/"+ args.folder+"-"+str(index)+"-"+str(int(args.shift))+".png")
            np.save(new_output_depth + file_stem +"-"+str(int(args.shift))+ ".npy", depth)
            plt.imsave(new_output_img + file_stem +"-"+str(int(args.shift))+".png", depth, cmap='jet_r')
            # plt.imshow(depth,cmap="jet_r")
        np.save(new_output_depth + "/"+args.folder+"-depth-"+str(int(args.shift))+".npy", depths)
        plt.imsave(new_output_img + "/"+args.folder+"-depth-"+str(int(args.shift))+".png", depths, cmap='jet_r')
        # plt.imshow(depths,cmap="jet_r")
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--model_midas', help="midas model", default="DPT_BEiT_L_384")
    # parser.add_argument('-i','--input_directory', help="directory to input images", default="input/12052023-1348/*/l.jpg")
    parser.add_argument('-i','--input_directory', help="directory to input images", default="output/panorama")
    parser.add_argument('-f','--folder', help="folder of input images", default="27072023-1628")
    parser.add_argument('-o','--output_directory', help="directory to save output", default="output")
    parser.add_argument('-s','--shift', help="shift of input images", default="170")
    parser.add_argument('-d','--divide', help="divide coefficent of input images", default="6")
    
    args = parser.parse_args()
    sanity(args)       
