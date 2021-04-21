"""
Contains motiondetector and tracker in a multiprocessed wrap.
The script is seperated into 2 main functions, each running on its own process.

First on is the CameraProcess - handling the reading of frames and emptying the buffer.
It sends frames to the algorithm process for further processing, otherwise sends a shutdown request to the algorithm
process which from ther is sent to the main process for shutdown.

The second process is the Algorithm Process - handling the UI, tracker, motiondetector and showing frames to the user.
connected to camera process to receive frames and to send 'im busy' (So the camera process will not try sending it frames)
additionally, it is connected to the main process for shutdown requests.

The idea of work is background subtraction, 2 frames are subtracted with pythagorean distance.
The output is a difference frame, which show where areas are different from before.
then after threshholding and gaussian bluring the WhiteProbe function probes the areas for differences.
once probing is done, the algorithm connects all close sectors into large ROI (Region Of Interest) and build an area
around the moving target. small object motion and too large objects can be discarded using the given parameters found
at the first lines of code. its possible to teak them for best performance.
When its done, the UI handler builds a user interface and marks the targets.

Optionally, a tracker will track the largest detected target at the moment using OpenCVs built in tracker.
if the tracker is stuck on the same position for too long (time can be configured) it discards the tracking and returns
automatically back to detection mode.

Probe, Section, Sample, Block - mean the same thing: Image Block

image co-ordinates system:
[y][x]
[0][0] - - - - x - - - >
|
|
Y
|
|
v
.
"""

import numpy as np
import cv2
import timeit
import multiprocessing
import sys
import time

import library.user_interface as ui
import library.detector as detector
import library.utility as utility

examplevideo = "75m.mp4"

sampleresolution = 3  # Number of pixel to take into calculation per block
samplesensitivity = 25  # Average white value in block (greyscale of each pixel divided by number of pixels), (full white block will return value of 255)
minimum_treshhold = 10 # Threshholds the distance frame to specified-255 (any value under specified value is discarded (back to 0))
min_detect_size = 15 # minimum size of the ROI to not be discarded, too large will discards any motion, too small will include too sensitive motion.
max_tracking_stuck_time = 1 # if tracker is stuck wait up to 3 seconds before returning to motion detector
bg_detect_sensitivity = 5 # level of motion required to trigger background detection warning (lower means less sensitive)
#frame_resolution = (680, 480)
frame_resolution = (1280, 720)

PROCESS_READY = (1, 1) 
PROCESS_BUSY = (2, 2)
PROCESS_SHUTDOWN = (69, 420)


# MAIN FUNCTION ------------------------------------------------------------------------------
# capture video stream from camera source. 0 refers to first camera,
# or write video file location, file name only if the image/video is in the same directory as this file


def CameraProcess(pipe):
    cap = cv2.VideoCapture(examplevideo)
    while True:
        good_frame, frame = cap.read()
        if not good_frame:
            print("ERROR: NO FRAME")
            pipe.send(PROCESS_SHUTDOWN)
            break

        frame = cv2.resize(frame, frame_resolution, interpolation=cv2.INTER_AREA)
        msg = pipe.recv()
        if msg == PROCESS_READY:
            pipe.send(frame)
        if msg == PROCESS_BUSY:
            good, frame = cap.read()
    
    #record.release()
    cap.release()
    cv2.destroyAllWindows()


def AlgorithmProcess(pipe, mainPipe):
    
    while True:
        starttime = timeit.default_timer()
        # receiving the frames - breaking if CameraProcess commands shutdown.
        pipe.send(PROCESS_READY)
        frame1 = pipe.recv()

        if frame1 == PROCESS_SHUTDOWN:
            mainPipe.send(PROCESS_SHUTDOWN)
            break

        pipe.send(PROCESS_READY)
        frame2 = pipe.recv()

        if frame2 == PROCESS_SHUTDOWN:
            mainPipe.send(PROCESS_SHUTDOWN)
            break

        pipe.send(PROCESS_BUSY)

        rows, cols, _ = np.shape(frame2)


        # running series of algorithms
        TargetROI, ROI_List, object_size, dist_frame = detector.detection_handler(frame1, frame2, sampleresolution, samplesensitivity, minimum_treshhold, min_detect_size)

        # Anything below this line (in the function) is solely for visualization.
        NumObjectsDetected = len(ROI_List)

        # Draw Rectangles
        #FrameOut = DrawRectROI(FrameOut, ROI_List, ObjectSize)
        # FrameOut = DrawROI(FrameOut, threshROI)

        # performance timer
        timeend = timeit.default_timer()
        timepass = (int((timeend - starttime) * 1000)) / 1000

        frame_out = ui.detection_gui(frame2, sampleresolution, NumObjectsDetected, object_size, ROI_List, timepass, (rows, cols), bg_detect_sensitivity)

        cv2.imshow("Detector", frame_out)

        if cv2.waitKey(1) & 0xFF == 27:
            mainPipe.send(PROCESS_SHUTDOWN)
            print("Algorithm Processor: EXIT REQUEST")


if __name__ == "__main__":
    AlgorithmSide, CameraSide = multiprocessing.Pipe()
    MainSide, AlgorithmToMainSide = multiprocessing.Pipe()
    p1 = multiprocessing.Process(target=CameraProcess, args=(AlgorithmSide,))
    p2 = multiprocessing.Process(target=AlgorithmProcess, args=(CameraSide, AlgorithmToMainSide))
    p1.start()
    p2.start()
    while True:
        if MainSide.recv() == PROCESS_SHUTDOWN:
            print("Main Process: EXIT REQUEST")
            break
    p1.terminate()
    print("Camera Process Terminated")
    p2.terminate()
    print("Algorithm Process Terminated")
    print("Have a good day :)")
    sys.exit(0)





