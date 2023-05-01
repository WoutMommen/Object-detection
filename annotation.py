import cv2 as cv
import yaml
import random

from Utils import value_to_key, df_to_intlist

class Annotator:
    def __init__(self):
        random.seed(10)
        self.colors, self.name_encoding = self.generate_colors()

    # generate a unique color for each class
    def generate_colors(self):
        with open("class_names.yaml", 'r') as stream:
            out = yaml.safe_load(stream)
            name_encoding = out['names']
            colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(name_encoding))] 
        return colors, name_encoding
 
    # set class variables needed for creating boxes
    def set_box_info(self, prediction):
        df = prediction.pandas().xyxy[0]
        self.name = df.loc[:,'name'].values.tolist()
        self.confidence = df.loc[:,'confidence'].values.tolist()
        self.xmin = df_to_intlist(df,'xmin')
        self.xmax = df_to_intlist(df,'xmax')
        self.ymin = df_to_intlist(df,'ymin')
        self.ymax = df_to_intlist(df,'ymax')
    
    # add bounding boxes to frame
    def add_boxes(self, frame, prediction): 
        self.set_box_info(prediction)
        for i in range(len(self.name)):
            self.add_one_box(frame, self.name[i], self.confidence[i], self.xmin[i], self.xmax[i], self.ymin[i], self.ymax[i])

    # add bounding box for one detected object
    def add_one_box(self,img, name, conf, xmin, xmax, ymin, ymax):
        start_point = (xmin, ymin)  
        end_point = (xmax, ymax) 
        idx = value_to_key(self.name_encoding, name)
        color = self.colors[idx]
        thickness = 2
    
        cv.rectangle(img, start_point, end_point, color, thickness)
        cv.rectangle(img, (xmin,ymin-30), (xmin+150+len(name)*10,ymin), color,-1)
        self.add_text(img, name + ' - ' + str(round(conf*100, 2)) + ' %',(xmin+10,ymin-10),0.6,(255,255,255))

    # add text on frame
    def add_text(self,frame,text,loc,size,col):
        font                   = cv.FONT_HERSHEY_SIMPLEX
        thickness              = 2
        lineType               = 2

        cv.putText(frame, text, loc, font, size, col, thickness, lineType)