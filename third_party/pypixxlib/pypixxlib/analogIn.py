from _libdpx import DPxUpdateRegCache, DPxGetAdcNumChans, DPxGetAdcValue, \
    DPxGetAdcRange, DPxGetAdcVoltage, DPxSetAdcBuffChanRef, \
    DPXREG_ADC_CHANREF_GND, DPXREG_ADC_CHANREF_DIFF, DPXREG_ADC_CHANREF_REF0, \
    DPXREG_ADC_CHANREF_REF1, DPxGetAdcBuffChanRef, DPxEnableAdcBuffChan, \
    DPxDisableAdcBuffChan, DPxIsAdcBuffChan, DPxEnableAdcCalibRaw, \
    DPxDisableAdcCalibRaw, DPxIsDacCalibRaw, DPxEnableDacAdcLoopback, \
    DPxDisableDacAdcLoopback, DPxIsDacAdcLoopback, DPxEnableAdcFreeRun, \
    DPxDisableAdcFreeRun, DPxIsAdcFreeRun, DPxSetAdcBuffBaseAddr, \
    DPxGetAdcBuffBaseAddr, DPxSetAdcBuffWriteAddr, DPxGetAdcBuffWriteAddr, \
    DPxSetAdcBuffSize, DPxGetAdcBuffSize, DPxSetAdcSchedOnset, \
    DPxGetAdcSchedOnset, DPxSetAdcSchedRate, DPxGetAdcSchedRate, \
    DPxSetAdcSchedCount, DPxGetAdcSchedCount, DPxEnableAdcSchedCountdown, \
    DPxDisableAdcSchedCountdown, DPxIsAdcSchedCountdown, DPxStartAdcSched, \
    DPxStopAdcSched, DPxIsAdcSchedRunning, DPxEnableAdcLogTimetags, \
    DPxDisableAdcLogTimetags, DPxIsAdcLogTimetags, DPxIsAdcCalibRaw, \
    DPxDisableAdcBuffAllChans
from abc import ABCMeta, abstractmethod
from schedule import Schedule




