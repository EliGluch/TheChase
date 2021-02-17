import sys
import pytube
import youtube
from pytube import YouTube
from pytube import Playlist


downloaded_episode_file = 'DownloadedChaseEpisodes.txt'
fifth_season_url = "https://www.youtube.com/playlist?list=PLLttfoK87AdUjGSmMYhtC-n-GcBBpcz8T"

playlist_url = fifth_season_url # Needs to be updated for every new season

def main(*args):
    get_newest_episode()

def get_newest_episode():
    latest_episode_url = get_latest_episode_url()

    if is_allready_downloaded(latest_episode_url):
        print("episode is allready downloaded. url is {}".format(latest_episode_url))
        return
    
    youtube.run(latest_episode_url)

def get_latest_episode_url():
    playlist = Playlist(playlist_url)
    
    if len(playlist.video_urls) == 0:
        print('Playlist has no videos')
        return None
    
    return playlist.video_urls[0]

def is_allready_downloaded(url):
    allready_downloaded = False

    with open(downloaded_episode_file, 'r+') as f:
        all_links = f.read()
        all_links = all_links.splitlines()

        if url in all_links:
            allready_downloaded = True

        else:
            all_links.append(url)

        f.seek(0)
        f.write('\n'.join(all_links))
        f.truncate()

    return allready_downloaded

if __name__ == "__main__":
   main(sys.argv[1:])
