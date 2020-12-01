"""
plots.py

Author: Jose Guzman, jose.guzman<at>guzman-lab.com

Created: Tue Sep 25 15:02:38 CEST 2018

Custom functions for plots and hypothesis testing
"""

import numpy as np

from scipy.stats import kruskal
from scipy.stats import mannwhitneyu as mwu
from scipy.stats import wilcoxon

from scipy.stats import linregress, norm, sem
from scipy.stats import t as T

import matplotlib.pyplot as plt

def plot_pairs(xdata, ydata, labels, colors, ax = None):
    """
    Generate a bar plot from a list containing the data
    perform a Wilcoxon rank-test to test for paired differences.

    Arguments
    ----------
    xdata   -- a list containing data to plot
    ydata   -- a list containing data to plot
    labels -- a list of string containig the variable names
    colors -- a list of strings containgin colors to plot the bars

    Returns:
    ax: a bar plot with the means, error bars with the standard error
    of the mean, and single data points.
    info: the mean and standard error of the samples, together with the
    the probability that the means are the same.
    """
    ax = ax or plt.gca()

    # single data points and error bars
    mycaps = dict(capsize = 10, elinewidth = 3, markeredgewidth = 3)

    ax.plot(0, np.mean(xdata), 'o', color= colors[0])
    ax.errorbar(0, np.mean(xdata), sem(xdata), **mycaps, color = colors[0])

    ax.plot(1, np.mean(ydata), 'o', color= colors[1])
    ax.errorbar(1, np.mean(ydata), sem(ydata), **mycaps, color = colors[1])

    # single data
    ax.plot(np.ones(len(xdata))*.25, xdata, 'o', color = colors[0])
    ax.plot(np.ones(len(ydata))*.75, ydata, 'o', color = colors[1])

    for i in zip(xdata, ydata):
        ax.plot( [0.25, 0.75], i, color = 'gray', alpha = 0.4)

    # remove axis and adjust
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.get_yaxis().tick_left()

    ax.set_xticklabels(labels, fontsize = 14)
    ax.set_xticks([0,1])
    ax.xaxis.set_ticks_position('none')
    ax.set_xlim(-.5,1.5)

    # statistics
    stats_0 =  ( labels[0],np.mean(xdata), sem(xdata), len(xdata) )
    stats_1 =  ( labels[1],np.mean(ydata), sem(ydata), len(ydata) )
    print('%s = %2.4f +/- %2.4f, n = %d' %stats_0)
    print('%s = %2.4f +/- %2.4f, n = %d' %stats_1)
    w_test = wilcoxon(xdata, ydata, alternative = 'two-sided')[1]
    print(f'P = {w_test:2.4}, Wilcoxon signed-rank test (two-sided W test)\n')
    infostats = {'P-value': w_test}

    return ax, infostats

def plot_bars(xdata, ydata, labels, colors, ax = None):
    """
    Generate a bar plot from a list containing the data
    perform a Mann-Whitney U-test to test for mean differences.

    Arguments
    ----------
    xdata   -- a list containing data to plot
    ydata   -- a list containing data to plot
    labels -- a list of string containig the variable names
    colors -- a list of strings containgin colors to plot the bars

    Returns:
    ax: a bar plot with the means, error bars with the standard error
    of the mean, and single data points.
    info: hhe mean and standard error of the samples, together with the
    the probability that the means are the same.
    """
    if ax is None:
        ax = plt.gca() # if not given, get current axis

    data = [xdata, ydata]

    yloc = (1,2)
    # add sample size to labels
    avg = np.mean(data[0]), np.mean(data[1])
    myparams = dict(width = 0.65, color = colors, align = 'center',
            alpha = 0.5)
    # bar
    ax.bar(yloc, avg, **myparams)

    # single data points and error bars
    mycaps = dict(capsize = 10, elinewidth = 3, markeredgewidth = 3)

    yerr0 = sem(data[0])
    xloc0 = np.random.normal(loc=1, scale=0.09, size = len(data[0]))
    ax.errorbar(yloc[0], avg[0], yerr0, color=colors[0], **mycaps) 
    ax.plot(xloc0, data[0], 'o', ms=4, color='k')

    yerr1 = sem(data[1])
    xloc1 = np.random.normal(loc=2, scale=0.09, size = len(data[1]))
    ax.errorbar(yloc[1], avg[1], yerr1, color=colors[1], **mycaps)
    ax.plot(xloc1, data[1], 'o', ms=4, color='k')
    
    # remove axis and adjust    
    ax.set_xlim(0,3)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # xlabels
    #xlabels = list()
    #for i in enumerate(data):
    #    xlabels.append(labels[i] + '\n(n=' + str(len(data[i])) + ')')
    ax.set_xticklabels(labels, fontsize=14)
    ax.set_xticks([1,2])
    ax.xaxis.set_ticks_position('none')

    # statistics
    stats_0 =  ( labels[0],np.mean(data[0]), sem(data[0]), len(data[0]) )
    stats_1 =  ( labels[1],np.mean(data[1]), sem(data[1]), len(data[1]) )
    print('%s = %2.4f +/- %2.4f, n = %d' %stats_0)
    print('%s = %2.4f +/- %2.4f, n = %d\n' %stats_1)
    u_test = mwu(data[0], data[1], alternative = 'two-sided')[1]
    print('P = %2.4f, Mann-Whitney (two-side U test)'%u_test)

    infostats = {'P-value': u_test}

    return(ax, infostats)

