# async-online-FDR-code
Code used to reproduce the plots in Asynchronous Online Testing of Multiple Hypotheses.

------------------------------------- README -------------------------------------

Plots are saved as .pdf files in the folder "plots", and simulation data is saved in the folder "dat" as .dat files.

The main file is run_and_plot.py. At the bottom of this file, there are several parameters the user can choose:

1. FDRrange - sequence of numbers corresponding to the algorithms to be run. The list of algorithms is given in exp_FDR_batch_new. For example, to run the minibatch versions of LORD* and SAFFRON*, set the parameter to ’10,11’.

2. num-runs - number of runs over which the FDR, mFDR and power are estimated

3. num-hyp - length of p-value sequence

4. alpha0 - target FDR level

5. mu-gap - determines the mean of Gaussians under the alternative. If set to a value greater than 0, it acts as mu_c in the paper, and if set to 0, the means are normally distributed

6. pirange - sequence of non-null proportions. Best to simply keep it as ‘0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9’, as used for all simulations in the paper

7. lag - sequence of lags of local dependence. If not simulating LORD* and SAFFRON* under dependence, set the parameter to ‘0’.

8. batch_size - sequence of batch sizes. If not simulating the minibatch versions of LORD* and SAFFRON*, set the parameter to ‘1’.

IMPORTANT: The plotting settings are not fully automated. In particular, the graph colors and legends are not automatic. Please adjust these parameters where indicated in files plotting.py and plot_batch_results.py.

