import cv2 as cv
import time
import torch

from Annotator import Annotator

class Stream:
    def __init__(self, camera, fps_updater=1):
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5x') # yolo_v5 model for inference
        self.cap = cv.VideoCapture(camera) # select camera for stream

        # initialize fps information
        self.fps = round(self.cap.get(cv.CAP_PROP_FPS),2) # get camera fps
        self.fps_iter = 1 # set current iteration for updating fps
        self.fps_t0 = 0. # define begin time for calculating fps
        self.fps_updater = fps_updater # indicates after how many frames fps should be updated

        # create annotator for annotating frames
        self.annotator = Annotator()
        self.annotator.generate_colors() # generate unique color for each class
    
    # updates fps info
    def update_fps(self):
        # only update after 'fps_updater' number of frames
        if self.fps_iter == self.fps_updater:
            dt = time.time() - self.fps_t0
            self.fps = round(self.fps_iter/dt,2)
            self.fps_iter = 0
            self.fps_t0 = time.time()
        self.fps_iter += 1
 
    # starts stream
    def start(self):
        self.fps_t0 = time.time() # set begin time for determining fps

        # start actual recording
        while(True):
            ret, frame = self.cap.read() # get current frame
            prediction = self.model(frame)  # inference
            self.update_fps() # updating fps

            # add fps info to frame
            self.annotator.add_text(frame,str(self.fps) + ' fps',(50,50),1,(0,255,0))

            # add bounding boxes to frame
            self.annotator.add_boxes(frame, prediction) 

            # show frame
            cv.imshow('frame', frame)

            # type 'q' to close stream
            if cv.waitKey(1) & 0xFF == ord('q'):
                break 

        # closing stream after while loop
        self.cap.release()
        cv.destroyAllWindows() 