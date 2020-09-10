"""
baseline10min.py

Jose Guzman, jose.guzman<at>guzman-lab.com

This script delivers on PULSE of 500 ms

To load it in Pulse Pal type:
>>> python singlepulse10.py

and press <Single Train> to start
"""

import time
from PulsePal import PulsePalObject as pulse

mypulse = pulse()
mypulse.connect('/dev/ttyACM0')
print('PulsePal (v2.0) firmware %d'%mypulse.firmwareVersion)

mypulse.setDisplay('baseline10min.py', 'pulse2 every 20 sec')

# define a PULSE 
mypulse.triggerMode[2] = 0 # no trigger
mypulse.isBiphasic[2] = 0 # monophasic
mypulse.restingVoltage[2] = 0 # in volts
mypulse.phase1Duration[2] = 0.5 # in volts
mypulse.phase1Voltage[2] = 5 # in volts
mypulse.interPulseInterval[2] = 19.5 # every 20 sec.
mypulse.setContinuousLoop(2,0)

mypulse.pulseTrainDelay[2] = 0 # zero delay
mypulse.pulseTrainDuration[2] = 600 # train of 600 seconds 
mypulse.customTrainLoop[2] = 1 # end defined in pulseTrainDuration

mypulse.syncAllParams()

mypulse.disconnect()
