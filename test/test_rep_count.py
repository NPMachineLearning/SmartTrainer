import sys
import os
sys.path.insert(1, os.getcwd())
import tensorflow as tf
import cv2
import traceback
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from rep_counting.movenet.movenet_infer import load_model, predict, preprocess_input_image, preprocess_kps, normalize_kps, INPUT_SIZE
from rep_counting.pkg.kps_metrics_jumping_jack import KpsMetricsJumpingJack
from rep_counting.pkg.kps_metrics_push_up import KpsMetricsPushup

WINDOW_NAME = "Frame"
FRAME_DELAY = 0.00001
EXAMPLE = "./test_video/jumpingjacks/jumpingjack.mp4"
CONFIG_FILE = './smart_trainer_config/config.json'

def plot_singal(track, mean=None, block=True, pause=None, ylim=None, title=""):
    ax = plt.gca()
    ax.clear()
    ax.plot(list(range(len(track))), track, 'b-')
    if ylim:
        ax.set_ylim(*ylim)
    ax.set_title(title)
    if mean:
        plt.hlines([mean, mean], xmin=[0], xmax=[len(track)], colors="red", label=f"mean:{mean:.2f}")
    plt.legend()
    plt.show(block=block)
    if pause:
        plt.pause(FRAME_DELAY)

cap = cv2.VideoCapture(EXAMPLE)

try:
    cv2.namedWindow(WINDOW_NAME)
    cv2.moveWindow(WINDOW_NAME, 30, 40)
    
    model, input_details, output_details = load_model()
    metrics = KpsMetricsJumpingJack(config_path=CONFIG_FILE)
    exercise_name = metrics.get_exercise_name()
    
    if not os.path.exists(EXAMPLE):
        raise Exception(f"{EXAMPLE} doesn't exists")
        
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            input_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            input_img = tf.convert_to_tensor(input_img)
            height, width = input_img.shape[0], input_img.shape[1]
            input_img = preprocess_input_image(input_img, INPUT_SIZE)
            kps = predict(input_img, model, input_details, output_details)
            kps = preprocess_kps(kps)
            metrics.update_metrics(kps)
            cv2.imshow(WINDOW_NAME, frame)
            
            # plot singal by frame
            plot_singal(metrics.tracked_metrics, 
                        mean=metrics.config['reference']['mean'], 
                        block=False, 
                        pause=FRAME_DELAY, 
                        title=f"{exercise_name} | rep: {metrics.reptition_count}")
        else:
            break
        
        cv2.setWindowTitle(WINDOW_NAME, f"{exercise_name}")
            
        # the 'q' button is set as the 
        # quitting button you may use any 
        # desired button of your choice 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # detect the window is closed by user
        if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            break
          
    # After the loop release the cap object 
    cap.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows()
    
    # plot signal 
    plot_singal(metrics.tracked_metrics, 
                mean=metrics.config['reference']['mean'], 
                title=f"Repetition: {metrics.reptition_count} for {exercise_name}")
except Exception as e:
    print(traceback.format_exc())
    cap.release()
    cv2.destroyAllWindows() 