import numpy as np
import matplotlib.colors

def flow_to_color(flow, norm):
    '''
    Middlebury colorcoding of optical flow
    Returns color image with hue representing vector angle
    and saturation representing vector module
    
    Keyword arguments:
        flow -- optical flow to colorcode
    '''
    rho = np.sqrt(flow[:, :, 0] ** 2 + flow[:, :, 1] ** 2)
    max_rho = np.max(rho)
    phi = np.arctan2(flow[:, :, 1], flow[:, :, 0])
    phi[phi < 0] = 2 * np.pi + phi[phi < 0]
    
    hue = phi / (2 * np.pi)
    if norm:
        sat = rho / max_rho
    else:
        sat = rho
    val = np.ones((flow.shape[0], flow.shape[1]))
    
    img = matplotlib.colors.hsv_to_rgb(np.stack((hue, sat, val), axis = -1))
    return img

def warp_img(img, flow, forward, over_from_points, init_zeros):
    '''
    Returns image warped according to an optical flow
    
    Keyword arguments:
        img -- image to warp
        flow -- optical flow between a pair of images
        forward (bool) -- warp forward vs backward
        over_from_points (bool) -- warp over from-points vs to-points
        init_zeros (bool) -- init with zeros vs with img
    '''
    if init_zeros:
        warp = np.zeros_like(img)
    else:
        warp = img.copy()
        
     # later interpolate
     # forward without interpolation?
     # backward: interpolate pixel based on neighbors of that second image pixel!
        
    for i in xrange(img.shape[0]):
        for j in xrange(img.shape[1]):
            if over_from_points:
                new_i = int(np.round(i + flow[i, j, 0]))
                new_j = int(np.round(j + flow[i, j, 1]))
            else:
                new_i = int(np.round(i - flow[i, j, 0]))
                new_j = int(np.round(j - flow[i, j, 1]))
            if new_i >= 0 and new_i < flow.shape[0] and new_j >= 0 and new_j < flow.shape[1]:
                if forward == over_from_points:
                    warp[new_i, new_j] = img[i, j]
                else:
                    warp[i, j] = img[new_i, new_j]
                    
    return warp