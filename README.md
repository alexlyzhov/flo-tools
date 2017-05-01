# flo-tools

## Optical flow from webcam stream

Video.ipynb takes webcam stream and computes optical flow between pairs of frames. Works with FlowNetPytorch pretrained on Flying Chairs.

How to run Video.ipynb?

- Clone [FlowNetPytorch @ f054bae](https://github.com/ClementPinard/FlowNetPytorch/tree/f054bae366b13bd1f8b7bce2b66b96d37ee2d5e1)
- Copy Video.ipynb and flow_algo.py to the root directory of this repository
- Edit argparse args in Video.ipynb, particularly the path to a [pretrained model](https://github.com/ClementPinard/FlowNetPytorch#pretrained-models)
- OpenCV isn't available for python 3, so you have to choose Python 2 Jupyter kernel
- Enjoy

## Optical flow visualization

Visualization.ipynb features

- Vectors superimposed onto image 1
- Middlebury colorcoding
- Image blending
- L1 difference visualization between predicted flow and ground truth
- Computing end-point error and angular error

## Warping.ipynb

Take one image and warp it to another with optical flow. Options include

- Initialize with black background or with image we have
- Forward or backward direction
- Iteration over beginnings or ends of flow vectors
