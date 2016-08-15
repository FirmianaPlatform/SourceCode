import numpy
import math
import sys, os
from math import sqrt
from scipy.special import erfc
import numpy as np
from numpy import array
from numpy import percentile
'''    
def quantile(data, q, precision=1.0):
    """
    Returns the q'th percentile of the distribution given in the argument
    'data'. Uses the 'precision' parameter to control the noise level.
    """
    N, bins = np.histogram(data, bins=precision * np.sqrt(len(data)))
    norm_cumul = 1.0 * N.cumsum() / len(data)
 
    return bins[norm_cumul > q][0]
'''
def quantile(data, q_list):
    data.sort()
    res = []
    for q in q_list:
        if q == 0:
            res.append(data[0])
            continue
        if q == 1:
            res.append(data[-1])
            continue
        L = len(data)
        Q = (L+1)*q
        iQ = int(Q)
        tmp = data[iQ-1] + (data[iQ]-data[iQ-1])*(Q-iQ)
        res.append(tmp)
        
    return res
  
def signif(ratio_list, inten_list):
   
    protNum = len(ratio_list)
    pvalue_list = [0 for i in range(protNum)]
    
    if protNum <= 300:
#         r1 = quantile(ratio_list, 0.1587)
#         r0 = quantile(ratio_list, 0.5000)
#         r2 = quantile(ratio_list, 0.8413)
        q_list = [0.1587, 0.5000, 0.8413]
        r1, r0, r2 = quantile(ratio_list, q_list)
        
        for i in range(protNum):
            if ratio_list[i] < r0:
                z = (r0 - ratio_list[i]) / (r0 - r1) if r0 != r1 else 0
            else:
                z = (ratio_list[i] - r0) / (r2 - r0) if r0 != r2 else 0
            
            pvalue_list[i] = float(0.5 * erfc(z / sqrt(2)))
            
    else:
        ratio_inten = []
        for i in range(protNum):
            ratio_inten.append((ratio_list[i], inten_list[i]))
        ratio_inten.sort(key=lambda x:x[1])

        ratio_sort = [r[0] for r in ratio_inten]
        
        index = array(inten_list).ravel().argsort()
        
        for i in range(protNum):
            left_idx = max(0, i - 150)
            right_idx = min(left_idx + 299, protNum - 1)
  
#             r1 = quantile(ratio_sort[left_idx:right_idx], 0.1587)
#             r0 = quantile(ratio_sort[left_idx:right_idx], 0.5000)
#             r2 = quantile(ratio_sort[left_idx:right_idx], 0.8413)
            q_list = [0.1587, 0.5000, 0.8413]
            r1, r0, r2 = quantile(ratio_sort[left_idx:right_idx], q_list)
  
            if ratio_sort[i] < r0:
                z = (r0 - ratio_sort[i]) / (r0 - r1) if r0 != r1 else 0
            else:
                z = (ratio_sort[i] - r0) / (r2 - r0) if r0 != r2 else 0
            
            pvalue_list[index[i]] = float(0.5 * erfc(z / sqrt(2)))
          
    return pvalue_list

def refine_data(ctrl_list, expr_list):
    '''
    x[is.na(x)] <- 0
    y[is.na(y)] <- 0
    threshold <- min(c(x[x != 0], y[y != 0]))
    x[x == 0] <- threshold / 2
    y[y == 0] <- threshold / 2
  
    avg <- apply(cbind(x, y), 1, mean)
    ratio <- y / x
    '''
    length = len(ctrl_list)
    #===========================================================================
    # 
    # for i in range(length):
    #     ctrl_list[i] = math.log(ctrl_list[i],2) if ctrl_list[i]>0 else 0
    #     expr_list[i] = math.log(expr_list[i],2) if expr_list[i]>0 else 0
    #===========================================================================
        
    tmp = set()
    for i in range(length):
        if ctrl_list[i]>0 : tmp.add(ctrl_list[i])
        if expr_list[i]>0 : tmp.add(expr_list[i])
    
    threshold = min(tmp)
    #print threshold
    for i in range(length):
        if ctrl_list[i]<=0 : ctrl_list[i] = threshold / 2.0
        if expr_list[i]<=0 : expr_list[i] = threshold / 2.0
        
    avg = []
    for i in range(length):
        avg.append( (expr_list[i]+ctrl_list[i])/2.0 )
    
    ratio = []
    for i in range(length):
        ratio_tmp = expr_list[i]/ctrl_list[i]     
        ratio.append( ratio_tmp )
    
    return ratio, avg


def __main__():
    
    
#===============================================================================
#     ctrl_file = 'ctrl.txt'
#     expr_file = 'expr.txt'
#     
#     ctrl_list = []
#     expr_list = []
# 
# 
#     f = open(ctrl_file, 'r')
#     for line in f:
#         tmp = line.split('\n')[0]
#         tmp = line.split('\r')[0]
#         if tmp == '':continue
#         ctrl_list.append(float(tmp))
#     f.close()
#     
#     f = open(expr_file, 'r')
#     for line in f:
#         tmp = line.split('\n')[0]
#         tmp = line.split('\r')[0]
#         if tmp == '':continue
#         expr_list.append(float(tmp))
#     f.close()
#   
#     if len(ctrl_list) != len(expr_list):
#         print 'ctrl_list != expr_list'
#         exit(0) 
#     print 'Length of ctrl_list=', len(ctrl_list)
#===============================================================================
    ctrl_list = [0,2,2222222,2,3,1]
    expr_list = [2,3,0,2,3,4]
    ratio_list, inten_list = refine_data(ctrl_list, expr_list)
    
    pvalue_list = signif(ratio_list, inten_list)
    f=open('3.txt','w')
    
    for line in  pvalue_list:
        f.write(line+'\n')
    f.close()
    #print pvalue_list
    #===========================================================================
    # i = 0
    # f = open('pvalue.txt', 'w')
    # for i in range(len(ratio_list)):
    #     f.write(str(ratio_list[i]) + '\t' + str(pvalue_list[i]) + '\n') 
    # f.close()
    #===========================================================================
    
if __name__ == '__main__':__main__()
