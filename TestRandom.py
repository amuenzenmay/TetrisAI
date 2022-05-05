import os
import pickle

qvalues = None
if os.path.getsize('qvalues.pickle') > 0:
    f_myfile = open('qvalues.pickle', 'rb')
    qvalues = pickle.load(f_myfile)  # variables come out in the order you put them in
    f_myfile.close()

with open('C:/Users/Augie/Desktop/Policy.csv', 'w') as f:
    for key in qvalues.keys():
        f.write("%s,%s,%s,%s,%s\n" % (key[0],key[1], key[2], key[3], qvalues[key]))

