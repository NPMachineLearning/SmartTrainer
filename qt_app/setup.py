from cx_Freeze import setup, Executable
import os

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [],
                 'includes': [], 
                 'excludes': [],
                 # including rep_counting source code
                 # and config file
                 'include_files': ['../rep_counting', '../smart_trainer_config'],
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
