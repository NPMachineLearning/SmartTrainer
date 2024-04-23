import cv2
import tensorflow as tf

# load labels
labels = []
with open("labels.txt", "r") as f:
    for line in f.readlines():
        labels.append(line.strip())

# input image size to model
INPUT_SIZE = (224, 224)

# number of frames per clip
NUM_FRAME_PER_CLIP = 1

def load_model(n_frame_per_clip=1):
  # load model and init states
  model = tf.saved_model.load("models/movinet")

  # genreate initial states
  states = model.signatures["init_states"](tf.shape(tf.ones([1,NUM_FRAME_PER_CLIP,INPUT_SIZE[0],INPUT_SIZE[1],3])))

  # warm up model
  _ = model({**states, "image":tf.ones([1,1,INPUT_SIZE[0],INPUT_SIZE[1],3])})
  
  return model, states


# All setting should be base on
# v4l2-ctl --list-formats-ext
# and 
# sudo guvcview
# output and configuration
# otherwise it will not work in Linux
WINDOW_NAME = "Frame"
WINDOW_SIZE = (1280, 720)
CAM_OUTPUT_FORMATE = "MJPG" 

# configure vide cap
vid = cv2.VideoCapture(0) 
vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*CAM_OUTPUT_FORMATE))
vid.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_SIZE[0])
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_SIZE[1])
vid.set(cv2.CAP_PROP_FPS, 30.)

actions = set()

try:
    model, states = load_model(NUM_FRAME_PER_CLIP)
    
    # configure window
    cv2.namedWindow(WINDOW_NAME)
    cv2.moveWindow(WINDOW_NAME, 30, 40)
    cv2.resizeWindow(WINDOW_NAME, WINDOW_SIZE[0], WINDOW_SIZE[1])
      
    while(True):
        # Capture the video frame 
        # by frame 
        ret, frame = vid.read()

        if vid.isOpened():
            if ret:
                # preprocessing frame
                input_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                input_img = tf.constant(input_img)
                input_img = tf.image.resize(input_img, INPUT_SIZE)
                input_img = tf.cast(input_img, tf.float32) / 255.
                input_img = input_img[tf.newaxis, tf.newaxis, ...]
                
                # make prediction
                output, states = model({**states, "image": input_img})
                pred_soft = tf.nn.softmax(output)
                pred_index = tf.argmax(pred_soft, axis=-1).numpy()[0]
                pred_prob = tf.reduce_max(pred_soft, axis=-1).numpy()[0]
                if pred_prob > 0.8:
                    actions.add(labels[pred_index])
                    print(f"{actions} | {input_img.shape}", end="\r", flush=True)
                    # print(f"{labels[pred_index]} | {pred_prob*100.:.2f}%", end="\r", flush=True)
                
                # display the resulting frame 
                cv2.imshow(WINDOW_NAME, frame)
                cv2.setWindowTitle(WINDOW_NAME, f"{WINDOW_NAME} | {vid.get(cv2.CAP_PROP_FPS)} FPS")
            else:
                raise Exception("Unable to read frame")
        
        # the 'q' button is set as the 
        # quitting button you may use any 
        # desired button of your choice 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        
        # detect the window is closed by user
        if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            print("Window closed")
            break
            
    # After the loop release the cap object 
    vid.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows()
except Exception as e:
    print(e)
    vid.release()
    cv2.destroyAllWindows()
    