""" Utility for working with table. """

import os
import cv2
import sys
import numpy as np
from pytesseract import image_to_string

sys.path.insert(0, os.path.abspath(".."))
from util.image_preprocessing import binarize


def get_cells(im, column):
    """
    xd
    """
    im = 255 - binarize(im)

    kernel_length = np.array(im).shape[1] // 40

    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    eroded_im = cv2.erode(im, vertical_kernel, iterations=3)
    vertical_lines_img = cv2.dilate(eroded_im, vertical_kernel, iterations=3)
    # cv2.imshow("Vertical lines Img", vertical_lines_img)

    horizontal_kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    eroded_im = cv2.erode(im, horizontal_kernal, iterations=3)
    horinzontal_img = cv2.dilate(eroded_im, horizontal_kernal, iterations=3)
    # cv2.imshow("Horizontal lines Img", horinzontal_img)

    table_image = cv2.add(vertical_lines_img, horinzontal_img)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    table_image = cv2.erode(~table_image, kernel, iterations=2)
    table_image = cv2.cvtColor(table_image, cv2.COLOR_BGR2GRAY)
    _, table_image = cv2.threshold(
        table_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
    )
    # cv2.imshow("Table", table_image)

    contours, _ = cv2.findContours(table_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    boundingBoxes = [cv2.boundingRect(c) for c in contours]
    contours, _ = zip(
        *sorted(zip(contours, boundingBoxes), key=lambda k: k[1][1], reverse=False)
    )

    i = 0
    data = []
    row = []
    try:
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 80 and h > 20:
                i += 1
                if i % column == 0:
                    data.append(row[::-1])
                    row = []
                cell = im[y : y + h, x : x + w]
                row.append(image_to_string(cell))

    except:
        print("Exception occurred!")
        pass

    return data


if __name__ == "__main__":
    im = cv2.imread("/home/luser/Desktop/demo-table.png")
    data = get_cells(im, 3)
    print(data)
