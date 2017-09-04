
import platform, os
import ctypes
from ctypes.util import find_library

sys_platform = platform.system()
path = os.path.dirname(os.path.realpath(__file__))
if sys_platform == 'Windows':
    IOneDll = ctypes.CDLL(os.path.join(path,"iOne.dll"))
elif sys_platform == 'Linux':
    IOneDll = ctypes.cdll.LoadLibrary(os.path.join(path,"iOne.so"))
elif (sys_platform == 'Darwin') or (sys_platform == 'Mac'):
    path_string = platform.__file__
    path_string = path_string.split('lib')
    try:
        IOneDll = ctypes.cdll.LoadLibrary(path_string[0] + "iOne.dylib")
    except:
        IOneDll = ctypes.cdll.LoadLibrary(path_string[0] + "iOne_64bit.dylib")
else:
    raise Exception('OS Not Recognized') 




# functions related to the i1Display
_initializeI1Display = IOneDll['InitializeI1Display']
def initializeI1Display():
    return i1DisplayErrorCode[_initializeI1Display()]
    
    
_closeI1Display = IOneDll['CloseI1Display']
def closeI1Display():
    return i1DisplayErrorCode[_closeI1Display()]


_getNumberOfI1Display = IOneDll['GetNumberOfI1Display']
def getNumberOfI1Display():
    return _getNumberOfI1Display()


_openI1DisplayDevice = IOneDll['OpenI1DisplayDevice']
def openI1DisplayDevice():
    return i1DisplayErrorCode[_openI1DisplayDevice()]



_geti1DisplayHandle = IOneDll['Geti1DisplayHandle']
_geti1DisplayHandle.restype = ctypes.c_void_p
def geti1DisplayHandle():
    handle = _geti1DisplayHandle()
    return handle
    
    
_init1DisplayCalibrationListData = IOneDll['Init1DisplayCalibrationListData']
def init1DisplayCalibrationListData():
    return _init1DisplayCalibrationListData()


class I1DisplayInfo(ctypes.Structure):
    _fields_ = [("ProductName", ctypes.c_char * 32),
                ("ProductType", ctypes.c_ushort),
                ("FirmwareVersion", ctypes.c_char * 32),
                ("FirmwareDate", ctypes.c_char * 32),
                ("IsLocked", ctypes.c_ubyte)]

_getI1DisplayInfo = IOneDll['GetI1DisplayInfo']
_getI1DisplayInfo.restype = ctypes.POINTER(I1DisplayInfo)
def getI1DisplayInfo():
    i1_display_info = _getI1DisplayInfo()
    
    info = {'Product Name':i1_display_info.contents.ProductName,
            'Product Type':i1_display_info.contents.ProductType,
            'Locked State': i1_display_info.contents.IsLocked,
            'Firmware Version': i1_display_info.contents.FirmwareVersion,
            'Firmware Date': i1_display_info.contents.FirmwareDate}
    
    return info


class I1DisplayMesurement(ctypes.Structure):
    _fields_ = [("Yluminance", ctypes.c_double),
                ("xchrominance", ctypes.c_double),
                ("ychrominance", ctypes.c_double),
                ("z", ctypes.c_double)]
    

_getMesure = IOneDll['GetI1DisplayMesure']
_getMesure.restype = ctypes.POINTER(I1DisplayMesurement)
_getAmbiantMesure = IOneDll['GetI1DisplayAmbiantMesure']
_getAmbiantMesure.restype = ctypes.POINTER(I1DisplayMesurement)
def getI1DisplayMesure(ambiant, raw=False, device='PP'):
    
    offset = {'PP': [0.003, 0.005],
              'VP': [0.003, -0.001],
              'VP3D': [0.003, -0.001],
              'VPEEG': [0.001, 0.005]}
    
    if ambiant == 0:
        i1_display_data = _getMesure()
    else:
        i1_display_data = _getAmbiantMesure()
    
    if raw:
        data = {'luminance':i1_display_data.contents.Yluminance,
                'chrominance': ( i1_display_data.contents.xchrominance, i1_display_data.contents.ychrominance)}
    else:
        data = {'luminance':i1_display_data.contents.Yluminance,
                'chrominance': (i1_display_data.contents.xchrominance + offset[device][0], i1_display_data.contents.ychrominance  + offset[device][1])}
    
    return data


