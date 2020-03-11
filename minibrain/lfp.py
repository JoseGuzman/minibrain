"""
lfp.py

Jose Guzman, jose.guzman@guzman-lab.com

Created: Thu Feb 13 10:03:06 CET 2020

Contains a class to analyze local filed potentials (LFP) with  
Cambride Neurotech silicon probes.

Example:
>>> from minibrain.lfp import power 
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
    
    # amplitudes until Nyquist frequency
    return (hz, amp[:len(hz)])

def low_pass(data, cutoff):
    """
    Returns the low-pass filter with a 4th butter

    Arguments
    ---------
    data (array):
    A NumPy array with the data (e.g., voltage in microVolts)

    cutoff (float):
    the cutoff frequency (in sample units, remember to divide it
    by the Nyquist frequency in sampling points.

    Example
    -------
    >>> Nyquist = 30e3/2
    >>> mycutoff = 250/Nyquist # for 250 Hz low pass filter
    >>> mytrace = low_pass(data = rec, cutoff = mycutoff)
    """
    myparams = dict(btype='lowpass', analog=False)
    # generate filter kernel (a and b)
    b, a = signal.butter(N = 4, Wn = cutoff, **myparams)
    return signal.filtfilt(b,a, data)

def band_pass(data, low, high):
    """
    Returns the band-pass filter with a 4th butter

    Arguments
    ---------
    data :array
        A NumPy array with the data (e.g., voltage in microVolts)

    low : float
        the low frequency (in sample units, remember to divide it
        by the Nyquist frequency in sampling points.

    high :float
        the low frequency (in sample units, remember to divide it
        by the Nyquist frequency in sampling points.

    Example
    -------
    >>> Nyquist = 30e3/2
    >>> low  = 150/Nyquist # for 150 Hz low pass filter
    >>> high = 250/Nyquist # for 250 Hz high pass filter
    >>> mytrace = band_pass(data = rec, low, high)
    """
    myparams = dict(btype='bandpass', analog=False)
    # generate filter kernel (a and b)
    b, a = signal.butter(N = 4, Wn = [low, high], **myparams)
    return signal.filtfilt(b,a, data)

def rms(data, segment):
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
    
def get_burst(data, srate):
    """
    Calculate the beginning and end of a burst based on 7x the
    standard deviation of the signal (generally the RMS). After
    detecting beginning and ends of the burst based on timings
    differences larger than 0.5, the closest point that crosses
    2x the standard deviation of the signal will be assigned as
    the real beginning and end of the burst.

    Arguments
    ---------
    data   (array)
        generally the squared root of the mean squared (RMS)

    Returns
    -------
        A (start, end) list containing the samples where start and
        end are detected in the signal.
    """
    mythr = data.std()*2
    p, _ = signal.find_peaks(x = data, height = data.std()*7 )

    # calculate big time differences > 0.5 seg
    dx = np.diff(p)
    idx = np.where(dx>0.5*srate)[0]
    
    # +1 is the next peak after big time difference
    # add peak 0 because we count first start is the first detected peak
    start = np.concatenate( ([0], idx + 1) )
    pstart = p[start] # selection from all peaks 

    for i, x in enumerate(pstart):
        tmp = data[x:x-int(0.05*srate):-1] # take 100 ms window backwards
        val, = np.where( tmp<mythr ) # stackoverlflow: 33747908
        try:
            pstart[i] -= val[0] # first below threshold 
        except IndexError:
            pass # do not assign new value

    # the value after the big difference is the last 
    # add last peak detected as the end of a peak
    end = np.concatenate( (idx, [-1]) )
    pend = p[end] # selection from all peaks

    for i, x in enumerate(pend):
        tmp = data[x:x+int(0.05*srate)] # 50 ms forward
        val, = np.where( tmp<mythr)
        try:
            pend[i] += val[0]
        except IndexError:
            pass # do not assign value

    # return indices of start-end burst periods
    # to unzip start, end = zip(*<list>)
    return list( zip(pstart, pend) )
    
    
class Power(object):
    """
    A class to handle extracellular signals acquired
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
            Nyquist = srate/2

            # 1) low-pass at 500 Hz
            lp_rec = self.low_pass(data, 500/Nyquist)

            # 2) down-sample the signal to 1 kHz 
            ds_rec = self.resample(lp_rec, num = int(data.size/30) )
            newsrate = int(srate/30)

            # 3) compute power spectrum (in uV^2) with Welch's method
            segment = int( newsrate*10 ) # 10 seconds window
            freq, ps = self.welch(ds_rec, newsrate, segment) # uV^2
            delta = self.get_delta(freq, ps)
        else:
            # zero power and frequencies between 0-100 Hz at 0.1 Hz reso
            freq, ps = np.arange(0,100,.1), np.zeros(int(100/0.1))
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
        band  =simps(self.ps[np.logical_and(freq>=0,freq<=500)],dx=freq[1])
        
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


class Burst(object):
    """
    A class to count burst in extracellular recordings acquired
    with silicon probes from Cambridge Neurotech.
    """

    def __init__(self, data = None, srate = 30000):
        """
        Reads the array and returns the number of burst. A burst
        is detected by taking the wide-band signal and band-pass 
        filter to 150-250 Hz. The squared root of the mean squared 
        (RMS) in segments of 10 ms is calculated and a burst is 
        detected if the RMS > 7 standard deviations 
        
        """
        if data is not None:
            Nyquist = srate/2
        
            # 1) 150-250 Hz band-pass filter
            low, high = 90/Nyquist, 250/Nyquist
            myrecBP = band_pass(data, low, high)

            # 2) Downsample to 500 Hz
            myrec = signal.decimate(myrecBP, 60, ftype = 'fir')
            mysrate = srate/60 # update sampling rate

            # square root of the mean squared (RMS)
            mysegment = 0.010*mysrate # 10 ms
            myrms = rms(data = myrec, segment = int(mysegment))

            # now get burst times 
            self.idx = get_burst(data = myrms, srate = mysrate)

        else:
            self.idx = [] # empty list 

    def __call__(self, data = None, srate = 30000):
        """
        Returns a Burst object
        """
        # create and object and return number of burst
        return Burst(data, srate)

    def __len__(self):
        """
        Returns the number of bursts detected
        """
        return len(self.idx)
        

power = Power(data = None, srate = 30000) # empty Power object
