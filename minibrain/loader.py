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
import copy

import numpy as np
import matplotlib.pyplot as plt

from scipy import signal 

from minibrain.lfpmanager import lfp

def spike_kinetics(waveform, dt = 1):
    """
    Calculates the following kinetic parameters from the spike waveform.

    * half-width:  the width of the spike at half-maximal amplitude. 
    It is related to rates of depolarization/repolarization.
    
    * latency : the trough to right (late) peak latency. It related to 
    the repolarization of an action potential.
    
    * asymmetry: the ratio of the amplitude of the second maximun (b) to 
    the amplitude of the first maximum (a). It reflects the differences in 
    the rate of fall of spike repolarization.
    
    * rise-time: the 10-90% rise-time of the spike, related to the number of 
    Na channels

    * repo_duration: the duration of the repolarization phase.

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
        mybase = 30 # take at least 30 samples (1 ms)
    else:
        mybase = int(1/dt) # 1 ms
    baseline = waveform[:mybase].mean()
    # substract baseline
    waveform -=baseline

    # first normalize the wave to it's peak
    mytrace = waveform/-waveform.min() # peak in y=1

    p_idx = mytrace.argmin() # peak index to calculate half-width
    a_idx = mytrace[:p_idx].argmax() # peak index the left part 
    b_idx = p_idx + mytrace[p_idx:].argmax() # peak index the right part 

    mydict = dict()
    # Half-width from the min found
    half_width = signal.peak_widths(-mytrace, [p_idx], rel_height = 0.5)
    half_width = float(half_width[0])

    p90 = float(signal.peak_widths(-mytrace, [p_idx], rel_height = 0.9)[2])
    p10 = float(signal.peak_widths(-mytrace, [p_idx], rel_height = 0.1)[2])

    if half_width <=0: # if half-width is zero
        mydict['half_width'] = np.nan
        mydict['asymmetry']   = np.nan
        mydict['latency'] = np.nan
        mydict['rise'] = np.nan
        mydict['repo_duration'] = np.nan 
    else:
        mydict['half_width'] = half_width*dt # in sampling points
        a = mytrace[a_idx] # left peak, baseline substracted 
        b = mytrace[b_idx] # right peak, baseline substracted

        mydict['asymmetry'] = b # b/peak
        mydict['latency'] = (b_idx - p_idx)*dt # in sampling points
        mydict['rise'] = (p10-p90)*dt # in sampling points

        if b <= 0: # below baseline => no repolarization
            mydict['repo_duration'] = 0.0 
            print(b)
        else:
            duration = signal.peak_widths(mytrace, [b_idx], rel_height =1) 
            duration = float(duration[0])
            mydict['repo_duration'] = duration * dt 

    mydict['waveform'] = mytrace # normalized to peak

    return mydict

class TTLLoader(object):
    """
    A class to load TTL signals acquired with Open-ephys gui
    It reads syn_messages.txt and files within events folder.
    """
    def __init__(self, path=None, ttl=1):
        """
        TTL construction object

        Arguments:
        ----------
        path (str) 
            path to syn_messages.txt, e.g., under 
            under experiment1/recording1/. If None

        ttl (int)
            the TTL signal to read (0 to 3). 

        """
        self.ttl = ttl

        if path is None:
            self.path = None
            self.time = np.nan
        else:
            self.path = path
            self.time = self._read_path(path, ttl)

    def __call__(self, path = None, ttl =1):
        """
        Execution of object creates a new object. 
        By default, the TTL signal to read is 1.
        """
        return TTLLoader(path, ttl)

    def __len__(self):
        """
        Count the pair of pulses. It will call self._get_pulse()
        """
        if self.path is None:
            mysize =  0
        elif self.time is np.nan:
            mysize =  0
        else:
            mysize = self.pulse.shape[0]

        return mysize

    def _read_path(self, path, ttl):
        """
        Reads sync_messages.txt, timestamps.npy and channels.npy
        from the location of the binary file acquired with 
        open-ephys gui.

        Arguments:
        ----------
        path (str) 
            path to syn_messages.txt, e.g., under 
            under experiment1/recording1/. If None

        ttl (int)
            the TTL signal to read (0 to 3). 

        Returns
        -------
        two NumPy arrays with values from timestamps.npy
        and channels.npy
        """
        # first read timestamps.npy from /continuous
        binarypath = os.path.join(path, 'timestamps.npy')
        tstart = np.load(binarypath)[0] # only first sample

        # then, read sync_messages from root by
        # removing last two directories
        path_list =  os.path.split(binarypath)[0].split('/')[1:-2]
        mypath = os.path.join('/', *path_list)

        mysynfile = os.path.join(mypath, 'sync_messages.txt')

        # get information from syn_messages.txt
        with open(mysynfile) as fp:
            lines = fp.readlines()

        myinfo = lines[1].split(':') # read only second line

        # 2) read Intan Controller
        myid = 'Intan_Rec._Controller-'
        processor = myinfo[2].split(' ')[1]
        subprocessor = myinfo[3].split(' ')[1]
        intan = myid + processor + '.' + subprocessor

        # 3) read TTL
        TTLdir = 'TTL_{:1d}'.format(ttl)
        ttl_path = os.path.join(mypath, 'events', intan, TTLdir)
        time_path = os.path.join(ttl_path, 'timestamps.npy') 
        channel_path = os.path.join(ttl_path, 'channels.npy')

        # check if TTL signals exists
        if np.load(time_path).size > 0:
            ttl_time = np.load(time_path) - tstart 
            channel = np.load(channel_path) 
            time = ttl_time[channel==ttl+1]
        else:
            time = np.nan

        return time

    def get_pulse(self):
        """
        Returns
        A 2D NumPy array with the start,end sampling points
        of the TTL signal.
        """

        if self.path is None:
            pulse = np.nan
        elif self.time is np.nan:
            pulse = np.nan
        else:
            mytime = self.time
            pulse = np.split(mytime, len(mytime)/2)

        return( np.array(pulse))

    # getter for pulse
    pulse = property(lambda self: self.get_pulse())

# object ready to use
ttl_info = TTLLoader(path = None, ttl = 1)

class EphysLoader(object):
    """
    A class to load extracellular recordings acquired
    with the silicon probes from Cambridge Neurotech 
    """
    # A dictionary with shanks ID and colors
    color = {'A': '#0080FF',
             'B': '#FF0000',
             'C': '#FF9933',
             'D': '#00AA00',

             'E': '#FF55FF',
             'F': '#DAA520', # goldenrod
             'G': '#000080', # navy
             'H': '#2E8B57', # seagreen

             'I': '#0080FF',
             'J': '#FF0000',
             'K': '#FF9933',
             'L': '#00AA00',
            }

    shank = {'A': range(16),
             'B': range(16,32),
             'C': range(32,48),
             'D': range(48,64),

             'E': range(64,80),
             'F': range(80,96),
             'G': range(96,112),
             'H': range(112,128)
            }

    
    shankF = {'A':range(0 ,10),
             'B': range(10,21),
             'C': range(21,32),
             'D': range(32,43),
             'E': range(43,54),
             'F': range(54,64),

             'G': range(64,74),
             'H': range(74,85),
             'I': range(85,96),
             'J': range(96,107),
             'K': range(107,118),
             'L': range(118,128)
            }

    # read "bit_volts" in structure.oebin
    gain =  0.19499999284744262695   # uVolts per bit (from Intant) 

    def __init__(self,
            fname,
            date = None,
            birth = None,
            nchan = 67,
            srate = 30000, 
            openephys_binary = True,
            show_info = True):
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

        self._fname = fname
        self._date = date
        self._birth = birth
        self._nchan = nchan
        self._srate = srate # number of samples per second
        self._oephys = openephys_binary

        self._dt = 1/(srate/1000) # sampling interval in ms
        if date is None or birth is None:
            age = 0
        else:
            try:
                myformat = '%Y-%m-%d_%H-%M-%S'
                recdate = datetime.datetime.strptime(date, myformat) 
            except ValueError: # if not hour:min:sec precission 
                recdate = datetime.datetime.strptime(date,'%Y-%m-%d') 
            try:
                birthdate = datetime.datetime.strptime(birth, myformat) 
            except ValueError: # if not hour:min:sec precission 
                birthdate = datetime.datetime.strptime(birth,'%Y-%m-%d') 

            delta = recdate-birthdate
            age = delta.days + delta.seconds/(24*60*60)

        self._age = age

        fp = open(fname, 'rb')
        nsamples = os.fstat(fp.fileno()).st_size // (nchan*2)
        myseconds = nsamples/srate # duration in seconds

        if openephys_binary: # open-ephys GUI
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

        fp.close()

        # prompt info: duration in minutes, age in months
        if show_info:
            print('Recording duration = {:2.4f} min.'.format(myseconds/60) )
            print('Recording age      = {:2.4f} months.'.format(age/30) ) 

    def __len__(self):
        return self._memmap.shape[0]

    def __add__(self, obj):
        """
        Adds EphysLoader objects together by simply
        adding the binaries together. The resulting object 
        will take the attributes of first object (e.g., age)
        with the exception of nsamples
        """
        # only add objects with same sampling rate, channels
        assert self.srate == obj.srate
        assert self.nchannels == obj.nchannels

        # IMPLEMENT copy() to account for memmaps!
        myparams = dict(
                fname = self.fname ,
                date  = self.date  ,
                birth = self.birth ,
                nchan = self.nchannels ,
                srate = self.srate  ,
                openephys_binary = self._oephys,
                show_info = False,
                )
        myrec = EphysLoader(**myparams)
        myrec._memmap = self._memmap

        # update memory access
        myrec._memmap = np.concatenate(( myrec._memmap, obj._memmap ))

        return myrec

    def __copy__(self):
        """ 
        Shallow copy of EphysLoader object
        """
        myparams = dict(
                fname = self.fname ,
                date  = self.date  ,
                birth = self.birth ,
                nchan = self.nchannels ,
                srate = self.srate  ,
                openephys_binary = self._oephys
                )
        myrec._memmap = self._memmap.copy() 

        return (myrec)



    def tofile(self, fname):
        """
        Saves the current recording as a binary file

        Arguments
        ---------

        fname (str)
            The filename to be saved (e.g., 'continuous.dat')
        """

        self._memmap.tofile( fname )

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
        

    def blank(self, sample_list, nshift = 15, fname = None):
        """
        Blanks the recording at the sampling point given
        in 'sample_list'. For nshift=15, it will move
        15 sampling points to the left of the sample to blank
        After that, read the previous 15x2 samples before
        that sample to copy it -15 and +15 samples around
        the value we want to blank.

        Arguments
        ---------
        sample_list (list) 
            the samples to be blanked (in sampling points)
    
        nshift (int) 
            number of sampling points copied around sample
        to remove. Default 15, meaning that 15 samples 
        before and after the point are to be removed. We
        will take the 30 samples before the substitution
        (i.e., sample - 30)

        fname (str)
            The filename to be saved (e.g., 'continuous.dat')
        """

        # access a copy of memory-mapped array 
        fp = self._memmap.copy() 

        for p in sample_list:
            # x[ samples , channels]
            fp[ p-nshift:p+nshift, : ] = fp[ p-(2*nshift)-nshift:p-nshift, : ]

        self._memmap = fp # realocate
        del fp # just in case

        # if not saved, we can use it like that to plot
        if fname:
            self._memmap.tofile(fname) 
            
        
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
        return self._memmap[:,channel]*self.gain 

    def waveform_kinetics(self, spk_times, channel):
        """
        gets kinetic parameters from the normalized average
        spike obtained by summing all spikes in the  channel 
        2.5 ms around the times given.

        Parameters
        ----------

        spk_times (array)
            a list of spike times (in sampling points)

        channel (int)
            the channel to record the spikes from.

        Returns
        -------
            a dictionary with half-width, latency, asymmetry
        and rise-time from the averaged and normalized
        spike waveform (see minibrain.spike_kinetics()).
        """
        tmax = 5 # in ms
        spk_times = spk_times.astype(int) # cast to int
        phalf = int((tmax/2)/self.dt)

        uvolt = self.channel(channel)
        uvolt -= np.median(uvolt) # correct for median
        avg = np.mean([uvolt[p-phalf:p+phalf] for p in spk_times],0)
        mydict = spike_kinetics(avg, dt = self.dt) # will normalize spike

        return mydict


    def fig_waveform(self, spk_times, nrandom, channel, ax=None):
        """
        Plots 5 ms of average voltage of the channel at the times given.

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

        tmax = 5 # in ms
        spk_times = spk_times.astype(int) # cast to int
        time = np.linspace(start = 0, stop = tmax, num = int(tmax/self.dt))
        phalf = int((tmax/2)/self.dt)

        uvolt = self.channel(channel)
        uvolt -= np.median(uvolt) # correct for median
        # move left 5 sampling points (0.5 ms) to get all repolarization
        avg = np.mean([uvolt[p-phalf+15:p+phalf+15] for p in spk_times],0)
        mydict = spike_kinetics(avg, dt = self.dt) # will normalize spike

        # take n random waveforms
        for peak in np.random.choice(spk_times, nrandom):
            # move left 5 sampling points (0.5 ms) to get all repolarization
            wave = uvolt[peak-phalf+15:peak+phalf+15]
            # remove 0.5 ms baseline to plot
            mybase = wave[:int(0.5/self.dt)].mean()
            wave -=mybase
            ax.plot(time, wave, lw=0.5, color='#999999')

        ax.plot(time, avg, color = 'k', lw=2) 
        ax.set_ylim(top = 30, bottom = -90)
        ax.axis('off')

        # plot scalebar
        # horizontal (time)
        ax.hlines(y=-50, xmin=3.2, xmax=4.2, lw=2, color='k') # 2 ms
        ax.text(s='1 ms', y=-60, x=3.7, horizontalalignment='center')
        # vertical (voltage)
        ax.vlines(x = 4.2, ymin = -50, ymax=0, lw=2, color='k')  # 50 uV
        ax.text(s='50 $\mu$V', y= -25, x=4.5, verticalalignment='center')

        return( ax, mydict )
        
        
    def fig_shank(self, spk_times, shankID, shanktype ='P', ax=None):
        """
        Plots 5 ms of average voltage of the shank at the times given.

        Arguments:
        ----------
        spk_times (list)  
            sampling points to take
        shankID (char)  
            'A', 'B', 'C', or 'D'
        shanktype (char)
            If P/E or F-type probes from Cambridge Neurotech
        ax (axis object)

        Returns the figure to plot
        
        """
        if ax is None:
            ax = plt.gca()

        tmax = 5 # in ms
        spk_times = spk_times.astype(int) # cast to int
        time = np.linspace(start = 0, stop = tmax, num = int(tmax/self.dt))
        phalf = int((tmax/2)/self.dt) # 2.5 before and after peak

        yoffset = 0 # y-offset to plot traces (will go negative)
        if shanktype == 'P' or shanktype == 'E':
            myshank = self.shank
        elif shanktype ==  'F' or shanktype == 'FF':
            myshank = self.shankF
        else:
            myshank = self.shank


        for ch in myshank[shankID]:
            uvolt = self.channel(ch)
            uvolt -= np.median(uvolt)
            # move left 5 sampling points (0.5 ms) to get all repolarization
            avg = np.mean([uvolt[p-phalf+15:p+phalf+15] for p in spk_times],0)

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

    # getter only attributes
    fname = property(lambda self: self._fname)
    date  = property(lambda self: self._date)
    birth = property(lambda self: self._birth)
    srate = property(lambda self: self._srate)
    openephys_binary = property(lambda self: self._oephys)
    dt    = property(lambda self: self._dt)
    age   = property(lambda self: self._age)
    # getter for the number of samples channels
    nsamples = property(lambda self: self._memmap.shape[0])
    nchannels = property(lambda self: self._memmap.shape[1])
