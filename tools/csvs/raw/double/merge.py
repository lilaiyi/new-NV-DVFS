import os
import pandas as pd

appname = ['matrixMul','nnForward','BlackScholes','vectorAdd','SobolQRNG','scalarProd','reduction','gaussian','sortingNetworks','mergeSort']
file_names = os.listdir()
merged_df = pd.DataFrame()
for i in range(len(appname)):
    for j in range(i+1,len(appname)):     
        target_df = pd.DataFrame()
        complete_name = appname[i]+'-and-'+appname[j]
        files = [file_name for file_name in file_names if complete_name in file_name]
        dcgm_csv_file = [file_name for file_name in files if file_name.endswith("dcgm.csv")]
        Performance_csv_file_app1 = [file_name for file_name in files if file_name.endswith("%s-Performance.csv"%appname[i])]
        Performance_csv_file_app2 = [file_name for file_name in files if file_name.endswith("%s-Performance.csv"%appname[j])]
        Power_csv_file = [file_name for file_name in files if file_name.endswith("%s-%s-POWER.csv"%(complete_name,appname[i]))]
        df1 = pd.read_csv(dcgm_csv_file[0])
        df2 = pd.read_csv(Performance_csv_file_app1[0])
        df4 = pd.read_csv(Performance_csv_file_app2[0])
        df3 = pd.read_csv(Power_csv_file[0])
        # 合并三个DataFrame对象，相同head的行进行整合
        target_df = df1.merge(df2[[ "coreF", "memF", "argNo", "time/ms"]], on=[ "coreF", "memF", "argNo"], how="left")
        target_df = target_df.merge(df3[["appName", "coreF", "memF", "argNo", "power"]], on=["appName", "coreF", "memF", "argNo"], how="left")
        target_df = target_df.merge(df4[[ "coreF", "memF", "argNo", "time/ms"]], on=[ "coreF", "memF", "argNo"], how="left", suffixes=('', '_2'))

        merged_df = pd.concat([merged_df, target_df], ignore_index=True)

merged_df.to_csv("merged_file.csv", index=False)
