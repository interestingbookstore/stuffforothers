from pytube import YouTube
from pathlib import Path
from string import ascii_letters, digits
import re

# Made by interestingbookstore
# Github: https://github.com/interestingbookstore
# ---------------------------------------------------------
# Version 1.2.0 Alpha October 26 2021 - Bundled Version
# -----------------------------------------


TMP_File_Save_Location = '/tmp'
Save_Location = f'{str(Path.home())}/Downloads'  # By default the tmp files and output files are saved in the current working directory.
#     (This should be a folder)                    Simply edit this line if you'd like to save them somewhere else.

default_quality = '1080'  # Say you always want the top resolution, but nothing above 8K, for example (8K is a bit overkill, eh?). Simply set
#                         this variable to '4K', and you'll never have to specify again! If you want this feature disabled, keep this variable
#                         at None.

default_filename = '{title}'  # Just like the previous option, set the filename to a default filename. How would that work? Well, you can
#                          use things like {title}, which adjust based on the video! See more below.

ask_save_location = False  # Say you're weird and want to be prompted for the save location the whenever downloading one or multiple
#                            video; just set this to True. Otherwise, False.

formatting = True  # By default, this script uses ANSI escape sequences to add color and text effects to certain elements.
#                    Normally, these wouldn't actually be visible, and they'd simply modify how the text looks. However, applications
#                    (like Windows's Command Prompt) still render them (and they don't actually change anything there), which looks a bit
#                    odd. So, if you're in a similar situation, or you simply dislike ANSI escape sequences, set this variable to "False"
#                    (case sensitive) to disable them.

def _filename_process(filename):
    # Say you want to automate everything, including the filenames. After you've set the default filename (although this will work
    # regardless), add whatever processing you want to the filename here.
    # Example:
    # filename = filename.replace(' ', '_')
    good_characters = ascii_letters + digits + ' _'
    filename2 = ''
    for i in filename:
        if i in good_characters:
            filename2 += i
    filename2 = filename2.replace(' ', '_')
    while '__' in filename2:
        filename2 = filename2.replace('__', '_')
    return filename2

# When choosing a filename, you can specify a couple "dynamic" strings.
# These include:

# {title} _or_ {name} -> The video's title
# {author} -> The channel that posted the video
# And, because why not;
# {views} -> The raw number of views the video has
# {length} -> The video's length (in seconds)

# If these are in the filename, they're replaced with the video's value for them.
# -----------------------------------------
# UILibrary  -----------  v  ----------------  v  ------------------------------------------



import pickle
from sys import exit as s_exit, argv
from platform import system
import subprocess
from os import system as run_command
from time import time
from pathlib import Path

try:
    import pyperclip

    tk = None
except ModuleNotFoundError:
    pyperclip = None
    from tkinter import Tk

    tk = Tk()

# Made by interestingbookstore
# Github: https://github.com/interestingbookstore/randomstuff
# ---------------------------------------------------------

txt_save_folder = r''


# ---------------------------------------------------------

# With this library, you can edit a dictionary, which will save its information, even if you close and rerun the python script.
# It accomplishes this through a pickle file, which has to be saved somewhere.
# If the variable above is left as an empty string, it'll be saved in the current directory. Otherwise,
# it'll be saved in the folder above. (no slash at the end)

def large_number_formatter(number, type='notation', decimal_places=2):
    num = str(number)
    length = len(num)
    thousands = (len(num) - 1) // 3
    if type == ',':
        for i in range(thousands):
            i += 1
            num = num[:length - i * 3] + ',' + num[length - i * 3:]
        return num
    else:
        notations = 'K', 'M', 'B', 'T', 'Q'
        return str(round(number / 10 ** (thousands * 3), decimal_places)) + notations[thousands - 1]


# def duration_formatter(duration, hi)


def check_type(val, validation):
    if validation == int:
        try:
            int(val)
            return True
        except ValueError:
            pass
    elif validation == float:
        try:
            float(val)
            return True
        except ValueError:
            pass
    return False


if txt_save_folder != '':
    txt_save_folder += '/'


