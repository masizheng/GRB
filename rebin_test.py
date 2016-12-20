import astropy.io.fits as fits
import numpy as np
import glob
import time
import sys, os
#get file name
year=glob.glob['2*']
#time resolution
t=0.005
#get the path
cur = os.getcwd()
for k in year:
    #make a new file
    os.system('mkdir'+' '+'lc_'+k)
    #get file name
    source = glob.glob(cur+'/'+k+'/b*')

    for m in range(len(source)):
        #if the file has already been created,go to creat the next one
        if os.path.exists(cur+'/'+'lc_'+k+'/'+source[m].split('/')[-1])==True:
            m=m+1
        else:
           

            os.system('mkdir'+' '+'lc_'+k+'/'+source[m].split('/')[-1])
            detector = glob.glob(source[m]+'/current/*tte*na*fit')
            for j in detector:
                start = time.time()
                try:
                    hdu = fits.open(j)
                except:
                    continue
                else:
                    a=hdu[2].data[:]['TIME  ']
                    #get the number of bins
                    n=int(round((np.max(a)-np.min(a))/t))
                    #rebin due to time
                    b=np.histogram(a,bins=n)
                    name='lc_'+k+'/'+source[m].split('/')[-1]+'/'
                    np.savetxt(name+'rebin.txt',b[0])
                    np.savetxt(name+'energyedge.txt',hdu[1].data)
                print time.time()-start

