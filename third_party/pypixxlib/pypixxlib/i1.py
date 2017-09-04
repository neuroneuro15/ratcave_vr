from _libione import getNumberOfI1Display, \
    geti1DisplayHandle, openI1DisplayDevice, closeI1Display, \
    getI1DisplayInfo, setI1DisplayRessourcesFilesPath, \
    setI1DisplayTechnologyStringFilesPath, \
    isI1DisplayDiffuserOn, setI1DisplayIntegrationTime, \
    getI1ProSpectrum, getI1ProTriStimulus, getI1DisplayMesure, \
    getI1ProHandle, getI1ProDeviceCount, openI1ProDevice, closeI1ProDevice, \
    getI1ProConnectionStatus, setI1ProAmbientLightMeasurementMode, \
    setI1ProEmissionSpotMeasurementMode, getI1ProMeasurementMode, \
    setI1ProIlluminationMode, getI1ProIlluminationMode, \
    setI1ProAdaptativMeasurementMode, getI1ProHardwareRevision, \
    setI1ProColorSpaceMode, getI1ProColorSpaceMode, getI1ProDeviceType, \
    getI1ProTimeUntilCalibrationExpire, getI1ProSerialNumber, calibrateI1Pro, \
    initializeI1Display, triggerI1ProMeasurement, getI1DisplayCalibrationList, \
    getI1DisplayCurrentCalibration, setI1DisplayCalibration, init1DisplayCalibrationListData, \
    getI1DisplayIntegrationTime, waitForButtonPress
import os
import time


