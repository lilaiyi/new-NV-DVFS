import time, argparse
import glob
import re
import configparser
import json
import csv
parser = argparse.ArgumentParser()
parser.add_argument('--benchmark-setting', type=str, help='gpu benchmark setting', default='v100-dvfs')
parser.add_argument('--kernel-setting', type=str, help='kernels of benchmark', default='synthetic')
parser.add_argument('--argnum',type=str,help='',default=0)
parser.add_argument('--core-base', type=int, help='base core frequency', default=0)
parser.add_argument('--mem-base', type=int, help='base memory frequency', default=0)
opt = parser.parse_args()
gpucard = opt.benchmark_setting
version = opt.kernel_setting
coreBase = opt.core_base
memBase = opt.mem_base
argnum = opt.argnum
appName_root = version +'-'+ argnum
logRoot = '/home/lyli/NV-DVFS-Benchmark-master/logs/microbenchmark/single/%s-%s' %( gpucard, appName_root)

perf_filelist = glob.glob(r'%s/benchmark_%s*perf.log' % (logRoot,version))

dcgm_filelist = glob.glob(r'%s/*dcgm.log' % (logRoot))

power_filelist = glob.glob(r'%s/*power.log' % (logRoot))

perf_filelist.sort()
dcgm_filelist.sort()
power_filelist.sort()

recs = []
recs2 = []
head = ["appName", "coreF", "memF", "time/ms"]
for fp in perf_filelist:
    fn = fp.split('/')[-1]
    print (fn)

    baseInfo = fn.split('_')
    appName = baseInfo[1]
    print (baseInfo)
    coreF = str(int(baseInfo[2][4:]) + coreBase)
    memF = str(int(baseInfo[3][3:]) + memBase)



    rec = [appName_root, coreF, memF]

    # extract execution time information
    f = open(fp, 'r')
    content = f.readlines()
    f.close()
    print(fp)
    # regex = re.compile(r'.*\%.*' + kernel)
    # time = filter(regex.search, content)[0].split()[3].strip()
    # if 'us' in time:
    #     time = float(time[:-2]) / 1000
    # else:
    #     time = float(time[:-2])

    # regex = re.compile(r'(iterated \d+, average time is)|(Average Kernel Time)|(Average Time)')
    regex = re.compile(r'last \d+ iterats, average time is (\d+\.\d+) msec')
    timeRaw = filter(regex.search, content)
    timeRaw = list(timeRaw)
    remove_percentage = 0.4
    remove_count = int(len(timeRaw) * remove_percentage)
    timeRaw = timeRaw[remove_count:-remove_count]
    extracted_count = len(timeRaw)
    if len(timeRaw) == 0:
        continue
    time = 0
    for time_string in timeRaw:
        time += float(time_string.split()[-2].strip())
    average_time = time/extracted_count
    print (average_time)
    rec.append(average_time)
    recs.append(rec)
# prepare csv file
csvfile = open('/home/lyli/NV-DVFS-Benchmark-master/tools/csvs/microbenchmark_single/%s-%s-Performance.csv' % (gpucard, appName_root), 'w')
csvWriter = csv.writer(csvfile, dialect='excel')
# write table head
csvWriter.writerow(head)
# write records
for rec in recs:
    csvWriter.writerow(rec[:len(head)])


rec = []
recs = []
head = ["appName", "coreF", "memF", "power"]
for fp in power_filelist:
    fn = fp.split('/')[-1]
    appName = opt.kernel_setting
    baseInfo = fn.split('_')
    coreF = str(int(baseInfo[0][4:]) + coreBase)
    memF = str(int(baseInfo[1][3:]) + memBase)

    rec = [appName_root, coreF, memF]

    # extract execution time information
    f = open(fp, 'r')
    content = f.readlines()
    f.close()
    print(fp)
    # regex = re.compile(r'.*\%.*' + kernel)
    # time = filter(regex.search, content)[0].split()[3].strip()
    # if 'us' in time:
    #     time = float(time[:-2]) / 1000
    # else:
    #     time = float(time[:-2])

    # regex = re.compile(r'(iterated \d+, average time is)|(Average Kernel Time)|(Average Time)')
    regex = re.compile(r'(\d+\.\d+) ms\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)')
    PowerRaw = filter(regex.search, content)
    PowerRaw = list(PowerRaw)
    power_values = sorted([float(power_string.split()[-1].strip()) for power_string in PowerRaw], reverse=True)
    
    top_power_values = power_values[:10]
    average_power = sum(top_power_values) / len(top_power_values)
    print (average_power)
    rec.append(average_power)
    recs.append(rec)
