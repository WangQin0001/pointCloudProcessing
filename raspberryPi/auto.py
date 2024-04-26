import subprocess
import time
import logging
from pathlib import Path
from API_controll import SSH_local
import os

# 获取main.py文件的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(script_dir, "input/")

# 常量和配置
BASE_DIR = Path("F:/repo/point_cloud_processing/3D-Model-Monocular-Vision-main")
LOG_FILE = BASE_DIR.parent / "raspberryPi" / "app.log"
SCRIPTS = {
    "match_images": "match_images.py",
    "sanity_panorama": "sanity_panorama.py",
    "search_point_in_panorama": "search_point_in_panorama.py",
    "solve_param_each_part": "solve_param_each_part.py",
    "match_difference": "match_difference.py",
    "calib_pcd_panorama": "calib_pcd_panorama.py",
    # "denoise": "denoise.py",
}

# 日志配置
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def run_command(script_name, step_number, **kwargs):
    print(f"STEP {step_number} STARTED: {script_name}", flush=True)
    cmd = ["python", str(BASE_DIR / SCRIPTS[script_name])]
    for key, value in kwargs.items():
        cmd.extend([f"-{key}", value])
    try:
        logging.info(f"Executing command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd, check=True, cwd=BASE_DIR, capture_output=True, text=True
        )
        logging.info(f"Command output: {result.stdout}")
        if result.stderr:
            logging.error(f"Command error: {result.stderr}")
        print(f"STEP {step_number} COMPLETED: {script_name}", flush=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(
            f"Command execution failed: {cmd}, Error: {str(e)}, Output: {e.stderr}"
        )
        print(f"Command failed with error: {e}")
        return False


def main():
    file = call_capture_image_full()  # 从这个函数获取 file 和 file_path
    # print("STEP 1 STARTED", flush=True)
    # # file = "23042024-1731"  # For example purposes
    # logging.info(f"get full image: {file}")
    # print("STEP 1 COMPLETED", flush=True)
    operations = [
        ("match_images", 2, {"f": file}),
        ("sanity_panorama", 3, {"f": file}),
        ("search_point_in_panorama", 4, {"f": file}),
        ("solve_param_each_part", 5, {"f": file}),
        ("match_difference", 6, {"f": file}),
        ("calib_pcd_panorama", 7, {"f": file}),
        # ("denoise", 8, {"file_path": file}),
    ]
    for script, step, params in operations:
        run_command(script, step, **params)


def call_capture_image_full():
    print("STEP 1 STARTED: capture_image_full", flush=True)
    # SSH Connection Parameters
    host = "192.168.1.81"
    username = "root"
    password = "root"
    path = "/media/Program"
    run_file = "auto"
    try:
        SSH = SSH_local(host, username, password, path, run_file)
        SSH.connect()
        SSH.compile(
            "stereoPi_new.cpp source/lidarlite_v3.cpp source/GPIO.cpp source/UART.cpp",
            "-I .",
        )
        step = 5
        dir = 1
        angle = 360

        file = SSH.capture_image_full(step, dir, angle, INPUT_DIR)
        SSH.ssh.close()
        print("STEP 1 COMPLETED: capture_image_full", flush=True)
        return file
    except Exception as e:
        print(f"Cannot connect to the hardware or perform the operation: {e}")
        return None


if __name__ == "__main__":
    main()
