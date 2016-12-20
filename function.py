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

<<<<<<< HEAD
"""
extend_energy
"""
import astropy.io.fits as fits
import math
import numpy as np
import glob
import sys, os
import time
from scipy import integrate
def F(x):
    """ Return dI/dE at a specific E
        Input x --Energy
        Output dI/dE /photons*cm^-2*KeV^-1*sr^-1*cm^-2
    """
    return 8.56*(x**-1.4)*S
def N(x):
    """Return photon number at a specific energy according to band GRB model
        Input x--Energy
        Output number of photons
    """
    if x<(alp-beta)*E0:
        return ((0.001*x)**alp)*math.exp(-x/E0)*S
    else:
        return S*(((alp-beta)*E0*0.01)**(alp-beta))*math.exp(beta-alp)*(0.01*x)**beta
def cut(rebin,ener,x):
    """Return CXB,burst and total light curve /number
       Input rebin--the light curve of source__when time resolution is 5ms
             ener--energy range of the source
             x--choose the output
       Output x=0:cc1--CXB__when energy range is 5Kev-200KeV
              x=1:dd1--burst__when energy range is 5Kev-200KeV
              x=2:a--total light curve:CXB+burst
    """
    hh=np.linspace(0,len(a)*t,num=len(a))
    j=[]
    """get trigger time by judging the difference between nearest two points
       when the difference is higher than 5sigma,select the point as a on going burst
       j---difference between nearest two points
       l--the end of burst
       k1--the beginning of burst
    """
    for i in range(len(a)):
        if i<len(a)-1:
            j.append(a[i+1]-a[i])
	else:
            j.append(0)
    
    l=np.max(np.where(j>np.median(j)+5*np.std(j)))
    k1=(np.where(j>np.median(j)+5*np.std(j)))[0][1]
    cc=np.zeros((len(a),1),float)
    dd=np.zeros((len(a),1),float)
    cc1=np.zeros((len(a),1),float)
    dd1=np.zeros((len(a),1),float)
    dd2=np.linspace(a[k1-1],a[l+1],num=l-k1)

    for i in range(k1,l):
        """Return data of burst
        set other parts(CXB) to 0
        """
        dd[i]=a[i]-dd2[i-k1]
    """Return data of CXB
       set other parts(burst) to 0
    """
    for i in range(0,k1):
        cc[i]=a[i]
    for i in range(l,len(a)):
     	cc[i]=a[i]
    #use formular F to get the parament of I(E)
    c=integrate.quad(F,low,top)[0]/integrate.quad(F,np.min(ener[1]),np.max(ener[2]))[0]
    #use band GRB modal to get parament of GRB model
    d=integrate.quad(N,low,top)[0]/integrate.quad(N ,np.min(ener[1]),np.max(ener[2]))[0]
    for i in range(len(a)):
        """Return extended data of CXB and burst
           Output cc1--CXB extended to 5KeV-200KeV
                  dd1---burst extended to 5KeV-200KeV
        """
        if cc[i]==0:
            cc1[i]==0
            dd1[i]=d*dd[i]
        else:
            cc1[i]=cc[i]*c
                        
            dd1[i]==0
    aa=np.zeros((len(a),1),float)
    aa=cc1+dd1
    for i in range(k1,l):
        """Return the whole light curve data
        """
        lc[i]=lc[i]+dd2[i-k1]*c
        cc1[i]=cc1[i]+dd2[i-k1]*c                    
    if x==0:
        return cc1
    if x==1:
        return dd1
    if x==2:
	return lc

=======
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
>>>>>>> c09d43631174bbb1c612c8d1696d0530ff41bfea
