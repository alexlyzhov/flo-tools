import numpy as np
import matplotlib.image as mpimg

def read_flo(path):
    f = open(path, 'rb')
    
    # check file
    magic = 202021.25
    if np.fromfile(f, np.float32, count=1) != magic:
        raise Exception('Invalid .flo file') 

    # read image parameters
    f.seek(4)
    w = np.fromfile(f, np.int32, count=1)[0]
    
    f.seek(8)
    h = np.fromfile(f, np.int32, count=1)[0]
    
    # read data
    f.seek(12)
    data = np.fromfile(f, np.float32, count=w*h*2)

    f.close()
    resized = np.resize(data, (h, w, 2))
    return resized

def read_img(path):
    return mpimg.imread(path)
