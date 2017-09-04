from _libdpx import DPxUpdateRegCache, DPxSetVidMode, DPxGetVidMode, \
    DPxEnableVidLcd3D60Hz, DPxDisableVidLcd3D60Hz, DPxIsVidLcd3D60Hz, \
    DPxSetVidBacklightIntensity, DPxGetVidBacklightIntensity
from analogIn import AnalogIn
from analogOut import AnalogOut
from audioIn import AudioIn
from audioOut import AudioOut
from digitalIn import DigitalIn
from digitalOut import DigitalOut
from dpxDevice import DpxDevice
from dualLinkOut import DualLinkOut
from scanningBackLight import ScanningBackLight
from threeDFeatures import ThreeDFeatures
from videoFeatures import VideoFeatures


class VIEWPixx(DpxDevice, DualLinkOut, ScanningBackLight, VideoFeatures, ThreeDFeatures):    
    """Class Definition for the VIEWPixx Device.
    
    The bases defined bellow are the core subsystems attached to a VIEWPixx devices. A VIEWPixx
    device also has very specific subsystems which are used through handles. See the example bellow
    for more details.
         
    Note: 
        If you have a **Lite** version of the device, some of these handles will 
        not be available. The usage of the handles is as follows:
    
    >>> from pypixxlib.viewpixx import VIEWPixx
    >>> my_device = VIEWPixx()
    >>> my_device.adc.function() # adc is the subsystem in this example.
    >>> my_device.BaseFunction() # A base function from one of the class' bases.
    
    Attributes:
        name: Name of the device.
        adc: Handle for the control of Analog In signal. See :doc:`analogIn`.
        dac: Handle for the control of Analog Out signal. See :doc:`analogOut`.
        audio: Handle for the audio controls. See :doc:`audioOut`.
        micro: Handle for the microphone controls. See :doc:`audioIn`.
        din: Handle for the control of Digital In signal. See :doc:`digitalIn`.
        dout: Handle for the control of Digital Out signal. See :doc:`digitalOut`.
        subsytems: A list of the available subsystems related to your physical device.
        
    """   
    def __init__(self):
        super(VIEWPixx, self).__init__('VIEWPixx')
        
        self.number_of_line = 1200
        self.devsel = 20
        
        if 'Lite' in self.name:
            self._setLiteSubSystems()
        else:
            self._setFullSubSystems()
            
    def _setLiteSubSystems(self):
        
        self.din = DigitalIn()
        self.dout = DigitalOut()
        self.subsystems = ['General','Digital I/O']

    def _setFullSubSystems(self):
        
        self.adc = AnalogIn()
        self.dac = AnalogOut()
        self.audio = AudioOut()
        self.micro = AudioIn()
        self.din = DigitalIn()
        self.dout = DigitalOut()
        
        self.subsystems = ['General','Analog I/O', 'Audio I/O', 'Digital I/O']
        
    def setPixelPolarityInversion(self, enable):
        """Sets the 3D pixel polarity inversion.
        
        Liquid crystal displays can exhibit an artifact when presenting 2 static images on alternating video frames,
        such as with frame-sequential 3D. The origin of this artifact is related to LCD pixel polarity inversion.
        The optical transmission of a liquid crystal cell varies with the magnitude of the voltage applied to the cell.
        Liquid crystal cells are designed to be driven by an AC voltage with little or no DC component.
        As such, the cell drivers alternate the polarity of the cell's driving voltage on alternate video frames.
        The cell will see no net DC driving voltage, as long as the pixel is programmed to the same intensity on even and odd video frames.
        Small differences in a pixel's even and odd frame luminance tend to leave the cell unaffected,
        and large differences in even and odd frame luminance for short periods of time (10-20 frames?) also do not seem to affect the cell;
        however, large differences in luminance for a longer period of time will cause a DC buildup in the pixel's liquid crystal cell.
        This can result in the pixel not showing the programmed luminance correctly, and can also cause the
        pixel to "stick" for several seconds after the image has been removed, causing an after-image on the display.
        VPixx Technologies has developed a strategy for keeping the pixel cells DC balanced.
        Instead of alternating the cell driving voltage on every video frame, we can alternate the voltage
        only on every second frame. This feature is enabled by calling the routine DPxEnableVidLcd3D60Hz().
        Call this routine before presenting static or slowly-moving 3D images, or when presenting 60Hz flickering stimuli.
        Be sure to call DPxDisableVidLcd3D60Hz() afterwards to return to normal pixel driving.
        Note that this feature is only supported on the VIEWPixx/3D when running with a refresh rate of 120Hz.

        Args:
            enable (Bool): True to enable the pixel polarity inversion, False to disable it.
            
        See Also:
            :class:`isPixelPolarityInversionEnabled`

        """
        if enable is True:
            DPxEnableVidLcd3D60Hz()
        else:
            DPxDisableVidLcd3D60Hz()


    def isPixelPolarityInversionEnabled(self):
        """Verifies that 3D pixel polarity inversion is enabled.
    
        Returns:
            Bool: True if the pixel polarity inversion is enabled, False otherwise.
                
        See Also:
            :class:`setPixelPolarityInversion`
            
            """
        if DPxIsVidLcd3D60Hz() == 0:
            enable = False
        else:
            enable = True
            
        return enable
    
    
    
    
    
