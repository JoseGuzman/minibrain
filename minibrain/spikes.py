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

from pathlib import Path

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
        the type of probe used: 
        the 'P' from Cambridge Neurotech has the same electrode organization
        as the 'E', but different geometry.
    """
    if shanktype == 'P' or shanktype == 'E':
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
    
        #myfile = path + 'cluster_info.tsv'
        myfile = Path(path, 'cluster_info.tsv')
        df = pd.read_csv(myfile, sep = '\t')
        
        # make a copy with only good units
        df_unit = df[ (df['group']=='good') ].copy()

        # remove some unused terms from Kilosort2
        remove = ['sh', 'group', 'Amplitude', 'amp', 'KSLabel', 'depth']
        df_unit.drop(remove, axis=1, inplace = True)

        # old phy-devel uses simply 'id'
        if 'id' in df_unit.columns:
            df_unit.rename(columns = {'id':'cluster_id'}, inplace=True)

        # map shank according to channel number 
        df_unit['shank'] = df_unit['ch'].apply(lambda x: read_shank(x, shanktype))

        # use human-readable columns
        df_unit.rename(columns = {'ch':'channel'}, inplace=True)
        df_unit.rename(columns = {'fr':'frequency'}, inplace=True)

        # read good units
        spike_times = np.load(path + 'spike_times.npy').flatten()
        spike_clusters = np.load(path + 'spike_clusters.npy')
        
        # read spikes from units
        dict_unit = dict() # a dictionary with all units
        for myid in df_unit['cluster_id'].values:
            dict_unit[myid]  = spike_times[np.where(spike_clusters==myid)]

        # reorder by channel and set index to cluster_id 
        df_unit.sort_values(by='channel', inplace=True)
        # recreate a new column index, without create it in the dataframe
        #df_unit.reset_index(drop = True, inplace = True)
        df_unit.set_index('cluster_id', inplace=True)

        self.df = df_unit
        # A dictionary with the spike times of all good units
        self.unit = dict_unit
        n_units = len(self.df)
        print('{0:2d} units found in cluster_info.tsv'.format(n_units))

    def get_spiketrain(self, pulse, cluster_id):
        """
        Returns a list of spike times of a unit between the beginning 
        and the end of a pulse. Times are substracted from the beginning of the 
        pulse.

        Arguments
        ---------
        pulse (list)
            a list of two start and end values (e.g., [(50,100),(150,200)]

        cluster_id (int)
            the ID of the unit in the cluster.

        Returns
        -------

        a dictionary containing properties of the burst during the pulse:
        'latency': number of sampling points from the beginning of the pulse
        'count ' : number of spikes during the pulse
        'duration' : number of sampling points between the first and last spike
        'isi'    : number of samples of the average inter-spike-interval (isi) 
        'prop_zeros': proportion of pulses without respones
        'prop_ones':  proportion of pulses with one single spike
        """
        myunit = self.unit[cluster_id]

        myspikes = list() # collects spike times for every pulse

        latency = list()  # latency from the beginning of pulse
        count   = list()  # number of spikes during the pulse
        duration = list() # number of samples between 1st and last spike
        isi = list() # average inter-spike interval (in samples)
        n_zeros, n_ones, n_more = (0, 0, 0)
        for p in pulse:
            start, end = p
            idx = np.logical_and( myunit>start, myunit< end )
            spk_times = list(myunit[idx] - start) # remove beginning of pulse

            # get latency, count, duration and isi
            if spk_times: # not empty spikes
                latency.append(spk_times[0])
                count.append( len(spk_times) )
            else:
                n_zeros +=1
                latency.append( np.nan )
                count.append( np.nan  )


            if len(spk_times) == 1: # one spike gives nan
                n_ones +=1
                duration.append(0)
                isi.append( np.nan )
            elif len(spk_times) >1: # more than 1 spike
                n_more +=1
                duration.append(  np.max(spk_times) - np.min(spk_times) )
                isi.append( np.diff(spk_times).mean() )
            
            myspikes.append( spk_times ) # remove beginning of pulse

        mydict = dict()
        # use masked arrays to avoid missing values
        # will return RuntimeWarning if arrays contain only np.nan 
        mydict['latency']  = np.nanmean( latency ) 
        mydict['count']    = np.nanmean( count   )
        mydict['duration'] = np.nanmean( duration)
        mydict['isi']      = np.nanmean( isi     )
        mydict['prop_zeros'] =  n_zeros/len(pulse)
        mydict['prop_ones']  =  n_ones/len(pulse)
        mydict['prop_more']  =  n_more/len(pulse)
        # flatten all spikes in 1D array
        mydict['spk_times'] = list(np.array([elem for trace in myspikes for elem in trace]))
        #mydict['raw'] = myspikes
        return mydict

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
