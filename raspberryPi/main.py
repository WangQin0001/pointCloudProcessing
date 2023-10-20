import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')#指定编码格式，避免乱码

from API_controll import SSH_local


def main(operation):
    print("现在传给pyton的操作是: " + operation)

    host = '192.168.1.75'
    username = 'root'
    password = 'root'
    path = '/media/Program'
    localpath = 'E:/Python/ZoeDepth/input/'
    run_file_name = 'main'

    try:
        SSH = SSH_local(host, username, password, path, run_file_name)

        SSH.connect()
        SSH.compile("stereoPi_new.cpp source/lidarlite_v3.cpp source/GPIO.cpp source/UART.cpp", "-I .")

        offset = SSH.read_angle()
        print("Offset angle: " + str(offset*360/1024))

        if operation == '0':
            pass  # 什么也不做，直接退出
        elif operation == '1':
            print("测试2")
            SSH.go_to_offset_angle(offset)
        elif operation == '2':
            SSH.capture_single_image(localpath)
        elif operation == '3':
            SSH.capture_image_full(localpath)
        elif operation == '4':
            SSH.rotate_platform()
        else:
            print("Invalid operation")

        SSH.ssh.close()
    except Exception as e:
        print(f"无法连接到硬件或执行硬件相关操作: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("No operation provided")
