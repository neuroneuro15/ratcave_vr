from _libdpx import DPxSetPPxDlpSeqPgrm, DPxGetPPxDlpSeqPgrm, \
    DPxGetPPx3dCrosstalk, DPxSetPPx3dCrosstalk, \
    DPxUpdateRegCache, DPxSetVidMode, DPxGetVidMode, \
    DPxEnablePPxCeilingMount, DPxDisablePPxCeilingMount, DPxIsPPxCeilingMount, \
    DPxEnablePPxRearProjection, DPxDisablePPxRearProjection, \
    DPxIsPPxRearProjection, DPxGetPPxVoltageMonitor, DPxGetPPxTemperature, \
    DPxGetPPxLedCurrent, DPxGetPPxFanTachometer, DPxGetPPxFanPwm, \
    DPxIsPPxVidSeqEnabled, DPxEnableVidVesaFreeRun, DPxDisableVidVesaFreeRun, \
    DPxIsVidVesaFreeRun, DPxSelectDevice, api_constants, DPxDetectDevice, \
    DPxSetPPxSleep, DPxSetPPxAwake, DPxIsPPxAwake, DPxEnablePPxLampLed, \
    DPxDisablePPxLampLed, DPxIsPPxLampLedEnabled, DPxEnablePPxQuietFanMode, \
    DPxDisablePPxQuietFanMode, DPxIsPPxQuietFanMode, DPxWriteRegCache, \
    DPxSpiRead, DPxSetReg16, PPXREG_LED_DAC_RED_H, PPXREG_LED_DAC_GRN_H, \
    PPXREG_LED_DAC_BLU_H, SPI_ADDR_PPX_LEDMAXD65
from analogIn import AnalogIn
from analogOut import AnalogOut
from audioIn import AudioIn
from audioOut import AudioOut
import ctypes
from digitalIn import DigitalIn
from digitalOut import DigitalOut
from dpxDevice import DpxDevice
from dualLinkOut import DualLinkOut
from threeDFeatures import ThreeDFeatures
from videoFeatures import VideoFeatures


