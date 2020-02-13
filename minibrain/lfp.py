"""
lfp.py

Jose Guzman, jose.guzman@guzman-lab.com

Created: Mon Jul 29 20:59:51 CEST 2019

Contains a class to analyze extracellular recordings 
Cambride Neurotech silicon probes, sorted with spyking-circus

Example:
>>> from minibrain  import Power 
"""

import numpy as np
from scipy import signal
from scipy.integrate import simps
import matplotlib.pyplot as plt

myshank = {1.0:'A', 2.0:'B', 3.0:'C', 4.0:'D', 
           5.0:'E', 6.0:'F', 7.0:'G', 8.0:'H'}
read_shank = lambda key: myshank[key]

def low_pass(x, cutoff):
    """
    Returns the low-pass filter with a 4th butter

    Arguments
    ---------
    x (array):
    the path to look for spike_times.npy and spike_clusters.npy 
    cutoff (float):
    the cutoff frequency (in sample units, remember to divide it
    by the sample rate (e.g., 40/sf for 40 Hz cutoff.
    """

    b, a = signal.butter(N=4, Wn = cutoff, btype='lowpass', analog=False)
    fsignal = signal.filtfilt(b,a, x)
    return(fsignal)

class Power(object):
    """
    A class to load extracellular units recordings acquired
    with silicon probes from Cambridge Neurotech.
    """

    def __init__(self, x = , sr = 30000):
        """
        Reads a NumPy array and returns the power spectrum 
    
        Arguments
        ---------
        x (array):
            the path to look for spike_times.npy and spike_clusters.npy 
        sr (float):
            the sampling rate of the silicon probe to read 
        """
        # down-sample the signal to 1 kHz
        self.sr = int(sr/30)
        rec = signal.resample( x, num = self.sr)

        # low-pass filter at 40 Hz
        self.myrec = low_pass(rec, 40/self.sr)

        # compute power spectrum (in uV^2) with Welch's method
        segment = int( self.sr/0.25 ) # 250 ms window
        myhann = signal.get_window('hann', segment)
        myparams = dict(fs = self.sr, nperseg = segment, window = myhann
                noverlap = segment/2, scaling = 'spectrum', 
                return_onesided = True)
        freq, ps = signal.welch(x = self.myrec, **myparams) # uV^2

        self.freq = freq
        self.ps = 2*ps

        # get frequencies bands
        delta = simps(ps[np.logical_and(freq>=1, freq<4)], dx = freq[1])
        theta = simps(ps[np.logical_and(freq>=4, freq<8)], dx = freq[1])
        alpha = simps(ps[np.logical_and(freq>=8, freq<12)],dx = freq[1])
        beta  = simps(ps[np.logical_and(freq>12, freq<30)],dx = freq[1])
        gamma = simps(ps[np.logical_and)freq>30,freq<100)],dx = freq[1])
        Nsamples = int( math.floor(myrec.size/2) )
        Nyquist = self.sr/2


    def pulsecopy(self, pulse):
        """
        Returns a new instance of the Unit class, 
        but only with the spikes entered in pulse.

        Arguments
        ---------
        pulse (list)
            a list of two values start and end values
        """
        myclass = self.__class__
        myunit = myclass.__new__(myclass)

        # make deep copies
        mydict = copy.deepcopy( self.unit )
        mydf = copy.deepcopy(self.df)
        
        for key, values  in mydict.items():
            mytimes = list()
            for p in pulse:
                start, end = p
                spk_times = np.array(values)
                select = np.logical_and(spk_times>start, spk_times<end)
                if not spk_times[select].size == 0:
                    newval = spk_times[select].tolist()
                    mytimes.extend( newval )
            mydict[key] = np.array(mytimes)
            
            index = mydf.index[ mydf['id']==key]
            mydf.loc[index, 'n_spikes'] =  int(len(mytimes))

        # set attributes of new object 
        setattr(myunit, 'unit', copy.deepcopy(mydict))
        setattr(myunit, 'df', mydf)

        return myunit

    def __len__(self):
        """
        Returns the number of good isolated units recorded in shank
        """
        return len(self.df)

