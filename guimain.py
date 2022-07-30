from moviepy.editor import *
import librosa.display
import tkinter as tk
import sys
import threading
import tempfile

logobase64 = "iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAMAAABHPGVmAAAACXBIWXMAAAsSAAALEgHS3X78AAADAFBMVEVHcEz////////////////////////////////l5eX///////////////////+6urr////+/v7////////+/v7AwMD///+8vLzh4eH///////////////////////+7u7v+/v7////q6ur////8/Pz////////////////////+/v7///////////+6urr////8/Pz////8/Pz////////////+/v7////////////29vb////////////+/v7////////////////+/v5HR0f8/Pz8/Pz+/v7+/v7////////V1dXDw8P///+9vb3////+/v7///////////////////////////////+9vb3///////////+urq7////////////////////////KysqOjo6vr6////////9jY2O3t7d6enrOzs6pqanh4eGtra3m5uZzc3P////ExMReXl7////AwMC/v7/////////7+/v8/Py2trbOzs6Hh4elpaU6OjpoaGjW1tbFxcX////////////////AwMDBwcG/v7+9vb2/v7/////AwMDg4OC8vLzAwMD+/v74+Pi8vLyVlZX39/dLS0vq6upQUFDz8/P////Kysq+vr7BwcHFxcXAwMC9vb2/v7++vr7///+7u7u8vLzAwMDf399XV1cICAiZmZktLS2MjIzt7e0nJydZWVk1NTWEhIQ+Pj7GxsbExMS+vr67u7vExMSrq6v9/f2Dg4P7+/ufn5/k5ORkZGSlpaUlJSV7e3vv7++4uLjc3NzZ2dnDw8Pz8/NVVVX5+fmlpaWkpKTi4uJlZWXj4+Py8vJtbW1hYWHu7u5ubm7e3t6Tk5OPj4/////////+/v68vLzExMTHx8fCwsLAwMDq6urT09NdXV2+vr7b29vLy8vm5uajo6N2dnbk5OTu7u7X19cXFxe0tLTQ0NBNTU1DQ0OpqalkZGQAAADx8fF+fn5YWFgzMzOAgICFhYX09PSOjo5qamqUlJSdnZ1sbGxvJtV2AAAA+XRSTlMA3dPV1NHOAgEB4uDL29YD0gPY2doBygIE3ufN3v3I/NXEBuP+wrHrNOWmQBdy/rzNEBN/Mbm4CIM5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"
icodata = b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00 \x00h\x04\x00\x00\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00 \x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xfe\xfe\xff\xcb\xcb\xcb\xff\xd2\xd2\xd2\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xf0\xf0\xf0\xff\xb9\xb9\xb9\xff\xa0\xa0\xa0\xff\xf1\xf1\xf1\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xec\xec\xec\xff\xca\xca\xca\xff\xae\xae\xae\xff\xd8\xd8\xd8\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfd\xfd\xfd\xff\xf7\xf7\xf7\xff\xfb\xfb\xfb\xff\xdb\xdb\xdb\xff\xf2\xf2\xf2\xff\x8c\x8c\x8c\xff\xbd\xbd\xbd\xff\xf9\xf9\xf9\xff\xf8\xf8\xf8\xff\xfc\xfc\xfc\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xf8\xf8\xf8\xff\xc7\xc7\xc7\xff\xe8\xe8\xe8\xff\xb9\xb9\xb9\xff\xd5\xd5\xd5\xff\x80\x80\x80\xff\xb7\xb7\xb7\xff\xe1\xe1\xe1\xff\xca\xca\xca\xff\xf0\xf0\xf0\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xf7\xf7\xf7\xff\x84\x84\x84\xff\x91\x91\x91\xff|||\xffZZZ\xffRRR\xff\x87\x87\x87\xff~~~\xffyyy\xff\xec\xec\xec\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xe8\xe8\xe8\xffHHH\xff\x04\x04\x04\xff\x1c\x1c\x1c\xff\t\t\t\xff\t\t\t\xff%%%\xff\x01\x01\x01\xff///\xff\xd4\xd4\xd4\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xd6\xd6\xd6\xff)))\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff\x14\x14\x14\xff\xb9\xb9\xb9\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xf4\xf4\xf4\xffQQQ\xff\x00\x00\x00\xff###\xff333\xff444\xff:::\xff\x03\x03\x03\xff:::\xff\xe7\xe7\xe7\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xca\xca\xca\xff,,,\xff\xa9\xa9\xa9\xff\xe4\xe4\xe4\xff\xe4\xe4\xe4\xff\xc0\xc0\xc0\xff444\xff\xbd\xbd\xbd\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xb6\xb6\xb6\xff\xc6\xc6\xc6\xff\xff\xff\xff\xff\xff\xff\xff\xff\xd1\xd1\xd1\xff\xbb\xbb\xbb\xff\xfe\xfe\xfe\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfc\xfc\xfc\xff\xf0\xf0\xf0\xff\xfd\xfd\xfd\xff\xfe\xfe\xfe\xff\xf4\xf4\xf4\xff\xfc\xfc\xfc\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

