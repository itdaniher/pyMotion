import Image
import time, urllib2, base64


def getImage():
	# Basic HTTP Authentication...
	url = 'http://192.168.1.116/videostream.cgi?user=admin&resolution=C&rate=6'
	ww = 'admin:'
	encodedstring = base64.encodestring(ww)[:-1]
	auth = "Basic %s" % encodedstring
	req = urllib2.Request(url,None, {"Authorization": auth })
	handle = urllib2.urlopen(req)
	
	def read_stream():
		buf = ''
		b = handle.readlines(45)
		for a in b:
			if a.startswith('Content-Length'):
				readlen = str(a).split()[1]
		b1 = handle.read(int(readlen)+4)
		return b1
	
	def parse_stream():
		jpg = read_stream()
		img = Image.fromstring('RGB',(640,480),jpg[2:], 'jpeg', 'RGB', None)
		return img

	return parse_stream()

if __name__ == "__main__":
	while True:
		getImage().show()
		time.sleep(1)
