from _libdpx import DPxUpdateRegCache, DPxGetDoutNumBits, DPxSetDoutValue, \
    DPxGetDoutValue, DPxEnableDoutButtonSchedules, DPxDisableDoutButtonSchedules, \
    DPxIsDoutButtonSchedules, DPxEnableDoutBacklightPulse, \
    DPxDisableDoutBacklightPulse, DPxIsDoutBacklightPulse, \
    DPxSetDoutBuffBaseAddr, DPxGetDoutBuffBaseAddr, DPxSetDoutBuffReadAddr, \
    DPxGetDoutBuffReadAddr, DPxSetDoutBuffSize, DPxGetDoutBuffSize, \
    DPxSetDoutSchedOnset, DPxGetDoutSchedOnset, DPxSetDoutSchedRate, \
    DPxGetDoutSchedRate, DPxSetDoutSchedCount, DPxGetDoutSchedCount, \
    DPxEnableDoutSchedCountdown, DPxDisableDoutSchedCountdown, \
    DPxIsDoutSchedCountdown, DPxStartDoutSched, DPxStopDoutSched, \
    DPxIsDoutSchedRunning, DPxEnableDoutPixelMode, DPxDisableDoutPixelMode, \
    DPxIsDoutPixelMode
from abc import ABCMeta, abstractmethod
from schedule import Schedule


