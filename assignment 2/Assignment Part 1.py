import cv2 as cv
import numpy as np

global colors 
global lower
global higher
global lower1
global higher1
global lower2
global higher2
global lower_hsv
global higher_hsv
global lower_hsv1
global higher_hsv1
global lower_hsv2
global higher_hsv2
global erosion
global dilation
global main
main = np.ones((5,5,5),np.uint8)
erosion = np.array((5, 5), np.uint8)
dilation = np.array((5, 5), np.uint8)
colors, lower, higher, lower1, higher1, lower2, higher2 = 0,0,0,0,0,0,0
lower_hsv=np.array([0,0,0])
higher_hsv=np.array([1,1,1])
lower_hsv1=np.array([0,0,0])
higher_hsv1=np.array([1,1,1])
lower_hsv2=np.array([0,0,0])
higher_hsv2=np.array([1,1,1])
def mouseclick(event,x,y,flags,param):
    global lower_hsv
    global higher_hsv
    global lower_hsv1
    global higher_hsv1
    global lower_hsv2
    global higher_hsv2
    global erosion
    global dilation
    global main
    if event == cv.EVENT_LBUTTONDOWN: 
        h = hsv_img[y,x,0]
        s = hsv_img[y,x,1]
        v = hsv_img[y,x,2]
        main = np.ones((h,s,v),np.uint8)
        lower_hsv=np.array([0,0,0])
        higher_hsv=np.array([0,0,0])
        # colors = hsv_img[y,x]
        print("h: ",h)
        print("s: ",s)
        print("v: ",v)
        # print("BRG Format: ",colors)
        # print("Coordinates of pixel: X: ",x,"Y: ",y)
        lower_hsv=np.array([h-lower,s-lower,v-lower])
        higher_hsv=np.array([h+higher,s+higher,v+higher])

        erosion=np.array([h-lower1,s-lower1,v-lower1])
        erosion=np.array([h+higher1,s+higher1,v+higher1])
        
        lower_hsv2=np.array([h-lower2,s-lower2,v-lower2])
        higher_hsv2=np.array([h+higher2,s+higher2,v+higher2])
        # cv.createTrackbar('lower', "hsv_img", 0, 100, on_change)
        # cv.createTrackbar('higher', "hsv_img", 0, 100, on_change)
        
        # mask = cv.inRange(colors, lower_hsv, lower_hsv)
        # Bitwise-AND mask and original image
        # res = cv.bitwise_and(frame,frame, mask= mask)
        # cv.imshow('mask',mask)
        # cv.imshow('res',res)
        # cv.imshow('hsv_img',res)
       

def on_changel(value):
    global lower
    lower = value
def on_changeh(value):
    global higher
    higher = value
def on_changel1(value):
    global lower1
    lower1 = value
def on_changeh1(value):
    global higher1
    higher1 = value
def on_changel2(value):
    global lower2
    lower2 = value
def on_changeh2(value):
    global higher2
    higher2 = value
cap = cv.VideoCapture(0)
cv.namedWindow("Video")

status, img = cap.read()
cv.imshow("Video", img)
dim = img.shape
hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# width, height = dim[0], dim[1]
# cv.namedWindow('mouseclick')
# cv.setMouseCallback('mouseclick',mouseclick)
# b = 75* np.ones((width, height, 3), np.uint8)
# bright = cv.add(img, b)
cv.imshow("hsv_img", hsv_img)

cv.createTrackbar('lower', "hsv_img", 0, 100, on_changel)
cv.createTrackbar('higher', "hsv_img", 0, 100, on_changeh)
cv.createTrackbar('lower1', "hsv_img", 0, 100, on_changel1)
cv.createTrackbar('higher1', "hsv_img", 0, 100, on_changeh1)
cv.createTrackbar('lower2', "hsv_img", 0, 100, on_changel2)
cv.createTrackbar('higher2', "hsv_img", 0, 100, on_changeh2)
print("start")    
kernel_3 = np.ones((5,5),np.uint8)
while 1:
    status, img = cap.read()
    cv.imshow("Video", img)
    dim = img.shape
    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    
    # width, height = dim[0], dim[1]
    # cv.namedWindow('mouseclick')
    # cv.setMouseCallback('mouseclick',mouseclick)
    # b = 75* np.ones((width, height, 3), np.uint8)
    # bright = cv.add(img, b)
    cv.imshow("hsv_img", hsv_img)
    cv.setMouseCallback("hsv_img",mouseclick) 
    test = cv.dilate(hsv_img, None,iterations=1)
    # test2 = cv.erode(hsv_img, kernel_3, iterations=1)
    # cv.imshow("test", test)
    mask = cv.inRange(test, lower_hsv, higher_hsv)
    res = cv.bitwise_and(test,hsv_img, mask= mask)
    cv.imshow('mask',mask)
    cv.imshow('res',res)
    # cv.imshow('mask',mask)
    # cv.imshow('res',res)
    # mouseclick;
    # ret, frame = cap.read()
    # cv.imshow('mouseRGB', frame)
    # cv.setMouseCallback('image',mouseclick)

    k = cv.waitKey(1)
    if k == 27:
        break
  
cv.destroyAllWindows()
