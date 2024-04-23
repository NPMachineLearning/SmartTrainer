import cv2
import tensorflow as tf
import time

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

def load_gif(file_path, image_size=(224,224)):
  raw = tf.io.read_file(file_path)
  video = tf.io.decode_gif(raw)
  video = tf.image.resize(video, image_size)
  video = tf.cast(video, tf.float32) / 255.
  return video

cap_actions = set()

WINDOW_NAME = "Frame"

try:
  file_gif = load_gif("./gifs/output.gif") 
  input_video = file_gif[tf.newaxis, ...]
  frames = tf.split(input_video, input_video.shape[1], axis=1)
  print(f"Total frames: {len(frames)}")
  
  model, states = load_model(NUM_FRAME_PER_CLIP)
  
  cv2.namedWindow(WINDOW_NAME)
  cv2.moveWindow(WINDOW_NAME, 30, 40)
  
  for i, frame in enumerate(frames):
    # make prediction for frame
    output, states = model({**states, "image":frame})
    pred_probs = tf.nn.softmax(output)
    pred_index = tf.argmax(pred_probs, axis=-1).numpy()[0]
    prob = tf.reduce_max(pred_probs, axis=-1).numpy()[0]
    true_label = labels[pred_index]
    
    # prepare and show image in window
    img = tf.squeeze(frame[0]).numpy()
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (640, 480))
    img = cv2.putText(img, 
                      f"{true_label} | {prob*100.:.2f}%", 
                      (0, 40),
                      cv2.FONT_HERSHEY_SIMPLEX,
                      1,
                      color=(0,0,255),
                      thickness=2)
    cv2.imshow(WINDOW_NAME, img)
    cv2.setWindowTitle(WINDOW_NAME, f"Frame: {i+1}/{len(frames)}")
    if cv2.waitKey(1) & 0xFF == ord('q'): 
       break
    # detect the window is closed by user
    if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
        print("Window closed")
        break
    
    # add distinct action
    cap_actions.add(true_label)
    
    # show frame result
    print(f"frame {i+1} | {true_label} | {prob*100.:.2f}% | shape: {frame.shape}")
    
  print(f"Captured actions: {cap_actions}")
  cv2.destroyAllWindows()
except Exception as e:
  print(e)