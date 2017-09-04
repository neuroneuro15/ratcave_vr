from _libdpx import DPxUpdateRegCache, DPxSelectDevice, DPxGetID, \
    DPxGetPartNumber, DPxGetFirmwareRev, DPxGetRamSize, DPxIsRamOffline, \
    DPxSetVidSource, DPxGetVidSource, DPxGetVidLine, DPxOpen, DPxClose, \
    DPxIsReady, DPxReadRam, DPxWriteRam, DPxGetTime, DPxGetTemp2Celcius, \
    DPxGetTempCelcius, DPxGetSupplyCurrent, DPxGetSupply2Current, DPxGetTemp3Celcius, \
    DPxGetSupplyVoltage, DPxGetSupply2Voltage, part_number_constants, \
    DPxReadProductionInfo, DPxGetVidHActive, DPxGetVidVActive, \
    DPxIsVidDviActiveDual, DPxIsVidDviActive, DPxSetCustomStartupConfig, \
    DPxGetError, DPxClearError, DPxWriteRegCache
from abc import ABCMeta, abstractmethod


class DpxDevice(object):
    """Implements the features common for all Devices.

    Attributes:
        identification: Number which identifies the type of device.
        part_number: Part number of the device.
        firmware_revision: Firmware revision of the device.
        ram_size: The size of the Ram found on the device.   
    
    """
    __metaclass__ = ABCMeta  
    def __init__(self, device_type):
        
        DPxOpen()
        if DPxGetError() != 'DPX_SUCCESS':
            DPxClearError()
            DPxDeviceError = "No device found. Please make sure that the device is connected to the computer and powered on."
            raise Exception(DPxDeviceError)
        else:
            DPxSelectDevice(device_type)
            production_info = DPxReadProductionInfo()
            
            self.identification = production_info['Part Number']
            self.serial_number = production_info['S/N']
            self.name = part_number_constants[ DPxGetPartNumber()] 
            self.nick_name = part_number_constants[ DPxGetPartNumber()]
            self.firmware_revision = str( DPxGetFirmwareRev() )
            self.ram_size = str(DPxGetRamSize()/1048576)+" MB"
            self.assembly_revision = production_info['Assembly REV']
            self.date_shipped = production_info['Shipping Date']
            self.expiration_date = production_info['Expiration Date']
            self.id_number = DPxGetID()
            
            self.device_type = device_type
            self.subsystems = []
            self.active = True



    def _updateInformation(self):
        DPxSelectDevice(self.device_type)
        production_info = DPxReadProductionInfo()
        self.identification = production_info['Part Number']
        self.serial_number = production_info['S/N']
        self.name = part_number_constants[ DPxGetPartNumber()] 
        self.nick_name = part_number_constants[ DPxGetPartNumber()]
        self.firmware_revision = str( DPxGetFirmwareRev() )
        self.ram_size = str(DPxGetRamSize()/1048576)+" MB"
        self.assembly_revision = production_info['Assembly REV']
        self.date_shipped = production_info['Shipping Date']
        self.expiration_date = production_info['Expiration Date']        
        
        
        
    def getAvailableSubSystem(self):
        """Gets the available subsystems for the device.

        Returns:
            List: Name of subsystems found on the device.

        """
        return self.subsystems
    
    
    
    def setActive(self):
        if DPxSelectDevice(self.device_type):
            self.active = True
        else:
            self.active = False
    
    
    
    def isActive(self):
        return self.active
    
    
    
    def open(self):
        """Opens a VPixx device.

        This method is used to get a handle on a VPixx device.

        """
        DPxOpen()



    def close(self):
        """Closes a VPixx device.

        This method is used to release a handle on a VPixx device.

        """
        DPxClose()        
        
        
            
    def isReady(self):
        """Verifies if s device has been properly opened.
        """
        return DPxIsReady()
        
        
        
    def readRam(self, address, int_list):
        """Reads a block of VPixx RAM into a local buffer.
    
        Args:
            address (int): Any even value equal or greater to 0.
            length (int): Any of value from 0 to RAM size.
        """
        return DPxReadRam(address, int_list)
        
        

    def writeRam(self, address, int_list):
        """Writes a local buffer into VPixx RAM.
    
        Args:
            address (int): Any even value equal or greater to 0.
            int_list (int): int_list is a list which will fill with RAM data. The length of RAM used is based on the
                length of int_list. It can't be bigger than RAM size.
        """
        DPxWriteRam(address, int_list)
        
        
                
    def updateRegisterCache(self):
        """Updates the registers and local register cache.
        """
        DPxSelectDevice(self.device_type)
        DPxUpdateRegCache()
        
        

    def writeRegisterCache(self):
        """Writes the registers with local register cache.
        """
        DPxSelectDevice(self.device_type)
        DPxWriteRegCache()
        
                        
    def setVideoSource(self, vidSource):
        """Set source of video to be displayed
    
        Args:
            vidSource (str): The source we want to display. \n
                - **DVI**: Monitor displays DVI signal.
                - **SWTP**: Software test pattern showing image from RAM.
                - **SWTP 3D**: 3D Software test pattern flipping between left/right eye images from RAM.
                - **RGB SQUARES**: RGB ramps.
                - **GRAY**: Uniform gray display having 12-bit intensity.
                - **BAR**: Drifting bar.
                - **BAR2**: Drifting bar.
                - **DOTS**: Drifting dots.
                - **RAMP**: Drifting ramp, with dots advancing x*2 pixels per video frame, where x is a 4-bit signed.
                - **RGB**: Uniform display with 8-bit intensity nn, send to RGBA channels enabled by mask m.
                - **PROJ**: Projector Hardware test pattern.
        """
        DPxSetVidSource(vidSource)
        
        
        
    def getVideoSource(self):
        """Get source of video pattern being displayed.

        Returns:
            int: Source of video pattern.
        """
        return DPxGetVidSource()        

    

    def getVideoLine(self):
        """
        Reads pixels from the VPixx device line buffer, and returns a list containing the data. 
        For each pixel, the buffer contains 16 bit R/G/B/U (where U is thrown away). The returned data is a list
        containing three lists for the respective R/G/B colors.
        
        Return:
            lists of list: A list which has [[RED], [GREEN], [BLUE]]
        """
        return DPxGetVidLine()
    
    
    
    def getTime(self):
        """Gets the device time since power up.

        Returns:
            float: Time in seconds.
        
        """
        DPxUpdateRegCache()
        return DPxGetTime()
    
    
    
    def getFrameTemperature(self):
        """Gets the temperature from the device chassis.

        Returns:
            float: Temperature in Celsius.
        
        """
        return DPxGetTempCelcius()
    
    
    
    def getFrameTemperature2(self):
        """Gets the temperature from the device chassis.
        
        Returns:
            float: Temperature in Celsius.
        
        """
        return DPxGetTemp2Celcius()  
            


    def getCoreTemperature(self):
        """Gets the core temperature from the device.

        Returns:
            float: Temperature in Celsius.
        
        """
        return DPxGetTemp3Celcius()
    
    
    
    def get5vCurrent(self):
        """Gets the current for the 5 volt Power supply.

        Returns:
            float: Temperature in Celsius.
        
        """
        return DPxGetSupplyCurrent()
    
    
    
    def get12vCurrent(self):
        """Gets the current for the 12 volt Power supply.

        Returns:
            float: Temperature in Celsius.
        
        """
        return DPxGetSupply2Current()

    
    
    
    def get5vVoltage(self):
        """Gets the voltage for the 5 volt Power supply.

        Returns:
            float: Temperature in Celsius.
        
        """
        return DPxGetSupplyVoltage()
    
    
    
    def get12vVoltage(self):
        """Gets the current for the 12 volt Power supply.

        Returns:
            float: Temperature in Celsius.
        
        """
        return DPxGetSupply2Voltage()

    
    
    
    def get5vPower(self):
        """Gets the current for the 5 volt Power supply.        
        
        Returns:
            float: power in watts.
        
        """
        return ( DPxGetSupplyVoltage() * DPxGetSupplyCurrent() )
    
    
    
    def get12vPower(self):
        """Gets the power for the 12 volt Power supply.        
        
        Returns:
            float: Power in watts.
        
        """
        return ( DPxGetSupply2Voltage() * DPxGetSupply2Current() )
    
    
    
    def getDisplayResolution(self):
        """Gets the resolution of the device.        
        
        Returns:
            string: Horizontal resolution followed by vertical resolution.
        
        """
        return str(DPxGetVidHActive()) +' x '+ str(DPxGetVidVActive())
    
    
    def getMonitorCableLink(self):
        """Gets the monitor cable link.
        
        This method allows the user to know what kind of cable link is
        detected by the VPixx device.        
        
        Returns:
            string: Any of the following predefined constants.\n
            - **DVI-Single Link**.
            - **DVI-Dual Link**.
        
        """
        dual_link = DPxIsVidDviActiveDual()
        single_link = DPxIsVidDviActive()
        
        if dual_link:
            link = 'DVI-Dual Link'
        elif single_link and not(dual_link):
            link = 'DVI-Single Link'
        elif not(single_link) and not(dual_link):
            link = 'Not Recognized'
            
        return link
    
    
    def setCustomStartupConfig(self):
        """Save the current registers to be used on start up.
    
        This can be useful if you set your projector to Ceiling mode or Rear projection and you
        want to keep it as such on reboot.
        """
        return  DPxSetCustomStartupConfig()
    
    
    def getName(self):
        """Gets the device type.
        
        Returns:
            string: Device type.
        
        """
        return self.name
    
    
    def getAssemblyRevision(self):
        """Gets the device revision.
        
        Returns:
            string: The assembly revision of the device.
        
        """
        return self.assembly_revision
    
    
    def getRamSize(self):
        """Gets the RAM size.
        
        Returns:
            string: The amount of RAM found on the device.
        
        """
        return self.ram_size
    
    
    def getFirmwareRevision(self):
        """Gets the firmware revision.
        
        Returns:
            string: The firmware revision of the device.
        
        """
        return self.firmware_revision
    
    
    def getSerialNumber(self):
        """Gets the serial number.
        
        Returns:
            string: The serial number of the device.
        
        """
        return self.serial_number
    
    
    def getInfo(self):
        """Gets the device production information.
        
        This method can be used to get information about the current device. Some of these information are different from one device
        to another. It can be useful when contacting VPixx Technologies.
        
        Returns:
            info (dict): Any of the predefined constants.\n
            - **Part Number**: The part number of the device.
            - **Shipping Date**: The date at which the device was shipped.
            - **Assembly REV**: The device assembly revision.
            - **Expiration Date**: Date when the warranty expires.
            - **S/N**: Serial number of the device.
        
        """
        return DPxReadProductionInfo()