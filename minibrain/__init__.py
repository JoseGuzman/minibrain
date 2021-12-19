# -*- coding: utf-8 -*-

"""
minibrain: 

A python module to analyze electrophysiology and calcium imaging in brain organoids.

"""

#-------------------------------------------------------------------------
# Global variables
#-------------------------------------------------------------------------
__version__ = 'v0.10'
__author__ = 'Jose Guzman'
__email__ = 'jose.guzman at guzman-lab.com'


#-------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------
from minibrain.loader import EphysLoader # from minibrain import EphysLoader
from minibrain.spikes import Units # from minibrain import Units
from minibrain.lfpmanager import lfp # from minibrain import lfp 
from minibrain.burstcounter import burst # from minibrain import burst
