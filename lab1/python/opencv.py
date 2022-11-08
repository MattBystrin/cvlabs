import cv2 as cv
import numpy as np
import argparse
from time import process_time as ptime

parser = argparse.ArgumentParser(description='Binarize image')
parser.add_argument('image', type=str)
parser.add_argument('-g', action='store_true', help='Show images using gui')
parser.add_argument('-o', help='Show images using gui')

args = parser.parse_args()
img = cv.imread(args.image,0)

start = ptime()
ret, bin = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
end = ptime()

if args.o:
    cv.imwrite(args.o, bin)

if args.g:
    render = True
    while True:
        key = cv.waitKey(0)
        if key == 27:
            break
        elif key == ord('n'):
            render = not render
        if render:
            cv.imshow('grayscale', img)
        else:
            cv.imshow('grayscale', bin)

print(end - start)
