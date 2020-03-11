"""
burstcounter.py

Jose Guzman, jose.guzman@guzman-lab.com

Created: Wed Mar 11 11:49:14 CET 2020

Contains a class to analyze burts from local field potentials (LFP) with  
Cambride Neurotech silicon probes.

Example:
>>> from minibrain import burst
>>> myburst = burst(channel10)
"""
import numpy as np
from scipy import signal

from minibrain import lfp # from minibrain.lfpmanager import lfp

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
        
            # 1) 90-250 Hz band-pass filter
            myrecBP = lfp.band_pass(data, low=90, high=250, srate = srate)

            # 2) Downsample to 500 Hz
            myrecDS = lfp.decimate(data = myrecBP, q = 60)
            mysrate = srate/60 # update sampling rate
            dt = 1/mysrate

            # square root of the mean squared (RMS)
            mysegment = 0.005/dt # 10 ms in sampling points
            myrms = lfp.rms(data = myrecDS, segment = int(mysegment))

            # now get burst times 
            self.idx = extract_burst(data = myrms, srate = mysrate)

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

    def extract_burst(self, rmsdata, srate):
        """
        Calculate the beginning and end of a burst based on 7x the
        standard deviation of the signal (generally the RMS). After
        detecting beginning and ends of the burst based on timings
        differences larger than 0.5, the closest point that crosses
        2x the standard deviation of the signal will be assigned as
        the real beginning and end of the burst.

        Arguments
        ---------
        rmsdata   (array)
        the squared root of the mean squared (RMS) of a recording

        Returns
        -------
        A list of (start, end) values containing the samples where 
        start and end are detected in the signal.
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
            # take 50 ms window backward
            tmp = data[x:x-int(0.05*srate):-1] 
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
    
burstobj = Burst(srate = 30000)