_getI1DisplayDiffuserPosition = IOneDll['GetI1DisplayDiffuserPosition']          
_getI1DisplayDiffuserPosition.restype = ctypes.c_ubyte
def isI1DisplayDiffuserOn():
    value = _getI1DisplayDiffuserPosition()
    if value == 1:
        return True
    elif value == 0:
        return False
        

_setI1DisplayIntegrationTime = IOneDll['SetI1DisplayIntegrationTime']
_setI1DisplayIntegrationTime.argtypes = [ctypes.c_double]
def setI1DisplayIntegrationTime(time=1.0):
    """
    time must be greater than 0.0
    """
    if (time <= 0.0):
        time = 0.2
    _setI1DisplayIntegrationTime(time)
    


_getI1DisplayIntegrationTime = IOneDll['GetI1DisplayIntegrationTime']
_getI1DisplayIntegrationTime.restype = ctypes.c_double
def getI1DisplayIntegrationTime():  
    return _getI1DisplayIntegrationTime()

    
    
_setI1DisplayMeasurementMode = IOneDll['SetI1DisplayMeasurementMode']
_setI1DisplayMeasurementMode.argtypes = [ctypes.c_int]
_setI1DisplayMeasurementMode.restype = None  
def setI1DisplayMeasurementMode(mode):
    
    measurement_mode = {"BURST": 0, "LCD": 1}
    _setI1DisplayMeasurementMode(measurement_mode[mode.upper()])



_getI1DisplayMeasurementMode = IOneDll['GetI1DisplayMeasurementMode']
_getI1DisplayMeasurementMode.restype = ctypes.c_int
def getI1DisplayMeasurementMode():
    
    measurement_mode = {7: "BURST", 1: "LCD"}
    mode = _getI1DisplayMeasurementMode()    
    return measurement_mode[mode]
    


class CalibrationSource(ctypes.Union):
    _fields_ = [("calSource", ctypes.c_int),
                ("padding1", ctypes.c_ubyte*8)]

 
class CalibrationTime(ctypes.Union):
    _fields_ = [("calTime", ctypes.c_int),
                ("padding2", ctypes.c_ubyte*8)]  

     
class CalibrationEntry(ctypes.Structure):
     
    _fields_ = [("source", ctypes.c_ubyte*8),
                ("time", ctypes.c_ubyte*8),
                ("fileName", ctypes.c_byte*512),
                ("displayName", ctypes.c_byte*64),
                ("displayMfg", ctypes.c_byte*64),
                ("displayModel", ctypes.c_byte*64),
                ("key", ctypes.c_byte*32),
                ("EDR_Type", ctypes.c_short)]
    
    
    
class CalibrationList(ctypes.Structure):
    _fields_ = [("calibration", ctypes.POINTER(CalibrationEntry)*64)]
    
    
    
_getI1DisplayCalibrationList = IOneDll['GetI1DisplayCalibrationList']
_getI1DisplayCalibrationList.restype = ctypes.POINTER(CalibrationList)
def getI1DisplayCalibrationList():
    calibration_list = {}
    i1_display_list = _getI1DisplayCalibrationList()
    data = i1_display_list.contents.calibration
    
    for i in range(64):
        try:
            calibration_list[i] = [ctypes.cast(data[i].contents.fileName, ctypes.c_char_p).value,
                                   ctypes.cast(data[i].contents.displayName, ctypes.c_char_p).value]
            
            
        except:
            # The list contains 64 pointers to data entries, but many can be empty.
            # We just need the valid ones.
            pass
        
    return calibration_list


_setI1DisplayRessourcesFilesPath = IOneDll['SetI1DisplayRessourcesFilesPath']
_setI1DisplayRessourcesFilesPath.argtypes = [ctypes.c_char_p]
_setI1DisplayRessourcesFilesPath.restype = None
def setI1DisplayRessourcesFilesPath(path):
    _setI1DisplayRessourcesFilesPath(path)


_setI1DisplayTechnologyStringFilesPath = IOneDll['SetI1DisplayTechnologyStringFilesPath']
_setI1DisplayTechnologyStringFilesPath.argtypes = [ctypes.c_char_p]
_setI1DisplayTechnologyStringFilesPath.restype = None
def setI1DisplayTechnologyStringFilesPath(path):
    _setI1DisplayTechnologyStringFilesPath(path)    
    

