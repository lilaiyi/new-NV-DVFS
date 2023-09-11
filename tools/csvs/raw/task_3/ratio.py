import pandas as pd
appname = ['matrixMul','nnForward','BlackScholes','vectorAdd','SobolQRNG','scalarProd','reduction','gaussian','sortingNetworks','mergeSort']
merged_df = pd.DataFrame()
count = 0
for i in range(len(appname)):
    for j in range(i+1,len(appname)):   
        target_df = pd.DataFrame()
        complete_name = appname[i]+'_'+appname[j]
        file_path = "merged_file.csv"
        df = pd.read_csv(file_path)
        data = df[df["appName"] == complete_name]
        data_1380 = df[(df["coreF"] == 1380)&(df["appName"] == complete_name)]
        time = data["time/ms"].values
        freq_1380_time_1 = data_1380["time/ms_single_1"].values[0]
        freq_1380_time_2 = data_1380["time/ms_single_2"].values[0]   
        result_time = time / freq_1380_time_1
        time_2 = data["time/ms_2"].values
        result_time_2 = time_2 / freq_1380_time_2
        
        data["time_ratio"] = result_time
        data["time_ratio_2"] = result_time_2
        merged_df = pd.concat([merged_df, data])

merged_df.to_csv("merged_file.csv", index=False)
