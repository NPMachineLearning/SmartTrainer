import tensorflow as tf
import matplotlib
import matplotlib.pylab as plt

matplotlib.use("TkAgg")

MODEL_PATH = "./rep_counting/movenet/movenet_singlepose_thunder_3.tflite"
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
    
    return interpreter, interpreter.get_input_details(), interpreter.get_output_details()

def predict(image, model, input_details, output_details):
    """
    Gnereate keypoints in yx coordinate

    Args:
        image (Tensor): Image to generate keypoints
        model (Movenet): Movenet model
        input_details : input_details from movenet model
        output_details : output_details from movenet model

    Returns:
        numpy array: in dimension [17, 3] in yx corrdinate for first two value in last dimension
        and they are in range of 0.0-1.0
    """
    validate_tensor_image(image)
    validate_image_dims(image, 4)
    model.set_tensor(input_details[0]['index'], image.numpy())
    model.invoke()
    kps_and_scores = model.get_tensor(output_details[0]['index'])
    
    return kps_and_scores[0][0]

def preprocess_kps(kps, height, width):
    """
    To change keypoints' yx to xy and
    recalculate keypoints position from given
    height and width 

    Args:
        kps (array): keypoints with dimension [17, 3] in yx coordinate
        height (int): height of image
        width (int): width of image
    """
    for i in range(len(kps)):
        temp_y = kps[i][0]
        kps[i][0] = kps[i][1] * width
        kps[i][1] = temp_y * height
        
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

if __name__ == "__main__":
    interpreter, inputs, outputs = load_model(MODEL_PATH)
    raw = tf.io.read_file("./gifs/squat.gif")
    raw_image = tf.io.decode_gif(raw)[15]
    image = preprocess_input_image(raw_image, INPUT_SIZE, False)
    kps_with_scores = predict(image, interpreter, inputs, outputs)
    kps_with_scores = preprocess_kps(kps_with_scores, raw_image.shape[0], raw_image.shape[1])
    fig, ax = plt.subplots(1)
    ax.imshow(raw_image)
    for kp in kps_with_scores:
        x, y = kp[0], kp[1]
        ax.add_patch(plt.Circle((x,y), 2.))
    plt.show()
    