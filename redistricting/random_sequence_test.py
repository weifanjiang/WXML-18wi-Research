# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 22:22:28 2018

@author: Langley
"""
import numpy as np
from scipy.stats import chisquare

def test_independence(sequence, step_size):
    
    x=[]
    for j in range(0,step_size):
        seq=[]
        for i in range(j,len(sequence),step_size):
            seq.append(int(sequence[i]))
        x.append(seq)
            
    idx = {}
    for seq in x:
        for val in seq:
            if not val in idx:
                idx[val]= len(idx)
    
    
    catagories = [[0 for j in range(len(idx))]for i in range(len(idx))]
    
    for seq in x:
        for i in range(1,len(seq)):
         catagories[idx[seq[i]]][idx[seq[i-1]]] += 1;
    
    freqs =  np.array(catagories)/np.sum(catagories)
    
    expected = np.array([[0 for j in range(len(idx))]for i in range(len(idx))])
    
    for i in range(len(freqs)):
        for j in range(len(freqs[i])):
            expected[i][j]= np.sum(catagories)*np.sum(freqs[i,:])*np.sum(freqs[:,j])
    
    exp = []
    cat = []
    
    for i in range(len(catagories)):
        for j in range(len(catagories[i])):
            if catagories[i][j]>0 and expected[i][j]>0:
                cat.append(catagories[i][j])
                exp.append(expected[i][j])
            else:
                cat.append(1)
                exp.append(1)
    return chisquare(cat, f_exp=exp).pvalue