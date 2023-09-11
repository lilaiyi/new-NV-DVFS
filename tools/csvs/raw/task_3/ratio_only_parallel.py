import pandas as pd
appname = ['matrixMul','nnForward','BlackScholes','vectorAdd','SobolQRNG','scalarProd','reduction','gaussian','sortingNetworks','mergeSort']
merged_df = pd.DataFrame()
count = 0
  
target_df = pd.DataFrame()
file_path = "merged_file_3.csv"
df = pd.read_csv(file_path)

        
df["time_ratio"] = df["time/ms"] / df["time/ms_single_1"]
df["time_ratio_2"] = df["time/ms_2"] / df["time/ms_single_2"]
merged_df = pd.concat([merged_df, df])

merged_df.to_csv("merged_file_3.csv", index=False)