class PROPixx(DpxDevice, VideoFeatures):
    """ Class Definition for the PROPixx Device.
    
    .. Tip::
        If you want to use these functions, you must connect your PROPixx device with a USB
        cable. If you want to use the PROPixx Controller, see :class:`PROPixxCtrl`.
    
    >>> from pypixxlib.propixx import PROPixx
    >>> my_device = PROPixx()
    >>> my_device.function() # A PROPixx has no sub-systems, only function and bases.
    >>> my_device.BaseFunction() # A base function from one of the class' bases.
    """
    def __init__(self):
        super(PROPixx, self).__init__("PROPixx")

        self.devsel = 40
        self.name = "PROPixx"
        self.led_intensity = "100.0"
        self.subsystems = ['General']                     
                              
    def setCeilingMountMode(self, enable):
        """Sets the ceiling mount mode.
        
        This method allows the user to turn the ceiling mount mode on or off.
        When enabled, the image will be displayed up side down. This allows the user to
        install the PROPixx on the ceiling. when this mode is disabled, the image will
        be displayed normally.

        Args:
            enable (bool): Ceiling mount mode.
        """
        DPxSelectDevice('PROPIXX')
        if enable == True:
            DPxEnablePPxCeilingMount()
        else:
            DPxDisablePPxCeilingMount()
        DPxWriteRegCache()
        self._selectValidDevice()



    def isCeilingMountEnabled(self):
        """ Gets the ceiling mount mode state.

        Returns:
            bool: True if enabled, False if disabled.
        """
        DPxSelectDevice('PROPIXX')
        if DPxIsPPxCeilingMount() == 0:
            enable = False
        else:
            enable = True
        self._selectValidDevice()
        return enable       
    



    def setRearProjectionMode(self, enable):
        """Sets the rear projection mode.
        
        This method allows the user to turn the rear projection mode on or off.
        When enabled, the image will be displayed in mirrored view, allowing the user to
        install the PROPixx behind a projection screen.

        Args:
            enable (bool): rear projection mode.
        """
        DPxSelectDevice('PROPIXX')
        if enable == True:
            DPxEnablePPxRearProjection()
        else:
            DPxDisablePPxRearProjection()
        DPxWriteRegCache()
        self._selectValidDevice()



    def isRearProjectionEnabled(self):
        """ Gets the rear projection mode state.

        Returns:
            bool: True if enabled, False if disabled.
        """
        DPxSelectDevice('PROPIXX')
        if DPxIsPPxRearProjection() == 0:
            enable = False
        else:
            enable = True
        self._selectValidDevice()
        return enable
    
    

    def getVoltageMonitor(self, power_supply_type):
        """Gets the voltage for a given power supply.
        
        Args:
            power_supply_type (int): Power supply for which the voltage is queried. Valid arguments are the following: \n
                - PPX_POWER_5V, 
                - PPX_POWER_2P5V, 
                - PPX_POWER_1P8V, 
                - PPX_POWER_1P5V, 
                - PPX_POWER_1P1V, 
                - PPX_POWER_1V, 
                - PPX_POWER_12V, 
                - PPX_POWER_VCC
        
        Returns:
            voltage (float): voltage for a given power supply.
        """
        DPxSelectDevice('PROPIXX')
        voltage = DPxGetPPxVoltageMonitor(power_supply_type)
        self._selectValidDevice()
        return voltage
    
    

    def getTemperature(self, component_temperature):
        """Gets the temperature for a given power supply.
        
        Args:
            component_temperature (int): power supply for which the voltage is queried. A valid argument is one of the following: \n
                - PPX_TEMP_LED_RED, 
                - PPX_TEMP_LED_GRN,
                - PPX_TEMP_LED_BLU, 
                - PPX_TEMP_LED_ALT,
                - PPX_TEMP_DMD, 
                - PPX_TEMP_POWER_BOARD,
                - PPX_TEMP_LED_POWER_BOARD,
                - PPX_TEMP_RX_DVI,
                - PPX_TEMP_FPGA,
                - PPX_TEMP_FPGA2,
                - PPX_TEMP_VOLTAGE_MONITOR
                
        Returns:
            temperature (float): temperature for a given power supply.
        """
        DPxSelectDevice('PROPIXX')
        temp = DPxGetPPxTemperature(component_temperature)
        self._selectValidDevice()
        return temp
    
    

    def getLedCurrent(self, led_nbr):
        """Gets the current for a given LED.
        
        Args:
            led_nbr (int): number of the queried LED.
        
        Returns:
            current (float): current for a given LED.
        """
        DPxSelectDevice('PROPIXX')
        current = DPxGetPPxLedCurrent(led_nbr)
        self._selectValidDevice()
        return current
    
    

    def getFanSpeed(self, fan_nbr):
        """Gets the speed of one of the PROPixx fans.

        Args:
            fan_nbr (int): number of the queried fan.
            
        Returns:
            speed (float): current for a given fan.
        """
        DPxSelectDevice('PROPIXX')
        tach =  DPxGetPPxFanTachometer(fan_nbr)
        self._selectValidDevice()
        return tach
    
    

    def getFanPwm(self):
        """Gets the PROPixx PWM.
        
        Returns:
            pwm (float): PWM value.
        """
        DPxSelectDevice('PROPIXX')
        pwn = DPxGetPPxFanPwm()
        self._selectValidDevice()
        return pwn
    
    

    def isSequencerEnabled(self):
        """ Gets the sequencer mode state.
        
        Returns:
            bool: True if enabled, False if disabled.
        """
        DPxSelectDevice('PROPIXX')
        if DPxIsPPxVidSeqEnabled() == 0:
            enable = False
        else:
            enable = True
        self._selectValidDevice()
        return enable

        
        
    def setVesaFreeRun(self, enable):
        """Enables or disables the Vesa output to work with the polariser.
        
        Args:
            enable (bool): Set to true to enable VesaFreeRun.
        """
        DPxSelectDevice('PROPIXX')
        if enable is True:
            DPxEnableVidVesaFreeRun()
        else:
            DPxDisableVidVesaFreeRun()
        self._selectValidDevice()
    
    
    def isVesaFreeRun(self):
        """Returns non-0 if PROPixx VESA 3D output is enabled."""
        DPxSelectDevice('PROPIXX')
        if DPxIsVidVesaFreeRun() == 0:
            self._selectValidDevice()
            return False
        else:
            self._selectValidDevice()
            return True
        
        
    def setDlpSequencerProgram(self, program):
        """Sets the PROPixx DLP Sequencer program.
    
        Only available for PROPixx Revision 6 and higher.

        Args:
            program (string) : Any of the following predefined constants.\n
                - **RGB**: Default RGB
                - **RB3D**: R/B channels drive grayscale 3D
                - **RGB240**: Only show the frame for 1/2 a 120 Hz frame duration.
                - **RGB180**: Only show the frame for 2/3 of a 120 Hz frame duration.
                - **QUAD4X**: Display quadrants are projected at 4x refresh rate.
                - **QUAD12X**: Display quadrants are projected at 12x refresh rate with grayscales.
                - **GREY3X**: Converts 640x1080@360Hz RGB to 1920x1080@720Hz Grayscale with blank frames.
        """
        DPxSelectDevice('PROPIXX')
        DPxSetPPxDlpSeqPgrm(program)
        self._selectValidDevice()
        
        
    def getDlpSequencerProgram(self):
        """Get PROPixx DLP Sequencer program.
        
        This method allows the user to set the video mode of the PROPixx.
        
        Returns:
            String: Any of the following predefined constants.\n
                - **RGB**: Default RGB
                - **RB3D**: R/B channels drive grayscale 3D
                - **RGB240**: Only show the frame for 1/2 a 120 Hz frame duration.
                - **RGB180**: Only show the frame for 2/3 of a 120 Hz frame duration.
                - **QUAD4X**: Display quadrants are projected at 4x refresh rate.
                - **QUAD12X**: Display quadrants are projected at 12x refresh rate with grayscales.
                - **GREY3X**: Converts 640x1080@360Hz RGB to 1920x1080@720Hz Grayscale with blank frames.
        """
        DPxSelectDevice('PROPIXX')
        dlp = DPxGetPPxDlpSeqPgrm()
        self._selectValidDevice()
        return dlp
    
    
    def set3dCrosstalk(self, crosstalk):
        """Set 3D crosstalk (0-1) which should be subtracted from stereoscopic stimuli.
    
        Warning:
            This only works with RB3D mode and requires revision 6 of the PROPixx.
            
        Args:
            crosstalk (double): A value between 0 and 1 which represents the 3d crosstalk.
        """
        DPxSelectDevice('PROPIXX')
        DPxSetPPx3dCrosstalk(crosstalk)
        self._selectValidDevice()
        
        
    def get3dCrosstalk(self):
        """Get 3D crosstalk (0-1) which is being subtracted from stereoscopic stimuli
    
        Warning:
            This only works with RB3D mode and requires revision 6 of the PROPixx.
            
        Returns:
            A double value for the 3D Crosstalk.
        """
        DPxSelectDevice('PROPIXX')
        crosstalk = DPxGetPPx3dCrosstalk()
        self._selectValidDevice()
        return crosstalk
    

    def setLampLED(self, enable):
        """Enables or disables the lamp LED.
        
        Warning:
            This requires revision 12 of the PROPixx.
        
        Args:
            enable (bool): Set to true to enable the lamp LED.

        See Also:
            :class:`isLampLEDMode`
        """
        DPxSelectDevice('PROPIXX')
        if enable is True:
            DPxEnablePPxLampLed()
        else:
            DPxDisablePPxLampLed()
        DPxWriteRegCache()    
        self._selectValidDevice()
            
    
    def isLampLEDMode(self):
        """Returns non-0 if PROPixx lamp LED is enabled.
        
        Warning:
            This requires revision 12 of the PROPixx.

        See Also:
            :class:`setLampLED`
        """    
        DPxSelectDevice('PROPIXX')
        if DPxIsPPxLampLedEnabled() == 0:
            self._selectValidDevice()
            return False
        else:
            self._selectValidDevice()
            return True
        
        
    def setSleepMode(self, enable):
        """Enables or disables the sleep mode.
        
        Enabling this mode turns the PROPixx off. Disabling it will turn the PROPixx on.
        
        Warning:
            This requires revision 12 of the PROPixx.
        
        Args:
            enable (bool): Set to true to enable sleep mode.
            
        See Also:
            :class:`isSleepMode`
        """
        DPxSelectDevice('PROPIXX')
        if enable is True:
            DPxSetPPxSleep()
        else:
            DPxSetPPxAwake()
        DPxWriteRegCache()     
        self._selectValidDevice()
            
    
    def isSleepMode(self):
        """Returns True if PROPixx sleep mode is enabled.
        
        Warning:
            This requires revision 12 of the PROPixx.
            
        See Also:
            :class:`setSleepMode`
        """
        DPxSelectDevice('PROPIXX')
        if DPxIsPPxAwake() == 0:
            return True
        else:
            return False


    def setQuietMode(self, enable):
        """Enables or disables the quiet mode.
        
        Enabling this mode reduces the noise generated by the PROPixx by lowering the speed of 
        the fans. It should be kept enabled unless reducing the noise is essential.
        
        Warning:
            This requires revision 19 of the PROPixx.
        
        Args:
            enable (bool): Set to true to enable quiet mode.
            
        See Also:
            :class:`isQuietMode`
        """
        DPxSelectDevice('PROPIXX')
        if enable is True:
            DPxEnablePPxQuietFanMode()
        else:
            DPxDisablePPxQuietFanMode()
        DPxWriteRegCache()
        self._selectValidDevice()
            
    
    def isQuietMode(self):
        """Returns non-0 if PROPixx quiet mode is enabled.
        
        Warning:
            This requires revision 19 of the PROPixx.
            
        See Also:
            :class:`setQuietMode`
        """
        DPxSelectDevice('PROPIXX')
        if DPxIsPPxQuietFanMode() == 0:
            self._selectValidDevice()
            return False
        else:
            self._selectValidDevice()
            return True
                
    
    def getLedIntensity(self):
        return self.led_intensity
        
    def setLedIntensity(self, intensity):
        intensity_dict = {"100.0": 0, "50.0": 1, "25.0": 2, "12.5": 3, "6.25": 4}
        try:
            intensity_index = intensity_dict[intensity]
            DPxSelectDevice('PROPIXX')
        except:
            print"Wrong value for argument 'intensity'."
            return
            
        class PpxLedWhites(ctypes.Structure):
            _fields_ = [("ledCur", ctypes.c_int*4),
                        ("ledDutyCycle", ctypes.c_int*4),
                        ("targetL", ctypes.c_double),
                        ("errorL", ctypes.c_double),
                        ("errorX", ctypes.c_double),
                        ("errorY", ctypes.c_double)]
        
        ppxLedWhites = [PpxLedWhites() for i in range(8)]
        dataBuff = DPxSpiRead(SPI_ADDR_PPX_LEDMAXD65, 128) # Get the D65 white points
        if not(dataBuff):
            raise ValueError("ERROR: Could not read SPI")
    
        for iWhite in range(8):
            for iRgb in range(4):
                ppxLedWhites[iWhite].ledCur[iRgb]  = (dataBuff[iWhite*16+iRgb*2+0] << 8) + dataBuff[iWhite*16+iRgb*2+1]
                ppxLedWhites[iWhite].ledDutyCycle[iRgb] = (dataBuff[iWhite*16+iRgb*2+8] << 8) + dataBuff[iWhite*16+iRgb*2+9]
     
        DPxSetReg16(PPXREG_LED_DAC_RED_H, ppxLedWhites[intensity_index].ledCur[0])
        DPxSetReg16(PPXREG_LED_DAC_GRN_H, ppxLedWhites[intensity_index].ledCur[1])
        DPxSetReg16(PPXREG_LED_DAC_BLU_H, ppxLedWhites[intensity_index].ledCur[2])
        DPxUpdateRegCache()
        self.led_intensity = intensity
        
            
    def _selectValidDevice(self):
        if DPxDetectDevice('PROPIXX CTRL'):
            DPxSelectDevice('PROPIXX CTRL')
        else:
            DPxSelectDevice('PROPIXX')




class PROPixxCTRL(DpxDevice, DualLinkOut, VideoFeatures):    
    """Class Definition for the PROPixx Controller Device.

    .. Tip::
        If you want to use these functions, you must connect your PROPixx controller 
        device with a USB cable. If you want to use the PROPixx, see :class:`PROPixx`.
    
    >>> from pypixxlib.propixx import PROPixxCTRL    
    >>> my_device = PROPixxCTRL()
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
        super(PROPixxCTRL, self).__init__("PROPixxCTRL")
        
        self.devsel = 30
         
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