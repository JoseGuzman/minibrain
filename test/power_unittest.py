"""
power_unittest.py

Author: Jose Guzman, jose.guzman@guzman-lab.com
Created: Thu Feb 20 13:31:16 CET 2020
"""

import unittest
import logging
import sys

import numpy as np
from numpy import pi as PI
from minibrain.lfp import power
from minibrain.lfp import fourier_spectrum


class TestPowerObject(unittest.TestCase):
    """
    Unittesting for objects in minibrain.lfp
    """
    
    def setUp(self):
        """
        Create a sine wave
        """
        self.logW = logging.getLogger("Welch's method")
        self.logF = logging.getLogger("Discrete Fourier")
        self.srate = 30000 # 30 kHz

        # 60-seg sine wave of 10 units amplitude
        t = np.linspace(0, 60, num = 60*self.srate)
        self.wave = lambda f: np.sin( 2*PI*f*t )

    def test_Fourier_amplitudes(self):
        """
        Test that the discrete Fourier transform computes
        the right amplitudes.
        """
        self.logF.debug('Amplitude analysis with Fourier\n')
        for amp in np.random.uniform(low=1,high=100,size = 10):
            mywave = amp*self.wave(5) # 5 Hz wave 
            f, myamp = fourier_spectrum(data = mywave, srate=self.srate)

            info = 'Wave amplitude = {:7.5f}, Fourier = {:7.5f}'
            self.logF.debug(info.format(amp, myamp.max()))

            # Once rounded to 4 places, the difference is 0.00001
            self.assertAlmostEqual(amp, myamp.max(), 4, 1e-5)
        
    def test_Fourier_frequencies(self):
        """
        Test that the discrete Fourier transform computes
        the right frequencies.
        """
        self.logF.debug('Frequency analysis with Fourier\n')
        for freq in np.random.uniform(low=1, high=100, size = 10):
            mywave = self.wave(freq)
            f, myamp = fourier_spectrum(data = mywave, srate=self.srate)
            myfreq = f[myamp.argmax()]

            info = 'Wave frequency = {:7.5f}, Fourier = {:7.5f}'
            self.logF.debug( info.format(freq, myfreq) )

            # Once rounded to 2 places, the difference is 0.001
            self.assertAlmostEqual(freq, myfreq, delta = 0.1)
        
    def test_Welch_amplitudes(self):
        """
        Test that the Welch's periodogram in power computes
        the right frequencies.
        """
        myparams = dict(srate = self.srate, segment = self.srate*5)

        self.logW.debug('Amplitude analysis with Welch\n')
        for amp in np.random.uniform(low=1,high=100,size = 10):
            mywave = amp*self.wave(5) # 5 Hz wave 
            f, mypower = power.welch(data = mywave, **myparams)
            myamp = np.sqrt( mypower.max() )

            info = 'Wave amplitude = {:7.5f}, Welch = {:7.5f}'
            self.logW.debug(info.format(amp, myamp))

            # Once rounded to 5 places, the difference is 0.00001
            self.assertAlmostEqual(amp, myamp, 5, 1e-5)

    def test_Welch_frequencies(self):
        """
        Test that the Welch's periodogram in power computes
        the right frequencies.
        """
        myparams = dict(srate = self.srate, segment = self.srate*5)

        self.logW.debug('Frequency analysis with Welch\n')
        for freq in np.random.uniform(low=1, high=100, size = 10):
            mywave = self.wave(freq)
            f, mypower = power.welch(data = mywave, **myparams)
            myfreq = f[mypower.argmax()]

            info = 'Wave frequency = {:7.5f}, Welch = {:7.5f}'
            self.logW.debug( info.format(freq,myfreq) )

            # Once rounded to 2 places, the difference is 0.01
            self.assertAlmostEqual(freq, myfreq, delta = 0.1)


if __name__ == '__main__':
    logging.basicConfig(stream = sys.stderr, level=logging.DEBUG)
    unittest.main() 
