import numpy as np
from scipy.stats import norm
from scipy.linalg import toeplitz


class rowexp_new_batch:

    def __init__(self, NUMHYP, numdraws, alt_vec, mu0, mu_alt_vec, lag):
        self.numhyp = NUMHYP
        self.alt_vec = alt_vec
        self.mu0 = mu0
        self.mu_vec = mu0*np.ones(NUMHYP) + np.multiply(alt_vec, mu_alt_vec)
        self.pvec = np.zeros(NUMHYP)
        self.numdraws = numdraws
        self.lag = lag

        '''
        Function drawing p-values: Mixture of two Gaussians
        '''
    def gauss_two_mix(self, mu_gap, sigma = 1, lag = 0, batch_size = 1, rndsd = 0):

        np.random.seed(rndsd)
        Z = np.zeros(self.numhyp)

        # Draw Z values according to lag
        if (lag == 0 and batch_size == 1):
            Z = self.mu_vec + np.random.randn(self.numhyp)*sigma
        elif (batch_size > 1):
            rho = 0.5
            numbatches = (int)(np.ceil(self.numhyp/batch_size))
            for i in range(numbatches):
                if i < (numbatches -1):
                    rho_vec = [rho ** j for j in range(batch_size)]
                    cov_mat = toeplitz(rho_vec)
                    np.fill_diagonal(cov_mat, 1)
                    Z[i*batch_size:(i+1)*batch_size] = np.random.multivariate_normal(self.mu_vec[i*batch_size:(i+1)*batch_size], cov_mat)
                else:
                    rho_vec = [rho ** j for j in range(1000-i*batch_size)]
                    cov_mat = toeplitz(rho_vec)
                    np.fill_diagonal(cov_mat, 1)
                    Z[i * batch_size:self.numhyp] = np.random.multivariate_normal(self.mu_vec[i * batch_size:self.numhyp], cov_mat)
        else: # Markov dependence
            # # cov_mat = np.ones([lag + 1,lag + 1])*0.2
            # rho = 0.5
            # rho_vec = [rho**i for i in range(lag + 1)]
            # cov_mat = toeplitz(rho_vec)
            # np.fill_diagonal(cov_mat,1)
            # # compute samples before L + 1
            # Z[0:(lag + 1)] = np.random.multivariate_normal(self.mu_vec[0:(lag + 1)], cov_mat)
            # # compute samples after L + 1
            # cov_vec = cov_mat[lag,0:lag]
            # cov_submat = cov_mat[0:lag,0:lag]
            # for i in range(lag + 1,self.numhyp):
            #     mu_i = self.mu_vec[i] + np.dot(np.dot(cov_vec,np.linalg.inv(cov_submat)),(Z[i-lag:i]-self.mu_vec[i-lag:i]))
            #     var_i = sigma*sigma - np.dot(np.dot(cov_vec,np.linalg.inv(cov_submat)),cov_vec)
            #     Z[i] = mu_i + np.random.randn(1)*np.sqrt(var_i)
            # cov_mat = np.ones([lag + 1,lag + 1])*0.2
            # normalvec = np.random.randn(self.numhyp+lag)*np.sqrt(lag + 1)
            # for i in range(self.numhyp):
            #     Z[i] = sum(normalvec[i:i+lag+1])/(lag+1) + self.mu_vec[i]
            # cov_mat = np.ones([lag + 1,lag + 1])*0.2
            # regular local dependence
            rho = 0.5
            rho_vec = [rho**i for i in range(lag + 1)]
            rho_vec = np.concatenate((np.asarray(rho_vec),np.asarray(np.zeros(self.numhyp-lag-1))))
            cov_mat = toeplitz(rho_vec)
            np.fill_diagonal(cov_mat,1)
            Z = np.random.multivariate_normal(self.mu_vec, cov_mat)


        # Compute p-values and save
        if mu_gap > 0:
            self.pvec = [(1 - norm.cdf(z)) for z in Z] # one-sided p-values
        else:
            self.pvec = [2*norm.cdf(-abs(z)) for z in Z] # two-sided p-values