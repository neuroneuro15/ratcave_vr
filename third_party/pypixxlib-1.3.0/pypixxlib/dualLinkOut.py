from abc import ABCMeta, abstractmethod

from _libdpx import DPxVideoScope




class DualLinkOut(object):
    """ Class Definition for the Dual Link Out for each Device.
    """   
    __metaclass__ = ABCMeta
    
    def exportVideoScopeToFile(self, file_pointer):
        #VIEWPixx video source analysis.
        #file_pointer (str): Where the file to analyze is located.
        DPxVideoScope(file_pointer)             
