from PIL import Image
import numpy as np
import math
import cv2

from constants import *

def preprocessImage(new_width, file_path, picture_number):
	thresh1 = cv2.imread(file_path,0)
#	imginfo = thresh1.shape[1::-1]
#	new_height = int((imginfo[1]/float(imginfo[0]))*new_width)
#	thresh1 = cv2.resize(thresh1, (new_width, new_height), interpolation = cv2.INTER_CUBIC)
	thresh1 = cv2.adaptiveThreshold(thresh1,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,15)
	cv2.imwrite('intermidiate/out'+picture_number+'.jpg',thresh1)
	cv2.imshow('image',thresh1)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return thresh1