class AnalogIn(Schedule):
    """Class which contains the ADC features.

    These functions should only be called from your device's ``adc`` parameter: ``my_device.adc.function()``. The functions
    below are used to configure and use Analog In of your VPixx Device.
    """
    __metaclass__ = ABCMeta
       
    def getNbrOfChannel(self):
        """Gets the number of channels available.

        Returns:
            int:   Number of channels.

        """
        return DPxGetAdcNumChans()
    
    
    
    def getChannelValue(self, channel):
        """Gets the current value of a channel.
        
        This method allows the user to know the value of a given channel. The return value is
        a 16-bit 2's complement signed number. Value can be obtained for channels 0 to 17.

        Returns:
            int: value of the channel.

        """
        return DPxGetAdcValue(channel)
        
        
        
    def getChannelRange(self, channel):
        """Gets the range of a channel.

        Returns:
            tuple: Range of the channel. The returned value is a tuple with the minimum range followed by the maximum range.
            Both values are integers.

        """
        return DPxGetAdcRange(channel)



    def getChannelVoltage(self, channel):
        """Gets the current voltage of a channel.

        Returns:
            float: voltage of the channel.

        """
        return DPxGetAdcVoltage(channel)
    
    
    
    def setChannelReference(self, channel, reference):
        """Sets a reference to a channel.
        
        This method allows the user to enable or disable ram buffering on a given channel.
        When enabled, a given channel is buffered in ram. Enabling RAM buffering can only
        be done for channels 0 to 15.

        Args:
            channel (int): Channel number to associate with a reference. 
            reference (String): Valid argument is one of the following predefined constants.\n
                - gnd  : Referenced to ground.
                - diff : Referenced to adjacent analog input. 
                - ref0 : Referenced to REF0 analog input.
                - ref1 : Referenced to REF1 analog input.
            
        See Also:
            :class:`getChannelReference`
        
        """
        DPxSetAdcBuffChanRef(channel, reference)     
            
            
            
    def getChannelReference(self, channel):
        """Gets the reference associated with a channel.

        Args:
            channel (int): channel to query.
        
        Returns:
            String: one of the following predefined constants.\n
                - gnd  : Referenced to ground.
                - diff : Referenced to adjacent analog input. 
                - ref0 : Referenced to REF0 analog input.
                - ref1 : Referenced to REF1 analog input.

        See Also:
            :class:`setChannelReference`

        """
        return DPxGetAdcBuffChanRef(channel)
        


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
                    DPxEnableAdcBuffChan(i) 
            else:
                DPxEnableAdcBuffChan(channel)
        else:
            if channel == None:
                DPxDisableAdcBuffAllChans()
            else:
                DPxDisableAdcBuffChan(channel) 
                
                
                
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
        if DPxIsAdcBuffChan(channel) == 0:
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
            DPxEnableAdcCalibRaw()
        else:
            DPxDisableAdcCalibRaw()
                
                
                
    def isHardwareCalibration(self):
        """Verifies the hardware calibration mode.

        Returns:
            Bool: True if hardware calibration is enabled, False otherwise.
            
        See Also:
            :class:`setHardwareCalibration`
        
        """
        if DPxIsAdcCalibRaw() == 0:
            enable = False
        else:
            enable = True
        return enable
    
    
                         
    def setLoopback(self, enable):
        """Sets the digital inputs and outputs loopback mode.
        
        This method allows the user to enable or disable the loopback between digital output ports and digital inputs.
        When enabled, the digital outputs send their data to the digital inputs.
        When disabled, the digital inputs will not get the digital outputs data.

        Args:
            enable (Bool): True if loopback is enabled, False otherwise.
            
        See Also:
            :class:`isLoopbackEnabled`
        
        """ 
        if enable == True:
            DPxEnableDacAdcLoopback()
        else:
            DPxDisableDacAdcLoopback()             
            
            
            
    def isLoopbackEnabled(self):
        """Verifies the digital inputs and outputs loop back mode.

        Returns:
            Bool: True if transitions are being stabilized, False otherwise.
            
        See Also:
            :class:`setLoopback`
        
        """
        if DPxIsDacAdcLoopback() == 0:
            enable = False
        else:
            enable = True
        return enable    
    
    
    
    def setFreeRunMode(self, enable):
        """Sets the continuous acquisition mode.
        
        This method allows the user to enable or disable the continuous acquisition (free running) mode.
        When enabled, the ADCs convert continuously. Doing so can add up to 4 microseconds random latency to scheduled samples.
        When disabled, the ADCs only convert on schedule ticks. This can be used for microsecond-precise sampling.

        Args:
            enable (Bool): True if loopback is enabled, False otherwise.
            
        See Also:
            :class:`isFreeRunEnabled`
        
        """ 
        if enable == True:
            DPxEnableAdcFreeRun()
        else:
            DPxDisableAdcFreeRun()
            
            
            
    def isFreeRunEnabled(self):
        """Verifies the continuous acquisition mode state.

        Returns:
            Bool: True if continuous acquisition is activated, False otherwise.
            
        See Also:
            :class:`setFreeRunMode`
        
        """
        if DPxIsAdcFreeRun() == 0:
            free_run = False
        else:
            free_run = True
        return free_run    
    
    
    
    def setBaseAddress(self, address):
        """Sets the Ram buffer start address.
        
        This method allows the user to set the RAM buffer start address used in schedules.
        The given address must be an even value.

        Args:
            address (int): Any value in a range of 0 up to the RAM size.
        
        """
        DPxSetAdcBuffBaseAddr(address)  
            
            
     
    def getBaseAddress(self):
        """Gets the Ram buffer start address.
        
        This method allows the user to get the RAM buffer start address used in schedules.
        It should only be used if the user wants the schedules to wrap when it has reached its maximum size.
        When schedules are expected to wrap, the user should also use setBufferSize()
        
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetAdcBuffBaseAddr()  



    def setWriteAddress(self, address):
        """Sets the Ram buffer write address.
        
        This method allows the user to set the RAM buffer write address used in schedules.
        This address is used by the schedule to know where the data should be first written to.
        The schedule will then write the following data to the address following the RAM 
        buffer write address. 
        
        The given address must be an even value.

        Args:
            address (int): Any value in a range of 0 up to the RAM size.
        
        """
        DPxSetAdcBuffWriteAddr(address)      
            
            
            
    def getWriteAddress(self):
        """Gets the Ram buffer write address.
        
        This method allows the user to get the RAM buffer write address used in schedules.
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetAdcBuffWriteAddr()
        


    def setBufferSize(self, buffer_size):
        """Sets the Ram buffer size.
        
        This method allows the user to set the RAM buffer size used in schedules. It should only be 
        used if the user wants the schedules to wrap when it has reached its maximum size. When 
        schedules are expected to wrap, the user should also use ``setBaseAddress()``.
        The given size is in bytes and must be an even value.

        Args:
            buffer_size (int): Any value in a range of 0 up to the RAM size.
        
        """
        DPxSetAdcBuffSize(buffer_size)
            
            
            
    def getBufferSize(self):
        """Gets the Ram buffer size.
        
        This method allows the user to get the RAM buffer size used in schedules.
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetAdcBuffSize()              




    def setScheduleOnset(self, onset):
        """Sets the schedule onset value.
        
        This method allows the user to set the nanosecond delay between schedule start and first sample.
        If no delay is required, this method does not need to be used. Default value is 0.

        Args:
            onset (int): Any positive value equal to or greater than 0.
        
        """
        DPxSetAdcSchedOnset(onset)        
            
            
            
    def getScheduleOnset(self):
        """Gets the schedule onset value.
        
        This method allows the user to get the schedule onset value used in schedules.
        The onset represents a nanosecond delay between schedule start and first sample.
        
        Returns:
            int: Any positive value equal to or greater than 0.

        """
        return DPxGetAdcSchedOnset()      



    def setScheduleRate(self, rate, unit='hz'):
        """Sets the schedule rate.
        
        This method allows the user to set the schedule rate. Since the rate can be given 
        with different units, the method also needs to have a unit associated with the rate.
        
        nanosecond delay between schedule start and first sample.
        If no delay is required, this method does not need to be used. Default value is 0.

        Args:
            rate (int): Any positive value equal to or greater than 0.
            unit (String): Any of the following predefined constants:\n
                - hz    : samples per second, maximum 200 kHz.
                - video : samples per video frame, maximum 200 kHz.
                - nano  : sample period in nanoseconds, minimum 5000 ns.
        
        """
        DPxSetAdcSchedRate(rate, unit)  
            
            
                    
    def getScheduleRate(self):
        """Gets the schedule rate value.
        
        This method allows the user to get the schedule rate value used in schedules.
        The rate represents the speed at which the schedule updates.
        
        Returns:
            int: Any positive value equal to or greater than 0.

        """
        schedule_rate = DPxGetAdcSchedRate()
        return schedule_rate[0]
    
    
    
    def getScheduleUnit(self):
        """Gets the schedule unit value.
        
        This method allows the user to get the schedule unit value used in schedules.
        
        Returns:
            int: Any positive value equal to or greater than 0.
            
        
        See Also:
            :class:`getScheduleRate`, :class:`setScheduleRate`

        """
        schedule_unit = DPxGetAdcSchedRate()
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
        DPxSetAdcSchedCount(count)
            
            
    def getScheduleCount(self):
        """Gets the schedule count value.
        
        This method allows the user to get the current count for a schedule.
        
        Returns:
            int: Any positive value equal to or greater than 0.
            
        
        See Also:
            :class:`setScheduleCount`, :class:`setScheduleCountDown`

        """
        return DPxGetAdcSchedCount()        



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
            DPxEnableAdcSchedCountdown()
        else:
            DPxDisableAdcSchedCountdown()

                

    def isCountDownEnabled(self):
        """Verifies the schedule count down mode.

        Returns:
            Bool: True if the schedule is decrementing at every sample, False otherwise.
            
        See Also:
            :class:`setScheduleCount`, :class:`stopSchedule`, :class:`setScheduleCountDown`
        
        """
        if DPxIsAdcSchedCountdown() !=0:
            enable = True
        else:
            enable = False 
        return enable        



    def startSchedule(self):
        """Starts a schedule.

        Schedules may be configured in different ways, affecting their behavior. Before a schedule is started, the user should
        make sure that it is properly set in the right mode.   
        
         
        See Also:
            :class:`stopSchedule`, :class:`setWriteAddress`, :class:`setBaseAddress`, :class:`setScheduleOnset`, :class:`setScheduleRate`,
            :class:`setScheduleCountDown`, :class:`setScheduleCount`
        
        """
        DPxStartAdcSched()



    def stopSchedule(self):
        """Stops the active schedule for a given subsystem.

        Depending on how the Schedules are configured, it may not be necessary to call this method. When a schedule is using a count down, it is not
        required to stop the schedule.   
        
         
        See Also:
            :class:`startSchedule`, :class:`setWriteAddress`, :class:`setBaseAddress`, :class:`setScheduleOnset`, :class:`setScheduleRate`,
            :class:`setScheduleCountDown`, :class:`setScheduleCount`
        
        """
        DPxStopAdcSched()        
        


    def isScheduleRunning(self):
        """Verifies if a schedule is currently running on the subsystem.

        Returns:
            Bool: True if a schedule is currently running, False otherwise.
            
        See Also:
            :class:`startSchedule`, :class:`stopSchedule`
        
        """
        if DPxIsAdcSchedRunning() == 0:
            schedule_running = False
        else:
            schedule_running = True
        return schedule_running
    

    
    def setLogTimetags(self, enable):
        """Sets the timetag mode on the data samples.
        
        This method allows the user to enable or disable the timetag on acquired data.
        When enabled, each buffered sample is preceded with a 64-bit nanosecond timetag.
        When disabled, buffered data has no timetags.

        Args:
            enable (Bool): True to activate the timetag mode, False otherwise.
            
        See Also:
            :class:`isLogTimetagsEnabled`
        
        """        
        if enable == True:
            DPxEnableAdcLogTimetags()
        else:
            DPxDisableAdcLogTimetags()
            
            
            
    def isLogTimetagsEnabled(self):
        """Verifies if the timetag mode is enabled.

        Returns:
            Bool: True if timetag mode is enabled, False otherwise.
            
        See Also:
            :class:`setLogTimetags`
        
        """
        if DPxIsAdcLogTimetags() == 0:
            enabled = False
        else:
            enabled = True
        return enabled
