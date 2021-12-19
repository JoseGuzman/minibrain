"""
singlepulse10.py

Jose Guzman, jose.guzman<at>guzman-lab.com

This script delivers on PULSE of 500 ms
every 10 seconds repeteadly.

To load it in Pulse Pal type:
>>> python singlepulse10.py

and press <Single Train> to start
"""

import time
from PulsePal import PulsePalObject as pulse

mypulse = pulse()
mypulse.connect('/dev/ttyACM0')
print('PulsePal (v2.0) firmware %d'%mypulse.firmwareVersion)

mypulse.setDisplay('singlepulse10.py', 'pulse2 every 10 sec')

# define a PULSE 
mypulse.triggerMode[2] = 0 # no trigger
mypulse.isBiphasic[2] = 0 # monophasic
mypulse.restingVoltage[2] = 0 # in volts
mypulse.phase1Duration[2] = 0.5 # in volts
mypulse.phase1Voltage[2] = 5 # in volts
mypulse.interPulseInterval[2] = 9.5 # every 1 sec.
mypulse.setContinuousLoop(2,1)

mypulse.syncAllParams()

#mypulse.disconnect()
# leaving this line commented allows you to use ipython to 
# run the script ;
