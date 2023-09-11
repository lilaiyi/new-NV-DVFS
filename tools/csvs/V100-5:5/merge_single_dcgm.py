import os
import pandas as pd
import configparser
import json
root_double = '/home/lyli/NV-DVFS-Benchmark-master/tools/csvs/V100-5:5/'
root_single =  '/home/lyli/NV-DVFS-Benchmark-master/tools/csvs/microbenchmark_single/'
KS_SETTING_1 = 'microbenchmark.cfg' 
KS_SETTING_2 = 'microbenchmark.cfg' 
cf_ks_1 = configparser.ConfigParser()
cf_ks_1.read("/home/lyli/NV-DVFS-Benchmark-master/configs/kernels/%s" % KS_SETTING_1)
benchmark_program_1 = cf_ks_1.sections()
cf_ks_2 = configparser.ConfigParser()
cf_ks_2.read("/home/lyli/NV-DVFS-Benchmark-master/configs/kernels/%s" % KS_SETTING_2)
benchmark_program_2 = cf_ks_2.sections()
file_names = os.listdir()
count = 0
file_names_double = os.listdir(root_double)
file_names_single = os.listdir(root_single)
merged_df = pd.DataFrame()
for i, app1 in enumerate(benchmark_program_1):
    for j, app2 in enumerate(benchmark_program_2):
        if j < i:
            continue
        if j==i: 
             args = json.loads(cf_ks_1.get(app1, 'args'))
             args_2 = json.loads(cf_ks_2.get(app2, 'args'))
             for argNo_1, arg_1 in enumerate(args):
                for argNo_2, arg_2 in enumerate(args_2):

                    if argNo_2<argNo_1 :
                        continue
                    count +=1
                    appname1 = app1+'-'+str(argNo_1)
                    appname2 = app2+'-'+str(argNo_2)
                    Pname = app2+'2'+'-'+str(argNo_2)

            
                    target_df = pd.DataFrame()
                    complete_name = appname1+'-and-'+appname2+'-'
                    files = [file_name for file_name in file_names_double if complete_name in file_name]
                    print(files)
                    dcgm_csv_file = [file_name for file_name in files if file_name.endswith("dcgm.csv")]
                    print(dcgm_csv_file)
                    Performance_csv_file_app1 = [file_name for file_name in files if file_name.endswith("%s-Performance.csv"%appname1)]
                    Performance_csv_file_app2 = [file_name for file_name in files if file_name.endswith("%s-Performance.csv"%Pname)]
                    Power_csv_file = [file_name for file_name in files if file_name.endswith("%sPOWER.csv"%complete_name)]
                    df1 = pd.read_csv(root_double+dcgm_csv_file[0],usecols=['appName','coreF'])
                    df2 = pd.read_csv(root_double+Performance_csv_file_app1[0])
                    df4 = pd.read_csv(root_double+Performance_csv_file_app2[0])
                    df3 = pd.read_csv(root_double+Power_csv_file[0])
                    # 合并三个DataFrame对象，相同head的行进行整合
                    target_df = df1.merge(df2[[ "coreF", "time/ms"]], on=[ "coreF"], how="left")
                    target_df = target_df.merge(df3[["coreF", "power"]], on=[ "coreF"], how="left")
                    target_df = target_df.merge(df4[[ "coreF",  "time/ms"]], on=[ "coreF"], how="left", suffixes=('', '_2'))


                    files_app1 = [file_name for file_name in file_names_single if appname1 in file_name]
                    files_app2 = [file_name for file_name in file_names_single if appname2 in file_name]
                    dcgm_csv_file_app1 = [file_name for file_name in files_app1 if file_name.endswith("dcgm.csv")]
                    dcgm_csv_file_app2 = [file_name for file_name in files_app2 if file_name.endswith("dcgm.csv")]
                    Performance_csv_file_app1 = [file_name for file_name in files_app1 if file_name.endswith("%s-Performance.csv"%appname1)]
                    Performance_csv_file_app2 = [file_name for file_name in files_app2 if file_name.endswith("%s-Performance.csv"%appname2)]
                    df1 = pd.read_csv(root_single+dcgm_csv_file_app1[0])
                    df2 = pd.read_csv(root_single+dcgm_csv_file_app2[0])
                    df3 = pd.read_csv(root_single+Performance_csv_file_app1[0])
                    df4 = pd.read_csv(root_single+Performance_csv_file_app2[0])
                    target_df = target_df.merge(df1[['coreF','SMACT','SMOCC','TENSO','DRAMA','FP64A','FP32A','FP16A']], on=[ "coreF"], how="left",suffixes=('', '_single_1'))
                    target_df = target_df.merge(df2[['coreF','SMACT','SMOCC','TENSO','DRAMA','FP64A','FP32A','FP16A']], on=[ "coreF"], how="left",suffixes=('', '_single_2'))
                    target_df = target_df.merge(df3[['coreF',"time/ms"]], on=[ "coreF"], how="left",suffixes=('', '_single_1'))
                    target_df = target_df.merge(df4[['coreF',"time/ms"]], on=[ "coreF"], how="left",suffixes=('', '_single_2'))






                    merged_df = pd.concat([merged_df, target_df], ignore_index=True)
        else :
             args = json.loads(cf_ks_1.get(app1, 'args'))
             args_2 = json.loads(cf_ks_2.get(app2, 'args'))
             for argNo_1, arg_1 in enumerate(args):
                for argNo_2, arg_2 in enumerate(args_2):
                    count +=1
                    appname1 = app1+'-'+str(argNo_1)
                    appname2 = app2+'-'+str(argNo_2)


            
                    target_df = pd.DataFrame()
                    complete_name = appname1+'-and-'+appname2+'-'
                    files = [file_name for file_name in file_names_double if complete_name in file_name]
                    dcgm_csv_file = [file_name for file_name in files if file_name.endswith("dcgm.csv")]
                    Performance_csv_file_app1 = [file_name for file_name in files if file_name.endswith("%s-Performance.csv"%appname1)]
                    Performance_csv_file_app2 = [file_name for file_name in files if file_name.endswith("%s-Performance.csv"%appname2)]
                    Power_csv_file = [file_name for file_name in files if file_name.endswith("POWER.csv")]
                    df1 = pd.read_csv(root_double+dcgm_csv_file[0],usecols=['appName','coreF'])
                    df2 = pd.read_csv(root_double+Performance_csv_file_app1[0])
                    df4 = pd.read_csv(root_double+Performance_csv_file_app2[0])
                    df3 = pd.read_csv(root_double+Power_csv_file[0])
                    # 合并三个DataFrame对象，相同head的行进行整合
                    target_df = df1.merge(df2[[ "coreF", "time/ms"]], on=[ "coreF"], how="left")
                    target_df = target_df.merge(df3[["coreF", "power"]], on=[ "coreF"], how="left")
                    target_df = target_df.merge(df4[[ "coreF",  "time/ms"]], on=[ "coreF"], how="left", suffixes=('', '_2'))


                    files_app1 = [file_name for file_name in file_names_single if appname1 in file_name]
                    files_app2 = [file_name for file_name in file_names_single if appname2 in file_name]
                    dcgm_csv_file_app1 = [file_name for file_name in files_app1 if file_name.endswith("dcgm.csv")]
                    dcgm_csv_file_app2 = [file_name for file_name in files_app2 if file_name.endswith("dcgm.csv")]
                    Performance_csv_file_app1 = [file_name for file_name in files_app1 if file_name.endswith("%s-Performance.csv"%appname1)]
                    Performance_csv_file_app2 = [file_name for file_name in files_app2 if file_name.endswith("%s-Performance.csv"%appname2)]
                    df1 = pd.read_csv(root_single+dcgm_csv_file_app1[0])
                    df2 = pd.read_csv(root_single+dcgm_csv_file_app2[0])
                    df3 = pd.read_csv(root_single+Performance_csv_file_app1[0])
                    df4 = pd.read_csv(root_single+Performance_csv_file_app2[0])
                    target_df = target_df.merge(df1[['coreF','SMACT','SMOCC','TENSO','DRAMA','FP64A','FP32A','FP16A']], on=[ "coreF"], how="left",suffixes=('', '_single_1'))
                    target_df = target_df.merge(df2[['coreF','SMACT','SMOCC','TENSO','DRAMA','FP64A','FP32A','FP16A']], on=[ "coreF"], how="left",suffixes=('', '_single_2'))
                    target_df = target_df.merge(df3[['coreF',"time/ms"]], on=[ "coreF"], how="left",suffixes=('', '_single_1'))
                    target_df = target_df.merge(df4[['coreF',"time/ms"]], on=[ "coreF"], how="left",suffixes=('', '_single_2'))






                    merged_df = pd.concat([merged_df, target_df], ignore_index=True)
merged_df.to_csv("merged_file_3.csv", index=False)
