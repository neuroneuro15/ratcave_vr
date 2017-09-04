
from abc import ABCMeta, abstractmethod




class Schedule(object):
    """ This class represents the possible Schedule
    
    In this class, we defined possible schedules and all their related functions.
    
    """
    __metaclass__ = ABCMeta
    
    val = []
    range = []
    volt = []
    buff_ref = []
    schedule_data = [0,0,0,0]
    schedule_address = [0,0,0,0]
    data_unit = 'Dec'
    rate_unit = 'Hz'
         
    def __init__(self):
        pass  

    def setRateUnit(self, rate=None):
        if rate is None:
            self.rate_unit = 'Hz'
        else:
            self.rate_unit = rate
                    
    def setDataUnit(self, unit):
        """Sets the data unit for the sub device.

        Args:
            unit (string): ``Dec`` for decimal representation or ``Hex`` for hexadecimal representation.
        
        """
        if unit.lower() is 'dec' or unit.lower() is 'hex':
            self.data_unit = unit
        
        
        
    def getDataUnit(self):
        """Gets the data unit for the sub device.

        returns:
            unit (string): ``Dec`` for decimal representation or ``Hex`` for hexadecimal representation.
        """
        return self.data_unit
  
       

    def setSchedData(self, field, value, addr):
        self.schedule_data = value

    def getSchedData(self, field=None):
        return self.schedule_data