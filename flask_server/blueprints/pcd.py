import open3d as o3d
import numpy as np
import os

from flask import Blueprint,request,jsonify,session
bp = Blueprint("pcd",__name__,url_prefix="/")

def display_point_cloud(pcd):
    center = pcd.get_center()
    # 坐标轴
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
        size=100, origin=center
    )
    o3d.visualization.draw_geometries([pcd, mesh_frame])


def pick_points(cloud):
    print(" Press [shift + right click] to undo point picking")
    print(" After picking points, press 'Q' to close the window")
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window(
        window_name="查看点坐标", width=800, height=800, left=50, top=50, visible=True
    )
    vis.add_geometry(cloud)
    vis.run()  # user picks points
    vis.destroy_window()
    return vis.get_picked_points()


def removeFarPoints(pcd):
    # 均值和标准差
    point_mean = np.mean(pcd.points, axis=0)
    print(point_mean)
    point_std = np.std(pcd.points, axis=0)
    # 定义滤波倍数
    num_std = 0.95
    # 计算距离均值超过一定倍数标准差的点，并剔除
    distances = np.sqrt(np.sum((pcd.points - point_mean) ** 2, axis=1))
    reserved_indices = np.where(distances < num_std * np.linalg.norm(point_std))[0]
    removedFar_pcd = pcd.select_by_index(reserved_indices)
    # display_point_cloud(removedFar_pcd)

    print("当前路径",os.getcwd())
    # 保存 PCD 文件
    o3d.io.write_point_cloud(
        "resources/output.pcd", removedFar_pcd
    )
    return removedFar_pcd

# 移除隐藏点
def removeHiddenPoints(pcd):
    print("->正在剔除隐藏点...")
    diameter = np.linalg.norm(
        np.asarray(pcd.get_max_bound()) - np.asarray(pcd.get_min_bound())
    )
    # 定义隐藏点去除的参数
    camera = [0, 0, diameter]  # 视点位置
    radius = diameter * 100  # 噪声点云半径,The radius of the sperical projection
    _, pt_map = pcd.hidden_point_removal(camera, radius)  # 获取视点位置能看到的所有点的索引 pt_map

    # 可视点点云
    pcd_visible = pcd.select_by_index(pt_map)
    # pcd_visible.paint_uniform_color([0, 0, 1])  # 可视点为蓝色
    print("->pcd_visible：", pcd_visible)
    # 隐藏点点云
    pcd_hidden = pcd.select_by_index(pt_map, invert=True)
    pcd_hidden.paint_uniform_color([1, 0, 0])  # 隐藏点为红色
    print("->pcd_hidden：", pcd_hidden)
    print("->正在可视化可视点和隐藏点点云...")
    o3d.visualization.draw_geometries([pcd_visible])


# 下采样
def downSamplePoints(pcd):
    pcd_downSample = pcd.voxel_down_sample(
        voxel_size=3
    )  # Downsample the point cloud with a voxel of 0.1
    print(
        "The points number after downsample：{}".format(
            np.asarray(pcd_downSample.points).shape[0]
        )
    )
    display_point_cloud(pcd_downSample)
    return pcd_downSample

@bp.route("/home",methods=['GET'])
def home():
    pcd = o3d.io.read_point_cloud("F:/OneDrive/100_work/python/.venv/resources/all.pcd")
    print("The orgin points number：{}".format(np.asarray(pcd.points).shape[0]))

    # 点云去噪
    pcd_downSample = downSamplePoints(pcd)

    removedFar_pcd = removeFarPoints(pcd_downSample)
    # removeHiddenPoints(pcd)

    # print(
    #     "Saved {} data points to output.pcd".format(
    #         np.asarray(pcd_denoised.points).shape[0]
    #     )
    # )
    return "success"
