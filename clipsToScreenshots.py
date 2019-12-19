# Adapted from https://stackoverflow.com/questions/30136257/how-to-get-image-from-video-using-opencv-python

import cv2
import os

def video_to_frames(video, path_output_dir):
    # extract frames from a video and save to directory as 'x.png' where 
    # x is the frame index
    vidcap = cv2.VideoCapture(video)
    count = 0
    FRAME_COUNT = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    NUMBER_OF_SS = 30
    FRAME_INCREMENT = int(FRAME_COUNT / NUMBER_OF_SS)
    while vidcap.isOpened():
        success, image = vidcap.read()
        if success:
            if count % FRAME_INCREMENT == 0:
                cv2.imwrite(os.path.join(path_output_dir, '%d.png') % count, image)
                #print("used")
            #else:
                #print("not used:", count % FRAME_INCREMENT)
            count += 1
        else:
            break
    cv2.destroyAllWindows()
    vidcap.release()

video_to_frames('data/test.mp4', 'data/test/screenshots')