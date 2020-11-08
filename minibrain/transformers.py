"""
transformers.py

Jose Guzman, jose.guzman <at> guzman-lab.com

Created: Thu Sep 17 21:56:11 CEST 2020

Custom transformers inherit from TransformerMixin to
obtain fit_transform() based on custom fit and transform methods
Inherinting from BaseEstimator we get get_params and set_params

Contains dataframe transformers for feature selection, 
feature scaling, feature encoders, collected into pipelines 
to be tested with different machine learning methods.

"""
import os
from pathlib import Path
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

from minibrain import EphysLoader, Units

# custom matplotlib colors for different organoids
mycolors = {'TSCp5_30s':     '#FFA500', # orange
          'TSCp5_32s':       '#4169E1', # royalblue
          'DLX_bluered':     '#DAA520', # goldenrod 
          'DLX_Cheriff':     '#228B22', # forestgreen
          'DLX_Cheriff_AS':  '#32CD32', # limegreen
          'DLX_H9' :         '#006400', # darkgreen 
          'AP_ctrl':         '#EE82EE', # violet 
          'AP_drug':         '#DC143C'  # crimson
    }

class PandasReader(BaseEstimator, TransformerMixin):
    """
    Reads the list of pandas files (eg., *df) in a directory 
    and creates a unique pandas DataFrame

    Usage
    -----
    >>> from transformers import PandasReader
    >>> myreader = PandasReader(extension = 'df')
    >>> df = myreader.transform(dir = 'waveforms/')
    >>> len(myreader) # returns the number of files (i.e. organoids)
    >>> myreader.nrecords # returns the number of recordings
    """

    def __init__(self, extension = '*df', path = None):
        """
        Select which extesion will be used to load pandas
        Dataframes (by default *.df).

        Parameter
        ---------
        extension: str
            The extension of DataFrame object (by default
            df).
        path:  a pathlib object 
            containing the directory to read extension file 
            (e.g., Path('waveforms'))
        """
        self.extension = extension
        if path is None:
           self.path = Path()

        self._nfiles = 0 # number of files loaded
        self._nrecords = 0 # number of recordings made

    def fit(self, X, y = None):
        """
        Nothing to do here
        """
        return self
   
    def transform(self, extension = None, path = None):
        """
        Returns a pandas DataFrame with all the DataFrame
        files found in the directory (e.g. 'waveforms/').

        Parameter
        ---------
        extension: str
            The extension of DataFrame object (by default
            df).
        path:  a pathlib object 
            containing the directory to read extension file 
            (e.g., Path('waveforms'))
        """
        # if we change the values defined at construction
        if extension is not None:
            self.extension = extension
        if path is not None:
            self.path = path

        flist = self.path.glob( self.extension )

        frames = [pd.read_pickle(df) for df in flist]
        self._nfiles = len(frames)
        df = pd.concat(frames, sort=False, ignore_index=True)
        df.set_index('uid', inplace=True)

        self._nrecords = df.shape[0]

        return df 

    def __len__(self):
        """
        Count the number of files loaded
        """
        return self._nfiles

    nrecords = property(lambda self: self._nrecords)

