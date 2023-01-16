import os
from glob import glob
import music_tag
import csv
import xlwt
import time


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def find_mp3s(mp3_dir):
    num_mp3s = 0
    sheet = "low_qual_mp3s"
    filename = "D:\\low_quality_mp3s"

    book = xlwt.Workbook()
    sh = book.add_sheet(sheet)
    currow = 0
    curcol = 0
    column_hdrs = ["artist", "title", "album", "bitrate", "codec", "length", "sample rate", "location"]

    out = csv.writer(open(filename + ".csv", "w", newline=''), delimiter="%", quoting=csv.QUOTE_NONE, escapechar='\\')
    out.writerow( column_hdrs )
    # sh.write( column_hdrs )
    c0 = "artist"
    sh.write(currow, 0, c0)
    sh.write(currow, 1, "title")
    sh.write(currow, 2, "album")
    sh.write(currow, 3, "bitrate")
    sh.write(currow, 4, "codec")
    sh.write(currow, 5, "length")
    sh.write(currow, 6, "sample rate")
    sh.write(currow, 7, "location")
    currow+=1

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
            artist = str(f['artist'])
            title = str(f['title'])
            album = str(f['album'])
            bitrate = int(f['#bitrate'])/1000
            codec = str(f['#codec'])
            length = int(f['#length'])
            sr = int(f['#samplerate'])
            # print("   {}, {}, {}, {}, {}, {}".format(artist, title,bitrate/1000, codec, length, sr))
            if bitrate < 256:
                print("%5d) %-*s %-*s %-*s %3d %-*s %5d, %-*s" % (num_mp3s, 25, artist, 40, title, 20, album, bitrate, 6, codec, length, 64, name))
                info = [artist, title, album, bitrate, codec, length, sr, name]
                # print(info)
                out.writerow(info)
                sh.write(currow, 0, artist)
                sh.write(currow, 1, title)
                sh.write(currow, 2, album)
                sh.write(currow, 3, bitrate)
                sh.write(currow, 4, codec)
                sh.write(currow, 5, length)
                sh.write(currow, 6, sr)
                sh.write(currow, 7, name)
                currow+=1

    book.save(filename + ".xls")

    return(num_mp3s)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # music_dir = 'M:\\'
    music_dir = 'E:\\Music'
    start_time = time.time()
    number_of_mp3s = find_mp3s( music_dir )
    print("Found {} mp3s at {} in {:4.2f} seconds".format(number_of_mp3s, music_dir, (time.time() - start_time)))

