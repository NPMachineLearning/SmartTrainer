import cv2
import imageio
from pygifsicle import optimize
import os

# All setting should be base on
# v4l2-ctl --list-formats-ext
# and 
# sudo guvcview
# output and configuration
# otherwise it will not work in Linux
WINDOW_NAME = "Frame"
WINDOW_SIZE = (960, 540)
CAM_OUTPUT_FORMATE = "MJPG" 

# configure vide cap
vid = cv2.VideoCapture(0) 
vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*CAM_OUTPUT_FORMATE))
vid.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_SIZE[0])
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_SIZE[1])
vid.set(cv2.CAP_PROP_FPS, 30.)


# input frames to record
n_frames = int(input("Enter number of frames to record: "))

# frame tracker
frame_count = 0

# gif save path
save_dir  ="./gifs"
filename = "output.gif"

# create output directory
if not os.path.exists(save_dir):
    os.makedirs(save_dir, exist_ok=True)

# start webcame recording    
try:
    # configure window
    cv2.namedWindow(WINDOW_NAME)
    cv2.moveWindow(WINDOW_NAME, 30, 40)
    cv2.resizeWindow(WINDOW_NAME, WINDOW_SIZE[0], WINDOW_SIZE[1])
    
    with imageio.get_writer(os.path.join(save_dir, filename), fps=30) as writer:  
        while(frame_count < n_frames):
            # Capture the video frame 
            # by frame 
            ret, frame = vid.read()

            if vid.isOpened():
                if ret:
                    print(f"Recording frame {frame_count+1} / {n_frames}", end="\r", flush=True)
                    # save frame to gif
                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    writer.append_data(img)
                    
                    # display the resulting frame 
                    cv2.imshow(WINDOW_NAME, frame)
                    cv2.setWindowTitle(WINDOW_NAME, f"{WINDOW_NAME} | {vid.get(cv2.CAP_PROP_FPS)} FPS")
                    
                    frame_count += 1
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
        
        # optimize gif
        print("")        
        print("optimizing gif file....")
        optimize(os.path.join(save_dir, filename))
except Exception as e:
    print(e)
    vid.release()
    cv2.destroyAllWindows()

