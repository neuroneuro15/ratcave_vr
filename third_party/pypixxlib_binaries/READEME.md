The libdpx_x64.dll file is **required** for the pyplixxlib installation on 64-bit systems, 
but due to a bug, isn't automatically installed.

To fix this, make sure the libdpx_x64.dll file is present in the python package (pypixxlib-1.3.0/pypixxlib);
if not, copy it in.  Then, make sure the setup.py file contains the 'libdpx_x64.dll' in the package_data line.

If these are both there, everything should work just fine.


