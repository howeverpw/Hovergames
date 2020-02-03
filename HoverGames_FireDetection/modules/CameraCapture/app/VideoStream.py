
from __future__ import absolute_import

from threading import Thread
import sys
if sys.version_info[0] < 3:  # e.g python version <3
    import cv2
else:
    import cv2
    from cv2 import cv2




if sys.version_info >= (3, 0):
    from queue import Queue

else:
    from Queue import Queue



class VideoStream(object):
    def __init__(self, path, queueSize=3):
        self.stream = cv2.VideoCapture(path)
        self.stopped = False
        self.Q = Queue(maxsize=queueSize)

    def start(self):
        # start a thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        try:
            while True:
                if self.stopped:
                    return

                if not self.Q.full():
                    (grabbed, frame) = self.stream.read()

                    # if the `grabbed` boolean is `False`, then we have
                    # reached the end of the video file
                    if not grabbed:
                        self.stop()
                        return

                    self.Q.put(frame)

                    # Clean the queue to keep only the latest frame
                    while self.Q.qsize() > 1:
                        self.Q.get()
        except Exception as e:
            print("got error: "+str(e))

    def read(self):
        return self.Q.get()

    def more(self):
        return self.Q.qsize() > 0

    def stop(self):
        self.stopped = True

    def __exit__(self, exception_type, exception_value, traceback):
        self.stream.release()
