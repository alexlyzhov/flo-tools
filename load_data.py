import glob

from read_data import read_flo, read_img

def read_flows(flow_patterns, n, first):
    flows = [[read_flo(pat.format(img_num)) for pat in flow_patterns] for img_num in xrange(first, n + first)]
    return flows

def read_imgs(img_patterns, n, first):
    imgs = [[read_img(img_pat.format(img_num)) for img_pat in img_patterns] for img_num in xrange(first, n + first)]
    return imgs

def read_img_laps(img_pat, n, first):
    imgs = [[read_img(img_pat.format(img_num)), read_img(img_pat.format(img_num + 1))]
            for img_num in xrange(1, n + 1)]
    return imgs

def read_flows_imgs(flow_patterns, img_patterns, n):
    flows = read_flows(flow_patterns, n, first = 0)
    imgs = read_imgs(img_patterns, n, first = 0)
    return flows, imgs

def get_data(dataset, name):
    if dataset == 'huawei':
        flo_dir = img_dir = '../huawei/cropped/' + name
        
        if '1027' in name:
            img_ext = 'png'
        else:
            img_ext = 'jpg'
    elif dataset == 'cells':
        (imgs_name, flows_name) = name.split('/')
        flo_dir = '../cells/' + name
        img_dir = '../cells/' + imgs_name
        
        img_ext = 'png'
        
        if 'gap1' not in name:
            raise Exception
    elif dataset == 'mydata':
        all_flows, all_imgs = read_flows_imgs(
            flow_patterns = ['mydata/flownets-pred-{0:0>7}.flo'],
            img_patterns = ['mydata/1.bmp', 'mydata/2.bmp'],
            n = 1
        )
        flow_labels = ['FlowNetS']
    elif dataset == 'mydata_small':
        all_flows, all_imgs = read_flows_imgs(
            flow_patterns = ['mydata_small/flownets-pred-{0:0>7}.flo'],
            img_patterns = ['mydata_small/1.bmp', 'mydata_small/2.bmp'],
            n = 1
        )
        flow_labels = ['FlowNetS']
    elif dataset == 'flownetdata':
        all_flows, all_imgs = read_flows_imgs(
            flow_patterns = ['data/{0:0>7}-gt.flo', 'data/flownets-pred-{0:0>7}.flo',
                             'data/flownet2-pred-{0:0>7}.flo'],
            img_patterns = ['data/{0:0>7}-img0.ppm', 'data/{0:0>7}-img1.ppm'],
            n = 8)
        flow_labels = ['Ground truth', 'FlowNetS', 'FlowNet2']
    elif dataset == 'flownetdata_small':
        all_flows, all_imgs = read_flows_imgs(
            flow_patterns = ['data_small/{0:0>7}-gt.flo', 'data_small/flownets-pred-{0:0>7}.flo'],
            img_patterns = ['data_small/{0:0>7}-img0.ppm', 'data_small/{0:0>7}-img1.ppm'],
            n = 8)
        flow_labels = ['Ground truth', 'FlowNetS']
    else:
        raise Exception
        
    if dataset == 'huawei' or dataset == 'cells':
        n = len(glob.glob1(flo_dir, "*.flo"))

        all_flows = read_flows([flo_dir + '/{0}.flo'], n, first = 1)
        all_imgs = read_img_laps(img_dir + '/{0}.' + img_ext, n, first = 1)
        flow_labels = ['FlowNet2']
    
    return all_flows, all_imgs, flow_labels