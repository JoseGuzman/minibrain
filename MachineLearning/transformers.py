"""
transformers.py

Jose Guzman, jose.guzman <at> guzman-lab.com

Created: Thu Sep 17 21:56:11 CEST 2020

Contains dataframe transformers for feature selection, 
feature scaling, feature encoders, collected into pipelines 
to be tested with different machine learning methods.

"""

from sklearn.base import BaseEstimator, TransformesMixin

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


mycolors = {'TSCp5_30s':     '#FFA500', # orange
          'TSCp5_32s':       '#4169E1', # royalblue
          'DLX_bluered':     '#00BFFF', # deepskyblue
          'DLX_Cheriff':     '#006400', # darkgreen
          'DLX_Cheriff_AS' : '#4B0082'  # indigo
    }


class ColumnsDelete():
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
        """
        mydf = df.copy() # create a new dataframe

        if self.columns:
            mydf.drop(self.columns, axis=1, inplace=True)

        return mydf


class OneHotEncoder():


Pipeline( steps = )