class _SavedInfo:
    def __init__(self, file_name):
        self.path = txt_save_folder + file_name + '.pkl'
        self.stuff = {}
        try:
            with open(self.path, 'rb') as f:
                self.stuff = pickle.load(f)
        except FileNotFoundError:
            with open(self.path, 'a'):
                pass

    def clear(self):
        self.stuff.clear()
        self._update()

    def __getitem__(self, item):
        return self.stuff[item]

    def _update(self):
        with open(self.path, 'wb') as f:
            f.truncate(0)
            pickle.dump(self.stuff, f, pickle.HIGHEST_PROTOCOL)

    def __setitem__(self, key, value):
        self.stuff[key] = value
        self._update()


class UI:
    class ProgressBar:
        def __init__(self, ui_class):
            self._progress = 0
            self._total = 0
            self._percent = None
            self.style = ui_class.style
            self._start_time = 0

        def update(self, progress, total, description='', length=50):
            if self._percent is None:
                self._start_time = time()
            if total == 0:  # If you only have to do 0 stuff, it's impossible to not have already done it
                print('\r' + description + self.style['progress_bar_done'] + ' Done!')
            else:
                if progress == 0:
                    time_remaining = ''
                else:
                    time_remaining = f'{round((time() - self._start_time) * (total - progress) / progress)} seconds left'
                fraction = progress / total
                percent = int(fraction * 100)
                amount = int(fraction * length)
                if percent != self._percent:
                    print('\r' + f"{description} {self.style['progress_bar_color']}{self.style['progress_bar'] * amount}{self.style['reset']}{' ' * (length - amount)} {percent}%  {time_remaining}", end='')
                    self._percent = percent
                    if percent >= 100:
                        print('\r' + description + self.style['progress_bar_done'] + ' Done!' + self.style['reset'])
                        self._percent = None

    class _OptionsList:
        """Used for making lists, of options!"""

        def __init__(self, ui_class, options=()):
            self.options = []
            self.ui_class = ui_class
            self.style = self.ui_class.style
            for i in options:
                self.add(i)

        def error_print(self, text):
            print(self.style['error'] + text + '\n')

        def add(self, option, option_func=None):
            if option_func is None:
                self.options.append((str(option), option))
            else:
                self.options.append((str(option), option_func))

        def show(self):
            for index, i in enumerate(self.options):
                index += 1
                print(f"{self.style['options_list_number']}{index}{self.style['options_list_separator']}{self.style['normal_output_color']}{str(i[0])}")

            while True:
                try:
                    inp = input(f"{self.style['bold_formatting']}{self.style['ask_color']}Choice: {self.style['reset']}{self.style['user_input']}")
                    if inp == '/help':
                        print(self.style['normal_output_color'] + 'Listed above are different options; simply type the number to the left of the option you want to select.\n')
                        continue
                    elif inp == '':
                        return self.options[0][1]
                    inp = int(inp)
                    if inp < 0:
                        inp += 1
                    elif inp == 0:
                        raise IndexError
                    self.options[inp - 1]  # Python will try to run this line. If it raises an error, we'll know that something is wrong.

                    return self.options[inp - 1][1]
                except (IndexError, ValueError):
                    option_names = tuple(i[0] for i in self.options)
                    inp = str(inp)
                    if inp in option_names:
                        return self.options[option_names.index(inp)][1]
                    self.error_print('Your choice must correspond to one of the options above!')

    class Colors:
        def __init__(self):
            self.reset = '\033[0m'

            self.white = '\33[97m'
            self.gray = '\33[37m'
            self.black = ''

            self.red = '\33[31m'
            self.orange = '\33[36m'
            self.yellow = '\33[33m'
            self.green = '\33[32m'
            self.blue = '\33[34m'
            self.purple = '\33[35m'

            self.bold = '\33[1m'
            self.underline = '\33[4m'
            self.italic = '\33[3m'
            self.strikethrough = '\33[9m'

            self.full_rectangle = '█'
            self.rectangles = {'Upper 1/2': '▀', '1/8': '▁', '1/4': '▂', '3/8': '▃', '1/2': '▄', '5/8': '▅', '3/4': '▆',
                               '7/8': '▇', '1': '█', 'l7/8': '▉', 'l3/4': '▊', 'l5/8': '▋', 'l1/2': '▌', 'l3/8': '▍',
                               'l1/4': '▎', 'l1/8': '▏', 'r1/2': '▐', 'light': '░', 'medium': '▒', 'dark': '▓',
                               'u1/8': '▔', 'r1/8': '▕'}

    def __init__(self, txt_name=None, formatting=True):
        if txt_name is not None:
            self.save_info = _SavedInfo(txt_name)
        self.os = system().lower()
        if self.os == 'darwin':
            self.os = 'macos'
        self.colors = self.Colors()
        if not formatting:
            self.colors.reset = ''

            self.colors.white = ''
            self.colors.gray = ''
            self.colors.black = ''

            self.colors.red = ''
            self.colors.orange = ''
            self.colors.yellow = ''
            self.colors.green = ''
            self.colors.blue = ''
            self.colors.purple = ''

            self.colors.bold = ''
            self.colors.underline = ''
            self.colors.italic = ''
            self.colors.strikethrough = ''
        self.style = {'ask_color': self.colors.yellow, 'options_list_number': self.colors.yellow, 'options_list_separator': ' - ', 'progress_bar': self.colors.full_rectangle,
                      'progress_bar_color': self.colors.yellow, 'progress_bar_done': self.colors.green, 'normal_output_color': self.colors.reset, 'user_input': self.colors.reset,
                      'error': self.colors.red, 'bold_formatting': self.colors.bold, 'reset': self.colors.reset}
        self.progress_bar = self.ProgressBar(self)

    def quit(self):
        s_exit()

    def get_clipboard(self):
        if pyperclip is not None:
            return pyperclip.paste()
        return tk.clipboard_get()

    def set_clipboard(self, text):
        if pyperclip is not None:
            pyperclip.copy(text)
        else:
            raise ModuleNotFoundError('UILibrary doesn\'t currently support pasting to clipboard without the module "pyperclip"')

    def set_default(self, name, default_value):
        if name not in self.save_info.stuff:
            self.save_info[name] = default_value

    def remove_invalid_filename_characters(self, path, window_only=True):
        if self.os == 'windows' or not window_only:
            bad_characters = r'<>:"|?*'
            for i in bad_characters:
                if ':\\' in path:
                    path = path.split(':\\', 1)[0] + ':\\' + path.split(':\\', 1)[1].replace(i, '')  # A ":" is only allowed in the "C:..." section.
                else:
                    path = path.replace(i, '')
        return path

    def format_slashes_for_windows(self, path):
        if self.os == 'windows':
            path = path.replace('/', '\\')
        return path


    def get_unique_file(self, path, invalid_characters='remove', format_slashes=True):
        if not (invalid_characters == 'remove' or invalid_characters == 'keep'):
            raise Exception(f'The invalid characters parameter should be either "remove" or "keep", but "{invalid_characters}" was given.')

        if Path(path).is_file():
            filename = '.'.join(path.split('.')[:-1])
            extension = '.' + path.split('.')[-1]

            filename_addition = ' (*)'

            num = 1
            while Path(filename + filename_addition.replace('*', str(num)) + extension).is_file():
                num += 1

            path = filename + filename_addition.replace('*', str(num)) + extension
        if invalid_characters == 'remove':
            path = self.remove_invalid_filename_characters(path)
        if format_slashes:
            path = self.format_slashes_for_windows(path)

        return path

    def OptionsList(self, options=()):
        return self._OptionsList(self, options)

    def error_print(self, text):
        print(self.style['error'] + text + '\n')

    def get_console_arguments(self):
        return argv[1:]

    def run_console_command(self, command):
        run_command(command)

    def open_path(self, path):
        path = path.replace('\\', '/')
        if self.os == 'windows':
            subprocess.Popen(f'explorer /select,"{path}"')
        elif self.os == 'macos':
            subprocess.Popen(['open', path])
        elif self.os == 'linux':
            run_command(f'gio open "{path}"')  # Origionally    subprocess.Popen(['xdg-open', path])    was used, but gio is faster, and it doesn't print a bunch of errors...

    def ask(self, question, validation=str, extra=None, end=': '):
        while True:
            add = ''
            if validation == 'y/n' or validation == 'yn':
                add += ' (y/n)'
            inp = input(self.style['bold_formatting'] + self.style['ask_color'] + question + add + end + self.colors.reset + self.style['user_input'])
            if inp == '/help':
                if validation == str or validation == 'str':
                    mes = 'Your answer can be pretty much anything.'
                elif validation == int or validation == 'int':
                    mes = 'Your answer should be an integer.'
                elif validation == float or validation == 'float':
                    mes = 'Your answer should be a float value. Any normal number (decimals included) pretty much.'
                elif validation == bool or validation == 'y/n' or validation == 'yn':
                    mes = """Your answer should just be a lowercase "y" for yes, or a lowercase "n" for no. y or n, that's it."""
                elif validation == tuple or validation == 'tuple':
                    if extra == int or extra == 'int':
                        idk = 'integers'
                    elif extra == float or extra == 'float':
                        idk = 'floats'
                    else:
                        idk = 'strings'
                    mes = f"""This one's a bit more tricky. You probably need to provide multiple answers (not necessarily, but more than likely), in this case {idk}.
Separate them with spaces, include a backslash directly before one ("...\\ ...") to ignore it."""
                else:
                    mes = "The validation is something else, you're on your own for this one!"
                print(self.style['normal_output_color'] + mes + '\n')
                continue

            if validation == str or validation == 'str':
                return inp
            elif validation == int or validation == 'int':
                if check_type(inp, int):
                    return int(inp)
                else:
                    self.error_print(f'Your answer must be an integer')
            elif validation == float or validation == 'float':
                if check_type(inp, float):
                    return float(inp)
                else:
                    self.error_print(f'Your answer must be a float')
            elif validation == bool or validation == 'y/n' or validation == 'yn':
                if inp == 'y':
                    return True
                elif inp == 'n':
                    return False
                else:
                    self.error_print('Your response should be either "y" or "n".')
            elif validation == tuple or validation == 'tuple':
                inp = [i.strip(' ') for i in inp.split(',')]

                for i in inp:
                    if extra == 'int':
                        if not check_type(i, int):
                            self.error_print('Your response consist of one or multiple integers, separated by a comma.')
                    elif extra == 'float':
                        if not check_type(i, float):
                            self.error_print('Your response consist of one or multiple float values, separated by a comma.')
                return inp

            else:
                while True:
                    try:
                        return validation[0](inp)
                    except validation[1]:
                        self.error_print(validation[2])