def plot_boxes(xdata, ydata, labels, colors, ax = None):
    """
    Generate a box plot from a list containing the data 
    perform a Mann-Whitney U-test to test for mean differences.

    Arguments:
    xdata   -- a list containing data to plot
    ydata   -- a list containing data to plot
    labels -- a list of string containig the variables
    colors -- a list of strings containgin colors

    Returns:
    ax: a box plots with where the horizontal line is the
    median, boxes the first and third quartiles, and 
    the whiskers the most extreme data points <1.5x
    the interquartile distance form the edges. It also
    show single data form the experiments.

    info: the mean and standard error of the samples, together with the
    the probability that the means are the same.
    """
    if ax is None:
        ax = plt.gca() # if not given, get current axis

    # Box plots (sym = '' do not mark outliners)
    data = [xdata, ydata]
    bp = ax.boxplot(data, widths = 0.45, patch_artist=1, sym='')
    # add sample size to labels

    #xlabels = list()
    #for i in enumerate(data):
    #    xlabels.append(labels[i] + '\n(n=' + str(len(data[i])) + ')')
    #ax.set_xticklabels(labels)

    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_edgecolor('black')
        patch.set_alpha(0.1)
        patch.set_linewidth(2)

    for patch in bp['whiskers']:
        patch.set(color='black', lw=3, ls='-')

    for cap in bp['caps']:
        cap.set(color='black', lw=3)

    for patch, color in zip(bp['medians'], colors):
        patch.set_color(color)
        patch.set_linewidth(3)

    # plot data points 
    mean = 1
    for points, color in zip(data, colors):
        xval = np.random.normal(loc = mean, scale = .045, size=len(points))
        mean +=1
        ax.plot(xval, points, 'o', color=color, ms=4)

    # remove axis and adjust
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.get_yaxis().tick_left()

    # xlabels
    #xlabels = list()
    #for i in enumerate(data):
    #    xlabels.append(labels[i] + '\n(n=' + str(len(data[i])) + ')')
    ax.set_xticklabels(labels, fontsize = 14)
    ax.set_xticks([1,2])
    ax.xaxis.set_ticks_position('none')

    # statistics
    stats_0 =  ( labels[0],np.mean(data[0]), sem(data[0]), len(data[0]) )
    stats_1 =  ( labels[1],np.mean(data[1]), sem(data[1]), len(data[1]) )
    print('%s = %2.4f +/- %2.4f, n = %d' %stats_0)
    print('%s = %2.4f +/- %2.4f, n = %d' %stats_1)
    u_test = mwu(data[0], data[1], alternative = 'two-sided')[1]
    print('P = %2.4f, Mann-Whitney (two-sided U test)\n'%u_test)

    infostats = {'P-value': u_test}

    return(ax, infostats)

    
