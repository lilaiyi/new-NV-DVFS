import time, argparse
import glob
import re
import configparser
import json
import csv
parser = argparse.ArgumentParser()
parser.add_argument('--benchmark-setting', type=str, help='gpu benchmark setting', default='v100-dvfs')
parser.add_argument('--kernel-setting', type=str, help='kernels of benchmark', default='synthetic')
parser.add_argument('--kernel-setting-2', type=str, help='kernels of benchmark', default='synthetic')
parser.add_argument('--core-base', type=int, help='base core frequency', default=0)
parser.add_argument('--mem-base', type=int, help='base memory frequency', default=0)
opt = parser.parse_args()
print (opt)
gpucard = opt.benchmark_setting
version = opt.kernel_setting
version_2 = opt.kernel_setting_2
coreBase = opt.core_base
memBase = opt.mem_base

logRoot = '/home/lyli/NV-DVFS-Benchmark-master/logs/double_tasks/%s-%s_%s' %( gpucard, version,version_2)

perf_filelist = glob.glob(r'%s/benchmark_%s*perf.log' % (logRoot,version))
perf_filelist2 = glob.glob(r'%s/benchmark_%s*perf.log' % (logRoot,version_2))

dcgm_filelist = glob.glob(r'%s/benchmark_%s*dcgm.log' % (logRoot,version))

power_filelist = glob.glob(r'%s/*power.log' % (logRoot))

perf_filelist.sort()
perf_filelist2.sort()
dcgm_filelist.sort()
power_filelist.sort()

cf_ks = configparser.ConfigParser()
cf_ks.read("../configs/kernels/%s.cfg" % version)
cf_ks_2 = configparser.ConfigParser()
cf_ks_2.read("../configs/kernels/%s.cfg" % version_2)
benchmark_program_1 = cf_ks.sections()
benchmark_program_2 = cf_ks_2.sections()
recs = []
recs2 = []
head = ["appName", "coreF", "memF", "argNo", "kernel", "time/ms"]
for fp in perf_filelist:
    fn = fp.split('/')[-1]
    print (fn)

    baseInfo = fn.split('_')
    appName = baseInfo[1]
    print (baseInfo)
    coreF = str(int(baseInfo[2][4:]) + coreBase)
    memF = str(int(baseInfo[3][3:]) + memBase)
    argNo = baseInfo[4]

    kernel = json.loads(cf_ks.get(appName, 'kernels'))[0]
    rec = [appName, coreF, memF, argNo, kernel]

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
    timeRaw = list(timeRaw)[20:-20]
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
csvfile = open('csvs/raw/double/%s-%s-and-%s-%s-Performance.csv' % (gpucard, version,version_2,version), 'w')
csvWriter = csv.writer(csvfile, dialect='excel')
# write table head
csvWriter.writerow(head)
# write records
for rec in recs:
    csvWriter.writerow(rec[:len(head)])

rec=[]
for fp in perf_filelist2:
    fn = fp.split('/')[-1]
    print (fn)

    baseInfo = fn.split('_')
    appName = baseInfo[1]
    print (baseInfo)
    coreF = str(int(baseInfo[2][4:]) + coreBase)
    memF = str(int(baseInfo[3][3:]) + memBase)
    argNo = baseInfo[4]

    kernel = json.loads(cf_ks_2.get(appName, 'kernels'))[0]
    rec = [appName, coreF, memF, argNo, kernel]

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
    timeRaw = list(timeRaw)[20:-20]
    extracted_count = len(timeRaw)
    if len(timeRaw) == 0:
        continue
    time = 0
    for time_string in timeRaw:
        time += float(time_string.split()[-2].strip())
    average_time = time/extracted_count
    print (average_time)
    rec.append(average_time)
    recs2.append(rec)
# prepare csv file
csvfile = open('csvs/raw/double/%s-%s-and-%s-%s-Performance.csv' % (gpucard, version,version_2,version_2), 'w')
csvWriter = csv.writer(csvfile, dialect='excel')
# write table head
csvWriter.writerow(head)
# write records
for rec in recs2:
    csvWriter.writerow(rec[:len(head)])



rec = []
recs = []
head = ["appName", "coreF", "memF", "argNo", "power"]
for fp in power_filelist:
    fn = fp.split('/')[-1]
    print (fn)
    appName = opt.kernel_setting+'_'+opt.kernel_setting_2
    baseInfo = fn.split('_')
    print (baseInfo)
    coreF = str(int(baseInfo[0][4:]) + coreBase)
    memF = str(int(baseInfo[1][3:]) + memBase)
    argNo = baseInfo[2]

    rec = [appName, coreF, memF, argNo]

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
    rec.append(average_power)
    recs.append(rec)
# prepare csv file
csvfile = open('csvs/raw/double/%s-%s-and-%s-%s-POWER.csv' % (gpucard, version,version_2,version), 'w')
csvWriter = csv.writer(csvfile, dialect='excel')
# write table head
csvWriter.writerow(head)
# write records
for rec in recs:
    csvWriter.writerow(rec[:len(head)])




rec = []
recs = []
head = ["appName", "coreF", "memF", "argNo",'SMACT','SMOCC','TENSO','DRAMA','FP64A','FP32A','FP16A']
for fp in dcgm_filelist:
    fn = fp.split('/')[-1]
    print (fn)
    appName = opt.kernel_setting+'_'+opt.kernel_setting_2

    baseInfo = fn.split('_')
    print (baseInfo)
    coreF = str(int(baseInfo[2][4:]) + coreBase)
    memF = str(int(baseInfo[3][3:]) + memBase)
    argNo = baseInfo[4]

    rec = [appName, coreF, memF, argNo]

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
    dcgmRaw = list(dcgmRaw)[100:-100]
    extracted_count = len(dcgmRaw)
    if len(dcgmRaw) == 0:
        continue
    SMACT = 0
    SMOCC = 0
    TENSO = 0
    DRAMA = 0
    FP64A = 0
    FP32A = 0
    FP16A = 0
    for dcgm_string in dcgmRaw:
        FP16A  += float(dcgm_string.split()[-1].strip())
        FP32A  += float(dcgm_string.split()[-2].strip())
        FP64A  += float(dcgm_string.split()[-3].strip())
        DRAMA  += float(dcgm_string.split()[-4].strip())
        TENSO  += float(dcgm_string.split()[-5].strip())
        SMOCC  += float(dcgm_string.split()[-6].strip())
        SMACT  += float(dcgm_string.split()[-7].strip())
    average_SMACT = SMACT/extracted_count
    average_SMOCC = SMOCC/extracted_count
    average_TENSO = TENSO/extracted_count
    average_DRAMA = DRAMA/extracted_count
    average_FP64A = FP64A/extracted_count
    average_FP32A = FP32A/extracted_count
    average_FP16A = FP16A/extracted_count
    rec.append(average_SMACT)
    rec.append(average_SMOCC)
    rec.append(average_TENSO)
    rec.append(average_DRAMA)
    rec.append(average_FP64A)
    rec.append(average_FP32A)
    rec.append(average_FP16A)
    recs.append(rec)
# prepare csv file
csvfile = open('csvs/raw/double/%s-%s-and-%s-%s-dcgm.csv' % (gpucard, version,version_2,version), 'w')
csvWriter = csv.writer(csvfile, dialect='excel')
# write table head
csvWriter.writerow(head)
# write records
for rec in recs:
    csvWriter.writerow(rec[:len(head)])