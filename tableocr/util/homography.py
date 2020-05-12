""" Homography utility """
import cv2
import numpy as np


def get_homography_matrix(src, dst):
    """ Calculate Homography matrix
    H, _ = cv2.findHomography(src, dst)
    """

    matrix_src = []
    for i in range(0, 4):
        point = src[i]
        point2 = dst[i]
        matrix = [
            point[0],
            point[1],
            1,
            0,
            0,
            0,
            -point[0] * point2[0],
            -point[1] * point2[0],
        ]
        matrix_src.append(matrix)
        matrix = [
            0,
            0,
            0,
            point[0],
            point[1],
            1,
            -point[0] * point2[1],
            -point[1] * point2[1],
        ]
        matrix_src.append(matrix)

    matrix_src = np.array(matrix_src)
    matrix_dst = np.array(dst).flatten()
    H = (np.linalg.inv((matrix_src.transpose()).dot(matrix_src))).dot(
        ((matrix_src.transpose()).dot(matrix_dst))
    )
    H = np.append(H, [1])
    H = H.reshape((3, 3))

    return H


def warp_perspective(image, H):
    """
    Warp the image

    image = np.array(image)
    warped_image = image.dot(np.array(H))
    warped_image /= warped_image[2]
    """
    warped_image = cv2.warpPerspective(image, H, (image.shape[1], image.shape[0]))

    return warped_image


def homography(image, src, dst):
    """ Homography module """
    H = get_homography_matrix(np.array(src), np.array(dst),)
    warpped_image = warp_perspective(image, H)

    return warpped_image
