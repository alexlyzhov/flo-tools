import numpy as np
import matplotlib.image as mpimg

flo_magic = 202021.25

def read_flo(path):
    f = open(path, 'rb') # b for binary
    
    # check file
    if np.fromfile(f, np.float32, count=1) != flo_magic:
        raise Exception('Invalid .flo file') 

    # read width and height
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

def write_flo(flow, path):
    f = open(path, 'wb') # b for binary
    
    # write magic header
    np.float32(flo_magic).tofile(f, sep = '')
    
    # write width and height
    f.seek(4)
    np.int32(flow.shape[1]).tofile(f)
    
    f.seek(8)
    np.int32(flow.shape[0]).tofile(f)
    
    # write data
    f.seek(12)
    flow.astype(np.float32).tofile(f)
    
    f.close()

def read_img(path):
    return mpimg.imread(path)
