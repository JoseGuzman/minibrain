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

from scipy import signal 

from minibrain.lfpmanager import lfp

def spike_kinetics(waveform, dt = 1):
    """
    Calculates the following kinetic parameters from the spike waveform.

    * half-width:  the width of the spike at half-maximal amplitude of the related to rates of depolarization/repolarization.
    * latency : the trough to right (late) peak latency. It related to 
    the repolarization of an action potential.
    * asymmetry: the ratio of the amplitude of the second maximun (b) to 
    the amplitude of the first maximum (a). It reflects the differences in 
    the rate of fall of spike repolarization.

    Parameters
    ----------
    waveform (array)
        a Numpy Array with the waveform to calculate spike kinetics.

    dt (sampling interval) 
        ampling interval in ms (e.g., 1/30 30 samples every ms).
        Default is one.

    Returns
    -------
    A dictionary with the parameters and the spike waveform normalized.
    """
    if dt == 1:
        mybase = 15; # take at least 15 samples
    else:
        mybase = int(0.5/dt) # 0.5 ms

    # first normalize the wave to it's peak
    mytrace = waveform/-waveform.min() # peak in y=1

    p_idx = mytrace.argmin() # peak index to calculate half-width
    a_idx = mytrace[:p_idx].argmax() # peak index the left part 
    b_idx = p_idx + mytrace[p_idx:].argmax() # peak index the right part 

    mydict = dict()
    # Half-width from the min found
    half_width = signal.peak_widths(-mytrace, [p_idx], rel_height = 0.5)
    half_width = float(half_width[0])

    if half_width <=0: # if half-width is zero
        mydict['half_width'] = np.nan
        mydict['asymmetry']   = np.nan
        mydict['latency'] = np.nan
    else:
        mydict['half_width'] = half_width*dt # in sampling points
        baseline = mytrace[:mybase].mean()
        a = mytrace[a_idx] - baseline
        b = mytrace[b_idx] - baseline

        mydict['asymmetry'] = (b-a)/(a+b) #(a-b)/(a+b)
        mydict['latency'] = (b_idx - p_idx)*dt # in sampling points

    mydict['waveform'] = mytrace # normalized to peak

    return mydict

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

    # read "bit_volts" in structure.oebin
    gain =  0.19499999284744262695   # uVolts per bit (from Intant) 

    def __init__(self,fname,date=None,birth=None,nchan=67,srate=30000, openephys_binary = True):
        """
        Reads binary data from Open Ephys acquired with
        the Intan 512ch Recording controller.

        Arguments:
        ----------
        fname (str) 
            filename (e.g., 'continuous.dat')
        date (str) 
            recording date format (e.g., %Y-%m-%d_%H-%M-%S, 
            like '2019-10-09_15-26-38')
        birth (str) 
            birth date format (e.g., '2019-10-07_00_00-00')
        nchan (int)  
            number of channels in recording. It is 67 by default 
            (64 ADC + 3 AUX from Intan RHD2000). Use
            134 (128 + 6 AUX) when using two shanks of electrodes.
        srate (int)
            sampling rate, the number of samples per second

        openephys_binary (bool) 
            if acquisition was with Open Ephys GUI (default True) 
        """

        self._nchan = nchan
        self.srate = srate      # number of samples per second
        self.dt = 1/(srate/1000) # sampling interval in ms
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
        self.seconds = nsamples/self.srate # duration in seconds
        # prompt info: duration in minutes, age in months
        print('Recording duration = {:2.4f} min.'.format(self.seconds/60) )
        print('Recording age      = {:2.4f} months.'.format(age/30) ) 

        if openephys_binary:
            btype = '<i2'
        else: # Intan software
            btype = 'int16'
        # accesss without reading the whole file 
        # np.int16 is 16-bits integer 
        # signed means that the (2**16 values) are between -32768 to 32767
        # i2 means 'signed 2-byte (16 bit) integer'
        # '<' means little-endian
        #self._memmap = np.memmap(fp, np.dtype('<i2'), mode = 'r', 
        #    shape = (nsamples, nchan))
        self._memmap = np.memmap(fp, np.dtype(btype), mode = 'r', 
                shape = (nsamples, nchan))

        # we transpose the map to handle 1D NumPy decently 
        # e.g., to use self._data[0] for channel zero.
        # this is the data we will use in the object
        self._data = np.transpose( self._memmap )

        fp.close()

    def get_rms_shank(self, shankID, pstart, pend):
        """
        Calculate the square root of the mean squared (RMS) of all the 
        channels in the shank from the times in pstart and pend.

        
        shankID (char)  -- 'A', 'B', 'C', or 'D'
        psart (int)     -- the beginning time of the channel in sampling points
        pend (int)     -- the end time of the channel in sampling points

        Returns
        -------
        A list with the maximal RMS (20 ms window length). 
        """
        myshank = list()
        for i, ch in enumerate(self.shank[shankID]):
            myrec = self.get_channel(ch)[pstart:pend]

            band_pass_params = dict(low = 90, high = 250, srate = self.srate)
            myrecBP = lfp.band_pass(data = myrec, **band_pass_params)
            myrecDC = lfp.decimate(data = myrecBP, q = 60)
            new_srate = self.srate/60
            mysegment = int(0.020*new_srate) # 20 ms for testing 
            myrecRMS = lfp.rms(data = myrecDC, segment = mysegment )
            myshank.append( myrecRMS.max() )

        return myshank
        

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
            peaks = signal.find_peaks(trace,height=myheight,distance = mydist)[0]
            print('%3d artifacts found in channel %3d'
                %(peaks.size, channel))

            if peaks.size >=1:
                shift = np.arange(len(peaks))*mydist*2
                peaks = peaks - shift
                for p in peaks:
                    pstart, pend = p - mydist, p + mydist
                    print('Remove t = %2.4f sec.'%(pstart/self.srate))
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
        # return self.gain*self._data[channel].T 
        return self._data[channel]*self.gain 

    def waveform_kinetics(self, spk_times, channel):
        """
        gets kinetic parameters from the voltage of the channel 
        4 ms around the times given.
        """
        tmax = 4 # in ms
        spk_times = spk_times.astype(int) # cast to int
        phalf = int((tmax/2)/self.dt)

        waveform = list()
        half_width = list()
        latency = list()
        asymmetry = list()
        uvolt = self.channel(channel)
        for p in spk_times:
            myspike = spike_kinetics(uvolt[p-phalf : p+phalf], dt=self.dt)
            waveform.append( myspike['waveform'] ) # normalized spike!
            half_width.append( myspike['half_width'] )
            latency.append( myspike['latency'] )
            asymmetry.append( myspike['asymmetry'] )

        mydict={'waveform': waveform,
                'half_width': half_width,
                'latency' : latency,
                'asymmetry' : asymmetry
                }
        return mydict


    def fig_waveform(self, spk_times, nrandom, channel, ax=None):
        """
        Plots 4 ms of average voltage of the channel at the times given.

        Arguments:
        ----------
        spk_times (list)  -- sampling points to take
        nrandom (int) -- the number of single random waveforms to plot
        channel (int)  -- the channel to plot 
        ax (axis object)

        Returns the axis to plot and a dictionary with the
        kinetic properties of the average waveform.
        
        """
        if ax is None:
            ax = plt.gca()

        tmax = 4 # in ms
        spk_times = spk_times.astype(int) # cast to int
        time = np.linspace(start = 0, stop = tmax, num = tmax/self.dt)
        phalf = int((tmax/2)/self.dt)

        uvolt = self.channel(channel)
        uvolt -= np.median(uvolt) # correct for median
        avg = np.mean([uvolt[p-phalf:p+phalf] for p in spk_times],0)
        mydict = spike_kinetics(avg, dt = self.dt)

        # take n random waveforms
        for peak in np.random.choice(spk_times, nrandom):
            wave = uvolt[peak-phalf:peak+phalf]
            ax.plot(time, wave, lw=0.5, color='#999999')

        ax.plot(time, avg, color = 'k', lw=2) 
        ax.set_ylim(top = 30, bottom = -90)
        ax.axis('off')

        # plot scalebar
        # horizontal (time)
        ax.hlines(y=-50, xmin=2.2, xmax=3.2, lw=2, color='k') # 2 ms
        ax.text(s='1 ms', y=-60, x=2.7, horizontalalignment='center')
        # vertical (voltage)
        ax.vlines(x = 3.2, ymin = -50, ymax=0, lw=2, color='k')  # 50 uV
        ax.text(s='50 $\mu$V', y= -25, x=3.5, verticalalignment='center')

        return( ax, mydict )
        
        
    def fig_shank(self, spk_times, shankID, ax=None):
        """
        Plots 5 ms of average voltage of the shank at the times given.

        Arguments:
        ----------
        spk_times (list)  -- sampling points to take
        shankID (char)  -- 'A', 'B', 'C', or 'D'
        ax (axis object)

        Returns the figure to plot
        
        """
        if ax is None:
            ax = plt.gca()

        spk_times = spk_times.astype(int) # cast to int
        time = np.linspace(start = 0, stop = 5, num = 5/self.dt)
        phalf = int(2.5/self.dt) # 2.5 before and after peak

        yoffset = 0 # y-offset to plot traces (will go negative)
        for ch in self.shank[shankID]:
            uvolt = self.channel(ch)
            uvolt -= np.median(uvolt)
            avg = np.mean([uvolt[p-phalf:p+phalf] for p in spk_times],0)

            avg +=yoffset
            if not ch%2: # even (e.g., 0, 2, 4, etc...)
                ax.plot(time, avg, c = self.color[shankID], lw =1.5)
                ax.text(s = str(ch), x= 0,y = yoffset+15, ha = 'left')
            else: # plot down if uneven
                ax.plot(time+6, avg+50, c = self.color[shankID], lw=1.5)
                ax.text(s = str(ch), x=6,y = yoffset+65, ha = 'left')
            yoffset -=80 # jump to the next subplot
            ax.axis('off')
        
        # plot scalebar
        ax.hlines(y = -1230, xmin = 10, xmax=12, lw=2, color='k') # 2 ms
        ax.text(s='2 ms', y=-1300, x=11, horizontalalignment='center')
        ax.vlines(x = 12, ymin = -1230, ymax=-1180, lw=2, color='k')  # 50 uV
        ax.text(s='50 $\mu$V', y= -1205, x= 12.5, verticalalignment='center')

        return( ax )

    
    # getter for the ADC channels
    channel = property(lambda self: self.get_channel)
    # getter for the number of samples channels
    nsamples = property(lambda self: self._nsamples)
