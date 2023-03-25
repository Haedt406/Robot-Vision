import cv2 as cv

src = cv.imread("japaneseflowers.jpg", 1)
if src is None:
    print("missing image")
else:
    cv.imshow("windowM", src)
    dim = src.shape
    
    print(dim)
    for row in range(dim[0]):
        for col in range(dim[1]):
                src[row][col][2]=0
    cv.imshow("windowMy", src)
                
                
                