_getI1DisplayCalibration = IOneDll['GetI1DisplayCalibration']
_getI1DisplayCalibration.restype = ctypes.c_char_p
def getI1DisplayCurrentCalibration(calibration_list):
    mapping = {0: "Unknown",
               2: "CCFL",
               4: "WHITE LED",
               5: "RGB LED",
               8: "CRT",
               9: "PROJECTOR",
               11:"VPIXX",
               12:"EEG"}
    
    calibration_number = None
    current_calibration = _getI1DisplayCalibration()
    key = calibration_list.keys()
    
    try:
        
        for i in range(len(key)):
            
            if current_calibration in calibration_list[key[i]]:
                calibration_number = i
                   
        if (getI1DisplayMeasurementMode() == 'BURST') and (calibration_number == 4):
            calibration_number = 12
        elif (getI1DisplayMeasurementMode() == 'BURST') and (calibration_number == 5):
            calibration_number = 11
            
    
    except:
        return mapping[0]
        
    return mapping[calibration_number]
    


_setI1DisplayCalibration = IOneDll['SetI1DisplayCalibration']
def setI1DisplayCalibration(calibration_number):
    number = calibration_number.upper()
    mapping = {"CCFL":      2,
               "WHITE LED": 4,
               "RGB LED":   5,
               "CRT":       8,
               "PROJECTOR": 9,
               "VPIXX":     5,
               "EEG":       4}     
    
    if (number == "RGB LED") or (number == "CCFL") or (number == "WHITE LED"):
        setI1DisplayMeasurementMode("LCD")
    else:
        setI1DisplayMeasurementMode("BURST")
                
    _setI1DisplayCalibration(mapping[number])



"""

 functions related to the i1Pro

"""
_getI1ProHandle = IOneDll['GetI1ProHandle']
_getI1ProHandle.restype = ctypes.c_void_p
def getI1ProHandle():
    return _getI1ProHandle()


_getI1ProDeviceCount = IOneDll['GetI1ProDeviceCount']
def getI1ProDeviceCount():
    return _getI1ProDeviceCount()


_openI1ProDevice = IOneDll['OpenI1ProDevice']
def openI1ProDevice():
    return i1ProErrorCode[_openI1ProDevice()]


_closeI1ProDevice = IOneDll['CloseI1ProDevice']
_closeI1ProDevice.restype = None
def closeI1ProDevice():
    _closeI1ProDevice()


_getI1ProConnectionStatus = IOneDll['GetI1ProConnectionStatus']
def getI1ProConnectionStatus():
    return i1ProConnectionStatus[_getI1ProConnectionStatus()]


_getI1ProLastError = IOneDll['GetI1ProLastError']
_getI1ProLastError.restype = ctypes.c_char_p
def getI1ProLastError():
    return _getI1ProLastError()       


_setI1ProAmbientLightMeasurementMode = IOneDll['SetI1ProAmbientLightMeasurementMode']
_setI1ProAmbientLightMeasurementMode.restype = None
def setI1ProAmbientLightMeasurementMode():
    _setI1ProAmbientLightMeasurementMode()
    

_setI1ProEmissionSpotMeasurementMode = IOneDll['SetI1ProEmissionSpotMeasurementMode']
_setI1ProEmissionSpotMeasurementMode.restype = None
def setI1ProEmissionSpotMeasurementMode():
    _setI1ProEmissionSpotMeasurementMode()  


_getI1ProMeasurementMode = IOneDll['GetI1ProMeasurementMode']
_getI1ProMeasurementMode.restype = ctypes.c_char_p
def getI1ProMeasurementMode():
    return _getI1ProMeasurementMode()   


_setI1ProIlluminationMode = IOneDll['SetI1ProIlluminationMode']
_setI1ProIlluminationMode.restype = None
_setI1ProIlluminationMode.argtypes = [ctypes.c_char_p]
def setI1ProIlluminationMode(mode):
    
    if mode in ["A", "B", "C", "D50", "D55", "D65", "D75", "F2", "F7", "F11", "Emission"]:
        _setI1ProIlluminationMode(mode)
    else:
        raise Exception("Wrong Illumination Mode")
        

_getI1ProIlluminationMode = IOneDll['GetI1ProIlluminationMode']
_getI1ProIlluminationMode.restype = ctypes.c_char_p
def getI1ProIlluminationMode():
    return _getI1ProIlluminationMode()       


