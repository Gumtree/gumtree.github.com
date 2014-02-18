import inspect
from java.lang import System
import time
import math
from gumpy.nexus.fitting import Fitting, GAUSSIAN_FITTING
from gumpy.commons import sics
from Experiment.lib import sicsext
# Script control setup area
# script info
__script__.title = 'Align s2'
__script__.version = ''

previous_file = '1_align_m1.py'
next_file = '3_align_a2.py'

pact = Act('previous_step()', '<- Previous Step')
    
G1 = Group('Align S2 at 0')
s2 = Par('float', 0)
scan = Par('string', str(math.ceil((s2.value + 2) * 1000) / 1000) + ', -0.2, 21, \'timer\', 1')
act1 = Act('find_s2()', 'Find s2 Zero')
def find_s2():
    aname = 's2'
    try:
        if DEBUGGING :
            aname = 'dummy_motor'
    except:
        pass
    axis_name.value = aname
    sicsext.call_back = __load_experiment_data__
    slog('scan ' + aname + ', ' + scan.value)
    exec('sicsext.runbmonscan(\'' + aname + '\', ' + scan.value + ', 0, \'call_back()\')')
    time.sleep(2)
    fit_curve()

    
G1.add(s2, scan, act1)

G2 = Group('Fitting')
data_name = Par('string', 'bm2_counts', \
               options = ['bm1_counts', 'bm2_counts'])
axis_name = Par('string', 's2')
peak_pos = Par('float', 'NaN')
offset_done = Par('bool', False)
act3 = Act('offset_s2()', 'Set s2 Zero Offset')
G2.add(data_name, axis_name, peak_pos, offset_done, act3)
def offset_s2():
    aname = 's2'
    try:
        if DEBUGGING :
            aname = 'dummy_motor'
    except:
        pass
    if offset_done.value :
        print 'You have already set the zero offset of ' + aname
    else:
        slog('drive ' + aname + ' ' + str(peak_pos.value))
        sics.drive(aname, peak_pos.value)
        slog('set peak position to ' + str(s2.value))
        sics.setpos(aname, peak_pos.value, s2.value)
        offset_done.value = True
        print 'done'
    
nact = Act('next_step()', 'Next Step ->')
    
def fit_curve():
    __std_fit_curve__()

# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
    __std_run_script__(fns)

def auto_run():
    pass

def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
