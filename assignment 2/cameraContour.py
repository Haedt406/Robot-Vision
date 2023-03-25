import cv2 as cv

capture = cv.VideoCapture(1)

if capture == None:
	print ("NULL")
else:
	print ("OK")
	
print ("subscribe done")

cv.namedWindow("original", 1)
cv.namedWindow("Canny", 1)

while(True):
    status, frame = capture.read()
    displayImage = frame.copy()
    gray= cv.cvtColor(frame,cv.COLOR_BGR2GRAY) 
    ret, thresh = cv.threshold(gray,127,255,0) 
	#calculate the contours from binary image
    contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE) 
    with_contours = cv.drawContours(frame,contours,-1,(255,0,0),3) 
    
    cv.imshow("original", gray)
    cv.imshow("Canny", with_contours)
    if cv.waitKey(10) == 27:
        break
   
cv.destroyAllWindows()
