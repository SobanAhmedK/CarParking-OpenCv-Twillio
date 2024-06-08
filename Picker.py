import cv2 as cv
import pickle


width , height = 105 , 47

try:
    with open("Park_Positions" , "rb") as f:
        Positions = pickle.load(f)

except:
    Positions = []      
        
        
def click_point(events , x , y , flags ,params):
    if events == cv.EVENT_LBUTTONDOWN:
        Positions.append((x,y))
    elif events == cv.EVENT_RBUTTONDOWN:
        for i , pos in enumerate(Positions):
            
         
           X , Y = pos
           if X<x<X+width and Y<y<Y+height:
                 Positions.pop(i)
    with open("Park_Positions" , "wb") as f:
        pickle.dump(Positions, f)
        
while 1:
    area_img=cv.imread('Area_img.png')
    for pos in Positions:
    
       cv.rectangle(area_img , pos,(pos[0] + width,pos[1]+ height) ,(255,0,0) ,2)
       
    cv.imshow("Area" ,area_img)
    cv.setMouseCallback("Area" , click_point)
    cv.waitKey(1)

