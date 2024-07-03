###
# Reference to https://github.com/marcelotduarte/cx_Freeze/blob/main/samples/pyqt5/setup.py
# and modify
###
from cx_Freeze import setup, Executable
import os

try:
    from cx_Freeze.hooks import get_qt_plugins_paths
except ImportError:
    get_qt_plugins_paths = None

# copy:
# exercise config file
include_files = ['./smart_trainer_config']
if get_qt_plugins_paths:
    # Inclusion of extra plugins (since cx_Freeze 6.8b2)
    # cx_Freeze automatically imports the following plugins depending on the
    # module used, but suppose we need the following:
    include_files += get_qt_plugins_paths("PySide6", "multimedia")

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [],
                 'includes': [], 
                 'excludes': ["tkinter", "email", "pydoc"],
                 "bin_excludes": ["libqpdf.so", "libqpdf.dylib"],
                 'include_files': include_files,
                 "zip_include_packages": ["PySide6", "shiboken6"],
                 # include module search path for 
                 # any modules outside and at same level
                 # of this directory
                 'include_path': os.path.abspath("../")}

base = 'gui'

executables = [
    Executable('app.py', base=base)
]

setup(name='Exercise Repetition Counter',
      version = '0.0.1',
      description = 'Counting exercise repetition',
      options = {'build_exe': build_options},
      executables = executables)
