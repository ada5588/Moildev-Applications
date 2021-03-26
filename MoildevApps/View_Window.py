from PyQt5 import QtCore


class ViewWindow(object):
    """Class to control the window in user interface
    :param parent= Main window
    :type parent = -
    """
    def __init__(self, MainWindow):
        """Constructed method.
        """
        self.parent = MainWindow
        self.connectToButton()

    def connectToButton(self):
        """The method for connect the function with UI event
        """
        self.parent.ui.actionMaximized.triggered.connect(self.show_Maximized)
        self.parent.ui.actionMinimized.triggered.connect(self.show_Minimized)
        self.parent.ui.actionHide_Toolbar.triggered.connect(self.hideToolbar)

    def show_Maximized(self):
        """To showing the result image in maximize window. it will hide the original label image.
        """
        if self.parent.image is None:
            pass
        else:
            self.parent.ui.scrollArea_2.hide()
            self.parent.width_img = 2000
            self.parent.ui.scrollArea_3.setMaximumSize(QtCore.QSize(self.parent.width_img, 16777215))
            self.parent.show.view_result(self.parent.image)
            self.maxi = True

    def show_Minimized(self):
        """To showing the result image in minimized window. it will hide the original label image.
        """
        if self.parent.image is None:
            pass
        else:
            self.parent.ui.scrollArea_2.show()
            self.parent.width_img = 1400
            self.parent.ui.scrollArea_3.setMaximumSize(QtCore.QSize(self.parent.width_img, 16777215))
            self.parent.show.view_result(self.parent.image)
            self.maxi = False

    def hideToolbar(self):
        """Hide the toolbar.
        """
        if self.parent.ui.actionHide_Toolbar.isChecked():
            self.parent.ui.toolBar.hide()
        else:
            self.parent.ui.toolBar.show()