# ------------------------------------------
ui = UI(formatting=formatting)
c = ui.colors
ui.style['ask_color'] = c.red
ui.style['options_list_number'] = c.red
ui.style['progress_bar_color'] = c.red

stream_size = 0
currently_downloading = 'video'


def download_progress(stream, chunk, bytes_remaining):
    ui.progress_bar.update(stream_size - bytes_remaining, stream_size, f'Downloading {currently_downloading}')


resolutions = {'240': '240', '240p': '240', 'qvga': '240',
               '360': '360', '360p': '360',
               '480': '480', '480p': '480', 'vga': '480', 'ntsc': '480', 'wvga': '480',
               '720': '720', '720p': '720', 'hd': '720', 'hd720': '720', 'hd 720': '720', '720hd': '720', '720 hd': '720',
               '1080': '1080', '1080p': '1080', 'fullhd': '1080', 'full hd': '1080', 'full-hd': '1080', 'fhd': '1080', 'hd 1080': '1080', 'hd1080': '1080', '1080 hd': '1080', '1080hd': '1080',
               '1440': '1440', '1440p': '1440', 'wqhd': '1440', '3k': '1440',
               '2160': '2160', '2160p': '2160', '4k': '2160', 'uhd': '2160', 'uhd4k': '2160', 'uhd 4k': '2160', '4kuhd': '2160', '4k uhd': '2160',
               '4320': '4320', '4320p': '4320', '8k': '4320', 'uhd8k': '4320', 'uhd 8k': '4320', '8kuhd': '4320', '8k uhd': '4320', 'max': '4320'}

