"""
pipeline.py

Jose Guzman, jose.guzman <at> guzman-lab.com

Created: Thu Sep 17 21:56:11 CEST 2020
"""

from sklearn.pipeline import Pipeline

class ColumnsDelete():
    """
    A custom transformer to delete a list of 
    features from a pandas dataframe.
    """
    def __init__(self, columns = None):
        self.columns = columns

    def fit(self, X, y = None, **fit_params):
        """
        Returns the transformer object, nothing to do here
        """
        return self

    def transform(self, X, **transform_params):
        """
        Deletes the column from a dataframe
        """
        mydf = X.copy() # create a new dataframe

        if self.columns:
            mydf.drop(self.columns, axis=1, inplace=True)

        return mydf




