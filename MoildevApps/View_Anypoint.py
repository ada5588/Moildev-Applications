from MoildevApps.Ui_Utils import drawPoint
from MoildevApps.View_ShowResult import ShowImageResult
import numpy as np
import cv2


class AnyPoint(object):
    """Anypoint class to process image on anypoint view
    """
    def __init__(self, MainWindow):
        """constructed method
        """
        self.parent = MainWindow
        self.show = ShowImageResult(self.parent)
        self.connectToButton()

    def connectToButton(self):
        """the method for connected function and event on main window user interface.
        """
        self.parent.ui.Button_setAnypoint.clicked.connect(self.set_anypoint)
        self.parent.ui.btn_Anypoint.clicked.connect(self.onclickAnypoint)
        self.parent.ui.radioAnypointM1.clicked.connect(self.anypoint_mode_1)
        self.parent.ui.radioAnypointM2.clicked.connect(self.anypoint_mode_2)
        self.parent.ui.spinBox_zoom.valueChanged.connect(self.zoomValue)
        self.parent.ui.btn_up.clicked.connect(self.up)
        self.parent.ui.btn_left.clicked.connect(self.left)
        self.parent.ui.btn_center.clicked.connect(self.center)
        self.parent.ui.btn_right.clicked.connect(self.right)
        self.parent.ui.brn_down.clicked.connect(self.down)
        self.parent.ui.radioAnypointM1.setChecked(True)

    def zoomValue(self):
        """The methode to change the zoom value when doing anypoint view.
        """
        self.parent.zoom = self.parent.ui.spinBox_zoom.value()
        self.anypoint_view()

    def resetAlphaBeta(self):
        """The method for reset alpa, beta, zoom, and angle.
        """
        self.parent.alpha = 0
        self.parent.beta = 0
        self.parent.zoom = 4
        self.parent.angle = 0
        if self.parent.image is None:
            self.parent.coordinate_point = None
        else:
            self.parent.coordinate_point = self.parent.center

    def onclickAnypoint(self):
        """The method for click button anypoint.
        """
        self.parent.ui.checkBox_ShowRecenterImage.setChecked(False)
        self.parent.panorama.recenterImage()
        if self.parent.ui.radioAnypointM1.isChecked():
            self.anypoint_mode_1()
        elif self.parent.ui.radioAnypointM2.isChecked():
            self.anypoint_mode_2()

    def anypoint_view(self):
        """The method to clearly process image on anypoint view.
        """
        if self.parent.image is None:
            pass
        else:
            image = self.parent.image.copy()
            if self.parent.ui.btn_Anypoint.isChecked():
                self.parent.ui.btn_Panorama.setChecked(False)
                self.parent.ui.frame_4.show()
                self.parent.ui.frame_5.hide()
                self.parent.ui.frame_4.setDisabled(False)
                self.parent.ui.frame_5.setDisabled(True)
                self.alpha = self.parent.alpha
                self.beta = self.parent.beta
                self.zoom = self.parent.zoom
                self.m_ratio = self.parent.m_ratio

                if self.parent.ui.radioAnypointM1.isChecked():
                    if self.beta < 0:
                        self.beta = self.beta + 360
                    if self.alpha < -90 or self.alpha > 90 or self.beta < 0 or self.beta > 360:
                        self.alpha = 0
                        self.beta = 0
                        self.parent.coordinate_point = self.parent.center
                    else:
                        self.alpha = -90 if self.alpha < -90 else self.alpha
                        self.alpha = 90 if self.alpha > 90 else self.alpha
                        self.beta = 0 if self.beta < 0 else self.beta
                        self.beta = 360 if self.beta > 360 else self.beta

                    self.parent.moildev.AnyPointM(self.parent.mapX, self.parent.mapY, self.parent.imageWidth,
                                                  self.parent.imageHeight, self.alpha,
                                                  self.beta, self.zoom, self.m_ratio)

                elif self.parent.ui.radioAnypointM2.isChecked():
                    if self.alpha < - 90 or self.alpha > 90 or self.beta < -90 or self.beta > 90:
                        self.alpha = 0
                        self.beta = 0
                        self.parent.coordinate_point = self.parent.center
                    else:
                        self.alpha = -90 if self.alpha < -90 else self.alpha
                        self.alpha = 90 if self.alpha > 90 else self.alpha
                        self.beta = -90 if self.beta < -90 else self.beta
                        self.beta = 90 if self.beta > 90 else self.beta

                    self.parent.moildev.AnyPointM2(self.parent.mapX, self.parent.mapY, self.parent.imageWidth,
                                                   self.parent.imageHeight, self.alpha,
                                                   self.beta, self.zoom, self.m_ratio)

                self.show.view_result(self.parent.image)
                self.updateParamAnypoint()

            else:
                self.parent.ui.frame_4.setDisabled(True)
                self.parent.ui.frame_5.setDisabled(True)
                self.parent.ui.frame_4.hide()
                self.parent.ui.frame_5.hide()
                self.show.showOriginalImage(image)
                self.show.view_result(image)

    def showPolygon(self):
        """showing the polygon on original image.
        """
        image = self.parent.image.copy()
        image = self.drawPolygon(image, self.parent.mapX, self.parent.mapY)
        if self.parent.coordinate_point is None:
            self.show.showOriginalImage(image)
        else:
            image = drawPoint(image, self.parent.imageHeight, self.parent.coordinate_point)
            self.show.showOriginalImage(image)

    def updateParamAnypoint(self):
        """The method for update anypoint on the beta, alpha and zoom
        """
        self.parent.ui.lineEdit_beta.setText("%.2f" % self.beta)
        self.parent.ui.lineEdit_alpha.setText("%.2f" % self.alpha)
        self.parent.ui.spinBox_zoom.setValue(self.zoom)

    def anypoint_mode_1(self):
        """Determine the anypoint mode 1.
        """
        self.parent.anypointState = 0
        self.resetAlphaBeta()
        self.anypoint_view()

    def anypoint_mode_2(self):
        """Determine the anypoint mode 2.
        """
        self.parent.anypointState = 1
        self.resetAlphaBeta()
        self.anypoint_view()

    def set_anypoint(self):
        """the method for event on click button set anypoint when has modify the parameter.
        """
        self.parent.alpha = float(self.parent.ui.lineEdit_alpha.text())
        self.parent.beta = float(self.parent.ui.lineEdit_beta.text())
        self.parent.zoom = float(self.parent.ui.spinBox_zoom.text())
        self.anypoint_view()

    def up(self):
        """The method showing anypoint view in specific area.
        """
        self.parent.coordinate_point = None
        if self.parent.ui.radioAnypointM1.isChecked():
            self.parent.alpha = 75
            self.parent.beta = 0
        elif self.parent.ui.radioAnypointM2.isChecked():
            self.parent.alpha = 50
            self.parent.beta = 0
        self.parent.anypoint.anypoint_view()

    def left(self):
        """The method showing anypoint view in specific area.
        """
        self.parent.coordinate_point = None
        if self.parent.ui.radioAnypointM1.isChecked():
            self.parent.alpha = 65
            self.parent.beta = -90
        elif self.parent.ui.radioAnypointM2.isChecked():
            self.parent.alpha = 0
            self.parent.beta = -75
        self.parent.anypoint.anypoint_view()

    def center(self):
        """The method showing anypoint view in specific area.
        """
        self.parent.coordinate_point = None
        if self.parent.ui.radioAnypointM1.isChecked():
            self.parent.alpha = 0
            self.parent.beta = 0
        elif self.parent.ui.radioAnypointM2.isChecked():
            self.parent.alpha = 0
            self.parent.beta = 0
        self.parent.anypoint.anypoint_view()

    def right(self):
        """The method showing anypoint view in specific area.
        """
        self.parent.coordinate_point = None
        if self.parent.ui.radioAnypointM1.isChecked():
            self.parent.alpha = 65
            self.parent.beta = 90
        elif self.parent.ui.radioAnypointM2.isChecked():
            self.parent.alpha = 0
            self.parent.beta = 65
        self.parent.anypoint.anypoint_view()

    def down(self):
        """The method showing anypoint view in specific area.
        """
        self.parent.coordinate_point = None
        if self.parent.ui.radioAnypointM1.isChecked():
            self.parent.alpha = 65
            self.parent.beta = 180
        elif self.parent.ui.radioAnypointM2.isChecked():
            self.parent.alpha = -65
            self.parent.beta = 0
        self.parent.anypoint.anypoint_view()

    def drawPolygon(self, image, mapX, mapY):
        """Draw polygon from mapX and mapY given in the original image.
        Args:
            image: Original image
            mapX: map image X from anypoint process
            mapY: map image Y from anypoint process
        return:
            image:
        """
        hi, wi = image.shape[:2]
        X1 = []
        Y1 = []
        X2 = []
        Y2 = []
        X3 = []
        Y3 = []
        X4 = []
        Y4 = []

        x = 0
        while x < wi:
            a = mapX[0,]
            b = mapY[0,]
            e = mapX[-1,]
            f = mapY[-1,]

            if a[x] == 0. or b[x] == 0.:
                pass
            else:
                X1.append(a[x])
                Y1.append(b[x])

            if f[x] == 0. or e[x] == 0.:
                pass
            else:
                Y3.append(f[x])
                X3.append(e[x])
            x += 10

        y = 0
        while y < hi:
            c = mapX[:, 0]
            d = mapY[:, 0]
            g = mapX[:, -1]
            h = mapY[:, -1]
            if d[y] == 0. or c[y] == 0.:  # or d[y] and c[y] == 0.0:
                pass

            else:
                Y2.append(d[y])
                X2.append(c[y])

            if h[y] == 0. or g[y] == 0.:
                pass
            else:
                Y4.append(h[y])
                X4.append(g[y])
            y += 10

        p = np.array([X1, Y1])
        q = np.array([X2, Y2])
        r = np.array([X3, Y3])
        s = np.array([X4, Y4])
        points = p.T.reshape((-1, 1, 2))
        points2 = q.T.reshape((-1, 1, 2))
        points3 = r.T.reshape((-1, 1, 2))
        points4 = s.T.reshape((-1, 1, 2))
        # print(self.points)
        cv2.polylines(image, np.int32([points]), False, (0, 255, 0), 10)
        cv2.polylines(image, np.int32([points2]), False, (0, 255, 0), 10)
        cv2.polylines(image, np.int32([points3]), False, (0, 255, 0), 10)
        cv2.polylines(image, np.int32([points4]), False, (0, 255, 0), 10)
        return image
