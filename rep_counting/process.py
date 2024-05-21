import os
import sys
sys.path.insert(0, os.getcwd())
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import traceback 
import tensorflow as tf
import argparse
import json
import numpy as np
import cv2
import time
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from movenet.movenet_infer import load_model, predict, preprocess_input_image, preprocess_kps, INPUT_SIZE
from pkg.kps_metrics_jumping_jack import KpsMetricsJumpingJack
from pkg.kps_metrics_push_up import KpsMetricsPushup

WINDOW_FRAME = "Frame"
# FRAME_DELAY = 1./30.
DEFAULT_OUTPUT_DIR = "./smart_trainer_config"

exercise_metrics = {
    "jumpingjack": KpsMetricsJumpingJack(),
    "pushup": KpsMetricsPushup()
}

def main(vid_path, exercise_name, output_directory=DEFAULT_OUTPUT_DIR):
    if not os.path.exists(vid_path):
        raise Exception(f"{vid_path} doesn't exists")
    if not os.path.isfile(vid_path):
        raise Exception(f"{vid_path} is not a file")
    
    try:
        # load model
        model, input_details, output_details = load_model()
        
        # get get metrics object for exercise
        metrics = exercise_metrics.get(exercise_name, None)
        if metrics is None:
            raise Exception(f"Unable to find exercise name {exercise_name}")
        
        # track all metrics
        tracks = {e.name: [] for e in metrics.get_metric_names()}
        
        cv2.namedWindow(WINDOW_FRAME)
        cv2.moveWindow(WINDOW_FRAME, 30, 40)

        cap = cv2.VideoCapture(str(vid_path))
            
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                input_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                input_img = tf.convert_to_tensor(input_img)
                input_img = preprocess_input_image(input_img, INPUT_SIZE)
                kps = predict(input_img, model, input_details, output_details)
                kps = preprocess_kps(kps)
                metrics.update_metrics(kps)
                exercise_state = metrics.get_metrics()
                for track_name, track_metrics in tracks.items():
                    track_metrics.append(exercise_state[track_name])
                
                cv2.imshow(WINDOW_FRAME, frame)
            else:
                break
            
            cv2.setWindowTitle(WINDOW_FRAME, f"{exercise_name}")
                
            # the 'q' button is set as the 
            # quitting button you may use any 
            # desired button of your choice 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # detect the window is closed by user
            if cv2.getWindowProperty(WINDOW_FRAME, cv2.WND_PROP_VISIBLE) < 1:
                break
            
        # After the loop release the cap object 
        cap.release() 
        # Destroy all the windows 
        cv2.destroyAllWindows()
        
        # filter stationary movement wave
        # and names
        filter_tracks = []
        filter_metric_names = []
        for name, mc in tracks.items():
            if name.endswith("dist") and np.std(mc)>=0.04:
                filter_tracks.append(mc)
                filter_metric_names.append(name)
            if name.endswith("angle") and np.std(mc)>=10.:
                filter_tracks.append(mc)
                filter_metric_names.append(name)
        
        # sum up all remaining tracks that are not
        # stationary
        tracks_sum = np.sum(filter_tracks, axis=0)
        
        # data
        statistics = {}
        statistics['mean'] = np.mean(tracks_sum)
        statistics['std'] = np.std(tracks_sum)
        statistics['width'] = INPUT_SIZE[1]
        statistics['height'] = INPUT_SIZE[0]
        statistic_data = {"motion_names": filter_metric_names,
                          "reference": statistics}
        
        # create directory if not exists
        if not os.path.isdir(output_directory):
            os.makedirs(output_directory)
        
        # save config file
        output_filename = os.path.join(output_directory, 'config.json')
        if os.path.isfile(output_filename):
            with open(output_filename, 'r') as f:
                config_data = json.load(f)
                config_data[exercise_name] = statistic_data
            with open(output_filename, 'w') as f:
                f.write(json.dumps(config_data))
        else:    
            with open(output_filename, "w") as f:
                config_data = {exercise_name: statistic_data}
                f.write(json.dumps(config_data))
        
        # plot result
        plt.plot(list(range(tracks_sum.shape[0])), tracks_sum, label="signals")
        plt.hlines([tracks_sum.mean(), tracks_sum.mean()], 
                   [0.], 
                   [tracks_sum.shape[0]-1], 
                   colors="black", 
                   linestyles="dashed",
                   label=f"mean {statistics['mean']:.2f}")
        plt.ylabel(f"sum of signals per frames")
        plt.xlabel("frames")
        plt.title(f"{exercise_name} sum of signals")
        plt.legend()
        plt.show()
        
    except Exception as e:
        print(traceback.format_exc())
        cap.release()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Processing exercise video and output config file",
                                     description="""This program process exercise video and add
                                     configuration data into config json file.
                                     """)
    parser.add_argument("--video", help="Path to video file", required=True)
    parser.add_argument("--exercise_name", help="Exercise name to be processed", required=True)
    parser.add_argument("--output_directory", help="Output directory", required=False, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    
    main(args.video, args.exercise_name.lower(), args.output_directory)
    # main("./gifs/squat.gif","JumpingJack".lower())