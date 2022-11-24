#!/bin/python3

import cv2 as cv
import argparse
import math
from time import process_time as ptime

def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p1[1])**2)

def pattern_match(template: str, image: str):
    img = cv.imread(image, cv.IMREAD_GRAYSCALE)
    tplt = cv.imread(template, cv.IMREAD_GRAYSCALE)
    w,h = tplt.shape[::-1]
    res = cv.matchTemplate(img, tplt, cv.TM_CCORR_NORMED)
    _, _, _, max_loc = cv.minMaxLoc(res)
    br = (max_loc[0] + w, max_loc[1] + h)
    cv.rectangle(img, max_loc, br, 255, 2)
    print(max_loc, br)
    return img

def orb_match(template, image):
    img = cv.imread(image, cv.IMREAD_GRAYSCALE)
    tpl = cv.imread(template, cv.IMREAD_GRAYSCALE)
    w,h = tpl.shape[::-1]
    orb = cv.ORB_create(edgeThreshold = 0, fastThreshold = 0)

    tplKP, tplDes = orb.detectAndCompute(tpl, None)
    imgKP, imgDes = orb.detectAndCompute(img, None)

    matcher = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(tplDes, imgDes)

    matches = sorted(matches, key = lambda x:x.distance)

    final_img = cv.drawMatches(tpl, tplKP, img, imgKP, matches[:20], None)

    # Find matched points on template
    (x1, y1) = imgKP[matches[0].trainIdx].pt
    train_dist = dist(imgKP[matches[0].trainIdx].pt, imgKP[matches[1].trainIdx].pt)
    
    (x2, y2) = tplKP[matches[0].queryIdx].pt
    query_dist = dist(tplKP[matches[0].queryIdx].pt, tplKP[matches[1].queryIdx].pt)

    scale = train_dist/query_dist
    print(scale)

    tl = (int(x1 - x2*scale), int(y1 - y2*scale))
    br = (int(tl[0] + w*scale), int(tl[1] + h*scale))

    cv.rectangle(img, tl, br, 255, 2)

    return img

def main():
    parser = argparse.ArgumentParser(description="Pattern match image search")
    parser.add_argument("-t", "--type", type=str, help="Type of search",
            choices=["orb", "pmatch"])
    parser.add_argument("template", type=str, help="What to find")
    parser.add_argument("image", type=str, help="Where to find")
    parser.add_argument("-o", "--output", type=str, help="Result output")
    parser.add_argument("-g", "--gui", action="store_true", help="Use gui mode")
    args = parser.parse_args()
    output = None
    start = ptime()
    if args.type == "orb":
        output = orb_match(args.template, args.image)
    else:
        output = pattern_match(args.template, args.image)
    end = ptime()

    if args.output:
        cv.imwrite(args.output, output)

    if args.gui:
        cv.imshow("result", output)
        while cv.waitKey(0) != 27:
            pass
    print("time " + args.type + " " + str(end - start))


if __name__ == "__main__":
    main()
