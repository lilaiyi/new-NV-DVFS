import pandas as pd

appname = ['BlackScholes', 'gaussian', 'matrixMul', 'mergeSort', 'nnForward', 'reduction', 'scalarProd', 'SobolQRNG', 'sortingNetworks', 'vectorAdd']
merged_df = pd.DataFrame()

file_path = "merged_file_2.csv"
df = pd.read_csv(file_path)

for app in appname:
    print(app)
    # 找到 "BlackScholes" 和 "1380" 这两组数据
    data = df[df["appName"] == app]
    data_1380 = data[(data["coreF"] == 1380)]
    columns_to_replace = ["SMACT", "SMOCC", "TENSO", "DRAMA", "FP64A", "FP32A", "FP16A"]

    for column in columns_to_replace:
        # 获取coreF不为1380的行的索引
        indices_to_replace = data.index[ (data["coreF"] != 1380)]
        
        # 使用coreF为1380的行的数据进行替换
        data.loc[indices_to_replace, column] = data_1380[column].values[0]
    
    # 将修改后的数据存储在merged_df中
    merged_df = pd.concat([merged_df, data])

# 将修改后的数据保存回文件
merged_df.to_csv("merged_file_2.csv", index=False)
