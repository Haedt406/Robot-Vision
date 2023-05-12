import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
# cv.namedWindow("Video")
status, img = cap.read()
status, img2 = cap.read()
average = np.float32(img)
src = cv.cvtColor(img,cv.COLOR_BGR2GRAY)    
# cv.imshow("gray", src)
# cv.imshow("32F, 3 channel image", cv.cvtColor(img, cv.COLOR_BGR2GRAY))
# cv.imshow("image1", img2)
diff = cv.absdiff(img,img2)
# cv.imshow("absdiff", diff)


dim = img.shape

while 1:
    status, img = cap.read()
    status, img2 = cap.read()
    # cv.imshow("img", img)
    
    width, height = dim[0], dim[1]
    b = 75* np.ones((width, height, 3), np.uint8)
    bright = cv.add(img, b)
    # cv.imshow("Bright", bright)
    dst = cv.GaussianBlur(bright, (1,1),0)

    dst = cv.accumulateWeighted(dst, average, 0.5)
    dst = cv.convertScaleAbs(dst)

    diff = cv.absdiff(img,dst)

    dst = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

    _,thresh = cv.threshold(dst, 0,20, cv.THRESH_BINARY)


    dst = cv.GaussianBlur(dst,(1,1),0)
    # cv.imshow("tellst", dst)

    _,thresh = cv.threshold(dst, 50,200, cv.THRESH_BINARY)

    # dst,_ = cv.findContours(dst)
    contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE) 
    with_contours = cv.drawContours(dst,contours,-1,(255,255,0),2)
    
    for c in contours:
          (x,y,w,h)=cv.boundingRect(c)
          cv.rectangle(img,(x,y), (x+w,y+h), (155,255,0),4)
    
    cv.imshow("test", img)

    k = cv.waitKey(5)
    if k == 27:
            break
  



cv.destroyAllWindows()



# import cv2 as cv
# import numpy as np

# cap = cv.VideoCapture(0)
# cv.namedWindow("Video")
# status, img = cap.read()
# status, img2 = cap.read()
# dim = img.shape
# average = np.float32(img)
# while 1:

#     status, img = cap.read()
#     cv.imshow("image1", img)
#     dim = img.shape
#     src = cv.cvtColor(img,cv.COLOR_BGR2GRAY)    
#     cv.imshow("gray", src)
 
    
#     ret, img2 = cap.read()
#     width, height = dim[0], dim[1]
#     b = 75* np.ones((width, height, 3), np.uint8)
#     bright = cv.add(img, b)
#     cv.imshow("Bright", bright)
#     dst = cv.blur(img, (5,5))
#     can = cv.Canny(dst, 10,40)
#     cv.imshow("blur", dst)            
#     # cv.accumulateWeighted(dst)
#     # cv.imshow("accumulateWeighted", dst) 
#     cv.accumulateWeighted(img, average, 0.5)
#     frameDelta = cv.absdiff(img, cv.convertScaleAbs(average))
#     # cv.convertScaleAbs()
#     diff = cv.absdiff(img,img2)
#     gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
#     blur = cv.GaussianBlur(gray, (5,5),0)
#     _, thresh = cv.threshold(blur, 50,200, cv.THRESH_BINARY)
#     dilated = cv.dilate(thresh, None, iterations=3)
#     contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
#     # cv.drawContours(img, contours, -1,(155,155,), 2)
#     for contour in contours:
#         (x, y, w, h) = cv.boundingRect(contour)

#         if cv.contourArea(contour) < 900:
#             continue
#         cv.rectangle(img, (x, y), (x+w, y+h), (155, 255, 0), 5)
#         # cv.putText(img, "Status: {}".format('Movement'), (10, 20), cv.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 3)
#     cv.imshow("feed", img)
#     k = cv.waitKey(5)
#     if k == 27:
#             break
  
# cv.destroyAllWindows()