musicfile = ""  # Music file to be played
videofiles = ""  # Video files to be combined
resultfile = ""  # Resulting video file
# Minimum time between two onset beats (also technically minimum video clip lengths I think)
mintime = 1
minstrength = 0  # Minimum strength of onset beat to be considered. Recommend 0? Unless looking for specific strong beats
startdelay = 3  # Delay before the first onset beat / clip
resultfps = 30  # Resulting video framerate
# If True, the audio will be combined with the video. If False, the video audio is replaced with music
combineAudio = False
fadeDuration = 2  # Duration of the audio fade out

initialtrim = 0  # Initial trimming of each video clip
# Time in seconds where the onset should be in each video clip (trimmed)
clippoi = 0


class Stdoutrewrite(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.see(tk.END)
        self.widget.insert("end", string)


window = tk.Tk()
window.title("Video Clips to Music Synchronizer by Dragonlinae")
_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(icodata)
window.iconbitmap(default=ICON_PATH)

window.geometry("1080x720")
canvas = tk.Canvas(window, width=500, height=500)
canvas.pack()

# Place to upload files
uploadMusic = tk.Button(window, text="Upload Music",
                        command=lambda: uploadMusicFiles())
uploadMusic.place(x=10, y=10)
selectedMusic = tk.Label(window, text="No music selected")
selectedMusic.place(x=150, y=10)

uploadVideos = tk.Button(window, text="Upload Videos",
                         command=lambda: uploadVideoFiles())
uploadVideos.place(x=10, y=50)
selectedVideos = tk.Label(window, text="No videos selected")
selectedVideos.place(x=150, y=50)

outputName = tk.Button(window, text="Output Name",
                       command=lambda: outputName())
outputName.place(x=10, y=90)
selectedOutput = tk.Label(window, text="No output selected")
selectedOutput.place(x=150, y=90)

mintimeinput = tk.Entry(window)
mintimeinput.place(x=10, y=130)
mintimeinput.insert(0, mintime)
mintimeinputlabel = tk.Label(
    window, text="Minimum time between two onset beats (also technically minimum video clip lengths I think)")
mintimeinputlabel.place(x=150, y=130)

minstrengthinput = tk.Entry(window)
minstrengthinput.place(x=10, y=170)
minstrengthinput.insert(0, minstrength)
minstrengthinputlabel = tk.Label(
    window, text="Minimum strength of onset beat to be considered. Recommend 0? Unless looking for specific strong beats")
minstrengthinputlabel.place(x=150, y=170)

startdelayinput = tk.Entry(window)
startdelayinput.place(x=10, y=210)
startdelayinput.insert(0, startdelay)
startdelayinputlabel = tk.Label(
    window, text="Delay before the first onset beat / clip")
startdelayinputlabel.place(x=150, y=210)

resultfpsinput = tk.Entry(window)
resultfpsinput.place(x=10, y=250)
resultfpsinput.insert(0, resultfps)
resultfpsinputlabel = tk.Label(window, text="Resulting video framerate")
resultfpsinputlabel.place(x=150, y=250)

combineAudio = tk.BooleanVar()
combineAudioinput = tk.Checkbutton(
    window, text="Combine audio", variable=combineAudio, onvalue=True, offvalue=False)
combineAudioinput.place(x=10, y=300)
combineAudioinputlabel = tk.Label(
    window, text="Combine audio with video. If False, the video audio is replaced with music")
combineAudioinputlabel.place(x=150, y=300)

fadeDurationinput = tk.Entry(window)
fadeDurationinput.place(x=10, y=350)
fadeDurationinput.insert(0, fadeDuration)
fadeDurationinputlabel = tk.Label(
    window, text="Duration of the audio fade out")
fadeDurationinputlabel.place(x=150, y=350)

initialtriminput = tk.Entry(window)
initialtriminput.place(x=10, y=400)
initialtriminput.insert(0, initialtrim)
initialtriminputlabel = tk.Label(
    window, text="Initial trimming of each video clip")
initialtriminputlabel.place(x=150, y=400)

clippoiinput = tk.Entry(window)
clippoiinput.place(x=10, y=450)
clippoiinput.insert(0, clippoi)
clippoiinputlabel = tk.Label(
    window, text="Time in seconds where the onset should be in each video clip (trimmed)")
clippoiinputlabel.place(x=150, y=450)

startButton = tk.Button(window, text="Start", command=lambda: startscript())
startButton.place(x=10, y=500)

showconsole = tk.Button(window, text="Show Console",
                        command=lambda: showconsole())
showconsole.place(x=150, y=500)

showconsolelabel = tk.Label(
    window, text="Showing console will probably will hurt perfrmance. Use with caution. Cannot disable after enabling. Literally just look at the cmd prompt or smthn")
showconsolelabel.place(x=250, y=500)

console = tk.Text(window, height=10, width=50)
console.place(x=10, y=550)

logo = tk.PhotoImage(data=logobase64)
logoLabel = tk.Label(window, image=logo)
logoLabel.place(x=500, y=550)


def showconsole():
    global console
    sys.stdout = Stdoutrewrite(console)
    sys.stderr = Stdoutrewrite(console)


def uploadMusicFiles():
    global musicfile
    musicfile = tk.filedialog.askopenfilename(title="Select music file", filetypes=[
        ("MP3", "*.mp3"), ("WAV", "*.wav")])
    selectedMusic.config(text=musicfile.split("/")[-1])


def uploadVideoFiles():
    global videofiles
    videofiles = tk.filedialog.askopenfilenames(
        title="Select video files", filetypes=[("MP4", "*.mp4")])
    selectedVideos.config(
        text=' '.join(list(map(lambda x: x.split("/")[-1], videofiles))))


def outputName():
    global resultfile
    resultfile = tk.filedialog.asksaveasfilename(
        title="Select output file", filetypes=[("MP4", "*.mp4")])
    selectedOutput.config(text=resultfile.split("/")[-1])


def startscript():
    # Check if all files are selected
    if musicfile == "" or videofiles == "" or resultfile == "":
        tk.messagebox.showinfo(
            "Error", "Please select all files before starting")
        return

    thread = threading.Thread(target=start)
    thread.start()


def start():
    global mintime, minstrength, startdelay, resultfps, combineAudio, fadeDuration, initialtrim, clippoi, videofiles, musicfile, resultfile, startButton, console

    # Disable start button
    startButton.config(state="disabled")

    console.insert(tk.END, "Starting...\n")

    mintime = float(mintimeinput.get())
    minstrength = float(minstrengthinput.get())
    startdelay = float(startdelayinput.get())
    resultfps = int(resultfpsinput.get())
    fadeDuration = float(fadeDurationinput.get())
    initialtrim = float(initialtriminput.get())
    clippoi = float(clippoiinput.get())

    if (not musicfile.split(".")[-1] == "wav"):
        audioclip = AudioFileClip(musicfile)
        # audioclip = audioclip.subclip(0, 100)
        audioclip.write_audiofile(musicfile.split(".")[0] + ".wav")

    console.insert(tk.END, "Finding onsets...\n")

    y, sr = librosa.load(musicfile.split(".")[0] + ".wav")

    onset_envelope = librosa.onset.onset_strength(y, sr)
    onsets = librosa.onset.onset_detect(onset_envelope=onset_envelope)

    onset_times = librosa.frames_to_time(onsets)

    onset_arr = onsets.tolist()
    onset_times_arr = onset_times.tolist()

    for frame in onset_arr:
        print(str(frame) + ': ' + str(onset_envelope[frame]))

    # Pop onsets that are too close to the previous onset
    i = 0
    while i < len(onset_times_arr):
        if (onset_times_arr[i] < startdelay):
            onset_times_arr.pop(i)
            onset_arr.pop(i)
            i -= 1
        elif (onset_envelope[onset_arr[i]] < minstrength):
            onset_times_arr.pop(i)
            onset_arr.pop(i)
            i -= 1
        elif i > 0 and onset_times_arr[i] - onset_times_arr[i - 1] < mintime:
            if(onset_envelope[onset_arr[i]] > onset_envelope[onset_arr[i - 1]]):
                onset_arr.pop(i-1)
                onset_times_arr.pop(i-1)
            else:
                onset_arr.pop(i)
                onset_times_arr.pop(i)
            i -= 1
        i += 1

    for i in range(len(onset_arr)):
        print(str(i) + ') ' + str(onset_arr[i]) + ': ' + str(onset_times_arr[i]
                                                             ) + ': ' + str(onset_envelope[onset_arr[i]]))

    combinedVideo = None
    currOnset = 0

    console.insert(tk.END, "Combining videos...\n")

    for i in range(len(videofiles)):
        video = VideoFileClip(videofiles[i]).subclip(initialtrim)
        # Check to see if it is the first clip. If so, trim clip to have the 16th second (or what the clippoi is) be at the osnet and
        # cut between the current onset and the next onset
        if (combinedVideo is None):
            enddelay = (onset_times_arr[currOnset+1] -
                        onset_times_arr[currOnset])/2
            combinedVideo = video.subclip(
                max(0, clippoi-onset_times_arr[currOnset]), clippoi+enddelay+max(0, enddelay-clippoi) + onset_times_arr[currOnset] - (clippoi - max(0, clippoi-onset_times_arr[currOnset])))
        # Check to see if it is the last clip or if the onset is the last onset, play to end if it is
        elif (i == len(videofiles) - 1 or currOnset == len(onset_times_arr) - 1):
            combinedVideo = concatenate_videoclips([combinedVideo, video.subclip(
                max(0, clippoi+combinedVideo.duration-onset_times_arr[currOnset]), video.duration)])
        else:
            enddelay = (onset_times_arr[currOnset+1] -
                        onset_times_arr[currOnset])/2
            combinedVideo = concatenate_videoclips([combinedVideo, video.subclip(max(0, clippoi+combinedVideo.duration -
                                                                                     onset_times_arr[currOnset]), clippoi+enddelay+max(0, enddelay-clippoi))])

        print("start: " + str(max(0, clippoi -
                                  onset_times_arr[currOnset])) + " time: " + str(combinedVideo.duration))
        currOnset += 1

    # for entry in videos:
    #     if (currOnset < len(onset_times_arr)-1):
    #         video = VideoFileClip('res/video/' + entry)
    #         if video.duration < 24:
    #             if combinedVideo is None:
    #                 combinedVideo = video.subclip(
    #                     16-onset_times_arr[currOnset], 16+(onset_times_arr[currOnset+1]-onset_times_arr[currOnset])/2)
    #             else:
    #                 combinedVideo = concatenate_videoclips(
    #                     [combinedVideo, video.subclip(16-(onset_times_arr[currOnset]-onset_times_arr[currOnset-1])/2, 16+(onset_times_arr[currOnset+1]-onset_times_arr[currOnset])/2)])
    #             currOnset += 1
    #     elif (currOnset == len(onset_times_arr)-1):
    #         video = VideoFileClip('res/video/' + entry)
    #         if video.duration < 24:
    #             if combinedVideo is None:
    #                 combinedVideo = video.subclip(
    #                     16-onset_times_arr[currOnset])
    #             else:
    #                 combinedVideo = concatenate_videoclips(
    #                     [combinedVideo, video.subclip(16-(onset_times_arr[currOnset]-onset_times_arr[currOnset-1])/2)])
    #             currOnset += 1

    if (combineAudio.get()):
        new_audioclip = CompositeAudioClip([combinedVideo.audio, audioclip])
    else:
        new_audioclip = audioclip

    combinedVideo.audio = new_audioclip.subclip(
        0, combinedVideo.duration).fx(AudioClip.audio_fadeout, duration=fadeDuration)

    console.insert(tk.END, "Rendering video... (May take a long time)\n")

    combinedVideo.write_videofile(
        resultfile.split('.')[0]+'.mp4', fps=resultfps)

    console.insert(tk.END, "Done!\n")

    # Enable start button
    startButton.config(state="normal")


window.mainloop()