_setI1ProColorSpaceMode = IOneDll['SetI1ProColorSpaceMode']
_setI1ProColorSpaceMode.restype = None
_setI1ProColorSpaceMode.argtypes = [ctypes.c_char_p]
def setI1ProColorSpaceMode(mode):
    
    if mode in ["CIELab", "CIELCh", "CIELuv", "CIELChuv", "CIEuvY1960", "CIEuvY1976", "CIEXYZ", "CIExyY"]:
        _setI1ProColorSpaceMode(mode)
    else:
        raise Exception("Wrong Color Space Mode")
        

_getI1ProColorSpaceMode = IOneDll['GetI1ProColorSpaceMode']
_getI1ProColorSpaceMode.restype = ctypes.c_char_p
def getI1ProColorSpaceMode():
    return _getI1ProColorSpaceMode()    


_setI1ProAdaptativMeasurementMode = IOneDll['SetI1ProAdaptativMeasurementMode']
_setI1ProAdaptativMeasurementMode.restype = None
_setI1ProAdaptativMeasurementMode.argtypes = [ctypes.c_char_p]
def setI1ProAdaptativMeasurementMode(mode):
    
    if mode == True:
        _setI1ProAdaptativMeasurementMode("1")
    else:
        _setI1ProAdaptativMeasurementMode("0") # what we want
        # Defaults to "0", reducing measurement time from about 2.5 seconds to 1.1 seconds.

        
_getI1ProAdaptativMeasurementMode = IOneDll['GetI1ProAdaptativMeasurementMode']
_getI1ProAdaptativMeasurementMode.restype = ctypes.c_char_p
def getI1ProAdaptativMeasurementMode():
    return _getI1ProAdaptativMeasurementMode() 


_getI1ProDeviceType = IOneDll['GetI1ProDeviceType']
_getI1ProDeviceType.restype = ctypes.c_char_p
def getI1ProDeviceType():
    return _getI1ProDeviceType() 


_getI1ProTimeUntilCalibrationExpire = IOneDll['GetI1ProTimeUntilCalibrationExpire']
_getI1ProTimeUntilCalibrationExpire.restype = ctypes.c_char_p
def getI1ProTimeUntilCalibrationExpire():
    try:
        time = int(_getI1ProTimeUntilCalibrationExpire())
    except:
        time = -1
    return time


_getI1ProHardwareRevision = IOneDll['GetI1ProHardwareRevision']
_getI1ProHardwareRevision.restype = ctypes.c_char_p
def getI1ProHardwareRevision():
    return _getI1ProHardwareRevision()


_getI1ProSerialNumber = IOneDll['GetI1ProSerialNumber']
_getI1ProSerialNumber.restype = ctypes.c_char_p
def getI1ProSerialNumber():
    return _getI1ProSerialNumber() 

calibrating = False
_calibrateI1Pro = IOneDll['CalibrateI1Pro']
_calibrateI1Pro.restype = ctypes.c_int
def calibrateI1Pro():
    global calibrating
    calibrating = True
    error_code = i1ProErrorCode[_calibrateI1Pro()]
    if error_code != 'success':
        closeI1ProDevice()
        Calibration_Error = "Calibration Failed. Error: "+ error_code
        raise Exception(Calibration_Error)
    calibrating = False


_waitForButtonPress = IOneDll['WaitForButtonPress']
_waitForButtonPress.restype = ctypes.c_int
def waitForButtonPress():
    _waitForButtonPress()    
    

def isI1ProCalibrating():
    return calibrating


_getI1ProSpectrum = IOneDll['GetI1ProSpectrum']
_getI1ProSpectrum.restype = ctypes.POINTER(ctypes.c_float)
def getI1ProSpectrum():
    value = _getI1ProSpectrum()
    data = []
    for i in range(36):
        data.append(value[i])
    return data


_getI1ProTriStimulus = IOneDll['GetI1ProTriStimulus']
_getI1ProTriStimulus.restype = ctypes.POINTER(ctypes.c_float)
def getI1ProTriStimulus():
    value = _getI1ProTriStimulus()
    return [value[0], value[1], value[2]]


