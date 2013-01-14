#!/usr/bin/python

# stupid-simple motion detection script with tons of dependencies

# get a frame, convert it to greyscale, convert it to a numpy array, smooth it, subtract from previous frame, and if threshold, save the pair of frames

import Image, requests, StringIO, numpy, time

import filterfft

#import getFrameFromVideoStream.getImage as getImage
import getFrameLocal.getImage as getImage

# "best guess" threshold - seems to work alright with a bunch of false positives. 
threshold = 480*640*256/500

def ImageToArray(jpg):
	# converts image to greyscale, load as numpy array
	a = numpy.fromstring(jpg.convert("L").tostring(), "uint8").reshape((480,640))
	return a

def getSmoothedArray():
	a = ImageToArray(getImage())
	af = filterfft.filter(a, filterfft.gaussian(2))
	return af

def viewArray(a):
	Image.fromarray(a).show()

def checkMotion():
	af = getSmoothedArray()
	bf = getSmoothedArray()
	# subtract images, sum results
	diff = int(numpy.abs(numpy.sum(bf-af)))
	print diff
	if diff > threshold:
		return True
	else:
		return False

def oneTick():
	if checkMotion():
		for i in range(10):
			fname = str(time.time())+".jpg"
			getImage().save(fname)
			print "saved " + fname

if __name__ == "__main__":
	while True:
		try:
			oneTick()
		except:
			time.sleep(10)
