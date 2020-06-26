# Imports--------------------------------------------------------------------

from tkinter import *
from tkinter import filedialog, StringVar
import subprocess
import os

# Main Gui & Windows --------------------------------------------------------

root = Tk()
root.title("FFMPEG Audio Encoder Alpha v0.48")
root.iconbitmap(r'C:\Users\jlw_4\PycharmProjects\Draft\reaper.ico')
root.geometry("440x240")
root.configure(background="#929292")

# Menu Bar ------------------------------------------------------------------

my_menu = Menu(root, tearoff=0)
root.config(menu=my_menu)

# About Window ---------------------------------------------------------------

def openaboutwindow():
    about_window = Toplevel()
    about_window.title('About')
    about_window.iconbitmap(r'C:\Users\jlw_4\PycharmProjects\Draft\reaper.ico')
    about_window.geometry("370x150")
    about_window.configure(background="#929292")
    about_window_label = Label(about_window, text="About Text Will Go Here Eventually...")
    about_window_label.grid(row=3, column=1, columnspan=1, padx=10, pady=10)

# Menu Items and Sub-Bars ----------------------------------------------------

shell: StringVar = StringVar()
shell.set("powershell.exe") #Default

file_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = Menu(my_menu, tearoff=0)
shellmenu = Menu(my_menu, tearoff=0)
shellmenu.add_radiobutton(label="PowerShell", value="powershell.exe", variable=shell)
shellmenu.add_radiobutton(label="Command Prompt", value="cmd", variable=shell)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_cascade(label="Shell", menu=shellmenu)

help_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=openaboutwindow) # Possibly Expand This Later

# Video Codec Window ---------------------------------------------------------

vcodec = StringVar()
vcodec.set('Audio Only')

def openvideowindow():
    global vcodec
    global vcodec_bitrate
    video_window = Toplevel()
    video_window.title('WORK IN PROGRESS')
    video_window.iconbitmap(r'C:\Users\jlw_4\PycharmProjects\Draft\reaper.ico')
    video_window.geometry("370x150")
    video_window.configure(background="#929292")

    def apply_button_hover(e):
        apply_button["bg"] = "white"
    def apply_button_hover_leave(e):
        apply_button["bg"] = "SystemButtonFace"

    apply_button = Button(video_window, text="Apply", command=video_window.destroy)
    apply_button.grid(row=3, column=1, columnspan=1, padx=10, pady=10)
    apply_button.bind("<Enter>", apply_button_hover)
    apply_button.bind("<Leave>", apply_button_hover_leave)

    # Video Codec Menu
    vcodec = StringVar(video_window)
    vcodec_choices = {
        "Copy": "-c:v copy",
        "x264": "-c:v libx264",
        "x265": "-c:v libx265",
        "Audio Only": "Audio Only"
    }
    vcodec.set('Audio Only')
    video_menu_label = Label(video_window, text="Choose Codec :")
    video_menu_label.grid(row=0, column=0, columnspan=1, padx=10, pady=5)
    video_menu = OptionMenu(video_window, vcodec, *vcodec_choices.values())
    video_menu.grid(row=2, column=0, columnspan=1, padx=5, pady=1)

# Audio Codec Window ---------------------------------------------------------

acodec = StringVar()
acodec.set('aac')  # set the default option
acodec_bitrate = StringVar()
acodec_bitrate.set('160k') # set the default option
acodec_channel = StringVar()
acodec_channel.set('2')

