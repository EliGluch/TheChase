# python -m pip install git+https://github.com/nficano/pytube 

import os
import re
import pytube
from pytube import YouTube
# url = r'https://www.youtube.com/watch?v=pkQRyZ707Gs'
# # url = r'http://www.youtube.com/watch?v=5FzAu6Xyx3s' 

# url = r'https://www.youtube.com/watch?v=ajKrcI-gIvM&t=248s' #the chase

# url = r'https://www.youtube.com/watch?v=qCT0bN-oGQo'


def downloadEpisode(url):

    '''
    Downloads the video given in url 360p and 720p
    '''

    youtube = pytube.YouTube(url)

    # Find datein name of video
    try:
        name = youtube.title

        # Search for date in video title, for example 15.09.2019
        match = re.search(r'\d{1,2}\.\d{2}\.\d{4}', name)
        print(match.group())

        # Convert date to be joined by '-' instead of '.'
        episodeDate = '-'.join(match.group().split('.'))
        print(episodeDate)

    except:
        print('Error extracting date')
        episodeDate = 'No-Date'

    lowQepisode  = 'Video\\TheChase360-%s.mp4' % episodeDate
    highQepisode = 'Video\\TheChase720-%s.mp4' % episodeDate

    # Download 360p
    stream = youtube.streams.filter(progressive=True, file_extension='mp4', res="360p").order_by('resolution').desc().first()
    output_file = stream.download(output_path='Video')
    os.replace(output_file, lowQepisode)

    # Download 720p
    stream = youtube.streams.filter(progressive=True, file_extension='mp4', res="720p").order_by('resolution').desc().first()
    output_file = stream.download(output_path='Video')
    os.replace(output_file, highQepisode)

    return (lowQepisode, highQepisode, episodeDate)

# url = r'https://www.youtube.com/watch?v=5Irkge4_lEo'

# downloadEpisode(url)