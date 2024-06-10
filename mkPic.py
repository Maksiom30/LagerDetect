import cv2 as cv

def mkPic():
    cap = cv.VideoCapture(0)
    _, frame = cap.read()
    cap.release()
    return frame