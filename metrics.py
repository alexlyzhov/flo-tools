import numpy as np

intensity = lambda x: np.dot(x, [0.299, 0.587, 0.114])

def img_norm_diff(images):
    diff = np.abs(intensity(images[0]) - intensity(images[1]))
    diff_max = np.max(diff)
    if diff_max != 0:
        diff /= np.max(diff)
    return diff
    
def flow_norm_diff(flows):
    diff = flows[1] - flows[0]
    diff_mod = np.sqrt(diff[:, :, 0] ** 2 + diff[:, :, 1] ** 2)
    max_mod = np.max(diff_mod)
    if max_mod != 0:
        diff_mod /= np.max(diff_mod)
    return diff_mod

def ang_error(flows): # check
    # angular error: angle in 3D between (u0, v0, 1) and (u1, v1, 1) 
    # normalize and take arccos(dot product)
    norm_flows = []
    for i in xrange(2):
        flow3d = np.append(flows[i], np.ones(flows[i].shape[:-1] + (1,)), axis = 2)
        norm = np.linalg.norm(flow3d, axis = 2)
        norm = np.stack([norm] * 3, axis = 2)
        norm_flow = np.divide(flow3d, norm, out = np.zeros_like(flow3d), where = (norm != 0))
        norm_flows.append(norm_flow)
    dot = np.sum(np.multiply(norm_flows[0], norm_flows[1]), axis = 2)
    dot /= np.max(np.abs(dot))
    ang = np.arccos(dot)
    return np.mean(ang)

def epe_error(flows):
    # end-point error: length of diff vector
    diff = flows[1] - flows[0]
    diff_mod = np.sqrt(diff[:, :, 0] ** 2 + diff[:, :, 1] ** 2)
    return np.mean(diff_mod)

def ssd_error(images): # sum of squared differences
    return np.sum((intensity(images[0].astype(np.float) / 255) -
                   intensity(images[1].astype(np.float) / 255)) ** 2)