video_id_characters = ascii_letters + digits + '-_'

args = ui.get_console_arguments()

if default_quality is not None:
    if default_quality.lower() not in resolutions:
        raise Exception(f'Default quality should be either "None" or a valid resolution, but "{default_quality}" given.')
if Save_Location[-1] == '/':
    Save_Location = Save_Location[:-1]
urls = []
qualities = []
filenames = []

for i in args:
    if (match := re.search('[a-zA-Z0-9_-]{11}', i)):
        urls.append('v=' + i[match.start():match.end()])
    elif i.lower() in resolutions:
        qualities.append(resolutions[i.lower()])
    else:
        filenames.append(i)

if len(urls) == 0:
    while True:
        urls = []
        urls2 = ui.ask('Video URL(s)', tuple)
        continue_going = False
        for i in urls2:
            if ' ' not in i and (match := re.search('[a-zA-Z0-9_-]{11}', i)):
                urls.append('v=' + i[match.start():match.end()])
            else:
                ui.error_print(f'The URL {i} is not a valid URL.')
                continue_going = True
        if not continue_going:
            break

if len(qualities) == 0:
    if default_quality is not None:
        qualities.append(resolutions[default_quality.lower()])
    else:
        qualities2 = ui.ask('Video quality(s)', tuple)
        for i in qualities2:
            if i.lower() in resolutions:
                qualities.append(resolutions[i.lower()])

