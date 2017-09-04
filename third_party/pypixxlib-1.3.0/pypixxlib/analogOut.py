from _libdpx import DPxUpdateRegCache, DPxGetDacNumChans, DPxSetDacValue, \
    DPxGetDacValue, DPxGetDacRange, DPxGetDacVoltage, DPxSetDacVoltage, \
    DPxEnableDacBuffChan, DPxDisableDacBuffChan, DPxIsDacBuffChan, \
    DPxEnableDacCalibRaw, DPxDisableDacCalibRaw, DPxIsDacCalibRaw, \
    DPxSetDacBuffBaseAddr, DPxGetDacBuffBaseAddr, DPxSetDacBuffReadAddr, \
    DPxGetDacBuffReadAddr, DPxSetDacBuffSize, DPxGetDacBuffSize, \
    DPxSetDacSchedOnset, DPxGetDacSchedOnset, DPxSetDacSchedRate, \
    DPxGetDacSchedRate, DPxSetDacSchedCount, DPxGetDacSchedCount, \
    DPxEnableDacSchedCountdown, DPxDisableDacSchedCountdown, \
    DPxIsDacSchedCountdown, DPxStartDacSched, DPxStopDacSched, \
    DPxIsDacSchedRunning, DPxDisableDacBuffAllChans
from abc import ABCMeta, abstractmethod
from schedule import Schedule



