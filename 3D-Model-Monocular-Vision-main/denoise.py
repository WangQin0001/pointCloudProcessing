import subprocess
import open3d as o3d
import numpy as np
import os
import sys

def removeFarPoints(pcd):
    point_mean = np.mean(pcd.points, axis=0)
    point_std = np.std(pcd.points, axis=0)
    num_std = 0.95
    distances = np.sqrt(np.sum((pcd.points - point_mean) ** 2, axis=1))
    reserved_indices = np.where(distances < num_std * np.linalg.norm(point_std))[0]
    return pcd.select_by_index(reserved_indices)

def downSamplePoints(pcd):
    return pcd.voxel_down_sample(voxel_size=0.01)

def flip_point_cloud(pcd, axis='y'):
    points = np.asarray(pcd.points)
    if axis == 'x':
        points[:, 0] = -points[:, 0]
    elif axis == 'y':
        points[:, 1] = -points[:, 1]
    elif axis == 'z':
        points[:, 2] = -points[:, 2]
    pcd.points = o3d.utility.Vector3dVector(points)
    return pcd

def center_point_cloud(pcd):
    points = np.asarray(pcd.points)
    centroid = np.mean(points, axis=0)
    centered_points = points - centroid
    centered_pcd = o3d.geometry.PointCloud()
    centered_pcd.points = o3d.utility.Vector3dVector(centered_points)
    if pcd.has_colors():
        centered_pcd.colors = pcd.colors
    return centered_pcd

def save_and_log_point_cloud(pcd, output_directory):
    existing_files = [f for f in os.listdir(output_directory) if f.startswith('output_denoised_')]
    next_file_number = len(existing_files) + 1
    output_file_name = f"output_denoised_{next_file_number}.pcd"
    output_path = os.path.join(output_directory, output_file_name)

    o3d.io.write_point_cloud(output_path, pcd)
    subprocess.run(f'explorer /select,{os.path.abspath(output_path)}', shell=True)

    print("处理后的点数:{}".format(np.asarray(pcd.points).shape[0]) + "\n")
    print(f"文件路径: {output_path}")

def process_point_cloud(file_path, output_directory):
    pcd = o3d.io.read_point_cloud(file_path)
    pcd_downSample = downSamplePoints(pcd)
    removedFar_pcd = removeFarPoints(pcd_downSample)
    flipped_pcd = flip_point_cloud(removedFar_pcd, axis='y')
    centered_pcd = center_point_cloud(flipped_pcd)
    save_and_log_point_cloud(centered_pcd, output_directory)
    return "处理完成"

if __name__ == "__main__":
    base_path = os.path.dirname(__file__)
    output_directory = os.path.join(base_path, 'output', 'denoised')

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 如果命令行参数提供了文件路径，则使用该路径，否则使用默认路径
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print("提供的路径"+file_path)
        process_point_cloud(file_path, output_directory)
    else:
        # 使用默认输入路径
        point_cloud_dir = os.path.join(base_path, 'output', '00000000-1628', '170', 'point-cloud')
        for file_name in os.listdir(point_cloud_dir):
            if file_name.endswith('-1628-170.pcd'):
                file_path = os.path.join(point_cloud_dir, file_name)
                process_point_cloud(file_path, output_directory)
