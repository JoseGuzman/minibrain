"""
loader.py

Jose Guzman, jose.guzman@guzman-lab.com

Created: Tue Jun 11 17:35:00 CEST 2019

Contains a class to load binary files recorded with Open Ephys

Example:
>>> from loader import DataLoader
>>> myrec = DataLoader('continuous.dat')
# to get one sec array at 30 kHz
>>> myrec.get_channel(channel = 25)[:30000] 
# to plot shankB on given times
>>> myrec.plot_insets(spk_times = [496,7161,16206,24804]'B')

"""

import os
import numpy as np
import matplotlib.pyplot as plt

class EphysLoader(object):
    """
    A class to load extracellular recordings acquired
    with 64 probes silicon probes from Cambridge Neurotech 
    """
    # A dictionary with shanks ID and colors
    shank = {'A': range(16),
             'B': range(16,32),
             'C': range(32,48),
             'D': range(48,64)
            }
    color = {'A': '#A52A2A',
             'B': '#0095FF',
             'C': '#FF9933',
             'D': '#00AA00' 
            }
    dt = 1/30 # in ms


    def __init__(self, fname, numchan = 67 ):
        """
        Reads binary data from Open Ephys 

        Arguments:
        ----------
        fname (str) -- filename (e.g., 'continuous.dat')
        numchan (int)   -- number of channels in recording. It
            is 67 by default (64 ADC + 3 AUX from Intan RHD2000).
        """

        fp = open(fname, 'rb')
        nsamples = os.fstat(fp.fileno()).st_size // (numchan*2)

        samples = np.memmap(fp, np.dtype('i2'), mode = 'r', 
            shape = (nsamples, numchan))

        # binary saved privately here
        self._samples = np.transpose( samples )
        fp.close()

    def get_channel(self, channel):
        """
        Returns a NumPy with the voltages (in microvolts)

        Arguments:
        ----------
        channel (int) -- zero-based ADC channel of Open Ephys

        Returns:
        --------
        A 1D Numpy array with voltage in microVolts
        """
        gain = 0.195 # 0.195 uV per bit
        return gain*self._samples[channel].T # traspose to create 1D- Numpy

    def fig_insets(self, spk_times, shankID):
        """
        Plots the average voltage of the probe at the times given.

        Arguments:
        ----------
        spk_times (list)  -- sampling points to take
        shankID (char)  -- 'A', 'B', 'C', or 'D'

        Returns the figure to plot
        
        """
        time = np.linspace(start = 0, stop = 5, num = 5/self.dt)
        phalf = int(2.5/self.dt)

        fig = plt.figure(figsize = (4,16))

        mysubplot = 1
        for ch in self.shank[shankID]:
            uvolt = self.ADC(ch)
            avg = np.mean([uvolt[p-phalf:p+phalf] for p in spk_times.astype(int)],0)
            ax = plt.subplot(8,1,mysubplot)
            if not ch%2: 
                ax.plot(time, avg, color = self.color[shankID])
                ax.text(s = str(ch), x= 0.5,y =  5, ha = 'center')
            else: # plot down if uneven
                ax.plot(time-5, avg-40, color = self.color[shankID])
                ax.text(s = str(ch), x= -4.5,y = -35, ha = 'center')
                mysubplot +=1 # jump to the next subplot
            ax.set_ylim(top = 30, bottom = -90)
            ax.axis('off')
        
        # plot scalebar
        ax = plt.gca()
        ax.hlines(y = -50, xmin = 2, xmax=4, lw=2, color='k') # 2 ms
        ax.vlines(x = 4, ymin = -50, ymax=0, lw=2, color='k')  # 50 uV
        ax.text(s='50 $\mu$V', y= -25, x=4.5, verticalalignment='center')
        ax.text(s='2 ms', y=-70, x=3, horizontalalignment='center')

        return( fig )

    
    # getter for the ADC channels
    ADC = property(lambda self: self.get_channel)

