import subprocess
import open3d as o3d
import numpy as np
import os

# def display_point_cloud(pcd):
#     center = pcd.get_center()
#     # 坐标轴
#     mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
#         size=100, origin=center
#     )
#     o3d.visualization.draw_geometries([pcd, mesh_frame])

def removeFarPoints(pcd,output_directory):
    # 均值和标准差
    point_mean = np.mean(pcd.points, axis=0)
    point_std = np.std(pcd.points, axis=0)
    # 定义滤波倍数
    num_std = 0.95
    # 计算距离均值超过一定倍数标准差的点，并剔除
    distances = np.sqrt(np.sum((pcd.points - point_mean) ** 2, axis=1))
    reserved_indices = np.where(distances < num_std * np.linalg.norm(point_std))[0]
    removedFar_pcd = pcd.select_by_index(reserved_indices)

    # 检查已存在的文件数量以生成新的文件名
    existing_files = [f for f in os.listdir(output_directory) if f.startswith('output_denoised_')]
    next_file_number = len(existing_files) + 1
    output_file_name = f"output_denoised_{next_file_number}.pcd"
    output_path = os.path.join(output_directory, output_file_name)

    # 保存 PCD 文件
    o3d.io.write_point_cloud(output_path, removedFar_pcd)
    # 打开文件资源管理器并选中文件
    subprocess.run(f'explorer /select,{os.path.abspath(output_path)}', shell=True)
    print("Points Number after Dnoise:{}".format(np.asarray(removedFar_pcd.points).shape[0])+"\n")
    print(f"Path: {output_path}")
    return removedFar_pcd

def downSamplePoints(pcd):
    pcd_downSample = pcd.voxel_down_sample(voxel_size=0.01)
    # display_point_cloud(pcd_downSample)
    return pcd_downSample

def process_point_cloud(file_path,output_directory):
    pcd = o3d.io.read_point_cloud(file_path)
    print("Origin Points Number:{}".format(np.asarray(pcd.points).shape[0])+"\n")

    # 点云去噪
    pcd_downSample = downSamplePoints(pcd)
    removedFar_pcd = removeFarPoints(pcd_downSample,output_directory)
    return "Process completed"

if __name__ == "__main__":
    # Assuming denoise.py is in the root, set the relative path to the point-cloud directory
    base_path = os.path.dirname(__file__)
    point_cloud_dir = os.path.join(base_path, 'output', '27072023-1628', '170', 'point-cloud')
    output_directory = os.path.join(base_path, 'output', 'denoised')

    # 确保输出目录存在
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for file_name in os.listdir(point_cloud_dir):
        if file_name.endswith('-1628-170.pcd'):
            file_path = os.path.join(point_cloud_dir, file_name)
            # print(f"Processing {file_name}...")
            process_point_cloud(file_path, output_directory)
