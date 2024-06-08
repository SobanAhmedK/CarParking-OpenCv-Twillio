import pickle
import cv2 as cv
import cvzone
import numpy

width , height = 105 , 47
capture = cv.VideoCapture("Parking_area.mp4")

with open("Park_Positions" , "rb") as f:
     positions = pickle.load(f)

while 1:
    if capture.get(cv.CAP_PROP_POS_FRAMES) == capture.get(cv.CAP_PROP_FRAME_COUNT):
        capture.set(cv.CAP_PROP_POS_FRAMES , 0)
  
    succes, area_img = capture.read()
    
    Gray_area_img = cv.cvtColor(area_img  , cv.COLOR_BGR2GRAY)
    Blur_area = cv.GaussianBlur(Gray_area_img , (3,3) , 1 )

    
    for pos in positions:
        x,y = pos
         
        Crop_Image = area_img[y:y+height , x:x+width] 
        cv.imshow(str(x * y ) , Crop_Image)
   
    for pos in positions:
       cv.rectangle(area_img , pos,(pos[0] + width,pos[1]+ height) ,(255,0,0) ,2)
          
   
    cv.imshow('Image' , area_img)
    cv.imshow('Image_Blur' , Blur_area)
    cv.waitKey(12)
 