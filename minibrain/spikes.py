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
    
        df_list = list() # a list with dfs for different shanks
        dict_unit = dict() # a dictionary with all units from different shanks 
        for myshank in shank:
            mypath = path + '/shank' + myshank + '/continuous.GUI/'
            myfile = mypath + 'cluster_info.tsv'
            df = pd.read_csv(myfile, sep = '\t')
            df['shank'] = df['shank'].apply(read_shank) # map probes
        
            # choose good units
            df_unit = df[ (df['group']=='good') ]
        
            # read good units
            spike_times = np.load(mypath + 'spike_times.npy')
            spike_clusters = np.load(mypath + 'spike_clusters.npy')
        
            for i in df_unit['id'].values:
                mykey = str(i) + myshank
                dict_unit[ mykey] =  spike_times[ np.where(spike_clusters==i) ] 
            
            df_unit['id'] = df_unit['id'].apply(lambda x: str(x) + myshank) # change to have unique identifiers
            df_list.append(df_unit)
        
        self.df = pd.concat(df_list).reset_index(drop=True)
        self.id = dict_unit
        print('%d units found'%len(self.df))
    
