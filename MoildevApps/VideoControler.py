from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
import cv2
import os


class Video_Controler(object):
    """The class to control the video. this class also inheritance from mainwindow class.
    :param parent : main window class
    :type : -
    """
    def __init__(self, Mainwindow):
        """Constructor method
        """
        self.parent = Mainwindow
        self.play = False
        self.record = False
        self.videoDir = None
        self.connectToButton()

    def connectToButton(self):
        """This functions to connect each button on the user interface
        """
        self.parent.ui.actionClose_Cam.triggered.connect(self.stop_camera)
        self.parent.ui.videoPlay.clicked.connect(self.videoPlayPouse)
        self.parent.ui.videoStop.clicked.connect(self.stop_video)
        self.parent.ui.videoSkip.clicked.connect(self.skip_video)
        self.parent.ui.videoBack.clicked.connect(self.prev_video)
        self.parent.ui.sliderVideotime.valueChanged.connect(self.changeValue)
        self.parent.ui.actionRecord_Video.triggered.connect(self.recordVideo)

    def videoButtonDisable(self):
        """This method has function to disable the buttons control video when not in video mode.
        """
        self.parent.ui.videoPlay.setDisabled(True)
        self.parent.ui.videoStop.setDisabled(True)
        self.parent.ui.videoSkip.setDisabled(True)
        self.parent.ui.videoBack.setDisabled(True)
        self.parent.ui.sliderVideotime.setDisabled(True)
        self.parent.ui.label_4.setDisabled(True)
        self.parent.ui.label_3.setDisabled(True)

    def videoButtonEnable(self):
        """This method has function to enable the buttons control video when in video mode.
        """
        self.parent.ui.videoPlay.setDisabled(False)
        self.parent.ui.videoStop.setDisabled(False)
        self.parent.ui.videoSkip.setDisabled(False)
        self.parent.ui.videoBack.setDisabled(False)
        self.parent.ui.sliderVideotime.setDisabled(False)
        self.parent.ui.label_4.setDisabled(False)
        self.parent.ui.label_3.setDisabled(False)

    def videoButtonCamera(self):
        """Control the video controller when in camera mode
        """
        self.parent.ui.videoPlay.setDisabled(False)
        self.parent.ui.videoStop.setDisabled(False)
        self.parent.ui.videoSkip.setDisabled(False)
        self.parent.ui.videoBack.setDisabled(False)
        self.parent.ui.sliderVideotime.setDisabled(True)
        self.parent.ui.label_4.setDisabled(True)
        self.parent.ui.label_3.setDisabled(True)

    def reset_time(self):
        """Reset the time when open the new video.
        """
        current = self.parent.ui.label_3
        current.setAlignment(QtCore.Qt.AlignCenter)
        current.setText("00:00")

        current_1 = self.parent.ui.label_4
        current_1.setAlignment(QtCore.Qt.AlignCenter)
        current_1.setText("00:00")

    def videoPlayPouse(self):
        """Control play and pause when playing video or camera.
        """
        if self.play:
            self.timer.stop()
            self.parent.ui.videoPlay.setIcon(QtGui.QIcon("assets/control.png"))
            self.pause_video()
            self.play = False

        else:
            self.parent.ui.videoPlay.setIcon(QtGui.QIcon("assets/control-pause.png"))
            self.play_video()
            self.play = True

    def play_video(self):
        """Play video.
        """
        if self.parent.cap.isOpened():
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.parent.next_frame_slot)
            self.timer.start(1000. / self.parent.fps)
        else:
            pass

    def pause_video(self):
        """Pause video.
        """
        self.timer.stop()

    def stop_video(self):
        """Stop Video.
        """
        self.play = False
        self.parent.ui.videoPlay.setIcon(QtGui.QIcon("assets/control.png"))
        if self.parent.cap.isOpened():
            self.parent.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.parent.next_frame_slot()
            self.pause_video()
            self.reset_time()
            # self.parent.image = None
        else:
            pass

    def stop_camera(self):
        """Stop camera and clear label view.
        """
        if self.parent.cam:
            self.timer.stop()
            self.parent.cap.release()
            self.parent.ui.windowOri.clear()
            self.parent.ui.windowResult.clear()
        else:
            pass

    def prev_video(self):
        """Previous video in 5 second.
        """
        if self.parent.cap.isOpened():
            position = self.parent.pos_frame - 5 * self.parent.fps
            self.parent.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
            self.parent.next_frame_slot()
        else:
            pass

    def skip_video(self):
        """skip video in 5 second.
        """
        if self.parent.cap.isOpened():
            position = self.parent.pos_frame + 5 * self.parent.fps
            self.parent.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
            self.parent.next_frame_slot()
        else:
            pass

    def changeValue(self, value):
        """Control slider time video.
        """
        if self.parent.cap.isOpened():
            dst_frame = self.parent.frame_count * value / self.parent.ui.sliderVideotime.maximum() + 1
            self.parent.cap.set(cv2.CAP_PROP_POS_FRAMES, dst_frame)
            self.parent.next_frame_slot()
            self.timer.stop()
        else:
            pass

    def controler(self):
        """Manage the video to setup the current timer.
        """
        dst_value = self.parent.pos_frame * (self.parent.ui.sliderVideotime.maximum() + 1) / self.parent.frame_count
        self.parent.ui.sliderVideotime.blockSignals(True)
        self.parent.ui.sliderVideotime.setValue(dst_value)
        self.parent.ui.sliderVideotime.blockSignals(False)

        current = self.parent.ui.label_3
        current.setAlignment(QtCore.Qt.AlignCenter)
        current.setText("%02d : %02d" % (self.parent.minute, self.parent.sec))

        if self.parent.minute > 1000:
            my_label3 = self.parent.ui.label_4
            my_label3.setAlignment(QtCore.Qt.AlignCenter)
            my_label3.setText("00:00")

        else:
            my_label3 = self.parent.ui.label_4
            my_label3.setAlignment(QtCore.Qt.AlignCenter)
            my_label3.setText("%02d : %02d" % (self.parent.minutes, self.parent.seconds))

    def recordVideo(self):
        """Create video writer to save video.
        """
        if self.record is False:
            self.timer.stop()
            ss = datetime.datetime.now().strftime("%m_%d_%H_%M_%S")
            frame_width = int(self.parent.cap.get(3))
            frame_height = int(self.parent.cap.get(4))
            filename = "Original"
            if self.parent.ui.btn_Panorama.isChecked() or self.parent.ui.btn_Anypoint.isChecked():
                filename = "result"
            if self.videoDir is None or self.videoDir == "":
                self.selectDir()
            else:
                name = self.videoDir + "/" + filename + "_" + str(ss) + ".avi"
                answer = QtWidgets.QMessageBox.information(self.parent.ui, "Information", " Start Record Video !!",
                                                           QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

                if answer == QtWidgets.QMessageBox.Yes:
                    self.timer.start()
                    self.video_writer = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'XVID'), 15,
                                                        (frame_width, frame_height))
                    os.makedirs(os.path.dirname(name), exist_ok=True)
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap.fromImage(self.parent.ui.ctx.img_recording))
                    self.parent.ui.actionRecord_Video.setIcon(icon)
                    self.record = True
                else:
                    pass

        else:
            self.video_writer.release()
            self.timer.stop()
            QtWidgets.QMessageBox.information(self.parent.ui, "Information", "Video saved !!\n\nLoc: " + self.videoDir)
            self.timer.start()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap.fromImage(self.parent.ui.ctx.img_rec))
            self.parent.ui.actionRecord_Video.setIcon(icon)
            self.record = False

    def selectDir(self):
        """Select destination directory to save the video file.
        """
        self.videoDir = QtWidgets.QFileDialog.getExistingDirectory(self.parent.ui, 'Select Save Directory')
        if self.videoDir:
            self.recordVideo()
