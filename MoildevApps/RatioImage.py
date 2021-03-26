from PyQt5 import QtCore, QtGui
import cv2


class Set_RatioImage(object):
    """To solve the ratio image problem where using the various of camera type.h

    :param parent= MainWindow of User Interface
    :type parent = QtWidget object
    """
    def __init__(self, MainWindow):
        """Constructor Method
        """
        self.parent = MainWindow

    def resize_original_image(self, image):
        """resize image for showing on Label original image user interface

        Args:
            image = original image
            image = array

        return:
            Resized image
        """
        h, w = image.shape[:2]
        r = 400 / float(w)
        hi = round(h * r)
        self.parent.ui.windowOri.setMinimumSize(QtCore.QSize(400, hi))
        self.parent.ui.labelImagerecenter.setMinimumSize(QtCore.QSize(400, hi))
        resized_image = cv2.resize(image, (400, hi), interpolation=cv2.INTER_AREA)
        return resized_image

    def resize_result_image(self, image, width_image):
        """Resize result image and the label result image based on width given

        Args:
            image = array
            width_image = integer

        return:
            Resized image
        """
        h, w = image.shape[:2]
        r = width_image / float(w)
        hi2 = round(h * r)

        self.parent.ui.windowResult.setGeometry(QtCore.QRect(10, 0, width_image, hi2))
        self.parent.ui.PlussIcon.setGeometry(QtCore.QRect(10, 10, width_image, hi2))
        if self.parent.ui.btn_Panorama.isChecked():
            blue = QtGui.QPixmap(width_image, hi2)
            blue.fill(QtCore.Qt.transparent)
            self.parent.ui.PlussIcon.setPixmap(blue)
        else:
            blue = QtGui.QPixmap(width_image, hi2)
            blue.fill(QtCore.Qt.transparent)
            p = QtGui.QPainter(blue)
            pen = QtGui.QPen(QtGui.QBrush(QtGui.QColor(0, 255, 0)), 3)
            p.setPen(pen)
            p.drawLine(round((width_image / 2) - 10), round(hi2 / 2), round((width_image / 2) + 10), round(hi2 / 2))
            p.drawLine(round(width_image / 2), round((hi2 / 2) - 10), round(width_image / 2), round((hi2 / 2) + 10))
            p.end()
            self.parent.ui.PlussIcon.setPixmap(blue)
        resized_image = cv2.resize(image, (width_image, hi2), interpolation=cv2.INTER_AREA)
        return resized_image
