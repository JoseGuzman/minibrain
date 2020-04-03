"""
lfpmanager.py

Jose Guzman, jose.guzman@guzman-lab.com

Created: Wed Mar 11 09:15:13 CET 2020

Contains a class to analyze local filed potentials (LFP) with  
Cambride Neurotech silicon probes.

Example:
>>> from minibrain import lfp # or from minibrain.lfpmanager import lfp

# compute the square root of the mean squared in 5 ms segments
>>> myburst = lfp.ms(data = myarray, segment = 0.005*srate)
"""

import numpy as np
from scipy import signal


class LFP(object):
    """
    A class to handle local field potentials acquired
    with silicon probes from Cambridge Neurotech.
    """

    def __init__(self, srate = 30000):
        """
        Manage data (e.g., NumPy arrays) to analyse
        local field potentials.
    
        Arguments
        ---------
        srate (float):
            the sampling rate of the silicon probe to read 
        """
        self.srate = srate
        self.Nyquist = srate/2

    def rms(self, data, segment):
        """
        Calculates the square root of the mean square (RMS)
        along the segment.

        Arguments
        ---------
        data (array):
        A NumPy array with the data (e.g., voltage in microVolts)

        segment (int):
        The size of the segment to calculate (in sampling points)
        """

        a2 = np.power(data,2)
        kernel = np.ones(segment)/float(segment)
        return np.sqrt( np.convolve(a2, kernel) )

    
    def low_pass(self, data, cutoff, srate = None):
        """
        Returns the low-pass filter with a 4th butter. Applies
        filter twice, once forward and once backward to avoid phase
        distortions (see scipy.signal.filtfilt for details).

        Arguments
        ---------
        data (array):
        A NumPy array with the data (e.g., voltage in microVolts)

        cutoff (float):
        the cutoff frequency (in sample units, remember to divide it
        by the Nyquist frequency in sampling points.

        Example
        -------
        # for 150 Hz low pass filter
        >>> signal_LP = lfp.low_pass(data = rec, cutoff = 150)

        Be carefull when using a signal with a different sampling
        rate than the lfp object
        
        >>> signal_LP = lfp.low_pass(rec, cutoff = 150, srate = 500)
        """
        if srate is None:
            srate = self.srate
            Nyquist = self.Nyquist
        else:
            Nyquist = srate/2

        myparams = dict(btype='lowpass', analog=False)
        mycutoff = cutoff/Nyquist

        # generate filter kernel (a and b)
        b, a = signal.butter(N = 4, Wn = mycutoff, **myparams)

        return signal.filtfilt(b,a, data)

    def band_pass(self, data, low, high, srate = None):
        """
        Returns the band-pass filter with a 4th butter. Applies the 
        filter twice, once forward and once backward to avoid phase
        distortions (see scipy.signal.filtfilt for details).

        Arguments
        ---------
        data :array
            A NumPy array with the data (e.g., voltage in microVolts)

        low : float
            the low frequency 

        high :float
            the low frequency (in sample units, remember to divide it
            by the Nyquist frequency in sampling points.

        Example
        -------
        >>> low  = 90 # for 150 Hz low pass filter
        >>> high = 250 # for 250 Hz high pass filter
        >>> signal_BP = lfp.band_pass(data = rec, low, high)

        Be carefull when using a signal with a different sampling
        rate than the lfp object
        
        >>> signal_BP = lfp.band_pass(rec, low=90, high = 250, srate = 500)
        """
        if srate is None:
            srate = self.srate
            Nyquist = self.Nyquist
        else:
            Nyquist = srate/2

        myparams = dict(btype='bandpass', analog=False)
        low, high = low/Nyquist, high/Nyquist

        # generate filter kernel (a and b)
        b, a = signal.butter(N = 4, Wn = [low, high], **myparams)

        return signal.filtfilt(b,a, data)

    def notch(self, data, band, srate = None):
        """
        Returns the band-stop filter with a 2nd order IIR filter
        with a narrow bandwidht (high quality factor). Applies the 
        filter twice, once forward and once backward to avoid phase
        distortions (see scipy.signal.filtfilt for details).

        Arguments
        ---------
        data :array
            A NumPy array with the data (e.g., voltage in microVolts)

        band : float
            the band-stop frequency 

        Example
        -------
        >>> band  = 50 # for 50 Hz band-stop filter
        >>> signal_BP = lfp.notch(data = rec, band)

        Be carefull when using a signal with a different sampling
        rate than the lfp object
        
        >>> signal_BP = lfp.band_pass(rec, band=50, srate = 500)
        """
        if srate is None:
            srate = self.srate
            Nyquist = self.Nyquist
        else:
            Nyquist = srate/2

        w0 = band/Nyquist
        Q = 30 # quality factor
        # generate filter kernel (a and b)
        b, a = signal.iirnotch(w0, Q)

        return signal.filtfilt(b, a, data)

    def decimate(self, data, q):
        """
        Down-sample the signal after applying an order 8
        Chebyshev type I FIR antialiasing filter. A Hamming window
        is used (see scipy.signal.decimate for details).

        Arguments
        ---------
        data : array_like
            The signal to be downsampled, as a N-dimensional array

        q : int
            The downsampling factor
        
        Returns:
        --------
        The down-sampled signal.
        """
        return signal.decimate(data, q, ftype = 'fir')

    def fourier_spectrum(self, data, fmax = None, srate = None):
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
        The frequencies and amplitudes extracted from the Fourier 
        coefficients until the Nyquist frequency. 
        """
        if srate is None:
            srate = self.srate
            Nyquist = self.Nyquist
        else:
            Nyquist = srate/2

        fcoeff = np.fft.fft(data)/data.size
        DC = [np.abs(fcoeff[0])] # DC component
        amp = np.concatenate( (DC, 2*np.abs(fcoeff[1:])) )
    
        Nsamples = int( np.floor(data.size/2) )
        hz = np.linspace(0, Nyquist, Nsamples + 1)
        dhz = hz[1] # spectral resolution 
    
        # some info
        #print('Nyquist frequency = %d Hz'%Nyquist)
        #print('Spectral resolution = %2.4f Hz'%dhz)    
    
        if fmax is not None:
            # read until fmax frequency
            hz = hz[:int(fmax/dhz)]
    
        # amplitudes until Nyquist frequency
        return (hz, amp[:len(hz)])

    def welch(self, data, segment, srate = None):
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

# this is the object we will use to analyze
lfp = LFP(srate = 30000) # empty LFP object
