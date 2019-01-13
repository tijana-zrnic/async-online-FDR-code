# Bonferroni

import numpy as np
from numpy import sqrt, log, exp, mean, cumsum, sum, zeros, ones, argsort, argmin, argmax, array, maximum


class Uncorrected_proc_batch:


    def __init__(self, alpha0):


        self.alpha0 = alpha0
        self.alpha = self.alpha0*ones(1000)
        self.wealth_vec = zeros(1000)

    def run_fdr(self, pvec):


        # Get rejection
        rej = np.less_equal(pvec,self.alpha0)


        return rej