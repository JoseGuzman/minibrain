"""
lfp.py

Jose Guzman, jose.guzman@guzman-lab.com

Created: Thu Feb 13 10:03:06 CET 2020

Contains a class to analyze local filed potentials with  
Cambride Neurotech silicon probes.

Example:
>>> from minibrain  import Power 
>>> mylfp = Power(data, fs = 30e3)
"""

import numpy as np
from scipy import signal
from scipy.integrate import simps

def fourier_spectrum(data, srate, fmax = None):
    """
    Calculate amplitudes and frequencies of the Fourier transform
    of the signal.
    
    Arguments:
    ----------
    data (array)
        A numpy array in microvolts
    
    srate (int)
        the sampling rate in samples per second
    
    fmax (float)
        the maximal frequency to compute the Fourier coefficients
        
    returns:
    The frequencies and amplitudes extracted from the Fourier coefficients
    until the Nyquist frequency. 
        
    """
    fcoeff = np.fft.fft(data)/data.size
    DC = [np.abs(fcoeff[0])] # DC component
    amp = np.concatenate( (DC, 2*np.abs(fcoeff[1:])) )
    
    Nsamples = int( np.floor(data.size/2) )
    Nyquist = srate/2.
    hz = np.linspace(0, Nyquist, Nsamples + 1)
    dhz = hz[1] # 
    
    # some info
    #print('Nyquist frequency = %d Hz'%Nyquist)
    #print('Spectral resolution = %2.4f Hz'%dhz)    
    
    if fmax is not None:
        # read until fmax frequency
        hz = hz[:int(fmax/dhz)]
    
    # amplitudes only untin Nyquist frequency
    return (hz, amp[:len(hz)])


class Power(object):
    """
    A class to load extracellular units recordings acquired
    with silicon probes from Cambridge Neurotech.
    """

    def __init__(self, data=None, srate = 30000):
        """
        Reads a NumPy array and returns the power spectrum 
    
        Arguments
        ---------
        data (array):
            the channel to analyze the power spectra. 
        srate (float):
            the sampling rate of the silicon probe to read 
        """
        if data is not None:
            mysr = int(srate/30)
            Nyquist = mysr/2

            # 1) down-sample the signal to 1 kHz 
            ds_rec = self.resample(data, num = int(data.size/30) )

            # 2) low-pass filter at 40 Hz
            lp_rec = self.low_pass(ds_rec, 49/Nyquist)

            # 2) compute power spectrum (in uV^2) with Welch's method
            segment = int( mysr*10 ) # 10 seconds window
            freq, ps = self.welch(lp_rec, mysr, segment) # uV^2
            delta = self.get_delta(freq, ps)
        else:
            # zero power and frequencies between 0-100 Hz at 0.2 Hz reso
            freq, ps = np.arange(0,100,.2), np.zeros(int(100/0.2))
            delta = 0.0

        self.freq = freq
        self.ps = ps
        self.delta = delta

        # get frequencies bands with Simpson integration
        delta =simps(self.ps[np.logical_and(freq>=1,freq<=4)],dx=freq[1])
        theta =simps(self.ps[np.logical_and(freq>=4,freq<=8)], dx=freq[1])
        alpha =simps(self.ps[np.logical_and(freq>=8,freq<=12)],dx=freq[1])
        beta  =simps(self.ps[np.logical_and(freq>=12,freq<=30)],dx=freq[1])
        gamma =simps(self.ps[np.logical_and(freq>=30,freq<=100)],dx=freq[1])
        band  =simps(self.ps[np.logical_and(freq>=0,freq<=100)],dx=freq[1])
        
        #self.delta = {'absolute': delta, 'relative': delta/band}

    def __call__(self, data = None, srate = 30000):
        """
        Returns a Power object upon call
        """
        return Power(data,srate) # empty freq and ps

    def get_delta(self, freq, ps):
        """
        Computes the absolute delta power (1-4Hz) calculating
        the area of the power vs frequency with the Simpson method.

        Results are in uV^2
        """
        delta = np.logical_and( freq >= 1, freq <= 4 )
        band = np.logical_and(freq >=0, freq <= 100)
        rdelta = simps( ps[delta] , dx = freq[1])
        rband = simps( ps[band] , dx = freq[1])
        return {'absolute':rdelta, 'relative':rdelta/rband}

    def low_pass(self, data, cutoff):
        """
        Returns the low-pass filter with a 4th butter

        Arguments
        ---------
        data (array):
        the path to look for spike_times.npy and spike_clusters.npy 

        cutoff (float):
        the cutoff frequency (in sample units, remember to divide it
        by the Nyquist frequency in sampling points.

        Example
        -------
        >>> Nyquist = 30000/2
        >>> mycutoff = 100/Nyquist # for 100 Hz low pass filter
        >>> mytrace = low_pass(data = rec, cutoff = mycutoff)
        """
        myparams = dict(btype='lowpass', analog=False)
        # generate filter kernel (a and b)
        b, a = signal.butter(N = 4, Wn = cutoff, **myparams)
        return signal.filtfilt(b,a, data)

    def resample(self, data, num):
        """
        Down sample the data at the size given in num.
        See signal.resample for details.
        """

        return signal.resample(data, num)

    def welch(self, data, srate, segment):
        """
        Computes the Welch's periodogram in segments of the size
        entered in sampling points. It uses a Hann window.
        The spectral resolution is 0.2 Hz by a 5 seconds window.

        Arguments:
        ----------
        data (array)
        A vector containing the voltages

        srate (int)
        The sampling rate
        
        segment (int)
        The number of sampling points to take for the segment.

        Returns:
        --------
        A tuple with frequencies and power (uV**2)
        """
        myhann = signal.get_window('hann', segment)
        myparams = dict(fs = srate, nperseg = segment, window = myhann,
            noverlap = segment/2, scaling = 'spectrum', 
            return_onesided = True)
        
        freq, ps = signal.welch(data, **myparams) # uV^2

        return(freq, 2*ps) # multiply to get negative frequencies

power = Power(data = None, srate = 30000) # empty Power object
