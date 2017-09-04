from abc import ABCMeta, abstractmethod

from _libdpx import DPxEnableVidHorizSplit, DPxDisableVidHorizSplit, \
    DPxIsVidHorizSplit, DPxAutoVidHorizSplit, DPxEnableVidHorizOverlay, \
    DPxDisableVidHorizOverlay, DPxIsVidHorizOverlay, DPxEnableVidVertStereo, \
    DPxDisableVidVertStereo, DPxAutoVidVertStereo, DPxIsVidVertStereo




class VgaOut(object):
    """Implements the methods available for a DATAPixx 1.
    
    Attributes:
        name: definition
    """        
    __metaclass__ = ABCMeta
    def setVideoHorizontalSplit(self, enable=None):
        """Sets the Video horizontal split mode.

        When this feature is enabled, VGA 1 shows left half of video image while VGA 2 shows right half of video image. The two VGA outputs are perfectly synchronized.
        When this feature is disabled, VGA 1 and VGA 2 both show the entire video image (hardware video mirroring). The device can also be set to automatically
        split video across the two VGA outputs if the horizontal resolution is at least twice the vertical resolution.
        This is considered as the automatic mode or default mode.

        Args:
            enable (Bool, optional): True to enable the horizontal split, false to disable it. When no argument is passed, automatic mode is set.
        """
        if enable == True:                
            DPxEnableVidHorizSplit()
        elif enable == False:
            DPxDisableVidHorizSplit()
        else:
            DPxAutoVidHorizSplit()
            
            
    
    def isVideoHorizontalSplitEnabled(self):
        """Returns the video horizontal split mode state.

        Returns:
            enable (Bool): True if video is being split across the two VGA outputs. False otherwise
        """
        if DPxIsVidHorizSplit() == 0:
            enable = False
        else:
            enable = True
        return enable      
            
 

    def setVideoHorizontalOverlay(self, enable=None):
        """Sets the Video horizontal overlay mode.

        VGA 1 and VGA 2 both show an overlay composite of the left/right halves of the video image.
        Horizontal overlay is disabled

        Args:
            enable (Bool): True to enable the horizontal overlay, false to disable it.
        """
        if enable == True:                
            DPxEnableVidHorizOverlay()
        else:
            DPxDisableVidHorizOverlay()
            
            
    
    def isVideoHorizontalOverlayEnabled(self):
        """Returns the video horizontal overlay mode state.

        Returns:
            enable (Bool): True if the left/right halves of the video image are being overlayed. False otherwise
        """
        if DPxIsVidHorizOverlay() == 0:
            enable = False
        else:
            enable = True
        return enable   



    def setVideoVerticalStereo(self, enable=None):
        """Sets the Video vertical stereo mode.

        When this feature is enabled, the top/bottom halves of the input image are output in two sequential video frames.
        VESA L/R output is set to 1 when first frame (left eye) is displayed, and set to 0 when second frame (right eye) is displayed.
        
        When this feature is disabled, the images are displayed normally. The device can also enable vertical stereo automatically
        if vertical resolution > horizontal resolution. This is considered as the automatic mode or default mode.

        Args:
            enable (Bool): True to enable the vertical stereo mode, false to disable it. When no argument is passed, automatic mode is set.
        """
        if enable == True:                
            DPxEnableVidVertStereo()
        elif enable == False:
            DPxDisableVidVertStereo()
        else:
            DPxAutoVidVertStereo()
            
            
    
    def isVideoVerticalStereoEnabled(self):
        """Returns the video vertical stereo mode state.

        Returns:
            enable (Bool): True if stereo mode is enabled. False otherwise
        """
        if DPxIsVidVertStereo() == 0:
            enable = False
        else:
            enable = True
        return enable