import cv2 as cv

cap = cv.VideoCapture(1)
cv.namedWindow("Video")

print("start")    
while True:
    status, img = cap.read()
    cv.imshow("Video", img)
    hls = cv.cvtColor(img, cv.COLOR_RGB2HLS)
    cv.imshow("hls", hls)
    k = cv.waitKey(1)
    if k == 27:
        break

print(img)   
cv.destroyAllWindows()
