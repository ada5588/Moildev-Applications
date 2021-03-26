from PyQt5 import QtWidgets
import datetime
import os
import cv2


def select_file(title, dir_path, file_filter):
    """find the file path from the directory computer

    Args:
        title: the title window of open dialog
        file_filter: determine the specific file want to search
        dir_path: Navigate to specific directory

    return:
        file_path:

    """
    options = QtWidgets.QFileDialog.DontUseNativeDialog
    file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, title, dir_path,
                                                         file_filter,
                                                         options=options)
    return file_path


def Rotate(src, angle, center=None, scale=1.0):
    """Turn an image in a clockwise or counterclockwise direction.

    Args:
        src: original image
        angle: the value angle for turn the image
        center: determine the specific coordinate to rotate image
        scale: scale image

    Returns:
        dst image: rotated image

    """
    h, w = src.shape[:2]
    if center is None:
        center = (w / 2, h / 2)
    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(src, M, (w, h))
    return rotated


def read_image(image_path):
    """Reading the image from given file path

    Args:
        image_path : image to be read from the image_path

    return:
        img:
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("`{}` not cannot be loaded".format(image_path))
    return image


def saveImage(filename, image):
    """Saving images and give a name to store in local directory

    Args:
        filename : give the image a filename
        image : the captured image

    return:
        None
    """
    save_time = datetime.datetime.now().strftime("%H_%M_%S")
    name = "../result/Images/" + filename + "_" + str(save_time) + ".png"
    os.makedirs(os.path.dirname(name), exist_ok=True)
    cv2.imwrite(name, image)
    QtWidgets.QMessageBox.information(None, "Information", "Image saved !!")


def drawPoint(image, heightImage, coordinatePoint):
    """Drawing the dot on the image from the coordinate given

    Args:
        image : Image
        heightImage : to determine the point size in the image
        coordinatePoint : determine the location of the point in the image

    return:
        image:
    """
    if heightImage >= 1000:
        cv2.circle(image, coordinatePoint, 10, (0, 255, 0), 20, -1)
    else:
        cv2.circle(image, coordinatePoint, 6, (0, 255, 0), 12, -1)
    return image
