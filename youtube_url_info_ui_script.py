from tkinter import *  # For the UI window and clipboard accessing
import ctypes  # Only used in the two non-import lines below. For scaling displays, ignores scaling (used for the two lines below imports)
from pytube import *  # For doing all' the YouTube stuff
from datetime import date  # To add the date to saved files
import pytube.exceptions  # To handle exceptions where the URL isn't a YouTube URL

result_formatting = 'idk %b-%d-%Y'

PROCESS_PER_MONITOR_DPI_AWARE = 2  # Ignore Windows Scaling, for high-res displays
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

tk = Tk()
tk.resizable(0, 0)  # Disables the ability to resize the window


def get_clipboard_info():
    return tk.clipboard_get()


def add_spaces(length, max_length):  # Used for the Button 2 function (b2_func())
    return ' ' * (max_length - length)


f = Frame(tk, width=1050, height=400)
f.grid(row=0, column=0)
f.grid_propagate(False)

lvar = StringVar(tk)  # Used for displaying Error if the first button encounters one.
l = Label(f, textvariable=lvar, width=15, height=4).grid(row=4, column=1)

l2var = StringVar(tk)  # For displaying the results of the three buttons
l2 = Label(f, textvariable=l2var, width=60, padx=20, justify=LEFT, anchor=W).grid(row=0, column=0)

clipboard_input = ''
res = ''  # The final result


def b_func():
    global clipboard_input
    global l2var

    try:
        clipboard_input = get_clipboard_info()
        l2var.set(clipboard_input)
        b3.config(state='disabled')
        lvar.set('')
    except Exception:
        lvar.set('Error!')


def b2_func():
    global l2var
    global res
    global b3

    # Remove any empty lines (use a while-loop in case of double empty lines (for example))
    urls = clipboard_input
    while '\n\n' in urls:
        urls.replace('\n\n', '\n')
    urls = urls.split('\n')
    # ----------------------------------------------------------------------------------------------------

    stuff = []  # This will have: (length_of_title,  length_of_author,  title,  author) for YouTube URLs, or just the URL for non YouTube ones.
    for index, i in enumerate(urls):
        try:
            yt = YouTube(i)
            save = (yt.title, yt.author)
            stuff.append((len(save[0]), len(save[1]), save[0], save[1]))
        except pytube.exceptions.RegexMatchError:
            stuff.append(i)
    max_length_t = max([i[0] for i in stuff if type(i) == tuple])  # Get the length of the longest title string (if it isn't a normal URL)
    max_length_a = max([i[1] for i in stuff if type(i) == tuple])  # Get the length of the longest author string (if it isn't a normal URL)

    for index, i in enumerate(urls):
        info = stuff[index]
        if type(info) == str:  # If it's a URL, which doesn't get a tuple
            res += info
        else:
            res += info[2] + add_spaces(info[0], max_length_t) + ' - ' + info[3] + add_spaces(info[1], max_length_a) + ' - ' + i
        res += '\n'  # Add a newline
        print(res)

    l2var.set(res)

    b3.config(state='normal')  # Enable button 3
    lvar.set('')  # Since everything worked, ensure that the lower left label doesn't say Error


def b3_func():
    name = date.today().strftime(result_formatting)

    with open(name + '.txt', 'w') as f:
        f.write(res)


b = Button(f, text='Get Clipboard Info', bd=8, width=15, pady=10, command=b_func).grid(row=0, column=1)
b2 = Button(f, text='Generate YT Stuff', bd=8, width=15, pady=10, command=b2_func).grid(row=1, column=1)
b3 = Button(f, text='Save as txt', bd=8, width=15, pady=10, command=b3_func, state=DISABLED)
b3.grid(row=2, column=1)

tk.mainloop()
