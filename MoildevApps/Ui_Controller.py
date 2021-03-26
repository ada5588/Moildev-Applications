from MoildevApps.Ui_Utils import read_image, select_file
from MoildevApps.View_ShowResult import ShowImageResult
from MoildevApps.View_Window import ViewWindow
from MoildevApps.OpenCamera import OpenCameras
from MoildevApps.View_Anypoint import AnyPoint
from MoildevApps.View_Panorama import Panorama
from MoildevApps.InitMoildev import Config
from MoildevApps.Ui_Mainwindow import *
from MoildevApps.VideoControler import Video_Controler
from PyQt5 import QtWidgets, QtGui, QtCore
from Moildev import Moildev
import numpy as np
import cv2
import datetime


class Controller(QtWidgets.QMainWindow):
    """The controller class to control UI MainWindow
    """
    def __init__(self, parent=None):
        """construction method
        """
        super(Controller, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.frame_4.hide()
        self.ui.frame_5.hide()
        self.ui.frame.hide()
        self.ui.labelRecenter.hide()
        self.ui.labelImagerecenter.hide()
        self.image = None
        self.coordinate_point = None
        self.revImage = None
        self.resultImage = None
        self.cap = None
        self.dir_save = None
        self.anypointState = 0
        self.angle = 0
        self.alpha = 0
        self.beta = 0
        self.zoom = 4
        self.width_img = 1400
        self.connect_button()

        self.showing = ShowImageResult(self)
        self.view = ViewWindow(self)
        self.videoControl = Video_Controler(self)
        self.videoControl.videoButtonDisable()
        self.anypoint = AnyPoint(self)
        self.panorama = Panorama(self)
        self.dialogOpenCam = QtWidgets.QDialog()
        self.winOpenCam = OpenCameras(self, self.dialogOpenCam)

    def connect_button(self):
        """Connect the button and event to the function
        """
        self.ui.actionLoad_video.triggered.connect(self.open_video_file)
        self.ui.actionLoad_Image.triggered.connect(self.open_image)
        self.ui.actionOpen_Cam.triggered.connect(self.onclick_open_camera)
        self.ui.actionAbout_Us.triggered.connect(self.aboutUs)
        self.ui.windowOri.mousePressEvent = self.mouse_event
        self.ui.windowOri.mouseMoveEvent = self.mouseMovedOriImage
        self.ui.windowOri.wheelEvent = self.mouse_wheelEvent
        self.ui.windowOri.mouseReleaseEvent = self.mouse_release_event
        self.ui.PlussIcon.mouseReleaseEvent = self.mouse_release_event
        self.ui.PlussIcon.mouseDoubleClickEvent = self.mouseDoubleclic_event
        self.ui.PlussIcon.wheelEvent = self.mouse_wheelEvent
        self.ui.closeEvent = self.closeEvent
        self.ui.actionHelp.triggered.connect(self.help)
        self.ui.actionExit.triggered.connect(self.exit)

    def init_parameter(self):
        """create initial parameter
        """
        self.camera = self.config.get_cameraName()
        self.sensor_width = self.config.get_sensorWidth()
        self.sensor_height = self.config.get_sensor_height()
        self.Icx = self.config.get_Icx()
        self.Icy = self.config.get_Icy()
        self.ratio = self.config.get_ratio()
        self.imageWidth = self.config.get_imageWidth()
        self.imageHeight = self.config.get_imageHeight()
        self.calibrationRatio = self.config.get_calibrationRatio()
        self.parameter0 = self.config.get_parameter0()
        self.parameter1 = self.config.get_parameter1()
        self.parameter2 = self.config.get_parameter2()
        self.parameter3 = self.config.get_parameter3()
        self.parameter4 = self.config.get_parameter4()
        self.parameter5 = self.config.get_parameter5()
        self.coorX = self.Icx
        self.coorY = self.Icy

    def init_Map(self):
        """
        create initial mapX and mapY
        """
        self.mapX = np.zeros((self.imageHeight, self.imageWidth), dtype=np.float32)
        self.mapY = np.zeros((self.imageHeight, self.imageWidth), dtype=np.float32)
        size = self.imageHeight, self.imageWidth, 3
        self.m_ratio = self.ratio
        self.res = np.zeros(size, dtype=np.uint8)

    def importMoildev(self):
        """Instantiate moildev library
        """
        self.init_parameter()
        self.moildev = Moildev(self.camera, self.sensor_width, self.sensor_height, self.Icx, self.Icy, self.ratio,
                               self.imageWidth, self.imageHeight, self.parameter0, self.parameter1, self.parameter2,
                               self.parameter3, self.parameter4, self.parameter5, self.calibrationRatio)

    def open_image(self):
        """Load image frame
        """
        self.filename = select_file("Select Image", "../", "Image Files (*.jpeg *.jpg *.png *.gif *.bmg)")
        if self.filename:
            file_name = select_file("Select Parameter", "../", "Parameter Files (*.json)")
            if file_name:
                self.ui.btn_Anypoint.setChecked(False)
                self.ui.btn_Panorama.setChecked(False)
                self.config = Config(file_name)
                self.importMoildev()
                self.image = read_image(self.filename)
                self.h, self.w = self.image.shape[:2]
                self.init_Map()
                image = self.image.copy()
                self.showing.view_result(image)
                self.ratio_x, self.ratio_y, self.center = self.init_ori_ratio(self.image)
                self.cam = False
                self.anypoint.resetAlphaBeta()

    def open_video_file(self):
        """Load video file.
        """
        videoFile = select_file("Select Video Files", "../", "Image Files (*.mp4 *.avi *.mpg *.gif *.mov)")
        if videoFile:
            paramName = select_file("Select Parameter", "../", "Parameter Files (*.json)")
            if paramName:
                self.anypoint.resetAlphaBeta()
                self.videoControl.videoButtonEnable()
                self.coordinate_point = None
                self.config = Config(paramName)
                self.importMoildev()
                self.init_Map()
                self.cap = cv2.VideoCapture(videoFile)
                self.fps = self.cap.get(cv2.CAP_PROP_FPS)
                self.cam = True
                self.next_frame_slot()

    def onclick_open_camera(self):
        """showing the window to select the source camera
        """
        self.dialogOpenCam.show()

    def cameraOpen(self):
        """Open camera following the source given.
        """
        self.videoStreamURL = self.winOpenCam.video_source()
        if self.videoStreamURL is None:
            pass
        else:
            self.cap = cv2.VideoCapture(self.videoStreamURL)
            self.coordinate_point = None
            self.ret, self.image = self.cap.read()
            if self.image is None:
                QtWidgets.QMessageBox.information(self, "Information", "No source camera founded")
            else:
                QtWidgets.QMessageBox.information(self, "Information", "Select Parameter Camera !!")
                file_name = select_file("Select Left Parameter", "../", "Parameter Files (*.json)")
                if file_name:
                    self.config = Config(file_name)
                    self.importMoildev()
                    self.videoControl.videoButtonCamera()
                    self.init_Map()
                    self.fps = self.cap.get(cv2.CAP_PROP_FPS)
                    self.cam = True
                    self.next_frame_slot()
                else:
                    self.cap.release()

    def next_frame_slot(self):
        """Control video frame.
        """
        self.ret, self.image = self.cap.read()
        if self.image is None:
            pass
        else:
            self.oriImage = self.image.copy()
            self.h, self.w = self.image.shape[:2]
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.pos_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            self.pos_msec = self.cap.get(cv2.CAP_PROP_POS_MSEC)
            self.frame_count = float(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration_sec = int(self.frame_count / self.fps)
            self.minutes = duration_sec // 60
            duration_sec %= 60
            self.seconds = duration_sec
            sec_pos = int(self.pos_frame / self.fps)
            self.minute = int(sec_pos // 60)
            sec_pos %= 60
            self.sec = sec_pos
            self.videoControl.controler()
            self.ratio_x, self.ratio_y, self.center = self.init_ori_ratio(self.image)
            image = self.image.copy()
            self.showing.view_result(image)
            if self.videoControl.record:
                if self.ui.btn_Anypoint.isChecked() or self.ui.btn_Panorama.isChecked():
                    self.videoControl.video_writer.write(self.showing.resultImage)
                else:
                    self.videoControl.video_writer.write(self.image)

    def init_ori_ratio(self, image):
        """Calculate the initial ratio of the image.
        Args:
            ratio_x = ratio width between image and ui window.
            ratio_y = ratio height between image and ui window.
            center = find the center image on window user interface.
        return:
            ratio_x:
            ratio_y:
            center:
        """
        h = self.ui.windowOri.height()
        w = self.ui.windowOri.width()
        height, width = image.shape[:2]
        ratio_x = width / w
        ratio_y = height / h
        center = (round((w / 2) * ratio_x), round((h / 2) * ratio_y))
        return ratio_x, ratio_y, center

    def mouse_event(self, e):
        """Specify coordinate from mouse left event.
        """
        if self.image is None:
            pass
        else:
            if e.button() == QtCore.Qt.LeftButton:
                self.currPos = e.pos()
                self.pos_x = round(e.x())
                self.pos_y = round(e.y())
                delta_x = round(self.pos_x * self.ratio_x - self.imageWidth * 0.5)
                delta_y = round(- (self.pos_y * self.ratio_y - self.imageHeight * 0.5))
                self.coordinate_point = (round(self.pos_x * self.ratio_x), round(self.pos_y * self.ratio_y))
                self.coorX = round(self.pos_x * self.ratio_x)
                self.coorY = round(self.pos_y * self.ratio_y)
                if self.ui.btn_Anypoint.isChecked():
                    self.alpha, self.beta = self.config.get_alpha_beta(self.anypointState, delta_x, delta_y)
                    self.anypoint.anypoint_view()
                elif self.ui.checkBox_ShowRecenterImage.isChecked():
                    self.alpha, self.beta = self.config.get_alpha_beta(0, delta_x, delta_y)
                    self.panorama.recenterImage()
                else:
                    print("coming soon")

    def mouseDoubleclic_event(self, e):
        """Reset to default by mouse event.
        """
        self.anypoint.resetAlphaBeta()
        if self.ui.btn_Anypoint.isChecked():
            self.anypoint.anypoint_view()
        elif self.ui.btn_Panorama.isChecked():
            self.panorama.resetCenter()
            self.panorama.recenterImage()
        else:
            pass

    def mouse_wheelEvent(self, e):
        """Resize image using mouse wheel event.
        """
        if self.image is None:
            pass
        else:
            modifiers = QtWidgets.QApplication.keyboardModifiers()
            if modifiers == QtCore.Qt.ControlModifier:
                wheelcounter = e.angleDelta()
                if wheelcounter.y() / 120 == -1:
                    if self.width_img == 1100:
                        pass
                    else:
                        self.width_img -= 100

                if wheelcounter.y() / 120 == 1:
                    if self.width_img == 4000:
                        pass
                    else:
                        self.width_img += 100
                self.showing.view_result(self.image)

    def mouseMovedOriImage(self, e):
        """Mouse move event to look in surrounding view in original label image
        """
        self.currPos = e.pos()
        self.pos_x = round(e.x())
        self.pos_y = round(e.y())
        delta_x = round(self.pos_x * self.ratio_x - self.imageWidth * 0.5)
        delta_y = round(- (self.pos_y * self.ratio_y - self.imageHeight * 0.5))
        self.coordinate_point = (round(self.pos_x * self.ratio_x), round(self.pos_y * self.ratio_y))
        self.coorX = round(self.pos_x * self.ratio_x)
        self.coorY = round(self.pos_y * self.ratio_y)
        if self.ui.btn_Anypoint.isChecked():
            self.alpha, self.beta = self.config.get_alpha_beta(self.anypointState, delta_x, delta_y)
            self.anypoint.anypoint_view()

    def mouse_release_event(self, e):
        """Mouse release event left click to show menu.
        """
        if e.button() == QtCore.Qt.LeftButton:
            pass
        else:
            if self.image is None:
                pass
            else:
                self.menuMouseEvent(e)

    def menuMouseEvent(self, e):
        """showing the menu image when release left click.
        """
        menu = QtWidgets.QMenu()
        maxi = menu.addAction("Show Maximized")
        maxi.triggered.connect(self.view.show_Maximized)
        mini = menu.addAction("Show Minimized")
        mini.triggered.connect(self.view.show_Minimized)
        save = menu.addAction("Save Image")
        info = menu.addAction("Show Info")
        save.triggered.connect(self.saveImage)
        info.triggered.connect(self.help)
        menu.exec_(e.globalPos())

    def saveImage(self):
        """Save image on local directory
        """
        ss = datetime.datetime.now().strftime("%m_%d_%H_%M_%S")
        name_image = "Original"
        image = self.image
        if self.ui.btn_Panorama.isChecked() or self.ui.btn_Anypoint.isChecked():
            name_image = "result"
            image = self.resultImage
        if self.dir_save is None or self.dir_save == "":
            self.selectDir()
        else:
            name = self.dir_save + "/" + name_image + "_" + str(ss) + ".png"
            cv2.imwrite(name, image)
            QtWidgets.QMessageBox.information(self, "Information", "Image saved !!\n\nLoc @: " + self.dir_save)

    def selectDir(self):
        """Select directory to save object such as image and video.
        """
        self.dir_save = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Save Folder')
        if self.dir_save:
            self.saveImage()

    def aboutUs(self):
        """showing prompt About us information (MOIL LAB)
        """
        self.dialogOpenCam.close()
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("About Us")
        msgbox.setText(
            "MOIL \n\nOmnidirectional Imaging & Surveillance Lab\nMing Chi University of Technology\n\n")
        msgbox.setIconPixmap(QtGui.QPixmap('./assets/128.png'))
        msgbox.exec()

    def help(self):
        """showing the message box to show help information obout this application
        """
        self.dialogOpenCam.close()
        msgbox = QtWidgets.QMessageBox()
        msgbox.setWindowTitle("Help !!")
        msgbox.setText("Moildev-Apps\n\n"
                       "Moildev-Apps is software to process fisheye "
                       "image with the result panorama view and Anypoint"
                       " view. \n\nThe panoramic view may present a horizontal"
                       "view in a specific immersed environment to meet the"
                       "common human visual perception, while the Anypoint"
                       "view is an image that has been undistorted in a certain"
                       "area according to the input coordinates."
                       "\n\nMore reference about Moildev, contact us\n\n")
        msgbox.setIconPixmap(QtGui.QPixmap('./assets/128.png'))
        msgbox.exec()

    def exit(self):
        """Exit the apps with showing the QMessageBox.
        """
        self.dialogOpenCam.close()
        self.close()

    def closeEvent(self, event):
        """Control exit application by ask yes or no question.
        """
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               "Are you sure to quit?", QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.exit()
            event.accept()
        else:
            event.ignore()
