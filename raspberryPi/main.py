import sys
import io
import json
import os
from API_controll import SSH_local

# 设置全局变量 FILENAME
# 获取main.py文件的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
# At the start of your script, where you define FILENAME
INPUT_DIR = os.path.join(script_dir, "input/")

# 构建offset_angle.json文件的绝对路径，并设置为全局变量
FILENAME = os.path.join(script_dir, "offsetValues", "offset_angle.json")


def get_offset_data():
    try:
        with open(FILENAME, "r") as file:
            data = json.load(file)
            return data.get("offset_angle"), data.get("is_offset_angle_saved", False)
    except FileNotFoundError:
        return None, False


def save_offset_angle(angle):
    data = {"offset_angle": angle, "is_offset_angle_saved": True}
    with open(FILENAME, "w") as file:
        json.dump(data, file)


def initialize_and_save_offset(host, username, password, path, run_file_name):
    SSH = SSH_local(host, username, password, path, run_file_name)
    SSH.connect()
    offset = SSH.read_angle()
    print("Current Offset angle: " + str(offset * 360 / 1024))

    _, is_saved = get_offset_data()
    if not is_saved:
        save_offset_angle(offset)
        print("Offset angle saved.")
    else:
        print("Offset angle has already been saved.")
    SSH.ssh.close()


def main(operation, step=None, dir=None, angle=None):
    print("The operation number is: " + operation)

    host = "192.168.1.81"
    username = "root"
    password = "root"
    path = "/media/Program"
    run_file_name = "main"

    try:
        SSH = SSH_local(host, username, password, path, run_file_name)
        SSH.connect()
        SSH.compile(
            "stereoPi_new.cpp source/lidarlite_v3.cpp source/GPIO.cpp source/UART.cpp",
            "-I .",
        )
        if operation == "0":
            pass
        elif operation == "1":
            saved_offset_angle, _ = get_offset_data()
            if saved_offset_angle is not None:
                print("Main function received offset: " + str(saved_offset_angle))
                SSH.go_to_offset_angle(saved_offset_angle)
            else:
                print("No saved offset angle available")
        elif operation == "2":
            print("INPUT_DIR2" + INPUT_DIR)
            SSH.capture_single_image(INPUT_DIR)
        elif operation == "3":
            if step is None or dir is None or angle is None:
                print("Error: Missing arguments for operation 3")
                return
            print("INPUT_DIR3" + INPUT_DIR)
            SSH.capture_image_full(step, dir, angle, INPUT_DIR)
        elif operation == "4":
            if angle is None or dir is None:
                print("Error: Missing arguments for operation 4")
                return
            SSH.rotate_platform(angle, dir)

        else:
            print("Invalid operation")

        SSH.ssh.close()
    except Exception as e:
        print(f"Cannot connect to the hardware or perform the operation: {e}")


if __name__ == "__main__":
    args = sys.argv[1:]
    operation = args[0] if len(args) > 0 else None
    step = int(args[1]) if len(args) > 1 and args[1] else None
    dir = int(args[2]) if len(args) > 2 and args[2] else None
    angle = int(args[3]) if len(args) > 3 and args[3] else None

    initialize_and_save_offset("192.168.1.81", "root", "root", "/media/Program", "main")

    if operation:
        main(operation, step, dir, angle)
    else:
        print("No operation provided")
