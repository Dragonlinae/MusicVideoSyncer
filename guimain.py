from moviepy.editor import *
import librosa.display
import tkinter as tk
import sys
import threading

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
window.title = "Video Clip to Music Synchronization"
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
    window, text="Showing console will probably will hurt perfrmance. Use with caution. Cannot disable after enabling")
showconsolelabel.place(x=250, y=500)

console = tk.Text(window, height=10, width=50)
console.place(x=10, y=550)


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
