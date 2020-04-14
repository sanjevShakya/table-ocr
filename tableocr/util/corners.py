""" Utility for detecting corners """
import cv2
import math
import numpy as np


def get_contours(img):
    """
    Get contours in image
    """
    # these constants are carefully picked
    MORPH = 9
    CANNY = 84
    HOUGH = 25
    orig = img
    img = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    ksize = (3, 3)
    cv2.GaussianBlur(img, ksize, 0, img)
    # this is to recognize white on white
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (MORPH, MORPH))
    dilated = cv2.dilate(img, kernel)
    edges = cv2.Canny(dilated, 0, CANNY, apertureSize=3)
    completeArc = math.pi / 180
    lines = cv2.HoughLinesP(edges, 1, completeArc, HOUGH)
    try:
        for line in lines[0]:
            cv2.line(edges, (line[0], line[1]), (line[2], line[3]), (255, 0, 0), 2, 8)

        # finding contours
        contours, _ = cv2.findContours(
            edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        contours = filter(lambda cont: cv2.arcLength(cont, False) > 100, contours)
        contours = filter(lambda cont: cv2.contourArea(cont) > 10000, contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    except:
        return False
    return contours


def get_corners_from_contours(contours, C=0.1):
    """
    Get 4 corners from provided contours
    C recursively modified for exact 4 corners
    """
    contours = np.array(contours)
    perimeter = cv2.arcLength(contours, True)
    perimeter = 1000
    epsilon = C * perimeter
    poly = cv2.approxPolyDP(contours, epsilon, True)
    hull = cv2.convexHull(poly)
    if len(hull) == 4:
        return hull
    elif len(hull) > 4:
        return get_corners_from_contours(contours, C + 0.01)
    else:
        return get_corners_from_contours(contours, C - 0.01)


def get_corners_dst(corners):
    """
    Destination corners; (0,0) +: Max W and H
    """
    w1 = np.sqrt(
        (corners[0][0] - corners[1][0]) ** 2 + (corners[0][1] - corners[1][1]) ** 2
    )
    w2 = np.sqrt(
        (corners[2][0] - corners[3][0]) ** 2 + (corners[2][1] - corners[3][1]) ** 2
    )
    w = max(int(w1), int(w2))

    h1 = np.sqrt(
        (corners[0][0] - corners[2][0]) ** 2 + (corners[0][1] - corners[2][1]) ** 2
    )
    h2 = np.sqrt(
        (corners[1][0] - corners[3][0]) ** 2 + (corners[1][1] - corners[3][1]) ** 2
    )
    h = max(int(h1), int(h2))

    dst = np.float32([(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)])

    return dst, w, h


def get_corners(image):
    """
    Corners of image
    """
    contours = get_contours(image)
    if contours is not False:
        corners = get_corners_from_contours(contours)
        corners = sorted(np.concatenate(corners).tolist())
        corners = [corners[i] for i in [3, 2, 1, 0]]
    else:
        corners = [
            [0, 0],
            [image.shape[1] - 1, 0],
            [0, image.shape[0] - 1],
            [image.shape[1] - 1, image.shape[0] - 1],
        ]
    return corners
