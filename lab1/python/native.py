import numpy as np
from PIL import Image
import argparse
from time import process_time as ptime

def disp(k, hist):
    P1 = 0;
    m = 0;
    m_g = 0;
    for i in range(k + 1):
        P1 = P1 + float(hist[i])
        m = m + float(hist[i]) * i
    for i in range(hist.size):
        m_g = m_g + float(hist[i]) * i;
    return (m_g * P1 - m) * (m_g * P1 - m) / (P1 * (1 - P1));

def get_thr(hist):
    k_max = 0
    d_max = 0
    for k in range(256):
        d = disp(k,hist)
        if d > d_max:
            d_max = d
            k_max = k
    return k_max

parser = argparse.ArgumentParser(description='Binarize image')
parser.add_argument('image', type=str)
parser.add_argument('-g', action='store_true', help='Show images using gui')
parser.add_argument('-o', help='Show images using gui')

args = parser.parse_args()

img = Image.open(args.image)
hist = img.histogram()
img = np.array(img)
hist = np.array(hist)
hist = hist / img.size

# for p in np.nditer(img, op_flags=["readwrite"]):
#     p = 255 if p > 127 else 0
start = ptime()
thr = get_thr(hist)
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        img[i,j] = 255 if img[i,j] > thr else 0
end = ptime()

print(end - start)

output = Image.fromarray(img)

if args.o:
    output.save(args.o)

if args.g:
    output.show()
