# import the necessary packages
from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2

def compare_images(imageA, imageB):
	# compute the structural similarity
	print("Computing structural similarity...")
	s = ssim(imageA, imageB)
	#resultDict = {"MSE" : m, "SSIM" : s}
	resultDict = {"SSIM" : s}
	#print("MSE = " + str(m))
	#print("SSIM = " + str(s))
	#print(resultDict)
	return resultDict

# load the images
def checkBootImg(imageApath, imageBpath):
	print("Reading Images...")
	original = cv2.imread(imageApath)
	current = cv2.imread(imageBpath)
	#print(original.shape)
	#print(current.shape)
	#current = cv2.resize(current_org, original.shape)
	# convert the images to grayscale
	print("Converting Images to grayscale...")
	original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
	current = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)

	# compare the images
	print("Comparing Images...")
	result = compare_images(original, current)
	return result

#test = checkBootImg("images/dock2.png", "images/dock.png")
#print(test)