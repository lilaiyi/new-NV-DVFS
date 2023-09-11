import pandas as pd
appname = ['matrixMul','nnForward','BlackScholes','vectorAdd','SobolQRNG','scalarProd','reduction','gaussian','sortingNetworks','mergeSort']
merged_df = pd.DataFrame()
file_path = "merged_file_3.csv"
df = pd.read_csv(file_path)
for i in range(len(appname)):
    for j in range(i+1,len(appname)):   
        complete_name = appname[i]+'_'+appname[j]
        data = df[df["appName"] == complete_name]
        data_1380 = data[(data["coreF"] == 1380)]
        columns_to_replace = ["SMACT", "SMOCC", "TENSO", "DRAMA", "FP64A", "FP32A", "FP16A",
                                "SMACT_single_2","SMOCC_single_2","TENSO_single_2","DRAMA_single_2",
                                "FP64A_single_2","FP32A_single_2","FP16A_single_2","power_single_1","power_single_2"]

        for column in columns_to_replace:
            # 获取coreF不为1380的行的索引
            indices_to_replace = data.index[ (data["coreF"] != 1380)]
            
            # 使用coreF为1380的行的数据进行替换
            data.loc[indices_to_replace, column] = data_1380[column].values[0]
        
        # 将修改后的数据存储在merged_df中
        merged_df = pd.concat([merged_df, data])

merged_df.to_csv("merged_file_realapp.csv", index=False)