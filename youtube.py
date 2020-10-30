import cv2
import time
import numpy as np
from matplotlib import pyplot as plt
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

videoName = r"TheChase360.mp4"


# Creates file called test1 consisting of 90 seconds from TheChase
ffmpeg_extract_subclip(videoName, 10, 100, targetname="test1.mp4")

def process_img(img_rgb, template, count):

    '''
    returns true if template img is somewhere in img_rgb
    '''

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        print(' in ptt!!dagfdfgasdg')
        print(pt)
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        cv2.imwrite('res{0}.png'.format(count),img_rgb)   
        return True
    
    return False

def findTimes():
    '''
    Finds a list of frames that start the minute of questions
    '''

    # start frame numbers
    startFrames = []

    vidcap = cv2.VideoCapture(videoName)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    print('fps is' + str(fps))
    template = cv2.imread(r"minute360.png",0)  # open template only once
    count = 0
    while True:
      success,image = vidcap.read()
      if not success: break         # loop and a half construct is useful
    #   print ('Read a new frame: ', success)
      if count % 20 ==0:
        # Check only every 20 frames for match
        if process_img(image, template, count):
            startFrames.append(count)

            # If found start, skip ahead 2 minutes
            for _ in range(3600):
                count += 1
                success,image = vidcap.read()
                if not success: break

      count += 1
    
    startTimes = [frame/fps for frame in startFrames]

    return startTimes
    

def run():


    start_time = time.time()
    startTimes = findTimes()
    print('startTimes are:')
    print(startTimes)
    print("--- %s seconds ---" % (time.time() - start_time))

run()