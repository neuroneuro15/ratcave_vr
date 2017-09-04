from pypixxlib.viewpixx import VIEWPixxEEG
my_device = VIEWPixxEEG() # Create an instance of your device.
my_device.setBacklightIntensity(35) # Value between 0-255 for the intensity.
my_device.updateRegisterCache() # Send the value to the device.
my_device.getBacklightIntensity() # Double check our value was sent and applied