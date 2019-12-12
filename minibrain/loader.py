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
import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

class EphysLoader(object):
    """
    A class to load extracellular recordings acquired
    with the probes silicon probes from Cambridge Neurotech 
    """
    # A dictionary with shanks ID and colors
    shank = {'A': range(16),
             'B': range(16,32),
             'C': range(32,48),
             'D': range(48,64),
             'E': range(64,80),
             'F': range(80,96),
             'G': range(96,112),
             'H': range(112,128)
            }

    color = {'A': '#0080FF',
             'B': '#FF0000',
             'C': '#FF9933',
             'D': '#00AA00',
             'E': '#FF55FF',
             'F': '#FFFF7F',
             'G': '#55FFFF',
             'H': '#00FF00'
            }

    dt = 1/30.       # in ms
    sf = 30000      # number of samples per second
    gain = 0.195    # uVolts per bit (from Intant) 

    def __init__(self, fname, date = None, birth = None, nchan = 67):
        """
        Reads binary data from Open Ephys acquired with
        the Intan 512ch Recording controller.

        Arguments:
        ----------
        fname (str) -- filename (e.g., 'continuous.dat')
        date (str) -- recording date format (e.g., %Y-%m-%d_%H-%M-%S, 
            like '2019-10-09_15-26-38')
        birth (str) -- birth date format (e.g., '2019-10-07_00_00-00')
        nchan (int)   -- number of channels in recording. It
            is 67 by default (64 ADC + 3 AUX from Intan RHD2000).
        """

        self._nchan = nchan
        #self._fname = fname 
        if date is None or birth is None:
            age = 0
        else:
            myformat = '%Y-%m-%d_%H-%M-%S'
            recdate = datetime.datetime.strptime(date, myformat) 
            birthdate = datetime.datetime.strptime(birth, myformat) 
            delta = recdate-birthdate
            age = delta.days + delta.seconds/(24*60*60)

        self.age = age

        fp = open(fname, 'rb')
        nsamples = os.fstat(fp.fileno()).st_size // (nchan*2)
        self._nsamples = nsamples
        self.seconds = nsamples/self.sf # duration in seconds
        print('Recording duration = %2.4f sec.'%self.seconds )
        print('Recording age      = %2.4f days.'%age )

        # accesss without reading the whole file 
        # np.int16 is Integer (-32768 to 32767)
        self._memmap = np.memmap(fp, np.dtype('i2'), mode = 'r', 
            shape = (nsamples, nchan))

        # we transpose the map to handle 1D NumPy decently 
        # this is the data we will use in the object
        self._data = np.transpose( self._memmap )
        fp.close()

    def savemove(self, ch_list = None, height = 1000, distance = 5):
        """
        Creates a new binary file when removing 
        the artifacts from the file. Artifacts are positive 
        deflections within a distance entered by the user.

        Arguments
        ---------
        ch_list (list) the channels to be cleaned.
        height (float) -- threshold for deleting artifacts (default 1000 uV)
    
        distance (float) -- minimal distance (default 5 ms)

        Returns
        -------
        A raw binary file (prefix cl_) with cleaned artefacts. The 
        artifacts are removed 2x the enter distance (10 ms by default).
        """

        # transform uV into bits (0.195 uV/bit from Intan)
        myheight   = int( height/self.gain )
        mydist = int( distance/self.dt ) # distance in sampling points 

        mydata = np.transpose( self._memmap )

        if ch_list is None:
            mychannel = range(self._nchan)
        else:
            mychannel = ch_list
        
        for channel in mychannel:
            trace = mydata[channel].T # now reads bytes from memory
            peaks = find_peaks(trace,height=myheight,distance = mydist)[0]
            print('%3d artifacts found in channel %3d'
                %(peaks.size, channel))

            if peaks.size >=1:
                shift = np.arange(len(peaks))*mydist*2
                peaks = peaks - shift
                for p in peaks:
                    pstart, pend = p - mydist, p + mydist
                    print('Remove t = %2.4f sec.'%(pstart/self.sf))
                    # rewrite mydata
                    mydata = np.delete(mydata, np.s_[pstart: pend], axis=1)
        
        # save new binary (in bytes)
        newdata = mydata.T
        myfname = 'cl_' + self._fname
        newdata.astype('int16').tofile( myfname )
        print('new raw binary saved as %s '%myfname )

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

    def fig_waveform(self, spk_times, nrandom, channel):
        """
        Plots 2 ms of average voltage of the channel at the times given.

        Arguments:
        ----------
        spk_times (list)  -- sampling points to take
        nrandom (int) -- the number of single random waveforms to plot
        channel (int)  -- the channel to plot 

        Returns the figure to plot
        
        """

        tmax = 2 # in ms
        spk_times = spk_times.astype(int) # cast to int
        time = np.linspace(start = 0, stop = tmax, num = tmax/self.dt)
        phalf = int((tmax/2)/self.dt)

        uvolt = self.channel(channel)
        avg = np.mean([uvolt[p-phalf:p+phalf] for p in spk_times],0)

        # plot average waveform
        fig = plt.figure(figsize = (5,6))
        ax = plt.subplot(111)

        # take n random waveforms
        for peak in np.random.choice(spk_times, nrandom):
            wave = uvolt[peak-phalf:peak+phalf]
            ax.plot(time, wave, lw=0.5, color='#999999')

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
        
        
    def fig_shank(self, spk_times, shankID):
        """
        Plots 5 ms of average voltage of the shank at the times given.

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
    # getter for the number of samples channels
    nsamples = property(lambda self: self._nsamples)
