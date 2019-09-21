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
from scipy.signal import find_peaks

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

    dt = 1/30       # in ms
    sf = 30000      # number of samples per second
    gain = 0.195    # uVolts per bit (from Intant) 


    def __init__(self, fname, nchan = 67 ):
        """
        Reads binary data from Open Ephys acquired with
        the Intan 512ch Recording controller.

        Arguments:
        ----------
        fname (str) -- filename (e.g., 'continuous.dat')
        nchan (int)   -- number of channels in recording. It
            is 67 by default (64 ADC + 3 AUX from Intan RHD2000).
        """

        self._nchan = nchan
        self._fname = fname 
        fp = open(fname, 'rb')
        nsamples = os.fstat(fp.fileno()).st_size // (nchan*2)

        # accesss without reading the whole file 
        # np.int16 is Integer (-32768 to 32767)
        self._memmap = np.memmap(fp, np.dtype('i2'), mode = 'r', 
            shape = (nsamples, nchan))

        # we transpose the map to handle 1D NumPy decently 
        # this is the data we will use in the object
        self._data = np.transpose( self._memmap )
        fp.close()

    def savemove(self, height = 1000, distance = 5):
        """
        Creates a new binary file when removing 
        the artifacts from the file. Artifacts are negative
        deflections within a distance entered by the user.

        Arguments
        ---------
        fname (str) -- filename (e.g., 'cl_continuous.dat')
        height (float) -- threshold for detecting artifacts (default 1000 uV)
        distance (float) -- minimal distance (default 5 ms)

        Returns
        -------
        A raw binary file (prefix clean_) with cleaned artefacts
        """

        # transform uV into bits (0.195 uV/bit from Intan)
        myheight   = int( height/self.gain )
        mydist = int( distance/self.dt ) # distance in ms

        mydata = np.transpose( self._memmap )

        
        for channel in range(self._nchan):
            mych = mydata[channel].T # now reads bytes from memory
            peaks = find_peaks(-mych, height=myheight, distance = mydist)[0]
            print('%3d artifacts found in channel %3d'
                %(peaks.size, channel))

            if peaks.size >=1:
                shift = np.arange(len(peaks))*mydist*2
                peaks = peaks - shift
                for p in peaks:
                    pstart, pend = p - mydist, p + mydist
                    mydata = np.delete(mydata, np.s_[pstart: pend], axis=1)
        
        # save new binary (in bytes)
        newdata = mydata.T
        newdata.astype('int16').tofile('clean_' + self._fname)
        print('new raw binary saved as %s '%('clean_' + self._fname))

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
        # traspose to have 1D Numpy
        return self.gain*self._data[channel].T 

    def fig_waveform(self, spk_times, channelID):
        """
        Plots 2 ms of average voltage of the channel at the times given.

        Arguments:
        ----------
        spk_times (list)  -- sampling points to take
        shankID (char)  -- 'A', 'B', 'C', or 'D'

        Returns the figure to plot
        
        """

        tmax = 2 # in ms
        spk_times = spk_times.astype(int) # cast to int
        time = np.linspace(start = 0, stop = tmax, num = tmax/self.dt)
        phalf = int((tmax/2)/self.dt)

        uvolt = self.channel(channelID)
        avg = np.mean([uvolt[p-phalf:p+phalf] for p in spk_times],0)

        # plot average waveform
        fig = plt.figure(figsize = (5,6))
        ax = plt.subplot(111)

        # take 11 random waveforms
        #for peak in np.random.choice(spk_times, 10):
        #    wave = uvolt[peak-phalf:peak+phalf]
        #    ax.plot(time, wave, lw=0.5, color='gray')

        ax.plot(time, avg, color = 'k', lw=2) 
        ax.set_ylim(top = 30, bottom = -90)
        ax.axis('off')

        # plot scalebar
        # horizontal (time)
        ax.hlines(y=-50, xmin=1.2, xmax=2.2, lw=2, color='k') # 2 ms
        ax.text(s='1 ms', y=-60, x=1.7, horizontalalignment='center')
        # vertical (voltage)
        ax.vlines(x = 2.2, ymin = -50, ymax=0, lw=2, color='k')  # 50 uV
        ax.text(s='50 $\mu$V', y= -25, x=2.5, verticalalignment='center')

        return( fig )
        
        
    def fig_insets(self, spk_times, shankID):
        """
        Plots 5 ms of average voltage of the probe at the times given.

        Arguments:
        ----------
        spk_times (list)  -- sampling points to take
        shankID (char)  -- 'A', 'B', 'C', or 'D'

        Returns the figure to plot
        
        """
        spk_times = spk_times.astype(int) # cast to int
        time = np.linspace(start = 0, stop = 5, num = 5/self.dt)
        phalf = int(2.5/self.dt)

        fig = plt.figure(figsize = (4,16))

        mysubplot = 1
        for ch in self.shank[shankID]:
            uvolt = self.channel(ch)
            avg = np.mean([uvolt[p-phalf:p+phalf] for p in spk_times],0)
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
    channel = property(lambda self: self.get_channel)

