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

myshank = {1.0:'A', 2.0:'B', 3.0:'C', 4.0:'D', 
           5.0:'E', 6.0:'F', 7.0:'G', 8.0:'H'}
read_shank = lambda key: myshank[key]

def read_shank(channel):
    """
    Returns the shankID of the channel.

    Parameters
    ----------
    channel (int)
        The number of the channel in the shank
    """
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

    def __init__(self, path = "./"):
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
    
        dict_unit = dict() # a dictionary with all units
        myfile = path + 'cluster_info.tsv'
        df = pd.read_csv(myfile, sep = '\t')
        #df['sh'] = df['sh'].apply(read_shank) # map probes
        df['sh']= read_shank(df['ch'])
            
        # choose only good units
        df_unit = df[ (df['group']=='good') ]
        df_unit = df_unit.drop('group', 1) # 1 is for dropping column
        
        # read good units
        spike_times = np.load(path + 'spike_times.npy')
        spike_clusters = np.load(path + 'spike_clusters.npy')
        
        for myid in df_unit['cluster_id'].values:
            #mykey = str(i) + myshank
            dict_unit[str(myid)]  = spike_times[np.where(spike_clusters==myid)] 

        # change to have unique identifiers
        #df_unit['id'] = df_unit['id'].apply(lambda x: str(x)+myshank)
        
        # set sort=True cause non-cocatenation axis is not aligned
        # Pandas dataframe with good units from clusteruing
        self.df = df_unit
        # A dictionary with the spike times of all good units
        self.unit = dict_unit
        print('%d units found'%len(self.df))

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

