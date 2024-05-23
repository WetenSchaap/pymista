"""
Class controlling zaber stage
"""
from .universal import *
import serial.tools.list_ports

class ZaberStage(UniversalStage):
    def __init__(self, port = None):
        import zaber_motion
        import zaber_motion.ascii
        self.zm = zaber_motion
        self.zm.ascii = zaber_motion.ascii
        super(ZaberStage, self).__init__(port) # be carefull with the order!
        self.unit = self.zm.Units.LENGTH_MICROMETRES
        self.stagetype = "zaber"

    def connectStage(self, port = None):
        """
        Connect to stage. Will autodetect port, but you can override this by setting port.

        Parameters
        ----------
        port : float, optional
            Port where Zaber stage is attached (if you do not want autodetect), by default None
        """
        if port == None:
            self.zaber_port = self._getZaberPort()
        else:
            self.zaber_port = port
        self.stageConnection = self.zm.ascii.Connection.open_serial_port(self.zaber_port)
        self.stageConnection.enable_alerts()
        device_list = self.stageConnection.detect_devices()
        self.axes = [dev.get_axis(1) for dev in device_list]

    def move_absolute(self, position, wait_until_idle=True):
        for i,ax in enumerate(self.axes):
            ax.move_absolute(position[i],self.unit,wait_until_idle=False)
        if wait_until_idle:
            self.wait_until_idle()

    def move_relative(self, move, wait_until_idle=True):
        for i,ax in enumerate(self.axes):
            ax.move_relative(move[i],self.unit,wait_until_idle=False)
        if wait_until_idle:
            self.wait_until_idle()

    def get_position(self):
        return [ax.get_position(self.unit) for ax in self.axes]

    def settings_get(self, setting : str, unit = None):
        if unit == None:
            unit = self.unit
        return super(ZaberStage, self).settings_get(setting,unit)

    def settings_set(self, setting : str, value, unit = None):
        if unit == None:
            unit = self.unit
        super(ZaberStage, self).settings_set(setting,value,unit)

    def _getZaberPort(self):
        """
        Automatically detect zaber stage USB-connection port.
        """
        zaberSerialPort = ""
        allPorts = serial.tools.list_ports.comports()
        for device in allPorts:
            if device.vid == 1027 and device.pid == 24577: # Our zaber devices have these VID/PIDs, I cannot really check if this is universal...
                zaberSerialPort = device.device
                return zaberSerialPort
        if zaberSerialPort == "":
            raise ConnectionError("Zaber XY stage not autodetected")