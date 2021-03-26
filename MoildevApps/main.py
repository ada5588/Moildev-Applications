#######################################################
# the application for implementation MoilSDK
# writen by Haryanto
# email: M07158031@o365.mcut.edu.twsour 
#######################################################
from MoildevApps.Ui_Controller import *
import sys


def main():
    """
    Create instance Main window to create the mainwindow of Application.

    """
    apps = QtWidgets.QApplication(sys.argv)
    window = Controller()
    window.show()
    sys.exit(apps.exec_())


if __name__ == '__main__':
    main()
