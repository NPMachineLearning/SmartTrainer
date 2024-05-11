import cv2
import numpy as np
import time


WINDOW_NAME = "Frame"
FRAME_DELAY = 1./3. 

# configure vide cap
cap = cv2.VideoCapture("./gifs/pushup.gif")
cap_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

feature_params = dict(maxCorners = 100,
                      qualityLevel = 0.1,
                      minDistance = 10,
                      blockSize = 10)

lk_params = dict(winSize  = (10,10), 
                 maxLevel = 1,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

color = np.random.randint(0, 155, (100, 3))

try:
    cv2.namedWindow(WINDOW_NAME)
    cv2.moveWindow(WINDOW_NAME, 30, 40)
    
    _, frame = cap.read()
    old_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    old_pts = cv2.goodFeaturesToTrack(old_frame_gray, mask=None, **feature_params)
    
    frame_count = 1
        
    while(True):
        ret, frame = cap.read()
        if ret:
            frame_count += 1
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            new_pts, st, err = cv2.calcOpticalFlowPyrLK(old_frame_gray, 
                                                   frame_gray,
                                                   old_pts, 
                                                   None, 
                                                   **lk_params)
            valid_new_pts = new_pts[st==1]
            valid_old_pts = old_pts[st==1]
            for i, (v_old_pts, v_new_pts) in enumerate(zip(valid_old_pts, valid_new_pts)):
                a, b = v_old_pts.ravel()
                c, d = v_new_pts.ravel()
                a, b, c, d = int(a), int(b), int(c), int(d)
                frame = cv2.circle(frame, (c, d), 5, (0,0,255), -1)
                frame = cv2.line(frame, (a,b), (c, d), (0,0,255), 2)
                
            cv2.imshow(WINDOW_NAME, frame)
            
            old_frame_gray = frame_gray.copy()
            old_pts = new_pts[st==1].reshape(-1,1,2)
        else:
            if frame_count < cap_length:
                raise Exception(f"Unable to capture frame at {frame_count+1}")
            else:
                break
        
        cv2.setWindowTitle(WINDOW_NAME, f"Frame: {frame_count}/{cap_length}")
            
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
except Exception as e:
    print(e)
    cap.release()
    cv2.destroyAllWindows()