if len(filenames) == 0:
    if default_filename is not None:
        filenames.append(default_filename)
    else:
        filenames = ui.ask('Video filename(s)', tuple)

if ask_save_location:
    Save_Location = ui.ask('Save Location')

final_videos = [[i] for i in urls]
for index, video in enumerate(final_videos):
    final_videos[index][0] = YouTube(video[0], download_progress)

if len(qualities) == 1:
    for index, _ in enumerate(final_videos):
        final_videos[index].append(qualities[0])
elif len(qualities) == len(urls):
    for index, i in enumerate(qualities):
        final_videos[index].append(i)
else:
    raise Exception(f'One or {len(urls)} qualities were expected, but {len(qualities)} were given;\n{qualities}')

if len(filenames) == 1:
    for index, _ in enumerate(final_videos):
        video = final_videos[index][0]
        final_videos[index].append(filenames[0].replace('{title}', video.title).replace('{name}', video.title).replace('{author}', video.author).replace('{views}', str(video.views)).replace('{length}', str(video.length)))
elif len(filenames) == len(urls):
    for index, i in enumerate(filenames):
        final_videos[index].append(i)
else:
    raise Exception(f'{len(urls)} filenames were expected, but {len(filenames)} were given;\n{filenames}')

for video in final_videos:
    print(f'{c.reset}{c.bold}{video[0].title}{c.reset}{c.gray}    by    '
          f'{c.reset}{c.bold}{video[0].author}{c.reset}{c.gray}    with    '
          f'{c.reset}{c.bold}{large_number_formatter(video[0].views)}{c.reset}{c.gray}    views at    '
          f'{c.reset}{c.bold}{video[0].length}{c.reset}{c.gray}    seconds long.{c.reset}')

for video in final_videos:
    yt_object = video[0]
    quality = video[1]
    filename = video[2]

    filename = _filename_process(filename)

    streams_object = yt_object.streams.order_by('bitrate').desc()

    audio = streams_object.get_audio_only()
    if quality == 'audio':
        audio.download(output_path=Save_Location, filename=filename)
    else:
        max_res = streams_object.first().resolution[:-1]
        if quality == 'max':
            quality = max_res
        if int(quality) > int(max_res):
            quality = max_res
        video_stream = streams_object.filter(res=quality + 'p').first()
        v_extension = video_stream.mime_type.split('/')[-1]
        a_extension = audio.mime_type.split('/')[-1]
        stream_size = video_stream.filesize
        currently_downloading = 'video'
        video_stream.download(output_path=TMP_File_Save_Location, filename=f'tmp_download_video.{v_extension}')
        currently_downloading = 'audio'
        audio.download(output_path=TMP_File_Save_Location, filename=f'tmp_download_audio.{a_extension}')

        filename = ui.remove_invalid_filename_characters(filename).replace('/', '').replace('\\', '')
        name = ui.get_unique_file(f'{Save_Location}/{filename}.mp4')
        short_name = filename + '.mp4'

        ui.run_console_command(f'ffmpeg -loglevel warning -i "{TMP_File_Save_Location}/tmp_download_video.{v_extension}" -i "{TMP_File_Save_Location}/tmp_download_audio.{a_extension}" -c copy "{name}"')
        print(f"Video saved as {short_name} at {name}")