_triggerI1ProMeasurement = IOneDll['TriggerI1ProMeasurement']
_triggerI1ProMeasurement.restype = ctypes.c_int
def triggerI1ProMeasurement():
    error_code = i1ProErrorCode[_triggerI1ProMeasurement()]
    if error_code != 'success':
        Trigger_Error = "Trigger Failed. Error: "+ error_code
        raise Exception(Trigger_Error)
    
    

i1ProErrorCode = {0 : 'success',
                  1 : 'Exception',
                  2 : 'Bad Buffer',
                  9 : 'Invalid Handle',
                  10 : 'Invalid Argument',
                  11 : 'Device Not Open',
                  12 : 'Device Not Connected',
                  13 : 'Device Not Calibrated',
                  14 : 'No Data Available',
                  15 : 'No Measure Mode Set',
                  17 : 'No Reference Chart Line',
                  18 : 'No Substrate White',
                  19 : 'Not Licensed',
                  20 : 'Device Already Open',
                  51 : 'Device Already In Use',
                  52 : 'Device Communication Error',
                  53 : 'USB Power Problem',
                  54 : 'Not On White Tile',                           
                  60 : 'Strip Recognition Failed',
                  61 : 'Chart Correlation Failed',
                  62 : 'Insufficient Movement',
                  63 : 'Excessive Movement',
                  64 : 'Early Scan Start',
                  65 : 'User Timeout',
                  66 : 'Incomplete Scan',
                  67 : 'Device Not Moved',
                  71 : 'Device Corrupt',
                  72 : 'Wavelength Shift' 
                  }



i1DisplayErrorCode = {0 : 'success',         
                   -100 : 'Non specific error',             
                   -101 : 'Device pointer is NULL',        
                   -102 : 'No device found    ',        
                   -504 : 'The requested Function is not supported by this device',
                   -505 : 'The device is password-locked',
                   -508 : 'The device is currently initialized', 
                   -509 : 'No device is currently initialized', 
                   -510 : 'The communications are out of sync',  
                   -512 : 'The diffuser arm is in the wrong position for measurement', 
                   -513 : 'The calculated checksum is incorrect', 
                   -517 : 'An invalid parameter was passed into the routine', 
                   -519 : 'The device returned an error', 
                   -520 : 'The firmware is obsolete', 
                   -521 : 'Error entering bootloader mode', 
                   -522 : 'USB timed out waiting for response from device', 
                   -523 : 'USB communication error', 
                   -524 : 'EEPROM-write protection error', 
                   -600 : 'Couldnt open file', 
                   -601 : 'Must have at least 3 colors in EDR file',
                   -602 : 'Currently we require 1nm wavelength increment',
                   -603 : 'Currently we require up to at least 730nm.',
                   -604 : 'Currently we require start at 380nm.',
                   -605 : 'Couldnt open CMF data file', 
                   -606 : 'Couldnt parse CMF data file', 
                   -700 : 'Must open file before making other requests.', 
                   -701 : 'File already opened, close to open another file.', 
                   -702 : 'File not found.', 
                   -703 : 'File too short.', 
                   -704 : 'Header didnt have correct signature or file too short.', 
                   -705 : 'Data didnt load properly.', 
                   -706 : 'EDR Data Signature Error', 
                   -707 : 'EDR Spectral Data Signature Error', 
                   -708 : 'Requested more color data than available.', 
                   -709 : 'Cant request tri-stimulus.', 
                   -710 : 'Cant request spectral data in file without it.', 
                   -711 : 'EDR No Wavelength Data.', 
                   -712 : 'Evenly-spaced wavelengths.', 
                   -713 : 'Wavelengths are from table.', 
                   -714 : 'Probably a null pointer to a call.', 
                     16 : 'i1Display3 is Locked.',                         
                     80 : 'EEPROM access error: clock is low.',             
                     81 : 'EEPROM access error: NACK received.',             
                     96 : 'Invalid EEPROM address.',                         
                    128 : 'Invalid command to i1Display3.',                 
                    129 : 'Diffuser is in wrong position for measurement.',
                    -8998: 'Could not find EDR files.',
                    -8999: 'i1Display not opened.',
                    -9000: 'Wrong type of i1Display Pro'}


i1ProConnectionStatus = {0x00 : 'Invalid Connection Handle',
                      0x01 : 'I1Pro Closed',
                      0x03 : 'I1Pro Open'
                      }
