# SAFFRON simulation code

import numpy as np


class SAFFRON_proc_batch:
    def __init__(self, alpha0, numhyp, lbd, gamma_vec_exponent, lag):
        self.alpha0 = alpha0 # FDR level
        self.lbd = lbd # candidate threshold lambda

        # Compute the discount gamma sequence and make it sum to 1
        tmp = range(1, 10000)
        self.gamma_vec = np.true_divide(np.ones(len(tmp)),
                np.power(tmp, gamma_vec_exponent))
        self.gamma_vec = self.gamma_vec / np.float(sum(self.gamma_vec))

        self.w0 = (1 - lbd) * self.alpha0/2 # initial wealth, has to satisfy w0 < (1 - lbd)*alpha0
        self.alpha = np.zeros(numhyp + 1) # vector of test levels alpha_t at every step
        self.alpha[0:2] = [0, self.gamma_vec[0] * self.w0]
        self.lag = lag



    # Computing the number of candidates after each rejection
    def count_candidates(self, last_rej, candidates, timestep):
        ret_val = [];
        for j in range(1,len(last_rej)):
            ret_val = np.append(ret_val, sum(candidates[last_rej[j]+1:timestep + 1]))
        return ret_val.astype(int)

    # Running SAFFRON on pvec
    def run_fdr(self, pvec):
        numhyp = len(pvec)
        last_rej = []
        rej = np.zeros(numhyp + 1 + self.lag)
        candidates = np.zeros(numhyp + 1 + self.lag)

        for k in range(0, numhyp):

            # Get candidate and rejection indicators
            this_alpha = self.alpha[k + 1]
            candidates[k + 1 + self.lag] = (pvec[k] < self.lbd)
            rej[k + 1 + self.lag] = (pvec[k] < this_alpha)

            # Check first rejection
            if (rej[k + 1 + self.lag] == 1):
                last_rej = np.append(last_rej, k + 1 + self.lag).astype(int)

            # # Update wealth
            # wealth = self.wealth_vec[k] - (1 - candidates[k + 1]) * this_alpha + rej[k + 1] * (1 - self.lbd) * (
            # self.alpha0) - rej[k + 1] * flag * self.w0
            # self.wealth_vec[k + 1] = wealth


            candidates_total = sum(candidates[0:k+2])
            zero_gam = self.gamma_vec[k + 1 - (int)(candidates_total)]
            # Update alpha_t
            if len(last_rej) > 0:
                if last_rej[0]<= (k+1):
                    candidates_after_first = sum(candidates[last_rej[0]+1:k+2])
                    first_gam = self.gamma_vec[k + 1 - (last_rej[0]) - (int)(candidates_after_first)]
                else:
                    first_gam = 0
                if len(last_rej) >= 2:
                    sum_gam = self.gamma_vec[(k + 1) * np.ones(len(last_rej)-1, dtype=int) - (last_rej[1:]) - self.count_candidates(last_rej, candidates, k+1)]
                    indic = last_rej<=(k+1)
                    sum_gam = sum(np.multiply(sum_gam, indic[1:]))
                else:
                    sum_gam = 0
                next_alpha = min(self.lbd, zero_gam * self.w0 + ((1-self.lbd)*self.alpha0 - self.w0) * first_gam + (1-self.lbd)*self.alpha0 * sum_gam)
            else:
                next_alpha = min(self.lbd, zero_gam * self.w0)
            if k < numhyp - 1:
                self.alpha[k + 2] = next_alpha



        rej = rej[1 + self.lag:]
        self.alpha = self.alpha[1:]
        return rej