def openaudiowindow():
    global acodec
    global acodec_bitrate
    global acodec_channel
    audio_window = Toplevel()
    audio_window.title('(WORK IN PROGRESS)')
    audio_window.iconbitmap(r'C:\Users\jlw_4\PycharmProjects\Draft\reaper.ico')
    audio_window.geometry("370x150")
    audio_window.configure(background="#929292")

    def apply_button_hover(e):
        apply_button["bg"] = "white"
    def apply_button_hover_leave(e):
        apply_button["bg"] = "SystemButtonFace"

    apply_button = Button(audio_window, text="Apply", command=audio_window.destroy)
    apply_button.grid(row=3, column=1, columnspan=1, padx=10, pady=10)
    apply_button.bind("<Enter>", apply_button_hover)
    apply_button.bind("<Leave>", apply_button_hover_leave)

    # Audio Codec Menu
    acodec = StringVar(audio_window)
    acodec_choices = {'AAC' : 'aac', 'AC3' : 'ac3'}
    acodec.set('aac')  # set the default option
    audio_menu_label = Label(audio_window, text="Choose Codec :")
    audio_menu_label.grid(row=0, column=0, columnspan=1, padx=10, pady=5)
    audio_menu = OptionMenu(audio_window, acodec, *acodec_choices.values())
    audio_menu.grid(row=2, column=0, columnspan=1, padx=5, pady=1)

    # Audio Bitrate Menu

    acodec_bitrate = StringVar(audio_window)
    acodec_bitrate_choices = [ '192k' ,'224k', '384k' ,'448k', '640k' ]
    acodec_bitrate.set('192k') # set the default option
    abitrate_menu_label = Label(audio_window, text="Choose Bitrate :")
    abitrate_menu_label.grid(row=0, column=1, columnspan=1, padx=10, pady=5)
    abitrate_menu = OptionMenu(audio_window, acodec_bitrate, *acodec_bitrate_choices)
    abitrate_menu.grid(row=2, column=1, columnspan=1, padx=10, pady=10)

    # Audio Channel Menu
    acodec_channel = StringVar(audio_window)
    acodec_channel_choices = [ '2' ,'6' ]
    acodec_channel.set('2') # set the default option
    achannel_menu_label = Label(audio_window, text="Choose Channel :")
    achannel_menu_label.grid(row=0, column=2, columnspan=1, padx=10, pady=5)
    achannel_menu = OptionMenu(audio_window, acodec_channel, *acodec_channel_choices)
    achannel_menu.grid(row=2, column=2, columnspan=1, padx=10, pady=10)

# Code------------------------------------------------------------------------

def file_input():
    global VideoInput
    VideoInput = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                            filetypes=(("MKV, MP4", "*.mp4 *.mkv"), ("All Files", "*.*")))
    input_entry.delete(0, END)  # Remove current text in entry
    input_entry.insert(0, VideoInput)  # Insert the 'path'
    if not VideoInput:
        output_button.config(state=DISABLED)
        show_streams_button.config(state=DISABLED)
        audiosettings_button.config(state=DISABLED)
        videosettings_button.config(state=DISABLED)
    else:
        output_button.config(state=NORMAL)
        show_streams_button.config(state=NORMAL)
        audiosettings_button.config(state=NORMAL)
        # videosettings_button.config(state=NORMAL)

def file_save():
    global VideoOutput
    if vcodec.get() == "Audio Only":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".mp4", initialdir="/",
                                                   title="Select a Save Location",
                                                   filetypes=(("AAC", "*.mp4"), ("AC3", "*.ac3"), ("All Files", "*.*")))
    if not vcodec.get() == "Audio Only":
        VideoOutput = filedialog.asksaveasfilename(defaultextension=".mkv", initialdir="/",
                                                   title="Select a Save Location",
                                                   filetypes=(("MKV", "*.mkv"), ("MP4", "*.mp4"), ("All Files", "*.*")))
    output_entry.delete(0, END)  # Remove current text in entry
    output_entry.insert(0, VideoOutput)  # Insert the 'path'
    if not VideoOutput:
        start_button.config(state=DISABLED)
        start_audio_button.config(state=DISABLED)
    else:
        # start_button.config(state=NORMAL)
        start_audio_button.config(state=NORMAL)

def input_button_hover(e):
    input_button["bg"] = "white"
def input_button_hover_leave(e):
    input_button["bg"] = "SystemButtonFace"

def output_button_hover(e):
    output_button["bg"] = "white"
def output_button_hover_leave(e):
    output_button["bg"] = "SystemButtonFace"

def videosettings_button_hover(e):
    videosettings_button["bg"] = "white"
def videosettings_button_hover_leave(e):
    videosettings_button["bg"] = "SystemButtonFace"

def audiosettings_button_hover(e):
    audiosettings_button["bg"] = "white"
def audiosettings_button_hover_leave(e):
    audiosettings_button["bg"] = "SystemButtonFace"

def show_streams_button_hover(e):
    show_streams_button["bg"] = "white"
def show_streams_button_hover_leave(e):
    show_streams_button["bg"] = "SystemButtonFace"

def start_button_hover(e):
    start_button["bg"] = "white"
def start_button_hover_leave(e):
    start_button["bg"] = "SystemButtonFace"

def start_audio_button_hover(e):
    start_audio_button["bg"] = "white"
def start_audio_button_hover_leave(e):
    start_audio_button["bg"] = "SystemButtonFace"

button_status_label = Label(root, relief=SUNKEN)

