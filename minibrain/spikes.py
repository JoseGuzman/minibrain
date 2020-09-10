"""
spikes.py

Jose Guzman, jose.guzman@guzman-lab.com

Created: Mon Jul 29 20:59:51 CEST 2019

Contains a class to load extracellular spikes recorded 
Cambride Neurotech silicon probes, sorted with Kilosort2
and curated with Phy2.

Example:
>>> from minibrain  import Units 
"""

import copy 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

@np.vectorize
def read_shank(channel, shanktype='P'):
    """
    Returns the shankID of the channel.

    Parameters
    ----------
    channel (int)
        The number of the channel in the shank

    shanktype (str):
        the type of probe used 'P' is ASSY-P from Cambridge Neurotech
    """
    if shanktype == 'P':
        rules = [range( 0,16), range(16,32), range(32,48), range(48,64),
                range(64,80), range(80,96), range(96,112), range(112,128)]
        shank = 'ABCDEFGH'

    elif shanktype == 'F':
        rules = [range( 0,10), range(10,21), range(21,32), range(32,43),
                range(43,54), range(54,64)]
        shank = 'ABCDEF'
    else:
        rules = [range( 0,16), range(16,32), range(32,48), range(48,64),
                range(64,80), range(80,96), range(96,112), range(112,128)]
        shank = 'ABCDEFGH'


    for i,sh in enumerate(rules):
        if channel in sh:
            return shank[i]

class Units(object):
    """
    A class to load extracellular units recordings acquired
    with silicon probes from Cambridge Neurotech.
    """

    def __init__(self, path = "./", shanktype = 'P'):
        """
        Reads all good isolated units from the probes and returns them 
        in a dataframe and dictionary
    
        Arguments
        ---------
        path (str):
            the path to look for cluster_info, spike_times.npy 
            and spike_clusters.npy generated with Phy2.

            Pandas dataframe with good units from clusteruing
            A dictionary with the spike times of all good units
        """
    
        myfile = path + 'cluster_info.tsv'
        df = pd.read_csv(myfile, sep = '\t')
        # map shank according to channel number 
        df['sh'] = df['ch'].apply(lambda x: read_shank(x, shanktype))
        
        # make a copy with only good units
        df_unit = df[ (df['group']=='good') ].copy()

        # remove some unused terms from Kilosort2
        del df_unit['group'] 
        del df_unit['Amplitude'] 
        del df_unit['amp'] 
        del df_unit['KSLabel'] 
        del df_unit['depth'] 

        # old phy-devel uses simply 'id'
        if 'id' in df.columns:
            df.rename(columns = {'id':'cluster_id'}, inplace=True)

        # read good units
        spike_times = np.load(path + 'spike_times.npy').flatten()
        spike_clusters = np.load(path + 'spike_clusters.npy')
        
        # read spikes from units
        dict_unit = dict() # a dictionary with all units
        for myid in df_unit['cluster_id'].values:
            dict_unit[myid]  = spike_times[np.where(spike_clusters==myid)]

        # reorder by channel and reset index
        df_unit.sort_values(by='ch', inplace=True)
        # recreate a new column index, without create it in the dataframe
        df_unit.reset_index(drop = True, inplace = True)

        self.df = df_unit
        # A dictionary with the spike times of all good units
        self.unit = dict_unit
        print('%d units found'%len(self.df))

    def get_spikes(self, pulse, unitID, lag = 30000):
        """
        Returns a list of spike times of a unit after the beginning of 
        the pulse. Times are substracted from the beginning of the 
        pulse.

        Arguments
        ---------
        pulse (list)
            a list of two values start and end values

        unitID (int)
            the ID of the unit in the cluster.

        lag (int)
            number of sampling points after the beginning of pulse.
        Default is 30000 (1 sec).
        """

        CONST = 150 # 5 ms delay to avoid artefact
        myunit = self.unit[unitID]

        myspikes = list() # containter
        for p in pulse:
            start, end = p
            idx = np.logical_and( myunit>start+CONST, myunit< end + lag)
            spk_times = list(myunit[idx] - start) # remove beginning of pulse
            myspikes.extend ( list(myunit[idx]-start ) ) #

        return myspikes

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
            
            index = mydf.index[ mydf['cluster_id']==key]
            mydf.loc[index, 'n_spikes'] =  int(len(mytimes))

        # set attributes of new object 
        setattr(myunit, 'unit', copy.deepcopy(mydict))
        setattr(myunit, 'df', mydf)

        return myunit

    def __len__(self):
        """
        Returns the number of good isolated units recorded.
        """
        return len(self.df)

