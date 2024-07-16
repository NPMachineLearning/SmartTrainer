# Exercise classification

The purpose is to classify exercise action in video or streaming video.

## References

### Video or stream action classification

- [movinet](https://www.tensorflow.org/hub/tutorials/movinet)

### Transfer learning for movinet

- [Transfer learning](https://github.com/tensorflow/models/blob/master/official/projects/movinet/movinet_streaming_model_training_and_inference.ipynb)

# Exercise repetition counting

The purpose is to counting exercise or action repetition.

Here I use signal processing to handle the problem. One of downside of doing
this is not generic which means it is specific to certain exercise or action and
we need to manually define measurement for particular exercise or action.

## Support exercises

- Jumping jacks
- Push ups

## ⚠ Note

- Use [opencv-python](https://pypi.org/project/opencv-python/) for running app.
- Use [opencv-python-headless](https://pypi.org/project/opencv-python-headless/) for app deployment to reduce package size.
- **Do not** install both [opencv-python](https://pypi.org/project/opencv-python/) and [opencv-python-headless](https://pypi.org/project/opencv-python-headless/) in the same environment. This could lead to unexpected problem.

## Install libraries

- Create isolated environment if needed.
- `pip install tensorflow-cpu opencv-python-headless linuxpy matplotlib PySide2 cx_Freeze tf2onnx onnxruntime`

## Run app

1. Go to qt_app directory
2. Run command `python app.py`

⚠ **Note**: on Linux might required to reinstall/install `libxcb-xinerama0` through apt
if encounter following error.
`qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found`. If issue still exists then use [opencv-python-headless](https://pypi.org/project/opencv-python-headless/) instead of [opencv-python](https://pypi.org/project/opencv-python/).

## Desktop app deployment

Directory qt_app is source code for application on desktop. Pre-build executable application can be downloaded from [here](https://mega.nz/folder/WJhi0ZTK#eWCuymKMZLN0NJTfE995Bg).

### Support platform

- Windows
- MacOSX
- Linux

### Create application instruction

**Note**: It is good idea to create and environment
before buiding application. Following two common options.

- [python venv](https://docs.python.org/3/library/venv.html)
- [virtualenv](https://virtualenv.pypa.io/en/latest/)

#### Python requirement

- `>=3.9.0`

#### Library requirements

Following libraries are required for building desktop application.

- [tensorflow](https://pypi.org/project/tensorflow/)
- [opencv-python](https://pypi.org/project/opencv-python/)
- [linuxpy](https://github.com/tiagocoutinho/linuxpy)
- [PyQt5](https://pypi.org/project/PyQt5/)
- [matplotlib](https://pypi.org/project/matplotlib/)

#### Steps

Note: Tool for creating executable application is using
[cx_Freeze](https://cx-freeze.readthedocs.io/en/stable/index.html)

**Note: PyQt6 and PySide6 is not working well with cx_Freeze for MacOSX**

1. At root folder run command either
   - `python3 -m venv .venv`
     or
   - `python -m venv .venv`
2. Activate environment
   - `.\.venv\Script\activate` (Windows)
   - `source ./.venv/bin/activate` (MacOSX, Linux)
   - `source ./.venv/bin/activate.fish` (MacOSX, Linux wiht fish shell)
3. Install packages
   `pip install tensorflow-cpu opencv-python-headless linuxpy matplotlib PySide2 cx_Freeze tf2onnx onnxruntime`
4. Go to directory qt_app
5. Run command
   - `python setup.py build_exe` (Windows)
   - `sudo python3 setup.py bdist_mac` (MacOSX)
   - `python3 setup.py build_exe` (Linux)

## References

### Human body keypoints

- [movenet](https://www.kaggle.com/models/google/movenet/tfLite/singlepose-thunder)
- [ONNX for runtime inference](https://onnxruntime.ai/)

### Rep counting

- [Possible methods](https://towardsdatascience.com/vision-based-rep-counting-in-the-wild-cb9a4d1bdb7e)
- [Signal for rep counting](https://towardsdatascience.com/building-an-exercise-rep-counter-using-ideas-from-signal-processing-fcdf14e76f81)

### Low pass filter

- [Low pass filter](https://dobrian.github.io/cmp/topics/filters/lowpassfilter.html)

### Camera streaming on Linux

- [linuxpy](https://github.com/tiagocoutinho/linuxpy)
