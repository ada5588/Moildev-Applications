import math
import json


class Config(object):
    """Reading the parameter camera from *.json file
    """
    def __init__(self, filename):
        """Constructor method
        Args:
            filename = .json file
            filename = dictionary

        return:
            camera name
            camera sensor width
            camera sensor height
            iCx
            iCy
            ratio
            image width
            image height
            calibration ratio
            parameter0
            parameter1
            parameter2
            parameter3
            parameter4
            parameter5
        """
        super(Config, self).__init__()
        self.PI = 3.1415926
        self.alphaToRho_Table = []
        self.rhoToAlpha_Table = []
        if filename is None:
            pass
        else:
            with open(filename) as f:
                data = json.load(f)
            self.camera = data["cameraName"]
            self.sensor_width = data['cameraSensorWidth']
            self.sensor_height = data['cameraSensorHeight']
            self.Icx = data['iCx']
            self.Icy = data['iCy']
            self.ratio = data['ratio']
            self.imageWidth = data['imageWidth']
            self.imageHeight = data['imageHeight']
            self.calibrationRatio = data['calibrationRatio']
            self.parameter0 = data['parameter0']
            self.parameter1 = data['parameter1']
            self.parameter2 = data['parameter2']
            self.parameter3 = data['parameter3']
            self.parameter4 = data['parameter4']
            self.parameter5 = data['parameter5']

        self.initAlphaRho_Table()

    def get_cameraName(self):
        """get camera name"""
        return self.camera

    def get_sensorWidth(self):
        """get sensor width"""
        return self.sensor_width

    def get_sensor_height(self):
        """get sensor height"""
        return self.sensor_height

    def get_Icx(self):
        """get center image in X axis"""
        return self.Icx

    def get_Icy(self):
        """get center image in Y axis"""
        return self.Icy

    def get_ratio(self):
        """get ratio image"""
        return self.ratio

    def get_imageWidth(self):
        """get image width"""
        return self.imageWidth

    def get_imageHeight(self):
        """get image height"""
        return self.imageHeight

    def get_calibrationRatio(self):
        """get calibration ratio"""
        return self.calibrationRatio

    def get_parameter0(self):
        """get parameter 0"""
        return self.parameter0

    def get_parameter1(self):
        """get parameter 1"""
        return self.parameter1

    def get_parameter2(self):
        """get parameter 2"""
        return self.parameter2

    def get_parameter3(self):
        """get parameter 3"""
        return self.parameter3

    def get_parameter4(self):
        """get parameter 4"""
        return self.parameter4

    def get_parameter5(self):
        """get parameter 5"""
        return self.parameter5

    def initAlphaRho_Table(self):
        """create list for initial alpha to rho(height image)"""
        for i in range(1800):
            alpha = i / 10 * 3.1415926 / 180
            self.alphaToRho_Table.append((self.parameter0 * alpha * alpha * alpha * alpha * alpha * alpha
                                          + self.parameter1 * alpha * alpha * alpha * alpha * alpha
                                          + self.parameter2 * alpha * alpha * alpha * alpha
                                          + self.parameter3 * alpha * alpha * alpha
                                          + self.parameter4 * alpha * alpha
                                          + self.parameter5 * alpha) * self.calibrationRatio)
            i += 1

        i = 0
        index = 0
        while i < 1800:
            while index < self.alphaToRho_Table[i]:
                self.rhoToAlpha_Table.append(i)
                index += 1
            i += 1

        while index < 3600:
            self.rhoToAlpha_Table.append(i)
            index += 1

    def getAlphaFromRho(self, rho):
        """return the alpha from rho image"""
        if rho >= 0:
            return self.rhoToAlpha_Table[rho] / 10
        else:
            return -self.rhoToAlpha_Table[-rho] / 10

    def getRhoFromAlpha(self, alpha):
        """return rho image from alpha given"""
        return self.alphaToRho_Table[round(alpha * 10)]

    def get_alpha_beta(self, mode, delta_x, delta_y):
        """calculate the alpha beta from specific coordinate image.
        Args:
            mode = the anypoint mode.
            mode = integer.
            delta_x = the coordinate point in quadrant 1 X axis.
            delta_x = integer.
            delta_y = the coordinate point in quadrant 1 Y axis.
            delta_y = integer.

        return:
            alpha
            beta.
        """
        if mode == 0:
            r = round(math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2)))
            alpha = self.getAlphaFromRho(r)

            if delta_x == 0:
                angle = 0
            else:
                angle = (math.atan2(delta_y, delta_x) * 180) / self.PI

            beta = 90 - angle

        else:
            alpha = self.getAlphaFromRho(delta_y)
            beta = self.getAlphaFromRho(delta_x)

        return alpha, beta

