"""
burstcounter.py

Jose Guzman, jose.guzman@guzman-lab.com

Created: Wed Mar 11 11:49:14 CET 2020

Contains a class to analyze burts from local field potentials (LFP) with  
Cambride Neurotech silicon probes.

Example:
>>> from minibrain import burst
>>> channel10 = # a NumPy array with voltages
>>> myburst = burst(channel10)
>>> myburst[0] # gets the first burst of the channel
>>> myburst[0]
"""

import pickle 
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

from minibrain import lfp # from minibrain.lfpmanager import lfp

class Burst(object):
    """
    A class to count burst in extracellular recordings acquired
    with silicon probes from Cambridge Neurotech.
    """

    def __init__(self, channel = None, upthr = 7, srate = 30000):
        """
        Reads the array and returns the number of burst. A burst
        is detected by taking the wide-band signal and band-pass 
        filter to 150-250 Hz. The squared root of the mean squared 
        (RMS) in segments of 10 ms is calculated and a burst is 
        detected if the RMS > 6 standard deviations 

        Arguments:
        ----------
        channel (array)
            Array with voltages (uV) of the signal
        srate (int)
            The sampling rate of the signal
        upthr (int)
            The upper threshold for the burst detection. By default
            is 7x the standar deviation of the RMS.
        """
        # update upper threshold value
        self.upthr = upthr

        if channel is not None:
            Nyquist = srate/2
        
            self.wband = lfp.decimate(channel, q = 60)

            # 1) 90-250 Hz band-pass filter
            myrecBP = lfp.band_pass(channel,low=90,high=250,srate = srate)

            # 2) Downsample to 500 Hz
            myrecDS = lfp.decimate(myrecBP, q = 60)
            self.srate = int(srate/60) # update sampling rate
            self.bpass = myrecDS

            # square root of the mean squared (RMS)
            mysegment = 0.005*self.srate # 5 ms in sampling points
            myrms = lfp.rms(self.bpass, segment = int(mysegment))
            self.rms = myrms

            # now get burst times 
            self._burst = self.__long_burst(upthr = upthr)

        else:
            self.rate = srate
            self._burst = np.empty((1,2)) # empty NumPy with one element. 
            self.wband = []
            self.bpass = []
            self.rms = []

    def delete(self, index):
        """
        Remove element from the bust in place
        """
        self._burst = np.delete(self._burst, index, axis = 0)

    def save(self, fname):
        """
        Save a hdf5 file with a list of burst obtained in the 
        band-pass (90-250 Hz) signal.
        """
        pstart = int(self.srate) # 1 sec. before peak detection
        pend   = int(1.5*self.srate) # 1.5 after peak detection 
        # select burst periods in down-sampled signal
        mylist = [self.bpass[ b[0]-pstart:b[1]+pend ] for b in self._burst]
    
        with open(fname, 'wb') as fp:
            # protocol 2 to make it compatible with python2
            pickle.dump(mylist, fp, protocol=2)

    def plot(self, index):
        """
        Return three axis with wide-band, band-pass (90-250 Hz) and
        rms from the burst with index.

        Argument
        --------
        index (int)
            the burst nubmer

        Return
        ------
        ax (array)
            An array of axis
        """
        time = np.arange(len(self.wband))/self.srate # time vector
        bstart, bend = self._burst[index]
        pstart = int(bstart - self.srate) # 1 second before beg. of burst
        pend   = int(bend + 1.5*self.srate)# 1.5 seconds after end. of burst

        fig, ax = plt.subplots(3,1, figsize = (16,8), sharex= True)
        fig.suptitle('Burst {:04d}'.format(index))

        # Wide-band signal
        ax[0].plot(time[pstart:pend],self.wband[pstart:pend],lw=1, c='gray')
        ax[0].plot(time[bstart:bend],self.wband[bstart:bend],lw=1,
            c='tab:blue', label = 'wide-band')
        ax[0].set_ylabel('Amplitude \n ($\mu$V)')

        # Band-pass signal
        ax[1].plot(time[pstart:pend],self.bpass[pstart:pend],lw=1, c='gray')
        ax[1].plot(time[bstart:bend],self.bpass[bstart:bend],lw=1,
            c='purple', label = '90-250 Hz')
        ax[1].set_ylabel('Amplitude \n ($\mu$V)')

        # RMS signal
        ax[2].plot(time[pstart:pend],self.rms[pstart:pend],lw=1, c='k')
        ax[2].axhline(y = self.rms.std()*self.upthr, color='darkgreen', 
            lw=2,linestyle = '--', label = str(self.upthr) + '$\sigma$')
        ax[2].axhline(y = self.rms.std()*2, color='brown', lw=2,
            linestyle = '--', label = '2$\sigma$')
        ax[2].set_ylabel('RMS \n ($\mu$V)')
        ax[2].set_xlabel('Time (sec.)')

        for myax in ax:
            myax.legend(frameon = False, loc = 2)

        return ax

    def plot_time(self, tstart, tend):
        """
        Return three axis with wide-band, band-pass (90-250 Hz) and
        rms from the burst.

        Argument
        --------
        tstart: (float) beginning of recording (in sec.)
        tend: (float) end of recording (in sec.)
        
        Return
        ------
        ax (array)
            An array of axis
        """
        time = np.arange(len(self.wband))/self.srate # time vector
        pstart = int(tstart*self.srate)
        pend   = int(tend*self.srate)
        
        fig, ax = plt.subplots(3,1, figsize = (16,8), sharex=True)
        
        ax[0].plot(time[pstart:pend], self.wband[pstart:pend], 
            label = 'wide-band', lw = 1, color='C0')
        ax[0].set_ylabel('Amplitude \n ($\mu$V)')

        ax[1].plot(time[pstart:pend], self.bpass[pstart:pend], 
            label = '90-250 Hz', lw = 1, color='black')
        ax[1].set_ylabel('Amplitude \n ($\mu$V)')

        ax[2].plot(time[pstart:pend], self.rms[pstart:pend], 
            label = 'RMS', lw = 1, color='brown')

        ax[2].axhline(y = self.rms.std()*self.upthr, color='darkgreen', 
            lw=2,linestyle = '--', label = str(self.upthr)+ '$\sigma$')
        ax[2].axhline(y = self.rms.std()*2, color='brown', lw=2,
            linestyle = '--', label = '2$\sigma$')
        ax[2].set_ylabel('RMS \n ($\mu$V)')
        ax[2].set_xlabel('Time (sec.)')

        for myax in ax:
            myax.legend(frameon = False, loc = 2)

        return ax

    def __call__(self, channel = None, upthr = 7, srate = 30000):
        """
        Returns a Burst object
        """
        # create and object and return number of burst
        return Burst(channel, upthr, srate)

    def __len__(self):
        """
        Returns the number of bursts detected
        """
        return len(self._burst)

    def __getitem__(self, index):
        """
        get the beginning and the end of the burst in sampling points
        """
        try:
            return self._burst[index]
        except IndexError: # if not found, return nan
            return np.full(2, np.nan)

    def __setitem__(self, index, pair):
        """
        set the beginning and the end of the burst in sampling points
        """
        self._burst[index] = pair 

    def __long_burst(self, upthr):
        """
        Calculate the beginning and end of a burst based on 6x the
        standard deviation of the signal (generally the RMS). After
        detecting beginning and ends of the burst based on timings
        differences larger than 750 ms, the closest point that crosses
        2x the standard deviation of the signal will be assigned as
        the real beginning and end of the burst.

        Arguments
        ---------
        thr   (int)
        the upper threshold over the squared root of the mean squared 
        (RMS) of a recording to detect a signal.

        Returns
        -------
        A list of (start, end) values containing the samples where 
        start and end are detected in the signal.
        """
        highthr = self.rms.std()*upthr
        lowthr = self.rms.std()*2.0
        p, _ = signal.find_peaks(x = self.rms, height = highthr )

        # calculate big time differences > 750 msec
        dx = np.diff(p)
        idx = np.where(dx>.75*self.srate)[0]
    
        # +1 is the next peak after big time difference
        # add peak 0 because we count first start is the first detected peak
        start = np.concatenate( ([0], idx + 1) )
        try:
            pstart = p[start] # selection from all peaks 
        except IndexError:
            # if index 0 no peak detected
            pstart = np.nan
        else:

            for i, x in enumerate(pstart):
                # take 100 ms window backward
                tmp = self.rms[x-int(0.150*self.srate):x]  
                # values bellow lower threshold
                val, = np.where( tmp>lowthr ) # stackoverlflow: 33747908
                try:
                    pstart[i] -= (int(0.150*self.srate)-val[0])
                except IndexError:
                    pass # do not assign new value if not found

        # the value after the big difference is the last 
        # add last peak detected as the end of a peak
        end = np.concatenate( (idx, [-1]) )
        # selection from all peaks
        try:
            pend = p[end]
        except IndexError:
            # if index 0 no peak detected
            pend = np.nan
        else:

            for i, x in enumerate(pend):
                # read 250 ms forward
                tmp = self.rms[x+int(0.250*self.srate):x:-1] 
                val, = np.where( tmp>lowthr )
                try:
                    # because we look form outside we need to substract
                    pend[i] += (int(0.250*self.srate)-val[0])
                except IndexError:
                    pass # do not assign value if not found

        # return indices of start-end burst periods
        # to unzip start, end = zip(*<list>)
        return np.column_stack( (pstart, pend) )
        #return list( zip(pstart, pend) )
    

# this is the object we will use to calculate bursts 
burst = Burst(upthr = 7, srate = 30000)
