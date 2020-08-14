import numpy as np
import cv2
import argparse
import datetime
import imutils
import time

#create arg parser
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

if args.get("video", None) is None:
    cap = cv2.VideoCapture(0)
    time.sleep(.5)
else:
    cap = cv2.VideoCapture(args["video"])

firstFrame = None

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = frame if args.get("video", None) is None else frame[1]
    text = "unoccupied"
    frame = cv2.flip(frame, 0)

    # Our operations on the frame come here
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # initialize firstFrame for motion detection
    if firstFrame is None:
        firstFrame = gray
        continue

    # threshold = background model - current frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    #loop over the contours
    for c in cnts:
	# if contour is too small then ignore
        if cv2.contourArea(c) < args["min_area"]:
            continue

	# compute bounding box
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "occupied"

    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
#    cv2.imshow("Thresh", thresh)
#    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
cap.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
