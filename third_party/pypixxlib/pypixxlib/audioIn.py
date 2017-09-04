from _libdpx import DPxUpdateRegCache, DPxGetMicLeftValue, DPxGetMicRightValue, \
    DPxSetMicLRMode, DPxGetMicLRMode, DPxSetAudBuffBaseAddr, \
    DPxGetMicBuffBaseAddr, DPxSetMicBuffWriteAddr, DPxGetMicBuffWriteAddr, \
    DPxSetMicBuffSize, DPxGetMicBuffSize, DPxSetMicSchedOnset, \
    DPxGetMicSchedOnset, DPxSetMicSchedRate, DPxGetMicSchedRate, \
    DPxSetMicSchedCount, DPxGetMicSchedCount, DPxEnableMicSchedCountdown, \
    DPxDisableMicSchedCountdown, DPxIsMicSchedCountdown, DPxStartMicSched, \
    DPxStopMicSched, DPxIsMicSchedRunning, DPxEnableAudMicLoopback, \
    DPxDisableAudMicLoopback, DPxIsAudMicLoopback, DPxGetAudGroupDelay, \
    DPxSetMicSource, DPxGetMicSource, api_constants
from abc import ABCMeta, abstractmethod
from schedule import Schedule


class AudioIn(Schedule):
    """Class which implements the Microphone features.

    Any device which has Audio IN should instantiate this class. It contains all the necessary methods to use the
    audio inputs of a VPIxx device.
    """
    __metaclass__ = ABCMeta    
    
    def getValueLeft(self):
        """Gets the current value of the left channel.
        
        This method allows the user to get the 16-bit 2's complement signed value for left MIC channel.

        Returns:
            int: 16-bit 2's complement signed value.

        """
        return DPxGetMicLeftValue()
     
    def getValueRight(self):
        """Gets the current value of the right channel.
        
        This method allows the user to get the 16-bit 2's complement signed value for right MIC channel.

        Returns:
            int: 16-bit 2's complement signed value.

        """
        return DPxGetMicRightValue()
    
    def setScheduleBufferMode(self, mode):
        """Sets the schedule buffer storing mode.
        
        This method allows the user to configure how microphone left and right channels are stored to the schedule buffer.

        Args:
            mode (str): Any of the following predefined constants.\n
                - **mono** : Mono data is written to the schedule buffer. The average of Left/Right CODEC data.
                - **left** : Left data is written to the schedule buffer.
                - **right** : Right data is written to the schedule buffer.
                - **stereo** : Left and Right data are both written to the schedule buffer.
                        
        See Also:
            :class:`getScheduleBufferMode`
        
        """
        DPxSetMicLRMode(mode)

    def getScheduleBufferMode(self):
        """Gets the microphone Left/Right configuration mode.
        
        This method allows the user to set the microphone to one of the mono, left, right or stereo mode.
        
        Returns:
            String: Any of the following predefined constants.\n
                - **mono** : Mono data is written to the schedule buffer. The average of Left/Right CODEC data.
                - **left** : Left data is written to the schedule buffer.
                - **right** : Right data is written to the schedule buffer.
                - **stereo** : Left and Right data are both written to the schedule buffer.
                        
        See Also:
            :class:`setScheduleBufferMode`
        
        """
        return DPxGetMicLRMode()    
        
    def setBaseAddress(self, address):
        """Sets the Ram buffer start address.
        
        This method allows the user to set the RAM buffer start address used in schedules.
        The given address must be an even value.

        Args:
            address (int): Any value in a range of 0 up to the RAM size.
        
        """
        DPxSetAudBuffBaseAddr(address)        
            
    def getBaseAddress(self):
        """Gets the Ram buffer start address.
        
        This method allows the user to get the RAM buffer start address used in schedules.
        It should only be used if the user wants the schedules to wrap when it has reached its maximum size.
        When schedules are expected to wrap, the user should also use setBufferSize()
        
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetMicBuffBaseAddr()

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
        DPxSetMicBuffWriteAddr(address)           
                 
    def getWriteAddress(self):
        """Gets the Ram buffer write address.
        
        This method allows the user to get the RAM buffer write address used in schedules.
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetMicBuffWriteAddr()                
        
    def setBufferSize(self, buffer_size):
        """Sets the Ram buffer size.
        
        This method allows the user to set the RAM buffer size used in schedules. It should only be 
        used if the user wants the schedules to wrap when it has reached its maximum size. When 
        schedules are expected to wrap, the user should also use setBaseAddress()
        The given size is in byte and must be an even value.

        Args:
            buffer_size (int): Any value in a range of 0 up to the RAM size.
        
        """
        DPxSetMicBuffSize(buffer_size)      
            
    def getBufferSize(self):
        """Gets the Ram buffer size.
        
        This method allows the user to get the RAM buffer size used in schedules.
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetMicBuffSize()

    def setScheduleOnset(self, onset):
        """Sets the schedule onset value.
        
        This method allows the user to set the nanosecond delay between schedule start and first sample.
        If no delay is required, this method doesn't need to be used. Default value is 0.

        Args:
            onset (int): Any positive value equal to or greater than 0.
        
        """
        DPxSetMicSchedOnset(onset)       
                      
    def getScheduleOnset(self):
        """Gets the schedule onset value.
        
        This method allows the user to get the schedule onset value used in schedules.
        The onset represents a nanosecond delay between schedule start and first sample.
        
        Returns:
            int: Any positive value equal to or greater than 0.

        """
        return DPxGetMicSchedOnset()        

    def setScheduleRate(self, rate, unit='hz'):
        """Sets the schedule rate.
        
        This method allows the user to set the schedule rate. Since the rate can be given 
        with different units, the method also needs to have a unit associated with the rate.
        
        nanosecond delay between schedule start and first sample.
        If no delay is required, this method does not need to be used. Default value is 0.

        Args:
            rate (int): Any positive value equal to or greater than 0.
            unit (str): Any of the following predefined constants. \n
                        - **hz**    : samples per second, maximum 102.4 kHz.
                        - **video** : samples per video frame, maximum 102.4 kHz.
                        - **nano**  : sample period in nanoseconds, minimum 9750 ns.
        """
        DPxSetMicSchedRate(rate, unit)
                       
    def getScheduleRate(self):
        """Gets the schedule rate value.
        
        This method allows the user to get the schedule rate value used in schedules.
        The rate represents the speed at which the schedule updates.
        
        Returns:
            int: Any positive value equal to or greater than 0.

        """
        schedule_rate = DPxGetMicSchedRate()
        return schedule_rate[0]
    
    def getScheduleUnit(self):
        """Gets the schedule unit value.
        
        This method allows the user to get the schedule unit value used in schedules.
        
        Returns:
            int: Any positive value equal to or greater than 0.
            
        
        See Also:
            :class:`getScheduleRate`, :class:`setScheduleRate`

        """
        schedule_unit = DPxGetMicSchedRate()
        return schedule_unit[1]
    
    def setScheduleCount(self, count):
        """Sets the schedule count.
        
        This method allows the user to set the schedule count for a schedule with a fixed number of samples.
        In this case, the schedule will decrement at a given rate and stop when the count reaches 0.


        Args:
            count (int): Any positive value greater than 0.
            
                        
        See Also:
            :class:`getScheduleCount`, :class:`setScheduleCountDown`
        
        """
        DPxSetMicSchedCount(count) 
                 
    def getScheduleCount(self):
        """Gets the schedule count value.
        
        This method allows the user to get the current count for a schedule.
        
        Returns:
            int: Any positive value equal to or greater than 0.
            
        
        See Also:
            :class:`setScheduleCount`, :class:`setScheduleCountDown`

        """
        return DPxGetMicSchedCount()     

    def setScheduleCountDown(self, enable):
        """Sets the schedule count down mode.
        
        This method allows the user to enable or disable the countdown on a schedule.
        When enabled, the schedule decrements at the given rate and stops automatically when the count hits 0.
        When disabled, the schedule increments at the given rate and is stopped by calling ``stopSchedule()``.


        Args:
            enable (Bool): True if countdown is enabled, False otherwise.
        
        
        See Also:
            :class:`setScheduleCount`, :class:`stopSchedule`, :class:`isCountDownEnabled`
        
        """
        if enable == True:
            DPxEnableMicSchedCountdown()
        else:
            DPxDisableMicSchedCountdown()

    def isCountDownEnabled(self):
        """Verifies the schedule count down mode.

        Returns:
            Bool: True if the schedule is decrementing at every sample, False otherwise.
            
        See Also:
            :class:`setScheduleCount`, :class:`stopSchedule`, :class:`setScheduleCountDown`
        
        """
        if DPxIsMicSchedCountdown() !=0:
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
        DPxStartMicSched()

    def stopSchedule(self):
        """Stops the active schedule for a given subsystem.

        Depending on how the Schedules are configured, it may not be necessary to call this method. When a schedule is using a countdown, it is not
        required to stop the schedule.   
        
         
        See Also:
            :class:`startSchedule`, :class:`setWriteAddress`, :class:`setBaseAddress`, :class:`setScheduleOnset`, :class:`setScheduleRate`,
            :class:`setScheduleCountDown`, :class:`setScheduleCount`
        
        """
        DPxStopMicSched()        
        
    def isScheduleRunning(self):
        """Verifies if a schedule is currently running on the subsystem.

        Returns:
            Bool: True if a schedule is currently running, False otherwise.
            
        See Also:
            :class:`startSchedule`, :class:`stopSchedule`, :class:`getScheduleRunningState`
        
        """
        if DPxIsMicSchedRunning() == 0:
            schedule_running = False
        else:
            schedule_running = True
        return schedule_running
    
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
            DPxEnableAudMicLoopback()
        else:
            DPxDisableAudMicLoopback()               
            
    def isLoopbackEnabled(self):
        """Verifies the digital inputs and outputs loopback mode.

        Returns:
            enable (Bool): True if transitions are being stabilized, False otherwise.
            
        See Also:
            :class:`setLoopback`
        
        """
        if DPxIsAudMicLoopback() == 0:
            enable = False
        else:
            enable = True
        return enable 

    def getGroupDelay(self, sample_rate):
        """Gets the CODEC Audio OUT group delay in seconds.

        Returns:
            float: delay in seconds.
        
        """
        return DPxGetAudGroupDelay(sample_rate)
    
    
    def setMicSource(self, source, gain, dBUnits=0):
        """Sets the source for the MIC
        
        Select the source of the microphone input. Typical gain values would be around 100 for a
        microphone input, and probably 1 for line-level input.
        
        Args:
            source (int): One of the following: \n
                    - ``MIC``: Microphone level input.
                    - ``LINE``: Line level audio input.
            gain (int): The gain can take the following values depending on the scale: \n
                    - linear scale : [1, 1000]
                    - dB scale     : [0, 60] dB
            dBUnits (int, optional): Set non-zero to return the gain in dB. Defaults to 0.
        """
        return DPxSetMicSource(api_constants[source], gain, dBUnits)


    def getMicSource(self, dBUnits=0):
        """Gets the source and the gain of the microphone input.
        
        Args:
            dBUnits (int, optional): Set non-zero to return the gain in dB. Defaults to 0.
        
        Returns:
            A list containing the [gain value, microphone source]
             
        :Low-level C definition:
            ``int DPxGetMicSource(int DBUnits)``
        """

        return DPxGetMicSource(dBUnits)