'''
Created on 11/02/2014

@author: jrh
'''
__script__.title     = 'Plot monitor'
__script__.version   = '1.0'
#
#  Create the GUI
#
monitors = {'Pre-mono':'/entry1/monitor/bm1_counts',
            'Post-mono':'/entry1/monitor/bm2_counts',
            'Post-sample':'/entry1/monitor/bm3_counts'}
mon_choice = Par('string','Pre-mono',options=monitors.keys())
mon_choice.title = 'Location'
mon_norm = Par('bool','False')
mon_norm.title = 'Normalise'
Group('Monitor Plot').add(mon_choice,mon_norm)
#
plh_copy = Act('plh_copy_proc()', 'Copy plot')
Group('Copy 1D Datasets to Plot 3').add(plh_copy)

def __run_script__(fns):
    # check input
    if (fns is None or len(fns) == 0) :
        print 'no input datasets'
        open_error('No input datasets')
        return

    df.datasets.clear()    #Erase previous fiddling
    clear_plot(Plot1)      #Remove old plots
    # Get the NeXuS path
    mon_path = monitors[mon_choice.value]
    for fn in fns:
        ds = df[fn]
        mon_counts = Dataset(ds[mon_path])
        if mon_norm.value is True:
            real_mon_counts = mon_counts/mon_counts.max()
            y_label = 'Normalised counts'
        else:
            real_mon_counts = mon_counts
            y_label = 'Counts'
        real_mon_counts.title = ds['/entry1/sample/name'] + ':' + mon_choice.value
        Plot1.add_dataset(real_mon_counts)
        Plot1.set_y_label(y_label)
    Plot1.set_x_label('Step')
    Plot1.set_title('Monitor counts')

             
def clear_plot(plotname):
    all_datasets = copy(plotname.ds)
    if plotname.ds is None:
        return
    for ds in all_datasets:
        plotname.remove_dataset(ds)

def plh_copy_proc():
    # We copy from Plot 1 to Plot 3
    if type(Plot1.ds) is not list:
        print 'Plot1 does not contain 1D datasets'
        return
    
    if type(Plot3.ds) is not list:
        dst_ds_ids = []
    else:
        dst_ds_ids = [id(ds) for ds in Plot3.ds]
    
    for ds in Plot1.ds:
        if id(ds) not in dst_ds_ids:
            Plot3.add_dataset(ds)