# prepare csv file
csvfile = open('/home/lyli/NV-DVFS-Benchmark-master/tools/csvs/microbenchmark_single/%s-%s-POWER.csv' % (gpucard,appName_root), 'w')
csvWriter = csv.writer(csvfile, dialect='excel')
# write table head
csvWriter.writerow(head)
# write records
for rec in recs:
    csvWriter.writerow(rec[:len(head)])




rec = []
recs = []
head = ["appName", "coreF", "memF",'SMACT','SMOCC','TENSO','DRAMA','FP64A','FP32A','FP16A']
for fp in dcgm_filelist:
    fn = fp.split('/')[-1]
    print (fn)
    appName = opt.kernel_setting

    baseInfo = fn.split('_')
    print (baseInfo)
    coreF = str(int(baseInfo[0][4:]) + coreBase)
    memF = str(int(baseInfo[1][3:]) + memBase)

    rec = [appName_root, coreF, memF]

    # extract execution time information
    f = open(fp, 'r')
    content = f.readlines()
    f.close()
    print(fp)
    # regex = re.compile(r'.*\%.*' + kernel)
    # time = filter(regex.search, content)[0].split()[3].strip()
    # if 'us' in time:
    #     time = float(time[:-2]) / 1000
    # else:
    #     time = float(time[:-2])

    # regex = re.compile(r'(iterated \d+, average time is)|(Average Kernel Time)|(Average Time)')
    regex = re.compile(r'GPU \d+\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)')
    dcgmRaw = filter(regex.search, content)
    dcgmRaw = list(dcgmRaw)
    remove_percentage = 0.4
    remove_count = int(len(dcgmRaw) * remove_percentage)
    dcgmRaw = dcgmRaw[remove_count:-remove_count]
    extracted_count = len(dcgmRaw)
    if len(dcgmRaw) == 0:
        continue
    SMACT = 0
    SMACT_C= 0
    SMOCC = 0
    SMOCC_C=0
    TENSO = 0
    TENSO_C=0 
    DRAMA = 0
    DRAMA_C=0
    FP64A = 0
    FP64A_C=0
    FP32A = 0
    FP32A_C=0
    FP16A = 0
    FP16A_C=0
    for dcgm_string in dcgmRaw:
        if(float(dcgm_string.split()[-1].strip())!=0):
            FP16A  += float(dcgm_string.split()[-1].strip())
            FP16A_C+=1
        if(float(dcgm_string.split()[-2].strip())!=0):    
            FP32A  += float(dcgm_string.split()[-2].strip())
            FP32A_C+=1
        if(float(dcgm_string.split()[-3].strip())!=0):    
            FP64A  += float(dcgm_string.split()[-3].strip())
            FP64A_C+=1
        if(float(dcgm_string.split()[-4].strip())!=0):    
            DRAMA  += float(dcgm_string.split()[-4].strip())
            DRAMA_C+=1
        if(float(dcgm_string.split()[-5].strip())!=0):    
            TENSO  += float(dcgm_string.split()[-5].strip())
            TENSO_C +=1
        if(float(dcgm_string.split()[-6].strip())!=0):    
            SMOCC  += float(dcgm_string.split()[-6].strip())
            SMOCC_C+=1
        if(float(dcgm_string.split()[-7].strip())!=0):    
            SMACT  += float(dcgm_string.split()[-7].strip())
            SMACT_C+=1
    average_SMACT=0
    average_SMOCC=0
    average_TENSO=0
    average_DRAMA=0
    average_FP64A=0
    average_FP32A=0
    average_FP16A=0
    if SMACT_C!=0:
        average_SMACT = SMACT/SMACT_C
    if SMOCC_C!=0:
        average_SMOCC = SMOCC/SMOCC_C
    if TENSO_C!=0:
        average_TENSO = TENSO/TENSO_C
    if DRAMA_C!=0:
        average_DRAMA = DRAMA/DRAMA_C
    if FP64A_C!=0:
        average_FP64A = FP64A/FP64A_C
    if FP32A_C!=0:
        average_FP32A = FP32A/FP32A_C
    if FP16A_C!=0:
        average_FP16A = FP16A/FP16A_C
    rec.append(average_SMACT)
    rec.append(average_SMOCC)
    rec.append(average_TENSO)
    rec.append(average_DRAMA)
    rec.append(average_FP64A)
    rec.append(average_FP32A)
    rec.append(average_FP16A)
    recs.append(rec)
# prepare csv file
csvfile = open('/home/lyli/NV-DVFS-Benchmark-master/tools/csvs/microbenchmark_single/%s-%s-dcgm.csv' % (gpucard, appName_root), 'w')
csvWriter = csv.writer(csvfile, dialect='excel')
# write table head
csvWriter.writerow(head)
# write records
for rec in recs:
    csvWriter.writerow(rec[:len(head)])