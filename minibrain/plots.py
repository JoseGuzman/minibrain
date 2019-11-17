"""
plots.py

Jose Guzman, sjm.guzman@gmail.com

Created: Tue Sep 25 15:02:38 CEST 2018

Custom functions for plots and hipothesis testing
"""

import numpy as np

from scipy.stats import linregress, norm
from scipy.stats import t as T

import matplotlib.pyplot as plt

def plot_bars(bar, mylabels, mycolors):
    """
    Bar plots

    Arguments:
    data   -- a list containing the arrays of data to plot
    mylabels -- a list of string containig the variables
    mycolors -- a list of strings containgin colors
    """
    fig = plt.figure(1)#, figsize=(5,3))
    ax = fig.add_subplot(111)

    y_loc = (1,2)
    ydata = np.mean(mylabels[0]), np.mean(mylabels[1])
    ax.bar(y_loc, ydata, align='center', color = mycolors, alpha=.1)

    # remove axis
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    return(ax)

def plot_boxes(data, mylabels, mycolors):
    """
    Plots box

    Arguments:
    data   -- a list containing the arrays of data to plot
    mylabels -- a list of string containig the variables
    mycolors -- a list of strings containgin colors
    """
    fig = plt.figure(1)#, figsize=(5,3))
    ax = fig.add_subplot(111)

    # Box plots
    bp = ax.boxplot(data, widths = 0.45, patch_artist=1)
    # add sample size to labels
    xlabels = list()
    for i in range(len(data)):
        xlabels.append(mylabels[i] + '\n(n=' + str(len(data[i])) + ')')
    ax.set_xticklabels(xlabels)

    for patch, color in zip(bp['boxes'], mycolors):
        patch.set_facecolor(color)
        patch.set_edgecolor('black')
        patch.set_alpha(0.1)
        patch.set_linewidth(2)

    for patch in bp['whiskers']:
        patch.set(color='black', lw=3, ls='-')

    for cap in bp['caps']:
        cap.set(color='black', lw=3)

    for patch, color in zip(bp['medians'], mycolors):
        patch.set_color(color)
        patch.set_linewidth(3)

    # plot data
    mean = 1
    for points, color in zip(data, mycolors):
        xval = np.random.normal(loc = mean, scale = .045, size=len(points))
        mean +=1
        ax.plot(xval, points, 'o', color=color, ms=5)

    # remove axis
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    #ax.tick_params(axis='both', direction='out')
    # remove top axis and right axes ticks
    #ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    return(ax)

    
def plot_linregress(xdata, ydata, ax = None, color = None, title = None):
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
    A table with parameters for linear fit of xdata and ydata
    """
    if ax is None:
        ax = plt.gca() # if not give, get current axis

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
    
    ax.set_title(title, color = color)
    ax.plot(xdata, ydata, 'o', color = color, markersize=5)
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

    # stdout statistic
    infostats = [
        (title, 'value'),
        ('Slope', m), 
        ('Intercept', a), 
        ('Correlation coef', rval), 
        ('P-value (slope=0)', pval),
        ('Standard error', stderr),
        ('Samples', n)
    ]
    #print AsciiTable(infostats).table

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
