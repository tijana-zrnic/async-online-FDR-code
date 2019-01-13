### Import Python libraries
import numpy as np
np.set_printoptions(precision = 4)

import sys


### Import utilities for plotting
from plotting import*
from settings_util import*
from toimport import*

pgf_with_rc_fonts = {"pgf.texsystem": "pdflatex"}
matplotlib.rcParams.update(pgf_with_rc_fonts)



def plot_results(FDRrange, pirange, mu_gap, sigma, NUMHYP, lag_list, batch_size_list, NUMDRAWS = 1):

    plot_dirname = './plots'
    numrun = 100000



    TDR_av = []
    TDR_std = []
    FDR_av = []
    FDR_std = []
    mFDR_av = []
    mFDR_std = []
    ind = 0
        
    for index, FDR in enumerate(FDRrange):

        for batch_size in batch_size_list:

            for lag in lag_list:

                if (FDR == 13 or FDR == 14) and (lag > 0 or batch_size >1):
                    continue;

                filename_pre = 'MG%.1f_Si%.1f_FDR%d_NH%d_ND%d_L%d_MINI%d_' % (mu_gap, sigma, FDR, NUMHYP, NUMDRAWS, lag, batch_size)
                all_filenames = [filename for filename in os.listdir('./dat') if filename.startswith(filename_pre)]

                if all_filenames == []:
                    print("No file found!")
                    print(filename_pre)
                    sys.exit()

                # Get different pis
                pos_PM_start = [all_filenames[i].index('PM') for i in range(len(all_filenames))]
                pos_PM_end = [all_filenames[i].index('_NR') for i in range(len(all_filenames))]
                PM_vec = [float(all_filenames[i][pos_PM_start[i] + 2:pos_PM_end[i]]) for i in range(len(all_filenames))]

                order = np.argsort(PM_vec)
                PM_list = sorted(set(np.array(PM_vec)[order]))

                # Initialize result matrices
                TDR_av.append(np.zeros([1, len(PM_list)]))
                TDR_std.append(np.zeros([1, len(PM_list)]))
                FDR_av.append(np.zeros([1, len(PM_list)]))
                FDR_std.append(np.zeros([1, len(PM_list)]))
                mFDR_av.append(np.zeros([1, len(PM_list)]))
                mFDR_std.append(np.zeros([1, len(PM_list)]))
                TDR_vec = np.zeros(len(PM_list))
                FDR_vec = np.zeros(len(PM_list))
                mFDR_vec = np.zeros(len(PM_list))
                TDR_vec_std = np.zeros(len(PM_list))
                FDR_vec_std = np.zeros(len(PM_list))
                mFDR_vec_std = np.zeros(len(PM_list))

                # Merge everything with the same NA and NH
                for k, PM in enumerate(PM_list):
                    indices = np.where(np.array(PM_vec) == PM)[0]
                    result_mat = []
                    result_mat_mfdr = []
                    # Load resultmats and append
                    for j, idx in enumerate(indices):
                        result_mat_cache = np.loadtxt('./dat/%s' % all_filenames[idx])
                        result_mat_cache_mfdr2 = sum(result_mat_cache[1*NUMHYP:2*NUMHYP, :],axis=0)
                        result_mat_cache_mfdr1 = sum(result_mat_cache[2*NUMHYP:3*NUMHYP, :],axis=0)
                        result_mat_cache = result_mat_cache[5*NUMHYP:5*NUMHYP+2,0:200]
                        if (j == 0):
                            result_mat = result_mat_cache
                            result_mat_mfdr = [result_mat_cache_mfdr1,result_mat_cache_mfdr2]
                        else:
                            result_mat = np.c_[result_mat, result_mat_cache]
                            result_mat_mfdr = np.c_[result_mat_mfdr, result_mat_mfdr]

                    numrun = len(result_mat[0])
                    # Get first vector for TDR
                    TDR_vec[k] = np.average(result_mat[0])
                    TDR_vec_std[k] = np.true_divide(np.std(result_mat[0]),np.sqrt(numrun))
                    # FDR
                    FDR_vec[k] = np.average(result_mat[1])
                    FDR_vec_std[k] = np.true_divide(np.std(result_mat[1]), np.sqrt(numrun))
                    # mFDR
                    mFDR_vec[k] = np.average(result_mat_mfdr[0])/max(1,np.average(result_mat_mfdr[1]))
                    mFDR_vec_std[k] = FDR_vec_std[k]
                TDR_av[ind] = [TDR_vec[k] for k in range(len(PM_list))]
                TDR_std[ind] = [TDR_vec_std[k] for k in range(len(PM_list))]
                FDR_av[ind] = [FDR_vec[k] for k in range(len(PM_list))]
                FDR_std[ind] = [FDR_vec_std[k] for k in range(len(PM_list))]
                mFDR_av[ind] = [mFDR_vec[k] for k in range(len(PM_list))]
                mFDR_std[ind] = [mFDR_vec_std[k] for k in range(len(PM_list))]

                ind = ind + 1



    # -------- PLOT ---------------
    xs = PM_list
    x_label = '$\pi_1$'

        # Choose the appropriate legend (the ones below appear in the paper)
        # legends_list = np.array(proc_list).take(FDRrange)
    # legends_list = [r"SAFFRON$_{dep}, L=0$", r"SAFFRON$_{dep}, L=50$", r"SAFFRON$_{dep}, L=100$", r"SAFFRON$_{dep}, L=150$",r"Alpha-spending", r"Uncorrected"]
    # legends_list = [r"SAFFRON$_{async}, p=1$", r"SAFFRON$_{async}, p=1/50$", r"SAFFRON$_{async}, p=1/100$", r"SAFFRON$_{async}, p=1/150$", r"Alpha-spending", r"Uncorrected"]
    # legends_list = [r"LORD$_{dep}, L=0$", r"LORD$_{dep}, L=50$", r"LORD$_{dep}, L=100$", r"LORD$_{dep}, L=150$", r"Alpha-spending", r"Uncorrected"]
    # legends_list = [r"LORD$_{async}, p=1$", r"LORD$_{async}, p=1/50$", r"LORD$_{async}, p=1/100$", r"LORD$_{async}, p=1/150$", r"Alpha-spending", r"Uncorrected"]
    # legends_list = [r"LORD$_{mini}, B=1$", r"LORD$_{mini}, B=50$", r"LORD$_{mini}, B = 100$", r"LORD$_{mini}, B=150$", r"Alpha-spending", r"Uncorrected"]
    legends_list = [r"SAFFRON$_{dep}$", r"LORD$_{dep}$", r"LORD under dependence", r"Alpha-spending", r"Uncorrected"]
    # legends_list = [r"SAFFRON$_{mini}, B=1$", r"SAFFRON$_{mini}, B=50$", r"SAFFRON$_{mini}, B = 100$",
    #                     r"SAFFRON$_{mini}, B=150$", r"Alpha-spending", r"Uncorrected"]

    ##### FDR vs pi #####
    filename = 'FDRvsPI_MG%.1f_Si%.1f_NH%d_ND%d_L%d_MINI%d' %  (mu_gap, sigma, NUMHYP, NUMDRAWS, lag_list[-1], batch_size_list[-1])
    plot_errors_mat(xs, FDR_av, FDR_std, legends_list, plot_dirname, filename, x_label, 'FDR')

     ##### mFDR vs pi #####
    filename = 'MFDRvsPI_MG%.1f_Si%.1f_NH%d_ND%d_L%d_MINI%d' % (mu_gap, sigma, NUMHYP, NUMDRAWS, lag_list[-1], batch_size_list[-1])
    plot_errors_mat(xs, mFDR_av, mFDR_std, legends_list, plot_dirname, filename, x_label, 'mFDR')

    ##### TDR vs pi ####
    filename = 'PowervsPI_MG%.1f_Si%.1f_NH%d_ND%d_L%d_MINI%d' %  (mu_gap, sigma, NUMHYP, NUMDRAWS, lag_list[-1], batch_size_list[-1])
    plot_errors_mat(xs, TDR_av, TDR_std, legends_list, plot_dirname, filename, x_label, 'Power')


