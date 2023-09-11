import os
import shutil

# 指定目录的路径
base_directory = "./5:5/12K-18K "

# 获取目录下的所有子目录
subdirectories = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]
print(len(subdirectories))
# 找出以'v100-dvfs-1'开头的目录
matching_directories = [d for d in subdirectories if d.startswith("v100-dvfs-1")]
print(len(matching_directories))
# 遍历匹配的目录
for directory_with_1 in matching_directories:
    # 构建目录的完整路径
    full_path_with_1 = os.path.join(base_directory, directory_with_1)
    print(full_path_with_1)
    # 去掉'-1'并构建对应目录名称
    directory_without_1 = directory_with_1.replace('-1', '', 1)
    print(directory_without_1)
    # 构建对应目录的完整路径
    full_path_without_1 = os.path.join(base_directory, directory_without_1)

    # 检查对应目录是否存在
    if os.path.exists(full_path_without_1) and os.path.isdir(full_path_without_1):
        # 移动目录-with-1下的内容到对应目录-without-1下
        for item in os.listdir(full_path_with_1):
            item_path = os.path.join(full_path_with_1, item)
            shutil.move(item_path, os.path.join(full_path_without_1, item))
        
        # 删除目录-with-1
        os.rmdir(full_path_with_1)
    else:
        # 重命名目录-with-1为目录-without-1
        os.rename(full_path_with_1, full_path_without_1)
