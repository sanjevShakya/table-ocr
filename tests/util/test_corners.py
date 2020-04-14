""" Test for corners.py """

import cv2
import pytest
import numpy as np

from tableocr.util.corners import (
    get_corners,
    get_contours,
    get_corners_dst,
    get_corners_from_contours,
)


def test_get_corners_no_contours():
    """
    Test for get_corners function when there is no contours
    Should return corner of image itself
    """
    blankImg = np.zeros(shape=[3, 3, 3], dtype=np.uint8)
    result = get_corners(blankImg)

    assert result == [[0, 0], [2, 0], [0, 2], [2, 2]]


def test_get_corners():
    """
    Test for get_corners function
    Should return corners of drawn rectangle
    """
    img = np.zeros(shape=[200, 200, 3], dtype=np.uint8)
    test_start_point = (50, 50)
    test_end_point = (150, 150)
    test_color = (255, 120, 34)
    cv2.rectangle(img, test_start_point, test_end_point, test_color, 2)
    result = get_corners(img)
    max_thresh = 10

    assert abs(min(result)[0] - test_start_point[0]) <= max_thresh
    assert abs(min(result)[1] - test_start_point[1]) <= max_thresh
    assert abs(max(result)[0] - test_end_point[0]) <= max_thresh
    assert abs(max(result)[1] - test_end_point[1]) <= max_thresh


def test_get_corner_dst():
    """
    Test for get_corner-dest
    """
    test_corners = [[0, 0], [0, 30], [30, 0], [30, 30]]
    destination, width, height = get_corners_dst(test_corners)

    assert width == 30 and height == 30
    assert (
        np.array(destination) == np.array([[0, 0], [29, 0], [0, 29], [29, 29]])
    ).all()