def plot_linregress(xdata, ydata, color = None, label = None, ax = None):
    """
    plots the linear fit together with the two-side 95% confidence interval.
    For 95% confident interval see:
    https://tomholderness.wordpress.com/2013/01/10/confidence_intervals/
    
    Arguments:
    ----------
    xdata: 1D NumPy array
    ydata: 1D NumPy array
    ax: axis matplotlib object

    Returns:
    --------
    An axis object and a dictionary with linear regression results.
    """
    if ax is None:
        ax = plt.gca() # if not given, get current axis

    m, a, rval, pval, stderr = linregress(xdata, ydata)
        
    # linear function
    f = lambda x: a + m*x
    xfit = np.linspace(xdata.min(), xdata.max(), 100)
    yfit = f(xfit)
    
    y_err = ydata - f(xdata) # residuals
    SSE = np.power(y_err,2).sum() # sum of squared errors

    # calculate confident intervals
    mu = xdata.mean()
    n = xdata.size
    # for a 2-tailed 95% confident interval enter 0.975
    tstat = T.ppf(0.975, n-1) 

    pow2 = lambda x: np.power(x,2)
    confs = tstat*np.sqrt( (SSE/(n-2)) * (1.0/n +\
        (pow2(xfit-mu)/ ((np.sum(pow2(xdata)) -
        n*(pow2(mu)))))))

    lower_conf = yfit - abs(confs)
    upper_conf = yfit + abs(confs)
    
    ax.set_title(label, color = color)
    ax.plot(xdata, ydata, 'o', color = color, markersize=4)
    ax.plot(xfit, yfit, lw=2, color = color)
    ax.plot(xfit, upper_conf, '--', lw=1, color = color)
    ax.plot(xfit, lower_conf, '--', lw=1, color = color)
    ax.fill_between(xfit, upper_conf, lower_conf, color = color,  alpha =.1)

    # axis
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(axis='both', direction='out')
    ax.get_xaxis().tick_bottom() # remove unneed ticks
    ax.get_yaxis().tick_left()

    # statistics
    stats = ( label, np.mean(ydata), sem(ydata), len(ydata) )
    print('%s = %2.4f +/- %2.4f, n = %d' %stats)

    infostats = {
        'Slope': m, 
        'Intercept': a, 
        'Correlation coef': rval, 
        'P-value': pval,
        'Standard error': stderr,
        'Samples': n
    }

    return(ax, infostats)
    
def plot_histogram(data, mybins, myYmax=None, mycolor = None):
    """
    Plot the probability density

    """
    fig = plt.figure()
    loc = [0.1, .5, 0.9, 0.8]
    ax1 = fig.add_axes(loc)
    # fit to a normal distribution
    xfit = np.linspace(0, max(mybins), 100)
    rv = norm(loc = np.mean(data), scale = np.std(data))
    yfit = rv.pdf(xfit) 
    ax1.plot(xfit, yfit, lw=3, color=mycolor)
    ax1.hist(data, mybins, color = mycolor, normed=1, alpha = .3)
    ax1.set_ylim(ymax=myYmax)
    

    loc2 = [0.1, -0.3, 0.9, 0.8]
    ax2 = fig.add_axes(loc2)
    len(data)
    ax2.eventplot(data, colors = [[mycolor]], lineoffsets=1, linelengths =.005)
    ax2.set_xticks(mybins)
    ax2.set_ylim(ymin=0.99)
    ax2.axis('off')


def plot_spike_waveforms(wavelist, color = 'k', ax = None):
    """
    Plots spike waveforms and the resulted averaged
    
    Arguments
    ---------
    wavelist : 2D array
        The array with the waveforms collected 
        (e.g. waveforms.values)

    """
    if wavelist.ndim != 2:
        raise TypeError('wavelist is not 2D array')

    if ax is None:
        ax = plt.gca()

    for wave in wavelist:
        ax.plot(wave, lw = 0.5, color = 'k', alpha = 0.2)
    
    # compute average waveform
    ax.plot(np.mean(wavelist, axis=0), lw = 2, color = color)

    # scalebar and number of waveforms
    ax.text(x = 5 , y = 0.25, s = f'n = {wavelist.shape[0]}' , fontsize = 14)
    ax.hlines(y = -1.1, xmin = 75, xmax = 105, lw = 2 , color='k') 
    ax.text(x = 75, y = -1, s = '1 ms', fontsize = 14)

    # remove axis
    ax.axis('off')

    # set limits
    ax.set_ylim(-1.3, 1.1)

    return ax
