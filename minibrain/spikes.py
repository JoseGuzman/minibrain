"""
spikes.py

Jose Guzman, jose.guzman@guzman-lab.com

Created: Mon Jul 29 20:59:51 CEST 2019

Contains a class to load extracellular spikes recorded 
Cambride Neurotech silicon probes, sorted with spyking-circus
and curated with phy.

Example:
>>> from minibrain  import UnitsLoader 
>>> myrec = DataLoader('./') # will load shankA, shankB, shankC and shankD
"""

import copy 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

myshank = {1.0:'A', 2.0:'B', 3.0:'C', 4.0:'D'}
read_shank = lambda key: myshank[key]

class Units(object):
    """
    A class to load extracellular units recordings acquired
    with silicon probes from Cambridge Neurotech.
    """

    def __init__(self, path = "./continuous/Bandpass_Filter-102_100.0/", shank = 'ABCD'):
        """
        Reads all good isolated units from the probes and returns them in a dataframe
        and dictionary
    
        Arguments
        ---------
        path (str):
            the path to look for spike_times.npy and spike_clusters.npy 
        shank (str):
            the shank of the silicon probe to read 
        """
    
        df_list = list() # list of dataframe
        dict_unit = dict() # a dictionary with all units
        for myshank in shank:
            mypath = path + '/shank' + myshank + '/continuous.GUI/'
            myfile = mypath + 'cluster_info.tsv'
            df = pd.read_csv(myfile, sep = '\t')
            df['shank'] = df['shank'].apply(read_shank) # map probes
            
            # choose only good units
            df_unit = df[ (df['group']=='good') ]
            df_unit = df_unit.drop('group', 1) # 1 is for dropping column
        
            # read good units
            spike_times = np.load(mypath + 'spike_times.npy')
            spike_clusters = np.load(mypath + 'spike_clusters.npy')
        
            for i in df_unit['id'].values:
                mykey = str(i) + myshank
                dict_unit[mykey] = spike_times[np.where(spike_clusters==i)] 

            # change to have unique identifiers
            df_unit['id'] = df_unit['id'].apply(lambda x: str(x)+myshank)
            df_list.append(df_unit)
        
        self.df = pd.concat(df_list).reset_index(drop=True)
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
                x = np.logical_and(spk_times>start, spk_times<end)
                if not spk_times[x].size == 0:
                    newval = spk_times[x].tolist()
                    mytimes.extend( newval )
            mydict[key] = np.array(mytimes)
            
            index = mydf.index[ mydf['id']==key]
            mydf.loc[index, 'n_spikes'] =  int(len(mytimes))

        # set attributes of new object 
        setattr(myunit, 'unit', copy.deepcopy(mydict))
        setattr(myunit, 'df', mydf)

        return myunit
