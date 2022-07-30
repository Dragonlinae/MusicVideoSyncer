from moviepy.editor import *
import librosa.display

musicfile = "res/music/music4.mp3"  # Music file to be played
videofiles = "res/video/"  # Folder containing video files
resultfile = "combined10.mp4"  # Resulting video file
# Minimum time between two onset beats (also technically minimum video clip lengths I think)
mintime = 1
minstrength = 0  # Minimum strength of onset beat to be considered. Recommend 0? Unless looking for specific strong beats
startdelay = 3  # Delay before the first onset beat / clip
resultfps = 30  # Resulting video framerate
# If True, the audio will be combined with the video. If False, the video audio is replaced with music
combineAudio = False
fadeDuration = 2  # Duration of the audio fade out

initialtrim = 10  # Initial trimming of each video clip
# Time in seconds where the onset should be in each video clip (trimmed)
clippoi = 0

audioclip = AudioFileClip(musicfile)
# audioclip = audioclip.subclip(0, 100)
audioclip.write_audiofile("res/music/music.wav")

y, sr = librosa.load("res/music/music.wav")

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

videos = os.listdir(videofiles)
# make empty videofileclip calledpip combinedVideo
combinedVideo = None
currOnset = 0

# Peak sorting algo
videos.sort(key=lambda x: (x.split('_')[1], int(x.split('_')[2].split('-')[0]), int(x.split('_')[2].split(
    '-')[1]), int(x.split('_')[2].split('-')[2]), int(x.split('_')[2].split('-')[3].split('.')[0])))



for i in range(len(videos)):
    video = VideoFileClip(videofiles + videos[i]).subclip(initialtrim)
    # Check to see if it is the first clip. If so, trim clip to have the 16th second (or what the clippoi is) be at the osnet and
    # cut between the current onset and the next onset
    if (combinedVideo is None):
        enddelay = (onset_times_arr[currOnset+1]-onset_times_arr[currOnset])/2
        combinedVideo = video.subclip(
            max(0, clippoi-onset_times_arr[currOnset]), clippoi+enddelay+max(0, enddelay-clippoi) + onset_times_arr[currOnset] - (clippoi - max(0, clippoi-onset_times_arr[currOnset])))
    # Check to see if it is the last clip or if the onset is the last onset, play to end if it is
    elif (i == len(videos) - 1 or currOnset == len(onset_times_arr) - 1):
        combinedVideo = concatenate_videoclips([combinedVideo, video.subclip(
            max(0, clippoi+combinedVideo.duration-onset_times_arr[currOnset]), video.duration)])
    else:
        enddelay = (onset_times_arr[currOnset+1]-onset_times_arr[currOnset])/2
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

if (combineAudio):
    new_audioclip = CompositeAudioClip([combinedVideo.audio, audioclip])
else:
    new_audioclip = audioclip
combinedVideo.audio = new_audioclip.subclip(
    0, combinedVideo.duration).fx(AudioClip.audio_fadeout, duration=fadeDuration)
# put text that says "beat" on each time the onset is detected
combinedVideo.write_videofile(resultfile, fps=resultfps)
