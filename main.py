import os
from glob import glob
import music_tag
import csv


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def find_mp3s(mp3_dir):
    num_mp3s = 0

    out = csv.writer(open("d:\low_quality_mp3s.csv", "w", newline=''), delimiter="%", quoting=csv.QUOTE_NONE, escapechar='\\')
    out.writerow(["artist", "title", "album", "bitrate", "codec", "length", "sample rate", "location"])

    # Use a breakpoint in the code line below to debug your script.
    print(f'Looking for mp3s in {mp3_dir}')  # Press Ctrl+F8 to toggle the breakpoint.

    result = [y for x in os.walk(mp3_dir) for y in glob(os.path.join(x[0], '*.mp3'))]
    num_mp3s = len(result)

    num_mp3s = 0

    for name in result:
        if name.endswith(".mp3"):
            num_mp3s+=1
            # print("{:5d}) {}".format(num_mp3s, name))
            f = music_tag.load_file(name)
            title = f['title']
            artist = f['artist']
            bitrate = int(f['#bitrate'])/1000
            codec = f['#codec']
            length = int(f['#length'])
            sr = int(f['#samplerate'])
            album = f['album']
            #print("   {}, {}, {}, {}, {}, {}".format(artist, title,bitrate/1000, codec, length, sr))
            if bitrate < 256:
                print("%5d) %-*s %-*s %-*s %3d %-*s %5d, %-*s" % (num_mp3s, 25, artist, 40, title, 20, album, bitrate, 6, codec, length, 64, name))
                info = [artist, title, album, bitrate, codec, length, sr, name]
                # print(info)
                out.writerow(info)

    return(num_mp3s)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    number_of_mp3s = find_mp3s('M:\\')
    print("Found {} mp3s".format(number_of_mp3s))