# Job Buttons ---------------------------------------------------------

def startaudiojob():
    VideoInputQuoted = '"' + VideoInput + '"'
    VideoOutputQuoted = '"' + VideoOutput + '"'
    if vcodec.get() == "Audio Only":
        subprocess.Popen(shell.get() + " ffmpeg -i " + VideoInputQuoted + " -c:a " + acodec.get() + " -b:a " + acodec_bitrate.get() + " -ac " + acodec_channel.get() + " -sn -vn " + VideoOutputQuoted)

def start(): # Button to Encode
    VideoInputQuoted = '"' + VideoInput + '"'
    VideoOutputQuoted = '"' + VideoOutput + '"'
    # Determine if user wants CMD or PowerShell
    if shell.get() == "cmd":
        subprocess.Popen(shell.get() + " /c " + "ffmpeg -i " + VideoInputQuoted + " " + vcodec.get() + " -c:a " + acodec.get() + " -b:a " + acodec_bitrate.get() + " -ac " + acodec_channel.get() + " " + VideoOutputQuoted)
    elif shell.get() == "powershell.exe":
        subprocess.Popen(shell.get() + " ffmpeg -i " + VideoInputQuoted + " " + vcodec.get() + " -c:a " + acodec.get() + " -b:a " + acodec_bitrate.get() + " -ac " + acodec_channel.get() + " " + VideoOutputQuoted)

def ffprobe_start():  # Start FFProbe based on cmd or powershell selection (Defualt is powershell)
    if shell.get() == "powershell.exe":
        VideoInputQuoted = '"' + VideoInput + '"' # Convert Variable with propper quotes
        subprocess.Popen(shell.get() + " -noexit " + "ffprobe.exe -hide_banner " + VideoInputQuoted)
    elif shell.get() == "cmd":
        VideoInputQuoted = '"' + VideoInput + '"' # Convert Variable with propper quotes
        subprocess.Popen(shell.get() + " /k " + "ffprobe.exe -hide_banner " + VideoInputQuoted)
        print()

# Buttons Main Gui -------------------------------------------------

show_streams_button = Button(root, text="Show Streams", command=ffprobe_start, state=DISABLED)
show_streams_button.grid(row=2, column=0, columnspan=1, padx=10, pady=10)
show_streams_button.bind("<Enter>", show_streams_button_hover)
show_streams_button.bind("<Leave>", show_streams_button_hover_leave)

videosettings_button = Button(root, text="Video Settings", command=openvideowindow, state=DISABLED)
videosettings_button.grid(row=2, column=2, columnspan=1, padx=10, pady=10)
videosettings_button.bind("<Enter>", videosettings_button_hover)
videosettings_button.bind("<Leave>", videosettings_button_hover_leave)

audiosettings_button = Button(root, text="Audio Settings", command=openaudiowindow, state=DISABLED)
audiosettings_button.grid(row=2, column=1, columnspan=1, padx=10, pady=10)
audiosettings_button.bind("<Enter>", audiosettings_button_hover)
audiosettings_button.bind("<Leave>", audiosettings_button_hover_leave)

input_button = Button(root, text="Open File", command=file_input)
input_button.grid(row=0, column=0, columnspan=1, padx=10, pady=10)
input_entry = Entry(root, width=35, borderwidth=5)
input_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=10)
input_button.bind("<Enter>", input_button_hover)
input_button.bind("<Leave>", input_button_hover_leave)

output_button = Button(root, text="Save File", command=file_save, state=DISABLED)
output_button.grid(row=1, column=0, columnspan=1, padx=10, pady=10)
output_entry = Entry(root, width=35, borderwidth=5)
output_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=10)
output_button.bind("<Enter>", output_button_hover)
output_button.bind("<Leave>", output_button_hover_leave)

# Start Video Job
start_button = Button(root, text="Start Video Job", command=start, state=DISABLED)
start_button.grid(row=3, column=1, columnspan=1, padx=10, pady=10)
start_button.bind("<Enter>", start_button_hover)
start_button.bind("<Leave>", start_button_hover_leave)

# Start Audio Job
start_audio_button = Button(root, text="Start Audio Job", command=startaudiojob, state=DISABLED)
start_audio_button.grid(row=3, column=0, columnspan=1, padx=10, pady=10)
start_audio_button.bind("<Enter>", start_audio_button_hover)
start_audio_button.bind("<Leave>", start_audio_button_hover_leave)

# End Loop -----------------------------------------------------------------------
root.mainloop()
