# import matplotlib
# import matplotlib.pylab as plt
# matplotlib.use("QtAgg")
import numpy as np
import os
import cv2
import onnxruntime as ort



MODEL_PATH = os.path.join(os.path.dirname(__file__), 
                          "movenet_singlepose_thunder_v4.onnx")
INPUT_SIZE = (256, 256)
    
def load_model(model_path=MODEL_PATH):
    """
    Load movenet model

    Args:
        - model_path (str): path to onnx model. Default model 
        https://www.kaggle.com/models/google/movenet/tensorFlow2/singlepose-thunder. 
        The model was converted from Tensorflow model to ONNX by
        https://onnxruntime.ai/

    Returns:
        ONNX model
    """
    sess_options = ort.SessionOptions()
    # use 1 thread for model inference
    sess_options.intra_op_num_threads = 1
    sess_options.execution_mode = ort.ExecutionMode.ORT_PARALLEL 
    
    ep_list = ['CPUExecutionProvider']
    
    model = ort.InferenceSession(model_path, sess_options=sess_options, providers=ep_list)
    
    return model

def predict(image:np.ndarray, model:ort.InferenceSession):
    """
    Use movenet model to gnereate keypoints in yx coordinate from image

    Args:
        - image (Tensor): Image to generate keypoints
        - model (Movenet): Movenet model

    Returns:
        NDArray: in dimension [17, 3], first two value is coordinate in yx from last dimension
        and they are in range of 0.0-1.0, last value is confident score from last dimension, 
        first dimension is 17 keypoints 
    """
    input_image = image.astype(np.int32)
    input_name = model.get_inputs()[0].name
    output_name = model.get_outputs()[0].name
    # return a list of predictions
    outputs = model.run([output_name], {input_name:input_image})
    return outputs[0][0][0]

def preprocess_kps(kps, scale_xy=(1., 1.)):
    """
    Change keypoints yx coordinate from movenet to xy coordinate

    Args:
        - kps (NDArray): Numpy 2d array straight from movenet in yx coordinate.
        expect coordinate in yx.
        - scale_xy (tuple, optional): Scale on x and y for keypoints. 
        Defaults to (1., 1.).

    Returns:
        - NDArray: Numpy 2d array in xy coordinate and scaled if scale_xy was
        provided.
        - Average confidence rate: float from 0.0 ~ 1.0 determine how confident
        the keypoints would be in average.
    """
    average_confidence_rate = np.mean(kps[:, 2], axis=0)
    
    for i in range(len(kps)):
        temp_y = kps[i][0]
        kps[i][0] = kps[i][1] * scale_xy[0]
        kps[i][1] = temp_y * scale_xy[1]
        
    return kps, average_confidence_rate

def normalize_kps(kps, image_width, image_height):
        """
        Normalize keypoints by image width and height

        Args:
            - kps (dict): keypoints
            - image_width (int): image width
            - image_height (int): image height

        Returns:
            _type_: _description_
        """
        for kp in kps:
            kp[0] /= image_width
            kp[1] /= image_height
            
        return kps

def preprocess_input_image_cv(cv_image, size=INPUT_SIZE, pad=False, pad_color=(0,0,0)):
    """
    Preprocess image before fed it to model
    
    This will resize image into target size, if pad is True then
    image is resized in aspect ratio and padded with border

    Args:
        - image (numpy): Image from opencv as NDArray. (height, width, color)
        where color is in RGB color channel. 
        - size (tuple, optional): Target size for image.
        - pad (bool, optional): Whether to pad image or not if true
        then image is resized in aspect ratio and padded with border.
        - pad_color(tuple, optional): Color for padding

    Returns:
        NDArray: an image with shape (1, height, width, color)
    """
    if not pad:
        img = cv2.resize(cv_image, size)
    
    if pad:
        # get original image size
        original_size = (cv_image.shape[1], cv_image.shape[0])
        
        # calculate aspect ratio
        ratio = float(max(size)) / max(original_size)
        
        # create new size to resize image to
        new_size = tuple([int(x*ratio) for x in original_size])
        img = cv2.resize(cv_image, new_size)
        
        # get padding size
        delta_w = size[0] - new_size[0]
        delta_h = size[1] - new_size[1]
        
        # define padding size for top bottom left right
        top, bottom = delta_h//2, delta_h-(delta_h//2)
        left, right = delta_w//2, delta_w-(delta_w//2)
        
        # make padding 
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=pad_color)
    
    # expand dimension    
    img = np.expand_dims(img, axis=0)
    return img

if __name__ == "__main__":
    pass 
    # model = load_model()
    
    # print(model.get_inputs()[0])
    # print(model.get_outputs()[0])
    
    # image = cv2.imread("./Squat.jpg")
    # print(image.shape)
    # image = preprocess_input_image_cv(image)
    
    # kps = predict(image, model)
    # print(kps.shape)
    