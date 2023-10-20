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
    torch.hub.help("intel-isl/MiDaS", args.model_midas, force_reload=True) 
    # torch.hub.help("intel-isl/MiDaS", "DPT_Large", force_reload=True) 

    # DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    DEVICE = "cpu"
    if DEVICE == "cpu":
        print("WARNING: Running on CPU. This will be slow. Check your CUDA installation.")
    print("*" * 20 + " Testing zoedepth " + "*" * 20)
    conf = get_config("zoedepth", "infer")
    print("Config:")
    pprint(conf)
    model = build_model(conf).to(DEVICE)
    model.eval()
       
    print("-"*20 + " Testing on an indoor scene from url " + "-"*20)
    
    try:
        folder_path = args.input_directory.split('/')[-3]
    except:
        folder_path = args.input_directory.split('\\')[-3]
        pass
    output_directory = Path(args.output_directory+"/single/"+folder_path)
    output_directory.mkdir(parents=True,exist_ok=True)

    with torch.no_grad():
        images_path = sorted(glob.glob(args.input_directory, recursive=True))        
        print(f"Found {len(images_path)} images. Saving files to {output_directory}/")
        for image_path in tqdm(images_path):
            img = Image.open(image_path).convert("RGB")
            img = img.resize((512,384),Image.LANCZOS)
            
            try:
                file_stem = image_path.split('\\')[-2]
            except:
                file_stem = image_path.split('/')[-2]
                pass
            # print(file_stem)
            
            # orig_size = img.size
            X = ToTensor()(img)
            X = X.unsqueeze(0).to(DEVICE)
            out = model.infer(X).cpu()            
            np.save(output_directory / f"{file_stem}.npy", out.numpy().squeeze())
            plt.imsave(output_directory / f"{file_stem}.png", out.numpy().squeeze(), cmap='jet_r')
            # or just, 
            # out = model.infer_pil(img)
            
            # pred = Image.fromarray(colorize(out))
            # # Stack img and pred side by side for comparison and save
            # pred = pred.resize(orig_size, Image.ANTIALIAS)
            # stacked = Image.new("RGB", (orig_size[0]*2, orig_size[1]))
            # stacked.paste(img, (0, 0))
            # stacked.paste(pred, (orig_size[0], 0))
            # stacked.save("pred.png")
            # print("saved pred.png")
            # model.infer_pil(img, output_type="pil").save("pred_raw.png")
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--model_midas', help="midas model", default="DPT_BEiT_L_384")
    parser.add_argument('-i','--input_directory', help="directory to input images", default="input/27072023-1628/*/l.jpg")
    parser.add_argument('-o','--output_directory', help="directory to save output", default="output")

    args = parser.parse_args()
    sanity(args)       