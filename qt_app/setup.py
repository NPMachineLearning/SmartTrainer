###
# refer to https://github.com/marcelotduarte/cx_Freeze/blob/main/samples/pyqt6/setup.py
###
from cx_Freeze import setup, Executable
import os

try:
    from cx_Freeze.hooks import get_qt_plugins_paths
except ImportError:
    get_qt_plugins_paths = None

# include:
# rep_counting source code
# exercise config file
include_files = ['../rep_counting', '../smart_trainer_config']
if get_qt_plugins_paths:
    # Inclusion of extra plugins (since cx_Freeze 6.8b2)
    # cx_Freeze automatically imports the following plugins depending on the
    # module used, but suppose we need the following:
    include_files += get_qt_plugins_paths("PyQt6", "multimedia")

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [],
                 'includes': [], 
                 'excludes': ["tkinter", "email", "pydoc"],
                 "bin_excludes": ["libqpdf.so", "libqpdf.dylib"],
                 'include_files': include_files,
                 "zip_include_packages": ["PyQt6"],
                 'include_path': os.path.abspath("../")}

base = 'gui'

executables = [
    Executable('app.py', base=base)
]

setup(name='Exercise Repetition Counter',
      version = '1.0',
      description = 'Counting exercise repetition',
      options = {'build_exe': build_options},
      executables = executables)
