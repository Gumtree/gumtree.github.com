'''
Created on 11/02/2014

@author: jrh
'''
# Script control setup area
__script__.title     = 'Time utilities'
__script__.version   = '1.0'
#
st = Par('bool','False')
st.title = 'Show the time'
addon = Par('string','Stardate ')
addon.title = 'Prepend this:'

Group('Time').add(st,addon)

def __run_script__(fns):
    import demo_script
    if st.value is True:
        print addon.value + demo_script.format_time()
    else:
        print 'Madness takes control'


