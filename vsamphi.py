# Script control setup area
# script info
__script__.title = 'Scan vsamphi'
__script__.version = '0.1'

G1 = Group('Scan on vsamphi')
device_name = 'vsamphi'
arm_length = Par('float', 0)
scan_start = Par('float', 0)
scan_stop = Par('float', 0)
number_of_points = Par('int', 0)
scan_mode = Par('string', 'time', options = ['time', 'count'])
scan_mode.enabled = True
scan_preset = Par('int', 0)
act1 = Act('scan_device()', 'Scan on Device')
def scan_device():
    aname = str(device_name)
#    axis_name.value = aname
    np = int(number_of_points.value)
    if np <= 0:
        return
    if np == 1:
        step_size = 0
    else:
        step_size = float(scan_stop.value - scan_start.value) / (np - 1)
    slog('runscan ' + str(device_name) + ' ' + str(scan_start.value) + ' ' + str(scan_stop.value) \
                    + ' ' + str(number_of_points.value) + ' ' + str(scan_mode.value) + ' ' + str(scan_preset.value))
    if str(scan_mode.value) == 'time' :
        mode = quokka.hmMode.time
    elif str(scan_mode.value) == 'count':
        mode = quokka.hmMode.monitor
    else:
        mode = quokka.hmMode.time
    sics.run_command('newfile HISTOGRAM_XY')
    org_z = sicsext.getStableValue('samz').getFloatData()
    time.sleep(1)
    for p in xrange(np):
        samphi = scan_start.value + step_size * p
        slog('drive ' + aname + ' ' + str(samphi))
        sics.drive('samphi', scan_start.value + step_size * p)
        samz = calc_samz(samphi, arm_length.value, org_z)
        slog('drive samz ' + str(samz))
        sics.drive('samz', samz)
        quokka.driveHistmem(mode, scan_preset.value)
        sics.run_command('save ' + str(p))
        slog('finished NP ' + str(p))
        time.sleep(1)
    
G1.add(arm_length, scan_start, scan_stop, number_of_points, scan_mode, scan_preset, act1)


def calc_samz(samphi, length, org_z):
    return org_z - length * math.sin(samphi * math.pi / 180)
    
# Use below example to create a new Plot
# Plot4 = Plot(title = 'new plot')

# This function is called when pushing the Run button in the control UI.
def __run_script__(fns):
    global Plot1
    global Plot2
    global Plot3
    
    # check if a list of file names has been given
    if (fns is None or len(fns) == 0) :
        print 'no input datasets'
    else :
        for fn in fns:
            # load dataset with each file name
            ds = Plot3.ds
            if ds != None and len(ds) > 0:
                if ds[0].location == fn:
                    return
            df.datasets.clear()
            ds = df[fn]
            axis_name = 'samphi'
            dname = 'total_counts'
            data = ds[dname]
            axis = ds[axis_name]
            if not hasattr(axis, '__len__'):
                axis = SimpleData([axis], title = axis_name)
            ds2 = Dataset(data, axes=[axis])
            ds2.title = ds.id
            ds2.location = fn
            Plot1.set_dataset(ds2)
            Plot1.x_label = axis_name.value
            Plot1.y_label = dname
            Plot1.title = dname + ' vs ' + axis_name.value
            Plot1.pv.getPlot().setMarkerEnabled(True)

    
def __dispose__():
    global Plot1
    global Plot2
    global Plot3
    Plot1.clear()
    Plot2.clear()
    Plot3.clear()
