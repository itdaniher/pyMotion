import Image
import select
import time
import v4l2capture

def getImage():
	video = v4l2capture.Video_device("/dev/video0")
	
	video.set_format(640, 480)
	
	video.create_buffers(1)
	
	video.start()
	
	time.sleep(.1)
	
	video.queue_all_buffers()
	select.select((video,), (), ())
	image_data = video.read()
	video.close()

	img = Image.fromstring("RGB", (640, 480), image_data)
	return img

if __name__ = "__main__":
	getImage().show()
