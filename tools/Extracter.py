import os
app=['matrixMul','nnForward','BlackScholes','vectorAdd','SobolQRNG','scalarProd','reduction','gaussian','sortingNetworks','mergeSort']
def main():
    for i in range(len(app)):
        # for j in range(i+1,len(app)):
        #         os.system('python DoublePerExtracter.py  --kernel-setting %s --kernel-setting-2 %s'%(app[i],app[j]))
            os.system('python  SinglePerExtracter.py  --kernel-setting %s'%(app[i]))
main()