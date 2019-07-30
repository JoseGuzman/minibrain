"""
spikes.py

Jose Guzman, jose.guzman@guzman-lab.com

Created: Mon Jul 29 20:59:51 CEST 2019

Contains a class to load extracellular spikes recorded 
Cambride Neurotech silicon probes, sorted with spyking-circus
and curated with phy.

Example:
>>> from spikes import UnitsLoader 
>>> myrec = DataLoader('./') # will load shankA, shankB, shankC and shankD
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

myshank = {1.0:'A', 2.0:'B', 3.0:'C', 4.0:'D'}
read_shank = lambda x: myshank[x]

class UnitsLoader(object):
    """
    A class to load extracellular units recordings acquired
    with 64 probes silicon probes from Cambridge Neurotech.
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

    def __init__(self, mytime, path = ""):
        """
        Reads phy files with sorted probes 

        Arguments:
        ----------
        mytime (tuple) containing minutes, seconds and miliseconds
        
        """
        # set duration of recording
        tmin, tsec, tms = mytime
        self._duration = tmin*60000 + tsec*1000 + tms

        # load phy files with units and sorted spikes
        self._dfA, self._unitA, self._spkA = self._read_phy(path + 'shankA')
        self._dfB, self._unitB, self._spkB = self._read_phy(path + 'shankB')
        self._dfC, self._unitC, self._spkC = self._read_phy(path + 'shankC')
        self._dfD, self._unitD, self._spkD = self._read_phy(path + 'shankD')


    def _read_phy(self, shank):
        """
        Loads phy generated files. It will generate a pandas DataFrame
        with all information of the units (e.g. myrec.dfA for probeA)
        and a list with units 'ids' and spike times (myrec.unitA for probeA)
        and list with all spike times of the probe (self.spkA).
        
        Arguments:
        ----------
        shank (str) 'shankA', 'shankB', 'shankC' or 'shankD'
        """
        wcpath = '/wc_continuous.GUI/'
        df = pd.read_csv( shank + wcpath + 'cluster_info.tsv', sep='\t')
        # substitute number by shank type 'A', 'B','C' or 'D'
        df['shank'] = df['shank'].apply(read_shank)

        # select well isolated units
        df_units = df[df['group'] == 'good']
        n_units = len(df_units)
        spm_avg = 0

        units, spk = list(), list()
        if n_units: # read in spikes per minute
            spm = df_units['n_spikes'].values/(self.duration/60000)
            np.savetxt(shank + '.spm', spm, fmt='%f')
            spm_avg = spm.mean()
            print('%2d extracellular units in %s: %2.4f spk/min'
            %(n_units, shank,spm_avg) )
            # read spike times
            spike_times = np.load( shank + wcpath + 'spike_times.npy')
            spike_clusters = np.load( shank + wcpath + 'spike_clusters.npy')
            for i in df_units['id'].values:
                mydict = {}
                spk_times = spike_times[np.where(spike_clusters == i)]
                mydict[i] = spk_times
                spk.append(spk_times)
                units.append(mydict)
        
        return( df_units, units, spk )

    # getters to avoid owerwriting
    duration = property(lambda self: self._duration)
    dfA = property(lambda self: self._dfA)
    dfB = property(lambda self: self._dfB)
    dfC = property(lambda self: self._dfC)
    dfD = property(lambda self: self._dfD)

    unitA = property(lambda self: self._unitA)
    unitB = property(lambda self: self._unitB)
    unitC = property(lambda self: self._unitC)
    unitD = property(lambda self: self._unitD)

    spkA = property(lambda self: self._spkA)
    spkB = property(lambda self: self._spkB)
    spkC = property(lambda self: self._spkC)
    spkD = property(lambda self: self._spkD)
