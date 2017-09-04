from schedule import Schedule
from abc import ABCMeta, abstractmethod

from _libdpx import DPxUpdateRegCache, DPxGetDinNumBits, DPxGetDinValue, \
    DPxSetDinDataDir, DPxGetDinDataDir, DPxSetDinDataOut, DPxGetDinDataOut, \
    DPxSetDinDataOutStrength, DPxGetDinDataOutStrength, DPxEnableDinStabilize, \
    DPxDisableDinStabilize, DPxIsDinStabilize, DPxEnableDinDebounce, \
    DPxDisableDinDebounce, DPxIsDinDebounce, DPxEnableDoutDinLoopback, \
    DPxDisableDoutDinLoopback, DPxIsDoutDinLoopback, DPxSetDinBuffBaseAddr, \
    DPxGetDinBuffBaseAddr, DPxSetDinBuffWriteAddr, DPxGetDinBuffWriteAddr, \
    DPxSetDinBuffSize, DPxGetDinBuffSize, DPxSetDinSchedOnset, \
    DPxGetDinSchedOnset, DPxSetDinSchedRate, DPxGetDinSchedRate, \
    DPxSetDinSchedCount, DPxGetDinSchedCount, DPxEnableDinSchedCountdown, \
    DPxDisableDinSchedCountdown, DPxIsDinSchedCountdown, DPxStartDinSched, \
    DPxStopDinSched, DPxIsDinSchedRunning, DPxIsAdcSchedRunning, \
    DPxEnableDinLogTimetags, DPxDisableDinLogTimetags, DPxIsDinLogTimetags, \
    DPxEnableDinLogEvents, DPxDisableDinLogEvents, DPxIsDinLogEvents, \
    DPxGetAdcSchedRate





