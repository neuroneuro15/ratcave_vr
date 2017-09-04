from pypixxlib.i1 import I1Display # We will use an i1Display here

# Initialize the device.
my_device = I1Display()
my_device.setCurrentCalibration('RGB LED') # We will be using a device with RGB LEDs
print 'Current calibration is: ', my_device.getCurrentCalibration() # Verify we have the right calibration

# Set the color/intensity you wish to measure
my_device.runMeasurement()
print 'next acquisition' # Change to the next color/intensity
my_device.runMeasurement()
print 'next acquisition' # Change to the next color/intensity
my_device.runMeasurement()

results = my_device.getAllMeasurement() # Get a list of all measurements
for i in range(len(results)):
    print results[i] # Print the different measurements

my_device.printLatestMeasurement() # If you want to print your latest measurement

my_device.close()  # Close the device.