class I1Display(object):    
    """Class Definition for the i1Display device.
    
    Attributes:
        measurement: Measurements taken by the i1Display.
        
    >>> from pypixxlib.i1 import I1Display
    >>> my_device = I1Display()
    >>> my_device.function()
    """     
    def __init__(self):
        
        self.ambiant = 0
        self.measurement = []
        self._raw = True
        self._device = 'VP3D'
        self._open_error = 0
        self._calibration_list = None
        
        initializeI1Display()
        number_of_i1display = getNumberOfI1Display()
                     
        if number_of_i1display == 1:
            self.handle_i1Display = geti1DisplayHandle()
            self._open()
             
        elif number_of_i1display > 1:
            print'Please select one device to use.'
            
        else:
            Open_Error = "Failed to find a device. Please connect an i1Display."
            raise Exception(Open_Error)
        
        
        
    def _setRawAcquitionMode(self, mode = False):
        self._raw = mode 
          
          
    def _open(self):
        self.open_status =  openI1DisplayDevice()
        if self.open_status != "success":
            self._open_error = self._open_error + 1
            self.close()
            time.sleep(1)
            
            if self._open_error > 2:
                Open_Error = "Failed to open device. Please disconnect and reconnect the device. Error: "
                raise Exception(Open_Error)
            else:
                self._open()
            
        else:
            self._open_error = 0
            info = getI1DisplayInfo()
            self.firmware_date = info['Firmware Date']
            self.firmware_revision = info['Firmware Version']
            self.device_name = info['Product Name']
            self._setI1DisplayRessourcesPath()
            self.setIntegrationTime()
            init1DisplayCalibrationListData()
            self._calibration_list = getI1DisplayCalibrationList()
            
            
            
    def close(self):
        """Releases the handle on the current I1Display device.
        
        This method should be the last call made on a I1Display object.        
        """
        closeI1Display()
        
        
        
        
        
    def getCurrentCalibration(self):
        """Sets the i1Display calibration mode.

        This method allows the user to set the calibration mode of the i1Display. The calibration mode should be chosen 
        based on the display that the i1Display will be measuring.
        
        Returns:
            mode (string): Calibration is one of the following predefined constants: \n
                - **CCFL**: Calibration used for displays with CCFL backlights.
                - **WHITE LED**: Calibration used for displays with white LED backlights.
                - **RGB LED**: Calibration used for displays with RGB LED backlights.
                - **CRT**: Calibration used for CRT.
                - **PROJECTOR**: Calibration used for projectors.
                - **VPIXX**: Calibration used for VIEWPixx and VIEWPixx /3D displays and PROPixx projectors.
                - **EEG**: Calibration used for VIEWPixx /EEG displays.
        
        See Also:
        :class:`getCurrentCalibration`
        """   
        return getI1DisplayCurrentCalibration(self._calibration_list)
        
        
    def setCurrentCalibration(self, calibration):
        """Sets the i1Display calibration mode.

        This method allows the user to set the calibration mode of the i1Display. The calibration mode should be chosen 
        based on the display that the i1Display will be measuring. The default value is RGB LED. When using a VPixx device,
        the default value should be kept.
        
        Args:
            mode (string): Calibration is one of the following predefined constants: \n
                - **CCFL**: Calibration used for displays with CCFL backlights.
                - **WHITE LED**: Calibration used for displays with white LED backlights.
                - **RGB LED**: Calibration used for displays with RGB LED backlights.
                - **CRT**: Calibration used for CRT.
                - **PROJECTOR**: Calibration used for projectors.
                - **VPIXX**: Calibration used for VIEWPixx and VIEWPixx /3D displays and PROPixx projectors.
                - **EEG**: Calibration used for VIEWPixx /EEG displays.
        
        See Also:
        :class:`getCurrentCalibration`
        """
        setI1DisplayCalibration(calibration)
        
        
            
    def _setI1DisplayRessourcesPath(self):
        path = os.path.dirname(os.path.realpath(__file__))
        files_path = os.path.abspath(path + "/i1d3Files/")
        
        if os.path.exists(files_path):
            setI1DisplayRessourcesFilesPath(files_path)
            setI1DisplayTechnologyStringFilesPath(files_path + "TechnologyStrings.txt")
        else:
            print'Could not find X-Rite Calibration files.'
        
        
    def setIntegrationTime(self, time = 1.0):
        """Sets the integration time for the i1Display.

        This method allows the user to change the time taken by the i1Display to take measurements.

        Args:
            time (float): Any value greater than 0.0. 
        
        """
        setI1DisplayIntegrationTime(time)
        
        
    def getIntegrationTime(self):
        """Gets the integration time used by the i1Display.

        This method allows the user to know the current integration time used by the i1Display to take measurements.
        
        Returns:
            time (float): Any value greater than 0.0. 
        
        """
        return getI1DisplayIntegrationTime()
        
        
    def runMeasurement(self):
        """Triggers an acquisition on the i1Display.
        
        This method triggers an acquisition on the I1Dsiplay. Since the measurement is affected by the position of
        the diffuser, the method verifies if the diffuser is located in front of the I1Dsiplay detector. Once the 
        acquisition is done, it is added to the measurement list.
        """ 
        if isI1DisplayDiffuserOn():
            print'Please remove diffuser for normal measurement\n'
        else:
            self.measurement.append(getI1DisplayMesure(self.ambiant, self._raw, self._device))
            
            
    def getFirmwareRevision(self):
        """Gets the i1Display firmware revision.
        
        Returns:
            revision (string): Firmware revision.
        
        """     
        return self.firmware_revision
    
    
    def getFirmwareDate(self):
        """Gets the i1Display firmware date.
        
        Returns:
            revision (string): Firmware date.
        
        """   
        return self.firmware_date
    
            
    def getLatestMeasurement(self):
        """Gets the latest measurements taken by the i1Display.
        
        All measurements are kept in a list. This method returns the last item from that list, which is a dictionary.
        Using the ``chrominance`` key, gives the ``x`` and ``y`` coordinates of the measurement on the chromaticity chart. Using the 
        ``luminance`` key gives the luminance value of the measurement.
        
        Returns:
            measurements (dict):
                - **chrominance**: Tuple of floating points coordinates. Ranges from 0 to 1.
                - **luminance**: floating point value in cd/m^2.
            
        See Also:
        :class:`getAllMeasurement`, :class:`printLatestMeasurement`
        
        """        
        return self.measurement[len(self.measurement)-1]
    
    
    def printLatestMeasurement(self):
        """Displays the latest measurements taken by the i1Display.
        
        This method allows the user to display on the monitor the last measurement taken by the I1Display.
        
        Returns:
            measurements (string): Chrominance coordinates and luminance with 4 decimal points.
            
        See Also:
        :class:`getAllMeasurement`, :class:`getLatestMeasurement`
        
        """  
        
        if (len(self.measurement) == 0):
            x = 0
            y = 0
            L = 0
            
        else:
            data = self.measurement[len(self.measurement)-1]
            x = data['chrominance'][0]
            y = data['chrominance'][1]
            L = data['luminance']
        
        print"(x,y) = ({0:.4f}, {1:.4f}), L = {2:.4f} cd/m2 ({3:.4f} fL)".format( x, y, L, 0.291863508*L)
        
    
    
    def getAllMeasurement(self):
        """Gets all the measurements taken by the i1Display.
        
        This method returns a list which contains all measurements taken since the creation of the I1Display object.
        Each item in the list is a dictionary with both chromaticity coordinates and luminance. 
        
        Returns:
            measurements (list): All measurements taken by the I1Display.
            
        See Also:
        :class:`getAllMeasurement`, :class:`printLatestMeasurement`
        
        """  
        return self.measurement
        
        
    def isDiffuserOn(self):
        """Verifies if the i1Display's diffuser is currently placed in front of the detector.

        Returns:
            state (Bool): True if the diffuser is in front of the detector, otherwise False.
        
        """
        return isI1DisplayDiffuserOn()

    
    



