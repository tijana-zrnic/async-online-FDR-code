import numpy as np


class LORD_classic_proc_batch:


    def __init__(self, alpha0, numhyp, startfac, gamma_vec_exponent):
        self.alpha0 = alpha0
        # discount factor \gamma_m
        tmp = range(1, 10000)
        if (gamma_vec_exponent == 0):
            self.gamma_vec = np.true_divide(np.log(np.maximum(tmp, np.ones(len(tmp)) * 2)),
                                            np.multiply(tmp, np.exp(np.sqrt(np.log(np.maximum(np.ones(len(tmp)),
                                                                                              tmp))))))  # asymptotically optimal for gaussian
        elif (gamma_vec_exponent == -1):
            self.gamma_vec = np.power(np.true_divide(np.log(np.maximum(tmp, 2 * np.ones(len(tmp)))), tmp),
                                      0.5)  # asymptotically optimal for beta
        else:
            self.gamma_vec = np.true_divide(np.ones(len(tmp)),
                                            np.power(tmp, gamma_vec_exponent))
        self.gamma_vec = self.gamma_vec / np.float(sum(self.gamma_vec))


        self.w0 = startfac * self.alpha0
        self.wealth_vec = np.zeros(numhyp + 1)
        self.wealth_vec[0] = self.w0
        self.alpha = np.zeros(numhyp + 1)
        self.alpha[0:2] = [0, self.gamma_vec[0] * self.w0]  # vector of alpha_js, first can be ignored
        self.b0 = self.alpha0

    def run_fdr(self, pvec):

        numhyp = len(pvec)
        last_rej = 0
        rej = np.zeros(numhyp + 1)

        for k in range(0, numhyp):

            if self.wealth_vec[k] > 0:
                # Get rejection
                this_alpha = self.alpha[k + 1]  # make sure first one doesn't do bullshit
                rej[k + 1] = (pvec[k] < this_alpha)

                # Calc wealth
                if (rej[k + 1] == 1):
                    last_rej = k + 1

                # Update wealth
                wealth = self.wealth_vec[k] - this_alpha + rej[k + 1] * self.b0
                self.wealth_vec[k + 1] = wealth

                # Calc new alpha
                # next_alpha = self.gamma_vec[k + 1 - last_rej] * self.wealth_vec[last_rej]
                next_alpha = self.gamma_vec[k+1] * self.wealth_vec[last_rej]
                if k < numhyp - 1:
                    self.alpha[k + 2] = next_alpha
            else:
                break
        rej = rej[1:]
        self.alpha = self.alpha[1:]
        return rej