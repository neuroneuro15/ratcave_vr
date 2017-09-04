from _libdpx import DPxEnableVidScanningBacklight, \
    DPxDisableVidScanningBacklight, DPxIsVidScanningBacklight, DPxOpen, DPxClose, \
    DPxSetVidBacklightIntensity, DPxGetVidBacklightIntensity
from abc import ABCMeta, abstractmethod


class ScanningBackLight(object):
    """ Implements the Scanning Back Light methods for a VIEWPixx.
    
    """                                          
    __metaclass__ = ABCMeta     
    def setScanningBackLight(self, enable):
        """Sets the scanning back light mode.
        
        This method allows the user to turn the scanning back light on or off.
        When the scanning back light is enabled, the screen will look dimmer. When
        scanning back light is disabled, the screen will look brighter.

        Args:
            enable (bool): Scanning back light mode.
        """
        if enable == True:
            DPxEnableVidScanningBacklight()
        else:
            DPxDisableVidScanningBacklight()



    def isScanningBackLightEnabled(self):
        """Gets the scanning back light state.

        Returns:
            bool: ``True`` if scanning back light is enabled, ``False`` otherwise.
        """
        if DPxIsVidScanningBacklight() is 0:
            enable = False
        else:
            enable = True
        return enable
    
    
    
    def setBacklightIntensity(self, intensity):
        """Sets the display current back light intensity.
        
        Args:
            intensity (int): Set to ``0`` for the lowest intensity level, ``255`` for the highest, or any value in between.
        
        :Example:
        
        >>> my_device.setBacklightIntensity(42)
        >>> my_device.updateRegisterCache()
        >>> print my_device.getBacklightIntensity()
        42
        
        See also:
            :class:`getBacklightIntensity` 
        """
        DPxSetVidBacklightIntensity(intensity)
    
    
    
    def getBacklightIntensity(self):
        """ Returns the level of the VIEWPixx back light intensity.
        
        Returns:
            An integer between 0 and 255.
                    
        :Example:
        
        >>> print my_device.getBacklightIntensity()
        255
            
        See also:
            :class:`setBacklightIntensity` 
        """
        return DPxGetVidBacklightIntensity()