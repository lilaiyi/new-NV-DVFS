import pandas as pd
import numpy  as ny
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import myscore
colums = ['coreF','SMACT','SMOCC','TENSO','DRAMA','FP32A','time/ms','power']
import joblib

standardScaler = StandardScaler()
df = pd.read_csv('/home/lyli/NV-DVFS-Benchmark-master/tools/csvs/raw/single/merged_file.csv')
x = standardScaler.fit_transform(df[["coreF","SMACT","SMOCC","DRAMA","FP32A"]])
y = df["power"]
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2)
model_power = RandomForestRegressor(n_estimators=300,random_state=42,n_jobs=-1)
model_power.fit(x_train,y_train)
print("power socre:")
print(myscore.score(model_power.predict(x_test),y_test))
joblib.dump(model_power, 'model_power.pkl')

x = standardScaler.fit_transform(df[["coreF","SMACT","SMOCC","DRAMA","FP32A"]])
y = df["time_ratio"]
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2)
model_per = RandomForestRegressor(n_estimators=300,random_state=42,n_jobs=-1)
model_per.fit(x_train,y_train)
print("ratio socre:")
print(myscore.score(model_per.predict(x_test),y_test))
joblib.dump(model_per, 'model_per.pkl')