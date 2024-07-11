import tensorflow as tf
import matplotlib
import matplotlib.pylab as plt
import numpy as np
import os

matplotlib.use("QtAgg")

MODEL_PATH = os.path.join(os.path.dirname(__file__), 
                          "movenet_singlepose_thunder_3.tflite")
INPUT_SIZE = (256, 256)

def validate_tensor_image(image):
    if not isinstance(image, (tf.Tensor)):
        raise Exception("image must be a Tensor image")

def validate_image_dims(image, ndims):
    image_dims = len(image.get_shape())
    if ndims != image_dims:
        raise Exception(f"image must be in dimension of {ndims} but got {image_dims}")
    
def load_model(model_path=MODEL_PATH):
    """
    Load movenet model

    Args:
        model_path (str): model path

    Returns:
        tuple: (model, input_details, output_details)
    """
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    
    # warming up model
    img = tf.convert_to_tensor(np.zeros((INPUT_SIZE[0], INPUT_SIZE[0], 3)), dtype=tf.float32)
    img = img[tf.newaxis, ...]
    predict(img, 
            interpreter, interpreter.get_input_details(), 
            interpreter.get_output_details())
    
    return interpreter, interpreter.get_input_details(), interpreter.get_output_details()

def predict(image, model, input_details, output_details):
    """
    Use movenet model to gnereate keypoints in yx coordinate from image

    Args:
        image (Tensor): Image to generate keypoints
        model (Movenet): Movenet model
        input_details : input_details from movenet model
        output_details : output_details from movenet model

    Returns:
        NDArray: in dimension [17, 3], first two value is coordinate in yx from last dimension
        and they are in range of 0.0-1.0, last value is confident score from last dimension, 
        first dimension is 17 keypoints 
    """
    validate_tensor_image(image)
    validate_image_dims(image, 4)
    model.set_tensor(input_details[0]['index'], image.numpy())
    model.invoke()
    kps_and_scores = model.get_tensor(output_details[0]['index'])
    
    return kps_and_scores[0][0]

def preprocess_kps(kps, scale_xy=(1., 1.)):
    """
    Change keypoints yx coordinate from movenet to xy coordinate

    Args:
        kps (NDArray): Numpy 2d array straight from movenet in yx coordinate.
        expect coordinate in yx.
        scale_xy (tuple, optional): Scale on x and y for keypoints. 
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
            kps (dict): keypoints
            image_width (int): image width
            image_height (int): image height

        Returns:
            _type_: _description_
        """
        for kp in kps:
            kp[0] /= image_width
            kp[1] /= image_height
            
        return kps
    
def preprocess_input_image(image, size=INPUT_SIZE, pad=False):
    """
    Preprocess image before fed it to model

    Args:
        image (Tensor): image in tensor
        size (tuple, optional): size of image.
        pad (bool, optional): True to pad image.

    Returns:
        Tensor: in dimension [batch, height, width channels]
    """
    validate_tensor_image(image)
    validate_image_dims(image, 3)
    new_image = tf.cast(image, dtype=tf.float32)
    new_image = tf.expand_dims(new_image, axis=0)
    if pad:
        new_image = tf.image.resize_with_pad(new_image, *size)
    else:
        new_image = tf.image.resize(new_image, size)
    
    return new_image

def preprocess_input_image_cv(cv_image, size=INPUT_SIZE, pad=False, pad_color=(0,0,0)):
    """
    Preprocess image before fed it to model
    
    This will resize image into target size, if pad is True then
    image is resized in aspect ratio and padded with border

    Args:
        - image (numpy): Image from opencv as NDArray. (height, width, color)
        where color is in BGR color channel. 
        - size (tuple, optional): Target size for image.
        - pad (bool, optional): Whether to pad image or not if true
        then image is resized in aspect ratio and padded with border.
        - pad_color(tuple, optional): Color for padding

    Returns:
        NDArray: an image with shape (1, height, width, color)
    """
    img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    if not pad:
        img = cv2.resize(img, size)
    
    if pad:
        # get original image size
        original_size = (cv_image.shape[1], cv_image.shape[0])
        
        # calculate aspect ratio
        ratio = float(max(size)) / max(original_size)
        
        # create new size to resize image to
        new_size = tuple([int(x*ratio) for x in original_size])
        img = cv2.resize(img, new_size)
        
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
    import onnxruntime as onnx_rt
    import cv2
    
    model = onnx_rt.InferenceSession("./movenet_singlepose_thunder_3.onnx", 
                                     providers=["CPUExecutionProvider"])
    print(model.get_inputs()[0])
    print(model.get_outputs()[0])
    
    image = cv2.imread("./Squat.jpg")
    print(image.shape)
    image = preprocess_input_image_cv(image)
    
    input_name = model.get_inputs()[0].name
    input_img = image.astype(np.float32)
    input_img = onnx_rt.OrtValue.ortvalue_from_numpy(input_img)
    outputs = model.run(None, {input_name:input_img})
    print(outputs[0].shape)
    
    
    # interpreter, inputs, outputs = load_model(MODEL_PATH)
    # raw = tf.io.read_file("./test_video/squats/squat.gif")
    # raw_image = tf.io.decode_gif(raw)[15]
    # image = preprocess_input_image(raw_image, INPUT_SIZE, False)
    # kps_with_scores = predict(image, interpreter, inputs, outputs)
    # kps_with_scores = preprocess_kps(kps_with_scores, (raw_image.shape[1], raw_image.shape[0]))
    # fig, ax = plt.subplots(1)
    # ax.imshow(raw_image)
    # for kp in kps_with_scores:
    #     x, y = kp[0], kp[1]
    #     ax.add_patch(plt.Circle((x,y), 2.))
    # plt.show()
    