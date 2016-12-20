#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 11:37:59 2016

@author: masizheng
"""

import numpy as np
import matplotlib.pylab as pl
import math
import random

def cc(t1,t2,f1,f2,maxim):
    """
    This function takes in two signals(function of time), as well as the maximum of time difference, 
    then return the real time difference
    
    t1 f1 signal one, t2 f2 signal 2. Assume signal one is before two.
    maxim: the maximum of time difference
    """
    tot =[]
    for i in np.linspace(-maxim,maxim,int(math.ceil(2*maxim/(t1[1]-t1[0])))):
        t2_move = t2+i
        # assume signal1 is before signal2, for signal 1, common area is index1:-1, for signal 2, common area is 0:index2
        index1 = np.where((t2_move[0]>=t1)==(t2_move[0]>=t1)[0])[0][-1] 
        index2 = np.where((t1[-1]<=t2_move)==(t1[-1]<=t2_move)[-1])[0][0]
        tot += [np.sum(f1[index1:-1]*f2[0:index2])]
    return np.linspace(-maxim,maxim,int(math.ceil(2*maxim/(t1[1]-t[0]))))[np.where(tot==max(tot))]

def pos_delay(theta, phi, N):
    '''
    Return an array of time delay of N satellites in the form of
    array[time_delay_1,time_delay_2,...,time_delay_N]
    Input: theta -- the angle between the source and the satellites' orbit
           phi   -- the angle between projection of parallel rays emitted by
                    source on satellite orbit and the first satellite
           N     -- the number of satellites
    Output: an array of time delay of N satellites
    '''
    res=[]
    for i in range(N):
        res.append(1000*R*math.cos(theta)*(-math.cos(phi+i*alpha)+math.cos(phi))/c)
    res=np.array(res)
    return res

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
    delay=pos_delay(theta,phi,N)
    for k in range(N):
        count_temp=[]
        time_temp=[]
        if (((phi+k*alpha)>=(math.pi/2))and((phi+k*alpha)<=(3*math.pi/2))):
            p=0
        else:
            p=math.cos(phi+k*alpha)
        for i in range(amount):
            time_temp.append(time[i]+delay[i])
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
