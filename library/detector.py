import cv2
import numpy as np


# takes list of rectangles and returns the largest target
def largest_target(inputList, sizeList):
    if len(inputList) > 0:
        largestObject = max(sizeList)
        #print(largestObject)
        if largestObject[0] < 50:
            for index in range(0, len(inputList)):
                if sizeList[index] == largestObject:
                    centerPoint = [int(inputList[index][0] + inputList[index][2] / 2),
                                   int(inputList[index][1] + inputList[index][3] / 2)]
                    return centerPoint
    else:
        centerPoint = [0, 0]
        return centerPoint




def largest_ROI(inputList, sizeList, sample_res = 6, min_size = 10):
    """
    Takes inputList and sizeList and returns ROI of the largest target,
    discards if ROI is too large (over 30% of the screen), discarding is required to avoid tracking noise.
    :param inputList: list of ROIs, list contaiing a list with 4 items
    :param sizeList: list of sizes of the ROIs (indexes meet the inputlist)
    :param min_size: minimum size of the ROI to not be discarded, too large will discards any motion,
    too small will include too sensitive motion.
    :return: the largest target as a ROI [x,y,sizex,sizey,] or None
    Note: this function is following the requirements of the cv2.groupRectangles standards.
    check the opencv documentation for more information.
    """

    if len(inputList) > 0:
        largestObject = max(sizeList)
        #print(largestObject)
        if min_size < largestObject < 20:
            for index in range(0, len(inputList)):
                if sizeList[index] == largestObject:
                    pointSize = sizeList[index]  # define the size of the given rectangle (value is 2 times the sectors in the area)
                    coefficient = int(np.sqrt(pointSize) * (sample_res / 2)*3)
                    centerPoint = (inputList[index][0] + inputList[index][2] / 2,
                                   inputList[index][1] + inputList[index][3] / 2)  # define the centerpoint of a certain rectangle
                    ROI = (int(centerPoint[0] - coefficient/2), int(centerPoint[1] - coefficient/2), coefficient, coefficient)
                    return ROI
    return None  # return None if no largest target was found, allows the algorithm to know to just skip it instead of causing errors


def dist_map(frame1, frame2):
    """
    outputs pythagorean distance between two frames
    :param frame1:
    :param frame2:
    :return: distance frame
    """
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:, :, 0]**2 + diff32[:, :, 1]**2 + diff32[:, :, 2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist



# splits the image by given resolution, and scans for sectors with average intensity over given sensitivity,
# returns list of rectangles (top left x, top left y, length, width)"""
def white_probe(image, sample_res = 24, sensitivity = 20):
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # enable if you get color error
    ySize, xSize = np.shape(image)  # store size of image in [y,x] order
    splity = int(ySize / sample_res)
    splitx = int(xSize / sample_res)
    sampleAvg = cv2.resize(image, (splitx, splity), interpolation = cv2.INTER_AREA)
    BlockOfInterest = []

    for y in range(0, splity):
        for x in range(0, splitx):
            if sampleAvg[y, x] > sensitivity:
                yPointTop = int(y * sample_res)
                xPointTop = int(x * sample_res)
                BlockOfInterest.append([xPointTop, yPointTop, sample_res, sample_res])
                BlockOfInterest.append([xPointTop, yPointTop, sample_res, sample_res])
    return BlockOfInterest


def detection_handler(frame1, frame2, sample_res, sample_sens, minimum_threshold, min_detect_size):
    dist_frame = dist_map(frame1, frame2)
    blur_frame = cv2.GaussianBlur(dist_frame, (9, 9), 0)
    _, thresh_frame = cv2.threshold(blur_frame, minimum_threshold, 255, 0)
    thresh_roi = white_probe(thresh_frame, sample_res, sample_sens)
    roi_list, object_size = cv2.groupRectangles(thresh_roi, 10, 3)
    target_roi = largest_ROI(roi_list, object_size, min_detect_size)
    return target_roi, roi_list, object_size, dist_frame
