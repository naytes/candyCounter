#Candy Color Detector
#Logan Shy and Nayte Chandler
import numpy as np
import cv2 as cv

kernal = np.ones((3,3), np.uint8) #kernel for bluring and dilate and erode
img = cv.imread("data/images/stitchedCandy.jpg", cv.IMREAD_COLOR) #tested on stitched image smaller tiny and worked almost perfect*** We missed only 2-3 M&Ms and miscolored only 1
img2 = img.copy()
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
eroded = cv.erode(img, kernal, iterations=2) #erode and dilate picture
dilated = cv.dilate(eroded, kernal, iterations=2)
blur = cv.blur(dilated, (3,3))
edges = cv.Canny(blur, 100, 200) #find edges

output = img.copy() #copy image
height, width = img.shape[:2]

black = np.zeros((height,width,3), np.uint8) #black image for binary output

circles = cv.HoughCircles(edges,cv.HOUGH_GRADIENT,1.5,20,
                            param1=50,param2=30,minRadius=4,maxRadius=30) #finds circles between radius 4 and 30 this max was plenty high for the test picture

def isRed(bgr): #functions that decide the color of M&M for all possible colors
    if bgr[2] < 210 and bgr[1] < 110 and bgr[0] < 150 and bgr[0] < bgr[2]:
        return True
def isGreen(bgr):
    if bgr[2] < 75 and bgr[1] > 110 and bgr[0] < 190:
        return True
def isYellow(bgr):
    if bgr[2] > 105 and bgr[1] > 135 and bgr[0] < 100:
        return True
def isOrange(bgr):
    if bgr[2] > 160 and bgr[1] > 10 and bgr[0] < 140:
        return True
def isBlue(bgr):
    if bgr[2] < 15 and bgr[1] > 100 and bgr[0] > 220:
        return True
    
def isBrown(bgr): #type casting all of these individually was the only way i could find to get rid of an error
    if (((int(bgr[0])+int(bgr[1])+int(bgr[2]))/3)-int(bgr[0])) < 10 and (((int(bgr[0])+int(bgr[1])+int(bgr[2])))/3)-int(bgr[0]) > -10:
        return True
    
global reds #made global variables for amount of each M&M
reds = 0
global blues
blues = 0
global greens
greens = 0
global oranges
oranges = 0
global yellows
yellows = 0
global browns
browns = 0
def get_dominant_color(image): #determines color based on bgr values sent in
    global reds
    global blues
    global greens
    global oranges
    global yellows
    global browns

    if isYellow(image): #the order of these functions is very important as some colors are easier to detect than others
        yellows = yellows + 1
        return "Yel"
        
    elif isGreen(image):
        greens = greens + 1
        return "Grn"
        
    elif isBlue(image):
        blues = blues + 1
        return "Blu"

    elif isBrown(image):
        browns = browns + 1
        return "Brn"
       
    elif isRed(image):
        reds = reds + 1
        return "Red"

    elif isOrange(image):
        oranges = oranges + 1
        return "Org"
    
    else: #browns were very hard to decide and some still werent found at end
        browns = browns + 1
        return "Brn"

circles = np.round(circles[0, :]).astype("int")
for (x, y, r) in circles:
    s = int(r-r/3) #scaler for squares that overlay M&Ms
    s2 = s/3
    cv.circle(black,(x,y),(r),(255,255,255),-5) #draws circles to binary image
    #print(r) #prints radius of each circle
    roi = cv.rectangle(output, (x - s-1, y - s-1), (x + s+1, y + s+1), (0, 0, 0), -1)
    color = blur[y,x]
    cv.rectangle(output, (x - s, y - s), (x + s, y + s), (int(color[0]), int(color[1]), int(color[2])), -1)
    #print(color) #prints bgr values of each circle
    stri = get_dominant_color(color) #determines color and saves string value to stri
    if stri == "Yel": #made "Yel" black so its easier to read
        cv.putText(output, stri, (x-s,y+s), cv.FONT_HERSHEY_SIMPLEX, .5, (0,0,0), 2, cv.LINE_AA)
    else:
        cv.putText(output, stri, (x-s,y+s), cv.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 2, cv.LINE_AA)

totalAll = reds + yellows + blues + greens + oranges + browns 
print("Total M&Ms found: ", totalAll) #prints total
print("reds: ", reds) #prints amount of each color
print("yellows: ", yellows)
print("blues: ", blues)
print("greens: ", greens)
print("oranges: ", oranges)
print("browns: ", browns)

cv.imshow("origin", img2)
cv.imshow("binary", black)
cv.imshow("original", output)
cv.imshow("edges", edges)

cv.waitKey(0)
cv.destroyAllWindows()

