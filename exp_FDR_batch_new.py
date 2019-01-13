# Import Python libraries
import numpy as np
from datetime import datetime
np.set_printoptions(precision = 4)

import os
#import matplotlib.pyplot as plt
import scipy.optimize as optim
from scipy.stats import norm
from scipy.stats import bernoulli

# Import FDR procedures
from LORD_batch import*
from SAFFRON_batch import*
from AlphaInvest_batch import*
from SAFFRON_ALPHA_INV import*
from SAFFRON_async_batch import*
from LORD_async_batch import*
from LORD_minibatch import*
from SAFFRON_minibatch import*
from LORD_classic import*
from Bonf_batch import*
from Uncorrected import*

# Import utilities
from rowexp_new_batch import*
from toimport import*
from settings_util import*
  
################ Running entire framework  ####################

def run_single(NUMRUN, NUMHYP, NUMDRAWS, mu_gap, pi, alpha0, lag, batch_size, FDR, sigma = 1, verbose = False, TimeString = False, rndseed = 0, startfac = 0.1):
    
    if rndseed == 0:
        TimeString = True

    ##------------- Setting hypotheses, penalty and prior weights -------------## 
    if TimeString:
        time_str = datetime.today().strftime("%m%d%y_%H%M")
    else:
        time_str = '0'

    Hypo = get_hyp(pi, NUMHYP)
    Hypo = Hypo.astype(int)
    num_alt = np.sum(Hypo)
       
    #### Set file and dirnames ##########
    dir_name = './dat'
    filename = 'MG%.1f_Si%.1f_FDR%d_NH%d_ND%d_L%d_MINI%d_PM%.2f_NR%d_%s' % (mu_gap, sigma, FDR, NUMHYP, NUMDRAWS, lag, batch_size, pi, NUMRUN, time_str)
    
    # ----------- initialize result vectors and mats ------------- ##
    pval_mat = np.zeros([NUMHYP, NUMRUN])
    rej_mat = np.zeros([NUMHYP, NUMRUN])
    alpha_mat = np.zeros([NUMHYP, NUMRUN])
    wealth_mat = np.zeros([NUMHYP, NUMRUN])
    falrej_vec = np.zeros(NUMRUN)
    correj_vec = np.zeros(NUMRUN)
    totrej_vec = np.zeros(NUMRUN)
    FDR_mat = np.zeros([NUMHYP, NUMRUN])
    TDR_mat = np.zeros([NUMHYP, NUMRUN])
    falrej_mat = np.zeros([NUMHYP, NUMRUN])
    correj_mat = np.zeros([NUMHYP, NUMRUN])

    # ----------------- Run experiments (with same mus) ------------------ # 
    for l in range(NUMRUN):

        #%%%%%%%%  Initialize theta_j, FDR and experiments %%%%%%%%#
        # Some random seed
        if (rndseed == 1):
            rndsd = l+50
        else:
            rndsd = None

        # Create a vector of gaps
        if (mu_gap > 0):
            gap = np.ones(NUMHYP)*mu_gap
        elif (mu_gap == 0):
            gap = np.random.randn(NUMHYP)*np.sqrt(2*np.log(NUMHYP))
        this_exp = rowexp_new_batch(NUMHYP, NUMDRAWS, Hypo, 0, gap, lag)

        #%%%%%%%%% Run experiments: Get sample and p-values etc. %%%%%%%%%%%%%
        # Run random experiments with same random seed for all FDR procedures
        this_exp.gauss_two_mix(mu_gap, sigma, lag, batch_size, rndsd)
        pval_mat[:, l] = this_exp.pvec

        # Initialize FDR

        if FDR == 1:
            proc = SAFFRON_proc_batch(alpha0, NUMHYP, 0.5, 1.6, lag)
        elif FDR == 2:
            proc = LORD_proc_batch(alpha0, NUMHYP, startfac, 1.6, lag)
        elif FDR == 3:
            proc = SAFFRON_async_proc_batch(alpha0, NUMHYP,0.5,1.6,1/50)
        elif FDR == 4:
            proc = SAFFRON_async_proc_batch(alpha0, NUMHYP,0.5,1.6,1/100)
        elif FDR == 5:
            proc = SAFFRON_async_proc_batch(alpha0, NUMHYP,0.5,1.6,1/150)
        elif FDR == 6:
            proc = LORD_async_proc_batch(alpha0, NUMHYP, 1.6, 1/50)
        elif FDR == 7:
            proc = LORD_async_proc_batch(alpha0, NUMHYP, 1.6, 1/100)
        elif FDR == 8:
            proc = LORD_async_proc_batch(alpha0, NUMHYP, 1.6, 1/150)
        elif FDR == 9:
            proc = LORD_proc_batch(alpha0, NUMHYP, startfac, 1.6, 0)
        elif FDR == 10:
            proc = LORD_mini_proc_batch(alpha0, NUMHYP, 1.6, batch_size)
        elif FDR == 11:
            proc = SAFFRON_mini_proc_batch(alpha0, NUMHYP, 0.5, 1.6, batch_size)
        elif FDR == 12:
            proc = LORD_classic_proc_batch(alpha0, NUMHYP, startfac, 1.6)
        elif FDR == 13:
            proc = BONF_proc_batch(alpha0, NUMHYP, 1.6)
        elif FDR == 14:
            proc = Uncorrected_proc_batch(alpha0)


        #%%%%%%%%%% Run FDR, get rejection and next alpha %%%%%%%%%%%%
        rej_mat[:, l] = proc.run_fdr(this_exp.pvec)
        alpha_mat[:, l] = proc.alpha

        #%%%%%%%%%%  Save results %%%%%%%%%%%%%%
        falrej_singlerun = np.array(rej_mat[:,l])*np.array(1-Hypo)
        correj_singlerun = np.array(rej_mat[:,l])*np.array(Hypo)
        totrej_singlerun = np.array(rej_mat[:,l])
        falrej_vec[l] = np.sum(falrej_singlerun)
        correj_vec[l] = np.sum(correj_singlerun)
        totrej_vec[l] = np.sum(totrej_singlerun)
        falrej_mat[:, l] = falrej_singlerun

        FDR_vec = np.zeros(NUMHYP)
        for j in range(NUMHYP):
            time_vec = np.arange(NUMHYP) < (j+1)
            FDR_num = np.sum(falrej_singlerun * time_vec)
            FDR_denom = np.sum(totrej_singlerun * time_vec)
            if FDR_denom > 0:
                FDR_vec[j] = np.true_divide(FDR_num, max(1, FDR_denom))
            else:
                FDR_vec[j] = 0

        FDR_mat[:,l] = FDR_vec
        
    # -----------------  Compute average quantities of interest ------------- #


    TDR_vec = np.true_divide(correj_vec, num_alt)
    FDR_vec = [FDR_mat[NUMHYP - 1][l] for l in range(NUMRUN)]

    if verbose == 1:
        print("done with computation")

    # Save data
    data = np.r_[FDR_mat, rej_mat, falrej_mat, pval_mat, alpha_mat, np.expand_dims(TDR_vec, axis=0), np.expand_dims(np.asarray(FDR_vec),axis=0)]
    saveres(dir_name, filename, data)

