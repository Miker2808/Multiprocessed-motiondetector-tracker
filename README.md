# Multiprocessed motion detector & tracker

#### Multiprocessed Python OpenCV motion detector with an optional tracker.

# requirements
```bash
Opencv >= 4.4.0.0 (recommended with 'pip3 install opencv-contrib-python')
numpy >= 1.18.0
python >= 3.6
```
# Installation & Use
Clone the repository, checkout to desired branch (with tracker or without).
open the 'multiprocessed-motiondetector-tracker.py' 
```python
# change the variable:
examplevideo = '' # to your video path, or otherwise an IP to your stream
```
simply run the script.

# How does it work?
The algorithm runs on multiple layers, on top, it is multiprocessed using 3 processes.
The first process, called CameraProcess, is a function responsible for handling the video buffer and sending the frames
to the second process, called the AlgorithmProcess, it handles the motion detector and the tracker.

The motion detector uses the background subtraction algorithm for detection, therefore it's weakness is moving cameras.
The motion detector scans sectors also know as 'blocks' from the subtracted images, like a "delta" image. if the scan senses motion,
which is represented in the subtracted image output as white colored area, it appends it.
Once the scan is complete, the algorithm connects the "blocks" using standard opencv method, which outputs a block with size proportional 
to the connected blocks, in averaged out area. The process continues until all blocks are connected or removed if they are too small
(This can be changed by tweaking the parameters).
The output of this process will be a list of ROIs (Region On Interests) as a (X,Y,W,H) tuples list.
The largest ROI is sent to the tracker to initiate tracking on the object in the ROI.
Once the tracker is initiated successfully it will either follow the moving object, or freeze on the same place.
To avert losing the target and locking on the background, the tracker is stopped after N seconds of motionlessness.
The number of seconds to wait (N) can be tweaked by user

# Samples
### Motion Detector -- the motion detector marks the largest motion object with green ROI and [TARGET] mark
![Motion Detector](https://i.imgur.com/CsQZ914.gif)

### Tracker -- the motion detector picked a target and initiated the tarcker right away.
![Motion Tracker](https://media.giphy.com/media/ET5BM50AUa4J2kHaKx/giphy.gif)

