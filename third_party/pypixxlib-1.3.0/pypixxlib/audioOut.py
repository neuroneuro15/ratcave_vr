from _libdpx import DPxUpdateRegCache, DPxSetAudCodecOutLeftVolume, \
    DPxSetAudCodecOutRightVolume, DPxSetAudCodecOutVolume, \
    DPxGetAudCodecOutLeftVolume, DPxGetAudCodecOutRightVolume, \
    DPxSetAudCodecSpeakerLeftVolume, DPxSetAudCodecSpeakerRightVolume, \
    DPxSetAudCodecSpeakerVolume, DPxGetAudCodecSpeakerLeftVolume, \
    DPxGetAudCodecSpeakerRightVolume, DPxSetAudLRMode, DPxGetAudLRMode, \
    DPxSetAudBuffBaseAddr, DPxGetAudBuffBaseAddr, DPxSetAudBuffReadAddr, \
    DPxGetAudBuffReadAddr, DPxSetAudBuffSize, DPxGetAudBuffSize, \
    DPxSetAudSchedOnset, DPxGetAudSchedOnset, DPxSetAudSchedRate, \
    DPxGetAudSchedRate, DPxSetAudSchedCount, DPxGetAudSchedCount, \
    DPxEnableAudSchedCountdown, DPxDisableAudSchedCountdown, \
    DPxIsAudSchedCountdown, DPxStartAudSched, DPxStopAudSched, \
    DPxIsAudSchedRunning, DPxSetAuxBuffBaseAddr, DPxGetAuxBuffBaseAddr, \
    DPxSetAuxBuffReadAddr, DPxGetAuxBuffReadAddr, DPxSetAuxBuffSize, \
    DPxGetAuxBuffSize, DPxSetAuxSchedOnset, DPxGetAuxSchedOnset, \
    DPxSetAuxSchedRate, DPxGetAuxSchedRate, DPxSetAuxSchedCount, \
    DPxGetAuxSchedCount, DPxEnableAuxSchedCountdown, DPxDisableAuxSchedCountdown, \
    DPxIsAuxSchedCountdown, DPxStartAuxSched, DPxStopAuxSched, \
    DPxIsAuxSchedRunning, DPxGetAudGroupDelay, DPxGetAudCodecSpeakerVolume, \
    DPxGetAudCodecOutVolume, DPxInitAudCodec, DPxSetAudBuff, \
    DPxSetAudRightVolume, DPxSetAudRightValue, DPxSetAudLeftVolume, \
    DPxSetAudVolume, DPxGetAudRightVolume, DPxGetAudLeftVolume, DPxGetAudVolume, \
    DPxSetAudSched, DPxWriteRam
from abc import ABCMeta, abstractmethod
import math
from schedule import Schedule


