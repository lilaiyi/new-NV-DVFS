import os
import pandas as pd
root_double = '/home/lyli/NV-DVFS-Benchmark-master/tools/csvs/raw/double/'
root_single =  '/home/lyli/NV-DVFS-Benchmark-master/tools/csvs/raw/single/'
appname = ['matrixMul','nnForward','BlackScholes','vectorAdd','SobolQRNG','scalarProd','reduction','gaussian','sortingNetworks','mergeSort']
file_names_double = os.listdir(root_double)
file_names_single = os.listdir(root_single)
merged_df = pd.DataFrame()
for i in range(len(appname)):
    for j in range(i+1,len(appname)):     
        target_df = pd.DataFrame()
        complete_name = appname[i]+'-and-'+appname[j]
        files = [file_name for file_name in file_names_double if complete_name in file_name]
        dcgm_csv_file = [file_name for file_name in files if file_name.endswith("dcgm.csv")]
        Performance_csv_file_app1 = [file_name for file_name in files if file_name.endswith("%s-Performance.csv"%appname[i])]
        Performance_csv_file_app2 = [file_name for file_name in files if file_name.endswith("%s-Performance.csv"%appname[j])]
        Power_csv_file = [file_name for file_name in files if file_name.endswith("%s-%s-POWER.csv"%(complete_name,appname[i]))]
        df1 = pd.read_csv(root_double+dcgm_csv_file[0],usecols=['appName','coreF'])
        df2 = pd.read_csv(root_double+Performance_csv_file_app1[0])
        df4 = pd.read_csv(root_double+Performance_csv_file_app2[0])
        df3 = pd.read_csv(root_double+Power_csv_file[0])
        # 合并三个DataFrame对象，相同head的行进行整合
        target_df = df1.merge(df2[[ "coreF", "time/ms"]], on=[ "coreF"], how="left")
        target_df = target_df.merge(df3[["coreF", "power"]], on=[ "coreF"], how="left")
        target_df = target_df.merge(df4[[ "coreF",  "time/ms"]], on=[ "coreF"], how="left", suffixes=('', '_2'))


        files = [file_name for file_name in file_names_single if appname[i] or appname[j] in file_name]
        dcgm_csv_file_app1 = [file_name for file_name in files if file_name.endswith(appname[i]+"-dcgm.csv")]
        dcgm_csv_file_app2 = [file_name for file_name in files if file_name.endswith(appname[j]+"-dcgm.csv")]
        Performance_csv_file_app1 = [file_name for file_name in files if file_name.endswith("%s-Performance.csv"%appname[i])]
        Performance_csv_file_app2 = [file_name for file_name in files if file_name.endswith("%s-Performance.csv"%appname[j])]
        POWER_csv_file_app1 = [file_name for file_name in files if file_name.endswith("%s-POWER.csv"%appname[i])]
        POWER_csv_file_app2 = [file_name for file_name in files if file_name.endswith("%s-POWER.csv"%appname[j])]
        df1 = pd.read_csv(root_single+dcgm_csv_file_app1[0])
        df2 = pd.read_csv(root_single+dcgm_csv_file_app2[0])
        df3 = pd.read_csv(root_single+Performance_csv_file_app1[0])
        df4 = pd.read_csv(root_single+Performance_csv_file_app2[0])
        df5 = pd.read_csv(root_single+POWER_csv_file_app1[0])
        df6 = pd.read_csv(root_single+POWER_csv_file_app2[0])
        target_df = target_df.merge(df1[['coreF','SMACT','SMOCC','TENSO','DRAMA','FP64A','FP32A','FP16A']], on=[ "coreF"], how="left",suffixes=('', '_single_1'))
        target_df = target_df.merge(df2[['coreF','SMACT','SMOCC','TENSO','DRAMA','FP64A','FP32A','FP16A']], on=[ "coreF"], how="left",suffixes=('', '_single_2'))
        target_df = target_df.merge(df3[['coreF',"time/ms"]], on=[ "coreF"], how="left",suffixes=('', '_single_1'))
        target_df = target_df.merge(df4[['coreF',"time/ms"]], on=[ "coreF"], how="left",suffixes=('', '_single_2'))
        target_df = target_df.merge(df5[["coreF","power"]],on=[ "coreF"], how="left",suffixes=('', '_single_1'))
        target_df = target_df.merge(df6[["coreF","power"]],on=[ "coreF"], how="left",suffixes=('', '_single_2'))





        merged_df = pd.concat([merged_df, target_df], ignore_index=True)

merged_df.to_csv("merged_file_3.csv", index=False)
