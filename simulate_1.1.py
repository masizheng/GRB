import numpy as np
import math
import os
import glob
import random
# changeable constants
N=4
c=299792458
R=7000000
alpha=2*math.pi/N
t=5

def sim (count, cxb, theta, phi, N):
    '''
    Return an array of N simulated data which satellites receive in the form of
    array[[[time1_1,count1_1],[time1_2,count1_2],...],
          [[time2_1,count2_1],[time2_2,count2_2],...],
           ...]
    Input: count -- an array of a lightcurve of a source
           cxb   -- an array of a lightcurve of cxb
           theta -- the angle between the source and the satellites' orbit
           phi   -- the angle between projection of parallel rays emitted by
                    source on satellite orbit and the first satellite
           N     -- the number of satellites
    Output: an array of N simulated data which satellites receive
    '''
    amount=len(count)
    time=[]
    data=[]
    for i in range(amount):
        time.append(float(t*i))
    time=np.array(time)
    for k in range(N):
        count_temp=[]
        time_temp=[]
        delay=1000*R*math.cos(theta)*(-math.cos(phi+k*alpha)+math.cos(phi))/c
        if (((phi+k*alpha)>=(math.pi/2))and((phi+k*alpha)<=(3*math.pi/2))):
            p=0
        else:
            p=math.cos(phi+k*alpha)
        for i in range(amount):
            time_temp.append(time[i]+delay)
		if ((count[i]*p+cxb[i])>=0):
            	noise=np.random.poisson((count[i]*p+cxb[i]),1)[0]
		else:
			noise=np.random.poisson(0,1)[0]
            count_temp.append(noise)
        count_temp=np.array(count_temp)
        time_temp=np.array(time_temp)
        temp=np.stack((time_temp,count_temp),axis=-1)
        data.append(temp)
    data=np.array(data)
    return data

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
        file_pos.writelines(str(phi+i*alpha)+'\n')
    file_pos.close()
    
    for k in range(N):
        file_out=open('result/'+K.split('/')[1]+'/simulate_'+str(k+1)+'.txt','w')
        np.savetxt(file_out,data[k])
        file_out.close()
        
    file_source.close()
    file_cxb.close()