class VIEWPixx3D(DpxDevice, DualLinkOut, ScanningBackLight, VideoFeatures, ThreeDFeatures):    
    """ Class Definition for the VIEWPixx3D Device.
    
    Note: If you have a **Lite** version of the device, some of these handles will 
    not be available. The usage of the handles is as follow:
    
    >>> from pypixxlib.viewpixx import VIEWPixx3D
    >>> my_device = VIEWPixx3D()
    >>> my_device.adc.function() # adc is the subsystem in this example.
    >>> my_device.BaseFunction() # A base function from one of the class' bases.
    
    Attributes:
        name: Name of the device.
        adc: Handle for the control of Analog In signal. See :doc:`analogIn`.
        dac: Handle for the control of Analog Out signal. See :doc:`analogOut`.
        audio: Handle for the audio controls. See :doc:`audioOut`.
        micro: Handle for the microphone controls. See :doc:`audioIn`.
        din: Handle for the control of Digital In signal. See :doc:`digitalIn`.
        dout: Handle for the control of Digital Out signal. See :doc:`digitalOut`.
        subsytems: A list of the available subsystems related to your physical device.
    """   
    def __init__(self):
        super(VIEWPixx3D, self).__init__('VIEWPixx3D')
        
        self.number_of_line = 1080
        self.devsel = 20
        
        if 'Lite' in self.name:
            self._setLiteSubSystems()
        else:
            self._setFullSubSystems()
                
 
    def _setLiteSubSystems(self):
        
        self.din = DigitalIn()
        self.dout = DigitalOut()
        
        self.subsystems = ['General','Digital I/O']
        
    def _setFullSubSystems(self):
        
        self.adc = AnalogIn()
        self.dac = AnalogOut()
        self.audio = AudioOut()
        self.micro = AudioIn()
        self.din = DigitalIn()
        self.dout = DigitalOut()
        
        self.subsystems = ['General','Analog I/O', 'Audio I/O', 'Digital I/O']
        
    def setPixelPolarityInversion(self, enable):
        """Sets the 3D pixel polarity inversion.
        
        Liquid crystal displays can exhibit an artifact when presenting 2 static images on alternating video frames,
        such as with frame-sequential 3D. The origin of this artifact is related to LCD pixel polarity inversion.
        The optical transmission of a liquid crystal cell varies with the magnitude of the voltage applied to the cell.
        Liquid crystal cells are designed to be driven by an AC voltage with little or no DC component.
        As such, the cell drivers alternate the polarity of the cell's driving voltage on alternate video frames.
        The cell will see no net DC driving voltage, as long as the pixel is programmed to the same intensity on even and odd video frames.
        Small differences in a pixel's even and odd frame luminance tend to leave the cell unaffected,
        and large differences in even and odd frame luminance for short periods of time (10-20 frames?) also do not seem to affect the cell;
        however, large differences in luminance for a longer period of time will cause a DC buildup in the pixel's liquid crystal cell.
        This can result in the pixel not showing the programmed luminance correctly, and can also cause the
        pixel to "stick" for several seconds after the image has been removed, causing an after-image on the display.
        VPixx Technologies has developed a strategy for keeping the pixel cells DC balanced.
        Instead of alternating the cell driving voltage on every video frame, we can alternate the voltage
        only on every second frame. This feature is enabled by calling the routine DPxEnableVidLcd3D60Hz().
        Call this routine before presenting static or slowly-moving 3D images, or when presenting 60Hz flickering stimuli.
        Be sure to call DPxDisableVidLcd3D60Hz() afterwards to return to normal pixel driving.
        Note that this feature is only supported on the VIEWPixx/3D when running with a refresh rate of 120Hz.

        Args:
            enable (Bool): True to enable the pixel polarity inversion, False to disable it.
            
        See Also:
            :class:`isPixelPolarityInversionEnabled`

        """
        if enable is True:
            DPxEnableVidLcd3D60Hz()
        else:
            DPxDisableVidLcd3D60Hz()
            
            
    def isPixelPolarityInversionEnabled(self):
        """Verifies that 3D pixel polarity inversion is enabled.
    
            Returns:
                Bool: True if the pixel polarity inversion is enabled, False otherwise.
                
            See Also:
                :class:`setPixelPolarityInversion`
            
            """
        if DPxIsVidLcd3D60Hz() == 0:
            enable = False
        else:
            enable = True
            
        return enable
    
    

    
         
class VIEWPixxEEG(DpxDevice, ScanningBackLight, VideoFeatures):    
    """ Class Definition for the VIEWPixxEEG Device.
    
    >>> from pypixxlib.viewpixx import VIEWPixxEEG
    >>> my_device = VIEWPixxEEG()
    >>> my_device.BaseFunction() # A base function from one of the class' bases.
    
    """   
    def __init__(self):
        super(VIEWPixxEEG, self).__init__('VIEWPixxEEG')
        
        self.number_of_line = 1080
        self.devsel = 20
        self.subsystems = ['General']
        
        
        
        