class AudioOut(Schedule):
    """Class which implements the AUDIO features.

    Any device which has Audio OUT should implement this class. It contains all the necessary methods to use the
    audio outputs of a VPIxx device.
    """
    __metaclass__ = ABCMeta    
    
    def initializeCodec(self):
        """This needs to be called once to configure initial audio CODEC state.        
        """
        
        return DPxInitAudCodec()
    
    def setAudioBuffer(self, buff_addr, buff_size):
        """
        Sets base address, reads address and buffer size for AUD schedules.
    
        This function is a shortcut which assigns Size/BaseAddr/ReadAddr
        
        Args:
            buff_addr (int): Base addresss.
            buff_size (int): Buffer size.
        """
        return DPxSetAudBuff(buff_addr, buff_size)
        
    def setCodecVolumeRight(self, volume, unit):
        """Sets the codec volume of the right channel.
        
        Args:
            volume (float): Range 0-1 or dB.
            unit (float): 0 for linear or 1 for dB.
                        
        See Also:
            :class:`getVolumeRight`, :class:`getVolumeLeft`, :class:`setVolumeRight`, :class:`setVolumeLeft`, :class:`setVolume`,
            :class:`setCodecVolume`, :class:`setCodecVolumeLeft`, :class:`getCodecVolumeRight`, :class:`getCodecVolume`, 
            :class:`getCodecVolumeLeft`
        
        """
        DPxSetAudCodecOutLeftVolume(volume, unit)
            
    def setCodecVolumeLeft(self, volume, unit):
        """Sets the codec volume of the left channel.
        
        Args:
            volume (float): Range 0-1 or dB.
            unit (float): 0 for linear or 1 for dB.
                        
        See Also:
            :class:`getVolumeRight`, :class:`getVolumeLeft`, :class:`setVolumeRight`, :class:`setVolumeLeft`, :class:`setVolume`,
            :class:`setCodecVolume`, :class:`getCodecVolumeLeft`, :class:`setCodecVolumeRight`, :class:`getCodecVolume`, 
            :class:`getCodecVolumeLeft`, :class:`getCodecVolumeRight`
        
        """
        DPxSetAudCodecOutLeftVolume(volume, unit)
        
    def setCodecVolume(self, volume, unit):
        """Sets the codec volume of for both left and right channels.
        
        Args:
            volume (float): Range 0-1 or dB.
            unit (float): 0 for linear or 1 for dB.
                        
        See Also:
            :class:`getVolumeRight`, :class:`getVolumeLeft`, :class:`setVolumeRight`, :class:`setVolumeLeft`, :class:`setVolume`,
            :class:`setCodecVolume`, :class:`setCodecVolumeLeft`, :class:`setCodecVolumeRight`, :class:`getCodecVolume`, 
            :class:`getCodecVolumeLeft`, :class:`getCodecVolumeRight`
    
        """
        DPxSetAudCodecOutVolume(volume, unit)
                    
    def getCodecVolumeLeft(self, unit=0):
        """Gets the current codec volume of the left channel.
    
        Args:
            unit (int): Set non-zero to return the gain in dB. Defaults to 0.
            
        Returns:
            float: Range 0 to 1.
        """
        return DPxGetAudCodecOutLeftVolume(unit)

    def getCodecVolumeRight(self, unit=0):
        """Gets the current codec volume of the right channel.

        Args:
            unit (int): Set non-zero to return the gain in dB. Defaults to 0.
            
        Returns:
            float: Range 0 to 1.
        """
        return DPxGetAudCodecOutRightVolume(unit)
    
    def getCodecVolume(self, unit=0):
        """Gets the current codec volume of the right channel.
        
        Args:
            unit (int): Set non-zero to return the gain in dB. Defaults to 0.

        Returns:
            float: Range 0 to 1.
        """
        return DPxGetAudCodecOutVolume(unit)
    
    def setCodecSpeakerRightVolume(self, volume, unit):
        """Sets the speaker volume of the right channel.
        
        Args:
            volume (float): Range 0-1 or dB.
            unit (float): 0 for linear or 1 for dB.
                        
        See Also:
            :class:`getCodecSpeakerLeftVolume`, :class:`getCodecSpeakerVolume`, :class:`getCodecSpeakerRightVolume`, :class:`setCodecSpeakerLeftVolume`, :class:`setCodecSpeakerVolume`
        """
        DPxSetAudCodecSpeakerRightVolume(volume, unit)
    
    def setCodecSpeakerLeftVolume(self, volume, unit=0):
        """Sets the speaker volume of the left channel.
        
        Args:
            volume (float): Range 0-1 or dB.
            unit (float): 0 for linear or 1 for dB.
                        
        See Also:
            :class:`getCodecSpeakerRightVolume`, :class:`getCodecSpeakerVolume`, :class:`getCodecSpeakerRightVolume`, :class:`setCodecSpeakerLeftVolume`, :class:`setCodecSpeakerVolume`
        
        """
        DPxSetAudCodecSpeakerLeftVolume(volume, unit)
    
    def setCodecSpeakerVolume(self, volume, unit=0):
        """Sets the speaker volume of both Left and right channels.
        
        Args:
            volume (float): Range 0-1 or dB.
            unit (float): 0 for linear or 1 for dB.
                        
        See Also:
           :class:`getCodecSpeakerLeftVolume`, :class:`getCodecSpeakerRightVolume`, :class:`getCodecSpeakerRightVolume`, :class:`setCodecSpeakerLeftVolume`, :class:`setCodecSpeakerVolume`
        
        """
        DPxSetAudCodecSpeakerVolume(volume, unit)
        
    def getCodecSpeakerRightVolume(self, unit=0):
        """Gets the current speaker volume of the right channel.

        Args:
            unit (float): 0 for linear or 1 for dB.
            
        Returns:
            float: Range 0 to 1.

        """
        return DPxGetAudCodecSpeakerRightVolume(unit)
        
    def getCodecSpeakerLeftVolume(self, unit):
        """Gets the current speaker volume of the left channel.

        Args:
            unit (float): 0 for linear or 1 for dB.
            
        Returns:
            float: Range 0 to 1.

        """
        return DPxGetAudCodecSpeakerLeftVolume(unit)
        
    def getCodecSpeakerVolume(self, unit):  
        """Gets the current speaker volume of the right and left channel.

        Args:
            unit (float): 0 for linear or 1 for dB.
            
        Returns:
            A tuple containing floats: [left Speaker Volume, Right speaker Volume]

        """
        return DPxGetAudCodecSpeakerVolume(unit)
    
    def setVolumeRight(self, volume):
        """ Sets volume for the Right audio channels, range 0-1
    
        Args:
            volume (float): Value for the desired volume, between 0 and 1.
        """
        return DPxSetAudRightVolume(volume)
            
    def setVolumeLeft(self, volume):
        """ Sets volume for the Left audio channels, range 0-1
    
        Args:
            volume (float): Value for the desired volume, between 0 and 1.
        """
        return DPxSetAudLeftVolume(volume)
        
    def setVolume(self, volume):
        """ Sets volume for the Left and Right audio channels, range 0-1
    
        Args:
            volume (float): Value for the desired volume, between 0 and 1.
        """
        return DPxSetAudVolume(volume)
        
    def getVolumeRight(self):
        """Get volume for the Right audio output channel, range 0-1
        """
        return DPxGetAudRightVolume()

    def getVolumeLeft(self):
        """Get volume for the Left audio output channel, range 0-1
        """
        return DPxGetAudLeftVolume()

    def getVolume(self):
        """Gets volume for both Left/Right audio channels
    
        Returns:
            A tuple containing floats: [left Speaker Volume, Right speaker Volume]
        """
        return DPxGetAudVolume()
    
    def setLeftRightMode(self, mode):
        """Sets how audio data is updated by schedules.

        Args:
            mode (str): Any of the following predefined constants.\n
                - **mono** : Left schedule data goes to left and right channels.
                - **left** : Each schedule data goes to left channel only.
                - **right** : Each schedule data goes to right channel only.
                - **stereo1** : Pairs of Left data are copied to left/right channels.
                - **stereo2** : Left data goes to left channel, Right data goes to right.
                        
        See Also:
            :class:`getLeftRightMode`
        
        """
        DPxSetAudLRMode(mode)

    def getLeftRightMode(self):
        """Gets the audio schedule update mode.
        
        Returns:
            String: Any of the following predefined constants.\n
                - **mono** : Left schedule data goes to left and right channels.
                - **left** : Each schedule data goes to left channel only.
                - **right** : Each schedule data goes to right channel only.
                - **stereo1** : Pairs of Left data are copied to left/right channels.
                - **stereo2** : Left data goes to left channel, Right data goes to right.
                        
        See Also:
            :class:`setScheduleBufferMode`
        
        """ 
        return DPxGetAudLRMode()    
        
    def setBaseAddressLeft(self, value):
        """Sets the Ram buffer start address.
        
        This method allows the user to set the RAM buffer start address used in schedules.
        The given address must be an even value.

        Args:
            address (int): Any value in a range of 0 up to the RAM size.
        """
        DPxSetAudBuffBaseAddr(value)         
            
    def getBaseAddressLeft(self):
        """Gets the Ram buffer start address.
        
        This method allows the user to get the RAM buffer start address used in schedules.
        It should only be used if the user wants the schedules to wrap when it has reached its maximum size.
        When schedules are expected to wrap, the user should also use setBufferSize()
        
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetAudBuffBaseAddr()   

    def setReadAddressLeft(self, address):
        """Sets the Ram buffer read address.
        
        This method allows the user to set the RAM buffer read address used in schedules.
        This address is used by the schedule to know where the data should be first read from.
        The schedule will then read the following data to the address following the RAM 
        buffer read address. 
        
        The given address must be an even value.

        Args:
            address (int): Any value in a range of 0 up to the RAM size.
        
        """
        DPxSetAudBuffReadAddr(address)   
            
    def getReadAddressLeft(self):
        """Gets the Ram buffer read address.
        
        This method allows the user to get the RAM buffer read address used in schedules.
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetAudBuffReadAddr()           

    def setBufferSizeLeft(self, buffer_size):
        """Sets the Ram buffer size.
        
        This method allows the user to set the RAM buffer size used in schedules. It should only be 
        used if the user wants the schedules to wrap when it has reached its maximum size. When 
        schedules are expected to wrap, the user should also use setBaseAddress()
        The given size is in bytes and must be an even value.

        Args:
            buffer_size (int): Any value in a range of 0 up to the RAM size.
        
        """
        DPxSetAudBuffSize(buffer_size)      
                
    def getBufferSizeLeft(self):
        """Gets the Ram buffer size.
        
        This method allows the user to get the RAM buffer size used in schedules.
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetAudBuffSize()
    
    def setAudioSchedule(self, onset, rateValue, rateUnits, count):
        """Sets AUD schedule onset, count and rate.
        
        This function is a shortcut which assigns Onset/Rate/Count. If Count > 0, enables Countdown mode.
        
        Args:
            onset (int): Schedule onset.
            rateValue (int): Rate value.
            rateUnits (string): Usually ``hz``. Can also be ``video`` to update every ``rateValue`` video frames or ``nano`` to update every ``rateValue`` nanoseconds.
            count (int): Schedule count.
        """
        return DPxSetAudSched(onset, rateValue, rateUnits, count)
    
    def stopSchedule(self):
        """Stops the active schedule for a given subsystem.

        Depending on how the schedules are configured, it may not be necessary to call this method. When a schedule is using a countdown, it is not
        required to stop the schedule.   
        
        """
        DPxStopAudSched()  
    
    def setScheduleOnsetLeft(self, onset):
        """Sets the schedule onset value.
        
        This method allows the user to set the nanosecond delay between schedule start and first sample.
        If no delay is required, this method does not need to be used. Default value is 0.

        Args:
            onset (int): Any positive value equal or greater to 0.
        
        """
        DPxSetAudSchedOnset(onset)      
            
    def getScheduleOnsetLeft(self):
        """Gets the schedule onset value.
        
        This method allows the user to get the schedule onset value used in schedules.
        The onset represents a nanosecond delay between schedule start and first sample.
        
        Returns:
            int: Any positive value equal or greater to 0.
        """
        return DPxGetAudSchedOnset()  


    def setScheduleRateLeft(self, rate, unit='hz'):
        """Sets the schedule rate.
        
        This method allows the user to set the schedule rate. Since the rate can be given 
        with different units, the method also needs to have a unit associated with the rate.
        If no delay is required, this method does not need to be used. Default value is 0.

        Args:
            rate (int): Any positive value equal or greater to 0.
            unit (str): hz    : samples per second, maximum 96 kHz. \n
                        video : samples per video frame, maximum 96 kHz.
                        nano  : sample period in nanoseconds, minimum 10417 ns.
        
        """
        DPxSetAudSchedRate(rate, unit)          
            
           
    def getScheduleRateLeft(self):
        """Gets the schedule rate value.
        
        This method allows the user to get the schedule rate value used in schedules.
        The rate represents the speed at which the schedule updates.
        
        Returns:
            int: Any positive value equal or greater to 0.

        """
        schedule_rate = DPxGetAudSchedRate()
        return schedule_rate[0]
    
    def getScheduleUnitLeft(self):
        """Gets the schedule unit value.
        
        This method allows the user to get the schedule unit value used in schedules.
        
        Returns:
            int: Any positive value equal or greater to 0.
            
        
        See Also:
            :class:`getScheduleRateLeft`, :class:`setScheduleRateLeft`

        """
        schedule_unit = DPxGetAudSchedRate()
        return schedule_unit[1]
    
    def setScheduleCountLeft(self, count):
        """Sets the schedule count.
        
        This method allows the user to set the schedule count for a schedule with a fixed number of samples.
        In which case, the schedule will decrement at a given rate and stop when the count reaches 0.


        Args:
            count (int): Any positive value greater than 0.
            
                        
        See Also:
            :class:`getScheduleUnitLeft`, :class:`setScheduleCountDownLeft`
        
        """
        DPxSetAudSchedCount(count)       
            
    def getScheduleCountLeft(self):
        """Gets the schedule count value.
        
        This method allows the user to get the current count for a schedule.
        
        Returns:
            int: Any positive value equal or greater to 0.
            
        
        See Also:
            :class:`setScheduleCountLeft`, :class:`setScheduleCountDownLeft`
        """
        return DPxGetAudSchedCount()        
    
    def setScheduleCountDownLeft(self, enable):
        """Sets the schedule countdown mode.
        
        This method allows the user to enable or disable the countdown on a schedule.
        When enabled, the schedule decrements at the given rate and stops automatically when the count hits 0.
        When disabled, the schedule increments at the given rate and is stopped by calling stopSchedule().


        Args:
            enable (Bool): True if countdown is enabled, False otherwise.
        
        
        See Also:
            :class:`setScheduleCountLeft`, :class:`stopScheduleLeft`, :class:`isCountDownEnabledLeft`
        
        """
        if enable == True:
            DPxEnableAudSchedCountdown()
        else:
            DPxDisableAudSchedCountdown()

    def isCountDownEnabledLeft(self):
        """Verifies the schedule countdown mode.

        Returns:
            enable (Bool): True if the schedule is decrementing at every sample, False otherwise.
            
        See Also:
            :class:`setScheduleCountLeft`, :class:`stopScheduleLeft`, :class:`setScheduleCountDownLeft`
        
        """
        if DPxIsAudSchedCountdown() !=0:
            enable = True
        else:
            enable = False 
        return enable        

    def startScheduleLeft(self):
        """Starts a schedule.

        Schedules may be configured in different ways, affecting their behavior. Before a schedule is started, the user should
        make sure that it is properly set in the right mode.   
        
         
        See Also:
            :class:`stopScheduleLeft`, :class:`setReadAddressLeft`, :class:`setBaseAddressLeft`, :class:`setScheduleOnsetLeft`, :class:`setScheduleRateLeft`,
            :class:`setScheduleCountDownLeft`, :class:`setScheduleCountLeft`
        
        """
        DPxStartAudSched()

    def stopScheduleLeft(self):
        """Stops the active schedule for a given subsystem.

        Depending on how the schedules are configured, it may not be necessary to call this method. When a schedule is using a countdown, it is not
        required to stop the schedule.   
        
         
        See Also:
            :class:`startScheduleLeft`, :class:`setReadAddressLeft`, :class:`setBaseAddressLeft`, :class:`setScheduleOnsetLeft`, :class:`setScheduleRateLeft`,
            :class:`setScheduleCountDownLeft`, :class:`setScheduleCountLeft`
        
        """
        DPxStopAudSched()        
        
    def isScheduleRunningLeft(self):
        """Verifies if a schedule is currently running on the subsystem.

        Returns:
            schedule_running (Bool): True if a schedule is currently running, False otherwise.
            
        See Also:
            :class:`startScheduleLeft`, :class:`stopScheduleLeft`, :class:`getScheduleRunningStateLeft`
        
        """
        if DPxIsAudSchedRunning() == 0:
            schedule_running = False
        else:
            schedule_running = True
        return schedule_running
    
    def getScheduleRunningStateLeft(self):
        """Gets the schedule state for the subsystem.

        Returns:
            schedule_state (str): "running" if a schedule is currently running, "stopped" otherwise.
            
        See Also:
            :class:`startScheduleLeft`, :class:`stopScheduleLeft`, :class:`isScheduleRunningLeft`
        
        """
        if DPxIsAudSchedRunning() == 0:
            self.schedule_state = "stopped"
        else:
            self.schedule_state = "running"
        return self.schedule_state
   
    def setBaseAddressRight(self, value):
        """Sets the Ram buffer start address.
        
        This method allows the user to set the RAM buffer start address used in schedules.
        The given address must be an even value.

        Args:
            address (int): Any value in a range of 0 up to the RAM size.
        
        """
        DPxSetAuxBuffBaseAddr(value)
       
            
    def getBaseAddressRight(self):
        """Gets the Ram buffer start address.
        
        This method allows the user to get the RAM buffer start address used in schedules.
        It should only be used if the user wants the schedules to wrap when it has reached its maximum size.
        When schedules are expected to wrap, the user should also use setBufferSize().
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetAuxBuffBaseAddr()  

    def setReadAddressRight(self, address):
        """Sets the Ram buffer read address.
        
        This method allows the user to set the RAM buffer read address used in schedules.
        This address is used by the schedule to know where the data should be first read from.
        The schedule will then read the following data to the address following the RAM 
        buffer read address. 
        
        The given address must be an even value.

        Args:
            address (int): Any value in a range of 0 up to the RAM size.
        
        """       
        DPxSetAuxBuffReadAddr(address)      
            
    def getReadAddressRight(self):
        """Gets the Ram buffer read address.
        
        This method allows the user to get the RAM buffer read address used in schedules.
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetAuxBuffReadAddr()
        
    def setBufferSizeRight(self, buffer_size):
        """Sets the Ram buffer size.
        
        This method allows the user to set the RAM buffer size used in schedules. It should only be 
        used if the user wants the schedules to wrap when it has reached its maximum size. When 
        schedules are expected to wrap, the user should also use setBaseAddress()
        The given size is in byte and must be an even value.

        Args:
            buffer_size (int): Any value in a range of 0 up to the RAM size.
        
        """
        return DPxSetAuxBuffSize(buffer_size)       
              
    def getBufferSizeRight(self):
        """Gets the Ram buffer size.
        
        This method allows the user to get the RAM buffer size used in schedules.
        
        Returns:
            int: Any value in a range of 0 up to the RAM size.

        """
        return DPxGetAuxBuffSize()

    def setScheduleOnsetRight(self, onset):
        """Sets the schedule onset value.
        
        This method allows the user to set the nanosecond delay between schedule start and first sample.
        If no delay is required, this method does not need to be used. Default value is 0.

        Args:
            onset (int): Any positive value equal or greater to 0.
        
        """
        DPxSetAuxSchedOnset(onset)         
             
    def getScheduleOnsetRight(self):
        """Gets the schedule onset value.
        
        This method allows the user to get the schedule onset value used in schedules.
        The onset represents a nanosecond delay between schedule start and first sample.
        
        Returns:
            int: Any positive value equal or greater to 0.

        """
        return DPxGetAuxSchedOnset()    

    def setScheduleRateRight(self, rate, unit='hz'):
        """Sets the schedule rate.
        
        This method allows the user to set the schedule rate. Since the rate can be given 
        with different units, the method also needs to have a unit associated with the rate.
        If no delay is required, this method does not need to be used. Default value is 0.

        Args:
            rate (int): Any positive value equal or greater to 0.
            unit (str): hz    : samples per second, maximum 96 kHz. \n
                        video : samples per video frame, maximum 96 kHz.
                        nano  : sample period in nanoseconds, minimum 10417 ns.
        
        """
        return DPxSetAuxSchedRate(rate, unit)      
                      
    def getScheduleRateRight(self):
        """Gets the schedule rate value.
        
        This method allows the user to get the schedule rate value used in schedules.
        The rate represents the speed at which the schedule updates.
        
        Returns:
            int: Any positive value equal or greater to 0.

        """
        schedule_rate = DPxGetAuxSchedRate()
        return schedule_rate[0]
    
    def getScheduleUnitRight(self):
        """Gets the schedule unit value.
        
        This method allows the user to get the schedule unit value used in schedules.
        
        Returns:
            int: Any positive value equal or greater to 0.
        
        See Also:
            :class:`getScheduleRateRight`, :class:`setScheduleRateRight`

        """
        schedule_unit = DPxGetAuxSchedRate()
        return schedule_unit[1]
    
    def setScheduleCountRight(self, count):
        """Sets the schedule count.
        
        This method allows the user to set the schedule count for a schedule with a fixed number of samples.
        In which case, the schedule will decrement at a given rate and stop when the count reaches 0.


        Args:
            count (int): Any positive value greater than 0.
            
                        
        See Also:
            :class:`getScheduleCountRight`, :class:`setScheduleCountDownRight`
        
        """
        DPxSetAuxSchedCount(count)         
            
    def getScheduleCountRight(self):
        """Gets the schedule count value.
        
        This method allows the user to get the current count for a schedule.
        
        Returns:
            int: Any positive value equal or greater to 0.
            
        
        See Also:
            :class:`setScheduleCountRight`, :class:`setScheduleCountDownRight`

        """
        return DPxGetAuxSchedCount()      

    def setScheduleCountDownRight(self, enable):
        """Sets the schedule countdown mode.
        
        This method allows the user to enable or disable the countdown on a schedule.
        When enabled, the schedule decrements at the given rate and stops automatically when the  count hits 0.
        When disabled, the schedule increments at the given rate and is stopped by calling stopSchedule().

        Args:
            enable (Bool): True if countdown is enabled, False otherwise.
        
        
        See Also:
            :class:`setScheduleCountRight`, :class:`stopScheduleRight`, :class:`isCountDownEnabledRight`
        
        """
        if enable == True:
            DPxEnableAuxSchedCountdown()
        else:
            DPxDisableAuxSchedCountdown()

    def isCountDownEnabledRight(self):
        """Verifies the schedule countdown mode.

        Returns:
            enable (Bool): True if the schedule is decrementing at every sample, False otherwise.
            
        See Also:
            :class:`setScheduleCountRight`, :class:`stopScheduleRight`, :class:`setScheduleCountDownRight`
        
        """
        if DPxIsAuxSchedCountdown() !=0:
            enable = True
        else:
            enable = False 
        return enable        

    def startScheduleRight(self):
        """Starts a schedule.

        Schedules may be configured in different ways, affecting their behavior. Before a schedule is started, the user should
        make sure that it is properly set in the right mode.   
        
         
        See Also:
            :class:`stopScheduleRight`, :class:`setReadAddressRight`, :class:`setBaseAddressRight`, :class:`setScheduleOnsetRight`, :class:`setScheduleRateRight`,
            :class:`setScheduleCountDownRight`, :class:`setScheduleCountRight`
        
        """
        DPxStartAuxSched()
        
    def stopScheduleRight(self):
        """Stops the active schedule for a given subsystem.

        Depending on how the schedules are configured, it may not be necessary to call this method. When a schedule is using a countdown, it is not
        required to stop the schedule.   
        
         
        See Also:
            :class:`startScheduleRight`, :class:`setReadAddressRight`, :class:`setBaseAddressRight`, :class:`setScheduleOnsetRight`, :class:`setScheduleRateRight`,
            :class:`setScheduleCountDownRight`, :class:`setScheduleCountRight`
        
        """
        
        DPxStopAuxSched()        
        
    def isScheduleRunningRight(self):
        """Verifies if a schedule is currently running on the subsystem.

        Returns:
            schedule_running (Bool): True if a schedule is currently running, False otherwise.
            
        See Also:
            :class:`startScheduleRight`, :class:`stopScheduleRight`, :class:`getScheduleRunningStateRight`
        
        """
        if DPxIsAuxSchedRunning() == 0:
            schedule_running = False
        else:
            schedule_running = True
        return schedule_running
    
    def getScheduleRunningStateRight(self):
        """Gets the schedule state for the subsystem.

        Returns:
            schedule_state (str): "running" if a schedule is currently running, "stopped" otherwise.
            
        See Also:
            :class:`startScheduleRight`, :class:`stopScheduleRight`, :class:`isScheduleRunningRight`
        
        """
        if DPxIsAuxSchedRunning() == 0:
            self.schedule_state = "stopped"
        else:
            self.schedule_state = "running"
        return self.schedule_state

    def getGroupDelay(self, sample_rate):
        """Gets the CODEC Audio OUT group delay in seconds.

        Returns:
            float: delay in seconds.
        
        """
        return DPxGetAudGroupDelay(sample_rate)
    
    def beep(self, volume=0.5, time=1, frequency=40000):
        """Beep bop beep bop bop beep beep beep.
        
        Args:
            volume (float): Value between 0 and 1 of the desired volume.
            time (int): Time factor for the beep duration.
            
        """
        DPxInitAudCodec()
        audioVolume = int(32767/2)
        SinVal = 0.19634954 #(2*3.14159265)/32
        sound_buffer = []
        for i in range(32):
            sound_buffer.append(int(audioVolume * math.sin(i * SinVal)))
                # Configure how audio Left/Right channels are updated by schedule data
        DPxWriteRam(DPxGetAudBuffBaseAddr(), sound_buffer)
        DPxSetAudVolume(volume)
        
        DPxSetAudBuff(DPxGetAudBuffBaseAddr(), 64)
        DPxSetAudSched(0, frequency, 'hz', int(16000*time))
        DPxStartAudSched()
        DPxUpdateRegCache()
