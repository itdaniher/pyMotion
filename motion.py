#!/usr/bin/python

# stupid-simple motion detection script with tons of dependencies

# get a frame, convert it to greyscale, convert it to a numpy array, smooth it, subtract from previous frame, and if threshold, save the pair of frames

import Image, requests, StringIO, numpy, time

import filterfft

# "best guess" threshold - seems to work alright with a bunch of false positives. 
threshold = 480*640*256/1000

def getImage():
	""" returns a 480x640 numpy array containing an image from a FOSCAM IP camera """
	imageFile = StringIO.StringIO(requests.get("http://192.168.1.116/snapshot.cgi?user=admin&pwd=").content)
	jpg = Image.open(imageFile)
	# ITU-R 601-2 luma
	jpg = jpg.convert("L")
	return jpg

def ImageToArray(jpg):
	a = numpy.fromstring(jpg.tostring(), "uint8").reshape((480,640))
	return a

def getSmoothedArray():
	a = ImageToArray(getImage())
	af = filterfft.filter(a, filterfft.gaussian(2))
	return af

def viewArray(a):
	Image.fromarray(a).show()

def oneTick():
	af = getSmoothedArray()
	bf = getSmoothedArray()
	# subtract images
	diff = numpy.abs(numpy.sum(bf-af))
	if diff > threshold:
		fa = open(str(time.time()).split('.')[0]+".a.jpg", "wb")
		fb = open(str(time.time()).split('.')[0]+".b.jpg", "wb")
		Image.fromarray(a.astype("uint8")).save(fa)
		Image.fromarray(b.astype("uint8")).save(fb)
	print diff

if __name__ == "__main__":
	while True:
		try:
			oneTick()
		except:
			print "napping"
			time.sleep(10)
