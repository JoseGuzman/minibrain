"""
spikes.py

Jose Guzman, jose.guzman@guzman-lab.com

Created: Mon Jul 29 20:59:51 CEST 2019

Contains a class to load extracellular spikes recorded 
Cambride Neurotech silicon probes, sorted with spyking-circus
and curated with phy.

Example:
>>> from spikes import UnitsLoader 
>>> myrec = DataLoader('./') # will load shankA, shankB, shankC and shankD
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

myshank = {1.0:'A', 2.0:'B', 3.0:'C', 4.0:'D'}
read_shank = lambda x: myshank[x]

class UnitsLoader(object):
	"""
	A class to load extracellular units recordings acquired
	with 64 probes silicon probes from Cambridge Neurotech 
	"""
	# A dictionary with shanks ID and colors
	shank = {'A': range(16),
		'B': range(16,32),
		'C': range(32,48),
		'D': range(48,64)
		}
	color = {'A': '#A52A2A',
		'B': '#0095FF',
		'C': '#FF9933',
		'D': '#00AA00' 
		}
	def __init__(self, mytuple='None', path = ""):
		"""
		Reads phy files with sorted probes 

		Arguments:
		----------
		"""
		self.duration = self.set_duration(mytuple)

		self.dfA = self._read_csv(path + 'shankA')
		self.dfB = self._read_csv(path + 'shankB')
		self.dfC = self._read_csv(path + 'shankC')
		self.dfD = self._read_csv(path + 'shankD')
		

	def _read_csv(self, shank):
		"""
		Loads cvs generated files into a pandas DataFrame
		and saves files with the spikes per minute.
		Arguments:
		----------
		shank (str) 'shankA', 'shankB', 'shankC' or 'shankD'
		"""

		mypath = '/wc_continuous.GUI/cluster_info.tsv'
		df = pd.read_csv( shank + mypath, sep='\t')
		# substitute number by shank type 'A', 'B','C' or 'D'
		df['shank'] = df['shank'].apply(read_shank)

		# select well isolated units
		df_units = df[df['group'] == 'good']
		n_units = len(df_units)
		print( '%d extracellular units in %s'%(n_units, shank) )
		#if n_units:
			#spm = df_units['n_spikes'].values
			#spm = spm/(self.duration/60000)
			#print(spm)
			#print( 'Average spk/min = %2.4f'%spm.mean())
			#np.savetxt(shank + '.spm', spm, fmt='%f')
		return( df_units )

	@duration.setter
	def set_duration(self, mytuple):
		"""
		Set the recording duration in ms
		"""
		m, s, ms = mytuple
		self._duration = int(m*60000 + s*1000 + ms)
		print('Total duration %d'%self.duration )


	duration = property(lambda self: self._duration)