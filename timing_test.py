from time import time
p = Dataset('/home/jrh/programs/echidna/Echidna-Gumtree-Scripts/Data/ECH0010240.nx.hdf')
print 'Read in dataset, shape: ' + `p.shape`
print 'Summing %d points individually' % (p.shape[-1]*p.shape[-2])
c = time()
result = 0
for point in p.storage[0].flatten():
    result = result + point
d = time()
print 'Result %d, required %f seconds' % (result,(d-c))
#
print 'Instead of ',
c = time()
result = p.storage[0].flatten().sum()
d = time()
print '%d in %f seconds' % (result, (d-c))