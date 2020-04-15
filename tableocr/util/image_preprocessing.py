""" Preprocessing utilities """
import cv2
from util.homography import homography
from util.corners import get_corners, get_corners_dst
import numpy as np


def to_gray(image):
    """
    Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    """

    for row in range(0, image.shape[0]):
        for column in range(0, image.shape[1]):
            pixel = np.array(image[row][column])
            avg = (int(pixel[0]) + int(pixel[1]) + int(pixel[2])) / 3
            image[row][column] = [avg, avg, avg]
    gray = image
    return gray


def binarize(image):
    """ 
    Image binarization
    blockSize = 7
    C = 3
    row = image.shape[0]
    column = image.shape[1]
    for i in range(0, int((row - 1) / blockSize)):
        for j in range(0, int((column - 1) / blockSize)):
            mean = np.mean(
                image[
                    i * blockSize : (i + 1) * blockSize,
                    j * blockSize : (j + 1) * blockSize,
                ]
            )
            for y in range(i * blockSize, (i + 1) * blockSize):
                for x in range(j * blockSize, (j + 1) * blockSize):
                    if np.mean(image[y, x]) < mean - C:
                        image[y, x] = [0, 0, 0]
                    else:
                        image[y, x] = [255, 255, 255]
    binarized = image
    """
    threshold = cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 0
    )  # src, maxValue, adaptiveMethod, thresholdType, blockSize, C
    binarized = threshold
    return binarized


def bgr_binarize(image):
    """ BGR image binarization """
    gray = to_gray(image)
    return binarize(gray)


def crop(image, x, y, w, h):
    """ Crop image to given position and size """
    image = image[y : y + h, x : x + w]
    return image


def flip_image(image, flag=0):
    return cv2.flip(image, flag)


def rotate(image, angle=-90, center=False, scale=1):
    if not center:
        center = (image.shape[1] / 2 - 1, image.shape[0] / 2 - 1)
    mtx = cv2.getRotationMatrix2D(center, angle, scale)
    image = cv2.warpAffine(image, mtx, (image.shape[1], image.shape[0]))
    return image


def preprocess(image, **kwargs):
    """
    Pre-processing
    kwargs: src<[[]]>, rotate<-360 360>
    """
    src = kwargs.get("src", get_corners(image))
    dst, width, height = get_corners_dst(src)
    homographic_image = homography(image, src, dst)
    image = crop(homographic_image, 0, 0, width, height)
    if kwargs.get("rotate", {}):
        image = rotate(image, kwargs.get("rotate", {}))

    return image


if __name__ == "__main__":
    """
    Success:
    a4-print.jpg
    a4-120gsm-letterhead-printing.webp
    page1.jpeg
    Fac-simile_of_an_Old_Printed_Page.jpg
    Failed:
    88a98d44b63cbfa57d602bc066cfd54e.png
    simple-invoice-template-vip-1.jpg
    """
    # image = cv2.imread("src/static/images/Fac-simile_of_an_Old_Printed_Page.jpg")
    # image = cv2.imread("src/static/images/page1.jpeg")
    # image = cv2.imread("src/static/images/simple-invoice-template-vip-1.jpg")
    # image = cv2.imread("src/static/images/88a98d44b63cbfa57d602bc066cfd54e.png")
    # image = cv2.imread("src/static/images/form3a.jpeg")
    image = cv2.imread("src/static/images/a4-print.jpg")
    cv2.imshow("Image", image)

    src = get_corners(image)
    # src = [[0,0], [image.shape[1]-1,0], [0,image.shape[0]-1], [image.shape[1]-1,image.shape[0]-1]] #for failed case: Full screen
    # src = [[280,90], [800,90], [200,625], [850, 630]] #for failed case: invoice
    dst, width, height = get_corners_dst(src)

    homographic_image = homography(image, src, dst)
    cv2.imshow("Warpped", homographic_image)
    cropped_image = crop(homographic_image, 0, 0, width, height)
    cv2.imshow("Cropped", cropped_image)
    rotated_image = rotate(cropped_image, -90)
    cv2.imshow("Rotated", rotated_image)

    binarized = bgr_binarize(image)
    cv2.imshow("Binarized", binarized)
    cv2.imshow("Fn Preprocess", preprocess(cv2.imread("src/static/images/page1.jpeg")))
    cv2.waitKey()
