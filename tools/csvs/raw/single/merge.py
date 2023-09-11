import os
import pandas as pd

appname = ['BlackScholes','gaussian','matrixMul','mergeSort','nnForward','reduction','scalarProd','SobolQRNG','sortingNetworks','vectorAdd']
file_names = os.listdir()

merged_df = pd.DataFrame()
for app_name in appname:
    target_df = pd.DataFrame()
    files = [file_name for file_name in file_names if app_name in file_name]
    dcgm_csv_file = [file_name for file_name in files if file_name.endswith("dcgm.csv")]
    Performance_csv_file = [file_name for file_name in files if file_name.endswith("Performance.csv")]
    Power_csv_file = [file_name for file_name in files if file_name.endswith("POWER.csv")]
    df1 = pd.read_csv(dcgm_csv_file[0])
    df2 = pd.read_csv(Performance_csv_file[0])
    df3 = pd.read_csv(Power_csv_file[0])
    # 合并三个DataFrame对象，相同head的行进行整合
    target_df = df1.merge(df2, on=["appName", "coreF", "memF", "argNo"], how="left")
    target_df = target_df.merge(df3, on=["appName", "coreF", "memF", "argNo"], how="left")
    merged_df = pd.concat([merged_df, target_df], ignore_index=True)

merged_df.to_csv("merged_file.csv", index=False)


# for file in dcgm_files:
#     df = pd.read_csv(file)
#     target_df= pd.concat([target_df, df])

# target_df.to_csv('all_dcgm.csv', index=False)


# import pandas as pd

# # 假设三个CSV文件的文件名分别为 "file1.csv", "file2.csv" 和 "file3.csv"
# file1 = "file1.csv"
# file2 = "file2.csv"
# file3 = "file3.csv"

# # 读取三个CSV文件为DataFrame对象
# df1 = pd.read_csv(file1)
# df2 = pd.read_csv(file2)
# df3 = pd.read_csv(file3)

# # 合并三个DataFrame对象，相同head的行进行整合
# merged_df = pd.concat([df1, df2, df3], ignore_index=True)

# # 将整合后的DataFrame保存为一个新的CSV文件
# merged_df.to_csv("merged_file.csv", index=False)
