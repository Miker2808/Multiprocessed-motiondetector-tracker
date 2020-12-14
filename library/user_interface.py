import cv2
import numpy as np

Yellow = (220, 255, 0)
Blue = (255, 0, 0)
Green = (0, 255, 0)
Red = (0, 0, 255)
Pink = (255, 0, 255)
Cyan = (220, 255, 0)
font = cv2.FONT_HERSHEY_SIMPLEX


def draw_point_roi(image, inputList, sizeList):
    """
    takes inputList and sizeList and draws points on the ROIs and their sizes
    :param image: frame
    :param inputList: list of ROIs
    :param sizeList: list of sizes of the ROIs of the inputList
    :return:
    """
    if len(inputList) > 0:  # run only if there are rectangles to place
        largestObject = max(sizeList)
        for index in range(0, len(inputList)):  #iterate through inputList and sizeList and print their correspondent values, sizeList and inputList share the same index per point
            if sizeList[index] == largestObject:
                centerPoint = (int(inputList[index][0] + inputList[index][2] / 2),
                               int(inputList[index][1] + inputList[index][3] / 2))  # define the centerpoint of a certain rectangle
                pointSize = sizeList[index]  # define the size of the given rectangle (value is 2 times the sectors in the area)
                image = cv2.putText(image,
                                    "(Y:{}, X:{}, Size:{})".format(centerPoint[0], centerPoint[1], pointSize),
                                    (centerPoint[0] - 50, centerPoint[1] - 20),
                                    font,
                                    0.4,
                                    (0, 255, 0),
                                    1,
                                    cv2.LINE_AA)  # put it all in the text
                image = cv2.putText(image, "[TARGET]", (centerPoint[0] - 25, centerPoint[1] - 40), font, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
                image = cv2.circle(image, centerPoint, 4, (0, 255, 0), 2)  # draw a circle for the beauty of it
            else:
                centerPoint = (int(inputList[index][0] + inputList[index][2] / 2),
                               int(inputList[index][1] + inputList[index][3] / 2))  # define the centerpoint of a certain rectangle
                pointSize = sizeList[index]  # define the size of the given rectangle (value is 2 times the sectors in the area)
                image = cv2.putText(image,
                                    "(Y:{}, X:{}, Size:{})".format(centerPoint[0], centerPoint[1], pointSize),
                                    (centerPoint[0] - 50, centerPoint[1] - 20),
                                    font,
                                    0.4,
                                    (0, 0, 255),
                                    1,
                                    cv2.LINE_AA)  # put it all in the text
                image = cv2.circle(image, centerPoint, 2, (0, 0, 255), -1)  # draw a circle for the beauty of it
        return image  # return the image with the text back to the main loop

    else:
        return image  # if the list is empty, return the image as it is


def draw_rect_roi(image, inputList, sizeList, sampleresolution):
    """
    Draws rectangles around ROIs
    :param image: the frame
    :param inputList: the list of detected ROIs
    :param sizeList: a second list of sizes which represent of size of each roi in the inputList
    :param sampleresolution: sample resolution (average n pixels for motion detection)
    :return: frame
    """
    if len(inputList) > 0:  # run only if there are rectangles to place
        largestObject = max(sizeList)
        for index in range(0, len(inputList)):  #iterate through inputList and sizeList and print their correspondent values, sizeList and inputList share the same index per point
            if sizeList[index] == largestObject:
                pointSize = sizeList[index]  # define the size of the given rectangle (value is 2 times the sectors in the area)
                coefficient = np.sqrt(pointSize)*(sampleresolution/2)
                centerPoint = (inputList[index][0] + inputList[index][2] / 2,
                               inputList[index][1] + inputList[index][3] / 2)  # define the centerpoint of a certain rectangle
                Point1 = (int(centerPoint[0] - coefficient), int(centerPoint[1] - coefficient))
                Point2 = (int(centerPoint[0] + coefficient), int(centerPoint[1] + coefficient))

                image = cv2.putText(image,
                                    "(Y:{}, X:{}, Size:{})".format(Point1[0], Point1[1], pointSize),
                                    (Point1[0] - 50, Point1[1] - 20),
                                    font,
                                    0.4,
                                    (0, 255, 0),
                                    1,
                                    cv2.LINE_AA)  # put it all in the text
                image = cv2.putText(image, "[TARGET]", (Point1[0] - 25, Point1[1] - 40), font, 0.6, Green, 1, cv2.LINE_AA)
                image = cv2.rectangle(image, Point1, Point2, Green, 1)  # draw a rectangle for the beauty of it

            else:
                pointSize = sizeList[index]  # define the size of the given rectangle (value is 2 times the sectors in the area)
                coefficient = np.sqrt(pointSize)*(sampleresolution/2)
                centerPoint = (inputList[index][0] + inputList[index][2] / 2,
                               inputList[index][1] + inputList[index][3] / 2)  # define the centerpoint of a certain rectangle
                Point1 = (int(centerPoint[0] - coefficient), int(centerPoint[1] - coefficient))
                Point2 = (int(centerPoint[0] + coefficient), int(centerPoint[1] + coefficient))

                image = cv2.putText(image,
                                    "(Y:{}, X:{}, Size:{})".format(Point1[0], Point1[1], pointSize),
                                    (Point1[0] - 50, Point1[1] - 20),
                                    font,
                                    0.4,
                                    Yellow,
                                    1,
                                    cv2.LINE_AA)  # put it all in the text
                image = cv2.rectangle(image, Point1, Point2, Yellow, 1)  # draw a rectangle for the beauty of it

        return image  # return the image with the text back to the main loop

    else:
        return image  # if the list is empty, return the image as it is

# Draws region of interest from list of rectangles
def draw_roi(image, inputList):
    """
    Basic code to draw blocks of inputlist, used to find out sectors where motion was detected
    :param image: the frame (list/tuple)
    :param inputList: list of ROIs (list(y, x, leny, lenx)
    :return:
    """
    if len(inputList) > 0:
        for Block in inputList:
            point1 = (Block[0], Block[1])
            point2 = (Block[0] + Block[2], Block[1] + Block[3])
            image = cv2.rectangle(image, point1, point2, Pink, 1)
        return image

    else:
        return image


def detection_gui(frame,sample_res, obj_num, obj_size, roi_list, time_pass, frame_size, bg_detect_sensitivity = 2):
    """
    Handles the whole HUD (gui) of the detection mechanism
    :param frame: the frame (list/tuple)
    :param sample_res: sample resolution (int)
    :param obj_num:  number of objects detected (int)
    :param obj_size: size of the target object (int)
    :param roi_list: list of ROIs detected (list/tuple)
    :param time_pass: time passed for a pass (float/int)
    :param frame_size: size of the frame (tuple(int, int))
    :param bg_detect_sensitivity: background sensitivity multiplier (int/float) default = 3 (smaller == more sensitive)
    :return: the output frame
    """
    frame = draw_rect_roi(frame, roi_list, obj_size, sample_res)
    rows, cols = frame_size

    if obj_num > bg_detect_sensitivity * sample_res:  # return background estimation if too many possible blocks are counted
        cv2.putText(frame, "[BACKGROUND MOVEMENT]", (int(rows * 0.025), int(cols / 2)), font, 1.5, Red, 2,
                    cv2.LINE_AA)
        cv2.putText(frame, "Background movement detected", (int(rows * 0.025), int(cols * 0.08)), font, 0.5, Red,
                    1, cv2.LINE_AA)

    # print all this very interesting shit
    cv2.putText(frame, "RunTime: {}s".format(time_pass), (int(rows * 0.025), int(cols * 0.025)), font, 0.5, Green,
                1, cv2.LINE_AA)
    cv2.putText(frame, "Objects Detected: {}".format(obj_num), (int(rows * 0.025), int(cols * 0.05)),
                font, 0.5, Green, 1, cv2.LINE_AA)
    cv2.putText(frame, "Resolution: {} Blocks".format(sample_res), (int(rows * 0.6), int(cols * 0.05)),
                font, 0.5, Green, 1, cv2.LINE_AA)
    cv2.putText(frame, "Image Resolution: {} x {}".format(rows, cols), (int(rows * 0.6), int(cols * 0.025)),
                font, 0.5, Green, 1, cv2.LINE_AA)
    return frame

def tracker_gui(frame, roi_first_point, roi_second_point):
    """
    Handles the basic HUD of the tracker
    :param frame:  the frame (list/tuple)
    :param roi_first_point:  first point of the target ROI (tuple(int, int))
    :param roi_second_point: second point of the target ROI (tuple(int, int)
    :return: frame
    """
    cv2.putText(frame, "Tracking Enabled", (50, 40), font, 0.5, Cyan, 2)
    cv2.rectangle(frame, roi_first_point, roi_second_point, Cyan, 2)
    return frame

