""" Test file for homography.py """

import cv2
import mock
import pytest

import numpy as np

from tableocr.util.homography import homography, warp_perspective, get_homography_matrix


def test_get_homography_matrx():
    """
    Test if the function gives exact homography matrix
    """
    test_src = [[0, 6], [3, 40], [32, 54], [40, 60]]
    test_dst = [[0, 0], [0, 30], [30, 0], [30, 30]]
    result = get_homography_matrix(test_src, test_dst)
    expected_result = cv2.findHomography(np.array(test_src), np.array(test_dst))[0]

    assert str(result) == str(expected_result)


@mock.patch("cv2.warpPerspective")
def test_warp_perspective(mock_warpPerspective):
    """
    Test warp perspective function
    """
    img = np.zeros(shape=[200, 200, 3], dtype=np.uint8)
    test_src = [[0, 6], [3, 40], [32, 54], [40, 60]]
    test_dst = [[0, 0], [0, 30], [30, 0], [30, 30]]
    H = get_homography_matrix(test_src, test_dst)
    mock_warpPerspective.return_value = np.zeros(shape=[50, 50, 3], dtype=np.uint8)
    res_img = warp_perspective(img, H)

    assert (res_img == np.zeros(shape=[50, 50, 3], dtype=np.uint8)).all()
    mock_warpPerspective.assert_called_once()


@mock.patch("cv2.warpPerspective")
def test_homography(mock_warpPerspective):
    """
    Test homography function
    """
    img = np.zeros(shape=[200, 200, 3], dtype=np.uint8)
    test_src = [[0, 6], [3, 40], [32, 54], [40, 60]]
    test_dst = [[0, 0], [0, 30], [30, 0], [30, 30]]
    mock_warpPerspective.return_value = np.zeros(shape=[50, 50, 3], dtype=np.uint8)
    res_img = homography(img, test_src, test_dst)

    assert (res_img == np.zeros(shape=[50, 50, 3], dtype=np.uint8)).all()
    mock_warpPerspective.assert_called_once()
