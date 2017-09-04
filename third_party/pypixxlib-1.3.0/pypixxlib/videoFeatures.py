from abc import ABCMeta, abstractmethod

# from docutils.nodes import line

from _libdpx import DPxSetVidMode, DPxGetVidMode, DPxOpen, DPxClose, \
    DPxGetVidHTotal, DPxGetVidVTotal, DPxGetVidHActive, DPxGetVidVActive, \
    DPxGetVidVPeriod, DPxGetVidVFreq, DPxGetVidHFreq, DPxGetVidDotFreq, \
    DPxIsVidDviActive, DPxIsVidDviActiveDual, DPxIsVidDviLockable, \
    DPxIsVidOverClocked, DPxSetVidPsyncRasterLine, DPxGetVidPsyncRasterLine, \
    DPxEnableVidPsyncSingleLine, DPxDisableVidPsyncSingleLine, \
    DPxIsVidPsyncSingleLine, DPxEnableVidPsyncBlankLine, \
    DPxDisableVidPsyncBlankLine, DPxIsVidPsyncBlankLine, DPxSetVidClut, \
    DPxSetVidCluts, DPxEnableVidVesaBlueline, DPxDisableVidVesaBlueline, \
    DPxIsVidVesaBlueline




class VideoFeatures(object): 
    """Implements the video methods for most Devices.

    This Class implements video features used by all devices except the PROPixx.
    If a video feature can be used in a DATAPixx as well as a VIEWPixx, it is included in this Class.
    """
    __metaclass__ = ABCMeta
             
    def setVideoMode(self, mode):
        """Sets the video processing mode.

        This method allows the user to change the display mode of the VPixx device. Each mode changes how
        the input video signal is used to display the video on the display.

        Warning:
            Mode **RB24** is availible on VIEWPixx ONLY, revision 21 or higher.
        
        Args:
            mode (string): video mode is one of the following predefined constants: \n
                - **C24**:   Straight pass through from DVI 8-bit (or HDMI "deep" 10/12-bit) RGB to VGA 8/10/12-bit RGB
                - **L48**:   DVI RED[7:0] is used as an index into a 256-entry 16-bit RGB color lookup table
                - **M16**:   DVI RED[7:0] & GREEN[7:0] concatenate into a VGA 16-bit value sent to all three RGB components
                - **C48**:   Even/Odd pixel RED/GREEN/BLUE[7:0] concatenate to generate 16-bit RGB components at half the horizontal resolution
                - **L48D**:   DVI RED[7:4] & GREEN[7:4] concatenate to form an 8-bit index into a 256-entry 16-bit RGB color lookup table
                - **M16D**:   DVI RED[7:3] & GREEN[7:3] & BLUE[7:2] concatenate into a VGA 16-bit value sent to all three RGB components
                - **C36D**:   Even/Odd pixel RED/GREEN/BLUE[7:2] concatenate to generate 12-bit RGB components at half the horizontal resolution
                - **RB24**:   DVI RED[7:0] & GREEN[7:4] concatenate to form 12-bit RED value, DVI BLUE[7:0] & GREEN[3:0] concatenate to form 12-bit BLUE value, GREEN is forced to 0.

        """ 
        DPxSetVidMode(mode)



    def getVideoMode(self):
        """Gets the current video processing mode.

        This method allows the user to know what is the current display mode of the VPixx device.
 
        Warning:
            Mode **RB24** is availible on VIEWPixx ONLY, revision 21 or higher.       
        
        Returns:
            mode (string): video mode is one of the following predefined constants: \n
               - **C24**:    Straight pass through from DVI 8-bit (or HDMI "deep" 10/12-bit) RGB to VGA 8/10/12-bit RGB
               - **L48**:    DVI RED[7:0] is used as an index into a 256-entry 16-bit RGB color lookup table
               - **M16**:    DVI RED[7:0] & GREEN[7:0] concatenate into a VGA 16-bit value sent to all three RGB components
               - **C48**:    Even/Odd pixel RED/GREEN/BLUE[7:0] concatenate to generate 16-bit RGB components at half the horizontal resolution
               - **L48D**:   DVI RED[7:4] & GREEN[7:4] concatenate to form an 8-bit index into a 256-entry 16-bit RGB color lookup table
               - **M16D**:   DVI RED[7:3] & GREEN[7:3] & BLUE[7:2] concatenate into a VGA 16-bit value sent to all three RGB components
               - **C36D**:   Even/Odd pixel RED/GREEN/BLUE[7:2] concatenate to generate 12-bit RGB components at half the horizontal resolution
               - **RB24**:   DVI RED[7:0] & GREEN[7:4] concatenate to form 12-bit RED value, DVI BLUE[7:0] & GREEN[3:0] concatenate to form 12-bit BLUE value, GREEN is forced to 0
        """ 
        return DPxGetVidMode()         



    def getVideoHorizontalTotal(self):
        """Gets the total number of clocks per horizontal line.

        This method allows the user to get the total number of clocks in one horizontal scan line. 
        This value includes the horizontal blanking interval.
        
        
        Returns:
                number (int): number of clocks per horizontal lines.
        
        """
        return DPxGetVidHTotal()
    
    
    
    def getVideoVerticalTotal(self):
        """Gets the total number of clocks per vertical line.

        This method allows the user to get the total number of clocks in one vertical frame. 
        This value includes the vertical blanking interval.
        
        Returns:
            number (int): number of clocks per vertical lines.
        
        """ 
        return DPxGetVidVTotal()
    
    
    
    def getVisiblePixelsPerHorizontalLine(self):
        """Gets the number of visible pixels in one horizontal scan line.
        
        Returns:
            number (int): Number of pixels.
        
        """ 
        return DPxGetVidHActive() 



    def getVisibleLinePerVerticalFrame(self):
        """Gets the number of visible lines in one vertical frame.
        
        Returns:
            number (int): Number of visible lines.
        
        """
        return DPxGetVidVActive()
    


    def getVideoVerticalFramePeriod(self):
        """Gets the video vertical frame period.
        
        Returns:
            period (int): Period in nanoseconds.
        
        """
        return DPxGetVidVPeriod()
        


    def getVideoVerticalFrameFrequency(self):
        """Gets the video vertical frame frequency.
        
        Returns:
            frequency (int): frequency in Hz.
        
        """
        return DPxGetVidVFreq() 
            


    def getVideoHorizontalLineFrequency(self):
        """Gets the video horizontal line frequency.
        
        Returns:
            frequency (int): frequency in Hz.
        
        """
        return DPxGetVidHFreq()   
            


    def getVideoDotFrequency(self):
        """Gets the video dot frequency (pixel sync.).
        
        Returns:
            frequency (int): frequency in Hz.
        
        """
        return DPxGetVidDotFreq()     
            


    def isVideoOnDvi(self):
        """Verifies if the device is currently receiving video data over DVI link.

        
        Returns:
            state (Bool): True if the device is currently receiving video data over DVI link, otherwise False.
        
        """
        if DPxIsVidDviActive() == 0:
            state = False
        else:
            state = True
        return state     
            


    def isVideoOnDualLinkDvi(self):
        """Verifies if the device is currently receiving video data over dual-link DVI.

        
        Returns:
            state (Bool): True if the device is receiving over dual-link DVI, otherwise False.
        
        """
        if DPxIsVidDviActiveDual() == 0:
            state = False
        else:
            state = True
        return state     
            


    def isVideoTimingDisplayable(self):
        """Verifies if the device can display the incoming data.

        This method allows the user to know if the device is currently receiving video whose timing can be directly driven by the display.

        
        Returns:
            state (Bool): True if the device can display the video signal, otherwise False.
        
        """
        if DPxIsVidDviLockable() == 0:
            state = False
        else:
            state = True
        return state     
            


    def isVideoTimingTooHigh(self):
        """Verifies if the video clock frequency is too high.

        This method allows the user to know if the clock frequency of the incoming data is too high for the device to display.
        
        Returns:
            state (Bool): True if the clock frequency is too high, otherwise False.
        
        """
        if DPxIsVidOverClocked() == 0:
            state = False
        else:
            state = True
        return state
    


    def setRasterLinePixelSync(self, line):
        """Sets the raster line on which the pixel synchronization sequence is expected.

        Args:
            line (int): line on which the pixel synchronization sequence is expected.
        
        """
        try:
            DPxSetVidPsyncRasterLine(line)
        except:
            pass
        
        
 
    def getRasterLinePixelSync(self):
        """Gets the raster line on which the pixel sync sequence is expected.

        Returns:
            line (int): line on which pixel sync sequence is expected.
        
        """
        return DPxGetVidPsyncRasterLine()



    def setPixelSyncOnSingleLine(self, enable):
        """Sets the Video pixel synchronization on a single raster line.

        Allows the user to set the video pixel synchronization on a single raster line or on any raster line.

        Args:
            enable (Bool): True to enable pixel synchronization on a single raster line. False to allow synchronization 
                            on any line.
        
        """
        if enable == True:                
            DPxEnableVidPsyncSingleLine()
        else:
            DPxDisableVidPsyncSingleLine()

            
    
    def isPixelSyncOnSingleLineEnabled(self):
        """Verifies the pixel synchronization mode state.

        Allows the user to know if the pixel synchronization is done on a single raster line or on any line.

        Returns:
            enable (Bool): True if pixel synchronization is only recognized on a single raster line, False otherwise.
        
        """
        if DPxIsVidPsyncSingleLine() == 0:
            enable = False
        else:
            enable = True
        return enable



    def setPixelSyncLineBlack(self, enable):
        """Sets the Video pixel synchronization black line mode.

        Allows the user to display the raster line black for video pixel synchronization. When enabled, the raster line
        is always displayed black. When disabled, the raster line is displayed normally.

        Args:
            enable (Bool): True to enable the black line mode. False to disable it on any line.
        """
        if enable == True:                
            DPxEnableVidPsyncBlankLine()
        else:
            DPxDisableVidPsyncBlankLine()

            
    
    def isPixelSyncLineBlackEnabled(self):
        """Verifies the pixel synchronization black line mode state.

        Allows the user to know if the raster line displayed black mode is enabled or not. When ``enable`` is True, the raster line displayed black mode is enabled.
        When disabled, the raster line is displayed normally.

        
        Returns:
            enable (Bool): True if black line mode is enabled, False otherwise.
        
        """
        if DPxIsVidPsyncBlankLine() == 0:
            enable = False
        else:
            enable = True
        return enable
    
    
    def restoreLinearCLUT(self):
        CLUT = [[],[],[]]
        for i in range(256):
            CLUT[0].append(i*256)
            CLUT[1].append(i*256)
            CLUT[2].append(i*256)
        for i in range(256):
            CLUT[0].append(i*256)
            CLUT[1].append(i*256)
            CLUT[2].append(i*256)
        DPxSetVidCluts(CLUT)
        
            
    def setCLUT(self, CLUT):
        """Sets the video color look up table data to be displayed.
        
        Pass 3x256 16-bit video data, [[R1...R256], [G1...G256], [B1...B256]].
        Or if you want a different CLUT for the console and the test display,        
        Pass a 3x512 16-bit video, [[R1...R512], [G1...G512], [B1...B512]].
        
        Warning:
            Since this is 16-bits, the colors RGB must vary between 0 and 65535.
            
        This functions returns immediately, and CLUT is implemented at next vertical blanking interval.

        
        Args:
            CLUT (list of lists of int): Color look-up table .
        
        """
        if len(CLUT) is not 3:
            raise "CLUT needs to be 3 lists of R, G and B of size 256 or 512"
            return
        size_r = len(CLUT[0])
        if len(CLUT[1]) is not size_r or len(CLUT[2]) is not size_r:
            raise "Need to have amount of elements in all colors"
            return
        if size_r is not 256 and size_r is not 512:
            raise "Your CLUT is too small or big. Allowed sizes are 256 or 512."
            return
        
        if size_r is 256:
            DPxSetVidClut(CLUT)
        else:
            DPxSetVidCluts(CLUT)
                     
                     

    def setVideoVesaBlueline(self, enable):
        """Sets the Video blue line mode.

        When enabled, the VESA 3D output interprets the middle pixel on the last raster line as a blue line code.
        When disabled, the VESA 3D output is not dependent on video content.

        
        Args:
            enable (Bool): Activate or deactivate the blue line mode.
        
        """
        if enable == True:                
            DPxEnableVidVesaBlueline()
        else:
            DPxDisableVidVesaBlueline()

            
    
    def isVideoVesaBluelineEnabled(self):
        """Verifies the video blue line mode state.

        
        Returns:
            enable (Bool): True if blue line mode is enabled, False otherwise.
        
        """
        if DPxIsVidVesaBlueline() == 0:
            enable = False
        else:
            enable = True
        return enable