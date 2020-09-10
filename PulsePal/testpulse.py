#!/usr/bin/python2.7
"""
testpulse.py

Jose Guzman, jose.guzman<at>guzman-lab.com

This script delivers one PULSE of 500 ms
every x seconds repeteadly upon activation of Trig1.

To load a 500 ms Pulse repeteadly delivered. For example,
>>> python testpulse.py -s 5 -out 2 -dir '/data/

will deliver a pulse in Out2 every 5 seconds and save a log file in /data

Activate Trigger1 to activate/deactivate the repeated pulse
"""

import argparse
from PulsePal import PulsePalObject as pulse

def loadpulse(args):
    """
    Create a 500 ms pulse delivered every 'sec' and load its
    in PulsePal v2.0
    """
    mypulse = pulse()
    mypulse.connect('/dev/ttyACM0')
    print('PulsePal (v2.0) firmware %d'%mypulse.firmwareVersion)
    mypulse.setDisplay('testpulse5sec.py', 'pulse2 every 1 sec')

    output = args['out']
    # define a PULSE 
    mypulse.triggerMode[2] = 0 # trigger on/off
    mypulse.triggerMode[1] = 1 # no trigger

    mypulse.isBiphasic[output] = 0 # monophasic
    mypulse.restingVoltage[output] = 0 # in volts
    mypulse.phase1Duration[output] = 0.5 # in volts
    mypulse.phase1Voltage[output] = 5 # in volts
    mypulse.interPulseInterval[output] = args['sec']-0.5 # every 5 sec.
    mypulse.setContinuousLoop(output,1) # repeatedly

    mypulse.syncAllParams()

    mypulse.disconnect()

if __name__ == '__main__':
    import logging
    from datetime import datetime

    # Parser
    parser = argparse.ArgumentParser(description='repeats a 500 ms pulse')
    # --out output channel
    parser.add_argument('--out', '-o', type = int, 
        help = 'Output channel', required = True)
    # --sec repetition interval 
    parser.add_argument('--sec', '-s', type = int, 
        help = 'repetition interval', required = True)
    # --dir  directory to save log (default /data)
    parser.add_argument('--dir', '-d', type = str, default = '.',
        help = 'directory to save log (default current)', required = False)
    myargs = vars(parser.parse_args())

    # Logging
    mytime = datetime.now()
    lognow = mytime.strftime('%Y-%m-%d_%H-%M-%S')
    logdate = mytime.strftime('%Y-%m-%d')
    logtime = mytime.strftime('%H-%M-%S')
    myfname = myargs['dir'] + '/testpulse_' + lognow + '.log'
    logging.basicConfig(filename = myfname, level = logging.DEBUG)
    logging.info(' Loading testpulse.py in PulsePal v2.0')
    logging.info(' Date: %s'%logdate)
    logging.info(' Time: %s'%logtime)
    
    output = (myargs['out'], myargs['sec'])
    logging.info(' OUT[%d] delivered 500 ms every %d sec'%(output))

    loadpulse(args = myargs)
