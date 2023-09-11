import os
import shutil

# 定义目录A和目录B的路径
directory_A = '/home/lyli/NV-DVFS-Benchmark-master/logs/5:5/1.8K-'
directory_B = '/home/lyli/NV-DVFS-Benchmark-master/logs/5:5/ALL'

# 获取目录A下的所有子目录
subdirectories_A = [d for d in os.listdir(directory_A) if os.path.isdir(os.path.join(directory_A, d))]

# 遍历每个子目录
for subdirectory in subdirectories_A:
    source_directory = os.path.join(directory_A, subdirectory)
    destination_directory = os.path.join(directory_B, subdirectory)

    # 确保目标子目录存在，如果不存在则创建
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # 获取子目录中的所有文件
    files_to_move = [f for f in os.listdir(source_directory) if os.path.isfile(os.path.join(source_directory, f))]

    # 移动文件到目标子目录
    for file_to_move in files_to_move:
        source_file = os.path.join(source_directory, file_to_move)
        destination_file = os.path.join(destination_directory, file_to_move)

        shutil.move(source_file, destination_file)

