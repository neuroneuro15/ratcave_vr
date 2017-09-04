from pypixxlib.propixx import PROPixx
my_device = PROPixx()
my_device.setDlpSequencerProgram('QUAD12X')
my_device.updateRegisterCache()
# You can now send you stimulus at 120 Hz to be displayed at 1440 Hz!