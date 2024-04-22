import cv2
import tensorflow as tf

# load labels
labels = []
with open("labels.txt", "r") as f:
    for line in f.readlines():
        labels.append(line.strip())

# input size
INPUT_SIZE = (224, 224)

# number of frame
NUM_FRAME = 5

frame_buffer = []

# load model and init states
model = tf.saved_model.load("models/movinet")

# genreate initial states
states = model.signatures["init_states"](tf.shape(tf.ones([1,NUM_FRAME,INPUT_SIZE[0],INPUT_SIZE[1],3])))

# warm up model
_ = model({**states, "image":tf.ones([1,NUM_FRAME,INPUT_SIZE[0],INPUT_SIZE[1],3])}) 

# All setting should be base on
# v4l2-ctl --list-formats-ext
# and 
# sudo guvcview
# output and configuration
# otherwise it will not work in Linux
WINDOW_NAME = "Frame"
WINDOW_SIZE = (848, 480)
CAM_OUTPUT_FORMATE = "MJPG" 

vid = cv2.VideoCapture(0, apiPreference=cv2.CAP_V4L2) 
vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*CAM_OUTPUT_FORMATE))
vid.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_SIZE[0])
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_SIZE[1])
vid.set(cv2.CAP_PROP_FPS, 5.)

try:  
    while(True): 
        
        # Capture the video frame 
        # by frame 
        ret, frame = vid.read()

        if vid.isOpened():
            if ret:
                if len(frame_buffer) >= NUM_FRAME:
                    frame_buffer.clear()
                    
                # resize frame
                img = cv2.resize(frame, INPUT_SIZE)
                frame_buffer.append(img)
                
                # if frame buffer is full then make prediction
                if len(frame_buffer) >= NUM_FRAME:
                    input_imgs = tf.constant(frame_buffer, dtype=tf.float32)[tf.newaxis, ...]
                    input_imgs = input_imgs / 255.
                    pred_logit, states = model({**states, "image": input_imgs})
                    pred_soft = tf.nn.softmax(pred_logit, axis=-1)
                    pred_index = tf.argmax(pred_soft, axis=-1).numpy()[0]
                    pred_prob = tf.reduce_max(pred_soft, axis=-1).numpy()[0]
                    if pred_prob > 0.9:
                        print(f"{labels[pred_index]} | {pred_prob*100.:.2f}%", end="\r", flush=True)
                
                # Display the resulting frame 
                cv2.imshow(WINDOW_NAME, frame)
                cv2.resizeWindow(WINDOW_NAME, WINDOW_SIZE[0], WINDOW_SIZE[1])
            else:
                raise Exception("Unable to read frame")
        
        # the 'q' button is set as the 
        # quitting button you may use any 
        # desired button of your choice 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        
        # detect the window is closed by user
        if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            print("All windows closed")
            vid.release()
            cv2.destroyAllWindows()
            
    
    # After the loop release the cap object 
    vid.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows()
except Exception as e:
    print(e)
    vid.release()
    cv2.destroyAllWindows()
    