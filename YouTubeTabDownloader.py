from UILibrary import *
from pytube import YouTube, Playlist, Channel, exceptions
from datetime import date
from threading import Thread

# Made by interestingbookstore
# Github: https://github.com/interestingbookstore/randomstuff
# -----------------------------------------------------------------------
# Version released on January 4 2022
# ---------------------------------------------------------

# Random comment, threading is awesome!

# -----------------------------------------------------------------------------------------------------------------------------------
#                          *    Options    *

txt_save_location = f'{Path.cwd()}/{date.today().strftime("%b-%d-%Y")}.txt'

yt_item_format = '"{title}" by {author}     {url}'
channel_item_format = 'CHANNEL: {name}     {url}'
playlist_item_format = 'PLAYLIST: {title} by {owner}     {url}'
video_playlist_item_format = 'VIDEO PLAYLIST: {playlist_title} by {owner}, "{video_title}" by {author}     {url}'

file_format = '{youtube_tabs}{channel_tabs}{playlist_tabs}{video_playlist_tabs}\n{general_tabs}'

remove_https = True  # "https://www.example.website" -> "www.example.website"    Note: ONLY "https://" will be removed. That is, "http://www.example.website" -> "http://www.example.website", so I don't think there's any concern with keeping this at True
progress_bar_length = 50

# >-----  End of options  -----<

ui = UI()

ui.style['progress_bar_color'] = ui.colors.red

youtube_reference_url = 'youtube.com/watch?v='
share_youtube_reference_url = 'youtu.be/'
c_reference_url = 'youtube.com/c/'                         # \ In case you're curious, you can check
user_reference_url = 'youtube.com/user/'                   # \ https://support.google.com/youtube/answer/6180214?hl=en
channel_reference_url = 'youtube.com/channel/'             # \ for an explanation on why channels can have three separate URL formats.
playlist_reference_url = 'youtube.com/playlist?list='
video_playlist_reference_url = 'youtube.com/watch?v=', '&list='
regular_url_length = 31
share_url_length = 20

youtube_tabs = []
channel_tabs = []
playlist_tabs = []
video_playlist_tabs = []
tabs = []

for url in ui.get_clipboard().split('\n'):
    if remove_https:
        url = url.lstrip('https://')
    surl = url.lstrip('https://').lstrip('www.').rstrip('/')  # Standardized URL, only used for comparing with reference URLs
    if surl.startswith(youtube_reference_url) and '&t=' in surl:  #         ]
        surl = surl[:surl.index('&t=')]  #                                  | Standardize by removing the "start at" time if present
    elif surl.startswith(share_youtube_reference_url) and '?t=' in surl:  # |
        surl = surl[:surl.index('?t=')]  #                                  ]
    if surl.startswith(user_reference_url):
        surl = c_reference_url + surl[len(user_reference_url):]
    elif surl.startswith(channel_reference_url):
        surl = c_reference_url + surl[len(channel_reference_url):]
    if surl.startswith(share_youtube_reference_url) and len(surl) == share_url_length:  # Convert a share URL to a regular one, as both are identical in terms of where they lead
        surl = youtube_reference_url + surl[share_url_length:]

    if surl.startswith(youtube_reference_url) and len(surl) == regular_url_length:
        youtube_tabs.append(url)
    elif surl.startswith(c_reference_url):
        channel_tabs.append(url)
    elif surl.startswith(playlist_reference_url):
        playlist_tabs.append(url)
    elif surl.startswith(video_playlist_reference_url[0]) and video_playlist_reference_url[1] in surl:
        video_playlist_tabs.append(url)
    else:
        tabs.append(url)

if len(youtube_tabs) == 0 and len(channel_tabs) == 0 and len(playlist_tabs) == 0 and len(video_playlist_tabs) == 0:
    for i in tabs:
        if i[:8] == 'https://':
            break
    else:
        if not ui.ask(f"{ui.get_clipboard()}\n{'-' * 40}\nThere don't seem to be any valid URLS in your clipboard (shown above),\nare these the correct browser tabs?", bool):
            ui.quit()

# -------------------------------------------------------------
def convert_youtube_tabs(url, index):
    global youtube_tabs
    yt = YouTube(url)
    try:
        youtube_tabs[index] = yt_item_format.replace('{title}', yt.title).replace('{author}', yt.author).replace('{url}', url)
    except exceptions.VideoUnavailable:
        pass

def convert_channel_tabs(url, index):
    global channel_tabs
    yt = Channel(url)
    channel_tabs[index] = channel_item_format.replace('{name}', yt.channel_name).replace('{url}', url)

def convert_playlist_tabs(url, index):
    global playlist_tabs
    yt = Playlist(url)
    playlist_tabs[index] = playlist_item_format.replace('{title}', yt.title).replace('{owner}', yt.owner).replace('{url}', url)

def convert_video_playlist_tabs(url, index):
    global video_playlist_tabs
    full_url, url = url, url.split('&list=')
    vid_yt = YouTube(url[0])
    list_yt = Playlist(playlist_reference_url + url[1])
    try:
        video_playlist_tabs[index] = video_playlist_item_format.replace('{video_title}', vid_yt.title).replace('{author}', vid_yt.author).replace('{playlist_title}', list_yt.title).replace('{owner}', list_yt.owner).replace('{url}', full_url)
    except exceptions.VideoUnavailable:
        pass

threads = []

for index, url in enumerate(youtube_tabs):
    threads.append(Thread(target=convert_youtube_tabs, args=[url, index]))
for index, url in enumerate(channel_tabs):
    threads.append(Thread(target=convert_channel_tabs, args=[url, index]))
for index, url in enumerate(playlist_tabs):
    threads.append(Thread(target=convert_playlist_tabs, args=[url, index]))
for index, url in enumerate(video_playlist_tabs):
    threads.append(Thread(target=convert_video_playlist_tabs, args=[url, index]))

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

# -------------------------------------------------------------
save_file_path = ui.get_unique_file(txt_save_location)

save_stuff = file_format \
                 .replace('{youtube_tabs}', ('\n'.join(youtube_tabs) + '\n') if len(youtube_tabs) > 0 else '') \
                 .replace('{channel_tabs}', ('\n'.join(channel_tabs) + '\n') if len(channel_tabs) > 0 else '') \
                 .replace('{playlist_tabs}', ('\n'.join(playlist_tabs) + '\n') if len(playlist_tabs) > 0 else '') \
                 .replace('{video_playlist_tabs}', ('\n'.join(video_playlist_tabs) + '\n') if len(video_playlist_tabs) > 0 else '') \
                 .replace('{general_tabs}', ('\n'.join(tabs) + '\n') if len(tabs) > 0 else '').strip() + '\n'

with open(save_file_path, 'x', encoding='utf-8') as f:
    f.write(save_stuff)

print(f'txt file saved at {save_file_path}')
