from time import time

def timeit(start_time):
    print 'Time since start %f' % (time()-start_time)

p = Dataset('/home/jrh/programs/echidna/Echidna-Gumtree-Scripts/Data/ECH0010240.nx.hdf')
print 'Read in dataset, shape: ' + `p.shape`
start_time = time()
good_points = filter(lambda a:a>0,p.flatten())  
timeit(start_time)
gumtree_points = array.asarray(good_points)
timeit(start_time)

