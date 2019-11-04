import logging, argparse
import numpy as np
from exp_FDR_batch_new import*
from plot_batch_results import*
from toimport import *


def main():

    if not os.path.exists('./dat'):
        os.makedirs('./dat')

    #########%%%%%%  SET PARAMETERS FOR RUNNING EXPERIMENT %%%%%%%##########

    FDRrange = str2list(args.FDRrange)
    pirange = str2list(args.pirange, 'float')
    mu_gap = args.mu_gap
    lag_list = str2list(args.lag, 'int')
    batch_size_list = str2list(args.batch_size, 'int')
    hyprange = [0]

    ########%%%%%%%%%%%%%%%%% RUN EXPERIMENT %%%%%%%%########################

    for pi in pirange:
        # Run single FDR
        for FDR in FDRrange:
            for lag in lag_list:
                for batch_size in batch_size_list:
                    # Prevent from running if data already exists
                    filename_pre = 'MG%.1f_Si1.0_FDR%d_NH%d_ND%d_L%d_MINI%d_PM%.2f_NR%d' % (args.mu_gap, FDR, args.num_hyp, 1, lag, batch_size, pi, args.num_runs)
                    all_filenames = [filename for filename in os.listdir('./dat') if filename.startswith(filename_pre)]

                    # Run experiment if data doesn't exist yet
                    if all_filenames == []:
                        print("Running experiment for FDR procedure %s and pi %.1f with lag %d and batch size %d" % (proc_list[FDR], pi, lag, batch_size))
                        run_single(args.num_runs, args.num_hyp, 1, mu_gap, pi, args.alpha0, lag, batch_size, FDR, sigma = 1, verbose = False)
                    else:
                        print("Experiments for FDR procedure %s and pi %.1f with lag %d and batch size %d are already run" % (proc_list[FDR], pi, lag, batch_size))

    # Plot different measures over hypotheses for different FDR
    print("Now plotting ... ")
    plot_results(FDRrange, pirange, mu_gap, 1, args.num_hyp, lag_list, batch_size_list)
            


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--FDRrange', type=str, default = '1') # choice of algorithms and parameters (listed in exp_FDR_batch_new)
    parser.add_argument('--num-runs', type=int, default = 200) # number of independent trials
    parser.add_argument('--num-hyp', type=int, default = 1000) # number of hypotheses
    parser.add_argument('--alpha0', type=float, default = 0.05) # test level
    parser.add_argument('--mu-gap', type=float, default = 0) # mu_c for gaussian tests
    parser.add_argument('--pirange', type=str, default = '0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9') # range of pi1
    parser.add_argument('--lag', type=str, default='150')
    parser.add_argument('--batch-size', type=str, default='1') # use only with minibatch
    args = parser.parse_args()
    logging.info(args)
    main()


    # FDR = 1 is SAFFRON non-asynchronous for varying lag
    # FDR = 2 is LORD non-asynchronous for varying lag
    # FDR = 3-5 is SAFFRON asynchronous without varying lag
    # FDR = 6-8 is LORD asynchronous without varying lag
    # FDR = 10 is LORD mini-batch
    # FDR = 11 is SAFFRON mini-batch
    # FDR = 12 is original LORD under dependence
    # FDR = 13 is Bonferroni
    # FDR = 14 is uncorrected testing
