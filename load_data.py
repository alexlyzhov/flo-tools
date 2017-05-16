import glob

from flow_io import read_flo, read_img

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

def load(dataset, name, get_dirs = False):
    # gaps larger than 1 not supported yet
    if dataset == 'huawei':
        flo_dir = img_dir = 'data/huawei/' + name
        
        if '1027' in name:
            img_ext = 'png'
        else:
            img_ext = 'jpg'
        is_gray = False
    elif dataset == 'cells':
        (imgs_name, flows_name) = name.split('/')
        flo_dir = 'data/cells/' + name
        img_dir = 'data/cells/' + imgs_name
        
        img_ext = 'png'
        is_gray = True
        
        if 'gap1' not in name:
            raise Exception
    elif dataset == 'ref':
        all_flows, img_pairs = read_flows_imgs(
            flow_patterns = ['data/ref/{0:0>7}-gt.flo', 'data/ref/flownets-pred-{0:0>7}.flo',
                             'data/ref/flownet2-pred-{0:0>7}.flo'],
            img_patterns = ['data/ref/{0:0>7}-img0.ppm', 'data/ref/{0:0>7}-img1.ppm'],
            n = 8)
        flow_labels = ['Ground truth', 'FlowNetS', 'FlowNet2']
        is_gray = False
    else:
        raise Exception
        
    if dataset == 'huawei' or dataset == 'cells':
        n = len(glob.glob1(img_dir, "*." + img_ext)) - 1

        img_pairs = read_img_laps(img_dir + '/{0}.' + img_ext, n, first = 1)
        
        all_flows = [[] for i in xrange(n)]
        flow_labels = []
                
        if len(glob.glob1(flo_dir, "farneback_*.flo")) > 0:
            new_flows = read_flows([flo_dir + '/farneback_{0}.flo'], n, first = 1)
            for i, entry in enumerate(all_flows):
                entry.extend(new_flows[i])
            flow_labels.append('Farneback')
        
        if len(glob.glob1(flo_dir, "flownet2_*.flo")) > 0:
            new_flows = read_flows([flo_dir + '/flownet2_{0}.flo'], n, first = 1)
            for i, entry in enumerate(all_flows):
                entry.extend(new_flows[i])
            flow_labels.append('FlowNet2')
    
    if not get_dirs:
        return img_pairs, all_flows, flow_labels, is_gray
    else:
        return img_pairs, all_flows, flow_labels, is_gray, img_dir, flo_dir
    
main_data_refs = [['huawei', '1015'], ['huawei', '1027'], ['huawei', 'ResolutionChart1'],
                  ['huawei', 'SiemensStar1'], ['cells', '15/gap1'], ['cells', '36/gap1'], ['cells', '60/gap1']]