"""
unittest_test.py

Author: Jose Guzman, jose.guzman@guzman-lab.com
Created: Thu Feb 20 13:31:16 CET 2020
"""

import unittest
import logging
import sys

import numpy as np
from numpy import pi as PI
from minibrain.lfp import power


class TestPowerObject(unittest.TestCase):
    """
    Unittestin for Power object in minibrain.lfp
    """
    
    def setUp(self):
        """
        Create a sine wave
        """
        self.log = logging.getLogger('Log info ')
        self.srate = 30000 # 30 kHz

        # 60-seg sine wave of 10 units amplitude
        t = np.linspace(0, 60, num = 60*self.srate)
        self.wave = lambda f: np.sin( 2*PI*f*t )

    def test_Welch_amplitudes(self):
        """
        Test that the Welch's periodogram in power compute 
        the right frequencies.
        """
        myparams = dict(srate = self.srate, segment = self.srate*5)

        self.log.debug('\nAmplitude analysis\n')
        for amp in np.random.uniform(low=1,high=100,size = 10):
            mywave = amp*self.wave(5) # 5 Hz wave 
            f, mypower = power.welch(data = mywave, **myparams)
            myamp = np.sqrt( mypower.max() )
            info = 'Wave amplitude = {:7.5f}, Welch = {:7.5f}'.format(amp, myamp)
            self.log.debug(info)

            # Once rounded to 5 places, the difference is 0.00001
            self.assertAlmostEqual(amp, myamp, 5, 1e-5)

    def test_Welch_frequencies(self):
        """
        Test that the Welch's periodogram in power compute 
        the right frequencies.
        """
        myparams = dict(srate = self.srate, segment = self.srate*5)

        self.log.debug('\nFrequency analysis\n')
        for freq in np.random.randint(low=1, high=100, size = 10):
            mywave = self.wave(freq)
            f, mypower = power.welch(data = mywave, **myparams)
            myfreq = f[mypower.argmax()]
            info = 'Wave frequency = {:7.5f}, Welch = {:7.5f}'.format(freq,myfreq)
            self.log.debug(info)

            # Once rounded to 5 places, the difference is 0.00001
            self.assertAlmostEqual(freq, myfreq, 5, 1e-5)


if __name__ == '__main__':
    logging.basicConfig(stream = sys.stderr, level=logging.DEBUG)
    unittest.main() 