class DigitalIn(Schedule):
    """Class which implements the DIN features.

    Any device which has Digital IN should implement this Class. It contains all the necessary methods to use the
    digital inputs of a VPixx device.
    """
    __metaclass__ = ABCMeta    
    
    def __init__(self):
        pass
                
    def getNbrOfBit(self):
        """Gets the number of bit available.

        Returns:
            int: Number of bits.

        """
        return DPxGetDinNumBits()
    
    
    
    def getValue(self):
        """Gets the current value of the bits.

        Returns:
            int: Value of bits.

        """
        return DPxGetDinValue()



    def setBitDirection(self, bit_mask):
        """Sets the port direction mask.
        
        Sets the port direction for each bit. The mask is one value representing all bits from the port.
        The given ``bit_mask`` will set the direction of all digital input bits. For each bit which should drive its port,
        the corresponding ``bit_mask`` value should be set to 1. An hexadecimal ``bit_mask`` can be provided. 
        
        For example, ``bit_mask = 0x0000F`` will enable the port for the first 4 bits on the right. All other ports will be
        disabled. User can then use the first 4 bits to drive the port.

        Args:
            int: Set bit to 1 to enable the port for that bit. Set bit to 0 to disable it.

        """
        DPxSetDinDataDir(bit_mask)
            
            
     
    def getBitDirection(self):
        """Gets the port direction mask.
        
        User can obtain the value in decimal or hexadecimal. 
                
        Returns:
            int: Bit set to 1 is an enabled port. Bit set to 0 is a disabled port.

        """        
        return DPxGetDinDataDir()



    def setOutputValue(self, value):
        """Sets the data which should be driven on each port.
        
        In order to be able to drive the ports with the given value, the port direction has to be properly enabled.
        This can be done using the "setBitDirection()" with the appropriate bit mask.

        Args:
            value (int): Any value in a range of 0 to 16777215.

        """
        DPxSetDinDataOut( int(value, 0) )     
            
            
     
    def getOutputValue(self):
        """Gets the data which is being driven on each output port.
        
        This method allows the user to get the data which is currently driven on the output port.
                
        Returns:
            int: Any value in a range of 0 to 16777215.

        """
        return DPxGetDinDataOut()              



    def setOutputStrength(self, strength):
        """Sets the strength of the driven outputs.  
        
        This method allows the user to set the current (Ampere) strength of the driven outputs.
        The implementation actual values uses ``1/16`` up to ``16/16``. So minimum strength will be ``0.0625``
        and maximum will be ``1``. The strength can be increased by ``0.0625`` up to ``1``. Giving a strength
        of ``0`` will thus set it to ``0.0625``. Giving a strength between ``0.0625`` and ``0.125`` will
        round the given strength to one of the two increments.
        
        The strength is the same for all bits.
        
        Args:
            strength (float): Any value in a range of 0 to 1.

        """
        DPxSetDinDataOutStrength(strength)        
            
            
     
    def getOutputStrength(self):
        """Gets the strength of the driven outputs.
        
        This method allows the user to get the strength currently driven by the outputs.
        The implementation uses values from ``1/16`` up to ``16/16``. Therefore minimum strength will be ``0.0625``
        and maximum will be ``1``. The strength can be increased by ``0.0625`` up to ``1``. 
                
        Returns:
            float: Any value in a range of 0 to 1.

        """
        return DPxGetDinDataOutStrength()           




    def setStabilize(self, enable):
        """Sets the input stabilization mode.
        
        This method allows the user to enable or disable the input transitions stabilization.
        When enabled, input transitions are only recognized after the entire input bus has been stable for 80 ns.
        This is useful for deskewing parallel busses, and ignoring transmission line reflections.
        When disabled, the input transitions are immediately recognized. In which case, it can be useful to enable
        debouncing using ``setDebounce()``.

        Args:
            enable (Bool): True if transitions are being stabilized, False otherwise.
        
        """
        if enable == True:
            DPxEnableDinStabilize()
        else:
            DPxDisableDinStabilize()
            
            
            
    def isStabilizeEnabled(self):
        """Verifies if the input transitions are being stabilized.

        Returns:
            stabilize (Bool): True if transitions are being stabilized, False otherwise.
        
        """
        if DPxIsDinStabilize() == 0:
            stabilize = False
        else:
            stabilize = True
        return stabilize 
    
    

    def setDebounce(self, enable):
        """Sets the input debounce mode.
        
        This method allows the user to enable or disable the input debounce mode.
        When a DIN transitions, ignore further DIN transitions for the next 30 milliseconds. This is useful for response buttons.
        When disabled, the inputs transitions are immediately recognized. In which case, it can be useful to enable
        debouncing using ``setStabilize()``.

        Args:
            enable (Bool): True if transitions are being debounced, False otherwise.
        
        """        
        if enable == True:
            DPxEnableDinDebounce()
        else:
            DPxDisableDinDebounce()
            
            
            
    def isDebounceEnabled(self):
        """Verifies if the input debounce mode is enabled.

        Returns:
            debouce (Bool): True if transitions are being stabilized, False otherwise.
        
        """
        if DPxIsDinDebounce() == 0:
            debouce = False
        else:
            debouce = True
        return debouce               
    
    
                    
    def setLoopback(self, enable):
        """Sets the digital inputs and outputs loopback mode.
        
        This method allows the user to enable or disable the loopback between digital output ports and digital inputs.
        When enabled, the digital outputs send their data to the digital inputs.
        When disabled, the digital inputs will not get the digital outputs data.
        debouncing using "setStabilize()".

        Args:
            enable (Bool): True if loopback is enabled, False otherwise.
            
        See Also:
            :class:`isLoopbackEnabled`
        
        """ 
        if enable == True:
            DPxEnableDoutDinLoopback()
        else:
            DPxDisableDoutDinLoopback()       
            
            
            
    def isLoopbackEnabled(self):
        """Verifies the digital inputs and outputs loopback mode.

        Returns:
            enable (Bool): True if transitions are being stabilized, False otherwise.
            
        See Also:
            :class:`setLoopback`
        
        """
        if DPxIsDoutDinLoopback() == 0:
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
        
        """
        DPxSetDinBuffBaseAddr(address)     
            
            
     
    def getBaseAddress(self):
        """Gets the Ram buffer start address.
        
        This method allows the user to get the RAM buffer start address used in schedules.
        It should only be used if the user wants the schedules to wrap when it has reached its maximum size.
        When schedules are expected to wrap, the user should also use setBufferSize().
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetDinBuffBaseAddr()  


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
        DPxSetDinBuffWriteAddr(address)         
            
            
            
    def getWriteAddress(self):
        """Gets the Ram buffer write address.
        
        This method allows the user to get the RAM buffer write address used in schedules.
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetDinBuffWriteAddr()                


    def setBufferSize(self, buffer_size):
        """Sets the Ram buffer size.
        
        This method allows the user to set the RAM buffer size used in schedules. It should only be 
        used if the user wants the schedule to wrap when it has reached its maximum size. When 
        schedules are expected to wrap, the user should also use ``setBaseAddress()``.
        The given size is in bytes and must be an even value.

        Args:
            buffer_size (int): Any value in a range of 0 up to the RAM size.
        
        """
        DPxSetDinBuffSize(buffer_size)
            
            
    def getBufferSize(self):
        """Gets the Ram buffer size.
        
        This method allows the user to get the RAM buffer size used in schedules.
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetDinBuffSize()



    def setScheduleOnset(self, onset):
        """Sets the schedule onset value.
        
        This method allows the user to set the nanosecond delay between schedule start and first sample.
        If no delay is required, this method does not need to be used. Default value is 0.

        Args:
            onset (int): Any positive value equal to or greater than 0.
            
        See Also:
            :class:`getScheduleOnset`
        
        """
        DPxSetDinSchedOnset(onset)
            
            
            
    def getScheduleOnset(self):
        """Gets the schedule onset value.
        
        This method allows the user to get the schedule onset value used in schedules.
        The onset represents a nanosecond delay between schedule start and first sample.
        
        Returns:
            int: Any positive value equal to or greater than 0.
            
        See Also:
            :class:`setScheduleOnset`

        """
        return DPxGetDinSchedOnset()          
  



    def setScheduleRate(self, rate, unit='hz'):
        """Sets the schedule rate.
        
        This method allows the user to set the schedule rate. Since the rate can be given 
        with different units, the method also needs to have a unit associated with the rate.

        Args:
            rate (int): Any positive value equal to or greater than 0.
            unit (str): hz    : samples per second, maximum 1 MHz.
                        video : samples per video frame, maximum 1 MHz.
                        nano  : sample period in nanoseconds, minimum 1000 ns.
                        
        See Also:
            :class:`getScheduleRate`, :class:`getScheduleUnit`
        
        """
        DPxSetDinSchedRate(rate, unit)
            
            
            
    def getScheduleRate(self):
        """Gets the schedule rate value.
        
        This method allows the user to get the schedule rate value used in schedules.
        The rate represents the speed at which the schedule updates.
        
        Returns:
            int: Any positive value equal to or greater than 0.
            
        See Also:
            :class:`setScheduleRate`, :class:`getScheduleUnit`

        """
        schedule_rate = DPxGetDinSchedRate()
        return schedule_rate[0]
    
    
    
    def getScheduleUnit(self):
        """Gets the schedule unit value.
        
        This method allows the user to get the schedule unit value used in schedules.
        
        Returns:
            int: Any positive value equal to or greater than 0.
            
        
        See Also:
            :class:`getScheduleRate`, :class:`setScheduleRate`

        """
        schedule_unit = DPxGetDinSchedRate()
        return schedule_unit[1]        
            
            
            
    def setScheduleCount(self, count):
        """Sets the schedule count.
        
        This method allows the user to set the schedule count for a schedule with a fixed number of sample.
        In which case, the schedule will decrement at a given rate and stop when the count reaches 0.


        Args:
            count (int): Any positive value greater than 0.
            
                        
        See Also:
            :class:`getScheduleCount`, :class:`setScheduleCountDown`
        
        """
        DPxSetDinSchedCount(count)           
            
            
            
    def getScheduleCount(self):
        """Gets the schedule count value.
        
        This method allows the user to get the current count for a schedule.
        
        Returns:
            int: Any positive value equal to or greater than 0.
            
        
        See Also:
            :class:`setScheduleCount`, :class:`setScheduleCountDown`

        """
        return DPxGetDinSchedCount()
       



    def setScheduleCountDown(self, enable):
        """Sets the schedule count down mode.
        
        This method allows the user to enable or disable the count down on a schedule.
        When enabled, the schedule decrements at the given rate and stops automatically when count hits 0.
        When disabled, the schedule increments at the given rate and is stopped by calling stopSchedule().


        Args:
            enable (Bool): True if count down is enabled, False otherwise.
        
        
        See Also:
            :class:`setScheduleCount`, :class:`stopSchedule`, :class:`isCountDownEnabled`
        
        """
        if enable == True:
            DPxEnableDinSchedCountdown()
        else:
            DPxDisableDinSchedCountdown()

                

    def isCountDownEnabled(self):
        """Verifies the schedule count down mode.

        Returns:
            enable (Bool): True if the schedule is decrementing at every sample, False otherwise.
            
        See Also:
            :class:`setScheduleCount`, :class:`stopSchedule`, :class:`setScheduleCountDown`
        
        """
        if DPxIsDinSchedCountdown() != 0:
            enable = True
        else:
            enable = False 
        return enable        



    def startSchedule(self):
        """Starts a schedule.

        Schedules may be configured in different ways, affecting their behavior. Before a schedule is started, the user should
        make sure that it is properly set in the right mode.   
        
         
        See Also:
            :class:`stopSchedule`, :class:`setWriteAddress`, :class:`setBaseAddress`, :class:`setScheduleOnset`,
            :class:`setScheduleRate`, :class:`setScheduleCountDown`, :class:`setScheduleCount`
        
        """
        DPxStartDinSched()



    def stopSchedule(self):
        """stop the active schedule for a given subsystem.

        Depending on how the Schedules are configured, it may not be necessary to call this method. When a schedule is using a count down, it is not
        required to stop the schedule.   
        
         
        See Also:
            :class:`startSchedule`, :class:`setWriteAddress`, :class:`setBaseAddress`, :class:`setScheduleOnset`, 
            :class:`setScheduleRate`, :class:`setScheduleCountDown`, :class:`setScheduleCount`
        
        """
        DPxStopDinSched()        
        


    def isScheduleRunning(self):
        """Verifies if a schedule is currently running on the subsystem.

        Returns:
            schedule_running (Bool): True if a schedule is currently running, False otherwise.
            
        See Also:
            :class:`startSchedule`, :class:`stopSchedule`
        
        """
        if DPxIsDinSchedRunning() == 0:
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
            DPxEnableDinLogTimetags()
        else:
            DPxDisableDinLogTimetags()
            
            
            
    def isLogTimetagsEnabled(self):
        """Verifies if the timetag mode is enabled.

        Returns:
            enable (Bool): True if timetag mode is enabled, False otherwise.
            
        See Also:
            :class:`setLogTimetags`
        
        """
        if DPxIsDinLogTimetags() == 0:
            enabled = False
        else:
            enabled = True
        return enabled
    


    def setLogEvents(self, enable):
        """Sets the transition log events mode on data samples.
        
        This method allows the user to enable or disable the transition log events on acquired data.
        When enabled, each transition is automatically logged. No schedule is required.  This is the
        best way to log response buttons. When disabled, logging of transitions is done automatically.

        Args:
            enable (Bool): True to activate the log event mode, False otherwise.
            
        See Also:
            :class:`isLogEventsEnabled`
        
        """
        if enable == True:
            DPxEnableDinLogEvents()
        else:
            DPxDisableDinLogEvents()
            
            
            
    def isLogEventsEnabled(self):
        """Verifies if the transition log events mode is enabled.

        Returns:
            enable (Bool): True if transition log events mode is enabled, False otherwise.
            
        See Also:
            :class:`setLogEvents`
        
        """
        if DPxIsDinLogEvents() == 0:
            enabled = False
        else:
            enabled = True
        return enabled