class AnalogOut(Schedule):
    """Class which implements the DAC features.

    It contains all the necessary methods to use the analog outputs of a VPixx device.
    """
    __metaclass__ = ABCMeta

    def getNbrOfChannel(self):
        """Gets the number of channels available.

        Returns:
            int:   Number of channels.

        """
        return DPxGetDacNumChans()
    
    
    
    def setChannelValue(self, value, channel):
        """Sets the current value of a channel.
        
        This method allows the user to modify the output value of a given channel. 

        Args:
            value (int): Value of the channel. It is a 16-bit 2's complement signed number.
            channel (int): Channel number.
            
        See Also:
            :class:`getChannelValue`

        """
        DPxSetDacValue(value, channel)
    
    
        
    def getChannelValue(self, channel):
        """Gets the current value of a channel.
        
        This method allows the user to know the value of a given channel. The return value is
        a 16-bit 2's complement signed number. Value can be obtained for channels 0 to 17.

        Returns:
            int: value of the channel.
            
        See Also:
            :class:`setChannelValue`

        """
        return DPxGetDacValue(channel)
        
        
        
    def getChannelRange(self, channel):
        """Gets the range of a channel.

        Returns:
            tuple: Range of the channel. The returned value is a tuple with the minimum range followed by the maximum range.
            Both values are integers.

        """
        return DPxGetDacRange(channel)



    def getChannelVoltage(self, channel):
        """Gets the current voltage of a channel.

        Returns:
            float: voltage of the channel.
            
        See Also:
            :class:`setChannelVoltage`

        """
        return DPxGetDacVoltage(channel)



    def setChannelVoltage(self, voltage, channel):
        """Sets the current Voltage of a channel.
        
        This method allows the user to modify the output voltage of a given channel.
        The voltage is +-10V for channels 0 and 1, and +-5V for channels 2 and 3.

        Args:
            voltage (float): Value of the channel.
            channel (int): Channel number.
            
        See Also:
            :class:`getChannelVoltage`

        """
        DPxSetDacVoltage(voltage, channel)    
        

 
    def setChannelRamBuffering(self, enable, channel=None):
        """Sets the ram buffering mode.
        
        This method allows the user to enable or disable ram buffering on a given channel.
        When enabled, a given channel is buffered in ram. Enabling RAM buffering can only
        be done for channels 0 to 15.

        Args:
            enable (Bool): True if hardware calibration is enabled, False otherwise.
            channel (int): Channel number to enable or disable. Passing None will set all channels. 
            
        See Also:
            :class:`isChannelRamBuffering`
        
        """
        all_channels = 16
        if enable == True:
            if channel == None:
                for i in range(all_channels):
                    DPxEnableDacBuffChan(i) 
            else:
                DPxEnableDacBuffChan(channel)
        else:
            if channel == None:
                DPxDisableDacBuffAllChans()
            else:
                DPxDisableDacBuffChan(channel) 
                                
                
                  
    def isChannelRamBuffering(self, channel):
        """Verifies the ram buffering mode.
        
        This method allows the user to know if a ram buffering is enabled for a given channel.
        
        Args:
            channel (int): Channel number to query.

        Returns:
            Bool: True if the given channel is buffered, False otherwise.
            
        See Also:
            :class:`setChannelRamBuffering`
        
        """
        if DPxIsDacBuffChan(channel) == 0:
            enable = False
        else:
            enable = True
            
        return enable 
                    
                  
                  
    def setHardwareCalibration(self, enable):
        """Sets the hardware calibration mode.
        
        This method allows the user to enable or disable the hardware calibration mode.
        When enabled, the ADC data bypasses the hardware calibration.
        When disabled, the ADC data passes by the hardware calibration.

        Args:
            enable (Bool): True if hardware calibration is enabled, False otherwise.
            
        See Also:
            :class:`isHardwareCalibration`
        
        """ 
        if enable == True:
            DPxEnableDacCalibRaw()
        else:
            DPxDisableDacCalibRaw()
                
                
                
    def isHardwareCalibration(self):
        """Verifies the hardware calibration mode.

        Returns:
            Bool: True if hardware calibration is enabled, False otherwise.
            
        See Also:
            :class:`setHardwareCalibration`
        
        """
        if DPxIsDacCalibRaw() == 0:
            enable = False
        else:
            enable = True
        return enable



    def setBaseAddress(self, address):
        """Sets the Ram buffer start address.
        
        This method allows the user to set the RAM buffer start address used in schedules.
        The given address must be an even value.

        Args:
            address (int): Any value in a range of 0 up to the RAM size.
            
        See Also:
            :class:`getReadAddress`, :class:`setReadAddress`, :class:`getBaseAddress`
        
        """
        DPxSetDacBuffBaseAddr(address)        
            
            
     
    def getBaseAddress(self):
        """Gets the Ram buffer start address.
        
        This method allows the user to get the RAM buffer start address used in schedules.
        It should only be used if the user wants the schedules to wrap when it has reached its maximum size.
        When schedules are expected to wrap, the user should also use setBufferSize()
        
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.
            
        See Also:
            :class:`getReadAddress`, :class:`setReadAddress`, :class:`setBaseAddress`

        """
        return DPxGetDacBuffBaseAddr()  




    def setReadAddress(self, address):
        """Sets the Ram buffer read address.
        
        This method allows the user to set the RAM buffer read address used in schedules.
        This address is used by the schedule to know where the data should be first read from.
        The schedule will then read the following data to the address following the RAM 
        buffer read address. 
        
        The given address must be an even value.

        Args:
            address (int): Any value in a range of 0 up to the RAM size.
            
        See Also:
            :class:`getReadAddress`, :class:`getBaseAddress`
        
        """
        DPxSetDacBuffReadAddr(address)           
            
            
            
    def getReadAddress(self):
        """Gets the Ram buffer read address.
        
        This method allows the user to get the RAM buffer read address used in schedules.
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.
            
        See Also:
            :class:`setReadAddress`, :class:`getBaseAddress`

        """
        return DPxGetDacBuffReadAddr()                

        


    def setBufferSize(self, buffer_size):
        """Sets the Ram buffer size.
        
        This method allows the user to set the RAM buffer size used in schedules. It should only be 
        used if the user wants the schedules to wrap when it has reached its maximum size. When 
        schedules are expected to wrap, the user should also use setBaseAddress().
        The given size is in bytes and must be an even value.

        Args:
            buffer_size (int): Any value in a range of 0 up to the RAM size.
            
        See Also:
            :class:`getBufferSize`
        
        """
        DPxSetDacBuffSize(buffer_size) 
            
            
            
    def getBufferSize(self):
        """Gets the Ram buffer size.
        
        This method allows the user to get the RAM buffer size used in schedules.
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.
            
        See Also:
            :class:`setBufferSize`

        """
        return DPxGetDacBuffSize()



    def setScheduleOnset(self, onset):
        """Sets the schedule onset value.
        
        This method allows the user to set the nanosecond delay between schedule start and first sample.
        If no delay is required, this method doesn't need to be used. Default value is 0.

        Args:
            onset (int): Any positive value equal to or greater than 0.
            
        See Also:
            :class:`getScheduleUnit`, :class:`getScheduleRate`, :class:`setScheduleRate`
        
        """
        DPxSetDacSchedOnset(onset)    
            
            
            
    def getScheduleOnset(self):
        """Gets the schedule onset value.
        
        This method allows the user to get the schedule onset value used in schedules.
        The onset represents a nanosecond delay between schedule start and first sample.
        
        Returns:
            int: Any positive value equal to or greater than 0.
            
        See Also:
            :class:`getScheduleUnit`, :class:`getScheduleRate`, :class:`setScheduleRate`

        """
        return DPxGetDacSchedOnset()        



    def setScheduleRate(self, rate, unit='hz'):
        """Sets the schedule rate.
        
        This method allows the user to set the schedule rate. Since the rate can be given 
        with different units, the method also needs to have a unit associated with the rate.
        If no delay is required, this method doesn't need to be used.

        Args:
            rate (int): Any positive value equal to or greater than 0.
            unit (str): hz    : samples per second, maximum 1 MHz.
                        video : samples per video frame, maximum 1 MHz.
                        nano  : sample period in nanoseconds, minimum 1000 ns.
                        
        See Also:
            :class:`getScheduleUnit`, :class:`getScheduleRate`, :class:`getScheduleOnset`
        
        """
        DPxSetDacSchedRate(rate, unit)        
            
            
                    
    def getScheduleRate(self):
        """Gets the schedule rate value.
        
        This method allows the user to get the schedule rate value used in schedules.
        The rate represents the speed at which the schedule updates.
        
        Returns:
            int: Any positive value equal to or greater than 0.
            
        See Also:
            :class:`getScheduleUnit`, :class:`setScheduleRate`, :class:`getScheduleOnset`

        """
        schedule_rate = DPxGetDacSchedRate()
        return schedule_rate[0]
    
    
    
    def getScheduleUnit(self):
        """Gets the schedule unit value.
        
        This method allows the user to get the schedule unit value used in schedules.
        
        Returns:
            int: Any positive value equal to or greater than 0.
            
        
        See Also:
            :class:`getScheduleRate`, :class:`setScheduleRate`

        """
        schedule_unit = DPxGetDacSchedRate()
        return schedule_unit[1]
    


    def setScheduleCount(self, count):
        """Sets the schedule count.
        
        This method allows the user to set the schedule count for a schedule with a fixed number of samples.
        In which case, the schedule will decrement at a given rate and stop when the count reaches 0.

        Args:
            count (int): Any positive value greater than 0.
                      
        See Also:
            :class:`getScheduleCount`, :class:`setScheduleCountDown`
        
        """
        DPxSetDacSchedCount(count)
         
            
            
            
    def getScheduleCount(self):
        """Gets the schedule count value.
        
        This method allows the user to get the current count for a schedule.
        
        Returns:
            int: Any positive value equal to or greater than 0.
            
        
        See Also:
            :class:`setScheduleCount`, :class:`setScheduleCountDown`

        """
        return DPxGetDacSchedCount()       



    def setScheduleCountDown(self, enable):
        """Sets the schedule count down mode.
        
        This method allows the user to enable or disable the count down on a schedule.
        When enabled, the schedule decrements at the given rate and stops automatically when the count hits 0.
        When disabled, the schedule increments at the given rate and is stopped by calling stopSchedule().


        Args:
            enable (Bool): True if count down is enabled, False otherwise.
        
        
        See Also:
            :class:`setScheduleCount`, :class:`stopSchedule`, :class:`isCountDownEnabled`
        
        """
        if enable == True:
            DPxEnableDacSchedCountdown()
        else:
            DPxDisableDacSchedCountdown()

                

    def isCountDownEnabled(self):
        """Verifies the schedule count down mode.

        Returns:
            enable (Bool): True if the schedule is decrementing at every sample, False otherwise.
            
        See Also:
            :class:`setScheduleCount`, :class:`stopSchedule`, :class:`setScheduleCountDown`
        
        """
        if DPxIsDacSchedCountdown() !=0:
            enable = True
        else:
            enable = False 
        return enable        



    def startSchedule(self):
        """Starts a schedule.

        Schedules may be configured in different ways, affecting their behavior. Before a schedule is started, the user should
        make sure that it is properly set in the right mode.   
        
         
        See Also:
            :class:`stopSchedule`, :class:`setReadAddress`, :class:`setBaseAddress`, :class:`setScheduleOnset`, :class:`setScheduleRate`,
            :class:`setScheduleCountDown`, :class:`setScheduleCount`
        
        """
        DPxStartDacSched()



    def stopSchedule(self):
        """Stops the active schedule for a given subsystem.

        Depending on how the Schedules are configured, it may not be necessary to call this method. When a schedule is using a count down, it is not
        required to stop the schedule.   
        
         
        See Also:
            :class:`startSchedule`, :class:`setReadAddress`, :class:`setBaseAddress`, :class:`setScheduleOnset`, :class:`setScheduleRate`,
            :class:`setScheduleCountDown`, :class:`setScheduleCount`
        
        """
        DPxStopDacSched()        
        


    def isScheduleRunning(self):
        """Verifies if a schedule is currently running on the subsystem.

        Returns:
            schedule_running (Bool): True if a schedule is currently running, False otherwise.
            
        See Also:
            :class:`startSchedule`, :class:`stopSchedule`, :class:`getScheduleRunningState()`
        
        """
        if DPxIsDacSchedRunning() == 0:
            schedule_running = False
        else:
            schedule_running = True
        return schedule_running