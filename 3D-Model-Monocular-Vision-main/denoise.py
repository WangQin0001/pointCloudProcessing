import subprocess
import open3d as o3d
import numpy as np
import os


def removeFarPoints(pcd):
    # 均值和标准差
    point_mean = np.mean(pcd.points, axis=0)
    point_std = np.std(pcd.points, axis=0)
    # 定义滤波倍数
    num_std = 0.95
    # 计算距离均值超过一定倍数标准差的点，并剔除
    distances = np.sqrt(np.sum((pcd.points - point_mean) ** 2, axis=1))
    reserved_indices = np.where(distances < num_std * np.linalg.norm(point_std))[0]
    return pcd.select_by_index(reserved_indices)


def downSamplePoints(pcd):
    return pcd.voxel_down_sample(voxel_size=0.01)

# 翻转点云模型
def flip_point_cloud(pcd, axis='y'):
    points = np.asarray(pcd.points)
    if axis == 'x':
        points[:, 0] = -points[:, 0]  # 沿X轴翻转
    elif axis == 'y':
        points[:, 1] = -points[:, 1]  # 沿Y轴翻转
    elif axis == 'z':
        points[:, 2] = -points[:, 2]  # 沿Z轴翻转
    pcd.points = o3d.utility.Vector3dVector(points)
    return pcd

# 将模型重新定位
def center_point_cloud(pcd):
    points = np.asarray(pcd.points)
    centroid = np.mean(points, axis=0)  # 计算所有点的均值
    centered_points = points - centroid  # 重定位每个点
    centered_pcd = o3d.geometry.PointCloud()
    centered_pcd.points = o3d.utility.Vector3dVector(centered_points)
    if pcd.has_colors():  # 如果原始点云有颜色信息，保留颜色信息
        centered_pcd.colors = pcd.colors
    return centered_pcd


def save_and_log_point_cloud(pcd, output_directory):
    existing_files = [f for f in os.listdir(output_directory) if f.startswith('output_denoised_')]
    next_file_number = len(existing_files) + 1
    output_file_name = f"output_denoised_{next_file_number}.pcd"
    output_path = os.path.join(output_directory, output_file_name)

    o3d.io.write_point_cloud(output_path, pcd)
    subprocess.run(f'explorer /select,{os.path.abspath(output_path)}', shell=True)

    print("Points Number after Processing:{}".format(np.asarray(pcd.points).shape[0]) + "\n")
    print(f"Path: {output_path}")


def process_point_cloud(file_path, output_directory):
    pcd = o3d.io.read_point_cloud(file_path)
    pcd_downSample = downSamplePoints(pcd)
    removedFar_pcd = removeFarPoints(pcd_downSample)
    flipped_pcd = flip_point_cloud(removedFar_pcd, axis='y')  # 根据需要选择翻转的轴
    # 将点云中心移到坐标原点
    centered_pcd = center_point_cloud(flipped_pcd)
    save_and_log_point_cloud(centered_pcd, output_directory)
    return "Process completed"

if __name__ == "__main__":
    base_path = os.path.dirname(__file__)
    point_cloud_dir = os.path.join(base_path, 'output', '27072023-1628', '170', 'point-cloud')
    output_directory = os.path.join(base_path, 'output', 'denoised')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for file_name in os.listdir(point_cloud_dir):
        if file_name.endswith('-1628-170.pcd'):
            file_path = os.path.join(point_cloud_dir, file_name)
            process_point_cloud(file_path, output_directory)
