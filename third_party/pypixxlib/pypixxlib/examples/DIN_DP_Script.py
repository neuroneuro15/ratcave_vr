from pypixxlib.datapixx import DATAPixx
my_device = DATAPixx()
din_state = my_device.din.getValue()
# Start your experiment
experiement_is_running = True
while experiement_is_running:
    old_state = din_state
    my_device.updateRegisterCache()
    din_state = my_device.din.getValue()
    if old_state is not din_state: # Something triggered.
        # Now we want to check, for example, if pin 6 triggered.
        if (old_state & 2**6) is not (din_state & 2**6):
            print 'Pin 6 triggered!'
            experiement_is_running = False
        else:
            print 'Pin 6 is in the same state as before'
# Finish your experiment