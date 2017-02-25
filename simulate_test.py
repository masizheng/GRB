import numpy as np
import math
import os
import glob
import random
import function
# changeable constants
N=4
c=299792458
R=7000000
alpha=2*math.pi/N
t=5


os.system('mkdir'+' '+'result')
detector=glob.glob('data/b*')

for K in detector:
    file_source=open(K+'/burst.txt')
    file_cxb=open(K+'/cxb.txt')

    count=[]
    cxb=[]

    count=np.loadtxt(file_source)
    count=count*1000/t
    
    cxb=np.loadtxt(file_cxb)
    cxb=cxb*1000/t

    theta=random.uniform(-math.pi/2,math.pi/2)
    phi=random.uniform(-alpha/2,alpha/2)
    
    data=sim(count, cxb, theta, phi, N)

    os.system('mkdir'+' '+'result/'+K.split('/')[1])
    file_pos=open('result/'+K.split('/')[1]+'/source_position.txt','w')
    file_pos.writelines(str(theta)+'\n')
    file_pos.writelines(str(phi)+'\n')
    file_pos.close()
    file_pos=open('result/'+K.split('/')[1]+'/satellites_position.txt','w')
    for i in range(N):
        file_pos.writelines(str(i*alpha)+'\n')
    file_pos.close()
    
    for k in range(N):
        file_out=open('result/'+K.split('/')[1]+'/simulate_'+str(k+1)+'.txt','w')
        np.savetxt(file_out,data[k])
        file_out.close()
        
    file_source.close()
    file_cxb.close()
