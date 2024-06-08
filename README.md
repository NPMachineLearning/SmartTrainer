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

## Desktop app deployment

Directory qt_app is source code for application on desktop.

### Support platform

- windows

### Buid instruction

Note: It is good idea to create and environment
before buiding application.

#### Python requirement

> =3.9.0

#### Library requirements

Following libraries are required for building desktop application.

- [tensorflow](https://pypi.org/project/tensorflow/)
- [opencv-python](https://pypi.org/project/opencv-python/)
- [linuxpy](https://github.com/tiagocoutinho/linuxpy)
- [pyqt6](https://pypi.org/project/PyQt6/)
- [matplotlib](https://pypi.org/project/matplotlib/)

#### Instruction

1. Install [cx-Freeze](https://pypi.org/project/cx-Freeze/)
2. Go to directory qt_app
3. Enter command `python setup.py build`

## References

### Human body keypoints

- [movenet](https://www.kaggle.com/models/google/movenet/tfLite/singlepose-thunder)

### Rep counting

- [Possible methods](https://towardsdatascience.com/vision-based-rep-counting-in-the-wild-cb9a4d1bdb7e)
- [Signal for rep counting](https://towardsdatascience.com/building-an-exercise-rep-counter-using-ideas-from-signal-processing-fcdf14e76f81)

### Low pass filter

- [Low pass filter](https://dobrian.github.io/cmp/topics/filters/lowpassfilter.html)

### Camera streaming on Linux

- [linuxpy](https://github.com/tiagocoutinho/linuxpy)
