# -*- coding: utf-8 -*-

"""
minibrain: 

A python module to analyze electrophysiology and calcium imaging in minibrains

"""

#-------------------------------------------------------------------------
# Global variables
#-------------------------------------------------------------------------
__version__ = '0.6'
__author__ = 'Jose Guzman'
__email__ = 'jose.guzman at guzman-lab.com'


#-------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------
from minibrain.loader import EphysLoader # from minibrain import EphysLoader
from minibrain.spikes import Units # from minibrain import Units
from minibrain.extracellular import LFP as lfp  
from minibrain.extracellular import Burst as burst 
