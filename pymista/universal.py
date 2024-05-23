import time

class UniversalStage(object):
    def __init__(self, port = None):
        self.stagetype = 'universal'
        self.connectStage(port)

    def connectStage(self, port = None):
        # This example has 4 axis for some reason!
        self.stageConnection = UniversalConnection()
        self.axes = (UniversalAxis(),UniversalAxis(),UniversalAxis(),UniversalAxis())

    def home(self, force = False):
        """
        Home all axis in the stage. Set force to alwayse home, otherwise only home when not allready homed.
        """
        for ax in self.axes:
            if not ax.is_homed() or force:
                ax.home()

    def is_homed(self) -> bool: 
        """
        Check if stage is homed
        """
        return [ax.is_homed() for ax in self.axes] 
    
    def close(self):
        """
        Close connection
        """
        self.stageConnection.close()

    def __enter__(self):
        '''for with... constructions'''
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        #Exception handling here, if an error occurs in the with block
        self.close()

    def move_absolute(self, position : list[float], wait_until_idle=True):
        """
        Move stage to absolute position.

        Parameters
        ----------
        position : list[float]
            position in micometer for each axis
        wait_until_idle : bool, optional
            block script until complete if True, by default True
        """
        for i,ax in enumerate(self.axes):
            ax.move_absolute(position[i],wait_until_idle=False)
        if wait_until_idle:
            self.wait_until_idle()

    def move_relative(self, move : list[float], wait_until_idle=True):
        """
        Move stage by given move.

        Parameters
        ----------
        move : list[float]
            distance to move in micrometer for each axis
        wait_until_idle : bool, optional
            block script until complete if True,, by default True
        """
        for i,ax in enumerate(self.axes):
            ax.move_relative(move[i],wait_until_idle=False)
        if wait_until_idle:
            self.wait_until_idle()

    def get_position(self) -> list[float]:
        """
        Get current position of all axis

        Returns
        -------
        list[float]
            position of each axis
        """
        return [ax.get_position() for ax in self.axes] 

    def stop(self):
        """Stop all movement ASAP"""
        _ = [ax.stop() for ax in self.axes] 

    def wait_until_idle(self):
        """Sleep until all movement is stopped"""
        while self.is_moving():
            pass
            # exit loop only when all axis are no longer moving

    def is_moving(self) -> bool:
        """Check if stage is currently moving"""
        return any([ax.is_busy() for ax in self.axes])

    def get_bounds(self):
        maxima = self.settings_get('limit.max')
        minima = self.settings_get('limit.min')
        return ((minima[0],maxima[0]),(minima[1],maxima[1]))

    def settings_get(self, setting : str, unit = None) -> list:
        """
        Get a setting for each axis.

        Parameters
        ----------
        setting : str
            Setting label. Available settings depend on brand.
        unit : float, optional
            Unit of the value in the setting, if applicable. By default None, meaning use micrometer if available, otherwise the default.

        Returns
        -------
        list
            setting value for each axis
        """
        return [ax.settings.get(setting, unit) for ax in self.axes] 

    def settings_set(self, setting, value: str, unit = None):
        """
        Set a setting in *all* axis.

        Parameters
        ----------
        setting : str
            Setting label. Available settings depend on brand.
        value : any type
            value to set setting to
        unit : float, optional
            Unit of the value in the setting, if applicable. By default None, meaning use micrometer if available, otherwise the default.
        """
        _ = [ax.settings.set(setting, value, unit) for ax in self.axes] 

#####################################
# The stuff that follows below are the minimal classes needed to mimick behaviour of the zaberstage
# for a dummyclass, or to serve as an example to implement a new stage with the same universal API.
# Not complete at all. If you get an error somehow, just add more bits to this.
#####################################

class UniversalConnection(object):
    def __init__(self):
        self.connected = True
    def close(self):
        self.connected = False

class UniversalAxis(object):
    def __init__(self):
        self.position = 0
        self.settings = UniveralsAxisSettings()
        self.homed = "True"
    
    def is_homed(self):
        return self.homed
    
    def home(self):
        time.sleep(1) # sleep to make it convincing
        return True

    def get_position(self):
        # ignore unit. Not interesting
        return self.position
    
    def move_absolute(self, position, wait_until_idle=True):
        self.position = position

    def stop(self):
        pass
    
    def is_busy(self):
        return False

    def move_relative(self, move, wait_until_idle=True):
        self.position += move

class UniveralsAxisSettings:
    def __init__(self):
        self.properties = { # give arbitrary bounds
            "limit.max" : 50000,
            "limit.min" : 0,
        }
    def get(self,property,unit):
        # ignore the unit, not interesting
        return self.properties[property]
    
    def set(self,property,value,unit):
        self.properties[property] = value
