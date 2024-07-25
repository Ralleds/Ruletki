import cv2
import sys
import numpy as np
import pyscreenshot as ImageGrab


def shift_channel(c, amount):
    if amount > 0:
        lim = 255 - amount
        c[c >= lim] = 255
        c[c < lim] += amount
    elif amount < 0:
        amount = -amount
        lim = amount
        c[c <= lim] = 0
        c[c > lim] -= amount
    return c


def nothing(x):
    pass

# Create a window
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('HMin','image',0,179,nothing) # Hue is from 0-179 for Opencv
cv2.createTrackbar('SMin','image',0,255,nothing)
cv2.createTrackbar('VMin','image',0,255,nothing)
cv2.createTrackbar('HMax','image',0,179,nothing)
cv2.createTrackbar('SMax','image',0,255,nothing)
cv2.createTrackbar('VMax','image',0,255,nothing)

# Set default value for MAX HSV trackbars.
cv2.setTrackbarPos('HMax', 'image', 179)
cv2.setTrackbarPos('SMax', 'image', 255)
cv2.setTrackbarPos('VMax', 'image', 255)

cv2.createTrackbar('SAdd','image',0,255,nothing)
cv2.createTrackbar('SSub','image',0,255,nothing)
cv2.createTrackbar('VAdd','image',0,255,nothing)
cv2.createTrackbar('VSub','image',0,255,nothing)

# Initialize to check if HSV min/max value changes
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

screenshot = ImageGrab.grab(bbox=(int(1920 / 3.92), int(1080 / 3.22), int(1920 / 1.43), int(1080 / 1.97)))
screenshot = np.array(screenshot)
# sharp_filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
# screenshot = cv2.filter2D(screenshot, ddepth=-1, kernel=sharp_filter)

output = screenshot
waitTime = 33

while(1):

    # get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin','image')
    sMin = cv2.getTrackbarPos('SMin','image')
    vMin = cv2.getTrackbarPos('VMin','image')

    hMax = cv2.getTrackbarPos('HMax','image')
    sMax = cv2.getTrackbarPos('SMax','image')
    vMax = cv2.getTrackbarPos('VMax','image')

    SAdd = cv2.getTrackbarPos('SAdd', 'image')
    SSub = cv2.getTrackbarPos('SSub', 'image')
    VAdd = cv2.getTrackbarPos('VAdd', 'image')
    VSub = cv2.getTrackbarPos('VSub', 'image')

    # Create HSV Image and threshold into a range.
    hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)

    # add/subtract saturation and value
    h, s, v = cv2.split(hsv)
    s = shift_channel(s, SAdd)
    s = shift_channel(s, -SSub)
    v = shift_channel(v, VAdd)
    v = shift_channel(v, -VSub)
    hsv = cv2.merge([h, s, v])

    # Set minimum and max HSV values to display
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Apply the thresholds
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(screenshot,screenshot, mask= mask)

    # Print if there is a change in HSV value
    if( (phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
        print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax

    # Display output image
    cv2.imshow('image',output)

    # Wait longer to prevent freeze for videos.
    if cv2.waitKey(waitTime) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()