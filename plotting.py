import numpy as np
from numpy import sqrt, log, exp, mean, cumsum, sum, zeros, ones, argsort, argmin, argmax, array, maximum, concatenate
from numpy.random import randn, rand
np.set_printoptions(precision = 4)

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['font.family'] = 'STIXGeneral'
mpl.rcParams['font.size'] = 14
mpl.rcParams['axes.labelsize'] = 36
mpl.rcParams['xtick.labelsize']= 28
mpl.rcParams['ytick.labelsize']= 28

import matplotlib.pyplot as plt
plt.switch_backend('agg')
pgf_with_rc_fonts = {"pgf.texsystem": "pdflatex"}
matplotlib.rcParams.update(pgf_with_rc_fonts)

from matplotlib import rc
# rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)


# Plot colors and styles (the ones below appear in the paper)

# for normal plots
# plot_style = ['-',  '--', '-.', ':','-','-'] # varying aggressiveness
# plot_style = ['-.', '-']
plot_style = ['-', '-', '--', '-.','-.','-','-'] # for algs under dependence
plot_col = ['firebrick', 'indigo','darkviolet', 'green', 'peru'] # SAFFRON, LORD, Alpha-spending, uncorrrected
# plot_col = ['mediumslateblue', 'mediumorchid', 'darkviolet', 'indigo', 'green','peru'] # LORD w uncorrected/alpha-spending colors
# plot_col = ['peachpuff','gold', 'firebrick','maroon','green','peru'] # SAFFRON w uncorrected/alpha-spending colors
plot_mark = [ 'x', 'o', '^', 'v', 'D', 'x', '+']
plots_ind = 1

def saveplot(direc, filename, lgd, ext = 'pdf',  close = True, verbose = True):
    filename = "%s.%s" % (filename, ext)
    if not os.path.exists(direc):
        os.makedirs(direc)
    savepath = os.path.join(direc, filename)
    plt.savefig(savepath, bbox_extra_artists=(lgd,), bbox_inches='tight')
    if verbose:
        print("Saving figure to %s" % savepath)
    if close:
        plt.close()


def plot_errors_mat(xs, matrix_av, matrix_err, labels, dirname, filename, xlabel, ylabel):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    no_lines = len(matrix_av)
    for i in range(no_lines):
            ys = np.array(matrix_av[i])
            zs = np.array(matrix_err[i])
            ax.errorbar(xs, ys, yerr = zs, color = plot_col[i % len(plot_col)], marker = plot_mark[i % len(plot_mark)], linestyle = plot_style[i % len(plot_style)], lw= 3, markersize =10, label=labels[i])
    lgd = ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, handletextpad=0.3,
                       ncol=min(no_lines,1), mode="expand", borderaxespad=0., prop={'size': 18})
    ax.set_xlabel(xlabel, labelpad=10)
    ax.set_ylabel(ylabel, labelpad=10)
    ax.set_xlim((min(xs), max(xs)))
    if ylabel == 'Power': # for power
        ax.set_ylim((0, 1))
    else: # for FDR and mFDR
        ax.set_ylim((0, 0.5))
    ax.grid(True)
    saveplot(dirname, filename, lgd)