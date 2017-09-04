"""
Description:
This module is a wrapper of VPixx low-level library for Python.
It provides all functions found in "Libdpx.h", as well as the error codes "defined".
The first section is the list of all functions available to the user.
The second section is the list of all error codes.
The last section provides short descriptions for each error codes.


This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


Copyright (C) 2008-2017 VPixx Technologies
"""
import platform, os
import ctypes
from ctypes.util import find_library
import sys

sys_platform = platform.system()
os_64bit = sys.maxsize > 2**32
path = os.path.dirname(os.path.realpath(__file__))
if sys_platform == 'Windows':
    if os_64bit:
        DPxDll = ctypes.CDLL(os.path.join(path,"libdpx_x64.dll"))
    else:
        DPxDll = ctypes.CDLL(os.path.join(path,"libdpx.dll"))
elif sys_platform == 'Linux':
    DPxDll = ctypes.cdll.LoadLibrary(os.path.join(path,"libdpx.so")) 
elif (sys_platform == 'Darwin') or (sys_platform == 'Mac'):
    try:
        DPxDll = ctypes.cdll.LoadLibrary(os.path.join(path,"libdpx.dylib"))
    except:
        DPxDll = ctypes.cdll.LoadLibrary(os.path.join(path,"libdpx_64bit.dylib"))
else:
    raise Exception('OS Not Recognized') 





Open = DPxDll['DPxOpen']
Open.restype = None
def DPxOpen():
    """Opens VPixx devices.
    
    Must be called before any other DPx functions.

    :Low-level C definition:
        ``void DPxOpen()``
    
    """
    Open()


GetNbrDevices = DPxDll['DPxGetNbrDevices']
def DPxGetNbrDevices():
    return GetNbrDevices()


close = DPxDll['DPxClose']
close.restype = None
def DPxClose():
    """Close currently selected VPixx device.
    
    :Low-level C definition:
        ``void DPxClose()``
    
    """
    close()



updateRegCache = DPxDll['DPxUpdateRegCache'] 
updateRegCache.restype = None
def DPxUpdateRegCache():
    """Updates the local register cache.
    
    DPxWriteRegCache, then readback registers over USB into local cache
    
    :Low-level C definition:
        ``void DPxUpdateRegCache()``
    
    """
    updateRegCache()



ReadRam = DPxDll['DPxReadRam']
def DPxReadRam(address, length):
    """Reads a block of VPixx RAM into a local buffer.
    
    Args:
        address (int): Any even value equal to or greater than zero.
        length (int): Any value from zero to the RAM size.
        
    Returns:
        list: Values taken from RAM.

    
    :Low-level C definition:
        ``void DPxReadRam(unsigned address, unsigned length, void* buffer)``
        
    
    :Example:
    
    >>> from _libdpx import *
    >>> 
    >>> DPxOpen()
    >>> 
    >>> # Here is a list with the data to write in RAM.
    >>> data = [1,2,3,4,5,6]
    >>> DPxWriteRam(address= 42, int_list= data)
    >>> 
    >>> DPxUpdateRegCache()
    >>> 
    >>> print'DPxReadRam() = ', DPxReadRam(address= 42, length= 6)
    >>> 
    >>> DPxClose()
    
    """
    RetVal = []
    int_list = [0]*length
    int_size = ctypes.sizeof(ctypes.c_ushort)
    item_count = len(int_list)
    total_size = int_size * item_count
    packed_data = (ctypes.c_ushort * item_count)(*int_list)
    ReadRam(ctypes.c_uint(address), ctypes.c_ushort(total_size), packed_data)

    for i in range(length):
        RetVal.append(packed_data[i])
        
    return RetVal




WriteRam = DPxDll['DPxWriteRam']
WriteRam.restype = None
def DPxWriteRam(address, int_list):
    """Writes a local buffer into VPixx RAM.
    
    Args:
        address (int): Any even value equal to or greater than zero.
        int_list (int): ``int_list`` is a list which will fill the RAM data. The length of RAM used is based on the
                        length of ``int_list``. It can't be greater than RAM size.
    
    :Low-level C definition:
        ``void DPxWriteRam(unsigned address, unsigned length, void* buffer)``
    
    See Also:
        :class:`DPxGetRamSize`
        
        
    :Example:
    
    >>> from _libdpx import *
    >>> 
    >>> DPxOpen()
    >>> 
    >>> # Here is a list with the data to write in RAM.
    >>> data = [1,2,3,4,5,6]
    >>> DPxWriteRam(address= 42, int_list= data)
    >>> 
    >>> DPxUpdateRegCache()
    >>> 
    >>> print'DPxReadRam() = ', DPxReadRam(address= 42, length= 6)
    >>> 
    >>> DPxClose()
    
    """
    if type(int_list) is list:
        int_size = ctypes.sizeof(ctypes.c_ushort)
        item_count = len(int_list)
        total_size = int_size * item_count
        packed_data = (ctypes.c_ushort * item_count)(*int_list)
        WriteRam(ctypes.c_uint(address), ctypes.c_ushort(total_size), packed_data) 
    else:
        WriteRam(ctypes.c_uint(address), ctypes.sizeof(int_list), ctypes.byref(int_list))
    



writeRegCache = DPxDll['DPxWriteRegCache']
writeRegCache.restype = None
def DPxWriteRegCache():
    """Write local register cache to VPixx device over USB.
    
    :Low-level C definition:
        ``void DPxWriteRegCache()``
    
    """
    writeRegCache()



writeRegCacheAfterVideoSync = DPxDll['DPxWriteRegCacheAfterVideoSync']                 
writeRegCacheAfterVideoSync.restype = None
def DPxWriteRegCacheAfterVideoSync():
    """Write local register cache to VPixx device over USB on the next video frame.
    
    This function is like DPxWriteRegCache, but the device only writes the registers on leading edge of next vertical sync pulse.
    
    :Low-level C definition:
        ``void DPxWriteRegCacheAfterVideoSync()``
    
    """
    writeRegCacheAfterVideoSync()



updateRegCacheAfterVideoSync = DPxDll['DPxUpdateRegCacheAfterVideoSync']              
updateRegCacheAfterVideoSync.restype = None
def DPxUpdateRegCacheAfterVideoSync():
    """Updates local register cache with VPixx device.
    
    This function is like DPxUpdateRegCache, but the device only writes the registers on the leading edge
    of the next vertical sync pulse.
    
    :Low-level C definition:
        ``void DPxUpdateRegCacheAfterVideoSync()``
    
    """
    updateRegCacheAfterVideoSync()




writeRegCacheAfterPixelSync = DPxDll['DPxWriteRegCacheAfterPixelSync']
writeRegCacheAfterPixelSync.restype = None
def DPxWriteRegCacheAfterPixelSync(nPixels, pixelData, timeout):
    """Write local register cache to VPixx device over USB.
    
    This function is like DPxWriteRegCache, but it waits for a pixel sync sequence.
    
    Args:
        nPixels (int): The number of pixels.
        pixelData (list): The requested pattern for PSync.
        timeout (int): Maximum time to wait before a PSync.
        
    :Low-level C definition:
        ``void DPxWriteRegCacheAfterPixelSync(int nPixels, unsigned char* pixelData, int timeout)``
    
    """
    p_pixelData = ctypes.c_char_p(pixelData)
    writeRegCacheAfterPixelSync(nPixels, ctypes.byref(p_pixelData), timeout)
    


spiRead = DPxDll['DPxSpiRead']
spiRead.restype = None
def DPxReadProductionInfo(address=None):
    if not(address):
        if DPxIsDatapixx():
            address = 0x1F0000
        else:
            address = 0x7F0000
    
    try:
        p_readBuffer = ctypes.create_string_buffer(256)
        spiRead(ctypes.c_int(address), ctypes.c_int(256), ctypes.byref(p_readBuffer), None)
        text = p_readBuffer.value.split(', ')
        text[0] = text[0].strip()
        
        text[1] = text[1].split('S/N:')[1]        
        text[1] = text[1].strip()
        
        text[2] = text[2].split('Shipping date:')[1]
        text[2] = text[2].strip()
        
        text[3] = text[3].split('Assembly REV:')[1]
        text[3] = text[3].strip()
        
        info = {'Part Number': text[0],
                'S/N':text[1],
                'Shipping Date':text[2],
                'Assembly REV': text[3]}
        
        temp = info['Shipping Date'].split()
        temp[0] = temp[0].strip()
        info['Expiration Date'] = temp[0] +" "+ temp[1] +" "+ str(int(temp[2])+2)
        
        if '\n' in info['Assembly REV']:
            info['Assembly REV'] = (info['Assembly REV'].split('\n'))[0]
    except:
        info = {'Part Number': 'Not found',
                'S/N':'Not found',
                'Shipping Date':'Not found',
                'Expiration Date':'Not found',
                'Assembly REV':'Not found'}
    return info


def DPxSpiRead(address, nReadBytes, buffer=None):
    if not(buffer):
        p_readBuffer = ctypes.create_string_buffer(nReadBytes)
        spiRead(ctypes.c_int(address), ctypes.c_int(nReadBytes), ctypes.byref(p_readBuffer), None)
        return_value = (ctypes.c_ubyte * nReadBytes).from_buffer_copy(p_readBuffer)
        return return_value
    else:
        try:
            spiRead(ctypes.c_int(address), ctypes.c_int(nReadBytes), ctypes.byref(buffer), None)
            return True
        except:
            return False

    
spiWrite = DPxDll['DPxSpiWrite'] 
spiWrite.restype = ctypes.c_int 
def DPxSpiWrite(address, writeBuffer):
    return spiWrite(address, ctypes.sizeof(writeBuffer), ctypes.byref(writeBuffer), None)


spiErase = DPxDll['DPxSpiErase']
spiErase.restype = ctypes.c_int 
def DPxSpiErase(address, n_byte):
    return spiErase(address, n_byte, None)


spiModify = DPxDll['DPxSpiModify']  
spiModify.restype = None 
def DPxSpiModify(address, nWriteBytes, writeBuffer):
    spiModify(address, nWriteBytes, ctypes.byref(writeBuffer))



updateRegCacheAfterPixelSync = DPxDll['DPxUpdateRegCacheAfterPixelSync']  
updateRegCacheAfterPixelSync.restype = None 
def DPxUpdateRegCacheAfterPixelSync(nPixels, pixelData, timeout):
    """Writes local register cache to VPixx device over USB, using Pixel Sync timing.
    
    This function is like DPxUpdateRegCache, but waits for a pixel sync sequence before executing.
    
    Args:
        nPixels (int): The number of pixels
        pixelData (list): The requested pattern for PSynx
        timeout (int): Maximum time to wait before a PSync.
        
    :Low-level C definition:
        ``void DPxUpdateRegCacheAfterPixelSync(int nPixels, unsigned char* pixelData, int timeout)``
    """
    p_pixelData = ctypes.c_char_p(pixelData)
    updateRegCacheAfterPixelSync(nPixels, ctypes.byref(p_pixelData), timeout)
    
    

isDatapixx = DPxDll['DPxIsDatapixx']
isDatapixx.restype = ctypes.c_int
def DPxIsDatapixx():
    """Verifies if the device is a DATAPixx.
    
    Returns:
        int: Non-zero if a DATAPixx was found, zero otherwise.
        
    :Low-level C definition:
        ``int DPxIsDatapixx()``
    
    """
    return isDatapixx()



isDatapixx2 = DPxDll['DPxIsDatapixx2']
isDatapixx2.restype = ctypes.c_int
def DPxIsDatapixx2():
    """Verifies if the device is a DATAPixx2.
    
    Returns:
        int: Non-zero if a DATAPixx2 was found, zero otherwise.
        
    :Low-level C definition:
        ``int DPxIsDatapixx2()``
    
    """
    return isDatapixx2()


detectDevice = DPxDll['DPxDetectDevice']
detectDevice.restype = ctypes.c_int
def DPxDetectDevice(devsel):
    """Verifies if a specific device exists in the system.
    
    Args:
        devsel (string): Any of the predefined constants. \n
            - **DATAPixx**: DATAPixx.
            - **DATAPixx2**: DATAPixx2.
            - **VIEWPixx**: VIEWPixx.
            - **PROPixx Ctrl**: PROPixx Controller.
            - **PROPixx**: PROPixx.
                
    Returns:
        int: Non-zero if the device exists, 0 if the device does not exist.
    
    :Low-level C definition:
        ``int DPxDetectDevice(int devsel)``
    
    """
    return detectDevice(api_constants[devsel.upper().replace(" ", "")])



selectDevice = DPxDll['DPxSelectDevice']
selectDevice.restype = ctypes.c_int
def DPxSelectDevice(devsel):
    """Selects which of the device found in the system should be used.
    
    Args:
        devsel (string): Any of the predefined constants.\n
            - **Auto**: Lets the low-level choose the device.
            - **DATAPixx**: DATAPixx.
            - **DATAPixx2**: DATAPixx2.
            - **VIEWPixx**: VIEWPixx.
            - **PROPixx Ctrl**: PROPixx Controller.
            - **PROPixx**: PROPixx.
                
    Returns:
        int: Non-zero if the device exists, 0 if the device does not exist.
    
    :Low-level C definition:
        ``int DPxSelectDevice(int)``
    
    """
    return selectDevice(api_constants[devsel.upper().replace(" ", "")])


selectDeviceSubName = DPxDll['DPxSelectDeviceSubName']
selectDeviceSubName.restype = ctypes.c_int
def DPxSelectDeviceSubName(devsel, name):
    """Select which VPixx device to access.
    
    Args:
        devsel (string): Any of the predefined constants.\n
            - **Auto**: Lets the low-level choose the device.
            - **DATAPixx**: DATAPixx.
            - **DATAPixx2**: DATAPixx2.
            - **VIEWPixx**: VIEWPixx.
            - **PROPixx Ctrl**: PROPixx Controller.
            - **PROPixx**: PROPixx.
        name (string): Must me a valid custom device name.\n
                
    Returns:
        int: Non-zero if the device exists, 0 if the device does not exist.
    
    :Low-level C definition:
        ``int DPxSelectDeviceSubName(int, char*)``
    
    """
    p_name = ctypes.create_string_buffer(name)
    return selectDeviceSubName(api_constants[devsel.upper().replace(" ", "")], p_name)


selectSysDevice = DPxDll['DPxSelectSysDevice']
selectSysDevice.restype = ctypes.c_int
def DPxSelectSysDevice(devsel):
    return selectDevice(api_constants[devsel.upper().replace(" ", "")])



isReady = DPxDll['DPxIsReady']
isReady.restype = ctypes.c_int
def DPxIsReady():
    """Verifies if the current device is ready to use.
                
    Returns:
        int: Non-zero if the device is ready to use, zero otherwise.
    
    :Low-level C definition:
        ``int DPxIsReady()``
    
    """
    return isReady()



getID = DPxDll['DPxGetID']
getID.restype = ctypes.c_int 
def DPxGetID():
    """Gets the VPixx device identifier code.
                
    Returns:
        int: Value higher than 0.
    
    :Low-level C definition:
        ``int DPxGetID()``
    
    """
    return getID()

 
 
isViewpixx = DPxDll['DPxIsViewpixx']
isViewpixx.restype = ctypes.c_int
def DPxIsViewpixx():
    """Verifies if the device is a VIEWPixx.
    
    Returns:
        int: Non-zero if a VIEWPixx (VIEWPixx, VIEWPixx /EEG or VIEWPixx /3D) is detected, zero otherwise.
        
    :Low-level C definition:
        ``int DPxIsViewpixx()``
    
    """
    return isViewpixx()



isViewpixx3D = DPxDll['DPxIsViewpixx3D']
isViewpixx3D.restype = ctypes.c_int
def DPxIsViewpixx3D():
    """Verifies if the device is a VIEWPixx3D.
    
    Returns:
        int: Non-zero if a VIEWPixx3D was found, zero otherwise.
        
    :Low-level C definition:
        ``int DPxIsViewpixx3D()``
    
    """
    return isViewpixx3D()



isViewpixxEeg = DPxDll['DPxIsViewpixxEeg']
isViewpixxEeg.restype = ctypes.c_int 
def DPxIsViewpixxEeg():
    """Verifies if the device is a VIEWPixxEEG.
    
    Returns:
        int: Non-zero if a VIEWPixxEEG was found, zero otherwise.
        
    :Low-level C definition:
        ``int DPxIsViewpixxEeg()``
    
    """
    return isViewpixxEeg()     


  
isPropixxCtrl = DPxDll['DPxIsPropixxCtrl']
isPropixxCtrl.restype = ctypes.c_int
def DPxIsPropixxCtrl():
    """Verifies if the device is a PROPixx Controller.
    
    Returns:
        int: Non-zero if a PROPixx Controller was found, zero otherwise.
        
    :Low-level C definition:
        ``int DPxIsPropixxCtrl()``
    
    """
    return isPropixxCtrl()  



isPropixx = DPxDll['DPxIsPropixx']
isPropixx.restype = ctypes.c_int 
def DPxIsPropixx():
    """Verifies if the device is a PROPixx.
    
    This function will not detect the PROPixx Controller.
    
    
    Returns:
        int: Non-zero if the device exists, 0 if the device does not exist.
        
    :Low-level C definition:
        ``int DPxIsPropixx()``
    
    """
    return isPropixx()



isTrackpixx = DPxDll['DPxIsTrackpixx']
isTrackpixx.restype = ctypes.c_int 
def DPxIsTrackpixx():
    """Verifies if the device is a TRACKPixx.
    
    Returns:
        int: Non-zero if a TRACKPixx was found. Else if not.
        
    :Low-level C definition:
        ``int DPxIsTrackpixx()``
    
    """
    return isTrackpixx()



getRamSize = DPxDll['DPxGetRamSize']
getRamSize.restype = ctypes.c_uint  
def DPxGetRamSize():
    """Gets the number of bytes of RAM in the VPixx device.
                
    Returns:
        int: Value higher than 0.
    
    :Low-level C definition:
        ``int DPxGetRamSize()``
    
    """
    return getRamSize()



getPartNumber = DPxDll['DPxGetPartNumber']
getPartNumber.restype = ctypes.c_int
def DPxGetPartNumber():
    """Gets the integer part number of the VPixx Device.
                
    Returns:
        int: Value higher than 0.
    
    :Low-level C definition:
        ``int DPxGetPartNumber()``
    
    """
    return getPartNumber()



getFirmwareRev = DPxDll['DPxGetFirmwareRev']
getFirmwareRev.restype = ctypes.c_int
def DPxGetFirmwareRev():
    """Gets the VPixx Device firmware revision.
                
    Returns:
        int: Value higher than 0.
    
    :Low-level C definition:
        ``int DPxGetFirmwareRev()``
    
    """
    return getFirmwareRev()



getSupplyVoltage = DPxDll['DPxGetSupplyVoltage']
getSupplyVoltage.restype = ctypes.c_double  
def DPxGetSupplyVoltage():
    """Gets the voltage being supplied from +5V supply.
                
    Returns:
        float: Value higher than 0 in Volt.
    
    :Low-level C definition:
        ``double DPxGetSupplyVoltage()``
    
    """
    return getSupplyVoltage()



getSupplyCurrent = DPxDll['DPxGetSupplyCurrent']
getSupplyCurrent.restype = ctypes.c_double   
def DPxGetSupplyCurrent():
    """Gets the current being supplied from the 5V power supply.
                
    Returns:
        float: Value higher than 0 in Amperes.
    
    :Low-level C definition:
        ``double DPxGetSupplyCurrent()``
    
    """
    return getSupplyCurrent()



getSupply2Voltage = DPxDll['DPxGetSupply2Voltage']
getSupply2Voltage.restype = ctypes.c_double
def DPxGetSupply2Voltage():
    """Gets the voltage being supplied from the 12V power supply.
                
    Returns:
        float: Value higher than 0 in Volts.
    
    :Low-level C definition:
        ``double DPxGetSupply2Voltage()``
    
    """
    return getSupply2Voltage()



getSupply2Current = DPxDll['DPxGetSupply2Current']
getSupply2Current.restype = ctypes.c_double
def DPxGetSupply2Current():
    """Gets the current being supplied from the +12V power supply.
                
    Returns:
        float: Value higher than 0 in Amperes.
    
    :Low-level C definition:
        ``double DPxGetSupply2Current()``
    
    """
    return getSupply2Current()



is5VFault = DPxDll['DPxIs5VFault']
is5VFault.restype = ctypes.c_int  
def DPxIs5VFault():
    """Verifies the state of the 5V power supply.
    
    This function allows the user to know if the VESA and Analog +5V input/output pins are trying to draw more than 500 mA.
                
    Returns:
        int: 0 if the current is normal, non-zero otherwise (too much current drawn).
    
    :Low-level C definition:
        ``int DPxIs5VFault()``
    
    """
    return is5VFault()



isPsyncTimeout = DPxDll['DPxIsPsyncTimeout']
isPsyncTimeout.restype = ctypes.c_int 
def DPxIsPsyncTimeout():
    """Verifies if a timeout occurred on the pixel synchronization.
    
    This function allows the user to know if the VESA and Analog +5V input/output pins are trying to draw more than 500 mA.
                
    Returns:
        int: Non-zero if a timeout occurred, zero otherwise.
    
    :Low-level C definition:
        ``int DPxIsPsyncTimeout()``
    
    """
    return isPsyncTimeout()



isRamOffline = DPxDll['DPxIsRamOffline']
isRamOffline.restype = ctypes.c_int
def DPxIsRamOffline():
    """Verifies if the RAM controller is offline.
                
    Returns:
        int: Zero if the RAM is online, non-zero otherwise.
    
    :Low-level C definition:
        ``int DPxIsRamOffline()``
    
    """
    return isRamOffline()



getTempCelcius = DPxDll['DPxGetTempCelcius']
getTempCelcius.restype = ctypes.c_double
def DPxGetTempCelcius():
    """Gets the temperature inside a VPixx device chassis.
    
    When used with a PROPixx, this function gets the temperature of the Receiver DVI.
    When used with other devices, it gets the chassis temperature.
                
    Returns:
        float: Temperature in degrees Celsius.
    
    :Low-level C definition:
        ``double DPxGetTempCelcius()``
    
    """
    return getTempCelcius()



getTemp2Celcius = DPxDll['DPxGetTemp2Celcius']
getTemp2Celcius.restype = ctypes.c_double
def DPxGetTemp2Celcius():
    """Gets the temperature inside a VPixx device.
    
    This function gets the board temperature of any VPixx device except the DATAPixx. 
                
    Returns:
        float: Temperature in degrees Celsius.
    
    :Low-level C definition:
        ``double DPxGetTemp2Celcius()``
    
    """
    return getTemp2Celcius()



getTemp3Celcius = DPxDll['DPxGetTemp3Celcius']
getTemp3Celcius.restype = ctypes.c_double
def DPxGetTemp3Celcius():
    """Gets the FPGA temperature inside a VPixx device.
    
    This function cannot be used with a DATAPixx.
                
    Returns:
        float: Temperature in degrees Celsius.
    
    :Low-level C definition:
        ``double DPxGetTemp3Celcius()``
    
    """
    return getTemp3Celcius()


 
getTempFarenheit = DPxDll['DPxGetTempFarenheit']
getTempFarenheit.restype = ctypes.c_double
def DPxGetTempFarenheit():
    """Gets the temperature inside a VPixx device in Fahrenheit.
                
    Returns:
        float: Temperature in degrees Fahrenheit.
    
    :Low-level C definition:
        ``double DPxGetTempFarenheit()``
    
    """
    return getTempFarenheit() 



getTime = DPxDll['DPxGetTime']
getTime.restype = ctypes.c_double
def DPxGetTime():
    """Gets the device time since last power up.
                
    Returns:
        float: Time in seconds.
    
    :Low-level C definition:
        ``double DPxGetTime()``
    
    """
    return getTime() 



setMarker = DPxDll['DPxSetMarker']
setMarker.restype = None
def DPxSetMarker():
    """Latches the current time value into the marker register.
    
    :Low-level C definition:
        ``void DPxGetMarker()``
        
    See Also:
        :class:`DPxSetMarker`, :class:`DPxGetNanoMarker`
    
    """
    return setMarker() 



getMarker = DPxDll['DPxGetMarker']
getMarker.restype = ctypes.c_double
def DPxGetMarker():
    """Gets the current marker from the register.
    
    This function allows the user to get the marker value previously latched.
                
    Returns:
        float: Time in seconds.
    
    :Low-level C definition:
        ``double DPxGetMarker()``

    See Also:
        :class:`DPxSetMarker`, :class:`DPxGetNanoMarker`        
    
    """
    return getMarker() 



GetNanoTime = DPxDll['DPxGetNanoTime']
def DPxGetNanoTime():
    """Gets the current time since power up with high precision.
    
    This function allows the user to get the marker value previously latched.
                
    Returns:
        tuple: Time in seconds.
    
    :Low-level C definition:
        ``void DPxGetNanoTime(unsigned *nanoHigh32, unsigned *nanoLow32)``

    See Also:
        :class:`DPxSetMarker`, :class:`DPxGetNanoMarker`        
    
    """
    nanoLow32 = 0
    nanoHigh32 = 0
    p_nanoLow32 = ctypes.c_uint(nanoLow32)
    p_nanoHigh32 = ctypes.c_uint(nanoHigh32)
    GetNanoTime(ctypes.byref(p_nanoLow32), ctypes.byref(p_nanoHigh32))
    return (p_nanoLow32.value, p_nanoHigh32.value)



GetNanoMarker = DPxDll['DPxGetNanoMarker']
def DPxGetNanoMarker():
    """Gets the current marker from the register with high precision.
    
    This function allows the user to get the marker value previously latched.
                
    Returns:
        tuple: Time in seconds.
    
    :Low-level C definition:
        ``void DPxGetNanoMarker(unsigned *nanoHigh32, unsigned *nanoLow32)``

    See Also:
        :class:`DPxSetMarker`, :class:`DPxGetNanoMarker`        
    
    """
    LowMrk32 = 0
    HighMrk32 = 0
    p_LowMrk32 = ctypes.c_uint(LowMrk32)
    p_HighMrk32 = ctypes.c_uint(HighMrk32)
    GetNanoMarker(ctypes.byref(p_LowMrk32), ctypes.byref(p_HighMrk32))
    return (p_LowMrk32.value, p_HighMrk32.value)

    

enableCalibReload = DPxDll['DPxEnableCalibReload']
enableCalibReload.restype = None
def DPxEnableCalibReload():
    enableCalibReload()
    
    
getDacNumChans = DPxDll['DPxGetDacNumChans']
getDacNumChans.restype = ctypes.c_int
def DPxGetDacNumChans():
    """Gets the number of channels available.
    
    This method returns the number of DAC channels in the system (4 in current implementation)
    
    Returns:
        int:   Number of channels.
        
    :Low-level C definition:
        ``int DPxGetDacNumChans()``
    
    """
    return getDacNumChans()




getDacRange = DPxDll['DPxGetDacRange']
def DPxGetDacRange(channel):
    """Gets the voltage range.
    
    This method returns the voltage range; For a VIEWPixx: +-10V, for aDATAPixx: +-10V for ch0/1, +-5V for ch2/3
    
    Args:
        channel (int): Channel number
    
    Returns:
        int:   Number of channel.
        
    :Low-level C definition:
        ``DPxGetDacRange(int channel, double *minV, double *maxV)``
    
    """
    minV = 0
    maxV = 0
    p_minV = ctypes.c_double(minV)
    p_maxV = ctypes.c_double(maxV)
    getDacRange(channel, ctypes.byref(p_minV), ctypes.byref(p_maxV))
    return (p_minV.value, p_maxV.value)
  

  

setDacValue = DPxDll['DPxSetDacValue']
setDacValue.argtypes = [ctypes.c_int, ctypes.c_int]
setDacValue.restype = None
def DPxSetDacValue(value, channel):
    """Sets the current value of a channel.
    
    This method allows the user to set the 16-bit 2's complement signed value for one DAC channel.
    In other words, this means that you have access to values between -32768 and +32768. For a positive
    number, you will simply need to leave it as is. For a negative number, since we are using signed, you will
    need to convert it to the 2's complement representation. 
    
    Args:
        value (int): Value of the channel. It is a 16-bit 2's complement signed number.
        channel (int): Channel number.
        
    :Low-level C definition:
        ``void DPxSetDacValue(int value, int channel)``
        
    See Also:
        :class:`DPxGetDacValue`
    
    """
    return setDacValue(value, channel)



getDacValue = DPxDll['DPxGetDacValue']
getDacValue.restype = ctypes.c_int 
getDacValue.argtypes = [ctypes.c_int]
def DPxGetDacValue(channel):
    """Gets the value for one DAC channel.
    
    Args:
        channel (int): Channel number.
    
    Returns:
        int: A 16-bit 2's complement signed value. 
        
    :Low-level C definition:
        ``int DPxGetDacValue(int channel)``
        
    See Also:
        :class:`DPxSetDacValue`
    
    """
    return getDacValue(channel) 



setDacVoltage = DPxDll['DPxSetDacVoltage']
setDacVoltage.argtypes = [ctypes.c_double, ctypes.c_int]
setDacVoltage.restype = None
def DPxSetDacVoltage(voltage, channel):
    """Sets the voltage for one DAC channel.
    
    For channels 0 and 1: |plusmn| 10V for ch0/1. For channels 2 and 3: |plusmn| 5V. 
    
    Args:4
        voltage (float): Voltage of the channel.
        channel (int): Channel number.
        
    :Low-level C definition:
        ``void DPxSetDacVoltage(double voltage, int channel)``
        
    See Also:
        :class:`DPxGetDacVoltage`

    """
    return setDacVoltage(voltage, channel)




getDacVoltage = DPxDll['DPxGetDacVoltage']
getDacVoltage.restype = ctypes.c_double
getDacVoltage.argtypes = [ctypes.c_int]
def DPxGetDacVoltage(channel):
    """Gets the value for one DAC channel.
    
    Args:
        channel (int): Channel number.
        
    For channel 0 and 1: |plusmn| 10V.
    For channel 2 and 3: |plusmn| 5V. 
    
    
    Returns:
        float: Voltage.
        
    :Low-level C definition:
        ``double DPxGetDacVoltage(int channel)``
        
    See Also:
        :class:`DPxSetDacValue`
        
    .. |plusmn| unicode:: U+000B1 .. PLUS-MINUS SIGN
    """
    return getDacVoltage(channel) 



enableDacCalibRaw = DPxDll['DPxEnableDacCalibRaw']
enableDacCalibRaw.restype = None
def DPxEnableDacCalibRaw():
    """Sets the hardware calibration mode.
    
    Enables DAC "raw" mode, causing DAC data to bypass hardware calibration.

    :Low-level C definition:
        ``void DPxEnableDacCalibRaw()``
                
    See Also:
        :class:`DPxDisableDacCalibRaw`
    """
    enableDacCalibRaw()
        


disableDacCalibRaw = DPxDll['DPxDisableDacCalibRaw']
disableDacCalibRaw.restype = None
def DPxDisableDacCalibRaw():
    """Sets the hardware calibration mode.
    
    Disables DAC "raw" mode, causing normal DAC hardware calibration.

    :Low-level C definition:
        ``void DPxDisableDacCalibRaw()``
                
    See Also:
        :class:`DPxEnableDacCalibRaw`
    """
    disableDacCalibRaw()



isDacCalibRaw = DPxDll['DPxIsDacCalibRaw']
isDacCalibRaw.restype = ctypes.c_int
def DPxIsDacCalibRaw():
    """Verifies if the hardware calibration mode is enabled.
    
    Returns:
        int: Non-zero if DAC data is bypassing hardware calibration.

    :Low-level C definition:
        ``int DPxIsDacCalibRaw()``
                
    See Also:
        :class:`DPxEnableDacCalibRaw`, :class:`DPxDisableDacCalibRaw`
    """
    return isDacCalibRaw()



enableDacBuffChan = DPxDll['DPxEnableDacBuffChan']
enableDacBuffChan.restype = None
def DPxEnableDacBuffChan(channel):
    """Enables RAM buffering of a DAC channel. 
    
    Args:
        channel (int): Channel number.
        
    :Low-level C definition:
        ``void DPxEnableDacBuffChan(int channel)``
        
    See Also:
        :class:`DPxDisableDacBuffChan`, :class:`DPxDisableDacBuffAllChans`
    
    """
    enableDacBuffChan(ctypes.c_int(channel))



disableDacBuffChan = DPxDll['DPxDisableDacBuffChan']
disableDacBuffChan.restype = None
def DPxDisableDacBuffChan(channel):
    """Disables RAM buffering of a DAC channel. 
    
    Args:
        channel (int): Channel number.
        
    :Low-level C definition:
        ``void DPxDisableDacBuffChan(int channel)``
        
    See Also:
        :class:`DPxEnableDacBuffChan`, :class:`DPxDisableDacBuffAllChans`
    
    """
    disableDacBuffChan(ctypes.c_int(channel))

    
    
disableDacBuffAllChans = DPxDll['DPxDisableDacBuffAllChans']
disableDacBuffAllChans.restype = None
def DPxDisableDacBuffAllChans():
    """Disables RAM buffering of all DAC channels. 
        
    :Low-level C definition:
        ``void DPxDisableDacBuffAllChans()``
        
    See Also:
        :class:`DPxEnableDacBuffChan`, :class:`DisableDacBuffChan`
    
    """
    disableDacBuffAllChans()
    


isDacBuffChan = DPxDll['DPxIsDacBuffChan']
isDacBuffChan.restype = ctypes.c_int
def DPxIsDacBuffChan(channel):
    """Verifies if RAM buffering is enabled for a DAC channel.
    
    Args:
        channel (int): Channel number.
    
    Returns:
        int: Non-zero if RAM buffering is enabled for a DAC channel.

    :Low-level C definition:
        ``int DPxIsDacBuffChan(int channel)``
                
    See Also:
        :class:`DPxEnableDacCalibRaw`, :class:`DPxDisableDacCalibRaw`
    """
    return isDacBuffChan(ctypes.c_int(channel))

    
    
setDacBuffBaseAddr = DPxDll['DPxSetDacBuffBaseAddr']
setDacBuffBaseAddr.argtypes = [ctypes.c_uint]
setDacBuffBaseAddr.restype = None
def DPxSetDacBuffBaseAddr(buffBaseAddr):
    """Sets the DAC RAM buffer start address.
    
    Must be an even value.
    
    Args:
        buffBaseAddr (int): Base address.
        
    :Low-level C definition:
        ``void DPxSetDacBuffBaseAddr(unsigned buffBaseAddr)``
        
    See Also:
        :class:`DPxGetDacBuffBaseAddr`
    
    """
    return setDacBuffBaseAddr(buffBaseAddr)



getDacBuffBaseAddr = DPxDll['DPxGetDacBuffBaseAddr']                           
getDacBuffBaseAddr.restype = ctypes.c_uint
def DPxGetDacBuffBaseAddr():
    """Gets the DAC RAM buffer start address.
    
    Returns:
        int: Base address.
        
    :Low-level C definition:
        ``unsigned DPxGetDacBuffBaseAddr()``
        
    See Also:
        :class:`DPxSetDacBuffBaseAddr`
    
    """
    return getDacBuffBaseAddr()


 
setDacBuffReadAddr = DPxDll['DPxSetDacBuffReadAddr']
setDacBuffReadAddr.argtypes = [ctypes.c_uint]
setDacBuffReadAddr.restype = None
def DPxSetDacBuffReadAddr(buffReadAddr):
    """Sets RAM address from which next DAC datum will be read.
    
    Must be an even value.
    
    Args:
        buffReadAddr (int): Read address.
        
    :Low-level C definition:
        ``void DPxSetDacBuffReadAddr(unsigned buffReadAddr)``
        
    See Also:
        :class:`DPxGetDacBuffReadAddr`
    
    """
    return setDacBuffReadAddr(buffReadAddr)
 


getDacBuffReadAddr = DPxDll['DPxGetDacBuffReadAddr']                            
getDacBuffReadAddr.restype = ctypes.c_uint
def DPxGetDacBuffReadAddr():
    """Gets RAM address from which next DAC datum will be read.
    
    Returns:
        int: Read address.
        
    :Low-level C definition:
        ``unsigned DPxGetDacBuffReadAddr()``
        
    See Also:
        :class:`DPxSetDacBuffReadAddr`
    
    """
    return getDacBuffReadAddr()



setDacBuffSize = DPxDll['DPxSetDacBuffSize']
setDacBuffSize.argtypes = [ctypes.c_uint]
setDacBuffSize.restype = None 
def DPxSetDacBuffSize(buffSize):
    """Sets DAC RAM buffer size in bytes.
    
     Must be an even value.  Buffer wraps to Base after Size.
    
    Args:
        buffSize (int): Buffer size.
        
    :Low-level C definition:
        ``void DPxSetDacBuffSize(unsigned buffSize)``
        
    See Also:
        :class:`DPxGetDacBuffReadAddr`
    
    """
    return setDacBuffSize(buffSize)




getDacBuffSize = DPxDll['DPxGetDacBuffSize']                                         
getDacBuffSize.restype = ctypes.c_uint
def DPxGetDacBuffSize():
    """Gets the DAC RAM buffer size in bytes.
    
    Returns:
        int: buffer size.
        
    :Low-level C definition:
        ``unsigned DPxGetDacBuffSize()``
        
    See Also:
        :class:`DPxSetDacBuffSize`
    
    """
    return getDacBuffSize()




setDacBuff = DPxDll['DPxSetDacBuff']
setDacBuff.argtypes = [ctypes.c_uint, ctypes.c_uint]
setDacBuff.restype = None 
def DPxSetDacBuff(buffAddr, buffSize):
    """Sets base address, read address and buffer size for DAC schedules.
    
    This function is a shortcut which assigns Size/BaseAddr/ReadAddr
    
    Args:
        buffAddr (int): Base address.
        buffSize (int): Buffer size.
        
    :Low-level C definition:
        ``void DPxSetDacBuff(unsigned buffAddr, unsigned buffSize)``
        
    See Also:
        :class:`DPxGetDacSchedOnset`, :class:`DPxSetDacBuffSize`, :class:`DPxSetDacBuffReadAddr`
    
    """
    return setDacBuff(buffAddr, buffSize)



setDacSchedOnset = DPxDll['DPxSetDacSchedOnset']
setDacSchedOnset.argtypes = [ctypes.c_uint]
setDacSchedOnset.restype = None
def DPxSetDacSchedOnset(onset):
    """Sets the nanosecond delay between schedule start and first DAC update.
    
    Args:
        onset (int): delay in nanoseconds.
        
    :Low-level C definition:
        ``void DPxSetDacSchedOnset(unsigned onset)``
        
    See Also:
        :class:`DPxGetDacSchedOnset`
    
    """
    return setDacSchedOnset(onset)


  

getDacSchedOnset = DPxDll['DPxGetDacSchedOnset']                             
getDacSchedOnset.restype = ctypes.c_uint
def DPxGetDacSchedOnset():
    """Gets the nanosecond delay between the schedule start and first DAC update.
    
    Returns:
        int: onset.
        
    :Low-level C definition:
        ``unsigned DPxGetDacSchedOnset()``
        
    See Also:
        :class:`DPxSetDacSchedOnset`
    
    """
    return getDacSchedOnset()



setDacSchedRate = DPxDll['DPxSetDacSchedRate']
setDacSchedRate.argtypes = [ctypes.c_uint, ctypes.c_int]
setDacSchedRate.restype = None  
def DPxSetDacSchedRate(rate, unit):
    """Sets the schedule rate.
    
    This method allows the user to set the schedule rate. Since the rate can be given 
    with different units, the method also needs to have a unit associated with the rate.
    
    
    If no delay is required, this method does not need to be used. Default value is 0.
    
    Args:
        rate (int): Any positive value equal to or greater than zero.
        unit (str): Any of the predefined constants.\n
                - **hz**: rate updates per second, maximum 1 MHz.
                - **video**: rate updates per video frame, maximum 1 MHz.
                - **nano**: rate updates period in nanoseconds, minimum 1000 ns.
    
    :Low-level C definition:
        ``void DPxSetDacSchedRate(unsigned rateValue, int rateUnits)``
    
    """
    setDacSchedRate(rate, api_constants[unit.upper()])
        

   

getDacSchedRate = DPxDll['DPxGetDacSchedRate']
def DPxGetDacSchedRate():
    """Gets DAC schedule update rate and the rate units.
    
    Returns:
        tuple: rate and unit.
        
    :Low-level C definition:
        ``unsigned DPxGetDacSchedRate(int *rateUnits)``
        
    See Also:
        :class:`DPxSetDacSchedRate`
    
    """
    Var = 0
    p_Var = ctypes.c_int(Var)
    getDacSchedRate.restype = ctypes.c_uint
    return (getDacSchedRate(ctypes.byref(p_Var)), rate_constants[p_Var.value])



setDacSchedCount = DPxDll['DPxSetDacSchedCount']
setDacSchedCount.argtypes = [ctypes.c_uint]
setDacSchedCount.restype = None
def DPxSetDacSchedCount(count):
    """Sets DAC schedule update count.
    
    Args:
        count (int): Schedule count.
        
    :Low-level C definition:
        ``void DPxSetDacSchedCount(unsigned count)``
        
    See Also:
        :class:`DPxGetDacSchedCount`
    
    """
    return setDacSchedCount(count)


    
getDacSchedCount = DPxDll['DPxGetDacSchedCount']                              
getDacSchedCount.restype = ctypes.c_uint
def DPxGetDacSchedCount():
    """Gets DAC schedule update count.
    
    Returns:
        int: Schedule sample count.
        
    :Low-level C definition:
        ``unsigned DPxGetDacSchedCount()``
        
    See Also:
        :class:`DPxSetDacSchedCount`
    
    """
    return getDacSchedCount()


   
enableDacSchedCountdown = DPxDll['DPxEnableDacSchedCountdown']
enableDacSchedCountdown.restype = None 
def DPxEnableDacSchedCountdown():
    """Enables DAC schedule count down.
    
    SchedCount decrements at SchedRate, and schedule stops automatically when count hits 0.

    :Low-level C definition:
        ``void DPxEnableDacSchedCountdown()``
                
    See Also:
        :class:`DPxDisableDacSchedCountdown`, :class:`DPxIsDacSchedCountdown`
    """
    enableDacSchedCountdown()


   
disableDacSchedCountdown = DPxDll['DPxDisableDacSchedCountdown']
disableDacSchedCountdown.restype = None
def DPxDisableDacSchedCountdown():
    """Disables DAC schedule count down.
    
    SchedCount increments at SchedRate, and schedule is stopped by calling SchedStop.

    :Low-level C definition:
        ``void DPxDisableDacSchedCountdown()``
                
    See Also:
        :class:`DPxEnableDacSchedCountdown`, :class:`DPxIsDacSchedCountdown`
    """
    disableDacSchedCountdown()
  

 
isDacSchedCountdown = DPxDll['DPxIsDacSchedCountdown']
isDacSchedCountdown.restype = ctypes.c_int
def DPxIsDacSchedCountdown():
    """Verifies if RAM buffering is enabled for a DAC channel.
    
    Returns:
        int: Non-zero if SchedCount decrements to 0 and automatically stops schedule.

    :Low-level C definition:
        ``int DPxIsDacSchedCountdown()``
                
    See Also:
        :class:`DPxEnableDacSchedCountdown`, :class:`DPxDisableDacSchedCountdown`
    """
    return isDacSchedCountdown()



setDacSched = DPxDll['DPxSetDacSched']
setDacSched.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint]
setDacSched.restype = None
def DPxSetDacSched(onset, rateValue, rateUnits, count):
    """Sets DAC schedule onset, count and rate.
    
    This function is a shortcut which assigns Onset/Rate/Count. If ``count`` is greater than zero, the count
    down mode is enabled.
    
    Args:
        onset (int): Schedule onset.
        rateValue (int): Rate value.
        rateUnits (str): Usually ``hz``. Can also be ``video`` to update every ``rateValue`` video frames or ``nano`` to update every ``rateValue`` nanoseconds.
        count (int): Schedule count.
        
    :Low-level C definition:
        ``void DPxSetDacSched(unsigned onset, unsigned rateValue, int rateUnits, unsigned count)``
    
    """
    return setDacSched(onset, rateValue, api_constants[rateUnits.upper()], count)


      
startDacSched = DPxDll['DPxStartDacSched']
startDacSched.restype = None
def DPxStartDacSched():
    """Starts running a DAC schedule.

    :Low-level C definition:
        ``void DPxStartDacSched()``
                
    See Also:
        :class:`DPxStopDacSched`, :class:`DPxIsDacSchedRunning`
    """
    startDacSched()

      

stopDacSched = DPxDll['DPxStopDacSched']
stopDacSched.restype = None
def DPxStopDacSched():
    """Stops running a DAC schedule.

    :Low-level C definition:
        ``void DPxStopDacSched()``
                
    See Also:
        :class:`DPxStartDacSched`, :class:`DPxIsDacSchedRunning`
    """
    stopDacSched()



isDacSchedRunning = DPxDll['DPxIsDacSchedRunning']
isDacSchedRunning.restype = ctypes.c_int
def DPxIsDacSchedRunning():
    """Verifies if a DAC schedule is currently running.
    
    Returns:
        int: Non-zero if a DAC schedule is currently running, zero otherwise.
        
    :Low-level C definition:
        ``int DPxIsDacSchedRunning()``
        
    See Also:
        :class:`DPxStartDacSched`, :class:`DPxStopDacSched`
    
    """
    return isDacSchedRunning()

  
                                    
getAdcNumChans = DPxDll['DPxGetAdcNumChans']
getAdcNumChans.restype = ctypes.c_int
def DPxGetAdcNumChans():
    """Gets the number of channel available.
    
    This method returns the number of ADC channels in the system (18 in current implementation)
    
    Returns:
        int:   Number of channels.
        
    :Low-level C definition:
        ``int DPxGetAdcNumChans()``
    
    """
    return getAdcNumChans()


                                
getAdcValue = DPxDll['DPxGetAdcValue']
getAdcValue.restype = ctypes.c_int
getAdcValue.argtypes = [ctypes.c_int]
def DPxGetAdcValue(channel):
    """Gets the value for one ADC channel.
    
    This method returns the 16-bit 2's complement signed value for one ADC channel. Can be used on channels 0-17.
    
    Args:
        channel (int): Channel number.    
    
    Returns:
        int: Channel value.
        
    :Low-level C definition:
        ``int DPxGetAdcValue(int channel)``
    
    """
    return getAdcValue(channel)


    
getAdcRange = DPxDll['DPxGetAdcRange']  
def DPxGetAdcRange(channel):
    """Gets the voltage range.
    
    This method returns the voltage range; +-10V for all channels
    
    Args:
        channel (int): Channel number.
    
    Returns:
        int: Range of channel.
        
    :Low-level C definition:
        ``void DPxGetAdcRange(int channel, double *minV, double *maxV)``
    
    """
    minV = 0
    maxV = 0
    p_minV = ctypes.c_double(minV)
    p_maxV = ctypes.c_double(maxV)
    getAdcRange(channel, ctypes.byref(p_minV), ctypes.byref(p_maxV))
    return (p_minV.value, p_maxV.value)


                                
getAdcVoltage = DPxDll['DPxGetAdcVoltage'] 
getAdcVoltage.restype = ctypes.c_double
getAdcVoltage.argtypes = [ctypes.c_int]
def DPxGetAdcVoltage(channel):
    """Gets the voltage for an ADC channel.
    
    Args:
        channel (int): Channel number.
    
    Returns:
        float: Voltage of channel.
        
    :Low-level C definition:
        ``double DPxGetAdcVoltage(int channel)``
    
    """
    return getAdcVoltage(channel)



setAdcBuffChanRef = DPxDll['DPxSetAdcBuffChanRef']
setAdcBuffChanRef.argtypes = [ctypes.c_int, ctypes.c_int]
setAdcBuffChanRef.restype = None
def DPxSetAdcBuffChanRef(channel, reference):
    """Sets a reference to a channel.
        
    This method allows the user to enable or disable ram buffering on a given channel.
    When enabled, a given channel is buffered in ram. Enabling RAM buffering can only
    be done for channels 0 to 15.

    Args:
        channel (int): Channel number to associate with a reference. 
        reference (str): Valid argument is one of the following predefined constants:\n
            - **gnd**: Referenced to ground.
            - **diff**: Referenced to adjacent analog input. 
            - **ref0**: Referenced to REF0 analog input.
            - **ref1**: Referenced to REF1 analog input.
    
    :Low-level C definition:
        ``void DPxSetAdcBuffChanRef(int channel, int chanRef)``

    """
    setAdcBuffChanRef(channel, api_constants[reference.upper()])
    



getAdcBuffChanRef = DPxDll['DPxGetAdcBuffChanRef']
getAdcBuffChanRef.restype = ctypes.c_int 
getAdcBuffChanRef.argtypes = [ctypes.c_int]
def DPxGetAdcBuffChanRef(channel):
    """Gets the reference associated with a channel.

    Returns:
        reference (string): one of the following predefined constants:\n
            - **gnd**: Referenced to ground.
            - **diff**: Referenced to adjacent analog input. 
            - **ref0**: Referenced to REF0 analog input.
            - **ref1**: Referenced to REF1 analog input.

    :Low-level C definition:
        ``int DPxGetAdcBuffChanRef(int channel)``

    """ 
    key = getAdcBuffChanRef(channel)
    return adc_channel_reference[ key ]


                           
enableAdcBuffChan = DPxDll['DPxEnableAdcBuffChan']   
enableAdcBuffChan.argtypes = [ctypes.c_int]
enableAdcBuffChan.restype = None
def DPxEnableAdcBuffChan(channel):
    """Enables RAM buffering of an ADC channel. 
    
    This function is only available for channels 0-15.
    
    Args:
        channel (int): Channel number.
        
    :Low-level C definition:
        ``void DPxEnableAdcBuffChan(int channel)``
        
    See Also:
        :class:`DPxDisableAdcBuffChan`, :class:`DPxDisableAdcBuffAllChans`, :class:`DPxIsAdcBuffChan`
    
    """
    enableAdcBuffChan(ctypes.c_int(channel))


                            
disableAdcBuffChan = DPxDll['DPxDisableAdcBuffChan']
disableAdcBuffChan.argtypes = [ctypes.c_int]
disableAdcBuffChan.restype = None
def DPxDisableAdcBuffChan(channel):
    """Disables RAM buffering of an ADC channel. 
    
    This function is only available for channels 0-15.
    
    Args:
        channel (int): Channel number.
        
    :Low-level C definition:
        ``void DPxDisableAdcBuffChan(int channel)``
        
    See Also:
        :class:`DPxEnableAdcBuffChan`, :class:`DPxDisableAdcBuffAllChans`, :class:`DPxIsAdcBuffChan`
    
    """
    disableAdcBuffChan(ctypes.c_int(channel))



disableAdcBuffAllChans = DPxDll['DPxDisableAdcBuffAllChans']
disableAdcBuffAllChans.restype = None
def DPxDisableAdcBuffAllChans():
    """Disables RAM buffering of all ADC channels. 
        
    :Low-level C definition:
        ``void DPxDisableAdcBuffAllChans()``
        
    See Also:
        :class:`DPxEnableAdcBuffChan`, :class:`DPxDisableAdcBuffChan`, :class:`DPxIsAdcBuffChan`
    
    """
    disableAdcBuffAllChans()



isAdcBuffChan = DPxDll['DPxIsAdcBuffChan']
isAdcBuffChan.restype = ctypes.c_int
isAdcBuffChan.argtypes = [ctypes.c_int]
def DPxIsAdcBuffChan(channel):
    """Verifies if RAM buffering is enabled for an ADC channel.
    
    This function is only available for channels 0-15.
    
    Args:
        channel (int): Channel number.
    
    Returns:
        int: Non-zero if RAM buffering is enabled for an ADC channel.

    :Low-level C definition:
        ``int DPxIsAdcBuffChan(int channel)``
                
    See Also:
        :class:`DPxEnableAdcBuffChan`, :class:`DPxDisableAdcBuffChan`
    """
    return isAdcBuffChan(ctypes.c_int(channel))


                                   
enableAdcCalibRaw = DPxDll['DPxEnableAdcCalibRaw']
enableAdcCalibRaw.restype = None
def DPxEnableAdcCalibRaw():
    """Sets the hardware calibration mode.
    
    Enables ADC "raw" mode, causing ADC data to bypass hardware calibration.

    :Low-level C definition:
        ``void DPxEnableAdcCalibRaw()``
                
    See Also:
        :class:`DPxDisableAdcCalibRaw`, :class:`DPxIsAdcCalibRaw`
    """
    enableAdcCalibRaw()



disableAdcCalibRaw = DPxDll['DPxDisableAdcCalibRaw']
disableAdcCalibRaw.restype = None
def DPxDisableAdcCalibRaw():
    """Sets the hardware calibration mode.
    
    Disables ADC "raw" mode, causing normal ADC hardware calibration.

    :Low-level C definition:
        ``void DPxDisableAdcCalibRaw()``
                
    See Also:
        :class:`DPxDisableAdcCalibRaw`, :class:`DPxIsAdcCalibRaw`
    """
    disableAdcCalibRaw()



isAdcCalibRaw = DPxDll['DPxIsAdcCalibRaw']
isAdcCalibRaw.restype = ctypes.c_int
def DPxIsAdcCalibRaw():
    """Verifies if the hardware calibration mode is enabled.
    
    Returns:
        int: Non-zero if ADC data is bypassing hardware calibration.

    :Low-level C definition:
        ``int DPxIsAdcCalibRaw()``
                
    See Also:
        :class:`DPxEnableAdcCalibRaw`, :class:`DPxDisableAdcCalibRaw`
    """
    return isAdcCalibRaw()


                       

enableDacAdcLoopback = DPxDll['DPxEnableDacAdcLoopback']
enableDacAdcLoopback.restype = None
def DPxEnableDacAdcLoopback():
    """Sets the loopback between ADC and DAC mode.
    
    ADC data readings are looped back internally from programmed DAC voltages: \n
        - DAC_DATA0 => ADC_DATA0/2/4/6/8/10/12/14
        - DAC_DATA1 => ADC_DATA1/3/5/7/9/11/13/15
        - DAC_DATA2 => ADC_REF0
        - DAC_DATA3 => ADC_REF1

    :Low-level C definition:
        ``void DPxEnableDacAdcLoopback()``
                
    See Also:
        :class:`DPxDisableDacAdcLoopback`, :class:`DPxIsDacAdcLoopback`
    """
    enableDacAdcLoopback()


                                
disableDacAdcLoopback = DPxDll['DPxDisableDacAdcLoopback']
disableDacAdcLoopback.restype = None
def DPxDisableDacAdcLoopback():
    """Disables the loopback between ADC and DAC.
    
    Disables ADC loopback, causes ADC readings to reflect real analog inputs.

    :Low-level C definition:
        ``void DPxDisableDacAdcLoopback()``
                
    See Also:
        :class:`DPxEnableDacAdcLoopback`, :class:`DPxIsDacAdcLoopback`
    """
    disableDacAdcLoopback()


                                    
isDacAdcLoopback = DPxDll['DPxIsDacAdcLoopback']
isDacAdcLoopback.restype = ctypes.c_int
def DPxIsDacAdcLoopback():
    """Verifies if the loopback between ADC and DAC is enabled.

    Returns:
        int: Non-zero if ADC inputs are looped back from DAC outputs.

    :Low-level C definition:
        ``void DPxIsDacAdcLoopback()``
                
    See Also:
        :class:`DPxEnableDacAdcLoopback`, :class:`DPxIsDacAdcLoopback`
    """
    isDacAdcLoopback()  


                                   
enableAdcFreeRun = DPxDll['DPxEnableAdcFreeRun']
enableAdcFreeRun.restype = None
def DPxEnableAdcFreeRun():
    """Sets the ADC free run mode.
    
    ADCs convert continuously. Can add up to 4 microseconds random latency to scheduled samples.

    :Low-level C definition:
        ``void DPxEnableAdcFreeRun()``
                
    See Also:
        :class:`DPxDisableAdcFreeRun`, :class:`DPxIsAdcFreeRun`
    """
    enableAdcFreeRun()
    


disableAdcFreeRun = DPxDll['DPxDisableAdcFreeRun']
disableAdcFreeRun.restype = None
def DPxDisableAdcFreeRun():
    """Sets the ADC free run mode.
    
    ADCs only convert on schedule ticks, for microsecond-precise sampling.

    :Low-level C definition:
        ``void DPxDisableAdcFreeRun()``
                
    See Also:
        :class:`DPxEnableAdcFreeRun`, :class:`DPxIsAdcFreeRun`
    """
    disableAdcFreeRun()



isAdcFreeRun = DPxDll['DPxIsAdcFreeRun']
isAdcFreeRun.restype = ctypes.c_int
def DPxIsAdcFreeRun():
    """Verifies if the loopback between ADC and DAC is enabled.

    Returns:
        int: Non-zero if ADCs are performing continuous conversions.

    :Low-level C definition:
        ``void DPxIsAdcFreeRun()``
                
    See Also:
        :class:`DPxEnableDacAdcLoopback`, :class:`DPxDisableAdcFreeRun`
    """
    isAdcFreeRun() 
    


setAdcBuffBaseAddr = DPxDll['DPxSetAdcBuffBaseAddr']  
setAdcBuffBaseAddr.argtypes = [ctypes.c_uint]
setAdcBuffBaseAddr.restype = None
def DPxSetAdcBuffBaseAddr(buffBaseAddr):
    """Sets the ADC RAM buffer start address.
    
    Must be an even value.
    
    Args:
        buffBaseAddr (int): Base address.
        
    :Low-level C definition:
        ``void DPxSetAdcBuffBaseAddr(unsigned buffBaseAddr)``
        
    See Also:
        :class:`DPxGetAdcBuffBaseAddr`
    
    """
    return setAdcBuffBaseAddr(buffBaseAddr)



getAdcBuffBaseAddr = DPxDll['DPxGetAdcBuffBaseAddr']                             
getAdcBuffBaseAddr.restype = ctypes.c_uint
def DPxGetAdcBuffBaseAddr():
    """Gets the ADC RAM buffer start address.
    
    Returns:
        int: Base address.
        
    :Low-level C definition:
        ``unsigned DPxGetDacBuffBaseAddr()``
        
    See Also:
        :class:`DPxSetAdcBuffBaseAddr`
    
    """
    return getAdcBuffBaseAddr()


                
setAdcBuffWriteAddr= DPxDll['DPxSetAdcBuffWriteAddr']    
setAdcBuffWriteAddr.argtypes = [ctypes.c_uint]
setAdcBuffWriteAddr.restype = None
def DPxSetAdcBuffWriteAddr(buffWriteAddr):
    """Sets RAM address from which next ADC datum will be written.
    
    Must be an even value.
    
    Args:
        buffWriteAddr (int): Write address.
        
    :Low-level C definition:
        ``void DPxSetAdcBuffWriteAddr(unsigned buffWriteAddr)``
        
    See Also:
        :class:`DPxGetAdcBuffWriteAddr`
    
    """
    return setAdcBuffWriteAddr(buffWriteAddr)


                              
getAdcBuffWriteAddr = DPxDll['DPxGetAdcBuffWriteAddr']                              
getAdcBuffWriteAddr.restype = ctypes.c_uint
def DPxGetAdcBuffWriteAddr():
    """Gets RAM address from which next ADC datum will be written.
    
    Returns:
        int: Write address.
        
    :Low-level C definition:
        ``unsigned DPxGetAdcBuffWriteAddr()``
        
    See Also:
        :class:`DPxSetAdcBuffWriteAddr`
    
    """
    return getAdcBuffWriteAddr()



setAdcBuffSize = DPxDll['DPxSetAdcBuffSize']   
setAdcBuffSize.argtypes = [ctypes.c_uint]
setAdcBuffSize.restype = None
def DPxSetAdcBuffSize(buffSize):
    """Sets ADC RAM buffer size in bytes.
    
     Must be an even value.  Buffer wraps to Base after Size.
    
    Args:
        buffSize (int): Buffer size.
        
    :Low-level C definition:
        ``void DPxSetAdcBuffSize(unsigned buffSize)``
        
    See Also:
        :class:`DPxGetAdcBuffSize`
    
    """
    return setAdcBuffSize(buffSize)



getAdcBuffSize = DPxDll['DPxGetAdcBuffSize']                                          
getAdcBuffSize.restype = ctypes.c_uint
def DPxGetAdcBuffSize():
    """Gets the ADC RAM buffer size in bytes.
    
    Returns:
        int: buffer size.
        
    :Low-level C definition:
        ``unsigned DPxGetAdcBuffSize()``
        
    See Also:
        :class:`DPxSetAdcBuffSize`
    
    """
    return getAdcBuffSize()



setAdcBuff = DPxDll['DPxSetAdcBuff']  
setAdcBuff.argtypes = [ctypes.c_uint, ctypes.c_uint]
setAdcBuff.restype = None
def DPxSetAdcBuff(buffAddr, buffSize):
    """Sets base address, write address and buffer size for ADC schedules.
    
    This function is a shortcut which assigns Size/BaseAddr/WriteAddr
    
    Args:
        buffAddr (int): Base address.
        buffSize (int): Buffer size.
        
    :Low-level C definition:
        ``void DPxSetAdcBuff(unsigned buffAddr, unsigned buffSize)``
        
    See Also:
        :class:`DPxGetAdcSchedOnset`, :class:`DPxSetAdcBuffSize`, :class:`DPxSetAdcBuffWriteAddr`
    
    """
    return setAdcBuff(buffAddr, buffSize)



setAdcSchedOnset = DPxDll['DPxSetAdcSchedOnset']
setAdcSchedOnset.argtypes = [ctypes.c_uint]
setAdcSchedOnset.restype = None
def DPxSetAdcSchedOnset(onset):
    """Sets nanosecond delay between schedule start and first ADC sample.
    
    Args:
        onset (int): delay in nanoseconds.
        
    :Low-level C definition:
        ``void DPxSetAdcSchedOnset(unsigned onset)``
        
    See Also:
        :class:`DPxGetAdcSchedOnset`
    
    """
    return setAdcSchedOnset(onset)



getAdcSchedOnset = DPxDll['DPxGetAdcSchedOnset']                                
getAdcSchedOnset.restype = ctypes.c_uint
def DPxGetAdcSchedOnset():
    """Gets the nanosecond delay between schedule start and first ADC sample.
    
    Returns:
        int: onset.
        
    :Low-level C definition:
        ``unsigned DPxGetAdcSchedOnset()``
        
    See Also:
        :class:`DPxSetAdcSchedOnset`
    
    """
    return getAdcSchedOnset()


setAdcSchedRate = DPxDll['DPxSetAdcSchedRate']
setAdcSchedRate.argtypes = [ctypes.c_uint, ctypes.c_int]
setAdcSchedRate.restype = None
def DPxSetAdcSchedRate(rate, unit):
    """Sets the schedule rate.
        
    This method allows the user to set the schedule rate. Since the rate can be given 
    with different units, the method also needs to have a unit associated with the rate.
    
    If no delay is required, this method does not need to be used. Default value is 0.

    Args:
        rate (int): Any positive value equal to or greater than zero.
        unit (str): Any of the predefined constants. \n
                - **hz**: rate updates per second, maximum 200 kHz.
                - **video**: rate updates per video frame, maximum 200 kHz.
                - **nano**: rate updates period in nanoseconds, minimum 5000 ns.
        
    :Low-level C definition:
        ``void DPxSetAdcSchedRate(unsigned  rateValue, int  rateUnits)``
    """
    setAdcSchedRate(rate, api_constants[unit.upper()])

  

GetAdcSchedRate = DPxDll['DPxGetAdcSchedRate']
def DPxGetAdcSchedRate():
    """
    This function gets the ADC schedule rate and the rate unit.
    Return value: (schedule rate, rate unit)
    
    :Low-level C definition:
        ``unsigned DPxGetAdcSchedRate(int *rateUnits)``
    """
    Var = 0
    p_Var = ctypes.c_int(Var)
    GetAdcSchedRate.restype = ctypes.c_uint
    return (GetAdcSchedRate(ctypes.byref(p_Var)) , rate_constants[p_Var.value])



setAdcSchedCount = DPxDll['DPxSetAdcSchedCount']
setAdcSchedCount.argtypes = [ctypes.c_uint]
setAdcSchedCount.restype = None
def DPxSetAdcSchedCount(count):
    """Sets ADC schedule update count.
    
    Args:
        count (int): Schedule count.
        
    :Low-level C definition:
        ``void DPxSetAdcSchedCount(unsigned count)``
        
    See Also:
        :class:`DPxGetAdcSchedCount`
    
    """
    return setAdcSchedCount(count)




getAdcSchedCount = DPxDll['DPxGetAdcSchedCount']  
getAdcSchedCount.restype = ctypes.c_uint
def DPxGetAdcSchedCount():
    """Gets ADC schedule update count.
    
    Returns:
        int: Schedule sample count.
        
    :Low-level C definition:
        ``unsigned DPxGetAdcSchedCount()``
        
    See Also:
        :class:`DPxSetAdcSchedCount`
    
    """
    return getAdcSchedCount()



enableAdcSchedCountdown = DPxDll['DPxEnableAdcSchedCountdown']
enableAdcSchedCountdown.restype = None   
def DPxEnableAdcSchedCountdown():
    """Enables ADC schedule count down.
    
    SchedCount decrements at SchedRate, and schedule stops automatically when count hits 0.

    :Low-level C definition:
        ``void DPxEnableAdcSchedCountdown()``
                
    See Also:
        :class:`DPxDisableAdcSchedCountdown`, :class:`DPxIsAdcSchedCountdown`
    """
    enableAdcSchedCountdown()
    


disableAdcSchedCountdown = DPxDll['DPxDisableAdcSchedCountdown']
disableAdcSchedCountdown.restype = None   
def DPxDisableAdcSchedCountdown():
    """Disables ADC schedule count down.
    
    SchedCount increments at SchedRate, and schedule is stopped by calling SchedStop.

    :Low-level C definition:
        ``void DPxDisableAdcSchedCountdown()``
                
    See Also:
        :class:`DPxEnableAdcSchedCountdown`, :class:`DPxIsAdcSchedCountdown`
    """
    disableAdcSchedCountdown()



isAdcSchedCountdown = DPxDll['DPxIsAdcSchedCountdown']
isAdcSchedCountdown.restype = ctypes.c_int
def DPxIsAdcSchedCountdown():
    """Verifies if RAM buffering is enabled for an ADC channel.
    
    Returns:
        int: Non-zero if SchedCount decrements to 0 and automatically stops schedule.

    :Low-level C definition:
        ``int DPxIsAdcSchedCountdown()``
                
    See Also:
        :class:`DPxEnableAdcSchedCountdown`, :class:`DPxDisableAdcSchedCountdown`
    """
    return isAdcSchedCountdown()




setAdcSched = DPxDll['DPxSetAdcSched']
setAdcSched.restype = None
def DPxSetAdcSched(onset, rateValue, rateUnits, count):
    """Sets ADC schedule onset, count and rate.
    
    This function is a shortcut which assigns Onset/Rate/Count. If ``count`` is greater than zero, the count
    down mode is enabled.
    
    Args:
        onset (int): Schedule onset.
        rateValue (int): Rate value.
        rateUnits (str): Usually ``hz``. Can also be ``video`` to update every ``rateValue`` video frames or ``nano`` to update every ``rateValue`` nanoseconds.
        count (int): Schedule count.
        
    :Low-level C definition:
        ``void DPxSetAdcSched(unsigned onset, unsigned rateValue, int rateUnits, unsigned count)``
    
    """
    return setAdcSched(onset, rateValue, api_constants[rateUnits.upper()], count)



                                        

startAdcSched = DPxDll['DPxStartAdcSched']
startAdcSched.restype = None
def DPxStartAdcSched():
    """Starts running an ADC schedule.

    :Low-level C definition:
        ``void DPxStartAdcSched()``
                
    See Also:
        :class:`DPxStopAdcSched`, :class:`DPxIsAdcSchedRunning`
    """
    startAdcSched()   


                                        
stopAdcSched = DPxDll['DPxStopAdcSched']
stopAdcSched.restype = None 
def DPxStopAdcSched():
    """Stops running an ADC schedule.

    :Low-level C definition:
        ``void DPxStopAdcSched()``
                
    See Also:
        :class:`DPxStartAdcSched`, :class:`DPxIsAdcSchedRunning`
    """
    stopAdcSched()



isAdcSchedRunning = DPxDll['DPxIsAdcSchedRunning']
isAdcSchedRunning.restype = ctypes.c_int
def DPxIsAdcSchedRunning():
    """Verifies if an ADC schedule is currently running.
    
    Returns:
        int: Non-zero if an ADC schedule is currently running, zero if there is one.
        
    :Low-level C definition:
        ``int DPxIsAdcSchedRunning()``
        
    See Also:
        :class:`DPxStartAdcSched`, :class:`DPxStopAdcSched`
    
    """
    return isAdcSchedRunning()



enableAdcLogTimetags = DPxDll['DPxEnableAdcLogTimetags']
enableAdcLogTimetags.restype = None
def DPxEnableAdcLogTimetags():
    """Enables ADC timetag mode.
    
    Each buffered ADC sample is preceeded by a 64-bit nanosecond timetag.

    :Low-level C definition:
        ``void DPxEnableAdcLogTimetags()``
                
    See Also:
        :class:`DPxDisableAdcLogTimetags`, :class:`DPxIsAdcLogTimetags`
    """
    enableAdcLogTimetags()


                               

disableAdcLogTimetags = DPxDll['DPxDisableAdcLogTimetags']
disableAdcLogTimetags.restype = None   
def DPxDisableAdcLogTimetags():
    """Disables ADC timetag mode.
    
    Buffered data has no timetags.

    :Low-level C definition:
        ``void DPxDisableAdcLogTimetags()``
                
    See Also:
        :class:`DPxDisableAdcLogTimetags`, :class:`DPxIsAdcLogTimetags`
    """
    disableAdcLogTimetags()


 
isAdcLogTimetags = DPxDll['DPxIsAdcLogTimetags']
isAdcLogTimetags.restype = ctypes.c_int
def DPxIsAdcLogTimetags():
    """Verifies if the ADC timetag mode is enabled.
    
    Returns:
        int: Non-zero if buffered data is preceeded with nanosecond timetag.
        
    :Low-level C definition:
        ``int DPxIsAdcLogTimetags()``
        
    See Also:
        :class:`DPxDisableAdcLogTimetags`, :class:`DPxIsAdcLogTimetags`
    
    """
    return isAdcLogTimetags()

       
 
getDinNumBits = DPxDll['DPxGetDinNumBits']
getDinNumBits.restype = ctypes.c_int
def DPxGetDinNumBits():
    """Gets the number of bits available.
    
    This method returns the number of digital input bits in the system (24 in current implementation).
    
    Returns:
        int:   Number of bits.
        
    :Low-level C definition:
        ``int DPxGetDinNumBits()``
    
    """
    return getDinNumBits()



getDinValue = DPxDll['DPxGetDinValue']
getDinValue.restype = ctypes.c_int
def DPxGetDinValue():
    """Gets the values of the 24 DIN bits.
    
    Returns:
        int: Bit values.
        
    :Low-level C definition:
        ``int DPxGetDinValue()``
    
    """
    return getDinValue()



setDinDataDir = DPxDll['DPxSetDinDataDir']
setDinDataDir.argtypes = [ctypes.c_int]
setDinDataDir.restype = None
def DPxSetDinDataDir(direction_mask):
    """Sets the port direction mask.
    
    Sets the port direction for each bit in ``direction_mask``. The mask is one value representing all bits from the port.
    The given ``direction_mask`` will set the direction of all digital input channels. For each bit which should drive its port,
    the corresponding ``direction_mask`` value should be set to 1. An hexadecimal ``direction_mask`` can be given. 
    
    For example, ``direction_mask = 0x0000F`` will enable the port for the first 4 bits on the right. All other ports will be
    disabled.

    Args:
        int: Value which corresponds in binary to the desired open ports.
        
    :Low-level C definition:
        ``void DPxSetDinDataDir(int DirectionMask)``
        
    See Also:
        :class:`DPxGetDinDataDir`, :class:`DPxSetDinDataDir` 

    """
    setDinDataDir(direction_mask)


                      

getDinDataDir = DPxDll['DPxGetDinDataDir']
getDinDataDir.restype = ctypes.c_int
def DPxGetDinDataDir():
    """Gets the port direction mask.
    
    Returns:
        int: Bit set to 1 is an enabled port. Bit set to 0 is a disabled port.
        
    :Low-level C definition:
        ``int DPxGetDinDataDir()``

    See Also:
        :class:`DPxSetDinDataDir`, :class:`DPxSetDinDataDir`        

    """
    return getDinDataDir()



setDinDataOut = DPxDll['DPxSetDinDataOut']
setDinDataOut.restype = ctypes.c_int
setDinDataOut.restype = None
def DPxSetDinDataOut(dataOut):
    """Sets the data which should be driven on each port.
    
    In order to be able to drive the ports with the given value, the port direction has to be properly enabled.
    This can be done using the ``DPxSetDinDataDir`` with the appropriate bit mask.

    Args:
        dataOut (int): Set bit to 1 will enable the port for that bit. Set bit to 0 will disable it.
        
    :Low-level C definition:
        ``void DPxSetDinDataOut(int dataOut)``
        
    See Also:
        :class:`DPxGetDinDataDir`, :class:`DPxSetDinDataDir` 

    """
    setDinDataOut(dataOut)


 
getDinDataOut = DPxDll['DPxGetDinDataOut']
getDinDataOut.restype = ctypes.c_int
def DPxGetDinDataOut():
    """Gets the data which is being driven on each output port.
        
    This function allows the user to get the data which is currently driven on the output port.
    
    Returns:
        int: Data which is being driven on each output port.
        
    :Low-level C definition:
        ``int DPxGetDinDataOut()``

    See Also:
        :class:`DPxSetDinDataDir`, :class:`DPxSetDinDataDir`        

    """
    return getDinDataOut()



setDinDataOutStrength = DPxDll['DPxSetDinDataOutStrength']
setDinDataOutStrength.argtypes = [ctypes.c_double]
setDinDataOutStrength.restype = None
def DPxSetDinDataOutStrength(strength):
    """Sets the strength of the driven outputs.  
    
    This function allows the user to set the current (Ampere) strength of the driven outputs.
    The implementation actual value uses ``1/16`` up to ``16/16``. So minimum strength will be ``0.0625``
    and maximum will be ``1``. The strength can be increased by ``0.0625`` up to ``1``. Giving a strength
    of ``0`` will thus set it to ``0.0625``. Giving a strength between ``0.0625`` and ``0.125`` will
    round the given strength to one of the two increments.
    
    The strength is the same for all channels.
    
    Args:
        strength (float): Any value in a range of 0 to 1.
        
    :Low-level C definition:
        ``void DPxSetDinDataOutStrength(double strength)``
        
    See Also:
        :class:`DPxGetDinDataOutStrength`

    """
    setDinDataOutStrength(strength)



getDinDataOutStrength = DPxDll['DPxGetDinDataOutStrength']
getDinDataOutStrength.restype = ctypes.c_double
def DPxGetDinDataOutStrength():
    """Gets the strength of the driven outputs.
    
    This function allows the user to get the strength currently driven by the outputs.
    The implementation actual values uses 1/16 up to 16/16. So minimum strength will be 0.0625
    and maximum will be 1. The strength can be increased by 0.0625 up to 1. 
            
    Returns:
        float: Any value in a range of 0 to 1.
        
    :Low-level C definition:
        ``double DPxSetDinDataOutStrength()``
        
    See Also:
        :class:`DPxGetDinDataOutStrength`

    """
    return getDinDataOutStrength()



enableDinStabilize = DPxDll['DPxEnableDinStabilize']
enableDinStabilize.restype = None
def DPxEnableDinStabilize():
    """Enables the input stabilization mode.

    :Low-level C definition:
        ``void DPxEnableDinStabilize()``
                
    See Also:
        :class:`DPxDisableDinStabilize`, :class:`DPxIsDinStabilize`
    """
    enableDinStabilize()

    

disableDinStabilize = DPxDll['DPxDisableDinStabilize']
disableDinStabilize.restype = None
def DPxDisableDinStabilize():
    """Disables the input stabilization mode.
    
    Immediately recognize all DIN transitions, possibly with debouncing.

    :Low-level C definition:
        ``void DPxDisableDinStabilize()``
                
    See Also:
        :class:`DPxEnableDinStabilize`, :class:`DPxIsDinStabilize`
    """
    disableDinStabilize()



isDinStabilize = DPxDll['DPxIsDinStabilize']
isDinStabilize.restype = ctypes.c_int
def DPxIsDinStabilize():
    """Verifies if the hardware calibration mode is enabled.
    
    Returns:
        int: Non-zero if DIN transitions are being stabilized.

    :Low-level C definition:
        ``int DPxIsDinStabilize()``
                
    See Also:
        :class:`DPxDisableDinStabilize`, :class:`DPxEnableDinStabilize`
    """
    return isDinStabilize()



enableDinDebounce = DPxDll['DPxEnableDinDebounce']
enableDinDebounce.restype = None
def DPxEnableDinDebounce():
    """Enables the input debounce mode.
    
    When a DIN transitions, ignore further DIN transitions for next 30 milliseconds (good for response buttons)

    :Low-level C definition:
        ``void DPxEnableDinDebounce()``
                
    See Also:
        :class:`DPxDisableDinDebounce`, :class:`DPxIsDinDebounce`
    """
    enableDinDebounce()



disableDinDebounce = DPxDll['DPxDisableDinDebounce']
disableDinDebounce.restype = None 
def DPxDisableDinDebounce():
    """Enables the input debounce mode.
    
    Immediately recognize all DIN transitions (after possible stabilization).

    :Low-level C definition:
        ``void DPxDisableDinDebounce()``
                
    See Also:
        :class:`DPxEnableDinDebounce`, :class:`DPxIsDinDebounce`
    """
    disableDinDebounce()


 
isDinDebounce = DPxDll['DPxIsDinDebounce']
isDinDebounce.restype = ctypes.c_int
def DPxIsDinDebounce():
    """Verifies if the DIN debounce mode is enabled.
    
    Returns:
        int: Non-zero if DIN transitions are being debounced.

    :Low-level C definition:
        ``int DPxIsDinDebounce()``
                
    See Also:
        :class:`DPxEnableDinDebounce`, :class:`DPxDisableDinDebounce`
    """
    return isDinDebounce()




enableDoutDinLoopback = DPxDll['DPxEnableDoutDinLoopback']
enableDoutDinLoopback.restype = None  
def DPxEnableDoutDinLoopback():
    """Enables loopback between digital output ports and digital inputs.

    :Low-level C definition:
        ``void DPxEnableDoutDinLoopback()``
                
    See Also:
        :class:`DPxDisableDoutDinLoopback`, :class:`DPxIsDoutDinLoopback`
    """
    enableDoutDinLoopback()  



disableDoutDinLoopback = DPxDll['DPxDisableDoutDinLoopback']
disableDoutDinLoopback.restype = None
def DPxDisableDoutDinLoopback():
    """Disables loopback between digital outputs and digital inputs.
    
    Immediately recognize all DIN transitions (after possible stabilization).

    :Low-level C definition:
        ``void DPxDisableDoutDinLoopback()``
                
    See Also:
        :class:`DPxEnableDoutDinLoopback`, :class:`DPxIsDoutDinLoopback`
    """
    disableDoutDinLoopback() 


 
isDoutDinLoopback = DPxDll['DPxIsDoutDinLoopback']
isDoutDinLoopback.restype = ctypes.c_int 
def DPxIsDoutDinLoopback():
    """Verifies if the DIN DOUT loopback is enabled.
    
    Returns:
        int: Non-zero if DIN are driven by digital output ports.

    :Low-level C definition:
        ``int DPxIsDoutDinLoopback()``
                
    See Also:
        :class:`DPxEnableDoutDinLoopback`, :class:`DPxDisableDoutDinLoopback`
    """
    return isDoutDinLoopback()



setDinBuffBaseAddr = DPxDll['DPxSetDinBuffBaseAddr']
setDinBuffBaseAddr.restype = None
def DPxSetDinBuffBaseAddr(buffBaseAddr):
    """Sets the DIN RAM buffer start address.
    
    Must be an even value.
    
    Args:
        buffBaseAddr (int): Base address.
        
    :Low-level C definition:
        ``void DPxSetDinBuffBaseAddr(unsigned buffBaseAddr)``
        
    See Also:
        :class:`DPxGetDinBuffBaseAddr`
    
    """
    return setDinBuffBaseAddr(buffBaseAddr)



getDinBuffBaseAddr = DPxDll['DPxGetDinBuffBaseAddr']                         
getDinBuffBaseAddr.restype = ctypes.c_uint
def DPxGetDinBuffBaseAddr():
    """Gets the DIN RAM buffer start address.
    
    Returns:
        int: Base address.
        
    :Low-level C definition:
        ``unsigned DPxGetDinBuffBaseAddr()``
        
    See Also:
        :class:`DPxSetDinBuffBaseAddr`
    
    """
    return getDinBuffBaseAddr()



setDinBuffWriteAddr = DPxDll['DPxSetDinBuffWriteAddr'] 
setDinBuffWriteAddr.argtypes = [ctypes.c_uint]
setDinBuffWriteAddr.restype = None
def DPxSetDinBuffWriteAddr(buffWriteAddr):
    """Sets RAM address from which next DIN datum will be written.
    
    Must be an even value.
    
    Args:
        buffWriteAddr (int): Write address.
        
    :Low-level C definition:
        ``void DPxSetDinBuffWriteAddr(unsigned buffWriteAddr)``
        
    See Also:
        :class:`DPxGetDinBuffWriteAddr`
    
    """
    return setDinBuffWriteAddr(buffWriteAddr)



getDinBuffWriteAddr = DPxDll['DPxGetDinBuffWriteAddr']                              
getDinBuffWriteAddr.restype = ctypes.c_uint
def DPxGetDinBuffWriteAddr():
    """Gets RAM address from which next DIN datum will be written.
    
    Returns:
        int: Write address.
        
    :Low-level C definition:
        ``unsigned DPxGetDinBuffWriteAddr()``
        
    See Also:
        :class:`DPxSetDinBuffWriteAddr`
    
    """
    return getDinBuffWriteAddr()



setDinBuffSize = DPxDll['DPxSetDinBuffSize']   
setDinBuffSize.argtypes = [ctypes.c_uint]
setDinBuffSize.restype = None
def DPxSetDinBuffSize(buffSize):
    """Sets Din RAM buffer size in bytes.
    
     Must be an even value.  Buffer wraps to Base after Size.
    
    Args:
        buffSize (int): Buffer size.
        
    :Low-level C definition:
        ``void DPxSetDinBuffSize(unsigned buffSize)``
        
    See Also:
        :class:`DPxGetDinBuffSize`
    
    """
    return setDinBuffSize(buffSize)



getDinBuffSize = DPxDll['DPxGetDinBuffSize']                                          
getDinBuffSize.restype = ctypes.c_uint
def DPxGetDinBuffSize():
    """Gets the Din RAM buffer size in bytes.
    
    Returns:
        int: buffer size.
        
    :Low-level C definition:
        ``unsigned DPxGetDinBuffSize()``
        
    See Also:
        :class:`DPxSetDinBuffSize`
    
    """
    return getDinBuffSize()



setDinBuff = DPxDll['DPxSetDinBuff']  
setDinBuff.argtypes = [ctypes.c_uint, ctypes.c_uint]
setDinBuff.restype = None
def DPxSetDinBuff(buffAddr, buffSize):
    """Sets base address, write address and buffer size for Din schedules.
    
    This function is a shortcut which assigns Size/BaseAddr/WriteAddr
    
    Args:
        buffAddr (int): Base address.
        buffSize (int): Buffer size.
        
    :Low-level C definition:
        ``void DPxSetDinBuff(unsigned buffAddr, unsigned buffSize)``
        
    See Also:
        :class:`DPxGetDinSchedOnset`, :class:`DPxSetDinBuffSize`, :class:`DPxSetDinBuffWriteAddr`
    
    """
    return setDinBuff(buffAddr, buffSize)



setDinSchedOnset = DPxDll['DPxSetDinSchedOnset']
setDinSchedOnset.argtypes = [ctypes.c_uint]
setDinSchedOnset.restype = None
def DPxSetDinSchedOnset(onset):
    """Sets nanosecond delay between schedule start and first Din sample.
    
    Args:
        onset (int): delay in nanoseconds.
        
    :Low-level C definition:
        ``void DPxSetDinSchedOnset(unsigned onset)``
        
    See Also:
        :class:`DPxGetDinSchedOnset`
    
    """
    return setDinSchedOnset(onset)



getDinSchedOnset = DPxDll['DPxGetDinSchedOnset']                                
getDinSchedOnset.restype = ctypes.c_uint
def DPxGetDinSchedOnset():
    """Gets the nanosecond delay between schedule start and first Din sample.
    
    Returns:
        int: onset.
        
    :Low-level C definition:
        ``unsigned DPxGetDinSchedOnset()``
        
    See Also:
        :class:`DPxSetDinSchedOnset`
    
    """
    return getDinSchedOnset()


setDinSchedRate = DPxDll['DPxSetDinSchedRate']
setDinSchedRate.argtypes = [ctypes.c_uint, ctypes.c_int]
setDinSchedRate.restype = None
def DPxSetDinSchedRate(rate, unit):
    """Sets the schedule rate.
    
    This method allows the user to set the schedule rate. Since the rate can be given 
    with different units, the method also needs to have a unit associated with the rate.
    
    
    If no delay is required, this method does not need to be used. Default value is 0.

    Args:
        rate (int): Any positive value equal to or greater than zero.
        unit (str): Any of the predefined constants.\n
                - **hz**: samples per second, maximum 1 MHz.
                - **video**: samples per video frame, maximum 1 MHz.
                - **nano**: sample period in nanoseconds, minimum 1000 ns.
                
                    
    :Low-level C definition:
        ``void DPxSetDinSchedRate(unsigned  rateValue, int  rateUnits)``
    
    """
    setDinSchedRate(rate, api_constants[unit.upper()])



GetDinSchedRate = DPxDll['DPxGetDinSchedRate']
def DPxGetDinSchedRate():
    """
    This function gets the Din schedule rate and the rate unit.
    Return value: (schedule rate, rate unit)
    
    :Low-level C definition:
        ``unsigned DPxGetDinSchedRate(int *rateUnits)``
    """
    Var = 0
    p_Var = ctypes.c_int(Var)
    GetDinSchedRate.restype = ctypes.c_uint
    return (GetDinSchedRate(ctypes.byref(p_Var)) , rate_constants[p_Var.value])


setDinSchedCount = DPxDll['DPxSetDinSchedCount']
setDinSchedCount.argtypes = [ctypes.c_uint]
setDinSchedCount.restype = None
def DPxSetDinSchedCount(count):
    """Sets Din schedule update count.
    
    Args:
        count (int): Schedule count.
        
    :Low-level C definition:
        ``void DPxSetDinSchedCount(unsigned count)``
        
    See Also:
        :class:`DPxGetDinSchedCount`
    
    """
    return setDinSchedCount(count)



getDinSchedCount = DPxDll['DPxGetDinSchedCount']  
getDinSchedCount.restype = ctypes.c_uint
def DPxGetDinSchedCount():
    """Gets Din schedule update count.
    
    Returns:
        int: Schedule sample count.
        
    :Low-level C definition:
        ``unsigned DPxGetDinSchedCount()``
        
    See Also:
        :class:`DPxSetDinSchedCount`
    
    """
    return getDinSchedCount()



enableDinSchedCountdown = DPxDll['DPxEnableDinSchedCountdown']
enableDinSchedCountdown.restype = None   
def DPxEnableDinSchedCountdown():
    """Enables Din schedule count down.
    
    SchedCount decrements at SchedRate, and schedule stops automatically when count hits 0.

    :Low-level C definition:
        ``void DPxEnableDinSchedCountdown()``
                
    See Also:
        :class:`DPxDisableDinSchedCountdown`, :class:`DPxIsDinSchedCountdown`
    """
    enableDinSchedCountdown()



disableDinSchedCountdown = DPxDll['DPxDisableDinSchedCountdown']
disableDinSchedCountdown.restype = None   
def DPxDisableDinSchedCountdown():
    """Disables Din schedule count down.
    
    SchedCount increments at SchedRate, and schedule is stopped by calling SchedStop.

    :Low-level C definition:
        ``void DPxDisableDinSchedCountdown()``
                
    See Also:
        :class:`DPxEnableDinSchedCountdown`, :class:`DPxIsDinSchedCountdown`
    """
    disableDinSchedCountdown()



isDinSchedCountdown = DPxDll['DPxIsDinSchedCountdown']
isDinSchedCountdown.restype = ctypes.c_int
def DPxIsDinSchedCountdown():
    """Verifies if RAM buffering is enabled for a Din channel.
    
    Returns:
        int: Non-zero if SchedCount decrements to 0 and automatically stops schedule.

    :Low-level C definition:
        ``int DPxIsDinSchedCountdown()``
                
    See Also:
        :class:`DPxEnableDinSchedCountdown`, :class:`DPxDisableDinSchedCountdown`
    """
    return isDinSchedCountdown()



setDinSched = DPxDll['DPxSetDinSched']
setDinSched.restype = None
def DPxSetDinSched(onset, rateValue, rateUnits, count):
    """Sets Din schedule onset, count and rate.
    
    This function is a shortcut which assigns Onset/Rate/Count. If ``count`` is greater than zero, the count
    down mode is enabled.
    
    Args:
        onset (int): Schedule onset.
        rateValue (int): Rate value.
        rateUnits (str): Usually ``hz``. Can also be ``video`` to update every ``rateValue`` video frames or ``nano`` to update every ``rateValue`` nanoseconds.
        count (int): Schedule count.
        
    :Low-level C definition:
        ``void DPxSetDinSched(unsigned onset, unsigned rateValue, int rateUnits, unsigned count)``
    
    """
    return setDinSched(onset, rateValue, api_constants[rateUnits.upper()], count)



startDinSched = DPxDll['DPxStartDinSched']
startDinSched.restype = None
def DPxStartDinSched():
    """Starts running a Din schedule.

    :Low-level C definition:
        ``void DPxStartDinSched()``
                
    See Also:
        :class:`DPxStopDinSched`, :class:`DPxIsDinSchedRunning`
    """
    startDinSched()



stopDinSched = DPxDll['DPxStopDinSched']
stopDinSched.restype = None 
def DPxStopDinSched():
    """Stops running a Din schedule.

    :Low-level C definition:
        ``void DPxStopDinSched()``
                
    See Also:
        :class:`DPxStartDinSched`, :class:`DPxIsDinSchedRunning`
    """
    stopDinSched()



isDinSchedRunning = DPxDll['DPxIsDinSchedRunning']
isDinSchedRunning.restype = ctypes.c_int
def DPxIsDinSchedRunning():
    """Verifies if a Din schedule is currently running.
    
    Returns:
        int: Non-zero if a Din schedule is currently running, zero otherwise.
        
    :Low-level C definition:
        ``int DPxIsDinSchedRunning()``
        
    See Also:
        :class:`DPxStartDinSched`, :class:`DPxStopDinSched`
    
    """
    return isDinSchedRunning() 



enableDinLogTimetags = DPxDll['DPxEnableDinLogTimetags']
enableDinLogTimetags.restype = None
def DPxEnableDinLogTimetags():
    """Enables Din timetag mode.
    
    Each buffered Din sample is preceeded with a 64-bit nanosecond timetag.

    :Low-level C definition:
        ``void DPxEnableDinLogTimetags()``
                
    See Also:
        :class:`DPxDisableDinLogTimetags`, :class:`DPxIsDinLogTimetags`
    """
    enableDinLogTimetags()



disableDinLogTimetags = DPxDll['DPxDisableDinLogTimetags']
disableDinLogTimetags.restype = None   
def DPxDisableDinLogTimetags():
    """Disables Din timetag mode.
    
    Buffered data has no timetags.

    :Low-level C definition:
        ``void DPxDisableDinLogTimetags()``
                
    See Also:
        :class:`DPxDisableDinLogTimetags`, :class:`DPxIsDinLogTimetags`
    """
    disableDinLogTimetags()



isDinLogTimetags = DPxDll['DPxIsDinLogTimetags']
isDinLogTimetags.restype = ctypes.c_int
def DPxIsDinLogTimetags():
    """Verifies if the Din timetag mode is enabled.
    
    Returns:
        int: Non-zero if buffered data is preceeded with nanosecond timetag.
        
    :Low-level C definition:
        ``int DPxIsDinLogTimetags()``
        
    See Also:
        :class:`DPxDisableDinLogTimetags`, :class:`DPxIsDinLogTimetags`
    
    """
    return isDinLogTimetags()    



enableDinLogEvents = DPxDll['DPxEnableDinLogEvents']
enableDinLogEvents.restype = None
def DPxEnableDinLogEvents():
    """Enables log events mode.
    
    Each DIN transition is automatically logged. No schedule is required.  Best way to log response buttons.

    :Low-level C definition:
        ``void DPxEnableDinLogEvents()``
                
    See Also:
        :class:`DPxDisableDinLogEvents`, :class:`DPxIsDinLogEvents`
    """
    enableDinLogEvents()



disableDinLogEvents = DPxDll['DPxDisableDinLogEvents']
disableDinLogEvents.restype = None
def DPxDisableDinLogEvents():
    """Disables log events mode.
    
    Disables automatic logging of DIN transitions. A schedule is required to look at DIN transitions.

    :Low-level C definition:
        ``void DPxDisableDinLogEvents()``
                
    See Also:
        :class:`DPxDisableDinLogEvents`, :class:`DPxIsDinLogEvents`
    """
    disableDinLogEvents()



isDinLogEvents = DPxDll['DPxIsDinLogEvents']
isDinLogEvents.restype = ctypes.c_int
def DPxIsDinLogEvents():
    """Verifies if the Din timetag mode is enable.
    
    Returns:
        int: Non-zero if DIN transitions are being logged to RAM buffer.
        
    :Low-level C definition:
        ``int DPxIsDinLogEvents()``
        
    See Also:
        :class:`DPxDisableDinLogEvents`, :class:`DPxEnableDinLogEvents`
    
    """
    return isDinLogEvents() 



getDoutNumBits = DPxDll['DPxGetDoutNumBits']
getDoutNumBits.restype = ctypes.c_int
def DPxGetDoutNumBits():
    """Gets the number of bits available.
    
    This method returns the number of digital output bits in the system (24 in current implementation).
    
    Returns:
        int:   Number of bits.
        
    :Low-level C definition:
        ``int DPxGetDoutNumBits()``
    
    """
    return getDoutNumBits()



setDoutValue = DPxDll['DPxSetDoutValue'] 
setDoutValue.argtypes = [ctypes.c_int, ctypes.c_int]
setDoutValue.restype = None
def DPxSetDoutValue(bit_value, bit_mask):
    """Sets the port direction mask.
    
    Sets the port direction for each bit in ``bit_mask``. The mask is one value representing all bits from the port.
    The given ``bit_mask`` will set the direction of all digital input channels. For each bit which should drive its port,
    the corresponding ``direction_mask`` value should be set to 1. An hexadecimal ``direction_mask`` can be given. 
    
    For example, ``bit_mask = 0x0000F`` will enable the port for the first 4 bits on the right. All other ports will be
    disabled.

    Args:
        bit_value (int): value of bits.
        bit_mask (int): Turns on or off the specific Digital Out channel. 1 for on, 0 for off.
        
    :Low-level C definition:
        ``void DPxSetDoutValue(int bitValue, int bitMask)``

    """
    setDoutValue(bit_value, bit_mask)



getDoutValue = DPxDll['DPxGetDoutValue']
getDoutValue.restype = ctypes.c_int
def DPxGetDoutValue():
    """Gets the values of the 24 Dout bits.
    
    Returns:
        int: Bit values.
        
    :Low-level C definition:
        ``int DPxGetDoutValue()``
    
    """
    return getDoutValue()



enableDoutButtonSchedules = DPxDll['DPxEnableDoutButtonSchedules']
enableDoutButtonSchedules.restype = None
def DPxEnableDoutButtonSchedules():
    """Enables automatic DOUT schedules upon DIN button presses.

    :Low-level C definition:
        ``void DPxEnableDoutButtonSchedules()``
                
    See Also:
        :class:`DPxDisableDoutButtonSchedules`, :class:`DPxIsDoutButtonSchedules`
    """
    enableDoutButtonSchedules()



disableDoutButtonSchedules = DPxDll['DPxDisableDoutButtonSchedules']
disableDoutButtonSchedules.restype = None 
def DPxDisableDoutButtonSchedules():
    """Disables automatic DOUT schedules upon DIN button presses.

    :Low-level C definition:
        ``void DPxDisableDoutButtonSchedules()``
                
    See Also:
        :class:`DPxEnableDoutButtonSchedules`, :class:`DPxIsDoutButtonSchedules`
    """
    disableDoutButtonSchedules()



isDoutButtonSchedules = DPxDll['DPxIsDoutButtonSchedules']
isDoutButtonSchedules.restype = ctypes.c_int 
def DPxIsDoutButtonSchedules():
    """Verifies if the DOUT automatic DOUT schedules mode is enabled.
    
    Returns:
        int: Non-zero if automatic DOUT schedules occur upon DIN button presses.
        
    :Low-level C definition:
        ``int DPxIsDoutButtonSchedules()``
        
    See Also:
        :class:`DPxEnableDoutButtonSchedules`, :class:`DPxDisableDoutButtonSchedules`
    
    """
    return isDoutButtonSchedules()



enableDoutBacklightPulse = DPxDll['DPxEnableDoutBacklightPulse']
enableDoutBacklightPulse.restype = None  
def DPxEnableDoutBacklightPulse():
    """Enables the Dout backlight pulse mode.
    
    LCD backlight LED are controlled by DOUT15. Can be used to make a tachistoscope by pulsing DOUT15 with a schedule.

    :Low-level C definition:
        ``void DPxEnableDoutBacklightPulse()``
                
    See Also:
        :class:`DPxDisableDoutBacklightPulse`, :class:`DPxIsDoutBacklightPulse`
    """
    enableDoutBacklightPulse()



 
disableDoutBacklightPulse = DPxDll['DPxDisableDoutBacklightPulse']
disableDoutBacklightPulse.restype = None 
def DPxDisableDoutBacklightPulse():
    """Disables the Dout backlight pulse mode.
    
    LCD backlight LEDs are unaffected by DOUT system.

    :Low-level C definition:
        ``void DPxDisableDoutBacklightPulse()``
                
    See Also:
        :class:`DPxEnableDoutBacklightPulse`, :class:`DPxIsDoutBacklightPulse`
    """
    disableDoutBacklightPulse()



isDoutBacklightPulse = DPxDll['DPxIsDoutBacklightPulse']
isDoutBacklightPulse.restype = ctypes.c_int 
def DPxIsDoutBacklightPulse():
    """Verifies if the Dout backlight pulse mode is enabled.
    
    Returns:
        int: Non-zero if LCD backlight LED enables are gated by DOUT15.
        
    :Low-level C definition:
        ``int DPxIsDoutBacklightPulse()``
        
    See Also:
        :class:`DPxEnableDoutBacklightPulse`, :class:`DPxDisableDoutBacklightPulse`
    
    """
    return isDoutBacklightPulse()



setDoutBuffBaseAddr = DPxDll['DPxSetDoutBuffBaseAddr']
setDoutBuffBaseAddr.argtypes = [ctypes.c_uint]
setDoutBuffBaseAddr.restype = None
def DPxSetDoutBuffBaseAddr(buffBaseAddr):
    """Sets the Dout RAM buffer start address.
    
    Must be an even value.
    
    Args:
        buffBaseAddr (int): Base address.
        
    :Low-level C definition:
        ``void DPxSetDoutBuffBaseAddr(unsigned buffBaseAddr)``
        
    See Also:
        :class:`DPxGetDoutBuffBaseAddr`
    
    """
    return setDoutBuffBaseAddr(buffBaseAddr)



getDoutBuffBaseAddr = DPxDll['DPxGetDoutBuffBaseAddr']                           
getDoutBuffBaseAddr.restype = ctypes.c_uint
def DPxGetDoutBuffBaseAddr():
    """Gets the Dout RAM buffer start address.
    
    Returns:
        int: Base address.
        
    :Low-level C definition:
        ``unsigned DPxGetDoutBuffBaseAddr()``
        
    See Also:
        :class:`DPxSetDoutBuffBaseAddr`
    
    """
    return getDoutBuffBaseAddr()



setDoutBuffReadAddr = DPxDll['DPxSetDoutBuffReadAddr']
setDoutBuffReadAddr.argtypes = [ctypes.c_uint]
setDoutBuffReadAddr.restype = None
def DPxSetDoutBuffReadAddr(buffReadAddr):
    """Sets RAM address from which next Dout datum will be read.
    
    Must be an even value.
    
    Args:
        buffReadAddr (int): Read address.
        
    :Low-level C definition:
        ``void DPxSetDoutBuffReadAddr(unsigned buffReadAddr)``
        
    See Also:
        :class:`DPxGetDoutBuffReadAddr`
    
    """
    return setDoutBuffReadAddr(buffReadAddr)



getDoutBuffReadAddr = DPxDll['DPxGetDoutBuffReadAddr']                            
getDoutBuffReadAddr.restype = ctypes.c_uint
def DPxGetDoutBuffReadAddr():
    """Gets RAM address from which next Dout datum will be read.
    
    Returns:
        int: Read address.
        
    :Low-level C definition:
        ``unsigned DPxGetDoutBuffReadAddr()``
        
    See Also:
        :class:`DPxSetDoutBuffReadAddr`
    
    """
    return getDoutBuffReadAddr()



setDoutBuffSize = DPxDll['DPxSetDoutBuffSize']
setDoutBuffSize.argtypes = [ctypes.c_uint]
setDoutBuffSize.restype = None 
def DPxSetDoutBuffSize(buffSize):
    """Sets Dout RAM buffer size in bytes.
    
     Must be an even value.  Buffer wraps to Base after Size.
    
    Args:
        buffSize (int): Buffer size.
        
    :Low-level C definition:
        ``void DPxSetDoutBuffSize(unsigned buffSize)``
        
    See Also:
        :class:`DPxGetDoutBuffReadAddr`
    
    """
    return setDoutBuffSize(buffSize)



getDoutBuffSize = DPxDll['DPxGetDoutBuffSize']                                         
getDoutBuffSize.restype = ctypes.c_uint
def DPxGetDoutBuffSize():
    """Gets the Dout RAM buffer size in bytes.
    
    Returns:
        int: buffer size.
        
    :Low-level C definition:
        ``unsigned DPxGetDoutBuffSize()``
        
    See Also:
        :class:`DPxSetDoutBuffSize`
    
    """
    return getDoutBuffSize()



setDoutBuff = DPxDll['DPxSetDoutBuff']
setDoutBuff.argtypes = [ctypes.c_uint, ctypes.c_uint]
setDoutBuff.restype = None 
def DPxSetDoutBuff(buffAddr, buffSize):
    """Sets base address, read address and buffer size for Dout schedules.
    
    This function is a shortcut which assigns Size/BaseAddr/ReadAddr
    
    Args:
        buffAddr (int): Base address.
        buffSize (int): Buffer size.
        
    :Low-level C definition:
        ``void DPxSetDoutBuff(unsigned buffAddr, unsigned buffSize)``
        
    See Also:
        :class:`DPxGetDoutSchedOnset`, :class:`DPxSetDoutBuffSize`, :class:`DPxSetDoutBuffReadAddr`
    
    """
    return setDoutBuff(buffAddr, buffSize)



setDoutSchedOnset = DPxDll['DPxSetDoutSchedOnset']
setDoutSchedOnset.argtypes = [ctypes.c_uint]
setDoutSchedOnset.restype = None
def DPxSetDoutSchedOnset(onset):
    """Sets nanosecond delay between schedule start and first Dout update.
    
    Args:
        onset (int): delay in nanoseconds.
        
    :Low-level C definition:
        ``void DPxSetDoutSchedOnset(unsigned onset)``
        
    See Also:
        :class:`DPxGetDoutSchedOnset`
    
    """
    return setDoutSchedOnset(onset)
 
 

getDoutSchedOnset = DPxDll['DPxGetDoutSchedOnset']                             
getDoutSchedOnset.restype = ctypes.c_uint
def DPxGetDoutSchedOnset():
    """Gets the nanosecond delay between schedule start and first Dout update.
    
    Returns:
        int: onset.
        
    :Low-level C definition:
        ``unsigned DPxGetDoutSchedOnset()``
        
    See Also:
        :class:`DPxSetDoutSchedOnset`
    
    """
    return getDoutSchedOnset()



setDoutSchedRate = DPxDll['DPxSetDoutSchedRate']  
setDoutSchedRate.argtypes = [ctypes.c_uint, ctypes.c_int]
setDoutSchedRate.restype = None
def DPxSetDoutSchedRate(rate, unit):
    """Sets the schedule rate.
        
        This method allows the user to set the schedule rate. Since the rate can be given 
        with different units, the method also needs to have a unit associated with the rate.

        Args:
            rate (int): Any positive value equal to or greater than zero.
            unit (str): Any of the predefined constants. \n
                    -**hz**: rate updates per second, maximum 10 MHz.
                    -**video**: rate updates per video frame, maximum 10 MHz.
                    -**nano**: rate updates period in nanoseconds, minimum 100 ns.
        
        
        :Low-level C definition:                
            ``void DPxSetDoutSchedRate(unsigned rateValue, int rateUnits)``
    """
    setDoutSchedRate(rate, api_constants[unit.upper()])



getDoutSchedRate = DPxDll['DPxGetDoutSchedRate']
def DPxGetDoutSchedRate():
    """Gets Dout schedule update rate and the rate units.
    
    Returns:
        tuple: rate and unit.
        
    :Low-level C definition:
        ``unsigned DPxGetDoutSchedRate(int *rateUnits)``
        
    See Also:
        :class:`DPxSetDoutSchedRate`
    
    """
    Var = 0
    p_Var = ctypes.c_int(Var)
    getDoutSchedRate.restype = ctypes.c_uint
    return (getDoutSchedRate(ctypes.byref(p_Var)), rate_constants[p_Var.value])



setDoutSchedCount = DPxDll['DPxSetDoutSchedCount']
setDoutSchedCount.argtypes = [ctypes.c_uint]
setDoutSchedCount.restype = None
def DPxSetDoutSchedCount(count):
    """Sets Dout schedule update count.
    
    Args:
        count (int): Schedule count.
        
    :Low-level C definition:
        ``void DPxSetDoutSchedCount(unsigned count)``
        
    See Also:
        :class:`DPxGetDoutSchedCount`
    
    """
    return setDoutSchedCount(count)



getDoutSchedCount = DPxDll['DPxGetDoutSchedCount']                              
getDoutSchedCount.restype = ctypes.c_uint
def DPxGetDoutSchedCount():
    """Gets Dout schedule update count.
    
    Returns:
        int: Schedule sample count.
        
    :Low-level C definition:
        ``unsigned DPxGetDoutSchedCount()``
        
    See Also:
        :class:`DPxSetDoutSchedCount`
    
    """
    return getDoutSchedCount()



enableDoutSchedCountdown = DPxDll['DPxEnableDoutSchedCountdown']
enableDoutSchedCountdown.restype = None 
def DPxEnableDoutSchedCountdown():
    """Enables Dout schedule count down.
    
    SchedCount decrements at SchedRate, and schedule stops automatically when count hits 0.

    :Low-level C definition:
        ``void DPxEnableDoutSchedCountdown()``
                
    See Also:
        :class:`DPxDisableDoutSchedCountdown`, :class:`DPxIsDoutSchedCountdown`
    """
    enableDoutSchedCountdown()



disableDoutSchedCountdown = DPxDll['DPxDisableDoutSchedCountdown']
disableDoutSchedCountdown.restype = None
def DPxDisableDoutSchedCountdown():
    """Disables Dout schedule count down.
    
    SchedCount increments at SchedRate, and schedule is stopped by calling SchedStop.

    :Low-level C definition:
        ``void DPxDisableDoutSchedCountdown()``
                
    See Also:
        :class:`DPxEnableDoutSchedCountdown`, :class:`DPxIsDoutSchedCountdown`
    """
    disableDoutSchedCountdown()



isDoutSchedCountdown = DPxDll['DPxIsDoutSchedCountdown']
isDoutSchedCountdown.restype = ctypes.c_int
def DPxIsDoutSchedCountdown():
    """Verifies if RAM buffering is enabled for a Dout channel.
    
    Returns:
        int: Non-zero if SchedCount decrements to 0 and automatically stops schedule.

    :Low-level C definition:
        ``int DPxIsDoutSchedCountdown()``
                
    See Also:
        :class:`DPxEnableDoutSchedCountdown`, :class:`DPxDisableDoutSchedCountdown`
    """
    return isDoutSchedCountdown()



setDoutSched = DPxDll['DPxSetDoutSched']
setDoutSched.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint]
setDoutSched.restype = None
def DPxSetDoutSched(onset, rateValue, rateUnits, count):
    """Sets Dout schedule onset, count and rate.
    
    This function is a shortcut which assigns Onset/Rate/Count. If ``count`` is greater than zero, the count
    down mode is enabled.
    
    Args:
        onset (int): Schedule onset.
        rateValue (int): Rate value.
        rateUnits (str): Usually ``hz``. Can also be ``video`` to update every ``rateValue`` video frames or ``nano`` to update every ``rateValue`` nanoseconds.
        count (int): Schedule count.
        
    :Low-level C definition:
        ``void DPxSetDoutSched(unsigned onset, unsigned rateValue, int rateUnits, unsigned count)``
    
    """
    return setDoutSched(onset, rateValue, api_constants[rateUnits.upper()], count)


startDoutSched = DPxDll['DPxStartDoutSched']
startDoutSched.restype = None
def DPxStartDoutSched():
    """Starts running a Dout schedule.

    :Low-level C definition:
        ``void DPxStartDoutSched()``
                
    See Also:
        :class:`DPxStopDoutSched`, :class:`DPxIsDoutSchedRunning`
    """
    startDoutSched()

      

stopDoutSched = DPxDll['DPxStopDoutSched']
stopDoutSched.restype = None
def DPxStopDoutSched():
    """Stops running a Dout schedule.

    :Low-level C definition:
        ``void DPxStopDoutSched()``
                
    See Also:
        :class:`DPxStartDoutSched`, :class:`DPxIsDoutSchedRunning`
    """
    stopDoutSched()



isDoutSchedRunning = DPxDll['DPxIsDoutSchedRunning']
isDoutSchedRunning.restype = ctypes.c_int
def DPxIsDoutSchedRunning():
    """Verifies if a Dout schedule is currently running.
    
    Returns:
        int: Non-zero if a Dout schedule is currently running, zero otherwise.
        
    :Low-level C definition:
        ``int DPxIsDoutSchedRunning()``
        
    See Also:
        :class:`DPxStartDoutSched`, :class:`DPxStopDoutSched`
    
    """
    return isDoutSchedRunning()   


enableDoutPixelMode = DPxDll['DPxEnableDoutPixelMode']
enableDoutPixelMode.restype = None 
def DPxEnableDoutPixelMode():
    """Enables pixel mode.

    When this function is enabled, the digital outputs show the RGB value of first upper left pixel of the screen.
    In which case, digital outputs cannot be used for other purposes.
    This feature is only available on VIEWPixx with firmware revision 31 and higher.

    :Low-level C definition:
        ``void DPxEnableDoutPixelMode()``
                
    See Also:
        :class:`DPxDisableDoutPixelMode`, :class:`DPxIsDoutPixelMode`
    """
    enableDoutPixelMode()



disableDoutPixelMode = DPxDll['DPxDisableDoutPixelMode']
disableDoutPixelMode.restype = None
def DPxDisableDoutPixelMode():
    """Disables pixel mode.
    
    When this function is disabled, the digital ouputs do not show the RGB value of first upper left pixel of the screen.
    The digital outputs can then be used normally. This is the default mode.
    This feature is only available on VIEWPixx with firmware revision 31 and higher.

    :Low-level C definition:
        ``void DPxDisableDoutPixelMode()``
                
    See Also:
        :class:`DPxEnableDoutPixelMode`, :class:`DPxIsDoutPixelMode`
    """
    disableDoutPixelMode()



isDoutPixelMode = DPxDll['DPxIsDoutPixelMode']
isDoutPixelMode.restype = ctypes.c_int
def DPxIsDoutPixelMode():
    """Verifies if the pixel mode is enabled on digital outputs.
    
    Returns:
        int: Non-zero if pixel mode is enabled, 0 if disabled.

    :Low-level C definition:
        ``int DPxIsDoutPixelMode()``
                
    See Also:
        :class:`DPxEnableDoutPixelMode`, :class:`DPxDisableDoutPixelMode`
    """
    return isDoutPixelMode()  



enableTouchpixx = DPxDll['DPxEnableTouchpixx']
enableTouchpixx.restype = None
def DPxEnableTouchpixx():
    """Enables the TOUCHPixx touch panel hardware subsystem.

    :Low-level C definition:
        ``void DPxEnableTouchpixx()``
                
    See Also:
        :class:`DPxDisableTouchpixx`, :class:`DPxIsTouchpixx`
    """
    enableTouchpixx()



disableTouchpixx = DPxDll['DPxDisableTouchpixx']
disableTouchpixx.restype = None
def DPxDisableTouchpixx():
    """Disables the TOUCHPixx touch panel hardware subsystem.

    :Low-level C definition:
        ``void DPxDisableTouchpixx()``
                
    See Also:
        :class:`DPxEnableTouchpixx`, :class:`DPxIsTouchpixx`
    """
    disableTouchpixx()



isTouchpixx = DPxDll['DPxIsTouchpixx']
isTouchpixx.restype = ctypes.c_int 
def DPxIsTouchpixx():
    """Verifies if a Dout schedule is currently running.
    
    Returns:
        int: Non-zero if TOUCHPixx touch panel hardware is present and enabled.
        
    :Low-level C definition:
        ``int DPxIsTouchpixx()``
        
    See Also:
        :class:`DPxEnableTouchpixx`, :class:`DPxDisableTouchpixx`
    
    """
    return isTouchpixx()


setTouchpixxBuffBaseAddr = DPxDll['DPxSetTouchpixxBuffBaseAddr']  
setTouchpixxBuffBaseAddr.argtypes = [ctypes.c_uint]
setTouchpixxBuffBaseAddr.restype = None
def DPxSetTouchpixxBuffBaseAddr(buffBaseAddr):
    """Sets the Touchpixx RAM buffer start address.
    
    Must be an even value.
    
    Args:
        buffBaseAddr (int): Base address.
        
    :Low-level C definition:
        ``void DPxSetTouchpixxBuffBaseAddr(unsigned buffBaseAddr)``
        
    See Also:
        :class:`DPxGetTouchpixxBuffBaseAddr`
    
    """
    return setTouchpixxBuffBaseAddr(buffBaseAddr)



getTouchpixxBuffBaseAddr = DPxDll['DPxGetTouchpixxBuffBaseAddr']                             
getTouchpixxBuffBaseAddr.restype = ctypes.c_uint
def DPxGetTouchpixxBuffBaseAddr():
    """Gets the Touchpixx RAM buffer start address.
    
    Returns:
        int: Base address.
        
    :Low-level C definition:
        ``unsigned DPxGetDacBuffBaseAddr()``
        
    See Also:
        :class:`DPxSetTouchpixxBuffBaseAddr`
    
    """
    return getTouchpixxBuffBaseAddr()


                
setTouchpixxBuffWriteAddr= DPxDll['DPxSetTouchpixxBuffWriteAddr']    
setTouchpixxBuffWriteAddr.argtypes = [ctypes.c_uint]
setTouchpixxBuffWriteAddr.restype = None
def DPxSetTouchpixxBuffWriteAddr(buffWriteAddr):
    """Sets RAM address from which next Touchpixx datum will be written.
    
    Must be an even value.
    
    Args:
        buffWriteAddr (int): Write address.
        
    :Low-level C definition:
        ``void DPxSetTouchpixxBuffWriteAddr(unsigned buffWriteAddr)``
        
    See Also:
        :class:`DPxGetTouchpixxBuffWriteAddr`
    
    """
    return setTouchpixxBuffWriteAddr(buffWriteAddr)


                              
getTouchpixxBuffWriteAddr = DPxDll['DPxGetTouchpixxBuffWriteAddr']                              
getTouchpixxBuffWriteAddr.restype = ctypes.c_uint
def DPxGetTouchpixxBuffWriteAddr():
    """Gets RAM address from which the next TOUCHPixx datum will be written.
    
    Returns:
        int: Write address.
        
    :Low-level C definition:
        ``unsigned DPxGetTouchpixxBuffWriteAddr()``
        
    See Also:
        :class:`DPxSetTouchpixxBuffWriteAddr`
    
    """
    return getTouchpixxBuffWriteAddr()



setTouchpixxBuffSize = DPxDll['DPxSetTouchpixxBuffSize']   
setTouchpixxBuffSize.argtypes = [ctypes.c_uint]
setTouchpixxBuffSize.restype = None
def DPxSetTouchpixxBuffSize(buffSize):
    """Sets Touchpixx RAM buffer size in bytes.
    
     Must be an even value.  Buffer wraps to Base after Size.
    
    Args:
        buffSize (int): Buffer size.
        
    :Low-level C definition:
        ``void DPxSetTouchpixxBuffSize(unsigned buffSize)``
        
    See Also:
        :class:`DPxGetTouchpixxBuffSize`
    
    """
    return setTouchpixxBuffSize(buffSize)



getTouchpixxBuffSize = DPxDll['DPxGetTouchpixxBuffSize']                                          
getTouchpixxBuffSize.restype = ctypes.c_uint
def DPxGetTouchpixxBuffSize():
    """Gets the Touchpixx RAM buffer size in bytes.
    
    Returns:
        int: buffer size.
        
    :Low-level C definition:
        ``unsigned DPxGetTouchpixxBuffSize()``
        
    See Also:
        :class:`DPxSetTouchpixxBuffSize`
    
    """
    return getTouchpixxBuffSize()



setTouchpixxBuff = DPxDll['DPxSetTouchpixxBuff']  
setTouchpixxBuff.argtypes = [ctypes.c_uint, ctypes.c_uint]
setTouchpixxBuff.restype = None
def DPxSetTouchpixxBuff(buffAddr, buffSize):
    """Sets base address, write address and buffer size for Touchpixx schedules.
    
    This function is a shortcut which assigns Size/BaseAddr/WriteAddr
    
    Args:
        buffAddr (int): Base address.
        buffSize (int): Buffer size.
        
    :Low-level C definition:
        ``void DPxSetTouchpixxBuff(unsigned buffAddr, unsigned buffSize)``
        
    See Also:
        :class:`DPxSetTouchpixxBuffSize`, :class:`DPxSetTouchpixxBuffWriteAddr`
    
    """
    return setTouchpixxBuff(buffAddr, buffSize)



enableTouchpixxLogEvents = DPxDll['DPxEnableTouchpixxLogEvents']
enableTouchpixxLogEvents.restype = None
def DPxEnableTouchpixxLogEvents():
    """Enables log events mode.
    
    Each Touchpixx transition is automatically logged. No schedule is required.  Best way to log response buttons.

    :Low-level C definition:
        ``void DPxEnableTouchpixxLogEvents()``
                
    See Also:
        :class:`DPxDisableTouchpixxLogEvents`, :class:`DPxIsTouchpixxLogEvents`
    """
    enableTouchpixxLogEvents()



disableTouchpixxLogEvents = DPxDll['DPxDisableTouchpixxLogEvents']
disableTouchpixxLogEvents.restype = None
def DPxDisableTouchpixxLogEvents():
    """Disables log events mode.
    
    Disables automatic logging of Touchpixx transitions. A schedule is needed to log transitions.

    :Low-level C definition:
        ``void DPxDisableTouchpixxLogEvents()``
                
    See Also:
        :class:`DPxDisableTouchpixxLogEvents`, :class:`DPxIsTouchpixxLogEvents`
    """
    disableTouchpixxLogEvents()



isTouchpixxLogEvents = DPxDll['DPxIsTouchpixxLogEvents']
isTouchpixxLogEvents.restype = ctypes.c_int
def DPxIsTouchpixxLogEvents():
    """Verifies if the Touchpixx timetag mode is enabled.
    
    Returns:
        int: Non-zero if Touchpixx transitions are being logged to RAM buffer.
        
    :Low-level C definition:
        ``int DPxIsTouchpixxLogEvents()``
        
    See Also:
        :class:`DPxDisableTouchpixxLogEvents`, :class:`DPxEnableTouchpixxLogEvents`
    
    """
    return isTouchpixxLogEvents()  



enableTouchpixxLogTimetags = DPxDll['DPxEnableTouchpixxLogTimetags']
enableTouchpixxLogTimetags.restype = None
def DPxEnableTouchpixxLogTimetags():
    """Enables Touchpixx timetag mode.
    
    Each buffered Touchpixx sample is preceeded with a 64-bit nanosecond timetag.

    :Low-level C definition:
        ``void DPxEnableTouchpixxLogTimetags()``
                
    See Also:
        :class:`DPxDisableTouchpixxLogTimetags`, :class:`DPxIsTouchpixxLogTimetags`
    """
    enableTouchpixxLogTimetags()



disableTouchpixxLogTimetags = DPxDll['DPxDisableTouchpixxLogTimetags']
disableTouchpixxLogTimetags.restype = None   
def DPxDisableTouchpixxLogTimetags():
    """Disables Touchpixx timetag mode.
    
    Buffered data has no timetags.

    :Low-level C definition:
        ``void DPxDisableTouchpixxLogTimetags()``
                
    See Also:
        :class:`DPxDisableTouchpixxLogTimetags`, :class:`DPxIsTouchpixxLogTimetags`
    """
    disableTouchpixxLogTimetags()



isTouchpixxLogTimetags = DPxDll['DPxIsTouchpixxLogTimetags']
isTouchpixxLogTimetags.restype = ctypes.c_int
def DPxIsTouchpixxLogTimetags():
    """Verifies if the Touchpixx timetag mode is enabled.
    
    Returns:
        int: Non-zero if buffered data is preceeded with nanosecond timetag.
        
    :Low-level C definition:
        ``int DPxIsTouchpixxLogTimetags()``
        
    See Also:
        :class:`DPxDisableTouchpixxLogTimetags`, :class:`DPxIsTouchpixxLogTimetags`
    
    """
    return isTouchpixxLogTimetags()  



enableTouchpixxLogContinuousMode = DPxDll['DPxEnableTouchpixxLogContinuousMode']
enableTouchpixxLogContinuousMode.restype = None
def DPxEnableTouchpixxLogContinuousMode():
    """Enables Touchpixx continuous logging mode.
    
    TOUCHPixx logging returns continuous position updates during a panel press.

    :Low-level C definition:
        ``void DPxEnableTouchpixxLogContinuousMode()``
                
    See Also:
        :class:`DPxDisableTouchpixxLogContinuousMode`, :class:`DPxIsTouchpixxLogContinuousMode`
    """
    enableTouchpixxLogContinuousMode()



disableTouchpixxLogContinuousMode = DPxDll['DPxDisableTouchpixxLogContinuousMode']
disableTouchpixxLogContinuousMode.restype = None
def DPxDisableTouchpixxLogContinuousMode():
    """Disables Touchpixx continuous logging mode.
    
    TOUCHPixx logging only returns initial press and release events.

    :Low-level C definition:
        ``void DPxDisableTouchpixxLogContinuousMode()``
                
    See Also:
        :class:`DPxDisableTouchpixxLogContinuousMode`, :class:`DPxIsTouchpixxLogContinuousMode`
    """
    disableTouchpixxLogContinuousMode()

    
 
isTouchpixxLogContinuousMode = DPxDll['DPxIsTouchpixxLogContinuousMode']
isTouchpixxLogContinuousMode.restype = ctypes.c_int
def DPxIsTouchpixxLogContinuousMode():
    """Verifies if the TOUCHPixx continuous logging mode is enabled.
    
    Returns:
        int:    Non-zero if the TOUCHPixx is in continuous logging mode, zero otherwise.

    :Low-level C definition:
        ``void DPxIsTouchpixxLogContinuousMode()``
                
    See Also:
        :class:`DPxDisableTouchpixxLogContinuousMode`, :class:`DPxEnableTouchpixxLogContinuousMode`
    """
    return isTouchpixxLogContinuousMode()




setTouchpixxStabilizeDuration = DPxDll['DPxSetTouchpixxStabilizeDuration']   
setTouchpixxStabilizeDuration.argtypes = [ctypes.c_double]
setTouchpixxStabilizeDuration.restype = None
def DPxSetTouchpixxStabilizeDuration(duration):
    """Sets the Touchpixx stabilization duration.
    
    This function sets duration in seconds that TOUCHPixx panel coordinates must be stable before being recognized as a touch in :class:`DPxGetTouchpixxCoords`
    
    Args:
        duration (int): Duration in seconds.
        
    :Low-level C definition:
        ``void DPxSetTouchpixxStabilizeDuration(double duration)``
        
    See Also:
        :class:`DPxGetTouchpixxStabilizeDuration`
    
    """
    return setTouchpixxStabilizeDuration(duration)




getTouchpixxStabilizeDuration = DPxDll['DPxGetTouchpixxStabilizeDuration']
getTouchpixxStabilizeDuration.restype = ctypes.c_double
def DPxGetTouchpixxStabilizeDuration():
    """Gets the Touchpixx stabilization duration.
    
    Gets the duration in seconds that TOUCHPixx panel coordinates must be stable before being recognized as a touch in :class:`DPxGetTouchpixxCoords`
    
    Returns:
        float: duration in seconds.
        
    :Low-level C definition:
        ``unsigned DPxGetTouchpixxStabilizeDuration()``
        
    See Also:
        :class:`DPxSetTouchpixxStabilizeDuration`
    
    """
    return getTouchpixxStabilizeDuration()


#int      DPxIsTouchpixxPressed()   
# Returns Non-zero if touch panel is currently pressed
IsTouchpixxPressed = DPxDll['DPxIsTouchpixxPressed']
IsTouchpixxPressed.restype = ctypes.c_int    
def DPxIsTouchpixxPressed():
    """Returns Non-zero if touch panel is currently pressed
    
    :Low-level C definition:
        ``int DPxIsTouchpixxPressed()``
    """
    return IsTouchpixxPressed()


# void    DPxGetTouchpixxCoords(int* x, int* y)
# Get the current touch panel X/Y coordinates.  Returns (0,0) if panel not pressed.
GetTouchpixxCoords = DPxDll['DPxGetTouchpixxCoords']
def DPxGetTouchpixxCoords():
    """Gets the current touch panel ``(X,Y)`` coordinates.  Returns ``(0,0)`` if panel not pressed.
    
    Returns:
        A tuple that contains the current pressed ``(X,Y)`` coordinate. ``(0,0)`` is returned when nothing is pressed. If there are multiple presses, it returns an average.
        
    :Low-level C definition:
        ``void DPxGetTouchpixxCoords(int* x, int* y)``
    """
    X = 0
    Y = 0
    p_X = ctypes.c_int(X)
    p_Y = ctypes.c_int(Y)
    GetTouchpixxCoords(ctypes.byref(p_X), ctypes.byref(p_Y))
    return (p_X.value, p_Y.value)



# void   DPxInitAudCodec()
# Call this once before other Aud/Mic routines to configure initial audio CODEC state
InitAudCodec = DPxDll['DPxInitAudCodec']
InitAudCodec.restype = None
def DPxInitAudCodec():
    """Initialize the required subsystems to play audio.
    
    You are required to call this once before other audio or microphone routines
    to configure initial audio CODEC state.
    
    :Low-level C definition:
        ``void DPxInitAudCodec()``
    """
    return InitAudCodec()

# void   DPxSetAudLeftValue(int value) 
# Set the 16-bit 2's complement signed value for the Left audio output channel
SetAudLeftValue = DPxDll['DPxSetAudLeftValue']
SetAudLeftValue.argtypes = [ctypes.c_int]
SetAudLeftValue.restype = None
def DPxSetAudLeftValue(volume):
    """Set the 16-bit 2's complement signed value for the Left audio output channel
    
    Args:
        volume (float): Value for the desired volume, between 0 and 1.
        
    :Low-level C definition:
        ``void DPxSetAudLeftValue(int value)``
    """
    return SetAudLeftValue(volume)

# void   DPxSetAudRightValue(int value)
# Set the 16-bit 2's complement signed value for the Right audio output channel
SetAudRightValue = DPxDll['DPxSetAudRightValue']
SetAudRightValue.argtypes = [ctypes.c_int]
SetAudRightValue.restype = None
def DPxSetAudRightValue(volume):
    """Set the 16-bit 2's complement signed value for the Right audio output channel
    
    Args:
        volume (float): Value for the desired volume, between 0 and 1.
        
    :Low-level C definition:
        ``void DPxSetAudRightValue(int value)``
    """
    return SetAudRightValue(volume)


#  int DPxGetAudLeftValue()
# Get the 16-bit 2's complement signed value for the Left audio output channel
GetAudLeftValue = DPxDll['DPxGetAudLeftValue'] 
GetAudLeftValue.restype = ctypes.c_int
def DPxGetAudLeftValue():
    """Get the 16-bit 2's complement signed value for the Left audio output channel
    
    :Low-level C definition:
        ``int DPxGetAudLeftValue()``
    """
    return GetAudLeftValue()
   
#  int DPxGetAudRightValue()
# Get the 16-bit 2's complement signed value for the Right audio output channel
GetAudRightValue = DPxDll['DPxGetAudRightValue']        
GetAudRightValue.restype = ctypes.c_int   
def DPxGetAudRightValue():
    """Get the 16-bit 2's complement signed value for the Right audio output channel
    
    :Low-level C definition:
        ``int DPxGetAudRightValue()``
    """
    return GetAudRightValue()


#  void DPxSetAudLeftVolume(double volume)
# Set volume for the Left audio output channel, range 0-1
SetAudLeftVolume = DPxDll['DPxSetAudLeftVolume']
SetAudLeftVolume.argtypes = [ctypes.c_double]
SetAudLeftVolume.restype = None
def DPxSetAudLeftVolume(volume):
    """ Sets volume for the Right audio channels, range 0-1
    
    Args:
        volume (float): Value for the desired volume, between 0 and 1.
        
    :Low-level C definition:
        ``void DPxSetAudRightVolume(double volume)``
    """
    SetAudLeftVolume(volume)

#  void DPxSetAudRightVolume(double volume)
# Set volume for the Right audio output channel, range 0-1
SetAudRightVolume = DPxDll['DPxSetAudRightVolume']
SetAudRightVolume.restype = None
SetAudRightVolume.argtypes = [ctypes.c_double]
def DPxSetAudRightVolume(volume):
    """ Sets volume for the Right audio channels, range 0-1
    
    Args:
        volume (float): Value for the desired volume, between 0 and 1.
        
    :Low-level C definition:
        ``void DPxSetAudRightVolume(double volume)``
    """
    SetAudRightVolume(volume)



# void   DPxSetAudVolume(double volume)
# Set volume for both Left/Right audio channels, range 0-1
SetAudVolume = DPxDll['DPxSetAudVolume']
SetAudVolume.argtypes = [ctypes.c_double]
SetAudVolume.restype = None
def DPxSetAudVolume(volume):
    """ Sets the volume for both Left/Right audio channels, range 0-1
    
    Args:
        volume (float): Value for the desired volume, between 0 and 1.
        
    :Low-level C definition:
        ``void DPxSetAudVolume(double volume)``
    """
    SetAudVolume(volume)
    
    
# double    DPxGetAudLeftVolume()    
# Get volume for the Left audio output channel, range 0-1
GetAudLeftVolume = DPxDll['DPxGetAudLeftVolume']
GetAudLeftVolume.restype = ctypes.c_double
def DPxGetAudLeftVolume():
    """ Get volume for the Left audio output channel, range 0-1
    
    :Low-level C definition:
        ``double DPxGetAudLeftVolume()``
    """
    return GetAudLeftVolume()
  
  
#  double DPxGetAudRightVolume()
# Get volume for the Right audio output channel, range 0-1
GetAudRightVolume = DPxDll['DPxGetAudRightVolume']
GetAudRightVolume.restype = ctypes.c_double
def DPxGetAudRightVolume():
    """Get volume for the Right audio output channel, range 0-1
    
    :Low-level C definition:
        ``double DPxGetAudRightVolume()``
    """
    return GetAudRightVolume()


#  double DPxGetAudVolume()   
# Get volume for both Left/Right audio channels
# The floating point volume parameter is in the range 0-1.
# The actual Left/Right volume controls are implemented as 16-bit unsigned FPGA registers.
# The audio samples read from the RAM buffer are multiplied by the volume registers
# (then right-shifted 16 bits) before forwarding the samples to the CODEC.
# Volume value 1.0 is a special case which bypasses this multiplication.
# NOTE: For safety's sake, reset value of L/R volumes = 0, so must set volume before playback.
#GetAudVolume = DPxDll['DPxGetAudVolume']
def DPxGetAudVolume():
    """ Gets the volume for both Left/Right audio channels
    
    Returns:
        A tuple containing floats: [left Speaker Volume, Right speaker Volume]
        
    :Low-level C definition:
        ``double DPxGetAudVolume()``    
    """
    return (DPxGetAudLeftVolume(), DPxGetAudRightVolume())



# The audio output API has two groups of volume control functions.
# See the above paragraph for a description of the first group of volume control functions.
# This second group uses CODEC internal registers to independently attenuate L/R audio outputs to the DATAPixx speaker and Audio OUT ports.
# These CODEC volume registers have a precision (step size) of about 0.5 dB (see TI TLV320AIC32 datasheet for details).
# These routines can use either ratio units (0 to 1), or the corresponding dB values (-inf to 0).
# To minimize hiss, it is a good idea to do ball-park attenuation using these CODEC registers.
# Then, for ultra-precise stimulus volume manipulation, use the above SetAudVolume() functions.
# Those functions very precisely attenuate the digital audio data _before_ sending to the CODEC.
#
#  void DPxSetAudCodecOutLeftVolume(double volume, # int DBUnits)
# Set volume for the DATAPixx Audio OUT Left channel, range 0-1 (or dB)
# dBUnits is one of the following value:
#       0 : Set dBUnits in linear scale
#       1 : Set dBUnits in dB scale
SetAudCodecOutLeftVolume = DPxDll['DPxSetAudCodecOutLeftVolume']
SetAudCodecOutLeftVolume.argtypes = [ctypes.c_double, ctypes.c_int]
SetAudCodecOutLeftVolume.restype = None
def DPxSetAudCodecOutLeftVolume(volume, dBUnits=0):
    """Set volume for the DATAPixx Audio OUT Right channel
    
    Args:
        volume (float): The value for the desired volume, between 0 and 1 or in dB.
        dBUnits (int, optional): Set non-zero to return the gain in dB. Defaults to 0
        
    :Low-level C definition:
        ``void DPxSetAudCodecOutLeftVolume(double volume, int DBUnits)``
    """
    return SetAudCodecOutLeftVolume(volume, dBUnits)

# double DPxGetAudCodecOutLeftVolume( int DBUnits)
# Gets volume for the DATAPixx Audio OUT Left channel, range 0-1 (or dB)
GetAudCodecOutLeftVolume = DPxDll['DPxGetAudCodecOutLeftVolume']
GetAudCodecOutLeftVolume.restype = ctypes.c_double     
GetAudCodecOutLeftVolume.argtypes = [ctypes.c_int]
def DPxGetAudCodecOutLeftVolume(dBUnits=0):
    """Gets the volume for the DATAPixx Audio OUT Left channel
    
    Args:
        dBUnits (int, optional): Set non-zero to return the gain in dB. Defaults to 0
    
    :Low-level C definition:
        ``double DPxGetAudCodecOutLeftVolume(int DBUnits)``
    """
    return GetAudCodecOutLeftVolume(dBUnits)

#  void DPxSetAudCodecOutRightVolume(double volume, int DBUnits)
# Set volume for the DATAPixx Audio OUT Right channel, range 0-1 (or dB)
SetAudCodecOutRightVolume = DPxDll['DPxSetAudCodecOutRightVolume']
SetAudCodecOutRightVolume.argtypes = [ctypes.c_double, ctypes.c_int]
SetAudCodecOutRightVolume.restype = None
def DPxSetAudCodecOutRightVolume(volume, dBUnits=0):
    """Sets the volume for the DATAPixx Audio OUT Right channel
    
    Args:
        volume (float): The value for the desired volume, between 0 and 1 or in dB.
        dBUnits (int, optional): Set non-zero to return the gain in dB. Defaults to 0
    
    :Low-level C definition:
        ``void DPxSetAudCodecOutRightVolume(double volume, int DBUnits)``
    """
    return SetAudCodecOutRightVolume(volume, dBUnits)

#  double DPxGetAudCodecOutRightVolume(int DBUnits)
# Get volume for the DATAPixx Audio OUT Right channel, range 0-1 (or dB)
GetAudCodecOutRightVolume = DPxDll['DPxGetAudCodecOutRightVolume']
GetAudCodecOutRightVolume.restype = ctypes.c_double    
GetAudCodecOutRightVolume.argtypes = [ctypes.c_int]
def DPxGetAudCodecOutRightVolume(dBUnits=0):
    """Gets the volume for the DATAPixx Audio OUT Right channel
    
    Args:
        dBUnits (int, optional): Set non-zero to return the gain in dB. Defaults to 0
    
    :Low-level C definition:
        ``double DPxGetAudCodecOutRightVolume(int DBUnits)``
    """
    return GetAudCodecOutRightVolume(dBUnits)

#  void DPxSetAudCodecOutVolume(double volume, int DBUnits)    
# Set volume for the DATAPixx Audio OUT Left and Right channels, range 0-1 (or dB)
# dBUnits is one of the following value:
#       0 : Set dBUnits in linear scale
#       1 : Set dBUnits in dB scale
SetAudCodecOutVolume = DPxDll['DPxSetAudCodecOutVolume']
SetAudCodecOutVolume.argtypes = [ctypes.c_double, ctypes.c_int]
SetAudCodecOutVolume.restype = None
def DPxSetAudCodecOutVolume(volume, dBUnits=0):
    """Sets the volume for the DATAPixx Audio OUT Left and Right channels
    
    Args:
        volume (float): The value for the desired volume, between 0 and 1 or in dB.
        dBUnits (int, optional): Set non-zero to return the gain in dB. Defaults to 0
        
    :Low-level C definition:
        ``void DPxSetAudCodecOutVolume(double volume, int DBUnits)``
    """
    return SetAudCodecOutVolume(volume, dBUnits)

#  double DPxGetAudCodecOutVolume(int DBUnits)    
# Get volume for the DATAPixx Audio OUT Left and Right channels
def DPxGetAudCodecOutVolume(dBUnits=0):
    """ Gets the volume for the DATAPixx Audio OUT Left and Right channels
    
    Args:
        dBUnits (int, optional): Set non-zero to return the gain in dB. Defaults to 0
    
    Returns:
        A tuple containing floats: [left Speaker Volume, Right speaker Volume]
        
    :Low-level C definition:
        ``double DPxGetAudCodecOutVolume(int DBUnits)``    
    """
    return (DPxGetAudCodecOutLeftVolume(dBUnits), DPxGetAudCodecOutRightVolume(dBUnits))


#  void DPxSetAudCodecSpeakerLeftVolume(double volume, int DBUnits)    
# Set volume for the DATAPixx Speaker Left channel, range 0-1 (or dB)
SetAudCodecSpeakerLeftVolume = DPxDll['DPxSetAudCodecSpeakerLeftVolume']
SetAudCodecSpeakerLeftVolume.argtypes = [ctypes.c_double, ctypes.c_int]
SetAudCodecSpeakerLeftVolume.restype = None
def DPxSetAudCodecSpeakerLeftVolume(volume, dBUnits=0):
    """Sets volume for the DATAPixx Speaker LEft channels
    
    Args:
        volume (float): The value for the desired volume, between 0 and 1 or in dB.
        dBUnits (int, optional): Set non-zero to return the gain in dB. Defaults to 0.
        
    :Low-level C definition:
        ``void DPxSetAudCodecSpeakerLeftVolume(double volume, int DBUnits)``
    """
    return SetAudCodecSpeakerLeftVolume(volume, dBUnits)

#  double DPxGetAudCodecSpeakerLeftVolume(int DBUnits)
# Get volume for the DATAPixx Speaker Left channel, range 0-1 (or dB)
GetAudCodecSpeakerLeftVolume = DPxDll['DPxGetAudCodecSpeakerLeftVolume']
GetAudCodecSpeakerLeftVolume.restype = ctypes.c_double  
GetAudCodecSpeakerLeftVolume.argtypes = [ctypes.c_int]
def DPxGetAudCodecSpeakerLeftVolume(dBUnits=0):
    """Gets the volume for the DATAPixx Speaker Left channel
    
    Args:
        dBUnits (int, optional): Set non-zero to return the gain in dB. Defaults to 0
    
    :Low-level C definition:
        ``double DPxGetAudCodecSpeakerLeftVolume(int DBUnits)``
    """
    return GetAudCodecSpeakerLeftVolume(dBUnits)

#  void DPxSetAudCodecSpeakerRightVolume(double volume, int DBUnits)
# Set volume for the DATAPixx Speaker Right channel, range 0-1 (or dB)
# dBUnits is one of the following value:
#       0 : Set dBUnits in linear scale
#       1 : Set dBUnits in dB scale
SetAudCodecSpeakerRightVolume = DPxDll['DPxSetAudCodecSpeakerRightVolume'] 
SetAudCodecSpeakerRightVolume.argtypes = [ctypes.c_double, ctypes.c_int]
SetAudCodecSpeakerRightVolume.restype = None
def DPxSetAudCodecSpeakerRightVolume(volume, dBUnits=0):
    """Sets volume for the DATAPixx Speaker Right channels
    
    Args:
        volume (float): The value for the desired volume, between 0 and 1 or in dB.
        dBUnits (int, optional): Set non-zero to return the gain in dB. Defaults to 0
    
    :Low-level C definition:
        ``void DPxSetAudCodecSpeakerRightVolume(double volume, int DBUnits)``
    """
    return SetAudCodecSpeakerRightVolume(volume, dBUnits)

# double DPxGetAudCodecSpeakerRightVolume( int DBUnits)
# Get volume for the DATAPixx Speaker Right channel, range 0-1 (or dB)
GetAudCodecSpeakerRightVolume = DPxDll['DPxGetAudCodecSpeakerRightVolume']
GetAudCodecSpeakerRightVolume.restype = ctypes.c_double  
GetAudCodecSpeakerRightVolume.argtypes = [ctypes.c_int]
def DPxGetAudCodecSpeakerRightVolume(dBUnits=0):
    """Gets the volume for the DATAPixx Speaker Right channel
    
    Args:
        dBUnits (int, optional): Set non-zero to return the gain in dB. Defaults to 0.
    
    :Low-level C definition:
        ``double DPxGetAudCodecSpeakerRightVolume(int DBUnits)``
    """
    return GetAudCodecSpeakerRightVolume(dBUnits)

#  void DPxSetAudCodecSpeakerVolume(double volume, int DBUnits)    
# Set volume for the DATAPixx Speaker Left and Right channels, range 0-1 (or dB)
# dBUnits is one of the following value:
#       0 : Set dBUnits in linear scale
#       1 : Set dBUnits in dB scale
SetAudCodecSpeakerVolume = DPxDll['DPxSetAudCodecSpeakerVolume']
SetAudCodecSpeakerVolume.argtypes = [ctypes.c_double, ctypes.c_int]
SetAudCodecSpeakerVolume.restype = None
def DPxSetAudCodecSpeakerVolume(volume, dBUnits=0):
    """Sets volume for the DATAPixx Speaker Left and Right channels
    
    Args:
        volume (float): The value for the desired volume, between 0 and 1 or in dB.
        dBUnits (int, optional): Set non-zero to return the gain in dB. Defaults to 0.
    
    :Low-level C definition:
        ``void DPxSetAudCodecSpeakerVolume(double volume, int DBUnits)``
    """
    return SetAudCodecSpeakerVolume(volume, dBUnits)


#  double DPxGetAudCodecSpeakerVolume(int DBUnits)
# Get volume for the DATAPixx Speaker Left and Right channels 
def DPxGetAudCodecSpeakerVolume(dBUnits=0):
    """ Gets volume for the DATAPixx Speaker Left and Right channels
    
    Args:
        dBUnits (int, optional): Set non-zero to return the gain in dB. Defaults to 0.
        
    Returns:
        A tuple containing floats: [left Speaker Volume, Right speaker Volume]
        
    :Low-level C definition:
        ``double DPxGetAudCodecSpeakerVolume(int DBUnits)``  
    """ 
    return (DPxGetAudCodecSpeakerLeftVolume(dBUnits),DPxGetAudCodecSpeakerRightVolume(dBUnits))

 

setAudLRMode = DPxDll['DPxSetAudLRMode']
setAudLRMode.argtypes = [ctypes.c_int]
setAudLRMode.restype = None
def DPxSetAudLRMode(mode):
    """Sets how audio data are updated by schedules.

    Args:
        mode (str): Any of the following predefined constants.\n
            - **mono**: Left schedule data goes to left and right channels.
            - **left**: Each schedule data goes to left channel only.
            - **right**: Each schedule data goes to right channel only.
            - **stereo1**: Pairs of Left data are copied to left/right channels.
            - **stereo2**: Left data goes to left channel, Right data goes to right.
                    
    :Low-level C definition:
        ``void DPxSetAudLRMode(int lrMode)``
    
    """
    setAudLRMode(api_constants[mode.upper()])
        
        
  
getAudLRMode = DPxDll['DPxGetAudLRMode']
getAudLRMode.restype = ctypes.c_int 
def DPxGetAudLRMode():
    """Gets the audio schedule update mode.
    
    Returns:
        String: Any of the following predefined constants.\n
            - **mono**: Left schedule data goes to left and right channels.
            - **left**: Each schedule data goes to left channel only.
            - **right**: Each schedule data goes to right channel only.
            - **stereo1**: Pairs of Left data are copied to left/right channels.
            - **stereo2**: Left data goes to left channel, Right data goes to right.
                    
    :Low-level C definition:
        ``int DPxGetAudLRMode()``
    
    """  
    return audio_mode_constants[ getAudLRMode() ]
 



#  void DPxSetAudBuffBaseAddr(unsigned buffBaseAddr)
#  Set AUD RAM buffer start address.  Must be an even value.
SetAudBuffBaseAddr = DPxDll['DPxSetAudBuffBaseAddr']
SetAudBuffBaseAddr.argtypes = [ctypes.c_uint]
SetAudBuffBaseAddr.restype = None
def DPxSetAudBuffBaseAddr(buffBaseAddr):
    """Sets the AUD RAM buffer start address.
    
    Must be an even value.
    
    Args:
        buffBaseAddr (int): Base address.
    
    :Low-level C definition:
        ``void DPxSetAudBuffBaseAddr(unsigned buffBaseAddr)``
    """
    return SetAudBuffBaseAddr(buffBaseAddr)

#  unsigned DPxGetAudBuffBaseAddr()
#  Get AUD RAM buffer start address
GetAudBuffBaseAddr = DPxDll['DPxGetAudBuffBaseAddr']
GetAudBuffBaseAddr.restype = ctypes.c_uint
def DPxGetAudBuffBaseAddr():
    """Gets the AUD RAM buffer start address.
    
    Returns:
        int: Base address
    
    :Low-level C definition:
        ``unsigned DPxGetAudBuffBaseAddr()``
    """
    return GetAudBuffBaseAddr()


# void DPxSetAudBuffReadAddr(unsigned buffReadAddr)
#  Set RAM address from which next AUD datum will be read.  Must be an even value.
SetAudBuffReadAddr = DPxDll['DPxSetAudBuffReadAddr']
SetAudBuffReadAddr.argtypes = [ctypes.c_uint]
SetAudBuffReadAddr.restype = None
def DPxSetAudBuffReadAddr(buffReadAddr):
    """Sets RAM address from which next AUD datum will be read.
    
    Must be an even value.
    
    Args:
        buffReadAddr (int): Read address.
    
    :Low-level C definition:
        ``void DPxSetAudBuffReadAddr(unsigned buffReadAddr)``
    """
    return SetAudBuffReadAddr(buffReadAddr)

# unsigned DPxGetAudBuffReadAddr()
#  Get RAM address from which next AUD datum will be read
GetAudBuffReadAddr = DPxDll['DPxGetAudBuffReadAddr']
GetAudBuffReadAddr.restype = ctypes.c_uint
def DPxGetAudBuffReadAddr():
    """Gets AUD address from which next AUD datum will be read.
    
    Returns:
        int: Read address.
    
    :Low-level C definition:
        ``unsigned DPxGetAudBuffReadAddr()``
    """
    return GetAudBuffReadAddr()


# void DPxSetAudBuffSize(unsigned buffSize)
#  Set AUD RAM buffer size in bytes.  Must be an even value.  Buffer wraps to Base after Size.
SetAudBuffSize = DPxDll['DPxSetAudBuffSize']
SetAudBuffSize.argtypes = [ctypes.c_uint]
SetAudBuffSize.restype = None
def DPxSetAudBuffSize(buffSize):
    """Sets AUD RAM buffer size in bytes.
    
    Must be an even value. Buffer wraps to Base after Size.
    
    Args:
        buffSize (int): Buffer size.
        
    :Low-level C definition:
        ``void DPxSetAudBuffSize(unsigned buffSize)``
    """
    return SetAudBuffSize(buffSize)

# unsigned DPxGetAudBuffSize()
#  Get AUD RAM buffer size in bytes
GetAudBuffSize = DPxDll['DPxGetAudBuffSize']
GetAudBuffSize.restype = ctypes.c_uint  
def DPxGetAudBuffSize():
    """Gets the AUD RAM buffer size in bytes.
    
    Returns:
        int: buffer size.
    
    :Low-level C definition:
        ``unsigned DPxGetAudBuffSize()``
    """
    return GetAudBuffSize()


# void DPxSetAudBuff(unsigned buffAddr, unsigned buffSize)
#  Shortcut which assigns Size/BaseAddr/ReadAddr
SetAudBuff = DPxDll['DPxSetAudBuff']
SetAudBuff.argtypes = [ctypes.c_uint, ctypes.c_uint]
SetAudBuff.restype = None
def DPxSetAudBuff(buffAddr, buffSize):
    """Sets base address, reads address and buffer size for AUD schedules.
    
    This function is a shortcut which assigns Size/BaseAddr/ReadAddr
    
    Args:
        buffAddr (int): Base address.
        buffSize (int): Buffer size.
    
    :Low-level C definition:
        ``void DPxSetAudBuff(unsigned buffAddr, unsigned buffSize)``
    """
    return SetAudBuff(buffAddr, buffSize)

# void DPxSetAuxBuffBaseAddr(unsigned buffBaseAddr)
#  Set AUX RAM buffer start address.  Must be an even value.
SetAuxBuffBaseAddr = DPxDll['DPxSetAuxBuffBaseAddr']
SetAuxBuffBaseAddr.argtypes = [ctypes.c_uint]
SetAuxBuffBaseAddr.restype = None
def DPxSetAuxBuffBaseAddr(buffBaseAddr):
    """Sets the AUX RAM buffer start address.
    
    Must be an even value.
    
    Args:
        buffBaseAddr (int): Base address.
    
    :Low-level C definition:
        ``void DPxSetAuxBuffBaseAddr(unsigned buffBaseAddr)``
    """
    return SetAuxBuffBaseAddr(buffBaseAddr)

# unsigned DPxGetAuxBuffBaseAddr()
#  Get AUX RAM buffer start address
GetAuxBuffBaseAddr = DPxDll['DPxGetAuxBuffBaseAddr']
GetAuxBuffBaseAddr.restype = ctypes.c_uint 
def DPxGetAuxBuffBaseAddr():
    """Gets the AUX RAM buffer start address.
    
    Returns:
        int: Base address.
    
    :Low-level C definition:
        ``unsigned DPxGetAuxBuffBaseAddr()``
    """
    return GetAuxBuffBaseAddr()

# void DPxSetAuxBuffReadAddr(unsigned buffReadAddr)
#  Set RAM address from which next AUX datum will be read.  Must be an even value.
SetAuxBuffReadAddr = DPxDll['DPxSetAuxBuffReadAddr']
SetAuxBuffReadAddr.argtypes = [ctypes.c_uint]
SetAuxBuffReadAddr.restype = None
def DPxSetAuxBuffReadAddr(buffReadAddr):
    """Sets RAM address from which next AUX datum will be read.
    
    Must be an even value.
    
    Args:
        buffReadAddr (int): Read address.
    
    :Low-level C definition:
        ``void DPxSetAuxBuffReadAddr(unsigned buffReadAddr)``
    """
    return SetAuxBuffReadAddr(buffReadAddr)


# unsigned DPxGetAuxBuffReadAddr()
#  Get RAM address from which next AUX datum will be read
GetAuxBuffReadAddr = DPxDll['DPxGetAuxBuffReadAddr']
GetAuxBuffReadAddr.restype = ctypes.c_uint 
def DPxGetAuxBuffReadAddr():
    """Gets RAM address from which next AUX datum will be read.
    
    Returns:
        int: Read address.
    
    :Low-level C definition:
        ``unsigned DPxGetAuxBuffReadAddr()``
    """
    return GetAuxBuffReadAddr()


# void DPxSetAuxBuffSize(unsigned buffSize)
#  Set AUX RAM buffer size in bytes.  Must be an even value.  Buffer wraps to Base after Size.
SetAuxBuffSize = DPxDll['DPxSetAuxBuffSize']
SetAuxBuffSize.argtypes = [ctypes.c_uint]
SetAuxBuffSize.restype = None
def DPxSetAuxBuffSize(buffSize):
    """Sets AUX RAM buffer size in bytes.
    
    Must be an even value. Buffer wraps to Base after Size.
    
    Args:
        buffSize (int): Buffer size.
    
    :Low-level C definition:
        ``void DPxSetAuxBuffSize(unsigned buffSize)``
    """
    return SetAuxBuffSize(buffSize)

# unsigned DPxGetAuxBuffSize()
#  Get AUX RAM buffer size in bytes
GetAuxBuffSize = DPxDll['DPxGetAuxBuffSize']
GetAuxBuffSize.restype = ctypes.c_uint 
def DPxGetAuxBuffSize():
    """Gets the AUX RAM buffer size in bytes.
    
    Returns:
        int: buffer size.
    
    :Low-level C definition:
        ``unsigned DPxGetAuxBuffSize()``
    """
    return GetAuxBuffSize()

# void DPxSetAuxBuff(unsigned buffAddr, unsigned buffSize)
#  Shortcut which assigns Size/BaseAddr/ReadAddr
SetAuxBuff = DPxDll['DPxSetAuxBuff'] 
SetAuxBuff.argtypes = [ctypes.c_uint, ctypes.c_uint]
SetAuxBuff.restype = None
def DPxSetAuxBuff(buffAddr, buffSize):
    """Sets base address, reads address and buffer size for AUX schedules.
    
    This function is a shortcut which assigns Size/BaseAddr/ReadAddr
    
    Args:
        buffAddr (int): Base address.
        buffSize (int): Buffer size.
    
    
    :Low-level C definition:
        ``void DPxSetAuxBuff(unsigned buffAddr, unsigned buffSize)``
    """
    return SetAuxBuff(buffAddr, buffSize)

# void DPxSetAudSchedOnset(unsigned onset)
#  Set nanosecond delay between schedule start and first AUD update
SetAudSchedOnset = DPxDll['DPxSetAudSchedOnset']
SetAudSchedOnset.argtypes = [ctypes.c_uint]
SetAudSchedOnset.restype = None
def DPxSetAudSchedOnset(onset):
    """Sets nanosecond delay between schedule start and first MIC update.
    
    Args:
        onset (int): The onset value.
    
    :Low-level C definition:
        ``void DPxSetAudSchedOnset(unsigned onset)``
    """
    return SetAudSchedOnset(onset)

# unsigned DPxGetAudSchedOnset()
#  Get nanosecond delay between schedule start and first AUD update
GetAudSchedOnset = DPxDll['DPxGetAudSchedOnset']
GetAudSchedOnset.restype = ctypes.c_uint 
def DPxGetAudSchedOnset():
    """Gets the nanosecond delay between schedule start and first AUD update.
    
    Returns:
        int: The nanosecond onset between the first update and the start of schedule.
    
    :Low-level C definition:
        ``unsigned DPxGetAudSchedOnset()``
    """
    return GetAudSchedOnset()


setAudSchedRate = DPxDll['DPxSetAudSchedRate']
setAudSchedRate.argtypes = [ctypes.c_uint, ctypes.c_int]
setAudSchedRate.restype = None
def DPxSetAudSchedRate(rate, unit):
    """Sets the schedule rate.
    
    This method allows the user to set the schedule rate. Since the rate can be given 
    with different units, the method also needs to have a unit associated with the rate.
    
    
    If no delay is required, this method does not need to be used. Default value is 0.

    Args:
        rate (int): Any positive value equal to or greater than zero.
        unit (str): Any of the following predefined constants.\n
        - **hz**: rate updates per second, maximum 96 kHz.
        - **video**: rate updates per video frame, maximum 96 kHz.
        - **nano**: rate updates period in nanoseconds, minimum 10417 ns.
    
    :Low-level C definition:
        ``void DPxSetAudSchedRate(unsigned rateValue, int rateUnits)``

    """
    setAudSchedRate(rate, api_constants[unit.upper()])



getAudSchedRate = DPxDll['DPxGetAudSchedRate']
getAudSchedRate.restype = ctypes.c_uint
def DPxGetAudSchedRate():
    """Gets the audio schedule update rate and optionally get rate units.
    
    This method allows the user to get the audio's left schedule update rate and optionally get rate units.
    The return value is a tuple containing the rate and the rate unit.
    
    The unit can be any of the following predefined constants.\n
        - **hz**: Updates per second, maximum 96 kHz.
        - **video**: Updates per video frame, maximum 96 kHz.
        - **nano**: Update period in nanoseconds, minimum 10417 ns.
    
    Returns:
        Tuple: Rate, Unit
            
                    
    :Low-level C definition:
        ``unsigned DPxGetAudSchedRate(int *rateUnits)``
    
    """
    temp = 0
    p_temp = ctypes.c_int(temp)
    return (getAudSchedRate(ctypes.byref(p_temp)), rate_constants[ p_temp.value ])



# void DPxSetAudSchedCount(unsigned count)
#  Set AUD schedule update count
SetAudSchedCount = DPxDll['DPxSetAudSchedCount']
SetAudSchedCount.argtypes = [ctypes.c_uint]
SetAudSchedCount.restype = None
def DPxSetAudSchedCount(count):
    """Sets MIC schedule update count.
    
    Args:
        count (int): Schedule count.
    
    :Low-level C definition:
        ``void DPxSetAudSchedCount(unsigned count)``
    """
    return SetAudSchedCount(count)

# unsigned DPxGetAudSchedCount()
#  Get AUD schedule update count
GetAudSchedCount = DPxDll['DPxGetAudSchedCount']
GetAudSchedCount.restype = ctypes.c_uint 
def DPxGetAudSchedCount():
    """Gets AUD schedule update count.
    
    Returns:
        int: The current MIC schedule count.
    
    :Low-level C definition:
        ``unsigned DPxGetAudSchedCount()``
    """
    return GetAudSchedCount()


# void DPxEnableAudSchedCountdown()
#  SchedCount decrements at SchedRate, and schedule stops automatically when count hits 0
EnableAudSchedCountdown = DPxDll['DPxEnableAudSchedCountdown']
EnableAudSchedCountdown.restype = None
def DPxEnableAudSchedCountdown():
    """Enables MIC schedule count down.
    
    SchedCount increments at SchedRate, and schedule is stopped by calling SchedStop.
    
    :Low-level C definition:
        ``void DPxEnableAudSchedCountdown()``
    """
    return EnableAudSchedCountdown()


# void DPxDisableAudSchedCountdown()
#  SchedCount increments at SchedRate, and schedule is stopped by calling SchedStop
DisableAudSchedCountdown = DPxDll['DPxDisableAudSchedCountdown']
DisableAudSchedCountdown.restype = None
def DPxDisableAudSchedCountdown():
    """Disables AUD schedule count down.
    
    SchedCount increments at SchedRate, and schedule is stopped by calling SchedStop.
    
    :Low-level C definition:
        ``void DPxDisableAudSchedCountdown()``
    """
    return DisableAudSchedCountdown()


# int DPxIsAudSchedCountdown()
#  Returns Non-zero if SchedCount decrements to 0 and automatically stops schedule
IsAudSchedCountdown = DPxDll['DPxIsAudSchedCountdown']
IsAudSchedCountdown.restype = ctypes.c_int  
def DPxIsAudSchedCountdown():
    """Returns non-zero if SchedCount decrements to 0 and automatically stops schedule.
    
    :Low-level C definition:
        ``int DPxIsAudSchedCountdown()``
    """
    return IsAudSchedCountdown()


# void DPxSetAudSched(unsigned onset, unsigned rateValue, int rateUnits, unsigned count)
#  Shortcut which assigns Onset/Rate/Count. If Count > 0, enables Countdown mode.
SetAudSched = DPxDll['DPxSetAudSched']
SetAudSched.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint]
SetAudSched.restype = None
def DPxSetAudSched(onset, rateValue, rateUnits, count):
    """Sets AUD schedule onset, count and rate.
    
    This function is a shortcut which assigns Onset/Rate/Count. If ``count`` is greater than zero, the count
    down mode is enabled.
    
    Args:
        onset (int): Schedule onset.
        rateValue (int): Rate value.
        rateUnits (str): Usually ``hz``. Can also be ``video`` to update every ``rateValue`` video frames or ``nano`` to update every ``rateValue`` nanoseconds.
        count (int): Schedule count.

    :Low-level C definition:
        ``void DPxSetAudSched(unsigned onset, unsigned rateValue, int rateUnits, unsigned count)``
    """
    return SetAudSched(onset, rateValue, api_constants[rateUnits.upper()], count)


# void DPxStartAudSched()
#  Start running a AUD schedule
StartAudSched = DPxDll['DPxStartAudSched']
StartAudSched.restype = None
def DPxStartAudSched():
    """Starts running an AUD schedule
    
    :Low-level C definition:
        ``void DPxStartAudSched()``
    """
    return StartAudSched()


# void DPxStopAudSched()
#  Stop running a AUD schedule
StopAudSched = DPxDll['DPxStopAudSched']
StopAudSched.restype = None
def DPxStopAudSched():
    """Stops running an AUD schedule
    
    :Low-level C definition:
        ``void DPxStopAudSched()``
    """
    return StopAudSched()


# int DPxIsAudSchedRunning()
#  Returns non-0 if AUD schedule is currently running
IsAudSchedRunning = DPxDll['DPxIsAudSchedRunning']
IsAudSchedRunning.restype = ctypes.c_int    
def DPxIsAudSchedRunning():
    """Returns non-zero if AUD schedule is currently running.
    
    :Low-level C definition:
        ``int DPxIsAudSchedRunning()``
    """
    return IsAudSchedRunning()


# void DPxSetAuxSchedOnset(unsigned onset)
#  Set nanosecond delay between schedule start and first AUX update
SetAuxSchedOnset = DPxDll['DPxSetAuxSchedOnset']
SetAuxSchedOnset.argtypes = [ctypes.c_uint]
SetAuxSchedOnset.restype = None
def DPxSetAuxSchedOnset(onset):
    """Sets nanosecond delay between schedule start and first AUX update.
    
    Args:
        onset (int): The nanosecond onset between the first update and the start of schedule.
    
    :Low-level C definition:
        ``void DPxSetAuxSchedOnset(unsigned onset)``
    """
    return SetAuxSchedOnset(onset)

# unsigned DPxGetAuxSchedOnset()
#  Get nanosecond delay between schedule start and first AUX update
GetAuxSchedOnset = DPxDll['DPxGetAuxSchedOnset']
GetAuxSchedOnset.restype = ctypes.c_uint 
def DPxGetAuxSchedOnset():
    """Gets the nanosecond delay between schedule start and the first AUX update.
    
    Returns:
        int: The nanosecond onset between the first update and the start of the schedule.
    
    :Low-level C definition:
        ``unsigned DPxGetAuxSchedOnset()``
    """
    return GetAuxSchedOnset()
    
setAuxSchedRate = DPxDll['DPxSetAuxSchedRate'] 
setAuxSchedRate.argtypes = [ctypes.c_uint, ctypes.c_int]
setAuxSchedRate.restype = None
def DPxSetAuxSchedRate(rate, unit):
    """Sets the schedule rate.
    
    This method allows the user to set the schedule rate. Since the rate can be given 
    with different units, the method also needs to have a unit associated with the rate.
    
    
    If no delay is required, this method does not need to be used. Default value is 0.

    Args:
        rate (int): Any positive value equal to or greater than zero.
        unit (str): Any of the following predefined constants.\n
                - **hz**: rate updates per second, maximum 96 kHz.
                - **video**: rate updates per video frame, maximum 96 kHz.
                - **nano**: rate updates period in nanoseconds, minimum 10417 ns.
    
    :Low-level C definition:
        ``void DPxSetAuxSchedRate(unsigned rateValue, int rateUnits)``

    """
    setAuxSchedRate(rate, api_constants[unit.upper()])


# unsigned DPxGetAuxSchedRate(int *rateUnits)
#  Get AUX schedule update rate (and optionally get rate units)
GetAuxSchedRate = DPxDll['DPxGetAuxSchedRate']
def DPxGetAuxSchedRate():
    """Gets AUX schedule update rate and the rate units.
    
    Returns:
        tuple: rate and unit.
        
    :Low-level C definition:
        ``unsigned DPxGetAuxSchedRate(int *rateUnits))``
    """
    Var = 0
    p_Var = ctypes.c_int(Var)
    GetAuxSchedRate.restype = ctypes.c_uint
    return (GetAuxSchedRate(ctypes.byref(p_Var)), rate_constants[p_Var.value])
    


# void DPxSetAuxSchedCount(unsigned count)
#  Set AUX schedule update count
SetAuxSchedCount = DPxDll['DPxSetAuxSchedCount']
SetAuxSchedCount.argtypes = [ctypes.c_uint]
SetAuxSchedCount.restype = None
def DPxSetAuxSchedCount(count):
    """Sets the AUX schedule update count
    
    Args:
        count (int): Schedule count.
        
    :Low-level C definition:
        ``void DPxSetAuxSchedCount(unsigned count)``
    """
    return SetAuxSchedCount(count)


# unsigned DPxGetAuxSchedCount()
#  Get AUX schedule update count
GetAuxSchedCount = DPxDll['DPxGetAuxSchedCount']
GetAuxSchedCount.restype = ctypes.c_uint
def DPxGetAuxSchedCount():
    """Gets AUX schedule update count.
    
    Returns:
        int: The schdule update total count.
    
    :Low-level C definition:
        ``unsigned DPxGetAuxSchedCount()``
    """
    return GetAuxSchedCount()

# void DPxEnableAuxSchedCountdown()
#  SchedCount decrements at SchedRate, and schedule stops automatically when count hits 0
EnableAuxSchedCountdown = DPxDll['DPxEnableAuxSchedCountdown']
EnableAuxSchedCountdown.restype = None
def DPxEnableAuxSchedCountdown():
    """Enables the AUX Schedule count down.
    
    SchedCount increments at SchedRate, and schedule is stopped by calling Sched
    
    :Low-level C definition:
        ``void DPxEnableAuxSchedCountdown()``
    """
    return EnableAuxSchedCountdown()


# void DPxDisableAuxSchedCountdown()
#  SchedCount increments at SchedRate, and schedule is stopped by calling SchedStop
DisableAuxSchedCountdown = DPxDll['DPxDisableAuxSchedCountdown']
DisableAuxSchedCountdown.restype = None
def DPxDisableAuxSchedCountdown():
    """Disables the AUX Schedule Countdown
    
    SchedCount increments at SchedRate, and schedule is stopped by calling Sched
    
    :Low-level C definition:
        ``void DPxDisableAuxSchedCountdown()``
    """
    return DisableAuxSchedCountdown()


# int DPxIsAuxSchedCountdown()
#  Returns non-0 if SchedCount decrements to 0 and automatically stops schedule
IsAuxSchedCountdown = DPxDll['DPxIsAuxSchedCountdown']
IsAuxSchedCountdown.restype = ctypes.c_int  
def DPxIsAuxSchedCountdown():
    """Returns non-zero if SchedCount decrements to 0 and automatically stops the schedule.
    
    :Low-level C definition:
        ``int DPxIsAuxSchedCountdown()``
    """
    return IsAuxSchedCountdown()


# void DPxSetAuxSched(unsigned onset, unsigned rateValue, int rateUnits, unsigned count)
#  Shortcut which assigns Onset/Rate/Count. If Count > 0, enables Countdown mode.
SetAuxSched= DPxDll['DPxSetAuxSched']
SetAuxSched.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint]
SetAuxSched.restype = None
def DPxSetAuxSched(onset, rateValue, rateUnits, count):
    """Sets AUX schedule onset, count and rate.
    
    This function is a shortcut which assigns Onset/Rate/Count. If ``count`` is greater than zero, the count
    down mode is enabled.
    
    Args:
        onset (int): Schedule onset.
        rateValue (int): Rate value.
        rateUnits (str): Usually ``hz``. Can also be ``video`` to update every ``rateValue`` video frames or ``nano`` to update every ``rateValue`` nanoseconds.
        count (int): Schedule count.
        
    :Low-level C definition:
        ``void DPxSetAuxSched(unsigned onset, unsigned rateValue, int rateUnits, unsigned count)``
    """
    SetAuxSched(onset, rateValue, api_constants[rateUnits.upper()], count)



# void DPxStartAuxSched()
#  Start running a AUX schedule
StartAuxSched = DPxDll['DPxStartAuxSched']
StartAuxSched.restype = None
def DPxStartAuxSched():
    """Starts running an AUX schedule.
    
    :Low-level C definition:
        ``void DPxStartAuxSched()``
    """
    return StartAuxSched()


# void DPxStopAuxSched()
#  Stop running a AUX schedule
StopAuxSched = DPxDll['DPxStopAuxSched']
StopAuxSched.restype = None
def DPxStopAuxSched():
    """Stops running an AUX schedule.
    
    :Low-level C definition:
        ``void DPxStopAuxSched()``
    """
    return StopAuxSched()


# int DPxIsAuxSchedRunning()
# Returns non-0 if AUX schedule is currently running
IsAuxSchedRunning = DPxDll['DPxIsAuxSchedRunning']
IsAuxSchedRunning.restype = ctypes.c_int   
def DPxIsAuxSchedRunning():
    """Returns non-zero if an AUX schedule is currently running.
    
    :Low-level C definition:
        ``int DPxIsAuxSchedRunning()``
    """
    return IsAuxSchedRunning()

                                  
GetAudGroupDelay = DPxDll['DPxGetAudGroupDelay']
GetAudGroupDelay.restype = ctypes.c_double 
GetAudGroupDelay.argtypes = [ctypes.c_double]
def DPxGetAudGroupDelay(sampleRate):
    """Gets the CODEC Audio OUT group delay in seconds.
    
    Args:
        sampleRate (float): The rate at which your schedule is running. 
    
    Returns:
        float: delay in seconds.
        
    :Low-level C definition:
        ``double DPxGetAudGroupDelay(double sampleRate)``
    
    """

    return GetAudGroupDelay(sampleRate)
    
    
    
# void    DPxSetMicSource(int source, double gain, int dBUnits)
# Select the source of the microphone input. Typical gain values would be around 100 for a
# microphone input, and probably 1 for line-level input.
#
# Return value:
#   N/A
# Arguments:
#   source is one of the following predefined constants:
#            DPX_MIC_SRC_MIC_IN    : Microphone level input
#            DPX_MIC_SRC_LINE_IN    : Line level audio input.
#   gain can take the following values:
#           linear scale : min = 1, max = 1000
#           dB scale     : min = 0, max = 60 dB
#   dBUnits is one of the following value:
#           0 : Set dBUnits in linear scale
#           1 : Set dBUnits in dB scale
SetMicSource = DPxDll['DPxSetMicSource']
SetMicSource.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_int]
SetMicSource.restype = None
def DPxSetMicSource(source, gain, dBUnits=0):
    """Sets the source for the microphone.
    
    Selects the source of the microphone input. Typical gain values would be around 100 for a
    microphone input, and around 1 for line-level input.
    
    Args:
        source (str): One of the following: \n
                - ``MIC``: Microphone level input
                - ``LINE``: Line level audio input.
        gain (int): The gain can take the following values depnding on the scale: \n
                - linear scale : [1, 1000]
                - dB scale     : [0, 60] dB
        dBUnits (int, optional): Set non-zero to return the gain in dB. Defaults to 0.
        
    :Low-level C definition:
        ``void DPxSetMicSource(int source, double gain, int dBUnits)``
    """
    return SetMicSource(api_constants[source.upper()], gain, dBUnits)

# int DPxGetMicSource(int DBUnits)
# Get the source and the gain of the microphone input
GetMicSource = DPxDll['DPxGetMicSource']    
GetMicSource.restype = ctypes.c_int
def DPxGetMicSource(dBUnits=0):
    """Gets the source and the gain of the microphone input.
    
    Args:
        dBUnits (int, optional): Set to non-zero to return the gain in dB. Defaults to 0.
    
    Returns:
        A list containing the [gain value, microphone source]
         
    :Low-level C definition:
        ``int DPxGetMicSource(int DBUnits)``
    """
    gain = 0
    p_gain = ctypes.c_double(gain)
    dbUnit = GetMicSource(ctypes.byref(p_gain), dBUnits)
    return [p_gain.value, dbUnit]


# int DPxGetMicLeftValue()
# Get the 16-bit 2's complement signed value for left MIC channel
GetMicLeftValue = DPxDll['DPxGetMicLeftValue'] 
GetMicLeftValue.restype = ctypes.c_int
def DPxGetMicLeftValue():
    """Get the 16-bit 2's complement signed value for left MIC channel
    
    :Low-level C definition:
        ``int DPxGetMicLeftValue()``
    """
    return GetMicLeftValue()


# int DPxGetMicRightValue()
# Get the 16-bit 2's complement signed value for right MIC channel
GetMicRightValue = DPxDll['DPxGetMicRightValue']
GetMicRightValue.restype = ctypes.c_int 
def DPxGetMicRightValue():
    """Get the 16-bit 2's complement signed value for right MIC channel
    
    :Low-level C definition:
        ``int DPxGetMicRightValue()``
    """
    return GetMicRightValue()


setMicLRMode = DPxDll['DPxSetMicLRMode']
setMicLRMode.restype = ctypes.c_int
setMicLRMode.restype = None
def DPxSetMicLRMode(mode):
    """Sets the schedule buffer storing mode.
    
    This method allows the user to configure how the microphone left and right channels are stored to the schedule buffer.
    
    Args:
        mode (str) : Any of the following predefined constants.\n
            - **mono**: Mono data is written to the schedule buffer. The average of Left/Right CODEC data.
            - **left**: Left data is written to the schedule buffer.
            - **right**: Right data is written to the schedule buffer.
            - **stereo**: Left and Right data are both written to the schedule buffer.
                    
    :Low-level C definition:
        ``void DPxSetMicLRMode(int lrMode)``
    
    """
    setMicLRMode(api_constants[mode.upper()])   
 
 
 
getMicLRMode = DPxDll['DPxGetMicLRMode']
getMicLRMode.restype = ctypes.c_int
def DPxGetMicLRMode():
    """Gets the microphone Left/Right configuration mode.
    
    This method allows the user to get the microphone left and right channels schedule buffer mode.
    
    Returns:
        String: Any of the following predefined constants.\n
            - **mono**: Mono data is written to the schedule buffer. The average of the Left/Right CODEC data.
            - **left**: Left data is written to the schedule buffer.
            - **right**: Right data is written to the schedule buffer.
            - **stereo**: Left and Right data are both written to the schedule buffer.
                    
    :Low-level C definition:
        ``int DPxGetMicLRMode()``
    """
    return mic_mode_constants[ getMicLRMode()]


# void DPxEnableAudMicLoopback()
# Enable loopback between audio outputs and microphone inputs
EnableAudMicLoopback = DPxDll['DPxEnableAudMicLoopback']
EnableAudMicLoopback.restype = None
def DPxEnableAudMicLoopback():
    """Enables loopback between audio outputs and microphone inputs
    
    :Low-level C definition:
        ``void DPxEnableAudMicLoopback()``
    """
    return EnableAudMicLoopback()


# void DPxDisableAudMicLoopback()
# Disable loopback between audio outputs and microphone inputs
DisableAudMicLoopback = DPxDll['DPxDisableAudMicLoopback']
DisableAudMicLoopback.restype = None
def DPxDisableAudMicLoopback():
    """Disables loopback between audio outputs and microphone inputs
    
    :Low-level C definition:
        ``void DPxDisableAudMicLoopback()``
    """
    return DisableAudMicLoopback()


# int DPxIsAudMicLoopback()
# Returns non-0 if microphone inputs are driven by audio outputs
IsAudMicLoopback = DPxDll['DPxIsAudMicLoopback']
IsAudMicLoopback.restype = ctypes.c_int
def DPxIsAudMicLoopback():
    """Returns non-zero if microphone inputs are driven by audio outputs.
    
    :Low-level C definition:
        ``int DPxIsAudMicLoopback()``
    """
    return IsAudMicLoopback()


# void DPxSetMicBuffBaseAddr(unsigned buffBaseAddr)
# Set MIC RAM buffer start address.  Must be an even value.
SetMicBuffBaseAddr  = DPxDll['DPxSetMicBuffBaseAddr']
SetMicBuffBaseAddr.argtypes = [ctypes.c_uint]
SetMicBuffBaseAddr.restype = None
def DPxSetMicBuffBaseAddr(buffBaseAddr):
    """Sets the MIC RAM buffer start address.
    
    Must be an even value.
    
    Args:
        buffBaseAddr (int): Base address.
    
    :Low-level C definition:
        ``void DPxSetMicBuffBaseAddr(unsigned buffBaseAddr)``
    """
    return SetMicBuffBaseAddr(buffBaseAddr)


# unsigned DPxGetMicBuffBaseAddr()
# Get MIC RAM buffer start address
GetMicBuffBaseAddr = DPxDll['DPxGetMicBuffBaseAddr']                                           
GetMicBuffBaseAddr.restype = ctypes.c_uint
def DPxGetMicBuffBaseAddr():
    """Gets the MIC RAM buffer start address.
    
    Returns:
        int: Base address.
    
    :Low-level C definition:
        ``unsigned DPxGetMicBuffBaseAddr()``
    """
    return GetMicBuffBaseAddr()


# void DPxSetMicBuffWriteAddr(unsigned buffWriteAddr)
# Set RAM address to which next MIC datum will be written.  Must be an even value.
SetMicBuffWriteAddr = DPxDll['DPxSetMicBuffWriteAddr'] 
SetMicBuffWriteAddr.argtypes = [ctypes.c_uint]
SetMicBuffWriteAddr.restype = None
def DPxSetMicBuffWriteAddr(buffWriteAddr):
    """Sets RAM address from which next MIC datum will be written.
    
    Must be an even value.
    
    :Low-level C definition:
        ``void DPxSetMicBuffWriteAddr(unsigned buffWriteAddr)``
    """
    return SetMicBuffWriteAddr(buffWriteAddr)


#  double DPxGetMicGroupDelay(double sampleRate)
# Returns CODEC MIC IN group delay in seconds
GetMicGroupDelay = DPxDll['DPxGetMicGroupDelay']
GetMicGroupDelay.restype = ctypes.c_double
GetMicGroupDelay.argtypes = [ctypes.c_double]
def DPxGetMicGroupDelay(sampleRate):
    """Gets the CODEC Audio OUT group delay in seconds.
    
    Args:
        sampleRate (float): The sample rate of your schedule
    Returns:
        float: delay in seconds.
    
    :Low-level C definition:
        ``double DPxGetMicGroupDelay(double sampleRate)``
    """
    return GetMicGroupDelay(sampleRate)

# unsigned    DPxGetMicBuffWriteAddr()
# Get RAM address to which next MIC datum will be written
GetMicBuffWriteAddr = DPxDll['DPxGetMicBuffWriteAddr']                                              
GetMicBuffWriteAddr.restype = ctypes.c_uint
def DPxGetMicBuffWriteAddr():
    """Gets RAM address from which next MIC datum will be written.
    
    Returns:
        int: Write address.
    
    :Low-level C definition:
        ``unsigned DPxGetMicBuffWriteAddr()``
    """
    return GetMicBuffWriteAddr()


# unsigned    DPxGetMicBuffSize()
# Get MIC RAM buffer size in bytes
GetMicBuffSize = DPxDll['DPxGetMicBuffSize']                                      
GetMicBuffSize.restype = ctypes.c_uint
def DPxGetMicBuffSize():
    """Gets the DAC RAM buffer size in bytes.
    
    Returns:
        int: buffer size.
    
    :Low-level C definition:
        ``unsigned DPxGetMicBuffSize()``
    """
    return GetMicBuffSize()


# unsigned    DPxGetMicSchedOnset()
# Get nanosecond delay between schedule start and first MIC sample
GetMicSchedOnset = DPxDll['DPxGetMicSchedOnset']                            
GetMicSchedOnset.restype = ctypes.c_uint
def DPxGetMicSchedOnset():
    """Gets the nanosecond delay between schedule start and first MIC update.
    
    Returns:
        int: The nanosecond onset between the first update and the start of schedule.
    
    :Low-level C definition:
        ``unsigned DPxGetMicSchedOnset()``
    """
    return GetMicSchedOnset()


# unsigned    DPxGetMicSchedRate(int *rateUnits)
# Get MIC schedule sample rate (and optionally get rate units)
GetMicSchedRate = DPxDll['DPxGetMicSchedRate']
GetMicSchedRate.restype = ctypes.c_uint
def DPxGetMicSchedRate():
    """Gets MIC schedule update rate and the rate units.
    
    Returns:
        tuple: rate and unit.
        
    :Low-level C definition:
        ``unsigned DPxGetDacSchedRate(int *rateUnits)``
    """
    Var = 0
    p_Var = ctypes.c_int(Var)
    return (int(GetMicSchedRate(ctypes.byref(p_Var))), rate_constants[p_Var.value])



# unsigned    DPxGetMicSchedCount()
# Get MIC schedule sample count
GetMicSchedCount = DPxDll['DPxGetMicSchedCount']                              
GetMicSchedCount.restype = ctypes.c_uint
def DPxGetMicSchedCount():
    """Gets MIC schedule update count.
    
    Returns:
        int: The current MIC schedule count.
    
    :Low-level C definition:
        ``unsigned DPxGetMicSchedCount()``
    """
    return GetMicSchedCount()


# void    DPxSetMicBuffSize(unsigned buffSize)
# Set MIC RAM buffer size in bytes.  Must be an even value.  Buffer wraps after Size.
SetMicBuffSize = DPxDll['DPxSetMicBuffSize']
SetMicBuffSize.argtypes = [ctypes.c_uint]
SetMicBuffSize.restype = None
def DPxSetMicBuffSize(buffSize):
    """Sets MIC RAM buffer size in bytes.
    
    Must be an even value. Buffer wraps to Base after Size.
    
    Args:
        buffSize (int): Buffer size.
        
    :Low-level C definition:
        ``void DPxSetMicBuffSize(unsigned buffSize)``
    """
    return SetMicBuffSize(buffSize)


# void    DPxSetMicBuff(unsigned buffAddr, unsigned buffSize)
# Shortcut which assigns Size/BaseAddr/ReadAddr
SetMicBuff = DPxDll['DPxSetMicBuff']
SetMicBuff.argtypes = [ctypes.c_uint, ctypes.c_uint]
SetMicBuff.restype = None
def DPxSetMicBuff(buffAddr, buffSize):
    """Sets base address, reads address and buffer size for MIC schedules.
    
    This function is a shortcut which assigns Size/BaseAddr/ReadAddr.
    
    Args:
        buffAddr (int): Base address.
        buffSize (int): Buffer size.
    
    :Low-level C definition:
        ``void DPxSetMicBuff(unsigned buffAddr, unsigned buffSize)``
    """
    return SetMicBuff(buffAddr, buffSize)


# void    DPxSetMicSchedOnset(unsigned onset)
# Set nanosecond delay between schedule start and first MIC sample
SetMicSchedOnset = DPxDll['DPxSetMicSchedOnset']
SetMicSchedOnset.argtypes = [ctypes.c_uint]
SetMicSchedOnset.restype = None
def DPxSetMicSchedOnset(onset):
    """Sets nanosecond delay between schedule start and first MIC update.
    
    Args:
        onset (int): The onset value.
    
    :Low-level C definition:
        ``void DPxSetMicSchedOnset(unsigned onset)``
    """
    return SetMicSchedOnset(onset)


setMicSchedRate = DPxDll['DPxSetMicSchedRate']
setMicSchedRate.argtypes = [ctypes.c_uint, ctypes.c_int]
setMicSchedRate.restype = None
def DPxSetMicSchedRate(rate, unit):
        """Sets the MIC schedule rate.
        
        This method allows the user to set the schedule rate. Since the rate can be given 
        with different units, the method also needs to have a unit associated with the rate.
        
        If no delay is required, this method does not need to be used. Default value is 0.

        Args:
            rate (int): Any positive value equal to or greater than zero.
            unit (str): Any of the following predefined constants.\n
                    - **hz**: rate updates per second, maximum 102.4 kHz.
                    - **video**: rate updates per video frame, maximum 102.4 kHz.
                    - **nano**: rate updates period in nanoseconds, minimum 9750 ns.
        
        :Low-level C definition:
            ``void DPxSetMicSchedRate(unsigned rateValue, int rateUnits)``

        """
        setMicSchedRate(rate, api_constants[unit.upper()])
        


# void    DPxSetMicSchedCount(unsigned count)
# Set MIC schedule sample count
SetMicSchedCount = DPxDll['DPxSetMicSchedCount']
SetMicSchedCount.argtypes = [ctypes.c_uint]
SetMicSchedCount.restype = None
def DPxSetMicSchedCount(count):
    """Sets MIC schedule update count.
    
    Args:
        count (int): Schedule count.
    
    :Low-level C definition:
        ``void DPxSetMicSchedCount(unsigned count)``
    """
    return SetMicSchedCount(count)


# void    DPxEnableMicSchedCountdown()
# SchedCount decrements at SchedRate, and schedule stops automatically when count hits 0
EnableMicSchedCountdown = DPxDll['DPxEnableMicSchedCountdown']
EnableMicSchedCountdown.restype = None
def DPxEnableMicSchedCountdown():
    """Enables MIC schedule count down.
    
    SchedCount increments at SchedRate, and schedule is stopped by calling SchedStop.
    
    :Low-level C definition:
        ``void DPxEnableMicSchedCountdown()``
    """
    return EnableMicSchedCountdown()


# void    DPxDisableMicSchedCountdown()
# SchedCount increments at SchedRate, and schedule is stopped by calling SchedStop
DisableMicSchedCountdown = DPxDll['DPxDisableMicSchedCountdown']
DisableMicSchedCountdown.restype = None
def DPxDisableMicSchedCountdown():
    """Disables MIC schedule count down.
    
    SchedCount increments at SchedRate, and schedule is stopped by calling SchedStop.
    
    :Low-level C definition:
        ``void DPxDisableMicSchedCountdown()``
    """
    return DisableMicSchedCountdown()


# void    DPxSetMicSched(unsigned onset, unsigned rateValue, int rateUnits, unsigned count)
# Shortcut which assigns Onset/Rate/Count. If Count > 0, enables Countdown mode.
SetMicSched = DPxDll['DPxSetMicSched']
SetMicSched.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_uint]
SetMicSched.restype = None
def DPxSetMicSched(onset, rateValue, rateUnits, count):
    """Sets MIC schedule onset, count and rate.
    
    This function is a shortcut which assigns Onset/Rate/Count. If ``count`` is greater than zero, the count
    down mode is enabled.
    
    Args:
        onset (int): Schedule onset.
        rateValue (int): Rate value.
        rateUnits (str): Usually ``hz``. Can also be ``video`` to update every ``rateValue`` video frames or ``nano`` to update every ``rateValue`` nanoseconds.
        count (int): Schedule count.
        
    :Low-level C definition:
        ``void DPxSetMicSched(unsigned onset, unsigned rateValue, int rateUnits, unsigned count)``
    """
    return SetMicSched(onset, rateValue, api_constants[rateUnits.upper()], count)


# void    DPxStartMicSched()
# Start running an MIC schedule
StartMicSched = DPxDll['DPxStartMicSched']
StartMicSched.restype = None
def DPxStartMicSched():
    """Starts running a MIC schedule
    
    :Low-level C definition:
        ``void DPxStartMicSched()``
    """
    return StartMicSched()


# void    DPxStopMicSched()
# Stop running an MIC schedule
StopMicSched= DPxDll['DPxStopMicSched']
StopMicSched.restype = None
def DPxStopMicSched():
    """Stops running a MIC schedule.
    
    :Low-level C definition:
        ``void DPxStopMicSched()``
    """
    return StopMicSched()


# int    DPxIsMicSchedCountdown()
# Returns non-0 if SchedCount decrements to 0 and automatically stops schedule
IsMicSchedCountdown = DPxDll['DPxIsMicSchedCountdown']
IsMicSchedCountdown.restype = ctypes.c_int                                                                 
def DPxIsMicSchedCountdown():
    """Returns non-zero if SchedCount decrements to 0 and automatically stops schedule
    
    :Low-level C definition:
        ``int DPxIsMicSchedCountdown()``
    """
    return IsMicSchedCountdown()


# int    DPxIsMicSchedRunning()
# Returns non-0 if MIC schedule is currently running
IsMicSchedRunning = DPxDll['DPxIsMicSchedRunning']
IsMicSchedRunning.restype = ctypes.c_int  
def DPxIsMicSchedRunning():
    """Returns non-zero if MIC schedule is currently running
    
    :Low-level C definition:
        ``int DPxIsMicSchedRunning()``
    """
    return IsMicSchedRunning()

    
setVidMode = DPxDll['DPxSetVidMode']
setVidMode.restype = None
def DPxSetVidMode(mode):
    """Sets the video processing mode.
    
    Only available for PROPixx Revision 6 and higher.
    
    
    Args:
        mode (str) : Any of the following predefined constants.\n
            - **L48**: DVI RED[7:0] is used as an index into a 256-entry 16-bit RGB colour lookup table.
            - **M16**: DVI RED[7:0] & GREEN[7:0] concatenate into a VGA 16-bit value sent to all three RGB components.
            - **C48**: Even/Odd pixel RED/GREEN/BLUE[7:0] concatenate to generate 16-bit RGB components at half the horizontal resolution.
            - **L48D**: DVI RED[7:4] & GREEN[7:4] concatenate to form an 8-bit index into a 256-entry 16-bit RGB colour lookup table.
            - **M16D**: DVI RED[7:3] & GREEN[7:3] & BLUE[7:2] concatenate into a VGA 16-bit value sent to all three RGB components.
            - **C36D**: Even/Odd pixel RED/GREEN/BLUE[7:2] concatenate to generate 12-bit RGB components at half the horizontal resolution.
            - **C24**: Straight passthrough from DVI 8-bit (or HDMI "deep" 10/12-bit) RGB to VGA 8/10/12-bit RGB.
                    
    :Low-level C definition:
        ``void DPxSetVidMode(int vidMode)``
    """
    setVidMode( api_constants[mode.upper()] )    

    

getVidMode = DPxDll['DPxGetVidMode']
getVidMode.restype = ctypes.c_int
def DPxGetVidMode():
    """Gets the video processing mode.
    
    Allows the user to know if it is in the correct mode or which mode is currently used on the device.
    
    Returns:
        String: Any of the following predefined constants.\n
            - **L48**: DVI RED[7:0] is used as an index into a 256-entry 16-bit RGB colour lookup table.
            - **M16**: DVI RED[7:0] & GREEN[7:0] concatenate into a VGA 16-bit value sent to all three RGB components.
            - **C48**: Even/Odd pixel RED/GREEN/BLUE[7:0] concatenate to generate 16-bit RGB components at half the horizontal resolution.
            - **L48D**: DVI RED[7:4] & GREEN[7:4] concatenate to form an 8-bit index into a 256-entry 16-bit RGB colour lookup table.
            - **M16D**: DVI RED[7:3] & GREEN[7:3] & BLUE[7:2] concatenate into a VGA 16-bit value sent to all three RGB components.
            - **C36D**: Even/Odd pixel RED/GREEN/BLUE[7:2] concatenate to generate 12-bit RGB components at half the horizontal resolution.
            - **C24**: Straight passthrough from DVI 8-bit (or HDMI "deep" 10/12-bit) RGB to VGA 8/10/12-bit RGB.
                    
    :Low-level C definition:
        ``int DPxGetVidMode()``
    """
    return video_mode_constants[getVidMode()]



# void DPxSetVidClut(UInt16* clutData)
# Pass 256*3 (=768) 16-bit video DAC data, in order R0,G0,B0,R1,G1,B1...
# DPxSetVidClut() returns immediately, and CLUT is implemented at next vertical blanking interval.
SetVidClut = DPxDll['DPxSetVidClut']
def DPxSetVidClut(CLUT):
    """Sets the video color lookup table (CLUT).
    
    This function returns immediately; the CLUT is implemented at next vertical blanking interval.
    
    Args:
        CLUT (list): A list of 3 lists representing the colors [[RED], [GREEN], [BLUE]]
    
    :Low-level C definition:
        ``void DPxSetVidClut(UInt16* clutData)``
    """
    # First we need to unpack the CLUT
    unpacked_CLUT = []
    for i in range(len(CLUT[0])):
        unpacked_CLUT.append(CLUT[0][i])
        unpacked_CLUT.append(CLUT[1][i])
        unpacked_CLUT.append(CLUT[2][i])

    # Then we need to convert it to a proper Uint16 array
    item_count = len(unpacked_CLUT)
    packed_data = (ctypes.c_uint16 * item_count)(*unpacked_CLUT)
    SetVidClut(packed_data)
    SetVidClut.restype = None


# void DPxSetVidCluts(UInt16* clutData)
# Pass 512*3 (=1536) 16-bit video DAC data to fill 2 channel CLUTs with independent data, in order R0,G0,B0,R1,G1,B1...
SetVidCluts = DPxDll['DPxSetVidCluts']
SetVidCluts.restype = None
def DPxSetVidCluts(CLUTs):
    """Sets the video color lookup tables.
    
    Args:
        CLUT (list): A list of 3 lists representing the colors [[RED], [GREEN], [BLUE]]
    
    :Low-level C definition:
        ``void DPxSetVidCluts(UInt16* clutData)``
    """
    unpacked_CLUT = []
    for i in range(len(CLUTs[0])):
        unpacked_CLUT.append(CLUTs[0][i])
        unpacked_CLUT.append(CLUTs[1][i])
        unpacked_CLUT.append(CLUTs[2][i])

    # Then we need to convert it to a proper Uint16 array
    item_count = len(unpacked_CLUT)
    packed_data = (ctypes.c_uint16 * item_count)(*unpacked_CLUT)
    SetVidCluts(packed_data)


SetVidClutTransparencyColor = DPxDll['DPxSetVidClutTransparencyColor']
SetVidClutTransparencyColor.restype = None
SetVidClutTransparencyColor.argtypes = [ctypes.c_uint16, ctypes.c_uint16, ctypes.c_uint16]
def DPxSetVidClutTransparencyColor(red, green, blue):
    """Set 48-bit RGB video CLUT transparency color.
    
    This function allows the user to set the value for the RGB video CLUT transparency color.
    
    Args:
        red (int): Pixel color value for the red channel. 
        green (int): Pixel color value for the green channel.
        blue (int): Pixel color value for the blue channel.
    
    :Low-level C definition:
        ``void DPxSetVidClutTransparencyColor(UInt16 red, UInt16 green, UInt16 blue)``
        
    See Also:
        :class:`DPxGetVidClutTransparencyColor`
    """  
    SetVidClutTransparencyColor(red, green, blue)



GetVidClutTransparencyColor = DPxDll['DPxGetVidClutTransparencyColor']
GetVidClutTransparencyColor.restype = None
def DPxGetVidClutTransparencyColor():
    """Get 48-bit RGB video CLUT transparency color
    
    This function allows the user to know the current register value for the RGB video CLUT transparency color.
    The returned value is a tupple which contains the red, green and blue values.
    
    Returns:
        red (int): Pixel color value for the red channel. 
        green (int): Pixel color value for the green channel.
        blue (int): Pixel color value for the blue channel.
    
    :Low-level C definition:
        ``void DPxGetVidClutTransparencyColor(UInt16* red, UInt16* green, UInt16* blue)``
    
    See Also:
        :class:`DPxSetVidClutTransparencyColor`
    """
    red = 0
    green = 0
    blue = 0
    p_red = ctypes.c_uint16(red)
    p_green = ctypes.c_uint16(green)
    p_blue = ctypes.c_uint16(blue)
    GetVidClutTransparencyColor(ctypes.byref(p_red), ctypes.byref(p_green), ctypes.byref(p_blue))
    return (p_red.value, p_green.value, p_blue.value)



EnableVidClutTransparencyColorMode= DPxDll['DPxEnableVidClutTransparencyColorMode']
EnableVidClutTransparencyColorMode.restype = None
def DPxEnableVidClutTransparencyColorMode():
    """Enables video CLUT transparency color mode.
    
    :Low-level C definition:
        ``void DPxEnableVidClutTransparencyColorMode()``
        
    See Also:
        :class:`DPxDisableVidClutTransparencyColorMode`, :class:`DPxIsVidClutTransparencyColorMode`, :class:`DPxGetVidClutTransparencyColor`, 
        :class:`DPxSetVidClutTransparencyColor`, 
    """
    return EnableVidClutTransparencyColorMode()



DisableVidClutTransparencyColorMode= DPxDll['DPxDisableVidClutTransparencyColorMode']
DisableVidClutTransparencyColorMode.restype = None
def DPxDisableVidClutTransparencyColorMode():
    """ Disables video CLUT transparency color mode
    
    :Low-level C definition:
        ``void DPxDisableVidClutTransparencyColorMode()``
        
    See Also:
        :class:`DPxEnableVidClutTransparencyColorMode`, :class:`DPxIsVidClutTransparencyColorMode`, :class:`DPxGetVidClutTransparencyColor`, 
        :class:`DPxSetVidClutTransparencyColor`
    """
    return DisableVidClutTransparencyColorMode()



IsVidClutTransparencyColorMode = DPxDll['DPxIsVidClutTransparencyColorMode']
IsVidClutTransparencyColorMode.restype = ctypes.c_int
def DPxIsVidClutTransparencyColorMode():
    """Verifies is the video CLUT transparency color mode is enabled.
    
    This function allows the user to know if the video CLUT transparency color mode is enabled or not.
    
    Returns:
        int: When the mode is disabled, 0 is returned. When the mode is enabled, it returns Non-zero.
    
    :Low-level C definition:
        ``int DPxIsVidClutTransparencyColorMode()``
        
    See Also:
        :class:`DPxEnableVidClutTransparencyColorMode`, :class:`DPxDisableVidClutTransparencyColorMode`, :class:`DPxGetVidClutTransparencyColor`, 
        :class:`DPxSetVidClutTransparencyColor`
    """
    return IsVidClutTransparencyColorMode()


# void        DPxEnableVidHorizSplit()
# VGA 1 shows left half of video image, VGA 2 shows right half of video image.  The two VGA outputs are perfectly synchronized.
EnableVidHorizSplit= DPxDll['DPxEnableVidHorizSplit']
EnableVidHorizSplit.restype = None
def DPxEnableVidHorizSplit():
    """Enables Video Horizontal Split.
    
    VGA 1 shows left half of video image, VGA 2 shows right half of video image.  The two VGA outputs are perfectly synchronized.
    
    :Low-level C definition:
        ``void DPxEnableVidHorizSplit()``
    """
    return EnableVidHorizSplit()


# void        DPxDisableVidHorizSplit()
# VGA 1 and VGA 2 both show entire video image (hardware video mirroring)
DisableVidHorizSplit= DPxDll['DPxDisableVidHorizSplit']
DisableVidHorizSplit.restype = None
def DPxDisableVidHorizSplit():
    """Disables Video Horizontal Split.
    
    VGA 1 and VGA 2 both show entire video image (hardware video mirroring)/
    
    :Low-level C definition:
        ``void DPxDisableVidHorizSplit()``
    """
    return DisableVidHorizSplit()


# void    DPxAutoVidHorizSplit()    
# DATAPixx will automatically split video across the two VGA outputs if the horizontal resolution is at least twice the vertical resolution (default mode)
AutoVidHorizSplit = DPxDll['DPxAutoVidHorizSplit']
AutoVidHorizSplit.restype = None
def DPxAutoVidHorizSplit():
    """ Sets the Horizontal Split mode automatically
    
    DATAPixx will automatically split video across the two VGA outputs if the horizontal 
    resolution is at least twice the vertical resolution (default mode).
    
    :Low-level C definition:
        ``void DPxAutoVidHorizSplit()``
    """
    return AutoVidHorizSplit()


# int        DPxIsVidHorizSplit()
# Returns non-0 if video is being split across the two VGA outputs.
IsVidHorizSplit = DPxDll['DPxIsVidHorizSplit']
IsVidHorizSplit.restype = ctypes.c_int 
def DPxIsVidHorizSplit():
    """Returns non-zero if video is being split across the two VGA outputs.
    
    :Low-level C definition:
        ``int DPxIsVidHorizSplit()``
    """
    return IsVidHorizSplit()


# void        DPxEnableVidVertStereo()
# Top/bottom halves of input image are output in two sequencial video frames.
# VESA L/R output is set to 1 when first frame (left eye) is displayed,
# and set to 0 when second frame (right eye) is displayed.
EnableVidVertStereo= DPxDll['DPxEnableVidVertStereo']
EnableVidVertStereo.restype = None
def DPxEnableVidVertStereo():
    """ Enables Vertical Stereo Video.
    
    Top/bottom halves of input image are output in two sequencial video frames.
    VESA L/R output is set to 1 when first frame (left eye) is displayed,
    and set to 0 when second frame (right eye) is displayed.
    
    :Low-level C definition:
        ``void DPxEnableVidVertStereo()``
    """
    return EnableVidVertStereo()

# void        DPxDisableVidVertStereo()    
# Normal display
DisableVidVertStereo= DPxDll['DPxDisableVidVertStereo']
DisableVidVertStereo.restype = None 
def DPxDisableVidVertStereo():
    """ Disables the Video Vertical Stereo.
    
    A normal display will be in this mode.
    
    :Low-level C definition:
        ``void DPxDisableVidVertStereo()``
    """
    return DisableVidVertStereo()


# void        DPxAutoVidVertStereo()
# Vertical stereo is enabled automatically when vertical resolution > horizontal resolution (default mode)
AutoVidVertStereo = DPxDll['DPxAutoVidVertStereo']
AutoVidVertStereo.restype = None
def DPxAutoVidVertStereo():
    """ Turns on the automatic mode for Video Vertical Stereo.
    
    Vertical stereo is enabled automatically when vertical resolution > horizontal resolution (default mode)
    
    :Low-level C definition:
        ``void DPxAutoVidVertStereo()``
    """
    return AutoVidVertStereo()

# int        DPxIsVidVertStereo()
# Returns non-0 if DATAPixx is separating input into sequencial left/right stereo images.
IsVidVertStereo = DPxDll['DPxIsVidVertStereo']
IsVidVertStereo.restype = ctypes.c_int
def DPxIsVidVertStereo():
    """Returns non-zero if DATAPixx is separating input into sequencial left/right stereo images.
    
    :Low-level C definition:
        ``int DPxIsVidVertStereo()``
    """
    return IsVidVertStereo()


# void DPxEnableVidHorizOverlay()
# VGA 1 and VGA 2 both show an overlay composite of the left/right halves of the video image
EnableVidHorizOverlay = DPxDll['DPxEnableVidHorizOverlay']
EnableVidHorizOverlay.restype = None 
def DPxEnableVidHorizOverlay():
    """Enables the Horizontal overlay
    
    VGA 1 and VGA 2 both show an overlay composite of the left/right halves of the video image
    
    :Low-level C definition:
        ``void DPxEnableVidHorizOverlay()``
    """
    return EnableVidHorizOverlay()


# void        DPxDisableVidHorizOverlay()    
# Horizontal overlay is disabled
DisableVidHorizOverlay = DPxDll['DPxDisableVidHorizOverlay']
DisableVidHorizOverlay.restype = None
def DPxDisableVidHorizOverlay():
    """Disables the Horizontal overlay.
    
    :Low-level C definition:
        ``void DPxDisableVidHorizOverlay()``
    """
    return DisableVidHorizOverlay()


# int        DPxIsVidHorizOverlay()    
# Returns non-0 if the left/right halves of the video image are being overlayed
IsVidHorizOverlay = DPxDll['DPxIsVidHorizOverlay']
IsVidHorizOverlay.restype = ctypes.c_int  
def DPxIsVidHorizOverlay():
    """Returns non-zero if the left/right halves of the video image are being overlayed
    
    :Low-level C definition:
        ``int DPxIsVidHorizOverlay()``
    """
    return IsVidHorizOverlay()


# void DPxSetVidHorizOverlayBounds(int X1, int Y1, int X2, int Y2)
# Set bounding rectangle within left half image whose contents are composited with right half image
SetVidHorizOverlayBounds = DPxDll['DPxSetVidHorizOverlayBounds']
SetVidHorizOverlayBounds.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
SetVidHorizOverlayBounds.restype = None
def DPxSetVidHorizOverlayBounds(x1, y1, x2, y2):
    """Sets bounding rectangle within left half image whose contents are composited with right half image.
    
    Args:
        x1 (int): Bottom left x position.
        y1 (int): Bottom left y position.
        x2 (int): Top right x position.
        y2 (int): Top right y position.
        
    :Low-level C definition:
        ``void DPxSetVidHorizOverlayBounds(int X1, int Y1, int X2, int Y2)``
    """
    return SetVidHorizOverlayBounds(x1, y1, x2, y2)


# void DPxGetVidHorizOverlayBounds(int* X1, int* Y1, int* X2, int* Y2)
# Get bounding rectangle of horizontal overlay window
GetVidHorizOverlayBounds = DPxDll['DPxGetVidHorizOverlayBounds']
GetVidHorizOverlayBounds.restype = None
def DPxGetVidHorizOverlayBounds():
    """Gets the bounding rectangle of horizontal overlay window
    
    Returns:
        A tuple of the form (X1, Y1, X2, Y2)
    
    :Low-level C definition:
        ``void DPxGetVidHorizOverlayBounds(int* X1, int* Y1, int* X2, int* Y2)``    
    """
    X1 = 0
    X2 = 0
    Y1 = 0
    Y2 = 0
    p_X1 = ctypes.c_int(X1)
    p_X2 = ctypes.c_int(X2)
    p_Y1 = ctypes.c_int(Y1)
    p_Y2 = ctypes.c_int(Y2)
    GetVidHorizOverlayBounds(ctypes.byref(p_X1), ctypes.byref(p_Y1), ctypes.byref(p_X2), ctypes.byref(p_Y2))
    return (p_X1.value, p_Y1.value, p_X2.value, p_Y2.value)



# void DPxSetVidHorizOverlayAlpha(UInt16* alphaData)
# Set 1024 16-bit video horizontal overlay alpha values, in order X0,X1..X511,Y0,Y1...Y511
SetVidHorizOverlayAlpha = DPxDll['DPxSetVidHorizOverlayAlpha']
SetVidHorizOverlayAlpha.restype = None
def DPxSetVidHorizOverlayAlpha(int_list):
    """Sets 1024 16-bit video horizontal overlay alpha values, in order X0,X1..X511,Y0,Y1...Y511.
    
    Args:
        int_list (list): A list of integers to set the overlay alpha values, defaults to all zeros
        
    :Low-level C definition:
        ``void DPxSetVidHorizOverlayAlpha(UInt16* alphaData)``
    """
    item_count = len(int_list)
    packed_data = (ctypes.c_uint * item_count)(*int_list)
    return SetVidHorizOverlayAlpha(packed_data)



    
# int DPxGetVidHTotal()
# Get number of video dot times in one horizontal scan line (includes horizontal blanking interval)
GetVidHTotal = DPxDll['DPxGetVidHTotal']
GetVidHTotal.restype = ctypes.c_int 
def DPxGetVidHTotal():
    """Get the number of video dot times in one horizontal scan line (includes horizontal blanking interval)
    
    :Low-level C definition:
        ``int DPxGetVidHTotal()``
    """
    return GetVidHTotal()


# int    DPxGetVidVTotal()
# Get number of video lines in one vertical frame (includes vertical blanking interval)
GetVidVTotal = DPxDll['DPxGetVidVTotal']
GetVidVTotal.restype = ctypes.c_int 
def DPxGetVidVTotal():
    """Gets number of video lines in one vertical frame (includes vertical blanking interval)
    
    :Low-level C definition:
        ``int DPxGetVidVTotal()``
    """
    return GetVidVTotal()


# int        DPxGetVidHActive()    
# Get number of visible pixels in one horizontal scan line
GetVidHActive = DPxDll['DPxGetVidHActive']
GetVidHActive.restype = ctypes.c_int 
def DPxGetVidHActive():
    """Gets the number of visible pixels in one horizontal scan line.
    
    :Low-level C definition:
        ``int DPxGetVidHActive()``
    """
    return GetVidHActive()


# int        DPxGetVidVActive()    
# Get number of visible lines in one vertical frame
GetVidVActive = DPxDll['DPxGetVidVActive']
GetVidVActive.restype = ctypes.c_int 
def DPxGetVidVActive():
    """Gets number of visible lines in one vertical frame.
    
    :Low-level C definition:
        ``int DPxGetVidVActive()``
    """
    return GetVidVActive()


# unsigned    DPxGetVidVPeriod()
# Get video vertical frame period in nanoseconds
GetVidVPeriod = DPxDll['DPxGetVidVPeriod']                                        
GetVidVPeriod.restype = ctypes.c_uint
def DPxGetVidVPeriod():
    """Gets video vertical frame period in nanoseconds
    
    The period is the inverse of the frequency.
    
    :Low-level C definition:
        ``unsigned DPxGetVidVPeriod()``
    """
    return GetVidVPeriod()


# double    DPxGetVidVFreq()
# Get video vertical frame rate in Hz
GetVidVFreq = DPxDll['DPxGetVidVFreq']
GetVidVFreq.restype = ctypes.c_double
def DPxGetVidVFreq():
    """Gets video vertical line rate in Hz.
    
    The vertical line rate in Hz, which represents the time taken for a whole vertical line to be switched on,
    including the blanking time.
    
    :Low-level C definition:
        ``double DPxGetVidVFreq()``
    """
    return GetVidVFreq()


# double    DPxGetVidHFreq()
# Get video horizontal line rate in Hz
GetVidHFreq = DPxDll['DPxGetVidHFreq']
GetVidHFreq.restype = ctypes.c_double
def DPxGetVidHFreq():
    """Gets the video horizontal line rate in Hz
    
    The Horizontal line rate in Hz, which represents the time taken for a whole horizontal line to be switched on,
    including the blanking time.
    
    :Low-level C definition:
        ``double DPxGetVidHFreq()``
    """
    return GetVidHFreq()


# double    DPxGetVidDotFreq()    
# Get video dot frequency in Hz
GetVidDotFreq = DPxDll['DPxGetVidDotFreq']
GetVidDotFreq.restype = ctypes.c_double
def DPxGetVidDotFreq():
    """ Gets the dot frequency for the device in Hz.
    
    The dot frequency represents the time taken for a pixel to be switched on. 
    It is calculated by considering all pixels (including those in blanking time) times the refresh rate.
    
    :Low-level C definition:
        ``double DPxGetVidDotFreq()``
    """
    return GetVidDotFreq()

# int DPxIsVidDviActive()    
# Returns non-0 if DATAPixx is currently receiving video data over DVI link
IsVidDviActive = DPxDll['DPxIsVidDviActive']
IsVidDviActive.restype = ctypes.c_int   
def DPxIsVidDviActive():
    """Returns non-zero if DATAPixx is currently receiving video data over DVI link
    
    :Low-level C definition:
        ``int DPxIsVidDviActive()``
    """
    return IsVidDviActive()


# int DPxIsVidDviActiveDual()    
# Returns non-zero if DATAPixx is currently receiving video data over dual-link DVI
IsVidDviActiveDual = DPxDll['DPxIsVidDviActiveDual']
IsVidDviActiveDual.restype = ctypes.c_int  
def DPxIsVidDviActiveDual():
    """Returns non-zero if DATAPixx is currently receiving video data over dual-link DVI
    
    :Low-level C definition:
        ``int DPxIsVidDviActiveDual()``
    """
    return IsVidDviActiveDual()


# int DPxIsVidDviLockable() 
# Returns non-zero if VIEWPixx is currently receiving video whose timing can directly drive display.
IsVidDviLockable = DPxDll['DPxIsVidDviLockable']
IsVidDviLockable.restype = ctypes.c_int 
def DPxIsVidDviLockable():
    """Returns non-zero if VIEWPixx is currently receiving video whose timing can directly drive display.
    
    :Low-level C definition:
        ``int DPxIsVidDviLockable()``
    """
    return IsVidDviLockable()


# int DPxIsVidOverClocked()
# Returns non-zero if DATAPixx is receiving video at too high a clock frequency
IsVidOverClocked = DPxDll['DPxIsVidOverClocked']
IsVidOverClocked.restype = ctypes.c_int
def DPxIsVidOverClocked():
    """Returns non-zero if DATAPixx is receiving video at clock frequency that is higher than normal.
    
    :Low-level C definition:
        ``int DPxIsVidOverClocked()``
    """
    return IsVidOverClocked()


# void DPxSetVidVesaLeft()    
# VESA connector outputs left-eye signal
SetVidVesaLeft = DPxDll['DPxSetVidVesaLeft']
SetVidVesaLeft.restype = None
def DPxSetVidVesaLeft():
    """VESA connector outputs left-eye signal.
    
    :Low-level C definition:
        ``void DPxSetVidVesaLeft()``
    """
    return SetVidVesaLeft()



SetVidVesaRight= DPxDll['DPxSetVidVesaRight']
SetVidVesaRight.restype = None
def DPxSetVidVesaRight():
    """VESA connector outputs right-eye signal.
    
    :Low-level C definition:
        ``void DPxSetVidVesaRight()``
    """
    return SetVidVesaRight()


# int DPxIsVidVesaLeft()
# Returns non-0 if VESA connector has left-eye signal
IsVidVesaLeft = DPxDll['DPxIsVidVesaLeft']
IsVidVesaLeft.restype = ctypes.c_int  
def DPxIsVidVesaLeft():
    """Returns non-zero if VESA connector has left-eye signal
    
    :Low-level C definition:
        ``int DPxIsVidVesaLeft()``
    """
    return IsVidVesaLeft()


# void    DPxEnableVidVesaBlueline() 
# VESA 3D output interprets middle pixel on last raster line as a blueline code
EnableVidVesaBlueline = DPxDll['DPxEnableVidVesaBlueline']
EnableVidVesaBlueline.restype = None
def DPxEnableVidVesaBlueline():
    """Enables the Video blue line mode.

    When enabled, the VESA 3D output interprets the middle pixel on last raster line as a blue line code.
    When disabled, the VESA 3D output is not dependent on video content.
    
    :Low-level C definition:
        ``void DPxEnableVidVesaBlueline()``
    """
    return EnableVidVesaBlueline()


# void        DPxDisableVidVesaBlueline()    
# VESA 3D output is not dependent on video content
DisableVidVesaBlueline= DPxDll['DPxDisableVidVesaBlueline']
DisableVidVesaBlueline.restype = None
def DPxDisableVidVesaBlueline():
    """Disables the Video blue line mode.

    When enabled, the VESA 3D output interprets the middle pixel on last raster line as a blue line code.
    When disabled, the VESA 3D output is not dependent on video content.
    
    :Low-level C definition:
        ``void DPxDisableVidVesaBlueline()``
    """
    return DisableVidVesaBlueline()


# int    DPxIsVidVesaBlueline()
# Returns non-zero if VESA 3D output is dependent on video blueline codes
IsVidVesaBlueline = DPxDll['DPxIsVidVesaBlueline']
IsVidVesaBlueline.restype = ctypes.c_int
def DPxIsVidVesaBlueline():
    """Returns non-zero if VESA 3D output is dependent on video blueline codes
       
    :Low-level C definition:
        ``int DPxIsVidVesaBlueline()``
    """
    return IsVidVesaBlueline()

    

setVidVesaWaveform = DPxDll['DPxSetVidVesaWaveform']
setVidVesaWaveform.argtypes = [ctypes.c_int]
setVidVesaWaveform.restype = None
def DPxSetVidVesaWaveform(waveform):
    """Sets the waveform which will be sent to the DATAPixx VESA 3D connector.
    
    Only available for PROPixx Revision 6 and higher.
    
    
    Args: 
        waveform (str) : Any of the following predefined constants.\n
            - **LR**: VESA port drives straight L/R squarewave for 3rd party emitter.  
            - **CRYSTALEYES**: VESA port drives 3DPixx IR emitter for CrystalEyes 3D goggles.   
            - **NVIDIA**: VESA port drives 3DPixx IR emitter for NVIDIA 3D goggles.
            
                    
    :Low-level C definition:
        ``void DPxSetVidVesaWaveform(int waveform)``
    
    """
    setVidVesaWaveform( api_constants[waveform.upper()] ) 
    


getVidVesaWaveform = DPxDll['DPxGetVidVesaWaveform']
getVidVesaWaveform.restype = ctypes.c_int
def DPxGetVidVesaWaveform():
    """Gets the waveform which is being sent to the DATAPixx VESA 3D connector.
    
    Returns:
        String: Any of the following predefined constants.\n
            - **LR**: VESA port drives straight L/R squarewave for 3rd party emitter.
            - **CRYSTALEYES**: VESA port drives 3DPixx IR emitter for CrystalEyes 3D goggles.
            - **NVIDIA**: VESA port drives 3DPixx IR emitter for NVIDIA 3D goggles.
            
                    
    :Low-level C definition:
        ``int DPxGetVidVesaWaveform()``
    
    """
    return vesa_mode_constants[getVidVesaWaveform()]    
    


# void     DPxSetVidVesaPhase(int phase)
# Set the 8-bit unsigned phase of the VESA 3D waveform
# Varying this phase from 0-255 will fine tune phase relationship between stereo video and 3D goggle switching
# The following combinations have been found to work well:
# Waveform=DPXREG_VID_VESA_WAVEFORM_NVIDIA, Phase=100, for VIEWPixx/3D + scanning backlight + 3DPixx IR emitter + NVIDIA 3D Vision glasses
# Waveform=DPXREG_VID_VESA_WAVEFORM_NVIDIA, Phase=245, for DATAPixx + CRT + 3DPixx IR emitter + NVIDIA 3D Vision glasses
# Waveform=DPXREG_VID_VESA_WAVEFORM_CRYSTALEYES, Phase=100, for VIEWPixx/3D + scanning backlight + 3DPixx  IR emitter + CrystalEyes glasses
SetVidVesaPhase = DPxDll['DPxSetVidVesaPhase']
SetVidVesaPhase.argtypes = [ctypes.c_int]
SetVidVesaPhase.restype = None
def DPxSetVidVesaPhase(phase):
    """Sets the 8-bit unsigned phase of the VESA 3D waveform.

    Varying this phase from 0-255, allows adjustements to the phase relationship between stereo video and 3D goggles switching.
    
    The following combinations have been found to work well:
           
    If you are using a VIEWPIxx/3D, you should set the ``phase`` to ``0x64``. If you
    are using a CTR with our DATAPixx, it should be set to ``0xF5``.
        
    Args:
        phase (int): Phase of the VESA 3D waveform

    :Low-level C definition:
        ``void DPxSetVidVesaPhase(int phase)``
    """
    return SetVidVesaPhase(phase)
 
 
# int DPxGetVidVesaPhase()
# Get the 8-bit unsigned phase of the VESA 3D waveform
GetVidVesaPhase = DPxDll['DPxGetVidVesaPhase']
GetVidVesaPhase.restype = ctypes.c_int 
def DPxGetVidVesaPhase():
    """Gets the 8 bits unsigned phase of the VESA 3D waveform.
    
    Returns:
            phase (int): Phase of the VESA 3D waveform.
            
    :Low-level C definition:
        ``int DPxGetVidVesaPhase()``
    """
    return GetVidVesaPhase()



GetVidLine = DPxDll['DPxGetVidLine']
GetVidLine.restype = ctypes.POINTER( ctypes.c_ushort )
def DPxGetVidLine(Hex = False):
    """
    Reads pixels from the VPixx device line buffer, and returns a list containing the data. 
    For each pixel, the buffer contains 16 bits R/G/B/U (where U is thrown away). The returned data is a list
    containing three lists for the respective R/G/B colors.
    
    Args:
        Hex (bool, optional): True returns the value in hexadecimal. Everything else will return the value in decimal. 
    
    Return:
        lists of list: A list which has [[RED], [GREEN], [BLUE]]
        
    :Low-level C definition:
        ``short* DPxGetVidLine()``
    """
    
    p_value = GetVidLine()
    
    print'type p_value: ', type(p_value)
    print'p_value ', p_value[0]
    
    pixel_values = [[],[],[]]
    for pixel_number in range(1920):
        pixel_values[0].append(p_value[4*pixel_number] >> 8) # R
        pixel_values[1].append(p_value[4*pixel_number + 1]>> 8) # G
        pixel_values[2].append(p_value[4*pixel_number + 2]>> 8) # B
    """
    line_buff = []
    line_nbr = 1920*4
    if Hex == True:
        for line in range(line_nbr):
            # trim the last part since its unused
            line_buff.append( hex(p_value[line]>> 8 ))
    else:
        for line in range(line_nbr):
            # trim the last part since its unused
            line_buff.append( p_value[line]>> 8 )
    """
    return pixel_values


# void    DPxSetVidPsyncRasterLine(int line)    
# Set the raster line on which pixel sync sequence is expected                                                                           
SetVidPsyncRasterLine  = DPxDll['DPxSetVidPsyncRasterLine']
SetVidPsyncRasterLine.argtypes = [ctypes.c_int]
SetVidPsyncRasterLine.restype = None
def DPxSetVidPsyncRasterLine(line):
    """Sets the raster line on which the pixel sync sequence is expected.
    
    Args:
        line (int): The line which will contain de PSync.
    
    :Low-level C definition:
        ``void DPxSetVidPsyncRasterLine(int line)``
    """
    return SetVidPsyncRasterLine(line)


# int    DPxGetVidPsyncRasterLine()    
# Get the raster line on which pixel sync sequence is expected
GetVidPsyncRasterLine = DPxDll['DPxGetVidPsyncRasterLine']
GetVidPsyncRasterLine.restype = ctypes.c_int 
def DPxGetVidPsyncRasterLine():
    """Gets the raster line on which pixel sync sequence is expected.
    
    Returns:
        An integer which represents the line which has the PSync.
        
    :Low-level C definition:
        ``int DPxGetVidPsyncRasterLine()``
    """
    return GetVidPsyncRasterLine()


# void    DPxEnableVidPsyncSingleLine()
# Pixel sync is only recognized on a single raster line                   
EnableVidPsyncSingleLine= DPxDll['DPxEnableVidPsyncSingleLine']
EnableVidPsyncSingleLine.restype = None
def DPxEnableVidPsyncSingleLine():
    """Enables Psync for Single (Raster) Line.
    
    :Low-level C definition:
        ``void DPxEnableVidPsyncSingleLine()``
    """
    return EnableVidPsyncSingleLine()


# void    DPxDisableVidPsyncSingleLine()    
# Pixel sync is recognized on any raster line                               
DisableVidPsyncSingleLine= DPxDll['DPxDisableVidPsyncSingleLine']
DisableVidPsyncSingleLine.restype = None 
def DPxDisableVidPsyncSingleLine():
    """Disables Psync for Single (Raster) Line.
    
    :Low-level C definition:
        ``void DPxDisableVidPsyncSingleLine()``
    """
    return DisableVidPsyncSingleLine()


# int DPxIsVidPsyncSingleLine()
# Returns non-zero if pixel sync is only recognized on a single raster line
IsVidPsyncSingleLine = DPxDll['DPxIsVidPsyncSingleLine']
IsVidPsyncSingleLine.restype = ctypes.c_int 
def DPxIsVidPsyncSingleLine():
    """ Returns non-zero if pixel sync is only recognized on a single raster line.
    
    :Low-level C definition:
        ``int DPxIsVidPsyncSingleLine()``
    """
    return IsVidPsyncSingleLine()


# void        DPxEnableVidPsyncBlankLine()
# Pixel sync raster line is always displayed black                         
EnableVidPsyncBlankLine= DPxDll['DPxEnableVidPsyncBlankLine']
EnableVidPsyncBlankLine.restype = None
def DPxEnableVidPsyncBlankLine():
    """Enables the PSync Black Line
    
    The sync raster line is always displayed black.
    
    :Low-level C definition:
        ``void DPxEnableVidPsyncBlankLine()``
    """
    return EnableVidPsyncBlankLine()


# void    DPxDisableVidPsyncBlankLine()    
# Pixel sync raster line is displayed normally                             
DisableVidPsyncBlankLine= DPxDll['DPxDisableVidPsyncBlankLine']
DisableVidPsyncBlankLine.restype = None
def DPxDisableVidPsyncBlankLine():
    """Disables the PSync Blank Line.
    
    Pixel sync raster line is displayed normally when this is disabled.
    
    :Low-level C definition:
        ``void DPxDisableVidPsyncBlankLine()``
    """
    return DisableVidPsyncBlankLine()


# int    DPxIsVidPsyncBlankLine()    
# Returns non-zero if pixel sync raster line is always displayed black
IsVidPsyncBlankLine = DPxDll['DPxIsVidPsyncBlankLine']
IsVidPsyncBlankLine.restype = ctypes.c_int 
def DPxIsVidPsyncBlankLine():
    """Returns non-zero if pixel sync raster line is always displayed black
    
    :Low-level C definition:
        ``int DPxIsVidPsyncBlankLine()``
    """
    return IsVidPsyncBlankLine()


# void     DPxSetVidSource(int vidSource)  
# Set source of video pattern to be displayed                              
SetVidSource  = DPxDll['DPxSetVidSource'] 
SetVidSource.argtypes = [ctypes.c_int]
SetVidSource.restype = None
def DPxSetVidSource(vidSource):
    """Sets the source of video to be displayed.
    
    Args:
        vidSource (str): The source we want to display. \n
            - **DVI**: Monitor displays DVI signal.
            - **SWTP**: Software test pattern showing image from RAM.
            - **SWTP 3D**: 3D Software test pattern flipping between left/right eye images from RAM.
            - **RGB SQUARES**: RGB ramps.
            - **GRAY**: Uniform gray display having 12-bit intensity.
            - **BAR**: Drifting bar.
            - **BAR2**: Drifting bar.
            - **DOTS**: Drifting dots.
            - **RAMP**: Drifting ramp, with dots advancing ``x*2`` pixels per video frame, where ``x`` is a 4-bit signed.
            - **RGB**: Uniform display with 8-bit intensity nn, send to RGBA channels enabled by mask m.
            - **PROJ**: Projector Hardware test pattern.
                
    :Low-level C definition:
        ``void DPxSetVidSource(int vidSource)``
    """
    if type(vidSource) is str:
        SetVidSource(test_pattern_constants[vidSource.upper()])
    else:
        SetVidSource(vidSource)
    
    
# int DPxGetVidSource()       
# Get source of video pattern being displayed
GetVidSource = DPxDll['DPxGetVidSource']
GetVidSource.restype = ctypes.c_int
def DPxGetVidSource(return_str=False):
    """Gets source of video being displayed.
    
    Args:
        return_str (Bool): When True, the return value is a string describing the video source used. Else, an integer is returned. \n
    
    Returns:
        vidSource (str): The source currently displayed. \n
            - **DVI**: Monitor displays DVI signal.
            - **SWTP**: Software test pattern showing image from RAM.
            - **SWTP 3D**: 3D Software test pattern flipping between left/right eye images from RAM.
            - **RGB SQUARES**: RGB ramps.
            - **GRAY**: Uniform gray display having 12-bit intensity.
            - **BAR**: Drifting bar.
            - **BAR2**: Drifting bar.
            - **DOTS**: Drifting dots.
            - **RAMP**: Drifting ramp, with dots advancing ``x*2`` pixels per video frame, where ``x`` is a 4-bit signed.
            - **RGB**: Uniform display with 8-bit intensity nn, send to RGBA channels enabled by mask m.
            - **PROJ**: Projector Hardware test pattern.
    
    :Low-level C definition:
        ``int DPxGetVidSource()``
    """
    temp = GetVidSource()
    vidSource = temp
    if return_str == True:
        vidSource = 'none'#In case we can't find the associated key.
        for key, value in test_pattern_constants.iteritems():
            if temp == 0:
                vidSource = 'DVI'
                break
            elif value == temp:
                vidSource = key
                break
    return vidSource


# void     DPxEnableVidScanningBacklight() 
# Enable VIEWPixx scanning backlight                                      
EnableVidScanningBacklight  = DPxDll['DPxEnableVidScanningBacklight']
EnableVidScanningBacklight.restype = None
def DPxEnableVidScanningBacklight():
    """Enables VIEWPixx scanning backlight
    
    :Low-level C definition:
        ``void DPxEnableVidScanningBacklight()``
    """
    return EnableVidScanningBacklight()


# void     DPxDisableVidScanningBacklight()
# Disable VIEWPixx scanning backlight                                     
DisableVidScanningBacklight = DPxDll['DPxDisableVidScanningBacklight']
DisableVidScanningBacklight.restype = None
def DPxDisableVidScanningBacklight():
    """Disables VIEWPixx scanning backlight.
    
    :Low-level C definition:
        ``void DPxDisableVidScanningBacklight()``
    """
    return DisableVidScanningBacklight()

# void     DPxEnableVidRescanWarning() 
# Enable VIEWPixx Rescan Warning                                      
EnableVidRescanWarning  = DPxDll['DPxEnableVidRescanWarning']
EnableVidRescanWarning.restype = None
def DPxEnableVidRescanWarning():
    """Enables VIEWPixx Rescan Warning
    
    :Low-level C definition:
        ``void DPxEnableVidRescanWarning()``
    """
    return EnableVidRescanWarning()


# void     DPxDisableVidScanningBacklight()
# Disable VIEWPixx scanning backlight                                     
DisableVidRescanWarning = DPxDll['DPxDisableVidRescanWarning']
DisableVidRescanWarning.restype = None
def DPxDisableVidRescanWarning():
    """Disables VIEWPixx Rescan Warning.
    
    :Low-level C definition:
        ``void DPxDisableVidRescanWarning()``
    """
    return DisableVidRescanWarning()


# int      DPxIsVidScanningBacklight()  
# Returns non-zero if VIEWPixx scanning backlight is enabled
IsVidScanningBacklight = DPxDll['DPxIsVidScanningBacklight']
IsVidScanningBacklight.restype = ctypes.c_int
def DPxIsVidScanningBacklight():
    """Returns non-zero if VIEWPixx scanning backlight is enabled
    
    :Low-level C definition:
        ``int DPxIsVidScanningBacklight()``
    """
    return IsVidScanningBacklight()


# void     DPxVideoScope(int toFile)
# VIEWPixx video source analysis
VideoScope = DPxDll['DPxVideoScope']
VideoScope.restype = None
def DPxVideoScope(file_path):
    """VIEWPixx video source analysis.

    Args:
        file_path (str): Where the file to analyze is located.
        
    :Low-level C definition:
        ``void DPxVideoScope(int toFile)``
    """
    return VideoScope(file_path)
 
 
# int DPxIsPPxVidSeqEnabled(void)
IsPPxVidSeqEnabled = DPxDll['DPxIsPPxVidSeqEnabled'] 
IsPPxVidSeqEnabled.restype = ctypes.c_int   
def DPxIsPPxVidSeqEnabled():
    """Checks to see if the PROPixx Video Sequencer is enabled.
    
    Returns:
        0 (False) if the PROPixx Video Sequencer is Disabled, 1 (True) if Enabled.
    
    :Low-level C definition:
        ``int DPxIsPPxVidSeqEnabled(void)``
    """
    return IsPPxVidSeqEnabled()

# double DPxGetPPxVoltageMonitor(int voltageNum)
GetPPxVoltageMonitor = DPxDll['DPxGetPPxVoltageMonitor']                             
GetPPxVoltageMonitor.restype = ctypes.c_double
GetPPxVoltageMonitor.argtypes = [ctypes.c_int]    
def DPxGetPPxVoltageMonitor(voltageNum):
    """Gets the Voltage for the given sensor.
    
    Args:
        voltageNum (int): The number of the sensor.
    
    Returns:
        The volatage in Volts for the chosen monitor.
        
    :Low-level C definition:
        ``double DPxGetPPxVoltageMonitor(int voltageNum)``
    """
    return GetPPxVoltageMonitor(voltageNum)


# double DPxGetPPxTemperature(int tempNum)
GetPPxTemperature = DPxDll['DPxGetPPxTemperature']                                   
GetPPxTemperature.restype = ctypes.c_double
GetPPxTemperature.argtypes = [ctypes.c_int]
def DPxGetPPxTemperature(tempNum):
    """Get a PROPixx temperature for a given sensor number.
    
    Args:
        tempNum (int): Number of the sensor.
    
    Returns
        The temperature in Celcius of the sensor.
    
    :Low-level C definition:
        ``double DPxGetPPxTemperature(int tempNum)``
    """
    return GetPPxTemperature(tempNum)
   
   
# double DPxGetPPxLedCurrent(int ledNum)
GetPPxLedCurrent = DPxDll['DPxGetPPxLedCurrent']                                     
GetPPxLedCurrent.restype = ctypes.c_double
GetPPxLedCurrent.argtypes = [ctypes.c_int]     
def DPxGetPPxLedCurrent(ledNum):
    """Get PROPixx LED Current.
    
    Args:
        ledNum (int): The number of the LED.
    
    Returns:
        The value of the current of the selected LED as a double in Amps.
         
    :Low-level C definition:
        ``double DPxGetPPxLedCurrent(int ledNum)``
    """
    return GetPPxLedCurrent(ledNum)


# void DPxSetPPxLedCurrent(int ledNum, double current);
SetPPxLedCurrent = DPxDll['DPxSetPPxLedCurrent']                                     
SetPPxLedCurrent.argtypes = [ctypes.c_int, ctypes.c_double]     
def DPxSetPPxLedCurrent(ledNum, current):
    return SetPPxLedCurrent(ledNum, current)

      
# double DPxGetPPxFanTachometer(int fanNum)
GetPPxFanTachometer  = DPxDll['DPxGetPPxFanTachometer']                              
GetPPxFanTachometer.restype = ctypes.c_double
GetPPxFanTachometer.argtypes = [ctypes.c_int]    
def DPxGetPPxFanTachometer(fanNum):
    """ Returns the speed at which a fan is rotating.
    
    Args:
        fanNum(int): The number of the fan.
    
    :Low-level C definition:
        ``double DPxGetPPxFanTachometer(int fanNum)``
    """
    return GetPPxFanTachometer(fanNum)

# double DPxGetPPxFanPwm(void)        
GetPPxFanPwm = DPxDll['DPxGetPPxFanPwm']                                             
GetPPxFanPwm.restype = ctypes.c_double
def DPxGetPPxFanPwm():
    """ Returns the Fans PWN.
    
    Return:
        Current fan PWN as a double.
        
    :Low-level C definition:
        ``double DPxGetPPxFanPwm(void)`` 
    """
    return GetPPxFanPwm()

# void DPxEnablePPxCeilingMount(void)    
EnablePPxCeilingMount = DPxDll['DPxEnablePPxCeilingMount']
EnablePPxCeilingMount.restype = None
def DPxEnablePPxCeilingMount():
    """Enables the PROPixx Ceiling Mount mode.
    
    :Low-level C definition:
        ``void DPxEnablePPxCeilingMount(void)`` 
    """
    return EnablePPxCeilingMount()

 
# void DPxDisablePPxCeilingMount(void)
DisablePPxCeilingMount = DPxDll['DPxDisablePPxCeilingMount']
DisablePPxCeilingMount.restype = None
def DPxDisablePPxCeilingMount():
    """Disables the PROPixx Ceiling Mount mode.
    
    :Low-level C definition:
        ``void DPxDisablePPxCeilingMount(void)``
    """
    return DisablePPxCeilingMount()

 
# int DPxIsPPxCeilingMount(void)
IsPPxCeilingMount = DPxDll['DPxIsPPxCeilingMount'] 
IsPPxCeilingMount.restype = ctypes.c_int
def DPxIsPPxCeilingMount():
    """Check to see if the PROPixx is in Ceiling Mount mode.
    
    Returns:
        0 (False) if the PROPixx is not in Ceiling Mount mode, 1 (True) otherwise.
    
    :Low-level C definition:
        ``int DPxIsPPxCeilingMount(void)``
    """
    return IsPPxCeilingMount()


# void DPxEnablePPxRearProjection(void)
EnablePPxRearProjection = DPxDll['DPxEnablePPxRearProjection']
EnablePPxRearProjection.restype = None
def DPxEnablePPxRearProjection():
    """ Enables the Rear Projection of the PROPixx.    
    
    :Low-level C definition:
        ``void DPxEnablePPxRearProjection(void)``
    """
    return EnablePPxRearProjection()

 
# void DPxDisablePPxRearProjection(void)
DisablePPxRearProjection = DPxDll['DPxDisablePPxRearProjection']
DisablePPxRearProjection.restype = None 
def DPxDisablePPxRearProjection():
    """Disables the Rear Projection of the PROPixx.
    
    :Low-level C definition:
        ``void DPxDisablePPxRearProjection(void)``
    """
    return DisablePPxRearProjection()

 
# int DPxIsPPxRearProjection(void)
IsPPxRearProjection = DPxDll['DPxIsPPxRearProjection'] 
IsPPxRearProjection.restype = ctypes.c_int
def DPxIsPPxRearProjection():
    """Check to see if the PROPixx is in Rear projection
    
    Returns:
        0 (False) if the PROPixx is not in rear projection, 1 (True) otherwise.
        
    :Low-level C definition:
        ``int DPxIsPPxRearProjection(void)``
    """
    return IsPPxRearProjection()

# void DPxSetPPx3dCrosstalk(double crosstalk)
# Set 3D crosstalk (0-1) which should be subtracted from stereoscopic stimuli
SetPPx3dCrosstalk = DPxDll['DPxSetPPx3dCrosstalk']
SetPPx3dCrosstalk.argtypes = [ctypes.c_double]
SetPPx3dCrosstalk.restype = None  
def DPxSetPPx3dCrosstalk(crosstalk):
    """Sets the 3D crosstalk (0-1) which should be subtracted from stereoscopic stimuli.
    
    Warning:
        This only works with RB3D mode and requires revision 6 of the PROPixx.
    Args:
        crosstalk (double): A value between 0 and 1 which represents the 3d crosstalk.
        
    :Low-level C definition:
        ``void DPxSetPPx3dCrosstalk(double crosstalk)``
    """
    return SetPPx3dCrosstalk(crosstalk)

# double    DPxGetPPx3dCrosstalk(void)
# Get 3D crosstalk (0-1) which is being subtracted from stereoscopic stimuli
GetPPx3dCrosstalk = DPxDll['DPxGetPPx3dCrosstalk']
GetPPx3dCrosstalk.restype = ctypes.c_double
def DPxGetPPx3dCrosstalk():
    """Gets 3D crosstalk (0-1) which is being subtracted from stereoscopic stimuli.
    
    Warning:
        This only works with RB3D mode and requires revision 6 of the PROPixx.
        
    Returns:
        A double value for the 3D Crosstalk.
    
    :Low-level C definition:
        ``double DPxGetPPx3dCrosstalk(void)``
    """
    return GetPPx3dCrosstalk()



setPPxDlpSeqPgrm = DPxDll['DPxSetPPxDlpSeqPgrm']
setPPxDlpSeqPgrm.argtypes = [ctypes.c_int]
setPPxDlpSeqPgrm.restype = None
def DPxSetPPxDlpSeqPgrm(program):
    """Sets the PROPixx DLP Sequencer program.
    
    Only available for PROPixx Revision 6 and higher.
    
    
    Args:
        String : Any of the following predefined constants.\n
            - **RGB**: Default RGB
            - **RB3D**: R/B channels drive grayscale 3D
            - **RGB240**: Only show the frame for 1/2 a 120 Hz frame duration.
            - **RGB180**: Only show the frame for 2/3 of a 120 Hz frame duration.
            - **QUAD4X**: Display quadrants are projected at 4x refresh rate.
            - **QUAD12X**: Display quadrants are projected at 12x refresh rate with grayscales.
            - **GREY3X**: Converts 640x1080@360Hz RGB to 1920x1080@720Hz Grayscale with blank frames.
                    
    :Low-level C definition:
        ``void DPxSetPPxDlpSeqPgrm(int program)``
    """
    setPPxDlpSeqPgrm( api_constants[program.upper()] )
    

 
getPPxDlpSeqPgrm = DPxDll['DPxGetPPxDlpSeqPgrm']
getPPxDlpSeqPgrm.restype = ctypes.c_int
def DPxGetPPxDlpSeqPgrm():
    """Get PROPixx DLP Sequencer program.
    
    This method returns the current program loaded in the PROPixx sequencer.
    
    Returns:
        String: Any of the following predefined constants.\n
            - **RGB**: Default RGB
            - **RB3D**: R/B channels drive grayscale 3D
            - **RGB240**: Only show the frame for 1/2 a 120 Hz frame duration.
            - **RGB180**: Only show the frame for 2/3 of a 120 Hz frame duration.
            - **QUAD4X**: Display quadrants are projected at 4x refresh rate.
            - **QUAD12X**: Display quadrants are projected at 12x refresh rate with grayscales.
            - **GREY3X**: Converts 640x1080@360Hz RGB to 1920x1080@720Hz Grayscale with blank frames.
                    
    :Low-level C definition:
        ``int DPxGetPPxDlpSeqPgrm(void)``
    """
    return propixx_sequencer_constants[ getPPxDlpSeqPgrm() ]

setPPxLedMask = DPxDll['DPxSetPPxLedMask']
setPPxLedMask.argtypes = [ctypes.c_int]
setPPxLedMask.restype = None
def DPxSetPPxLedMask(mask):
    """Sets the PROPixx mask to turn off specific LEDs.
    
    Only available for PROPixx Revision 33 and higher.
    
    
    Args:
        Int : Any of the following predefined constants.\n
            - **0**: All LEDs are on.   
            - 1: RED is turned off.
            - 2: GREEN is turned off.
            - 3: RED and GREEN are turned off.
            - 4: BLUE is turned off.
            - 5: RED and BLUE are turned off.
            - 6: BLUE and GREEN are turned off.
            - 7: ALL LEDs are off.\n";
                    
    :Low-level C definition:
        ``void DPxSetPPxLedMask(int mask)``
    """
    setPPxLedMask(mask)
    
getPPxLedMask = DPxDll['DPxGetPPxLedMask']
getPPxLedMask.restype = ctypes.c_int
def DPxGetPPxLedMask():
    """Get the PROPixx LED mask.
    
    Only available for PROPixx Revision 33 and higher.
    
    
    Returns:
        Int : Any of the following number.\n
            - **0**: All LEDs are on.   
            - **1**: RED is turned off.
            - **2**: GREEN is turned off.
            - **3**: RED and GREEN are turned off.
            - **4**: BLUE is turned off.
            - **5**: RED and BLUE are turned off.
            - **6**: BLUE and GREEN are turned off.
            - **7**: ALL LEDs are off.\n";
                    
    :Low-level C definition:
        ``int DPxGetPPxDlpSeqPgrm()``
    """
    return getPPxLedMask()   
    
# void DPxEnablePPxLampLed(void)
enablePPxLampLed = DPxDll['DPxEnablePPxLampLed']
enablePPxLampLed.restype = None
def DPxEnablePPxLampLed():
    """ Enables the lamp LED of the PROPixx.
    
    Only available for PROPixx Revision 12 and higher.    
    
    :Low-level C definition:
        ``void DPxEnablePPxLampLed(void)``
    """
    return enablePPxLampLed()

 
# void DPxDisablePPxLampLed(void)
disablePPxLampLed = DPxDll['DPxDisablePPxLampLed']
disablePPxLampLed.restype = None 
def DPxDisablePPxLampLed():
    """Disables the lamp LED of the PROPixx.
    
    Only available for PROPixx Revision 12 and higher.
    
    :Low-level C definition:
        ``void DPxDisablePPxLampLed(void)``
    """
    return disablePPxLampLed()


# int DPxIsPPxLampLedEnabled(void)
isPPxLampLedEnabled = DPxDll['DPxIsPPxLampLedEnabled'] 
isPPxLampLedEnabled.restype = ctypes.c_int
def DPxIsPPxLampLedEnabled():
    """Check to see if the PROPixx lamp LED is enabled.
    
    Only available for PROPixx Revision 12 and higher.
    
    Returns:
        0 (False) if the PROPixx lamp LED is disabled, 1 (True) otherwise.
    
    :Low-level C definition:
        ``int DPxIsPPxLampLedEnabled(void)``
    """
    return isPPxLampLedEnabled()


# void DPxEnablePPxQuietFanMode(void)
enablePPxQuietFanMode = DPxDll['DPxEnablePPxQuietFanMode']
enablePPxQuietFanMode.restype = None
def DPxEnablePPxQuietFanMode():
    """ Enables the quiet fan mode on the PROPixx.
    
    Enabling this mode reduces the speed of the fans to reduce noise.
    Only available for PROPixx Revision 19 and higher.    
    
    :Low-level C definition:
        ``void DPxEnablePPxQuietFanMode(void)``
    """
    return enablePPxQuietFanMode()

 
# void DPxDisablePPxQuietFanMode(void)
disablePPxQuietFanMode = DPxDll['DPxDisablePPxQuietFanMode']
disablePPxQuietFanMode.restype = None 
def DPxDisablePPxQuietFanMode():
    """Disables the quiet fan mode on the PROPixx.
    
    Disabling this mode sets the fans to maximum speed, thus increasing the noise produced by them.
    Only available for PROPixx Revision 19 and higher.
    
    :Low-level C definition:
        ``void DPxDisablePPxQuietFanMode(void)``
    """
    return disablePPxQuietFanMode()


# int DPxIsPPxQuietFanMode(void)
isPPxQuietFanMode = DPxDll['DPxIsPPxQuietFanMode'] 
isPPxQuietFanMode.restype = ctypes.c_int
def DPxIsPPxQuietFanMode():
    """Check to see if the PROPixx quiet mode is enabled.
    
    Only available for PROPixx Revision 19 and higher.
    
    Returns:
        0 (False) if the PROPixx quiet mode is disabled, 1 (True) otherwise.
    
    :Low-level C definition:
        ``int DPxIsPPxQuietFanMode(void)``
    """
    return isPPxQuietFanMode()


setPPxAwake = DPxDll['DPxSetPPxAwake']
setPPxAwake.restype = None
def DPxSetPPxAwake():
    """Turns on the PROPixx.
    
    Only available for PROPixx Revision 12 and higher.
                    
    :Low-level C definition:
        ``void DPxSetPPxAwake()``
    """
    setPPxAwake()
    

setPPxSleep = DPxDll['DPxSetPPxSleep']
setPPxSleep.restype = None
def DPxSetPPxSleep():
    """Turns off the PROPixx.
    
    Only available for PROPixx Revision 12 and higher.
                    
    :Low-level C definition:
        ``void DPxSetPPxSleep()``
    """
    setPPxSleep()
    
        
# int DPxIsPPxAwake(void)
isPPxAwake = DPxDll['DPxIsPPxAwake'] 
isPPxAwake.restype = ctypes.c_int
def DPxIsPPxAwake():
    """Check to see if the PROPixx is awake.
    
    Returns:
        0 (False) if the PROPixx is in sleep mode, 1 (True) otherwise.
    
    :Low-level C definition:
        ``int DPxIsPPxAwake(void)``
    """
    return isPPxAwake()


# PROPixx Controller Rev >= 24 only
DPxEnableTxDviPassthru = DPxDll['DPxEnableTxDviPassthru']
DPxEnableTxDviPassthru.restype = None


# PROPixx Controller Rev >= 24 only
DPxDisableTxDviPassthru = DPxDll['DPxDisableTxDviPassthru']
DPxDisableTxDviPassthru.restype = None


# PROPixx Controller Rev >= 24 only
DPxIsTxDviPassthru = DPxDll['DPxIsTxDviPassthru']
DPxIsTxDviPassthru.restype = ctypes.c_int


DPxIsPPxAsyncResetEnabled = DPxDll['DPxIsPPxAsyncResetEnabled']
DPxIsPPxAsyncResetEnabled.restype = ctypes.c_int

DPxIsPPxPowerFloatEnabled = DPxDll['DPxIsPPxPowerFloatEnabled']
DPxIsPPxPowerFloatEnabled.restype = ctypes.c_int


SetCustomStartupConfig = DPxDll['DPxSetCustomStartupConfig']
SetCustomStartupConfig.restype = None
def DPxSetCustomStartupConfig():
    """Saves the current registers to be used on start up.
    
    This can be useful if you set your projector to ceiling mode or rear projection and you 
    want those settings to persist.
    
    Note:
        PROPixx Rev >= 6 only and VIEWPixx/PROPixxCTRL Rev >= 25 only
    
    :Low-level C definition:
        ``void DPxSetCustomStartupConfig(void)``    
    """
    return SetCustomStartupConfig()




setFactoryStartupConfig = DPxDll['DPxSetFactoryStartupConfig']
setFactoryStartupConfig.restype = None
def DPxSetFactoryStartupConfig():
    """Returns your device's configurable registers to their default state. This will reset all your customs setting such as
    rear projection. 
    
    :Low-level C definition:
        ``void DPxSetFactoryStartupConfig(void)``    
    """
    setFactoryStartupConfig()




IsCustomStartupConfig = DPxDll['DPxIsCustomStartupConfig']
IsCustomStartupConfig.restype = ctypes.c_int
def DPxIsCustomStartupConfig():
    """Returns True if VPixx device has loaded custom startup register values
    
    Note: 
        PROPixx Rev >= 8 only and VIEWPixx/PROPixxCTRL Rev >= 26 only

    :Low-level C definition:
        ``int DPxIsCustomStartupConfig(void)``
    """
    temp = DPxSpiRead(SPI_ADDR_VPX_REGDEF, 2)
    if (temp[0] == 255) and (temp[1] == 255):
        return False
    else:
        return True




EnableVidVesaFreeRun = DPxDll['DPxEnableVidVesaFreeRun']
EnableVidVesaFreeRun.restype = None
def DPxEnableVidVesaFreeRun():
    """Enables PROPixx 3D VESA output freeRun enable bit.
    
    Note:
        PROPixx Rev >= 7 only.
        
    :Low-level C definition:
        ``void DPxEnableVidVesaFreeRun(void)`` 
    """
    return EnableVidVesaFreeRun()




DisableVidVesaFreeRun = DPxDll['DPxDisableVidVesaFreeRun']
DisableVidVesaFreeRun.restype = None
def DPxDisableVidVesaFreeRun():
    """Disables PROPixx 3D VESA output freeRun enable bit
    
    Note:
        PROPixx Rev >= 7 only.
    
    :Low-level C definition:
        ``void DPxDisableVidVesaFreeRun(void)`` 
    """
    return DisableVidVesaFreeRun()




IsVidVesaFreeRun = DPxDll['DPxIsVidVesaFreeRun']
IsVidVesaFreeRun.restype = ctypes.c_int
def DPxIsVidVesaFreeRun():
    """Returns non-zero if PROPixx VESA 3D output is enabled.
    
    Note:
        PROPixx Rev >= 7 only.
        
    :Low-level C definition:
        ``int DPxIsVidVesaFreeRun(void)`` 
    """
    return IsVidVesaFreeRun()




EnableVidLcd3D60Hz = DPxDll['DPxEnableVidLcd3D60Hz']
EnableVidLcd3D60Hz.restype = None
def DPxEnableVidLcd3D60Hz():
    """Enables 3D pixel polarity inversion
    
    :Low-level C definition:
        ``void DPxEnableVidLcd3D60Hz(void)`` 
    """
    return EnableVidLcd3D60Hz()





DisableVidLcd3D60Hz = DPxDll['DPxDisableVidLcd3D60Hz']
DisableVidLcd3D60Hz.restype = None
def DPxDisableVidLcd3D60Hz():
    """Returns to normal pixel polarity inversion.
    
    :Low-level C definition:
        ``int DPxIsVidLcd3D60Hz(void)`` 
    """
    return DisableVidLcd3D60Hz()





IsVidLcd3D60Hz = DPxDll['DPxIsVidLcd3D60Hz']
IsVidLcd3D60Hz.restype = ctypes.c_int
def DPxIsVidLcd3D60Hz():
    """Returns non-zero if 3D pixel polarity inversion is enabled
    
    :Low-level C definition:
        ``int DPxIsVidLcd3D60Hz(void)`` 
    """
    return IsVidLcd3D60Hz()
 


'''
-If an API function detects an error, it will assign a unique error code to a global error variable.
This strategy permits DPxGet*() functions to conveniently return requested values directly,
and still make available a global error code which can be checked when desired.
'''
setError = DPxDll['DPxSetError']
setError.restype = None
def DPxSetError(errCode):
    """Sets the device to the given error code.
    
    Args:
        errCode (int): Given error code we wish to set the device to.
        
    :Low-level C definition:
        ``void DPxSetError(int error)`` 
    """
    if err.has_key(errCode):
        setError(err[errCode])

    






ClearError = DPxDll['DPxClearError']
ClearError.restype = None
def DPxClearError():
    """Clear any error on the device.
    
    :Low-level C definition:
        ``void DPxClearError()`` 
    """
    return ClearError()



"""
When using "disErr()" or " DPxGetError() ", the last detected error will be returned.
Note that if an error occured long before and wasn't cleared, that error will be returned.
There might not currently be an error, but it will still return an error. So it might be
necessary to clear previous if users want to test if there is an error.

example:

        DPx***() call
        if disErr() != 0:
            ...
        else:
            ...
        
    In that case, it might be better to do:
    
        DPxClearError()
        DPx***() call
        
        if disErr() != 0:
            ...
        else:
            ...

"""
getError= DPxDll['DPxGetError']
getError.restype = ctypes.c_int
def DPxGetError():
    """ Returns the error code
    
    Returns:
        Error code if an error occured, otherwise 0.

    :Low-level C definition:
        ``int DPxGetError()``         
    """
    errCode = getError()
    if err_return.has_key(errCode):
        return err_return[errCode]
    else :
        return 'Unknown Error'


GetErrorString = DPxDll['DPxGetErrorString']
GetErrorString.restype = ctypes.c_char_p
def DPxGetErrorString():
    """Returns the current error string
    
    Returns:
        Latest error string
        
    :Low-level C definition:
        ``const char* DPxGetErrorString()`` 
    """
    return GetErrorString()
    
    
    

GetDebug = DPxDll['DPxGetDebug']
GetDebug.restype = ctypes.c_int
def DPxGetDebug():
    """ Returns the current debug level
    
    Returns:
        Debug level
    
    :Low-level C definition:
        ``int DPxGetDebug()``  
    """
    return GetDebug()



SetDebug = DPxDll['DPxSetDebug']
SetDebug.restype = None
def DPxSetDebug(level):
    """Debugging level controls verbosity of debug and trace messages.
    
    Args:
        level (int): Set to ``0`` to disable messages, ``1`` to print libdpx, ``2``, to print libusb debug messages.
        
    :Low-level C definition:
        ``void DPxSetDebug(int level)``  
    """
    return SetDebug(level)



SaveRegs= DPxDll['DPxSaveRegs']
SaveRegs.restype = None
def DPxSaveRegs():
    """ Get all DATAPixx registers, and save them in a local copy
    
    :Low-level C definition:
        ``void DPxSaveRegs()``     
    """
    return SaveRegs()



RestoreRegs = DPxDll['DPxRestoreRegs']
RestoreRegs.restype = None
def DPxRestoreRegs():
    """Write the local copy back to the DATAPixx
    
    :Low-level C definition:
        ``void DPxRestoreRegs()`` 
    """
    return RestoreRegs()


# void        DPxStopAllScheds()
# Shortcut to stop running all DAC/ADC/DOUT/DIN/AUD/AUX/MIC schedules
StopAllScheds = DPxDll['DPxStopAllScheds']
StopAllScheds.restype = None
def DpxStopAllScheds():
    """Shortcut to stop running all DAC/ADC/DOUT/DIN/AUD/AUX/MIC schedules.
    
    :Low-level C definition:
        ``void DPxStopAllScheds()``  
    """
    return StopAllScheds()

# void DPxSetReg16(int regAddr, int regValue)
# Set a 16-bit register's value in dpRegisterCache[]
DPxSetReg16 = DPxDll['DPxSetReg16']
DPxSetReg16.restype = None

# DPxGetReg16(int regAddr);                        
# Read a 16-bit register's value from dpRegisterCache[]
DPxGetReg16 = DPxDll['DPxGetReg16']
DPxGetReg16.restype = ctypes.c_uint


# void DPxSetReg32(int regAddr, int regValue)
# Set a 32-bit register's value in dpRegisterCache[]
DPxSetReg32 = DPxDll['DPxSetReg16']
DPxSetReg32.restype = None


# DPxGetReg32(int regAddr);                        
# Read a 32-bit register's value from dpRegisterCache[]
DPxGetReg32 = DPxDll['DPxGetReg32']
DPxGetReg32.restype = ctypes.c_uint


# DPxGetRegSize(int regAddr);                        
# Returns the size of a register in bytes.
DPxGetRegSize = DPxDll['DPxGetRegSize']
DPxGetRegSize.restype = ctypes.c_uint

# void TPxSetBuff(unsigned buffAddr, unsigned buffSize);
SetBufferTracker = DPxDll['TPxSetBuff']
SetBufferTracker.restype = None
def TPxSetBuff(buffer_addres, buffer_size):
    """Shortcut to set up the the base address and buffer size for
    schedule recording of TRACKPixx data.
    
    """
    return SetBufferTracker(buffer_addres, buffer_size)

# void TPxEnableFreeRun();
TrackerEnableFreeRun = DPxDll['TPxEnableFreeRun']
TrackerEnableFreeRun.restype = None
def TPxEnableFreeRun():
    """Enable the schedule to automatically record all data
    
    """
    return TrackerEnableFreeRun()

# void TPxDisableFreeRun();
TrackerDisableFreeRun = DPxDll['TPxDisableFreeRun']
TrackerDisableFreeRun.restype = None
def TPxDisableFreeRun():
    """Disable the schedule to automatically record all data
    
    """
    return TrackerDisableFreeRun()

# unsigned TPxSaveToCsv(unsigned address);
TrackerSaveToCSV = DPxDll['TPxSaveToCsv']
TrackerSaveToCSV.restype = ctypes.c_uint32
def TPxSaveToCSV(last_read_address, fileName):
    """Save from last_read_address up to TPxGetReadAddr(), into the default file for today
    """
    
    return TrackerSaveToCSV(last_read_address, fileName)
# To be change: add filetype compatibility, because it will help the user save to its own file.

# void TPxGetEyePositionDuringCalib(float screen_x, float screen_y);
GetEyePositionDuringCalib = DPxDll['TPxGetEyePositionDuringCalib']
GetEyePositionDuringCalib.restype = None
def TPxGetEyePositionDuringCalib(x_screen, y_screen):
    #""" Tells the camera to get eye position now.
    #    
    #This function is to be called during calibration, when there is a focus point displayed on the stimulus display.
    #
    #Args:
    #    x_screen (float): x-coordinate of the stimulus
    #    y_screen (float): y-coordinate of the stimulus
    #Note:
    #    You (will be able to soon) to call this soon after stimulus is displayed (~500 ms after) since the tracker will wait for a fixation itself.
    # 
    # :Low-level C definition:
    #    ``void TPxGetEyePositionDuringCalib(float screen_x, float screen_y)``  
    #"""
    return GetEyePositionDuringCalib(x_screen, y_screen)

# void TPxFinishCalibration();
FinishCalibration_newPoly = DPxDll['TPxFinishCalibration_newPoly']
FinishCalibration_newPoly.restype = None
def TPxFinishCalibration_newPoly():
    #""" Finishes the calibration on the Device.
    #    
    #This function is to be called when you are done displaying stimuli for calibration. It will calculate the calibrations parameter
    #on the device and set the state to calibrated (which can be verified through ``isDeviceCalibrated``.
    #
    #:Low-level C definition:
    #    ``void TPxFinishCalibration()``  
    #"""
    return FinishCalibration_newPoly()

# void TPxFinishCalibration();
FinishCalibration = DPxDll['TPxFinishCalibration']
FinishCalibration.restype = None
def TPxFinishCalibration():
    #""" Finishes the calibration on the Device.
    #    
    #This function is to be called when you are done displaying stimuli for calibration. It will calculate the calibrations parameter
    #on the device and set the state to calibrated (which can be verified through ``isDeviceCalibrated``.
    #
    #:Low-level C definition:
    #    ``void TPxFinishCalibration()``  
    #"""
    return FinishCalibration()

# float* TPxGetEyePosition();
GetEyePosition = DPxDll['TPxGetEyePosition']
GetEyePosition.restype = ctypes.c_float
def TPxGetEyePosition(packed_data):
    #""" Returns the current gaze position.
    #
    #This returns the current calibrated gaze position on the screen using the calibration parameters found for the latest calibration. If you
    #would like to have un-calibrated data, you can call ``getRawEyePosition`` (not implemented yet).
    #
    #Returns:
    #    A list of gaze position, such that first element is screen_x_left_eye, screen_y_left_eye, screen_x_right_eye, screen_y_right_eye
    #    
    #:Example:
    #
    #>>> print my_device.getEyePosition()
    #[132, 152, 131, 152]
    #    
    #See also:
    #    :class:`getRawEyePosition`
    #
    #:Low-level C definition:
    #    ``float* TPxGetEyePosition()``  
    #"""
    return GetEyePosition(packed_data)

# TPxGetEyePosition_newPoly();
GetEyePosition_newPoly = DPxDll['TPxGetEyePosition_newPoly']
GetEyePosition_newPoly.restype = None
def TPxGetEyePosition_newPoly(packed_data):
    #""" Returns the current gaze position.
    #
    #This returns the current calibrated gaze position on the screen using the calibration parameters found for the latest calibration. If you
    #would like to have un-calibrated data, you can call ``getRawEyePosition`` (not implemented yet).
    #
    #Returns:
    #    A list of gaze position, such that first element is screen_x_left_eye, screen_y_left_eye, screen_x_right_eye, screen_y_right_eye
    #    
    #:Example:
    #
    #>>> print my_device.getEyePosition()
    #[132, 152, 131, 152]
    #    
    #See also:
    #    :class:`getRawEyePosition`
    #
    #:Low-level C definition:
    #    ``float* TPxGetEyePosition()``  
    #"""
    return GetEyePosition_newPoly(packed_data)
 
# void TPxFinishCalibration();
FinishCalibration_new = DPxDll['TPxFinishCalibration_new']
FinishCalibration_new.restype = None
def TPxFinishCalibration_new():
    #""" Finishes the calibration on the Device.
    #    
    #This function is to be called when you are done displaying stimuli for calibration. It will calculate the calibrations parameter
    #on the device and set the state to calibrated (which can be verified through ``isDeviceCalibrated``.
    #
    #:Low-level C definition:
    #    ``void TPxFinishCalibration()``  
    #"""
    return FinishCalibration_new()

# float* TPxGetEyePosition();
GetEyePosition_new = DPxDll['TPxGetEyePosition_new']
GetEyePosition_new.restype = ctypes.c_float
def TPxGetEyePosition_new(packed_data):
    #""" Returns the current gaze position.
    #
    #This returns the current calibrated gaze position on the screen using the calibration parameters found for the latest calibration. If you
    #would like to have un-calibrated data, you can call ``getRawEyePosition`` (not implemented yet).
    #
    #Returns:
    #    A list of gaze position, such that first element is screen_x_left_eye, screen_y_left_eye, screen_x_right_eye, screen_y_right_eye
    #    
    #:Example:
    #
    #>>> print my_device.getEyePosition()
    #[132, 152, 131, 152]
    #    
    #See also:
    #    :class:`getRawEyePosition`
    #
    #:Low-level C definition:
    #    ``float* TPxGetEyePosition()``  
    #"""
    return GetEyePosition_new(packed_data)   

# float* TPxGetEyePosition_newPoly();
BestPolyGetEyePosition = DPxDll['TPxBestPolyGetEyePosition']
BestPolyGetEyePosition.restype = None
def TPxBestPolyGetEyePosition(packed_data):
    return BestPolyGetEyePosition(packed_data)

# void TPxFinishCalibration();
BestPolyFinishCalibration = DPxDll['TPxBestPolyFinishCalibration']
BestPolyFinishCalibration.restype = None
def TPxBestPolyFinishCalibration():
    #""" Finishes the calibration on the Device.
    #    
    #This function is to be called when you are done displaying stimuli for calibration. It will calculate the calibrations parameter
    #on the device and set the state to calibrated (which can be verified through ``isDeviceCalibrated``.
    #
    #:Low-level C definition:
    #    ``void TPxFinishCalibration()``  
    #"""
    return BestPolyFinishCalibration()

# int TPxIsDeviceCalibrated();
IsDeviceCalibrated = DPxDll['TPxIsDeviceCalibrated']
IsDeviceCalibrated.restye = ctypes.c_int
def TPxIsDeviceCalibrated():
    #""" Returns the calibrated state of the tracker.
    #    
    #Returns:
    #    True when tracked has been successfully calibrated, false otherwise.
    #    
    #:Low-level C definition:
    #    ``int TPxIsDeviceCalibrated()``  
    #"""
    return IsDeviceCalibrated()



getVidSwtpAddr = DPxDll['DPxGetVidSwtpAddr']
getVidSwtpAddr.restye = ctypes.c_int
def DPxGetVidSwtpAddr():
    return getVidSwtpAddr()



setVidSwtp = DPxDll['DPxSetVidSwtp']
setVidSwtp.argtypes = [ctypes.c_int]
setVidSwtp.restye = None
def DPxSetVidSwtp(address):
    setVidSwtp(address)


setVidSwtp3D = DPxDll['DPxSetVidSwtp3D']
setVidSwtp3D.argtypes = [ctypes.c_int]
setVidSwtp3D.restye = None
def DPxSetVidSwtp3D(address):
    setVidSwtp3D(address)


# void PPxDownloadTestPattern(unsigned char testPattern[1920][1080][3], int loadAddr, int page)
def PPxLoadTestPattern(image, add, page):
    """ Loads an image in the PROPixx since the PROPixx is different for software test patterns.
    :param image:
    :param add:
    :param page:
    """
    
    class image_conv(ctypes.Structure):
        _fields_ = [("array", (ctypes.c_ubyte * 3) * 1920 * 1080)]
    loadTestPattern = DPxDll['PPxDownloadTestPattern']
    loadTestPattern.argtypes = [ctypes.POINTER(image_conv), ctypes.c_int, ctypes.c_int ]
    loadTestPattern.restype = None
    
    image_c = image_conv()
    #image_c.array = image
    for i in range(0,3):
        for x in range(0, 1920):
            for y in range(0, 1080):
                image_c.array[y][x][i] = int(image[y][x][i])
    loadTestPattern(image_c, add, page)
    
loadTestPattern = DPxDll['DPxSetPPxHotSpotLut']
loadTestPattern.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_uint16)]
loadTestPattern.restype = None   
def DPxSetPPxHotSpotLut(x, y, psi):
    """
    
    :param x:
    :param y:
    :param psi:
    """
    item_count = len(psi)
    packed_data = (ctypes.c_uint16 * item_count)(*psi)
    
    loadTestPattern(x,y, packed_data)
    
#void DPxEnablePPxHotSpotCorrection()
EnablePPxHotSpotCorrection = DPxDll['DPxEnablePPxHotSpotCorrection']
EnablePPxHotSpotCorrection.argtypes = None
EnablePPxHotSpotCorrection.restype = None
def DPxEnablePPxHotSpotCorrection():
    """
    
    """
    EnablePPxHotSpotCorrection()
    
DisablePPxHotSpotCorrection = DPxDll['DPxDisablePPxHotSpotCorrection']
DisablePPxHotSpotCorrection.argtypes = None
DisablePPxHotSpotCorrection.restype = None
def DPxDisablePPxHotSpotCorrection():
    """
    
    """
    DisablePPxHotSpotCorrection()
    
SetPPxHotSpotCenter = DPxDll['DPxSetPPxHotSpotCenter']
SetPPxHotSpotCenter.argtypes = [ctypes.c_int, ctypes.c_int]
SetPPxHotSpotCenter.restypes = None
def DPxSetPPxHotSpotCenter(x,y):
    """ Sets the hotspot correction location only.
    
    Arguments:
        x (int): The position in x from the center, + to the left.
        y (int): The position in y from the center, + to the bottom.
    """
    SetPPxHotSpotCenter(x,y)
        

IsPPxHotSpotCorrection = DPxDll['DPxIsPPxHotSpotCorrection']
IsPPxHotSpotCorrection.argtypes = None
IsPPxHotSpotCorrection.restype = ctypes.c_int
def DPxIsPPxHotSpotCorrection():
    """
    
    """
    return IsPPxHotSpotCorrection()    
    
#void DPxGetPPxHotSpotCenter(int *x, int *y)
GetPPxHotSpotCenter = DPxDll['DPxGetPPxHotSpotCenter']
GetPPxHotSpotCenter.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
GetPPxHotSpotCenter.restype = None
def DPxGetPPxHotSpotCenter():
    """
    
    """
    p_x = ctypes.c_int(0)
    p_y = ctypes.c_int(0)
    GetPPxHotSpotCenter(ctypes.byref(p_x), ctypes.byref(p_y))
    return (p_x.value, p_y.value)


getBacklightIntensity = DPxDll['DPxGetVidBacklightIntensity']
def DPxGetVidBacklightIntensity():
    """ Returns the display current back light intensity.
    
    Returns:
        An integer between 0 and 255.
                
    :Example:
    
    >>> print my_device.getBacklightIntensity()
    255
        
    See also:
        :class:`DPxSetBacklightIntensity`
    
    :Low-level C definition:
        ``int DPxGetVidBacklightIntensity()``  
    """
    return getBacklightIntensity()
    
    

setBacklightIntensity = DPxDll['DPxSetVidBacklightIntensity']
setBacklightIntensity.argtypes = [ctypes.c_int]
setBacklightIntensity.restye = None
def DPxSetVidBacklightIntensity(intensity):
    """Sets the display current back light intensity.
    
    Args:
        intensity (int): Set to ``0`` for the lowest intensity level, ``255`` for the highest, or any other value in between.
    
    :Example:
    
    >>> my_device.setBacklightIntensity(42)
    >>> my_device.updateRegisterCache()
    >>> print my_device.getBacklightIntensity()
    42
    
    See also:
        :class:`DPxGetBacklightIntensity`
            
    :Low-level C definition:
        ``void DPxSetBacklightIntensity(int intensity)``  
    """
    setBacklightIntensity(intensity)
    
# Returns non-zero if there is a custom edid.    
DPxIsCustomEdid = DPxDll['DPxIsCustomEdid']
DPxIsCustomEdid.restype = ctypes.c_int


hasRawUsb = DPxDll['DPxHasRawUsb'] 
hasRawUsb.restype = ctypes.c_int
def DPxHasRawUsb():
    # The low-level also sometimes returns an address. In that case, the value is
    # Non-Zero, but the USB is not Raw. So when the return value is higher than
    # 2^15, it could be an address. It should be safe safe to assume that the function
    # will never reach that value when a raw usb is detected.
    temp_value = hasRawUsb()
    if temp_value > 32768:
        temp_value = 0
    return temp_value
    
    
isUsbTreeChanged = DPxDll['DPxIsUsbTreeChanged'] 
isUsbTreeChanged.restype = ctypes.c_int
def DPxIsUsbTreeChanged():
    return isUsbTreeChanged()


usbScan = DPxDll['DPxUsbScan'] 
usbScan.restype = None#ctypes.c_int
def DPxUsbScan(print_info=0):
    usbScan(print_info)
    
    
reset = DPxDll['DPxReset'] 
reset.restype = None
def DPxReset():
    reset()
    

resetAll = DPxDll['DPxResetAll'] 
resetAll.restype = None
def DPxResetAll():
    resetAll()
    
"""
This section provides the list of all predefined constants.
"""
api_constants = {'AUTO': -1,
                 'CRYSTALEYES':0x10,
                 'C48': 3,
                 'C36D': 7,
                 'C24': 0,
                 'DEPTH Q':0x40, 
                 'DIFF': 1, 
                 'DPX_REG_SPACE': 480,
                 'GREY3X': 0x90,
                 'GND' : 0,
                 'HZ': 0,
                 'LEFT': 0x10,
                 'LINE' : 2,
                 'LR': 0,
                 'L48': 1,
                 'L48D': 5,
                 'M16': 2,
                 'M16O': 2,
                 'MIC': 1,
                 'MONO': 0,
                 'M16D': 6,
                 'NANO': 32,
                 'NVIDIA': 0x20,
                 'PPXREG_VID_SEQ_CSR_PGRM_RGB':0,  #Default RGB 120Hz
                 'QUAD4X': 0x20,
                 'QUAD12X': 0x50,
                 'RAW': -2,
                 'RB24': 8,
                 'RB3D': 0x10,
                 'RGB': 0,
                 'RGB240': 0x30,
                 'RGB180': 0x40,
                 'REF0': 2,
                 'REF1': 3,
                 'RIGHT': 0x20,
                 'STEREO': 0x30,
                 'UNCONFIGURED': 0,
                 'DATAPIXX': 10,
                 'VIEWPIXX': 20,
                 'VIEWPIXX3D': 20,
                 'VIEWPIXXEEG': 20,
                 'PROPIXXCTRL': 30,
                 'PROPIXX': 40,
                 'DATAPIXX2': 50,
                 'TRACKPIXX': 60,
                 'TRACKPIXX_C': 70,
                 'TRACKPIXX_B': 80,
                 'VIDEO': 16,
                 }


adc_channel_reference = {0 : 'GND',
                         1 : 'DIFF', 
                         2 : 'REF0',
                         3 : 'REF1'
                         }
                         
rate_constants = {0x00: 'HZ',
                  0x10: 'VIDEO', 
                  0x20: 'NANO'
                  }
                        
mic_mode_constants = {0x00: 'mono',
                      0x10: 'left', 
                      0x20: 'right',
                      0x30: 'stereo'
                      }

audio_mode_constants = {0x00: 'mono',
                        0x100: 'left', 
                        0x200: 'right',
                        0x300: 'stereo1',
                        0x400: 'stereo2',
                        }

video_mode_constants = {1: 'L48',
                        2: 'M16',
                        3: 'C48',
                        5: 'L48D',
                        6: 'M16D',
                        7: 'C36D',
                        0: 'C24',
                        8: 'RB24'
                        }

propixx_sequencer_constants = {0x00: 'RGB',
                               0x10: 'RB3D',
                               0x20: 'QUAD4X',
                               0x50: 'QUAD12X'                               
                               }

vesa_mode_constants = {0x00: 'LR',
                       0x10: 'CRYSTALEYES',
                       0x20: 'NVIDIA',
                       0x40: 'PPX_DEPTHQ'                               
                       }

part_number_constants = {0x1000: 'DATAPixx LITE',
                         0x1001: 'DATAPixx FULL',
                         0x2000: 'VIEWPixx LITE',
                         0x2001: 'VIEWPixx FULL',
                         0x2004: 'VIEWPixx3D LITE',
                         0x2005: 'VIEWPixx3D FULL',
                         0x2006: 'VIEWPixxEEG', 
                         0x5068: 'PROPixx Ctrl LITE',
                         0x5069: 'PROPixx Ctrl FULL',
                         0x5050: 'PROPixx',     
                         0x1002: 'DATAPixx2 LITE',
                         0x1003: 'DATAPixx2 FULL'
                         }

test_pattern_constants = {'MASK': 0xF000,
                          'C24': 0,
                          'DVI': 0x0000,
                          'LVDS': 0x1000,
                          'SWTP': 0x4000,
                          'SWTP 3D': 0x5000,
                          'RGB SQUARES': 0x8000,
                          'GRAY': 0x9000,
                          'BAR': 0xA000,
                          'BAR2': 0xB000,
                          'DOTS': 0xC000,
                          'DOTS1': 0xC000 + 0x4E1,
                          'DOTS2': 0xC000 + 0x4D1,
                          'DOTS PPX': 0xC000 + 0xAF0,
                          'RAMP': 0xD000,
                          'RGB': 0xE000,
                          'PROJ': 0xF000
                          }

DPXREG_SCHED_CTRL_RATE_HZ = 0 # rateValue is updates per second, maximum 96 kHz
DPXREG_SCHED_CTRL_RATE_XVID = 16 # rateValue is updates per video frame, maximum 96 kHz
DPXREG_SCHED_CTRL_RATE_NANO = 32 # rateValue is update period in nanoseconds, minimum 10417 ns

DPXREG_ADC_CHANREF_GND =  0 # Referenced to ground
DPXREG_ADC_CHANREF_DIFF = 1 # Referenced to adjacent analog input 
DPXREG_ADC_CHANREF_REF0 = 2 # Referenced to REF0 analog input
DPXREG_ADC_CHANREF_REF1 = 3 # Referenced to REF1 analog input

DPXREG_AUD_CTRL_LRMODE_MONO =     0x0000  # Each AUD schedule datum goes to left and right channels
DPXREG_AUD_CTRL_LRMODE_LEFT =     0x0100  # Each AUD schedule datum goes to left channel only
DPXREG_AUD_CTRL_LRMODE_RIGHT =    0x0200  # Each AUD schedule datum goes to right channel only
DPXREG_AUD_CTRL_LRMODE_STEREO_1 = 0x0300 # Pairs of AUD data are copied to left/right channels 
DPXREG_AUD_CTRL_LRMODE_STEREO_2 = 0x0400 # AUD data goes to left channel, AUX data goes to right

PPX_POWER_5V   = 0x0000
PPX_POWER_2P5V = 0x0001
PPX_POWER_1P8V = 0x0002
PPX_POWER_1P5V = 0x0003
PPX_POWER_1P1V = 0x0004
PPX_POWER_1V   = 0x0005
PPX_POWER_12V  = 0x0006

PPX_TEMP_LED_RED        = 0x0000
PPX_TEMP_LED_GRN        = 0x0001      
PPX_TEMP_LED_BLU        = 0x0002
PPX_TEMP_LED_ALT        = 0x0003
PPX_TEMP_DMD            = 0x0004
PPX_TEMP_POWER_BOARD    = 0x0005
PPX_TEMP_LED_POWER_BOAD = 0x0006
PPX_TEMP_RX_DVI         = 0x0007
PPX_TEMP_FPGA           = 0x0008
PPX_TEMP_FPGA2          = 0x0009


PPX_LED_DAC_RED_L = 0x0000 
PPX_LED_DAC_RED_H = 0x0001 
PPX_LED_DAC_GRN_L = 0x0002 
PPX_LED_DAC_GRN_H = 0x0003 
PPX_LED_DAC_BLU_L = 0x0004 
PPX_LED_DAC_BLU_H = 0x0005

PPX_FAN_TACH_1 = 0x0000
PPX_FAN_TACH_2 = 0x0001
PPX_FAN_TACH_3 = 0x0002
PPX_FAN_TACH_4 = 0x0003
PPX_FAN_TACH_5 = 0x0004
PPX_FAN_TACH_6 = 0x0005

DPXREG_VID_SRC_MASK = 0xF000
DPXREG_VID_SRC_DVI  = 0x0000
DPXREG_VID_SRC_LVDS = 0x1000
DPXREG_VID_SRC_SWTP = 0x4000
DPXREG_VID_SRC_SWTP_3D = 0x5000
DPXREG_VID_SRC_HWTP_RGB_SQUARES = 0x8000
DPXREG_VID_SRC_HWTP_GRAY = 0x9000
DPXREG_VID_SRC_HWTP_DRIFTING_BAR = 0xA000
DPXREG_VID_SRC_HWTP_DRIFTING_BAR2 = 0xB000
DPXREG_VID_SRC_HWTP_DRIFTING_DOTS = 0xC000
DPXREG_VID_SRC_HWTP_DRIFTING_RAMP = 0xD000
DPXREG_VID_SRC_HWTP_RGB = 0xE000
DPXREG_VID_SRC_HWTP_PROJ = 0xF000
DPXREG_SCHED_CTRL_LOG_TOUCHPIXX = 2097152 # 0x00200000 
DPXREG_SCHED_CTRL_LOG_EVENTS  = 1048576 # 0x00100000
DPXREG_SCHED_CTRL_LOG_TIMETAG = 65536   # 0x00010000
DPXREG_SCHED_CTRL_COUNTDOWN = 256     # 0x00000100
DPXREG_SCHED_CTRL_RATE_MASK = 48      # 0x00000030
DPXREG_SCHED_CTRL_RATE_XVID = 16      # 0x00000010
DPXREG_SCHED_CTRL_RATE_NANO = 32      # 0x00000020
DPXREG_SCHED_CTRL_RUNNING = 1       # 0x00000001
DPXREG_VID_LCD_TIMING = 0x1A6
DPXREG_VID_BL_INTENSITY = 0x1A8
DPXREG_VID_VPERIOD_L = 0x180
DPXREG_VID_VPERIOD_H = 0x182
DPXREG_VID_HTOTAL  = 0x184
DPXREG_VID_VTOTAL  = 0x186
DPXREG_VID_HACTIVE = 0x188
DPXREG_VID_VACTIVE = 0x18A
DPXREG_VID_CLK_CTRL = 0x18C
DPXREG_VID_STATUS = 0x18E
DPXREG_VID_CTRL2  = 0x1A0
DPXREG_VID_CTRL   = 0x19E
DPXREG_VID_CTRL_NATIVE100HZ      = 0x4000
DPXREG_VID_CTRL2_EEG_BRIGHT_MODE = 0x0040  
DPXREG_VID_CTRL2_NO_EXTPOL      = 0x0020
DPXREG_VID_CTRL2_NO_VLOCK_LAMP  = 0x0010
DPXREG_VID_CTRL2_NO_VLOCK       = 0x0008
DPXREG_VID_CTRL2_NO_VCALIB      = 0x0004
DPXREG_VID_CTRL2_NO_VDITH       = 0x0002
DPXREG_VID_CTRL2_NO_HDITH       = 0x0001
DPXREG_VID_CTRL2_PIXELDRIVE       = 0x8000
DPXREG_VID_CTRL2_PIXELDRIVE_ACCUM = 0x4000
DPXREG_VID_CTRL2_PIXELDRIVE_ACCUM2 = 0x2000
DPXREG_VID_CTRL2_LCD_3D60HZ = 0x0800
DPXREG_VID_CTRL2_TX_DVI_1080P = 0x0100
DPXREG_VID_BL_SCAN_CTRL = 0x1AE
DPXREG_VID_STATUS_DVI_AUTO_3D_MODE  = 0x1000
DPXREG_VID_STATUS_DVI_DIRECT_ACTIVE = 0x0800
DPXREG_VID_STATUS_DVI_STRETCH_DE = 0x0400
DPXREG_VID_STATUS_DVI_LOCKABLE = 0x0200
DPXREG_VID_STATUS_LCD_HIFREQ = 0x0100
DPXREG_VID_STATUS_SLEEP = 0x0008
DPXREG_VID_STATUS_TURBO = 0x0004
DPXREG_VID_STATUS_DVI_ACTIVE_DUAL = 0x0002
DPXREG_VID_STATUS_DVI_ACTIVE = 0x0001
DPXREG_VID_BL_POWER_FAULT = 0x80
DPXREG_VID_BL_POWER_CTRL = 0x1AC
DPXREG_STATS0  = 0x1C0
DPXREG_STATS1  = 0x1C2
DPXREG_STATS2  = 0x1C4
DPXREG_STATS3  = 0x1C6
DPXREG_STATS4  = 0x1C8
DPXREG_STATS5  = 0x1CA
DPXREG_STATS6  = 0x1CC
DPXREG_STATS7  = 0x1CE
DPXREG_DDR_CSR = 0x1DC
PPXREG_SLEEP   = 0x0A
PPXREG_SLEEP_AWAKE_STATUS = 0x4
PPX_TEMP_LED_POWER_BOARD  = 6
PPXREG_TEMP_STATUS = 0x2E

PPXREG_SLEEP_LAMP_LED_ON_STATUS  = 0x20
PPXREG_SLEEP_LAMP_LED_OFF    = 0x10
PPXREG_SLEEP_LAMP_LED_ON    = 0x8
PPXREG_SLEEP_GOTO_SLEEP  = 0x2
PPXREG_SLEEP_GOTO_AWAKE  = 0x1
PPXREG_TEMP_LED_GRN_RED  = 0x20
PPXREG_TEMP_LED_ALT_BLU  = 0x22
PPXREG_TEMP_DMD_POW   = 0x24
PPXREG_TEMP_RX_DVI_LED_POW_BD  = 0x26
PPXREG_TEMP_DDC4100_FPGA    = 0x28
PPXREG_TEMP_VOLTAGE_MONITOR    = 0x2A
PPXREG_TEMP_UNUSED   = 0x2C
PPXREG_POWER_FIRST   = 0x30
PPXREG_POWER_5V    = 0x30
PPXREG_POWER_2P5V  = 0x32
PPXREG_POWER_1P8V  = 0x34
PPXREG_POWER_1P5V  = 0x36
PPXREG_POWER_1P1V  = 0x38
PPXREG_POWER_1P0V  = 0x3A
PPXREG_POWER_12V   = 0x3C
PPXREG_FAN_CONFIG   = 0x40
PPXREG_FAN_CONFIG_PWM   = 0x00FF
PPXREG_FAN_CONFIG_IDLE_PWM  = 0xFF00
PPXREG_FAN_TACH_1_2   = 0x42
PPXREG_FAN_TACH_3_4   = 0x44
PPXREG_FAN_TACH_5_6   = 0x46
PPXREG_FAN_CONFIG2   = 0x48
PPXREG_FAN_CONFIG2_FAN_QUIET_MODE  = 0x0001
PPXREG_TSCOPE_BUFF_BASEPAGE   = 0x120
PPXREG_TSCOPE_BUFF_NPAGES     = 0x122
PPXREG_TSCOPE_CSR  = 0x12E
PPXREG_TSCOPE_CSR_PREP_ACK  = 0x0020
PPXREG_TSCOPE_CSR_PREP_REQ  = 0x0010
PPXREG_TSCOPE_CSR_EN    = 0x0001
PPXREG_TSCOPE_SCHED_ONSET_L   = 0x130  # Delay between schedule start and first TACH update tick, in nanoseconds
PPXREG_TSCOPE_SCHED_ONSET_H   = 0x132
PPXREG_TSCOPE_SCHED_RATE_L    = 0x134  # Tick rate in ticks/second or ticks/frame, or tick period in nanoseconds
PPXREG_TSCOPE_SCHED_RATE_H    = 0x136
PPXREG_TSCOPE_SCHED_COUNT_L   = 0x138  # Tick counter
PPXREG_TSCOPE_SCHED_COUNT_H   = 0x13A
PPXREG_TSCOPE_SCHED_CTRL_L    = 0x13C  # Bits are defined in DPXREG_DAC_SCHED_CTRL register
PPXREG_TSCOPE_SCHED_CTRL_H    = 0x13E
PPXREG_3D_CROSSTALK_RED_LR    = 0x140
PPXREG_3D_CROSSTALK_RED_RL    = 0x142
PPXREG_3D_CROSSTALK_GRN_LR    = 0x144
PPXREG_3D_CROSSTALK_GRN_RL    = 0x146
PPXREG_3D_CROSSTALK_BLU_LR    = 0x148
PPXREG_3D_CROSSTALK_BLU_RL    = 0x14A
PPXREG_0x14C  = 0x14C
PPXREG_0x14E  = 0x14E
PPXREG_HS_CTRL     = 0x150
PPXREG_HS_CTRL_CORRECTION_EN  = 0x0001
PPXREG_HS_CTRL_SPI_LUT_FOUND  = 0x0002
PPXREG_HS_CTRL_SPI_CENTER_FOUND  = 0x0004
PPXREG_HS_CENTER_X_COORD    = 0x152
PPXREG_HS_CENTER_Y_COORD    = 0x154
PPXREG_0x156  = 0x156
PPXREG_0x158  = 0x158
PPXREG_0x15A  = 0x15A
PPXREG_0x15C = 0x15C
PPXREG_0x15E  = 0x15E
PPXREG_VID_DDC_CFG   = 0x160
PPXREG_VID_DDC_CFG_PATGEN     = 0xFF00
PPXREG_VID_DDC_CFG_ARST     = 0x0080
PPXREG_VID_DDC_CFG_PWR_FLOAT  = 0x0040
PPXREG_VID_DDC_CFG_WDT_EN     = 0x0020
PPXREG_VID_DDC_CFG_ROWADD_MODE  = 0x0010
PPXREG_VID_DDC_CFG_NS_FLIP_EN   = 0x0008
PPXREG_VID_DDC_CFG_COMP_DATA_EN = 0x0004
PPXREG_VID_DDC_CFG_CNT_HALT   = 0x0002
PPXREG_VID_DDC_CFG_DDC_FLOAT  = 0x0001
PPXREG_VID_MIRROR_TIME  = 0x162
PPXREG_VID_MIRROR_TIME_SETTLING   = 0xFF00
PPXREG_VID_MIRROR_TIME_RESET_ACTIVE = 0x00FF
PPXREG_3D_CROSSTALK_LR    = 0x164
PPXREG_3D_CROSSTALK_RL    = 0x166
PPXREG_3D_CROSSTALK     = 0x168
PPXREG_VID_INTENSITY    = 0x16A
PPXREG_VID_SEQ_PERIOD     = 0x16C
PPXREG_VID_SEQ_CSR      = 0x16E
PPXREG_VID_SEQ_CSR_STATUS     = 0xFF00
PPXREG_VID_SEQ_CSR_PGRM_MASK  = 0x00F0  # Only bit 4 is used for now
PPXREG_VID_SEQ_CSR_PGRM_CUSTOM  = 0x00F0  # Custom USB uploaded
PPXREG_VID_SEQ_CSR_PGRM_RGB   = 0x0000  # Default RGB 120Hz
PPXREG_VID_SEQ_CSR_PGRM_RB3D  = 0x0010  # R/B channels drive grayscale 3D
PPXREG_VID_SEQ_CSR_PGRM_QUAD4X  = 0x0020  # 4 display quadrants are projected at 4x refresh rate
PPXREG_VID_SEQ_CSR_PGRM_RGB240  = 0x0030  # RGB 240Hz
PPXREG_VID_SEQ_CSR_PGRM_RGB180  = 0x0040  # RGB 180Hz
PPXREG_VID_SEQ_CSR_PGRM_QUAD12X = 0x0050  # 4 display quadrants are projected at 12x refresh rate with grayscales
PPXREG_VID_SEQ_CSR_EN       = 0x0001
PPXREG_LED_DAC_RED_L    = 0x170
PPXREG_LED_DAC_RED_H    = 0x172
PPXREG_LED_DAC_GRN_L    = 0x174
PPXREG_LED_DAC_GRN_H    = 0x176
PPXREG_LED_DAC_BLU_L    = 0x178
PPXREG_LED_DAC_BLU_H    = 0x17A
PPXREG_LED_DAC_ALT_L    = 0x17C
PPXREG_LED_DAC_ALT_H    = 0x17E
PPX_POWER_5V = 0
PPX_POWER_2P5V     =  1
PPX_POWER_1P8V     =  2
PPX_POWER_1P5V     =  3
PPX_POWER_1P1V     =  4
PPX_POWER_1V  = 5
PPX_POWER_12V     =  6
PPX_TEMP_LED_RED  = 0
PPX_TEMP_LED_GRN  = 1
PPX_TEMP_LED_BLU   = 2
PPX_TEMP_LED_ALT   = 3
PPX_TEMP_DMD = 4
PPX_TEMP_POWER_BOARD  = 5
PPX_TEMP_LED_POWER_BOARD  = 6
PPX_TEMP_RX_DVI     =  7
PPX_TEMP_FPGA = 8
PPX_TEMP_FPGA2 = 9
PPX_LED_DAC_RED_L  =  0
PPX_LED_DAC_RED_H  =  1
PPX_LED_DAC_GRN_L  =  2
PPX_LED_DAC_GRN_H       =  3
PPX_LED_DAC_BLU_L  =   4
PPX_LED_DAC_BLU_H  =   5
PPX_LED_DAC_ALT_L  =   6
PPX_LED_DAC_ALT_H  =   7
PPX_FAN_TACH_1 = 0
PPX_FAN_TACH_2 = 1
PPX_FAN_TACH_3 = 2
PPX_FAN_TACH_4 = 3
PPX_FAN_TACH_5 = 4
PPX_FAN_TACH_6 = 5
PPX_SEQ_CMD_FLASH_START = 0x1000
PPX_SEQ_CMD_FLASH_WAIT  = 0x2000
PPX_SEQ_CMD_FLASH_STOP  = 0x3000
PPX_SEQ_CMD_DDC_LOAD  = 0x4000
PPX_SEQ_CMD_DDC_CLEAR   = 0x5000
PPX_SEQ_CMD_DDC_RESET   = 0x6000
PPX_SEQ_CMD_TIMER_START = 0x7000
PPX_SEQ_CMD_TIMER_WAIT  = 0x8000
PPX_SEQ_CMD_EOP = 0xF000
DPX_DAC_NCHANS  = 4
DPX_ADC_NCHANS  = 16
DPX_MIC_SRC_UNKNOWN  =  0
DPX_MIC_SRC_MIC_IN   = 1
DPX_MIC_SRC_LINE_IN   = 2
DPX_VID  = 0x04b4
DPX_PID  = 0x4450
DPX_DID  = 0x0000
VPX_PID  = 0x5650
PPX_PID  = 0x5050
PCX_PID  = 0x5043
DP2_PID  = 0x4432
TPX_PID = 0x5450


NBR_VPIXX_DEV = 4 
DATAPIXX = 1
DATAPIXX2 = 5
VIEWPIXX = 2
PROPIXX_CTR = 3
PROPIXX = 4

SPI_ADDR_DPX_FPGA   = 0x010000
SPI_ADDR_DPX_TEXT   = 0x1F0000
SPI_ADDR_DPX_EDID   = 0x3E0000
SPI_ADDR_DPX_ANALOG = 0x3F0000
SPI_ADDR_VPX_FPGA   = 0x000000
SPI_ADDR_FULL_SS    = 0x6D0000
SPI_ADDR_LITE_SS    = 0x730000
SPI_ADDR_VPX_REGDEF = 0x790000
SPI_ADDR_PPX_LEDCAL = 0x7A0000
SPI_ADDR_VPX_LEDCUR = 0x7B0000
SPI_ADDR_VPX_VCALIB = 0x7C0000
SPI_ADDR_VPX_ANALOG = 0x7D0000
SPI_ADDR_PPX_HS_LUT = 0x7D0000
SPI_ADDR_PPX_HS_POS = 0x7D6000
SPI_ADDR_VPX_EDID   = 0x7E0000
SPI_ADDR_VPX_TEXT   = 0x7F0000
SPI_ADDR_PPX_DDD    = 0x300000
SPI_ADDR_PPX_SS     = 0x400000
SPI_ADDR_PPX_LEDMAXD65 = (SPI_ADDR_PPX_LEDCAL + 0x0000)
SPI_ADDR_PPX_LEDMAXCUR = (SPI_ADDR_PPX_LEDCAL + 0xFF00)

err = {'DPX_SUCCESS':0,
'DPX_FAIL':-1,
'DPX_ERR_USB_NO_DATAPIXX':-1000,
'DPX_ERR_USB_RAW_EZUSB':-1001,
'DPX_ERR_USB_RAW_FPGA':-1002,
'DPX_ERR_USB_OPEN':-1003,
'DPX_ERR_USB_OPEN_FPGA':-1004,
'DPX_ERR_USB_SET_CONFIG':-1005,
'DPX_ERR_USB_CLAIM_INTERFACE':-1006,
'DPX_ERR_USB_ALT_INTERFACE':-1007,
'DPX_ERR_USB_UNKNOWN_DPID':-1008,
'DPX_ERR_USB_REG_BULK_WRITE':-1009,
'DPX_ERR_USB_REG_BULK_READ':-1010,
'DPX_ERR_USB_DEVSEL_INDEX':-1011,
'DPX_ERR_USB_SYSDEVSEL_INDEX':-1012,
'DPX_ERR_SPI_START':-1100,
'DPX_ERR_SPI_STOP':-1101,
'DPX_ERR_SPI_READ':-1102,
'DPX_ERR_SPI_WRITE':-1103,
'DPX_ERR_SPI_ERASE':-1104,
'DPX_ERR_SPI_WAIT_DONE':-1105,
'DPX_ERR_SETREG16_ADDR_ODD':-1200,
'DPX_ERR_SETREG16_ADDR_RANGE':-1201,
'DPX_ERR_SETREG16_DATA_RANGE':-1202,
'DPX_ERR_GETREG16_ADDR_ODD':-1203,
'DPX_ERR_GETREG16_ADDR_RANGE':-1204,
'DPX_ERR_SETREG32_ADDR_ALIGN':-1205,
'DPX_ERR_SETREG32_ADDR_RANGE':-1206,
'DPX_ERR_GETREG32_ADDR_ALIGN':-1207,
'DPX_ERR_GETREG32_ADDR_RANGE':-1208,
'DPX_ERR_NANO_MARK_NULL_PTR':-1301,
'DPX_ERR_NANO_TIME_NULL_PTR':-1300,
'DPX_ERR_UNKNOWN_PART_NUMBER':-1302,
'DPX_ERR_RAM_UNKNOWN_SIZE':-1400,
'DPX_ERR_RAM_WRITEREAD_FAIL':-1401,
'DPX_ERR_RAM_WRITE_ADDR_ODD':-1402,
'DPX_ERR_RAM_WRITE_LEN_ODD':-1403,
'DPX_ERR_RAM_WRITE_TOO_HIGH':-1404,
'DPX_ERR_RAM_WRITE_BUFFER_NULL':-1405,
'DPX_ERR_RAM_WRITE_USB_ERROR':-1406,
'DPX_ERR_RAM_READ_ADDR_ODD':-1407,
'DPX_ERR_RAM_READ_LEN_ODD':-1408,
'DPX_ERR_RAM_READ_TOO_HIGH':-1409,
'DPX_ERR_RAM_READ_BUFFER_NULL':-1410,
'DPX_ERR_RAM_READ_USB_ERROR':-1411,
'DPX_ERR_DAC_SET_BAD_CHANNEL':-1500,
'DPX_ERR_DAC_SET_BAD_VALUE':-1501,
'DPX_ERR_DAC_GET_BAD_CHANNEL':-1502,
'DPX_ERR_DAC_RANGE_NULL_PTR':-1503,
'DPX_ERR_DAC_RANGE_BAD_CHANNEL':-1504,
'DPX_ERR_DAC_BUFF_BAD_CHANNEL':-1505,
'DPX_ERR_DAC_BUFF_ODD_BASEADDR':-1506,
'DPX_ERR_DAC_BUFF_BASEADDR_TOO_HIGH':-1507,
'DPX_ERR_DAC_BUFF_ODD_READADDR':-1508,
'DPX_ERR_DAC_BUFF_READADDR_TOO_HIGH':-1509,
'DPX_ERR_DAC_BUFF_ODD_WRITEADDR':-1510,
'DPX_ERR_DAC_BUFF_WRITEADDR_TOO_HIGH':-1511,
'DPX_ERR_DAC_BUFF_ODD_SIZE':-1512,
'DPX_ERR_DAC_BUFF_TOO_BIG':-1513,
'DPX_ERR_DAC_SCHED_TOO_FAST':-1514,
'DPX_ERR_DAC_SCHED_BAD_RATE_UNITS':-1515,
'DPX_ERR_ADC_GET_BAD_CHANNEL':-1600,
'DPX_ERR_ADC_RANGE_NULL_PTR':-1601,
'DPX_ERR_ADC_RANGE_BAD_CHANNEL':-1602,
'DPX_ERR_ADC_REF_BAD_CHANNEL':-1603,
'DPX_ERR_ADC_BAD_CHAN_REF':-1604,
'DPX_ERR_ADC_BUFF_BAD_CHANNEL':-1605,
'DPX_ERR_ADC_BUFF_ODD_BASEADDR':-1606,
'DPX_ERR_ADC_BUFF_BASEADDR_TOO_HIGH':-1607,
'DPX_ERR_ADC_BUFF_ODD_READADDR':-1608,
'DPX_ERR_ADC_BUFF_READADDR_TOO_HIGH':-1609,
'DPX_ERR_ADC_BUFF_ODD_WRITEADDR':-1610,
'DPX_ERR_ADC_BUFF_WRITEADDR_TOO_HIGH':-1611,
'DPX_ERR_ADC_BUFF_ODD_SIZE':-1612,
'DPX_ERR_ADC_BUFF_TOO_BIG':-1613,
'DPX_ERR_ADC_SCHED_TOO_FAST':-1614,
'DPX_ERR_ADC_SCHED_BAD_RATE_UNITS':-1615,
'DPX_ERR_DOUT_SET_BAD_MASK':-1700,
'DPX_ERR_DOUT_BUFF_ODD_BASEADDR':-1701,
'DPX_ERR_DOUT_BUFF_BASEADDR_TOO_HIGH':-1702,
'DPX_ERR_DOUT_BUFF_ODD_READADDR':-1703,
'DPX_ERR_DOUT_BUFF_READADDR_TOO_HIGH':-1704,
'DPX_ERR_DOUT_BUFF_ODD_WRITEADDR':-1705,
'DPX_ERR_DOUT_BUFF_WRITEADDR_TOO_HIGH':-1706,
'DPX_ERR_DOUT_BUFF_ODD_SIZE':-1707,
'DPX_ERR_DOUT_BUFF_TOO_BIG':-1708,
'DPX_ERR_DOUT_SCHED_TOO_FAST':-1709,
'DPX_ERR_DOUT_SCHED_BAD_RATE_UNITS':-1710,
'DPX_ERR_DIN_SET_BAD_MASK':-1800,
'DPX_ERR_DIN_BUFF_ODD_BASEADDR':-1801,
'DPX_ERR_DIN_BUFF_BASEADDR_TOO_HIGH':-1802,
'DPX_ERR_DIN_BUFF_ODD_READADDR':-1803,
'DPX_ERR_DIN_BUFF_READADDR_TOO_HIGH':-1804,
'DPX_ERR_DIN_BUFF_ODD_WRITEADDR':-1805,
'DPX_ERR_DIN_BUFF_WRITEADDR_TOO_HIGH':-1806,
'DPX_ERR_DIN_BUFF_ODD_SIZE':-1807,
'DPX_ERR_DIN_BUFF_TOO_BIG':-1808,
'DPX_ERR_DIN_SCHED_TOO_FAST':-1809,
'DPX_ERR_DIN_SCHED_BAD_RATE_UNITS':-1810,
'DPX_ERR_DIN_BAD_STRENGTH':-1811,
'DPX_ERR_AUD_SET_BAD_VALUE':-1900,
'DPX_ERR_AUD_SET_BAD_VOLUME':-1901,
'DPX_ERR_AUD_SET_BAD_LRMODE':-1902,
'DPX_ERR_AUD_BUFF_ODD_BASEADDR':-1903,
'DPX_ERR_AUD_BUFF_BASEADDR_TOO_HIGH':-1904,
'DPX_ERR_AUD_BUFF_ODD_READADDR':-1905,
'DPX_ERR_AUD_BUFF_READADDR_TOO_HIGH':-1906,
'DPX_ERR_AUD_BUFF_ODD_WRITEADDR':-1907,
'DPX_ERR_AUD_BUFF_WRITEADDR_TOO_HIGH':-1908,
'DPX_ERR_AUD_BUFF_ODD_SIZE':-1909,
'DPX_ERR_AUD_BUFF_TOO_BIG':-1910,
'DPX_ERR_AUX_BUFF_ODD_BASEADDR':-1911,
'DPX_ERR_AUX_BUFF_BASEADDR_TOO_HIGH':-1912,
'DPX_ERR_AUX_BUFF_ODD_READADDR':-1913,
'DPX_ERR_AUX_BUFF_READADDR_TOO_HIGH':-1914,
'DPX_ERR_AUX_BUFF_ODD_WRITEADDR':-1915,
'DPX_ERR_AUX_BUFF_WRITEADDR_TOO_HIGH':-1916,
'DPX_ERR_AUX_BUFF_ODD_SIZE':-1917,
'DPX_ERR_AUX_BUFF_TOO_BIG':-1918,
'DPX_ERR_AUD_SCHED_TOO_FAST':-1919,
'DPX_ERR_AUD_SCHED_TOO_SLOW':-1920,
'DPX_ERR_AUD_SCHED_BAD_RATE_UNITS':-1921,
'DPX_ERR_AUD_CODEC_POWERUP':-1922,
'DPX_ERR_MIC_SET_GAIN_TOO_LOW':-2000,
'DPX_ERR_MIC_SET_GAIN_TOO_HIGH':-2001,
'DPX_ERR_MIC_SET_BAD_SOURCE':-2002,
'DPX_ERR_MIC_SET_BAD_LRMODE':-2003,
'DPX_ERR_MIC_BUFF_ODD_BASEADDR':-2004,
'DPX_ERR_MIC_BUFF_BASEADDR_TOO_HIGH':-2005,
'DPX_ERR_MIC_BUFF_ODD_READADDR':-2006,
'DPX_ERR_MIC_BUFF_READADDR_TOO_HIGH':-2007,
'DPX_ERR_MIC_BUFF_ODD_WRITEADDR':-2008,
'DPX_ERR_MIC_BUFF_WRITEADDR_TOO_HIGH':-2009,
'DPX_ERR_MIC_BUFF_ODD_SIZE':-2010,
'DPX_ERR_MIC_BUFF_TOO_BIG':-2011,
'DPX_ERR_MIC_SCHED_TOO_FAST':-2012,
'DPX_ERR_MIC_SCHED_BAD_RATE_UNITS':-2013,
'DPX_ERR_VID_SET_BAD_MODE':-2100,
'DPX_ERR_VID_CLUT_WRITE_USB_ERROR':-2101,
'DPX_ERR_VID_VSYNC_USB_ERROR':-2102,
'DPX_ERR_VID_EDID_WRITE_USB_ERROR':-2103,
'DPX_ERR_VID_LINE_READ_USB_ERROR':-2104,
'DPX_ERR_VID_PSYNC_NPIXELS_ARG_ERROR':-2105,
'DPX_ERR_VID_PSYNC_TIMEOUT_ARG_ERROR':-2106,
'DPX_ERR_VID_PSYNC_LINE_ARG_ERROR':-2107,
'DPX_ERR_VID_ALPHA_WRITE_USB_ERROR':-2108,
'DPX_ERR_VID_BASEADDR_ALIGN_ERROR':-2109,
'DPX_ERR_VID_BASEADDR_TOO_HIGH':-2110,
'DPX_ERR_VID_VSYNC_WITHOUT_VIDEO':-2111,
'DPX_ERR_VID_BL_INTENSITY_ARG_ERROR':-2112,
'DPX_ERR_PPX_BAD_VOLTAGE':-3000,
'DPX_ERR_PPX_BAD_TEMP':-3001,
'DPX_ERR_PPX_BAD_LED':-3002,
'DPX_ERR_PPX_BAD_FAN':-3003,
'DPX_ERR_PPX_BAD_LED_CURRENT':-3004,
'DPX_ERR_PPX_SEQ_WRITE_USB_ERROR':-3005}

err_return = {0:'DPX_SUCCESS',
-1:'DPX_FAIL',
-1000:'DPX_ERR_USB_NO_DATAPIXX',
-1001:'DPX_ERR_USB_RAW_EZUSB',
-1002:'DPX_ERR_USB_RAW_FPGA',
-1003:'DPX_ERR_USB_OPEN',
-1004:'DPX_ERR_USB_OPEN_FPGA',
-1005:'DPX_ERR_USB_SET_CONFIG',
-1006:'DPX_ERR_USB_CLAIM_INTERFACE',
-1007:'DPX_ERR_USB_ALT_INTERFACE',
-1008:'DPX_ERR_USB_UNKNOWN_DPID',
-1009:'DPX_ERR_USB_REG_BULK_WRITE',
-1010:'DPX_ERR_USB_REG_BULK_READ',
-1011:'DPX_ERR_USB_DEVSEL_INDEX',
-1012:'DPX_ERR_USB_SYSDEVSEL_INDEX',
-1100:'DPX_ERR_SPI_START',
-1101:'DPX_ERR_SPI_STOP',
-1102:'DPX_ERR_SPI_READ',
-1103:'DPX_ERR_SPI_WRITE',
-1104:'DPX_ERR_SPI_ERASE',
-1105:'DPX_ERR_SPI_WAIT_DONE',
-1200:'DPX_ERR_SETREG16_ADDR_ODD',
-1201:'DPX_ERR_SETREG16_ADDR_RANGE',
-1202:'DPX_ERR_SETREG16_DATA_RANGE',
-1203:'DPX_ERR_GETREG16_ADDR_ODD',
-1204:'DPX_ERR_GETREG16_ADDR_RANGE',
-1205:'DPX_ERR_SETREG32_ADDR_ALIGN',
-1206:'DPX_ERR_SETREG32_ADDR_RANGE',
-1207:'DPX_ERR_GETREG32_ADDR_ALIGN',
-1208:'DPX_ERR_GETREG32_ADDR_RANGE',
-1301:'DPX_ERR_NANO_MARK_NULL_PTR',
-1300:'DPX_ERR_NANO_TIME_NULL_PTR',
-1302:'DPX_ERR_UNKNOWN_PART_NUMBER',
-1400:'DPX_ERR_RAM_UNKNOWN_SIZE',
-1401:'DPX_ERR_RAM_WRITEREAD_FAIL',
-1402:'DPX_ERR_RAM_WRITE_ADDR_ODD',
-1403:'DPX_ERR_RAM_WRITE_LEN_ODD',
-1404:'DPX_ERR_RAM_WRITE_TOO_HIGH',
-1405:'DPX_ERR_RAM_WRITE_BUFFER_NULL',
-1406:'DPX_ERR_RAM_WRITE_USB_ERROR',
-1407:'DPX_ERR_RAM_READ_ADDR_ODD',
-1408:'DPX_ERR_RAM_READ_LEN_ODD',
-1409:'DPX_ERR_RAM_READ_TOO_HIGH',
-1410:'DPX_ERR_RAM_READ_BUFFER_NULL',
-1411:'DPX_ERR_RAM_READ_USB_ERROR',
-1500:'DPX_ERR_DAC_SET_BAD_CHANNEL',
-1501:'DPX_ERR_DAC_SET_BAD_VALUE',
-1502:'DPX_ERR_DAC_GET_BAD_CHANNEL',
-1503:'DPX_ERR_DAC_RANGE_NULL_PTR',
-1504:'DPX_ERR_DAC_RANGE_BAD_CHANNEL',
-1505:'DPX_ERR_DAC_BUFF_BAD_CHANNEL',
-1506:'DPX_ERR_DAC_BUFF_ODD_BASEADDR',
-1507:'DPX_ERR_DAC_BUFF_BASEADDR_TOO_HIGH',
-1508:'DPX_ERR_DAC_BUFF_ODD_READADDR',
-1509:'DPX_ERR_DAC_BUFF_READADDR_TOO_HIGH',
-1510:'DPX_ERR_DAC_BUFF_ODD_WRITEADDR',
-1511:'DPX_ERR_DAC_BUFF_WRITEADDR_TOO_HIGH',
-1512:'DPX_ERR_DAC_BUFF_ODD_SIZE',
-1513:'DPX_ERR_DAC_BUFF_TOO_BIG',
-1514:'DPX_ERR_DAC_SCHED_TOO_FAST',
-1515:'DPX_ERR_DAC_SCHED_BAD_RATE_UNITS',
-1600:'DPX_ERR_ADC_GET_BAD_CHANNEL',
-1601:'DPX_ERR_ADC_RANGE_NULL_PTR',
-1602:'DPX_ERR_ADC_RANGE_BAD_CHANNEL',
-1603:'DPX_ERR_ADC_REF_BAD_CHANNEL',
-1604:'DPX_ERR_ADC_BAD_CHAN_REF',
-1605:'DPX_ERR_ADC_BUFF_BAD_CHANNEL',
-1606:'DPX_ERR_ADC_BUFF_ODD_BASEADDR',
-1607:'DPX_ERR_ADC_BUFF_BASEADDR_TOO_HIGH',
-1608:'DPX_ERR_ADC_BUFF_ODD_READADDR',
-1609:'DPX_ERR_ADC_BUFF_READADDR_TOO_HIGH',
-1610:'DPX_ERR_ADC_BUFF_ODD_WRITEADDR',
-1611:'DPX_ERR_ADC_BUFF_WRITEADDR_TOO_HIGH',
-1612:'DPX_ERR_ADC_BUFF_ODD_SIZE',
-1613:'DPX_ERR_ADC_BUFF_TOO_BIG',
-1614:'DPX_ERR_ADC_SCHED_TOO_FAST',
-1615:'DPX_ERR_ADC_SCHED_BAD_RATE_UNITS',
-1700:'DPX_ERR_DOUT_SET_BAD_MASK',
-1701:'DPX_ERR_DOUT_BUFF_ODD_BASEADDR',
-1702:'DPX_ERR_DOUT_BUFF_BASEADDR_TOO_HIGH',
-1703:'DPX_ERR_DOUT_BUFF_ODD_READADDR',
-1704:'DPX_ERR_DOUT_BUFF_READADDR_TOO_HIGH',
-1705:'DPX_ERR_DOUT_BUFF_ODD_WRITEADDR',
-1706:'DPX_ERR_DOUT_BUFF_WRITEADDR_TOO_HIGH',
-1707:'DPX_ERR_DOUT_BUFF_ODD_SIZE',
-1708:'DPX_ERR_DOUT_BUFF_TOO_BIG',
-1709:'DPX_ERR_DOUT_SCHED_TOO_FAST',
-1710:'DPX_ERR_DOUT_SCHED_BAD_RATE_UNITS',
-1800:'DPX_ERR_DIN_SET_BAD_MASK',
-1801:'DPX_ERR_DIN_BUFF_ODD_BASEADDR',
-1802:'DPX_ERR_DIN_BUFF_BASEADDR_TOO_HIGH',
-1803:'DPX_ERR_DIN_BUFF_ODD_READADDR',
-1804:'DPX_ERR_DIN_BUFF_READADDR_TOO_HIGH',
-1805:'DPX_ERR_DIN_BUFF_ODD_WRITEADDR',
-1806:'DPX_ERR_DIN_BUFF_WRITEADDR_TOO_HIGH',
-1807:'DPX_ERR_DIN_BUFF_ODD_SIZE',
-1808:'DPX_ERR_DIN_BUFF_TOO_BIG',
-1809:'DPX_ERR_DIN_SCHED_TOO_FAST',
-1810:'DPX_ERR_DIN_SCHED_BAD_RATE_UNITS',
-1811:'DPX_ERR_DIN_BAD_STRENGTH',
-1900:'DPX_ERR_AUD_SET_BAD_VALUE',
-1901:'DPX_ERR_AUD_SET_BAD_VOLUME',
-1902:'DPX_ERR_AUD_SET_BAD_LRMODE',
-1903:'DPX_ERR_AUD_BUFF_ODD_BASEADDR',
-1904:'DPX_ERR_AUD_BUFF_BASEADDR_TOO_HIGH',
-1905:'DPX_ERR_AUD_BUFF_ODD_READADDR',
-1906:'DPX_ERR_AUD_BUFF_READADDR_TOO_HIGH',
-1907:'DPX_ERR_AUD_BUFF_ODD_WRITEADDR',
-1908:'DPX_ERR_AUD_BUFF_WRITEADDR_TOO_HIGH',
-1909:'DPX_ERR_AUD_BUFF_ODD_SIZE',
-1910:'DPX_ERR_AUD_BUFF_TOO_BIG',
-1911:'DPX_ERR_AUX_BUFF_ODD_BASEADDR',
-1912:'DPX_ERR_AUX_BUFF_BASEADDR_TOO_HIGH',
-1913:'DPX_ERR_AUX_BUFF_ODD_READADDR',
-1914:'DPX_ERR_AUX_BUFF_READADDR_TOO_HIGH',
-1915:'DPX_ERR_AUX_BUFF_ODD_WRITEADDR',
-1916:'DPX_ERR_AUX_BUFF_WRITEADDR_TOO_HIGH',
-1917:'DPX_ERR_AUX_BUFF_ODD_SIZE',
-1918:'DPX_ERR_AUX_BUFF_TOO_BIG',
-1919:'DPX_ERR_AUD_SCHED_TOO_FAST',
-1920:'DPX_ERR_AUD_SCHED_TOO_SLOW',
-1921:'DPX_ERR_AUD_SCHED_BAD_RATE_UNITS',
-1922:'DPX_ERR_AUD_CODEC_POWERUP',
-2000:'DPX_ERR_MIC_SET_GAIN_TOO_LOW',
-2001:'DPX_ERR_MIC_SET_GAIN_TOO_HIGH',
-2002:'DPX_ERR_MIC_SET_BAD_SOURCE',
-2003:'DPX_ERR_MIC_SET_BAD_LRMODE',
-2004:'DPX_ERR_MIC_BUFF_ODD_BASEADDR',
-2005:'DPX_ERR_MIC_BUFF_BASEADDR_TOO_HIGH',
-2006:'DPX_ERR_MIC_BUFF_ODD_READADDR',
-2007:'DPX_ERR_MIC_BUFF_READADDR_TOO_HIGH',
-2008:'DPX_ERR_MIC_BUFF_ODD_WRITEADDR',
-2009:'DPX_ERR_MIC_BUFF_WRITEADDR_TOO_HIGH',
-2010:'DPX_ERR_MIC_BUFF_ODD_SIZE',
-2011:'DPX_ERR_MIC_BUFF_TOO_BIG',
-2012:'DPX_ERR_MIC_SCHED_TOO_FAST',
-2013:'DPX_ERR_MIC_SCHED_BAD_RATE_UNITS',
-2100:'DPX_ERR_VID_SET_BAD_MODE',
-2101:'DPX_ERR_VID_CLUT_WRITE_USB_ERROR',
-2102:'DPX_ERR_VID_VSYNC_USB_ERROR',
-2103:'DPX_ERR_VID_EDID_WRITE_USB_ERROR',
-2104:'DPX_ERR_VID_LINE_READ_USB_ERROR',
-2105:'DPX_ERR_VID_PSYNC_NPIXELS_ARG_ERROR',
-2106:'DPX_ERR_VID_PSYNC_TIMEOUT_ARG_ERROR',
-2107:'DPX_ERR_VID_PSYNC_LINE_ARG_ERROR',
-2108:'DPX_ERR_VID_ALPHA_WRITE_USB_ERROR',
-2109:'DPX_ERR_VID_BASEADDR_ALIGN_ERROR',
-2110:'DPX_ERR_VID_BASEADDR_TOO_HIGH',
-2111:'DPX_ERR_VID_VSYNC_WITHOUT_VIDEO',
-2112:'DPX_ERR_VID_BL_INTENSITY_ARG_ERROR',
-3000:'DPX_ERR_PPX_BAD_VOLTAGE',
-3001:'DPX_ERR_PPX_BAD_TEMP',
-3002:'DPX_ERR_PPX_BAD_LED',
-3003:'DPX_ERR_PPX_BAD_FAN',
-3004:'DPX_ERR_PPX_BAD_LED_CURRENT',
-3005:'DPX_ERR_PPX_SEQ_WRITE_USB_ERROR'};


detailed_error = {
    'DPX_SUCCESS':'Function executed successfully',
    'DPX_FAIL':'Generic failure code',
    'DPX_ERR_USB_NO_DATAPIXX':'No DATAPixx was found',
    'DPX_ERR_USB_RAW_EZUSB':'EZ-USB appears to have no firmware',
    'DPX_ERR_USB_RAW_FPGA':'FPGA appears to be unconfigured',
    'DPX_ERR_USB_OPEN':'An error occurred while opening a USB channel',
    'DPX_ERR_USB_OPEN_FPGA':'An FPGA detection error occurred while opening DATAPixx',
    'DPX_ERR_USB_SET_CONFIG':'Could not set the USB configuration',
    'DPX_ERR_USB_CLAIM_INTERFACE':'Could not claim the USB interface',
    'DPX_ERR_USB_ALT_INTERFACE':'Could not set the USB alternate interface',
    'DPX_ERR_USB_UNKNOWN_DPID':'Unrecognized DATAPixx ID register value',
    'DPX_ERR_USB_REG_BULK_WRITE':'USB error while writing register set',
    'DPX_ERR_USB_REG_BULK_READ':'USB error while reading register set',
    'DPX_ERR_USB_DEVSEL_INDEX':'Illegal device index',
    'DPX_ERR_USB_SYSDEVSEL_INDEX':'Illegal system device index',
    'DPX_ERR_SPI_START':'SPI communication startup error',
    'DPX_ERR_SPI_STOP':'SPI communication termination error',
    'DPX_ERR_SPI_READ':'SPI communication read error',
    'DPX_ERR_SPI_WRITE':'SPI communication write error',
    'DPX_ERR_SPI_ERASE':'SPI communication erase error',
    'DPX_ERR_SPI_WAIT_DONE':'SPI communication error while waiting for SPI write to complete',
    'DPX_ERR_SETREG16_ADDR_ODD':'DPxSetReg16 passed an odd address',
    'DPX_ERR_SETREG16_ADDR_RANGE':'DPxSetReg16 passed an address which was out of range',
    'DPX_ERR_SETREG16_DATA_RANGE':'DPxSetReg16 passed a datum which was out of range',
    'DPX_ERR_GETREG16_ADDR_ODD':'DPxGetReg16 passed an odd address',
    'DPX_ERR_GETREG16_ADDR_RANGE':'DPxGetReg16 passed an address which was out of range',
    'DPX_ERR_SETREG32_ADDR_ALIGN':'DPxSetReg32 passed an address which was not 32-bit aligned',
    'DPX_ERR_SETREG32_ADDR_RANGE':'DPxSetReg32 passed an address which was out of range',
    'DPX_ERR_GETREG32_ADDR_ALIGN':'DPxGetReg32 passed an address which was not 32-bit aligned',
    'DPX_ERR_GETREG32_ADDR_RANGE':'DPxGetReg32 passed an address which was out of range',
    'DPX_ERR_NANO_TIME_NULL_PTR':'A pointer argument was null',
    'DPX_ERR_NANO_MARK_NULL_PTR':'A pointer argument was null',
    'DPX_ERR_UNKNOWN_PART_NUMBER':'Unrecognized part number',
    'DPX_ERR_RAM_UNKNOWN_SIZE':'Unrecognized RAM configuration',
    'DPX_ERR_RAM_WRITEREAD_FAIL':'RAM read did not return same value written',
    'DPX_ERR_RAM_WRITE_ADDR_ODD':'RAM write buffer address must be even',
    'DPX_ERR_RAM_WRITE_LEN_ODD':'RAM write buffer length must be even',
    'DPX_ERR_RAM_WRITE_TOO_HIGH':'RAM write block exceeds end of DATAPixx memory',
    'DPX_ERR_RAM_WRITE_BUFFER_NULL':'RAM write source buffer pointer is null',
    'DPX_ERR_RAM_WRITE_USB_ERROR':'A USB error occurred while writing the RAM buffer',
    'DPX_ERR_RAM_READ_ADDR_ODD':'RAM read buffer address must be even',
    'DPX_ERR_RAM_READ_LEN_ODD':'RAM read buffer length must be even',
    'DPX_ERR_RAM_READ_TOO_HIGH':'RAM read block exceeds end of DATAPixx memory',
    'DPX_ERR_RAM_READ_BUFFER_NULL':'RAM read destination buffer pointer is null',
    'DPX_ERR_RAM_READ_USB_ERROR':'A USB error occurred while reading the RAM buffer',
    'DPX_ERR_DAC_SET_BAD_CHANNEL':'Valid channels are 0-3',
    'DPX_ERR_DAC_SET_BAD_VALUE':'Value falls outside DAC''s output range',
    'DPX_ERR_DAC_GET_BAD_CHANNEL':'Valid channels are 0-3',
    'DPX_ERR_DAC_RANGE_NULL_PTR':'A pointer argument was null',
    'DPX_ERR_DAC_RANGE_BAD_CHANNEL':'Valid channels are 0-3',
    'DPX_ERR_DAC_BUFF_BAD_CHANNEL':'Valid channels are 0-3',
    'DPX_ERR_DAC_BUFF_ODD_BASEADDR':'An odd buffer base was requested',
    'DPX_ERR_DAC_BUFF_BASEADDR_TOO_HIGH':'The requested buffer is larger than the DATAPixx RAM',
    'DPX_ERR_DAC_BUFF_ODD_READADDR':'An odd buffer read address was requested',
    'DPX_ERR_DAC_BUFF_READADDR_TOO_HIGH':'The requested read address exceeds the DATAPixx RAM',
    'DPX_ERR_DAC_BUFF_ODD_WRITEADDR':'An odd buffer write address was requested',
    'DPX_ERR_DAC_BUFF_WRITEADDR_TOO_HIGH':'The requested write address exceeds the DATAPixx RAM',
    'DPX_ERR_DAC_BUFF_ODD_SIZE':'An odd buffer size was requested',
    'DPX_ERR_DAC_BUFF_TOO_BIG':'The requested buffer is larger than the DATAPixx RAM',
    'DPX_ERR_DAC_SCHED_TOO_FAST':'The requested schedule rate is too fast',
    'DPX_ERR_DAC_SCHED_BAD_RATE_UNITS':'Unnrecognized schedule rate units parameter',
    'DPX_ERR_ADC_GET_BAD_CHANNEL':'Valid channels are 0-17',
    'DPX_ERR_ADC_RANGE_NULL_PTR':'A pointer argument was null',
    'DPX_ERR_ADC_RANGE_BAD_CHANNEL':'Valid channels are 0-17',
    'DPX_ERR_ADC_REF_BAD_CHANNEL':'Valid channels are 0-15',
    'DPX_ERR_ADC_BAD_CHAN_REF':'Unrecognized channel reference parameter',
    'DPX_ERR_ADC_BUFF_BAD_CHANNEL':'Valid channels are 0-15',
    'DPX_ERR_ADC_BUFF_ODD_BASEADDR':'An odd buffer base was requested',
    'DPX_ERR_ADC_BUFF_BASEADDR_TOO_HIGH':'The requested buffer is larger than the DATAPixx RAM',
    'DPX_ERR_ADC_BUFF_ODD_READADDR':'An odd buffer read address was requested',
    'DPX_ERR_ADC_BUFF_READADDR_TOO_HIGH':'The requested read address exceeds the DATAPixx RAM',
    'DPX_ERR_ADC_BUFF_ODD_WRITEADDR':'An odd buffer write address was requested',
    'DPX_ERR_ADC_BUFF_WRITEADDR_TOO_HIGH':'The requested write address exceeds the DATAPixx RAM',
    'DPX_ERR_ADC_BUFF_ODD_SIZE':'An odd buffer size was requested',
    'DPX_ERR_ADC_BUFF_TOO_BIG':'The requested buffer is larger than the DATAPixx RAM',
    'DPX_ERR_ADC_SCHED_TOO_FAST':'The requested schedule rate is too fast',
    'DPX_ERR_ADC_SCHED_BAD_RATE_UNITS':'Unnrecognized schedule rate units parameter',
    'DPX_ERR_DOUT_SET_BAD_MASK':'Valid masks set bits 23 downto 0',
    'DPX_ERR_DOUT_BUFF_ODD_BASEADDR':'An odd buffer base was requested',
    'DPX_ERR_DOUT_BUFF_BASEADDR_TOO_HIGH':'The requested buffer is larger than the DATAPixx RAM',
    'DPX_ERR_DOUT_BUFF_ODD_READADDR':'An odd buffer read address was requested',
    'DPX_ERR_DOUT_BUFF_READADDR_TOO_HIGH':'The requested read address exceeds the DATAPixx RAM',
    'DPX_ERR_DOUT_BUFF_ODD_WRITEADDR':'An odd buffer write address was requested',
    'DPX_ERR_DOUT_BUFF_WRITEADDR_TOO_HIGH':'The requested write address exceeds the DATAPixx RAM',
    'DPX_ERR_DOUT_BUFF_ODD_SIZE':'An odd buffer size was requested',
    'DPX_ERR_DOUT_BUFF_TOO_BIG':'The requested buffer is larger than the DATAPixx RAM',
    'DPX_ERR_DOUT_SCHED_TOO_FAST':'The requested schedule rate is too fast',
    'DPX_ERR_DOUT_SCHED_BAD_RATE_UNITS':'Unnrecognized schedule rate units parameter',
    'DPX_ERR_DIN_SET_BAD_MASK':'Valid masks set bits 23 downto 0',
    'DPX_ERR_DIN_BUFF_ODD_BASEADDR':'An odd buffer base was requested',
    'DPX_ERR_DIN_BUFF_BASEADDR_TOO_HIGH':'The requested buffer is larger than the DATAPixx RAM',
    'DPX_ERR_DIN_BUFF_ODD_READADDR':'An odd buffer read address was requested',
    'DPX_ERR_DIN_BUFF_READADDR_TOO_HIGH':'The requested read address exceeds the DATAPixx RAM',
    'DPX_ERR_DIN_BUFF_ODD_WRITEADDR':'An odd buffer write address was requested',
    'DPX_ERR_DIN_BUFF_WRITEADDR_TOO_HIGH':'The requested write address exceeds the DATAPixx RAM',
    'DPX_ERR_DIN_BUFF_ODD_SIZE':'An odd buffer size was requested',
    'DPX_ERR_DIN_BUFF_TOO_BIG':'The requested buffer is larger than the DATAPixx RAM',
    'DPX_ERR_DIN_SCHED_TOO_FAST':'The requested schedule rate is too fast',
    'DPX_ERR_DIN_SCHED_BAD_RATE_UNITS':'Unnrecognized schedule rate units parameter',
    'DPX_ERR_DIN_BAD_STRENGTH':'Strength is in the range 0-1',
    'DPX_ERR_AUD_SET_BAD_VALUE':'Value falls outside AUD''s output range',
    'DPX_ERR_AUD_SET_BAD_VOLUME':'Valid volumes are in the range 0-1',
    'DPX_ERR_AUD_SET_BAD_LRMODE':'See DPxSetAudLRMode() for valid values',
    'DPX_ERR_AUD_BUFF_ODD_BASEADDR':'An odd buffer base was requested',
    'DPX_ERR_AUD_BUFF_BASEADDR_TOO_HIGH':'The requested buffer is larger than the DATAPixx RAM',
    'DPX_ERR_AUD_BUFF_ODD_READADDR':'An odd buffer read address was requested',
    'DPX_ERR_AUD_BUFF_READADDR_TOO_HIGH':'The requested read address exceeds the DATAPixx RAM',
    'DPX_ERR_AUD_BUFF_ODD_WRITEADDR':'An odd buffer write address was requested',
    'DPX_ERR_AUD_BUFF_WRITEADDR_TOO_HIGH':'The requested write address exceeds the DATAPixx RAM',
    'DPX_ERR_AUD_BUFF_ODD_SIZE':'An odd buffer size was requested',
    'DPX_ERR_AUD_BUFF_TOO_BIG':'The requested buffer is larger than the DATAPixx RAM',
    'DPX_ERR_AUX_BUFF_ODD_BASEADDR':'An odd buffer base was requested',
    'DPX_ERR_AUX_BUFF_BASEADDR_TOO_HIGH':'The requested buffer is larger than the DATAPixx RAM',
    'DPX_ERR_AUX_BUFF_ODD_READADDR':'An odd buffer read address was requested',
    'DPX_ERR_AUX_BUFF_READADDR_TOO_HIGH':'The requested read address exceeds the DATAPixx RAM',
    'DPX_ERR_AUX_BUFF_ODD_WRITEADDR':'An odd buffer write address was requested',
    'DPX_ERR_AUX_BUFF_WRITEADDR_TOO_HIGH':'The requested write address exceeds the DATAPixx RAM',
    'DPX_ERR_AUX_BUFF_ODD_SIZE':'An odd buffer size was requested',
    'DPX_ERR_AUX_BUFF_TOO_BIG':'The requested buffer is larger than the DATAPixx RAM',
    'DPX_ERR_AUD_SCHED_TOO_FAST':'The requested schedule rate is too fast',
    'DPX_ERR_AUD_SCHED_TOO_SLOW':'The requested schedule rate is too slow',
    'DPX_ERR_AUD_SCHED_BAD_RATE_UNITS':'Unnrecognized schedule rate units parameter',
    'DPX_ERR_AUD_CODEC_POWERUP':'The CODEC didn''t set its internal powerup bits',
    'DPX_ERR_MIC_SET_GAIN_TOO_LOW':'See DPxSetMicSource() for valid values',
    'DPX_ERR_MIC_SET_GAIN_TOO_HIGH':'See DPxSetMicSource() for valid values',
    'DPX_ERR_MIC_SET_BAD_SOURCE':'See DPxSetMicSource() for valid values',
    'DPX_ERR_MIC_SET_BAD_LRMODE':'See DPxSetMicLRMode() for valid values',
    'DPX_ERR_MIC_BUFF_ODD_BASEADDR':'An odd buffer base was requested',
    'DPX_ERR_MIC_BUFF_BASEADDR_TOO_HIGH':'The requested buffer is larger than the DATAPixx RAM',
    'DPX_ERR_MIC_BUFF_ODD_READADDR':'An odd buffer read address was requested',
    'DPX_ERR_MIC_BUFF_READADDR_TOO_HIGH':'The requested read address exceeds the DATAPixx RAM',
    'DPX_ERR_MIC_BUFF_ODD_WRITEADDR':'An odd buffer write address was requested',
    'DPX_ERR_MIC_BUFF_WRITEADDR_TOO_HIGH':'The requested write address exceeds the DATAPixx RAM',
    'DPX_ERR_MIC_BUFF_ODD_SIZE':'An odd buffer size was requested',
    'DPX_ERR_MIC_BUFF_TOO_BIG':'The requested buffer is larger than the DATAPixx RAM',
    'DPX_ERR_MIC_SCHED_TOO_FAST':'The requested schedule rate is too fast',
    'DPX_ERR_MIC_SCHED_BAD_RATE_UNITS':'Unnrecognized schedule rate units parameter',
    'DPX_ERR_VID_SET_BAD_MODE':'See DPxSetVidMode() for valid values',
    'DPX_ERR_VID_CLUT_WRITE_USB_ERROR':'A USB error occurred while writing a video CLUT',
    'DPX_ERR_VID_VSYNC_USB_ERROR':'A USB error occurred while waiting for vertical sync',
    'DPX_ERR_VID_EDID_WRITE_USB_ERROR':'A USB error occurred while writing EDID data',
    'DPX_ERR_VID_LINE_READ_USB_ERROR':'A USB error occurred while reading the video line buffer',
    'DPX_ERR_VID_PSYNC_NPIXELS_ARG_ERROR':'Pixel sync nPixels argument must be in the range 1-8',
    'DPX_ERR_VID_PSYNC_TIMEOUT_ARG_ERROR':'Pixel sync timeout argument must be in the range 0-65535',
    'DPX_ERR_VID_PSYNC_LINE_ARG_ERROR':'Pixel sync raster line argument must be in the range 0-4095',
    'DPX_ERR_VID_ALPHA_WRITE_USB_ERROR':'A USB error occurred while writing video horizontal overlay alpha data',
    'DPX_ERR_VID_BASEADDR_ALIGN_ERROR':'The requested base address was not aligned on a 64kB boundary',
    'DPX_ERR_VID_BASEADDR_TOO_HIGH':'The requested base address exceeds the DATAPixx RAM',
    'DPX_ERR_VID_VSYNC_WITHOUT_VIDEO':'The API was told to block until VSYNC; but DATAPixx is not receiving any video',
    'DPX_ERR_VID_BL_INTENSITY_ARG_ERROR': 'Backlight intensity argument must be in the range 0-255',
    'DPX_ERR_PPX_SEQ_WRITE_USB_ERROR':'A USB error occurred while writing a video sequence'}

# Define SCOPE_CTRL_DE       0x4000
# Define SCOPE_CTRL_HSYNC    0x2000
# Define SCOPE_CTRL_VSYNC    0x1000
# Define SCOPE_CTRL_DDC_SCL  0x0002
# Define SCOPE_CTRL_DDC_SDA  0x0001

# Define N_SCOPE_TEST_FRAMES 10
# Define MAX_SCOPE_HMSGS     20
# Define PPX_LEDCUR_TO_VDAC 786.432

# Define HIGH_CAL_DAC_VALUE0x6000# Gives +7.5V on +-10V DACs

# DefineTOUCHPIXX_STABILIZE_DISTANCE 1500
# Define LOW_CAL_DAC_VALUE0xA000# Gives -7.5V on +-10V DACs