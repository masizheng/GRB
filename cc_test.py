#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 18 10:58:07 2016

@author: masizheng
"""

import numpy as np
import matplotlib.pylab as pl
import math
t = np.linspace(-5,5,1000)
t1 = t
t2 = t+3
f1 = 1000*np.exp(-t1**2)
f2 = 1000*np.exp(-(t2-3)**2)
f1 = np.random.poisson(lam = f1)
f2 = np.random.poisson(lam = f2)
pl.plot(t1,f1)
pl.plot(t2,f2)
pl.show()

maxim = 5
def cc(t1,t2,f1,f2,maxim):
    tot =[]
    for i in np.linspace(-maxim,maxim,int(math.ceil(2*maxim/(t1[1]-t1[0])))):
        t2_move = t2+i
        # assume signal1 is before signal2, for signal 1, common area is index1:-1, for signal 2, common area is 0:index2
        index1 = np.where((t2_move[0]>=t1)==(t2_move[0]>=t1)[0])[0][-1] 
        index2 = np.where((t1[-1]<=t2_move)==(t1[-1]<=t2_move)[-1])[0][0]
        tot += [np.sum(f1[index1:-1]*f2[0:index2])]
    return np.linspace(-maxim,maxim,int(math.ceil(2*maxim/(t1[1]-t[0]))))[np.where(tot==max(tot))]

