from MoildevApps.Ui_Utils import drawPoint
from MoildevApps.View_ShowResult import ShowImageResult
import cv2


class Panorama(object):
    """The class to process image on panorama view
    :param parent= Main window class
    :type parent = object
    """
    def __init__(self, MainWindow):
        """Constructed method.
        """
        self.parent = MainWindow
        self.show = ShowImageResult(self.parent)
        self.max = float(110)
        self.min = float(10)
        self.parent.ui.lineEdit_Max.setText(str(self.max))
        self.parent.ui.lineEdit_Min.setText(str(self.min))
        self.connectToButton()

    def connectToButton(self):
        """This function for connect to button in user interface
        """
        self.parent.ui.btn_Panorama.clicked.connect(self.panorama_view)
        self.parent.ui.btn_setPanorama.clicked.connect(self.set_pano)
        self.parent.ui.spinBox_coorX.valueChanged.connect(self.positionCoorX)
        self.parent.ui.spinBox_coorY.valueChanged.connect(self.positionCoorY)
        self.parent.ui.checkBox_ShowRecenterImage.clicked.connect(self.recenterImage)

    def set_pano(self):
        """This function for setting the maximum and minimum of panorama view
        """
        self.max = float(self.parent.ui.lineEdit_Max.text())
        self.min = float(self.parent.ui.lineEdit_Min.text())
        self.panorama_view()

    def panorama_view(self):
        """This function to process image to panorama view.
        """
        if self.parent.image is None:
            pass
        else:
            image = self.parent.image.copy()
            if self.parent.ui.btn_Panorama.isChecked():
                self.parent.coor = self.parent.center
                self.parent.ui.btn_Anypoint.setChecked(False)
                self.parent.ui.frame_4.hide()
                self.parent.ui.frame_4.setDisabled(True)
                self.parent.ui.frame_5.show()
                self.parent.ui.frame_5.setDisabled(False)
                self.parent.ui.lineEdit_Max.setText(str(self.max))
                self.parent.ui.lineEdit_Min.setText(str(self.min))
                self.parent.moildev.PanoramaX(self.parent.mapX, self.parent.mapY, self.parent.imageWidth,
                                              self.parent.imageHeight, self.parent.m_ratio,
                                              self.max, self.min)
                self.resetCenter()
                self.show.view_result(self.parent.image)

            else:
                self.parent.ui.frame_4.setDisabled(True)
                self.parent.ui.frame_5.setDisabled(True)
                self.parent.ui.frame_4.hide()
                self.parent.ui.frame_5.hide()
                self.parent.ui.checkBox_ShowRecenterImage.setChecked(False)
                self.recenterImage()
                self.show.showOriginalImage(image)
                self.show.view_result(image)

    def recenterImage(self):
        """Process original image to change the original center image.
        """
        if self.parent.ui.checkBox_ShowRecenterImage.isChecked():
            self.parent.ui.frame.show()
            self.parent.ui.labelRecenter.show()
            self.parent.ui.labelImagerecenter.show()
            self.max = float(self.parent.ui.lineEdit_Max.text())
            self.min = float(self.parent.ui.lineEdit_Min.text())
            self.parent.revImage = self.reverseImage(self.parent.image, self.parent.res,
                                                     self.parent.alpha, self.parent.beta)
            self.parent.moildev.Panorama(self.parent.mapX, self.parent.mapY, self.min, self.max)
            self.show.showInRecenterLabel(self.parent.revImage)
            self.show.view_result(self.parent.image)
            self.updatePossCenter()

        else:
            self.parent.ui.labelRecenter.hide()
            self.parent.ui.labelImagerecenter.hide()
            self.parent.ui.frame.hide()

    def reverseImage(self, dst, src, alpha, beta):
        """reverse original image using moil SDK to recenter image.
        """
        self.parent.moildev.PanoramaM_Rt(self.parent.mapX, self.parent.mapY, 110, alpha, beta)
        panoImage = cv2.remap(dst, self.parent.mapX, self.parent.mapY, cv2.INTER_CUBIC)
        self.parent.moildev.revPanorama(panoImage, src, 110, beta)
        return src

    def positionCoorX(self):
        """Change the position coordinate center X on image recenter process
        """
        if self.parent.image is None:
            pass
        else:
            self.parent.coorX = self.parent.ui.spinBox_coorX.value()
            self.setCoorCenterObject()
            self.recenterImage()

    def positionCoorY(self):
        """Change the position coordinate center Y on image recenter process
        """
        if self.parent.image is None:
            pass
        else:
            self.parent.coorY = self.parent.ui.spinBox_coorY.value()
            self.setCoorCenterObject()
            self.recenterImage()

    def updatePossCenter(self):
        """Update position center x and y point in the user interface
        """
        self.parent.ui.spinBox_coorX.setValue(self.parent.coorX)
        self.parent.ui.spinBox_coorY.setValue(self.parent.coorY)

    def resetCenter(self):
        """This function for reset coordinate x and y.
        """
        self.parent.coorX = self.parent.imageWidth * 0.5
        self.parent.coorY = self.parent.imageHeight * 0.5
        self.parent.ui.spinBox_coorX.setValue(self.parent.coorX)
        self.parent.ui.spinBox_coorY.setValue(self.parent.coorY)

    def setCoorCenterObject(self):
        """calculate alpha and beta from the original center image.
        """
        delta_x = round(self.parent.coorX - self.parent.imageWidth * 0.5)
        delta_y = round(- (self.parent.coorY - self.parent.imageHeight * 0.5))
        self.parent.alpha, self.parent.beta = self.parent.config.get_alpha_beta(0, delta_x, delta_y)

    def showOriginalPanorama(self):
        """show original image when doing panorama view on the original label.
        """
        image = self.parent.image.copy()
        if self.parent.coor:
            oriImage = drawPoint(image, self.parent.imageHeight, self.parent.coor)
        else:
            oriImage = drawPoint(image, self.parent.imageHeight, self.parent.center)
        self.show.showOriginalImage(oriImage)