class I1Pro(object):    
    """Class Definition for the i1Pro device.
    
    Attributes:
        spectrum: Spectrum measurements taken by the i1Pro.
        tristimulus: Tristimulus measurements taken by the i1Pro.
        revision: Revision of the current i1Pro.
        serial_number: Serial number of the current i1Pro.
        
    >>> from pypixxlib.i1 import I1Pro()
    >>> my_device = I1Pro()
    >>> my_device.function()
    """   
    def __init__(self):
    
        self._device_type = None
        self.spectrum = []
        self.tristimulus = []
        self._open_error = 0
        
        self.i1_pro_handle = getI1ProHandle()
        
        if getI1ProDeviceCount() > 1:
            print"Warning, "+ str(self.number_of_i1pro)+" I1Pro detected. Only 1 I1Pro can be used."
      
        self._open()
             
             
    def _open(self):
        self.open_status =  openI1ProDevice()
        
        if self.open_status != "success":
            self._open_error = self._open_error + 1
            self.close()
            time.sleep(1)
            
            if self._open_error > 2:
                # we can try this a few times and then throw the error.
                Open_Error = "Failed to open device. Please disconnect and reconnect the device. Error: "+ self.getConnectionStatus()
                raise Exception(Open_Error)
            else:
                self._open()
            
        else:
            self._open_error = 0
            self._device_type = getI1ProDeviceType()
            self.revision = getI1ProHardwareRevision()
            self.serial_number = getI1ProSerialNumber()   
        
    
        
    def close(self):
        """Releases the handle on the current i1Pro device.
        
        This methods closes the i1Pro and should be the last call made on a I1Pro object.        
        """
        closeI1ProDevice()
        
        
    def setMeasurementMode(self, mode, adaptative=False):
        """Sets the measurement mode on the i1Pro.

        This method allows the user to change the measurement mode of the i1Pro. The mode should be chosen based on the
        light source.
        
        Args:
            mode (string): measurement mode is one of the following predefined constants: \n
                - **Emission**: Mode for an emission measurement on an emitting probe like a display.
                - **Ambiant**: Mode for an ambient light measurement.
                
            adaptative (Bool): When this mode is ``True``, a trial measurement is done first to get the best measurement result.
                When it is ``False``, the measurement duration is lower, but the results precision is also lower.
        
        See Also:
        :class:`getMeasurementMode`
        """
        if mode == 'Emission':
            setI1ProEmissionSpotMeasurementMode()
        else:
            setI1ProAmbientLightMeasurementMode()
            
        setI1ProAdaptativMeasurementMode(adaptative)
            
            
    def getMeasurementMode(self):
        """Gets the current measurement mode on the i1Pro.

        This method allows the user to know what is the current measurement mode on the i1Pro.
        
        Returns:
            mode (string): measurement mode is one of the following predefined constants: \n
                - **Emission**: Mode for an emission measurement on an emitting probe like a display.
                - **Ambiant**: Mode for an ambient light measurement.
                
        See Also:
        :class:`setMeasurementMode`        
        """ 
        return getI1ProMeasurementMode()
        
        
    def setColorSpace(self, mode):
        """Sets the color space mode for the i1Pro.

        This method allows the user to change the color space mode used during measurements. The mode should be chosen based on the
        light the source.
        
        Args:
            mode (string): measurement mode is one of the following predefined constants: \n
                - **CIELab**: Mode for an emission measurement on an emitting probe like a display.
                - **CIELCh**: Mode for an ambient light measurement.
                - **CIELuv**:
                - **CIELChuv**:
                - **CIEuvY1960**:
                - **CIEuvY1976**:
                - **CIEXYZ**:
                - **CIExyY**:
                
        See Also:
        :class:`getColorSpace`               
        """
        setI1ProColorSpaceMode(mode)
        
        
    def getColorSpace(self):
        """Gets the current color space mode for the i1Pro.

        This method allows the user to know what is the current color space mode on the i1Pro.
        
        Returns:
            mode (string): measurement mode is one of the following predefined constants: \n
                - **CIELab**: Mode for an emission measurement on an emitting probe like a display.
                - **CIELCh**: Mode for an ambient light measurement.
                - **CIELuv**:
                - **CIELChuv**:
                - **CIEuvY1960**:
                - **CIEuvY1976**:
                - **CIEXYZ**:
                - **CIExyY**:
                
        See Also:
        :class:`setColorSpace`
        
        """
        return getI1ProColorSpaceMode()
    
    
    def setIlluminationMode(self, mode='Emission'):
        """Sets the illumination mode the i1Pro.

        This method allows the user to change the illumination mode used during measurements.
        
        Args:
            mode (string): mode is one of the following predefined constants: \n
                - **A**
                - **B**
                - **C**
                - **D50**
                - **D55**
                - **D65**
                - **D75**
                - **F2**
                - **F7**
                - **F11**
                - **Emission**           
        """
        setI1ProIlluminationMode(mode)
        
        
    def getIlluminationMode(self):
        """Gets the current color illumination mode on the i1Pro.

        This method allows the user to know what is the current illumination mode on the i1Pro.
        
        Returns:
            mode (string): mode is one of the following predefined constants: \n
                - **A**
                - **B**
                - **C**
                - **D50**
                - **D55**
                - **D65**
                - **D75**
                - **F2**
                - **F7**
                - **F11**
                - **Emission**  
        
        """
        return getI1ProIlluminationMode()
    
        
    def getConnectionStatus(self):
        """Gets the current connection status on the i1Pro.

        This method allows the user to know what is the current connection status on the i1Pro.
        When an error occurs, this method will give the user an error code which indicates what the problem is.
        
        Returns:
            mode (string): Connection status.        
        """   
        return getI1ProConnectionStatus()
        
        
    def isCalibrationExpired(self):
        """Verifies if the calibration on the i1Pro has expired.
        
        In order to get precise results, the i1Pro needs to be calibrated frequently. This method allows the user to know if the 
        calibration needs to be done. It should be noted that a calibration is required before each use of the device.
                
        Returns:
            state (Bool): True if the calibration has expired, otherwise False.
        
        """
        return (getI1ProTimeUntilCalibrationExpire() < 200)
        
        
    def getTimeUntilCalibrationExpire(self):
        """Gets the time left until the calibration on the i1Pro expires.

        This method allows the user to know how much time is left until a calibration needs to be performed on the i1Pro.
        When an error occurs, this method will give the user an error code which indicates what the problem is.
        
        Returns:
            time (int): Time is a value greater than -1. When -1 is returned, it indicates that the time has expired.
        """  
        return getI1ProTimeUntilCalibrationExpire()
        
            
    def calibrate(self, measure_mode):
        """ Calibrates the i1Pro.
        
        This method allows the user to calibrate the i1Pro. It should be noted that when a calibration is done, 
        it is done for a specific 'measurement mode'. The required measurement mode must be specified.
        
        Args:
            measure_mode (string): mode is one of the following predefined constants: \n
                - **Emission**: Mode for an emission measurement on an emitting probe like a display.
                - **Ambiant**: Mode for an ambient light measurement.
            
        """
        self.setMeasurementMode(measure_mode)
        calibrateI1Pro()
        
        
    def waitForButtonPress(self):
        waitForButtonPress()
        
            
    def setModes(self, measurement = 'Ambiant', color_space = 'CIExyY', illumination = 'Emission'):
        """Sets the measurement, color space and illumination mode on the i1Pro.

        This method allows the user to set the three i1Pro modes in a single method call.
        
        Args:
            measurement (string): One of the following predefined constants: \n
                - **Emission**: Mode for an emission measurement on an emitting probe like a display.
                - **Ambiant**: Mode for an ambient light measurement.
            
            color_space (string): One of the following predefined constants: \n
                - **CIELab**: Mode for an emission measurement on an emitting probe like a display.
                - **CIELCh**: Mode for an ambient light measurement.
                - **CIELuv**:
                - **CIELChuv**:
                - **CIEuvY1960**:
                - **CIEuvY1976**:
                - **CIEXYZ**:
                - **CIExyY**:
                    
            illumination (string): One of the following predefined constants: \n
                - **A**
                - **B**
                - **C**
                - **D50**
                - **D55**
                - **D65**
                - **D75**
                - **F2**
                - **F7**
                - **F11**
                - **Emission**
                
        See Also:
        :class:`setMeasurementMode`, :class:`setColorSpace`, :class:`setIlluminationMode`, 
        :class:`getMeasurementMode`, :class:`getColorSpace`, :class:`getIlluminationMode`,  
        """
        self.setMeasurementMode(measurement)
        self.setColorSpace(color_space)      
        self.setIlluminationMode(illumination)
        
        
    def getLatestTriStimulusMeasurements(self):
        """Gets the latest triStimulus measurements taken by the i1Pro.
        
        All measurements are kept in a list. This method returns the last item from that list.
        
        Returns:
            measurements (list): Latest spectrum measurement taken by he i1Pro.
            
        See Also:
        :class:`getAllSpectrumMeasurements`
        
        """        
        return self.tristimulus[len(self.tristimulus)-1]
    
        
    def getAllTriStimulus(self):
        """Gets all the triStimulus measurements taken by the i1Pro.
        
        This method returns a list which contains all triStimulus values taken since the creation of the i1Pro object. 
        
        Returns:
            spectrum (list): All triStimulus measurements taken by the i1Pro.
            
        See Also:
        :class:`getLatestTriStimulus`
        
        """
        return self.tristimulus
    
    
    def getLatestSpectrumMeasurements(self):
        """Gets the latest spectrum measurements taken by the i1Pro.
        
        All measurements are kept in a list. This method returns the last item from that list.
        
        Returns:
            measurements (list): Latest spectrum measurement taken by he i1Pro.
            
        See Also:
        :class:`getAllSpectrumMeasurements`
        
        """        
        return self.spectrum[len(self.spectrum)-1]
    
    
    def getAllSpectrumMeasurements(self):
        """Gets all the spectrum measurements taken by the i1Pro.
        
        This method returns a list which contains all spectrum values taken since the creation of the i1Pro object. 
        
        Returns:
            spectrum (list): All spectrum measurements taken by the i1Pro.
            
        See Also:
        :class:`getLatestSpectrum`, :class:`getAllTriStimulus`
        
        """ 
        return self.spectrum


    def printLatestMeasurement(self):
        """Displays the latest measurements taken by the i1Pro.
        
        This method allows the user to display on the monitor the last measurement taken by the I1Pro.
        
        Returns:
            measurements (string): Chrominance coordinates and luminance with 4 decimal points.
            
        See Also:
        :class:`getAllTriStimulus`, :class:`getLatestSpectrumMeasurements`
        
        """  
        data = self.tristimulus[len(self.tristimulus)-1]
        x = data[0]
        y = data[1]
        L = data[2]
        print"(x,y) = ({0:.4f}, {1:.4f}), L = {2:.4f} cd/m2 ({3:.4f} fL)".format( x, y, L, 0.291863508*L)
         
            
    def runMeasurement(self):
        """Triggers an acquisition on the i1Pro.
        
        This method triggers an acquisition on the i1Pro.  Once the acquisition is done, it is added to the measurement list.
        """
        triggerI1ProMeasurement()
        self.spectrum.append(getI1ProSpectrum())
        self.tristimulus.append(getI1ProTriStimulus())