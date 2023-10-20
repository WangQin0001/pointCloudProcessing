import sys
import io
import json
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 指定编码格式，避免乱码

from API_controll import SSH_local


def save_offset_angle(angle, filename='F:/OneDrive/100_work/repo/point_cloud_processing/raspberryPi/offsetValues/offset_angle.json'):
    with open(filename, 'w') as file:
        json.dump({'offset_angle': angle}, file)

# 这里os报错unreseloved reference os怎么回事？
def get_saved_offset_angle(filename='F:/OneDrive/100_work/repo/point_cloud_processing/raspberryPi/offsetValues/offset_angle.json'):
    if not os.path.exists(filename):
        return None  # 如果文件不存在，返回None
    with open(filename, 'r') as file:
        data = json.load(file)
        return data.get('offset_angle')  # 如果键不存在，则返回None

def initialize_and_save_offset(host, username, password, path, run_file_name):
    SSH = SSH_local(host, username, password, path, run_file_name)
    SSH.connect()
    # 可能还需要其他设置或初始化操作
    offset = SSH.read_angle()
    print("Current Offset angle: " + str(offset * 360 / 1024))
    save_offset_angle(offset)  # 保存当前Offset angle
    SSH.ssh.close()


def main(operation, step=None, dir=None, angle=None):
    print("the operation number is: " + operation)

    host = '192.168.1.75'
    username = 'root'
    password = 'root'
    path = '/media/Program'
    localpath = 'F:/OneDrive/100_work/repo/point_cloud_processing/raspberryPi/input/'
    run_file_name = 'main'

    try:
        SSH = SSH_local(host, username, password, path, run_file_name)

        SSH.connect()
        SSH.compile("stereoPi_new.cpp source/lidarlite_v3.cpp source/GPIO.cpp source/UART.cpp", "-I .")

        if operation == '0':
            pass  # 什么也不做，直接退出
        elif operation == '1':
            saved_offset_angle = get_saved_offset_angle()
            print("offset角度是：" + str(saved_offset_angle))

            if saved_offset_angle is not None:
                print("the offset angle: " + str(saved_offset_angle))
                SSH.go_to_offset_angle(saved_offset_angle)
            else:
                print("No saved offset angle available")
        elif operation == '2':
            SSH.capture_single_image(localpath)
        elif operation == '3':
            if step is None or dir is None or angle is None:
                print("Error: Missing arguments for operation 3")
                return
            SSH.capture_image_full(step, dir, angle, localpath)
        elif operation == '4':
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
    initialize_and_save_offset('192.168.1.75', 'root', 'root', '/media/Program', 'main')#先初始化和保存现在的offset

    args = sys.argv[1:]  # 获取除第一个元素（脚本名）之外的所有命令行参数
    operation = args[0] if len(args) > 0 else None

    # 将字符串参数转换为整数，如果它们存在且不为空
    step = int(args[1]) if len(args) > 1 and args[1] else None
    dir = int(args[2]) if len(args) > 2 and args[2] else None
    angle = int(args[3]) if len(args) > 3 and args[3] else None

    print("methodName: " + str(operation), "step: " + str(step), "dir: " + str(dir), "angle: " + str(angle))

    if operation:
        main(operation, step, dir, angle)
    else:
        print("No operation provided")
