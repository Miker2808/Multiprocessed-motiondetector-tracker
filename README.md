# Multiprocessed motion detector & tracker

#### Multiprocessed Python OpenCV motion detector with an optional tracker.

# requirements
```bash
Opencv >= 4.4.0.0 (recommended with 'pip3 install opencv-contrib-python')
numpy >= 1.19.0
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
The algorithm runs on multiple layers, at top, it is multiprocessed using 3 processes
first process, is the CameraProcess fuction, handling the video buffer and sending the frames
to the second process, called the AlgorithmProcess, it handles the motion detector and the tracker.

The motion detector uses the background subtraction method for detection, therefore its weakness is moving cameras.
the motion detector scans sectors or 'blocks' if from the subtraction it sensed motion, it appends it.
after scanning the whole frame differance, it connects the close blocks into one block, with the size proportional
to the connected blocks. This process generates a list of ROIs, then, the algorithm sends the largest ROI to the tracker
and it starts to track the largest ROI it got.

To avoid noise, it ignores too large or too small blocks - dependent on user configured parameters.
the tracker follows the target, if the tracker is 'lost' and gets stuck on the same position, it stops and returns
automatically to the motion detector - amount of wait in seconds is configured by user.

# Samples
### Motion Detector -- the motion detector marks the largest motion object with green ROI and [TARGET] mark
![Motion Detector](https://i.imgur.com/gKy9Hn9.gif)

### Tracker -- the motion detector picked a target and initiated the tarcker right away.
![Motion Tracker](https://media.giphy.com/media/ET5BM50AUa4J2kHaKx/giphy.gif)

