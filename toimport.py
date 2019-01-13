import numpy as np
import os

# replace with procedure names from exp_FDR_batch_new
proc_list = ['FDR0','FDR1','FDR2','FDR3','FDR4','FDR5','FDR6','FDR7','FDR8','FDR9','FDR10','FDR11','FDR12','FDR13','FDR14','FDR15','FDR16']

def saveres(direc, filename, mat, ext = 'dat', verbose = True):
    filename = "%s.%s" % (filename, ext)
    if not os.path.exists(direc):
        os.makedirs(direc)
    savepath = os.path.join(direc, filename)
    np.savetxt(savepath, mat, fmt='%.3e', delimiter ='\t')
    if verbose:
        print("Saving results to %s" % savepath)
    
def str2list(string, type = 'int'):
    str_arr =  string.split(',')
    if type == 'int':
        str_list = [int(char) for char in str_arr]
    elif type == 'float':
        str_list = [float(char) for char in str_arr]
    return str_list
