import pickle
import cv2 as cv
import cvzone
import numpy
from twilio.rest import Client

width , height = 105 , 47
capture = cv.VideoCapture("Parking_area.mp4")

with open("Park_Positions" , "rb") as f:
     positions = pickle.load(f)
     
account_sid = ''
auth_token = ''
twilio_number = ''
admin_number = ''

client = Client(account_sid, auth_token)
notification_sent = False

def send_sms(message):
    client.messages.create(
        body=message,
        from_=twilio_number,
        to=admin_number
    )

while 1:
    if capture.get(cv.CAP_PROP_POS_FRAMES) == capture.get(cv.CAP_PROP_FRAME_COUNT):
        capture.set(cv.CAP_PROP_POS_FRAMES , 0)
  
    succes, area_img = capture.read()
    
    Gray_area_img = cv.cvtColor(area_img  , cv.COLOR_BGR2GRAY)
    Blur_area = cv.GaussianBlur(Gray_area_img , (5,5) , 2 )
    Thresh_holding = cv.adaptiveThreshold ( Blur_area , 255 , cv.ADAPTIVE_THRESH_GAUSSIAN_C , cv.THRESH_BINARY_INV , 25, 16 , )
    median_Blur = cv.medianBlur(Thresh_holding  , 5 )
    Dilated_image = cv.dilate( median_Blur ,numpy.ones((3,3) ,numpy.uint8) , iterations= 2)
    counter= 0
    for pos in positions:
        x,y = pos
         
        Crop_Image = Dilated_image[y:y+height , x:x+width] 
        # cv.imshow(str(x * y ) , Crop_Image)
        count = cv.countNonZero(Crop_Image)
        cvzone.putTextRect(area_img , str(count) , (x , y+height -4), scale=1 , thickness=2, offset=0 ,colorR=(255, 0, 0))
        
        if count<1100:
            color = (0,255,0)
            thickness=5
            counter+=1
        else:
            color = (0,0,2555)
            thickness = 2
        cv.rectangle(area_img , pos,(pos[0] + width,pos[1]+ height) ,color ,thickness)
        cvzone.putTextRect(area_img , f"Spaces free : {counter}" , (50 , 50), scale=2 , thickness=3, offset=10 ,colorR=(0, 255, 0))
        
        # if counter == 14 and not notification_sent:
        #   send_sms("14  more parking spaces are empty.")
        #   notification_sent = True
        # elif counter < 14:
        #   notification_sent = False
          
  
  
    cv.namedWindow("Image", cv.WINDOW_NORMAL)  
    cv.resizeWindow("Image", 1500, 770)  

    cv.imshow('Image' , area_img)
    cv.waitKey(12)
 