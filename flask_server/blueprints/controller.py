from flask import Blueprint,request,jsonify,session
bp = Blueprint("controller",__name__,url_prefix="/controller")
# bp = Blueprint("api",__name__,url_prefix="/api")

from .API_controll import SSH_local

host = '192.168.1.75'
username = 'root'
password = 'root'
# path - path of file program in the 3D scanner (in StereoPi)
path = '/media/Program'
# localpath - path of saving result in personal computer
localpath = 'E:/Python/ZoeDepth/input/'
# run_file_name - name of exe file after compiling cpp files (Don't need to change)
run_file_name = 'main'

SSH = SSH_local(host,username,password,path,run_file_name)

SSH.connect()

SSH.compile("stereoPi_new.cpp source/lidarlite_v3.cpp source/GPIO.cpp source/UART.cpp","-I .")

offset = SSH.read_angle()
print("Offset angle: "+str(offset*360/1024))

@bp.route('/offsetPosition',methods=['GET'])
def offsetPosition():
    # session.clear()
    # SSH.go_to_offset_angle(offset)
    print("offsetPosition")
    return jsonify({"code": 200, "message": "offsetPosition success", "data": None})





@bp.route('/captureCurrentImage')
def captureCurrentImage():
    try:
        SSH.capture_single_image(localpath)
    except:
        print("cant connect the host")
    return jsonify({"code": 200, "message": "captureCurrentImage success", "data": None})

@bp.route('/captureSurroundingImage')
def captureSurroundingImage():
    step = SSH.choose_step()
    dir = SSH.choose_direction()
    angle = SSH.choose_angle()
    SSH.capture_image_full(step, dir, angle, localpath)
    return jsonify({"code": 200, "message": "captureSurroundingImage success", "data": None})

@bp.route('/manualRotate')
def manualRotate():
    SSH.rotate_platform()
    return jsonify({"code": 200, "message": "ManualRotate success", "data": None})

SSH.ssh.close()