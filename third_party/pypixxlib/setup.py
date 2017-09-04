from setuptools import setup, find_packages
#TO USE ME: (1st for pip, 2nd for windows exe)
# python setup.py sdist --formats=gztar
# python setup.py bdist --formats=wininst
setup(
        name='pypixxlib',
        
        version='1.3.0',
        
        description='VPixx Devices SDK',
        
        url='https://vpixx.com',
        
        author='VPixx Technologies',
        author_email='support@vpixx.com',
        
        packages=['pypixxlib', 'pypixxlib/examples'],
        
        install_requires=[],
        
        package_data={'pypixxlib': ['libdpx.dll', 'libdpx_x64.dll', 'libdpx.so', 'libdpx.dylib', 'libdpx_64bit.dylib', 'docs/pypixxlib.pdf', 'i1d3Files/*', 
        'iOne.so', 'iOne.dll', 'libi1d3.so', 'libi1Pro.so', 'Logo_VPixx.jpg']}  
 )
