"""
waveforms_unittest.py

Author: Jose Guzman, jose.guzman<at>guzman-lab.com
Created: Sun Nov  1 17:50:10 CET 2020

Unit-testing for kinetic parameters of extracellular
waveforms
"""

import unittest

import pandas as pd
from minibrain.loader import spike_kinetics

class TestWaveforKinetics(unittest.TestCase):
    """
    Unittest for testing kinetic parameters
    of extracellular spike waveforms.
    """

    def setUp(self):
        """
        Load some random extracellular spikes
        """
        waveforms = pd.read_csv('DataSets/waveforms.cvs', index_col = 'uid')


if __name__ == '__main__':
    unittest.main()
