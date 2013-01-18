#!/usr/bin/python

import Image, numpy, time

import filterfft

from getFrameFromVideoStream import getImage
#from getFrameLocal import getImage

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


def checkMotion(a, b):
	c = numpy.abs(b-a)
	thresh = c.mean() * 5
	c = numpy.piecewise(c, [c > thresh, c <= thresh], [0xFF, 0])
	s = numpy.abs(numpy.sum(c))
	if s > 500000:
		return True
	else:
		return False

def oneTick():
	af = getSmoothedArray()
	bf = getSmoothedArray()
	if checkMotion(af, bf):
		for i in range(10):
			fname = str(time.time())+".jpg"
			getImage().save(fname)
			print "saved " + fname

if __name__ == "__main__":
	print "Welcome to motion - successfully launched."
	while True:
		try:
			oneTick()
		except:
			time.sleep(10)
