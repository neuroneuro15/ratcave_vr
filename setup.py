

setuptools.setup(
    name="ratcave_vr",
    version="0.1.0",
    url="https://github.com/neuroneuro15/ratcave_vr",

    author="Nicholas A. Del Grosso",
    author_email="delgrosso@bio.lmu.de",

    description="An API and installation guide for the Sirota Lab freely-moving VR system based on ratcave",
    long_description=open('README.md').read(),

    packages=setuptools.find_packages(),

    install_requires=['numpy', 'future', 'pyglet', 'ratcave', 'scipy', 'natnetclient',
                      'six', 'wavefront-reader', 'wxPython', 'pypixxlib', 'psychopy'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