class DigitalOut(Schedule):
    """The Dout class is used to set and get all values related to the Dout.
    """
    __metaclass__ = ABCMeta   
    
    def __init__(self):
        pass
    
    def getNbrOfBit(self):
        """Gets the number of bits available.

        Returns:
            int:   Number of bits.

        """
        return DPxGetDoutNumBits()
    
    
    
    def setBitValue(self, value, bit_mask):
        """ Sets the value of the bits.
        
        This method allows the user to set the bit value for the subsystem. The mask is one value representing all bits from the port.
        The given bit_mask will set the direction of all digital input bits. For each bit which should drive its port,
        the corresponding bit_mask value should be set to 1.
        
        For example, ``bit_mask = 0x0000F`` will enable the port for the first 4 bits on the right. All other ports will be
        disabled. User can then use the first 4 bits to drive the port.
        
        Args:
            value (int): value of bits.
            bit_mask (int): Set bit to 1 will enable the port for that bit. Set bit to 0 will disable it.
            
        
        See Also:
            :class:`getBitValue`

        """
        DPxSetDoutValue(value, bit_mask)
    
    
        
    def getBitValue(self):
        """Gets the current value of the bits.

        Returns:
            int:   value of bit.
            
        See Also:
            :class:`setBitValue`

        """
        return DPxGetDoutValue()
        


    def setButtonSchedules(self, enable):
        """Sets the schedule start on button press mode.
        
        This method allows the user to enable or disable the transition log events on acquired data.
        When enabled, digital output schedules are done following a digital input button press. When disabled, digital output schedules have to
        be started manually.

        Args:
            enable (Bool): True to activate the log event mode, False otherwise.
            
        See Also:
            :class:`isButtonSchedulesEnabled`
        
        """
        if enable == True:
            DPxEnableDoutButtonSchedules()
        else:
            DPxDisableDoutButtonSchedules()

                

    def isButtonSchedulesEnabled(self):
        """Verifies if the schedule start on button press mode is enabled.

        Returns:
            enable (Bool): True if the mode is enabled, False otherwise.
            
        See Also:
            :class:`setButtonSchedules`
        
        """
        if DPxIsDoutButtonSchedules() !=0:
            enable = True
        else:
            enable = False 
        return enable    



    def setBacklightPulse(self, enable):
        """Sets the back light pulse mode.
        
        This method allows the user to enable or disable the back light pulse mode.
        When enabled, the LCD back light LEDs are gated by bit 15 of the digital output. It can be used to make a tachistoscope
        by pulsing bit 15 of the digital output with a schedule. When disabled, the outputs work normally and are unaffected.

        Args:
            enable (Bool): True to activate the back light pulse mode, False otherwise.
            
        See Also:
            :class:`isBacklightPulseEnabled`
        
        """
        if enable == True:
            DPxEnableDoutBacklightPulse()
        else:
            DPxDisableDoutBacklightPulse()

                

    def isBacklightPulseEnabled(self):
        """Verifies if the back light pulse mode is enabled.

        Returns:
            enable (Bool): True if back light pulse mode is enabled, False otherwise.
            
        See Also:
            :class:`setBacklightPulse`
        
        """
        if DPxIsDoutBacklightPulse() !=0:
            enable = True
        else:
            enable = False 
        return enable



    def setBaseAddress(self, value):
        """Sets the Ram buffer start address.
        
        This method allows the user to set the RAM buffer start address used in schedules.
        The given address must be an even value.

        Args:
            address (int): Any value in a range of 0 up to the RAM size.
        
        """
        return DPxSetDoutBuffBaseAddr(value)          
            
            
     
    def getBaseAddress(self):
        """Gets the Ram buffer start address.
        
        This method allows the user to get the RAM buffer start address used in schedules.
        It should only be used if the user wants the schedules to wrap when it has reached its maximum size.
        When schedules are expected to wrap, the user should also use setBufferSize()
        
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetDoutBuffBaseAddr()



    def setReadAddress(self, address):
        """Sets the Ram buffer read address.
        
        This method allows the user to set the RAM buffer read address used in schedules.
        This address is used by schedule to know where the data should be first read from.
        The schedules will then read the following data to the address following the RAM 
        buffer read address. 
        
        The given address must be an even value.

        Args:
            address (int): Any value in a range of 0 up to the RAM size.
        
        """
        DPxSetDoutBuffReadAddr(address)            
            
            
            
    def getReadAddress(self):
        """Gets the Ram buffer read address.
        
        This method allows the user to get the RAM buffer read address used in schedules.
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetDoutBuffReadAddr()                
        


    def setBufferSize(self, buffer_size):
        """Sets the Ram buffer size.
        
        This method allows the user to set the RAM buffer size used in schedules. It should only be 
        used if the user wants the schedules to wrap when it has reached its maximum size. When 
        schedules are expected to wrap, the user should also use ``setBaseAddress()``.
        The given size is in bytes and must be an even value.

        Args:
            buffer_size (int): Any value in a range of 0 up to the RAM size.
        
        """
        DPxSetDoutBuffSize(buffer_size)  
            
            
            
    def getBufferSize(self):
        """Gets the Ram buffer size.
        
        This method allows the user to get the RAM buffer size used in schedules.
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetDoutBuffSize()




    def setScheduleOnset(self, onset):
        """Sets the schedule onset value.
        
        This method allows the user to set the nanosecond delay between schedule start and first sample.
        If no delay is required, this method doesn't need to be used. Default value is 0.

        Args:
            onset (int): Any positive value equal to or greater than 0.
        
        """
        DPxSetDoutSchedOnset(onset)          
            
            
            
    def getScheduleOnset(self):
        """Gets the schedule onset value.
        
        This method allows the user to get the schedule onset value used in schedules.
        The onset represents a nanosecond delay between schedule start and first sample.
        
        Returns:
            int: Any positive value equal to or greater than 0.

        """
        return DPxGetDoutSchedOnset()
    



    def setScheduleRate(self, rate, unit='hz'):
        """Sets the schedule rate.
        
        This method allows the user to set the schedule rate. Since the rate can be given 
        with different units, the method also needs to have a unit associated with the rate.

        If no delay is required, this method doesn't need to be used. Default value is 0.

        Args:
            rate (int): Any positive value equal to or greater than 0.
            unit (str): hz    : rate updates per second, maximum 10 MHz.
                        video : rate updates per video frame, maximum 10 MHz.
                        nano  : rate updates period in nanoseconds, minimum 100 ns.
        
        """
        DPxSetDoutSchedRate(rate, unit)
            
                    
    def getScheduleRate(self):
        """Gets the schedule rate value.
        
        This method allows the user to get the schedule rate value used in schedules.
        The rate represents the speed at which the schedule updates.
        
        Returns:
            int: Any positive value equal to or greater than 0.

        """
        schedule_rate = DPxGetDoutSchedRate()
        return schedule_rate[0]
    
    
    
    def getScheduleUnit(self):
        """Gets the schedule unit value.
        
        This method allows the user to get the schedule unit value used in schedules.
        
        Returns:
            int: Any positive value equal to or greater than 0.
            
        
        See Also:
            :class:`getScheduleRate`, :class:`setScheduleRate`

        """
        schedule_unit = DPxGetDoutSchedRate()
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
        DPxSetDoutSchedCount(count)          
            
            
            
    def getScheduleCount(self):
        """Gets the schedule count value.
        
        This method allows the user to get the current count for a schedule.
        
        Returns:
            int: Any positive value equal to or greater than 0.
            
        
        See Also:
            :class:`setScheduleCount`, :class:`setScheduleCountDown`
        """
        return DPxGetDoutSchedCount()       



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
            DPxEnableDoutSchedCountdown()
        else:
            DPxDisableDoutSchedCountdown()

                

    def isCountDownEnabled(self):
        """Verifies the schedule count down mode.

        Returns:
            enable (Bool): True if the schedule is decrementing at every sample, False otherwise.
            
        See Also:
            :class:`setScheduleCount`, :class:`stopSchedule`, :class:`setScheduleCountDown`
        
        """
        if DPxIsDoutSchedCountdown() !=0:
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
        DPxStartDoutSched()



    def stopSchedule(self):
        """Stops the active schedule for a given subsystem.

        Depending on how the schedules are configured, it may not be necessary to call this method. When a schedule is using a count down, it is not
        needed to stop the schedule.   
        
         
        See Also:
            :class:`startSchedule`, :class:`setReadAddress`, :class:`setBaseAddress`, :class:`setScheduleOnset`, :class:`setScheduleRate`,
            :class:`setScheduleCountDown`, :class:`setScheduleCount`
        
        """
        DPxStopDoutSched()        
        


    def isScheduleRunning(self):
        """Verifies if a schedule is currently running on the subsystem.

        Returns:
            schedule_running (Bool): True if a schedule is currently running, False otherwise.
            
        See Also:
            :class:`startSchedule`, :class:`stopSchedule`, :class:`getScheduleRunningState`
        
        """
        if DPxIsDoutSchedRunning() == 0:
            schedule_running = False
        else:
            schedule_running = True
        return schedule_running
    
    
    

    def getScheduleRunningState(self):
        """Gets the schedule state for the subsystem.

        Returns:
            schedule_state (str): "running" if a schedule is currently running, "stopped" otherwise.
            
        See Also:
            :class:`startSchedule`, :class:`stopSchedule`, :class:`isScheduleRunning`
        
        """
        if DPxIsDoutSchedRunning() == 0:
            self.schedule_state = "stopped"
        else:
            self.schedule_state = "running"
        return self.schedule_state
    
    

    def enablePixelMode(self):
        """Enables pixel mode.
        
        When this function is enabled, the digital outputs show the RGB value of first upper left pixel of the screen.
        In this case, digital outputs cannot be used for other purposes.
        This feature is only available on VIEWPixx with firmware revision 31 and higher.
                    
        See Also:
            :class:`disablePixelMode`, :class:`isPixelModeEnabled`
        """
        DPxEnableDoutPixelMode()
    
    
    
    
    def disablePixelMode(self):
        """Disables pixel mode.
        
        When this function is disabled, the digital ouputs do not show the RGB value of first upper left pixel of the screen.
        The digital outputs can then be used normally. This is the default mode.
        This feature is only available on VIEWPixx with firmware revision 31 and higher.
    
        See Also:
            :class:`enablePixelMode`, :class:`isPixelModeEnabled`
        """
        DPxDisableDoutPixelMode()
    
    
    
    
    def isPixelModeEnabled(self):
        """Verifies if the pixel mode is enabled on digital outputs.
        
        Returns:
            enable (Bool): True if the mode is enabled, False otherwise.
                    
        See Also:
            :class:`enablePixelMode`, :class:`disablePixelMode`
        """
        if DPxIsDoutPixelMode() !=0:
            enable = True
        else:
            enable = False 
        return enable