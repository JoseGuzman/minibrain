#!/usr/bin/env python3
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

Requirements:
minibrain 
"""
import logging
import pandas as pd

def write_readme(path, mystr):
    """
    updates Readme.md with new data

    Arguments
    ---------

    path: pathlib object (e.g. Path('minibrain')
    mystr: message to add the the beginning of the file
    """
    lines = list()
    with open(path, 'r') as fp:
        for line in fp:
            if line.startswith('The dataset'):
                line = mystr
            lines.append(line)

    with open(path, 'r+') as fp:
        fp.writelines(lines)
        
def write_line(path, line, mystr):
    """
    writes Readme.md in line 

    Arguments
    ---------

    path: pathlib object (e.g. Path('minibrain')
    line: (int) the line to write
    mystr: message to add to Readme.md in the line
    """
    # read file in a list (fp.readlines()
    with open(path, 'r') as fp:
        lines = fp.readlines()

    lines[line] = mystr 
    with open(path, 'r+') as fp:
        fp.writelines(lines)

if __name__ == '__main__':
    from pathlib import Path
    from minibrain.transformers import PandasReader

    # Globals
    HOME = Path.home()
    GIT = Path(HOME, 'git', 'minibrain', 'DataSets')
    # directories where recordings are located
    TC = Path(HOME, 'Guzman.VCB', 'TSC2', 'Analysis' , 'SiliconProbes',
        'waveforms')
    VT = Path(HOME, 'Guzman.VCB', 'DLXi56', 'Analysis' , 'SiliconProbes',
        'VT', 'waveforms')
    FH = Path(HOME, 'Guzman.VCB', 'DLXi56', 'Analysis' , 'SiliconProbes',
        'FH', 'waveforms')
    FS = Path(HOME, 'Guzman.VCB', 'DLXi56', 'Analysis' , 'SiliconProbes',
        'FS', 'waveforms')
    AP = Path(HOME, 'Guzman.VCB', 'AP', 'Analysis' , 'SiliconProbes',
        'waveforms')

    pathlist = [VT, FS, FH, TC, AP]


    dfreader = PandasReader(extension = '*df') # all *df files

    dfspikes_list = list()
    dfwaveforms_list = list()
    dforganoid_list = list()
    nsamples = 0 # counter
    for mypath in pathlist:
        dfspikes = dfreader.transform(path = mypath)
        print(f'{"#"*73}')
        print(f'{mypath}')
        print(f'{dfreader.nrecords:3d} spikes')
        print(f'{len(dfreader):3d} samples\n')
        nsamples +=len(dfreader)
        dfwaveforms = pd.DataFrame(dfspikes['waveform'].tolist(),
                index = dfspikes.index)
        dfwaveforms['organoid'] = dfspikes['organoid'] # copy organoid type

        dfspikes.drop('waveform', axis = 1, inplace = True)
        dforganoid = pd.DataFrame(dfspikes['organoid'].tolist(),
                columns = ['organoid'], index = dfspikes.index)

        # both dfspikes and dfwaveforms maintain 'organoid' column
        dfspikes_list.append(dfspikes)
        dfwaveforms_list.append(dfwaveforms)
        dforganoid_list.append(dforganoid)

    # merge in GitHub all organoids together 
    # verify that we have unique index with ignore_index = False
    # sort=True is because AP organoids have location column
    dfspikes = pd.concat(dfspikes_list, ignore_index = False, sort=True)
    dfwaveforms = pd.concat(dfwaveforms_list, ignore_index = False)
    dforganoid = pd.concat(dforganoid_list, ignore_index = False)


    # Create/update Datasets in git 
    #logging.info(f'Saving  {dfspikes.shape[0]:4d} spike waveforms in {git}')
    dfspikes.to_csv(Path(GIT ,'spikes.csv'), index = True)
    dfwaveforms.to_csv(Path(GIT, 'waveforms.csv'), index = True)
    dforganoid.to_csv(Path(GIT, 'organoID.csv'), index = True)
    mytotal = f'The dataset contains a total of {dfspikes.shape[0]:3d} spikes in {nsamples} samples.\n'

    print(mytotal)
    myreadme = Path(GIT, 'Readme.md')
    write_line(myreadme, line = 2, mystr = mytotal)
    #write_readme(path = Path(GIT, 'Readme.md'), mystr = mytotal)
