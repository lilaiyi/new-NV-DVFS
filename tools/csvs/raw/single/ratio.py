import pandas as pd
appname = ['BlackScholes','gaussian','matrixMul','mergeSort','nnForward','reduction','scalarProd','SobolQRNG','sortingNetworks','vectorAdd']
merged_df = pd.DataFrame()
for  app in appname:
        file_path = "merged_file.csv"
        df = pd.read_csv(file_path)

        # 找到 "BlackScholes" 和 "1380" 这两组数据
        data = df[df["appName"] == app]
        data_1380 = df[(df["coreF"] == 1380)&(df["appName"] == app)]
        # 将 "BlackScholes" 的 "time/ms" 列除以 1380 频率下的 "time/ms" 列
        time = data["time/ms"].values
        freq_1380_time = data_1380["time/ms"].values[0]  # 假设 "1380" 只有一组数据，所以取第一个值
        result_time = time / freq_1380_time

        # 将结果存储在新的列 "time_ratio" 中
        data["time_ratio"] = result_time
        merged_df = pd.concat([merged_df, data])
        # 更新原始 DataFrame 中 "BlackScholes" 这部分的数据
merged_df.to_csv("merged_file.csv", index=False)