class WaveformExtractor(BaseEstimator, TransformerMixin):
    """
    Reads a csv file to create the paths for the binaries 
    and the clustering file (cluster_info.csv), to create 
    a pandas DataFrame with spike waveforms and kinetics.

    The csv file must contain: expID, binarypath, experiment
    recording, Channel_Map, EB, nchan and organoid.

    Usage
    -----
    >>> from transformers impor WaveformExtractor
    >>> mywaveforms = WaveforExtractor()
    >>> mydf = mywaveforms.fit_transform(fname = 'filelist.csv')
    """
    def __init__(self, split_waveforms = False):
        """
        Reads csv file containing the following columns:
        'expID', 'binarypath', 'experiment', 'recording', 
        'Channel_Map', 'EB', 'nchan' and 'organoid'.

        Columns are all necessary and case-sensitive!

        Arguments
        ---------

        split_waveforms (bool)

            True if returns the sampling points of the 
        normalized waveforms as a second panda DataSet.
        """
        self.split_waveforms = split_waveforms

    def __get_units(self,prefix,organoid,spk_path,**loader_params):
        """
        Reads units from path, and extract all kinetic parameters
        and the waveform in every normalized spike.

        Arguments
        ---------
        prefix (str)
            This is the recording prefix (e.g. VT001) that 
        corresponding to a single experiment.

        organoid (str)
            The organoid type used (e.g., DLX_Cheriff for 
        ventralized organoids containing blue Channelrhodopsin)

        spk_path (str)
            It is the path to cluster_info.csv generated by
        KiloSort2. It is need for Units objects to read the
        spike clusters.

        **loader_params (kwargs)
            A dictionary with the parameters to pass to the
        EphysLoader object.

        Returns
        -------
        A list of dictionaries with all spike waveform kinetics
        together with an unique identifier (uid) corresponding
        to the expID + cluster_id.
        
        """
        # first load Units and Ephysloader objects
        myrec = EphysLoader(**loader_params)
        myunits = Units(spk_path) # return good spike clusters
        df = myunits.df

        # to obtain kinetic properties from all units
        # we create a list of dictionaries
        dict_list = list()
        for idx in df.index: # idx are cluster_ids
            myspk = myunits.unit[idx]
            spike_kinetics = myrec.waveform_kinetics(
                    spk_times = myspk, 
                    channel = df.loc[idx].channel)
            sh = df.loc[idx].shank
            spike_kinetics['uid'] = prefix + f'_{idx:03d}' + sh
            # add relevant data from KiloSort2 clustering
            spike_kinetics['frequency'] = df.loc[idx].frequency
            spike_kinetics['n_spikes'] = df.loc[idx].n_spikes
            spike_kinetics['ISI.median'] = df.loc[idx,'ISI.median']
            # add relevant recording properties
            spike_kinetics['age'] = myrec.age/30 # in months
            spike_kinetics['organoid'] = organoid # from csv file
            dict_list.append( spike_kinetics )


        # create unique identifiers (uid)
        df.reset_index(inplace=True) # cluster_id is not index
        df['uid']=df.cluster_id.apply(lambda x: prefix+f'_{x:03d}')

        return dict_list 
        
    def fit(self, X, y = None, **fit_params):
        """
        Returns the transformer object, nothing to do here
        """
        return self
        

    def transform(self, df, **transform_params):
        """
        Merge the columns in a single path to load 
        both the binary file and the location of 
        'cluster_info.csv' from KiloSort2. The units object
        from minibrain will load the spike times from every
        isolated unit form 'spike_times.npy' & 'spike_clusters.npy'
        and it will create a DataFrame with kinetic parameters
        from the normalized waveforms.

        Parameter
        ---------
        df - a DataFrame pandas object

        """

        #df = pd.read_csv(fname)
        mycols = ['expID', 'binarypath', 'experiment','recording',
                'Channel_Map', 'EB', 'nchan', 'organoid']

        for val in mycols:
            if val not in df.columns:
                raise ValueError(f'{val} column not found')

        # dataframe accomodation to EphysLoader and Units objects
        # set index to 'expID'
        # transform recording and experiment number to strings
        df.set_index('expID', inplace = True)
        df.recording = pd.to_numeric(df.recording, \
                downcast = 'integer').astype(str)
        df.experiment = pd.to_numeric(df.experiment, \
                downcast = 'integer').astype(str) 
        df.nchan = pd.to_numeric(df.nchan, downcast='integer') 
        
        # read every line of the csv file to get units
        myhome = os.environ['HOME']
        units_list = list() # a list of dictionaries
        for idx in df.index:
            binary = os.path.join(myhome, df.loc[idx].binarypath)
            experiment = 'experiment' + df.loc[idx].experiment
            recording  = 'recording'  + df.loc[idx].recording  
            channelmap = 'Channel_Map-' + df.loc[idx].Channel_Map
            # dictionary of parameter for EphysLoader
            params = dict()
            rec_path = os.path.join(binary, experiment, \
                    recording,'continuous', channelmap)
            params['fname']=os.path.join(rec_path,'continuous.dat')
            day = df.loc[idx].binarypath.split('_')[1]
            time = df.loc[idx].binarypath.split('_')[2]
            mydate = day + '_' + time
            params['date'] = mydate.replace('/', '-')
            params['birth'] = df.loc[idx, 'EB'].replace('/','-')
            params['nchan'] = df.loc[idx].nchan


            # prepare to read all units from that file
            organoid = df.loc[idx].organoid
            spk_path = os.path.join(rec_path, 'sorting/')
            # will return a list of units
            mylist =self.__get_units(prefix=idx,organoid=organoid,\
                    spk_path = spk_path, **params)
            units_list.extend( mylist )
            #units.extend( df )

        mydf = pd.DataFrame(units_list)
        # set unique identifier based on cluster_id
        mydf.set_index('uid', inplace=True)

        if self.split_waveforms:
            dfspikes = mydf.loc[:, mydf.columns !='waveform']
            dfwaveforms = pd.DataFrame(mydf['waveform'].tolist(), 
                    index = mydf.index)
            dfwaveforms['organoid'] = mydf.organoid 

            mytuple = (dfspikes, dfwaveforms)
        else:
            mytuple = (mydf,None)

        return mytuple

class ColumnsDelete(BaseEstimator, TransformerMixin):
    """
    A feature selection transformer to delete a list of 
    features from a pandas dataframe.
    """
    def __init__(self, columns = None):
        self.columns = columns

    def fit(self, df, y = None, **fit_params):
        """
        Parameter
        ---------
        df (Pandas DataFrame object)
        a Pandas DataFrame object.
        Returns the transformer object, nothing to do here
        """
        return self

    def transform(self, df, **transform_params):
        """
        Deletes the column from a dataframe

        Parameter
        ---------
        df (Pandas DataFrame object)
        a Pandas DataFrame object.

        Returns
        -------
        A new pandas DataFrame with the columns removed
        """

        if self.columns:
            df.drop(self.columns, axis=1, inplace=True)

        return df

#class OneHotEncoder():
#Pipeline( steps = )
