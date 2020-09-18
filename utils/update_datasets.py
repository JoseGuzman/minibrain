#!/usr/bin/env python
"""
update_datasets.py

Jose Guzman, jose.guzman@guzman-lab.com
Thu Aug 27 12:22:12 CEST 2020

This script creates a csv file for spike waveforms (*waveforms.csv)
for the kinetics of the spikes (*spikes.csv) for every single 
organoid type collected in $HOME/Guzman.VCB/
In addition, it will update the minibrain repository
(github.com/JoseGuzman/minibrain) with three datasets:
    1. waveforms.csv: normalized waveforms from organoids.
    2. spikes.csv : spike kinetic properties from organoids.
    3. organoID.csv: the type of of organoid for every unique identifier.

"""
import logging
import sys
import glob
import pandas as pd

def read_waveform(path):
    """
    Creates csv of normalized waveforms (*waveforms.csv) and kinetics
    of the spikes (*spikes.csv) in the directory entered in path.

    Returns
    -------
    A dataFrame with normalized waveforms and spike kinetics for 
    the experiments entered in path (they correspond to a different
    organoid type).

    """
    logging.basicConfig(stream = sys.stdout, level = logging.INFO)
    
    files = glob.glob(path + 'waveforms/*df')
    frames = [pd.read_pickle(wave) for wave in files ]
    dfspikes = pd.concat( frames, sort = False, ignore_index = True)
    # set uid as pandas index
    dfspikes.set_index(dfspikes.uid, inplace=True)
    dfspikes.drop('uid', axis = 1, inplace = True)

    # we order by index to have the latest recording on top
    dfspikes.sort_index(ascending = False, inplace = True) 

    logging.info(f'Reading {dfspikes.shape[0]:4d} spike waveforms in {path}')

    OrgID = dfspikes.index[0][:2] # first two alphanumeric values

    # create local *spikes.csv include index to have uid !!!!
    myname = path + OrgID + "_spikes.csv"
    dfspikes.loc[:, dfspikes.columns !='waveform'].to_csv(myname,index=True)
    
    # create local *waveforms.csv include index to have uid !!!
    dfwaveforms = pd.DataFrame(dfspikes['waveform'].tolist(), 
            index = dfspikes.index)
    myname = path + OrgID + "_waveforms.csv"
    dfwaveforms.to_csv(myname, index = True)

    return (dfspikes) # uid is now included as index

if __name__ == '__main__':
    import os 
    HOME = os.getenv('HOME')
    # directories where recordings are saved
    VTpath = HOME + '/Guzman.VCB/DLXi56/Analysis/SiliconProbes/VT/'
    FSpath = HOME + '/Guzman.VCB/DLXi56/Analysis/SiliconProbes/FS/'
    TCpath = HOME + '/Guzman.VCB/TSC2/Analysis/SiliconProbes/'

    dfVT = read_waveform(VTpath)
    dfTC = read_waveform(TCpath)
    dfFS = read_waveform(FSpath)

    # merge in GitHub all organoids together 
    # verify that we have unique index
    dfspikes = pd.concat([dfVT, dfTC, dfFS], ignore_index = False)

    git = HOME + '/git/minibrain/DataSets/'

    # Create/update spikes.csv
    logging.info(f'Saving  {dfspikes.shape[0]:4d} spike waveforms in {git}')
    name = git + 'spikes.csv'
    dfspikes.loc[:,dfspikes.columns !='waveform'].to_csv(name, index=True)

    # Create/update waveforms.csv
    name = git + 'waveforms.csv'
    dfwaveforms = pd.DataFrame(dfspikes['waveform'].tolist(), 
            index = dfspikes.index)
    dfwaveforms.to_csv(name, index=True)

    # Create/update organoID.csv
    name = git + 'organoID.csv'
    dfspikes.loc[:,dfspikes.columns =='organoid'].to_csv(name, index=True)
