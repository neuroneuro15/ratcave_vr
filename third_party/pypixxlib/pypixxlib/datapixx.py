from dpxDevice import DpxDevice
from _libdpx import DPxUpdateRegCache, DPxSetVidMode, DPxGetVidMode
from vgaOut import VgaOut
from threeDFeatures import ThreeDFeatures 
from videoFeatures import VideoFeatures
from dualLinkOut import DualLinkOut
from analogIn import AnalogIn
from analogOut import AnalogOut
from audioOut import AudioOut
from audioIn import AudioIn
from digitalIn import DigitalIn
from digitalOut import DigitalOut


        
        
class DATAPixx(DpxDevice, VgaOut, VideoFeatures, ThreeDFeatures):    
    """ Class Definition for the DATAPixx Device.
    
    The bases defined below are the core subsystems attached to a DATAPixx devices. A DATAPixx
    device also has very specific subsystems which are used through handles. See the example bellow
    for more details.
         
    Note: 
        If you have a **Lite** version of the device, some of these handles will 
        not be available. The usage of the handles is as follows:
    
    >>> from pypixxlib.datapixx import DATAPixx
    >>> my_device = DATAPixx()
    >>> my_device.adc.function() # adc is the subsystem in this example.
    >>> my_device.BaseFunction() # A base function from one of the class' bases.
    
    Attributes:
        name: Name of the device.
        adc: Handle for the control of Analog In signal. See :doc:`analogIn`.
        dac: Handle for the control of Analog Out signal. See :doc:`analogOut`.
        audio: Handle for the audio controls. See :doc:`audioOut`.
        micro: Handle for the microphone controls. See :doc:`audioIn`.
        din: Handle for the control of Digital In signal. See :doc:`digitalIn`.
        dout: Handle for the control of Digital Out signal. See :doc:`digitalOut`.
        subsytems: A list of the available subsystems related to your physical device.
    """   
    def __init__(self):
        super(DATAPixx, self).__init__('DATAPixx')
        
        self.devsel = 10
        
        if 'Lite' in self.name:
            self._setLiteSubSystems()
        else:
            self._setFullSubSystems()
        
        DPxUpdateRegCache()
 
    def _setLiteSubSystems(self):
        
        self.din = DigitalIn()
        self.dout = DigitalOut()
        
        self.subsystems = ['Digital I/O']
        


    def _setFullSubSystems(self):
        
        self.adc = AnalogIn()
        self.dac = AnalogOut()
        self.audio = AudioOut()
        self.micro = AudioIn()
        self.din = DigitalIn()
        self.dout = DigitalOut()
        
        self.subsystems = ['General','Analog I/O', 'Audio I/O', 'Digital I/O']
 
    
class DATAPixx2(DpxDevice, DualLinkOut, VideoFeatures):    
    """ Class Definition for the DATAPixx2 Device.
    
    The bases defined below are the core subsystems attached to a DATAPixx2 devices. A DATAPixx2
    device also has very specific subsystems which are used through handles. See the example bellow
    for more details.
         
    Note: 
        If you have a **Lite** version of the device, some of these handles will 
        not be available. The usage of the handles is as follows:
    
    >>> from pypixxlib.datapixx import DATAPixx2
    >>> my_device = DATAPixx2()
    >>> my_device.adc.function() # adc is the subsystem in this example.
    >>> my_device.BaseFunction() # A base function from one of the class' bases.
    
    Attributes:
        name: Name of the device.
        adc: Handle f or the control of Analog In signal. See :doc:`analogIn`.
        dac: Handle for the control of Analog Out signal. See :doc:`analogOut`.
        audio: Handle for the audio controls. See :doc:`audioOut`.
        micro: Handle for the microphone controls. See :doc:`audioIn`.
        din: Handle for the control of Digital In signal. See :doc:`digitalIn`.
        dout: Handle for the control of Digital Out signal. See :doc:`digitalOut`.
        subsytems: A list of the available subsystems related to your physical device.
    """   
    def __init__(self):
        super(DATAPixx2, self).__init__('DATAPixx2')
        self.devsel = 50
        DPxUpdateRegCache()

        if 'Lite' in self.name:
            self._setLiteSubSystems()
        else:
            self._setFullSubSystems()
        
        
 
    def _setLiteSubSystems(self):
        
        self.din = DigitalIn()
        self.dout = DigitalOut()
        
        self.subsystems = ['General','Digital I/O']
        


    def _setFullSubSystems(self):
        
        self.adc = AnalogIn()
        self.dac = AnalogOut()
        self.audio = AudioOut()
        self.micro = AudioIn()
        self.din = DigitalIn()
        self.dout = DigitalOut()
        
        self.subsystems = ['General','Analog I/O', 'Audio I/O', 'Digital I/O']        
