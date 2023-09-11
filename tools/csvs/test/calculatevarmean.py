import pandas as pd

# 假设您已经有了包含数据的 DataFrame，如果没有，您需要先创建一个 DataFrame
# 这里假设您的数据已经存储在一个名为 "data.csv" 的 CSV 文件中
data = pd.read_csv('merged_file_4.csv')

# 计算新的列 "var/power"，并将结果存储在名为 "var_over_power" 的新列中
data['var_over_power'] = data['var'] / data['power']

# 保存包含新列的 DataFrame 到一个新的 CSV 文件
data.to_csv('merged_file_var_power_single_dcgm.csv', index=False)
