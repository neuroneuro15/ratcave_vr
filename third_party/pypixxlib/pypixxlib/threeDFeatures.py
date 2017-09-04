
from abc import ABCMeta, abstractmethod

from _libdpx import DPxGetVidVesaPhase, \
    DPxSetVidVesaLeft, DPxSetVidVesaPhase, DPxSetVidVesaRight, DPxIsVidVesaLeft, \
    DPxSetVidVesaWaveform, DPxGetVidVesaWaveform




class ThreeDFeatures(object):
    """Implements the the different 3D features for your device.
    """ 
    __metaclass__ = ABCMeta
    def setVesaPhase(self, phase):
        """Sets the 8-bit unsigned phase of the VESA 3D waveform.

        Varying this phase from 0-255 will fine tune phase relationship between stereo video and 3D goggle switching.
        The following combinations have been found to work well:
           
        If you are using a VIEWPIxx/3D, you should set the ``phase`` to ``0x64``. If you
        are using a CTR with our DATAPixx, it should be set to ``0xF5``.
        
        Args:
            phase (int): Phase of the VESA 3D waveform
        """
        DPxSetVidVesaPhase(phase)
        
        
 
    def getVesaPhase(self):
        """Gets the 8-bit unsigned phase of the VESA 3D waveform.

        Returns:
            phase (int): Phase of the VESA 3D waveform
        """
        return DPxGetVidVesaPhase()


        
    def setVesaOutputSignalEye(self, eye):
        """Sets the VESA output signal eye.

        The VESA connector can output image signal on either left or right eye. This method
        allows the user to choose one.

        Args:
            eye (string): left if VESA connector it to output left-eye signal. right otherwise.
        """
        if eye.upper() == 'LEFT':                
            DPxSetVidVesaLeft()
        elif eye.upper() == 'RIGHT':
            DPxSetVidVesaRight()

            
    
    def getVesaOutputSignalEye(self):
        """Returns the eye on which the VESA outputs an image signal.

        Returns:
            eye (str): Eye on which VESA is outputting the signal.

        """
        if DPxIsVidVesaLeft() == 0:
            eye = 'right'
        else:
            eye = 'left'
        return eye



    def setVesaWaveform(self, waveform):
        """Sets the 8-bit unsigned phase of the VESA 3D waveform.

        Sets the waveform which will be sent to the DATAPixx VESA 3D connector

        Args:
            waveform (str): If you are using NVIDIA 3D Vision Glasses, you should set the ``Waveform`` to ``NVIDIA``. 
                            If you are using Crystaleyes Glasses, it should be set to ``CRYSTALEYES``. 
                            For a basic L/R square wave, it should be ``LR``.
        """
        DPxSetVidVesaWaveform(waveform)
        
        
 
    def getVesaWaveform(self):
        """Gets the waveform which is being sent to the VESA 3D connector.

        Returns:
            waveform (str): Phase of the VESA 3D waveform
        """
        return DPxGetVidVesaWaveform()
    
