#!/usr/bin/python

import Image, requests, StringIO


def getImage():
	""" returns a 480x640 numpy array containing an image from a FOSCAM IP camera """
	imageFile = StringIO.StringIO(requests.get("http://192.168.1.116/snapshot.cgi?user=admin&pwd=").content)
	jpg = Image.open(imageFile)
	return jpg

if __name__ == "__main__":
	getImage().show()
