import astropy.io.fits as fits
import math
import numpy as np
import glob
import sys, os
import time
from scipy import integrate
S=1 #area of our dectcor/batse's(or fermi's)
#parameters of band GRB model
alp=-0.968
beta=-2.427
E0=149.5
#energy range
low=5
top=200
#time resolution
t=0.005
cur = os.getcwd()
name=glob.glob('2*')
for k in name:
    os.system('mkdir'+' '+cur+'/'+k+'_seperate')
    source = glob.glob(cur+'/'+k+'/'+'/*/')
    for m in range(len(source)):
        if os.path.exists(cur+'/'+k+'_seperate'+'/'+source[m].split('/')[-2])==True :
            m=m+1
        else:
            os.system('mkdir'+' '+cur+'/'+k+'_seperate'+'/'+source[m].split('/')[-2]+'/')
            j1=glob.glob(source[m]+'/*rebin*')
            j2=glob.glob(source[m]+'/*energy*')
            #skip empty/error file
            try:
                start=time.time()
                a=np.transpose(np.loadtxt(j1[0]))
                ener=np.transpose(np.loadtxt(j2[0]))
            except:
                continue
            else:
     
                np.savetxt(cur+'/'+k+'_seperate'+'/'+source[m].split('/')[-2]+'/'+'CXB.txt',cut(a,ener,0))
                np.savetxt(cur+'/'+k+'_seperate'+'/'+source[m].split('/')[-2]+'/'+'burst.txt',cut(a,ener,1))
                np.savetxt(cur+'/'+k+'_seperate'+'/'+source[m].split('/')[-2]+'/'+'lc.txt',cut(lc,ener,2))
                print time.time()-start

