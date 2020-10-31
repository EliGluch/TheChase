#!/usr/bin/python3

import os
import cv2
import sys
import time
import argparse
import downloader
import numpy as np
from matplotlib import pyplot as plt
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, concatenate_videoclips

minutePic     = r"minute360.png"

# Creates file called test1 consisting of 90 seconds from TheChase
# ffmpeg_extract_subclip(videoName, 10, 100, targetname="test1.mp4")
    
def_url = r'https://www.youtube.com/watch?v=ajKrcI-gIvM&t=248s' #the chase

def run(url):
    start_time = time.time()
    lowVideoName, highVideoName, episodeDate = downloader.downloadEpisode(url)
    startTimes = findTimes(lowVideoName, minutePic)
    print('startTimes are:')
    print(startTimes)
    createVideo(highVideoName, startTimes, episodeDate)
    print("--- %s seconds ---" % (time.time() - start_time))


def findTimes(video, img):
    '''
    Finds a list of frames in video that contain img.
    should corespond to beggining of question sections in The Chase Episode
    '''

    # start frame numbers
    startFrames = []

    template = cv2.imread(img, 0)  # open template only once
    vidcap   = cv2.VideoCapture(video)
    fps      = vidcap.get(cv2.CAP_PROP_FPS)
    count    = 0

    while True:
      success,image = vidcap.read()
      if not success: break         # loop and a half construct is useful
      if count % 20 ==0:
        # Check only every 20 frames for match
        if process_img(image, template, count):
            startFrames.append(count)

            # If found start of question section, skip ahead 2 minutes
            for _ in range(int(fps * 130)):
                count += 1
                success,image = vidcap.read() 
                if not success: break

      count += 1
    
    startTimes = [int(frame/fps) for frame in startFrames]

    return startTimes

def createVideo(video, times, videoDate):

  '''
  params:
    video - path to video to edit.
    times - list of integers - points to cut from.
  '''
  if len(times) is not 6:
    raise Exception("Error, expected exactly 6 times")

  clips        = []

  for i, startTime in enumerate(times):
    # The first 4 rounds are one minute long, the fifth is 2, and the last is more than 2
    endtime = startTime + 60 + 10

    if i == 4:
      endtime = startTime + 120 + 10

    if i == 5:
      endtime = -60


    # Cut clip of questoin section
    clip = VideoFileClip(video).subclip(t_start=startTime, t_end=endtime)
    clips.append(clip)

  final_clip = concatenate_videoclips(clips)

  final_clip.write_videofile("Video\\TheChaseHighlights-%s.mp4" % videoDate)

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
        print('Found frame')
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        return True
    
    return False

def main(args):

  for url in args:
    print(url)

    if not 'youtube' in url:
      print('Please enter youtube url')

    else:
        run(url)

if __name__ == "__main__":
   main(sys.argv[1:])