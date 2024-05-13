import sys
import os
sys.path.insert(1, os.getcwd())
import tensorflow as tf
import cv2
import time
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from rep_counting.movenet_infer import load_model, predict, preprocess_input_image, preprocess_kps, INPUT_SIZE
from rep_counting.kps_metrics_jumping_jack import KpsMetricsJumpingJack

WINDOW_NAME = "Frame"
FRAME_DELAY = 1./3. 

def plot_singal(track, block=True, pause=None, ylim=None):
    ax = plt.gca()
    ax.clear()
    ax.plot(list(range(len(track))), track, 'b-')
    if ylim:
        ax.set_ylim(*ylim)
    plt.show(block=block)
    if pause:
        plt.pause(FRAME_DELAY)

cap = cv2.VideoCapture("./gifs/jumpingjack.gif")

try:
    cv2.namedWindow(WINDOW_NAME)
    cv2.moveWindow(WINDOW_NAME, 30, 40)
    
    model, input_details, output_details = load_model("./models/movenet/movenet_singlepose_thunder_3.tflite")
    jj_metrics = KpsMetricsJumpingJack(low_pass_filter=True)
    track = []
        
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            input_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            input_img = tf.convert_to_tensor(input_img)
            height, width = input_img.shape[0], input_img.shape[1]
            input_img = preprocess_input_image(input_img, INPUT_SIZE)
            kps = predict(input_img, model, input_details, output_details)
            kps = preprocess_kps(kps, height, width)
            kps = jj_metrics.normalize_kps(kps, width, height)
            jj_metrics.update_metrics(kps)
            track.append(jj_metrics.get_metrics()[jj_metrics.metric_names.lrpalm_dist.name])
            cv2.imshow(WINDOW_NAME, frame)
            
            # plot singal by frame
            plot_singal(track, block=False, pause=FRAME_DELAY)
        else:
            break
        
        cv2.setWindowTitle(WINDOW_NAME, f"Frame")
            
        # the 'q' button is set as the 
        # quitting button you may use any 
        # desired button of your choice 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # detect the window is closed by user
        if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            break
        
        time.sleep(FRAME_DELAY)
        
    # After the loop release the cap object 
    cap.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows()
    
    # plot signal 
    plot_singal(track)
except Exception as e:
    print(e)
    cap.release()
    cv2.destroyAllWindows()