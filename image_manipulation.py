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
	#cv2.imshow('image',thresh1)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return thresh1
	

def findText(new_width, file_path, picture_number):
	image = Image.open(file_path)
	image = resize(image, new_width, picture_number)
	image = toGreyscale(image, picture_number)
	image = toBW(image, picture_number)
	return image

def resize(image, new_width, picture_number):
	old_width, old_height = image.size	
	new_height = int((old_height/float(old_width))*new_width)
	image = image.resize((new_width,new_height))
	image.save('intermidiate/outa{}.jpg'.format(picture_number))
	return image

def toGreyscale(image, picture_number):
	im = np.asarray(image)
	im.setflags(write=1)
	for i in range(im.shape[0]):
		for j in range(im.shape[1]):
			r = int(im[i][j][0])
			g = int(im[i][j][1])
			b = int(im[i][j][2])
			gr = (r+g+b)/3.0
			im[i][j][0]=gr;
			im[i][j][1]=gr;
			im[i][j][2]=gr;
	image = Image.fromarray(im,'RGB')
	image.save('intermidiate/outb{}.jpg'.format(picture_number))
	return image

def toBW(image, picture_number):
	im = np.asarray(image)
	im.setflags(write=1)
	border = findBorder(im)
	for i in range(im.shape[0]):
		for j in range(im.shape[1]):
			if im[i][j][0] >= border:
				im[i][j]=[255,255,255]
			else:
				im[i][j]=[0,0,0]
	image = Image.fromarray(im)
	image.save('intermidiate/outc{}.jpg'.format(picture_number))
	return image

def findBorder(image):
	res = []
	for i in range(1,image.shape[0]-1):
		for j in range(1,image.shape[1]-1):
			if math.fabs( int(image[i][j][0]) - int(image[i-1][j-1][0]) ) > diff:
				res.append(image[i][j][0])
			elif math.fabs( int(image[i][j][0]) - int(image[i-1][j][0]) ) > diff:
				res.append(image[i][j][0])
			elif math.fabs( int(image[i][j][0]) - int(image[i-1][j+1][0]) ) > diff:
				res.append(image[i][j][0])
			elif math.fabs( int(image[i][j][0]) - int(image[i][j-1][0]) ) > diff:
				res.append(image[i][j][0])
			elif math.fabs( int(image[i][j][0]) - int(image[i][j+1][0]) ) > diff:
				res.append(image[i][j][0])
			elif math.fabs( int(image[i][j][0]) - int(image[i+1][j-1][0]) ) > diff:
				res.append(image[i][j][0])
			elif math.fabs( int(image[i][j][0]) - int(image[i+1][j][0]) ) > diff:
				res.append(image[i][j][0])
			elif math.fabs( int(image[i][j][0]) - int(image[i+1][j+1][0]) ) > diff:
				res.append(image[i][j][0])
	avg = 0
	for i in range(len(res)):
		avg+=res[i]
	avg/=len(res)	
	return avg

'''def divideLines(image, number):
	image_num = 0
	images = []
	im = np.asarray(image)
	im.setflags(write=1)
	for i in range(im.shape[0]):
		print(numBlacks(im[i]))

def numBlacks(row):
	num = 0
	for i in range(row.shape[0]):
		if row[i][0] == 0:
			num+=1
	return num'''



