# Bonferroni

import numpy as np
from numpy import sqrt, log, exp, mean, cumsum, sum, zeros, ones, argsort, argmin, argmax, array, maximum


class BONF_proc_batch:


    def __init__(self, alpha0, numhyp, gamma_vec_exponent):

        tmp = range(1, 10000)

        self.gamma_vec = np.true_divide(np.ones(len(tmp)),
                                        np.power(tmp, gamma_vec_exponent))
        self.gamma_vec = self.gamma_vec / np.float(sum(self.gamma_vec))

        self.alpha0 = alpha0
        self.alpha = np.zeros(numhyp + 1)
        self.alpha[0:2] = [0, self.gamma_vec[0] * self.alpha0]  # vector of alpha_js, first can be ignored

    def run_fdr(self, pvec):

        numhyp = len(pvec)
        rej = np.zeros(numhyp + 1)

        for k in range(0, numhyp):

            # Get rejection
            this_alpha = self.alpha[k + 1]
            rej[k + 1] = (pvec[k] < this_alpha)

            # Calc new alpha
            next_alpha = self.gamma_vec[k + 1] * self.alpha0
            if k < numhyp - 1:
                self.alpha[k + 2] = next_alpha

        rej = rej[1:]
        self.alpha = self.alpha[1:]

        return rej