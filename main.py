import os
from glob import glob
import music_tag
import csv
import time
import sys
import argparse
import xlsxwriter

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def find_mp3s(mp3_dir, is_low_bitrate, is_various, make_correction):

    if is_low_bitrate:
        # sheet = "low_qual_mp3s"
        filename = "D:\\low_quality_mp3s"
    elif is_various:
        # sheet = "various_artists_mp3s"
        filename = "D:\\various_artists_mp3s"
    else:
        print("INVALID CONFIG!!! is_low_bitrate {}, is_various {}".format(is_low_bitrate, is_various))
        return -1

    wb = xlsxwriter.Workbook(filename + '.xlsx')
    ws = wb.add_worksheet('low_qual_mp3s')

    row = 0
    col = 0
    column_headers = ["artist", "title", "album", "album_artist", "bitrate", "codec", "length", "sample rate", "location"]
    column_widths = [32, 32, 32, 32, 7, 7, 7, 7, 48]
    column_align = [{'align': 'left'}, {'align': 'left'}, {'align': 'left'}, {'align': 'left'}, {'align': 'center'}, {'align': 'center'}, {'align': 'center'}, {'align': 'center'}, {'align': 'left'} ]

    out = csv.writer(open(filename + ".csv", "w", newline=''), delimiter="%", quoting=csv.QUOTE_NONE, escapechar='\\')
    out.writerow( column_headers )

    for hdr in column_headers:
        print("{} of {}) colhdr {} ({})".format(col+1, len(column_headers), hdr, column_align[col]))
        ws.write(row, col, hdr)
        center = wb.add_format(column_align[col])
        ws.set_column(col, col, column_widths[col], center)  # Set column width
        col += 1

    # Adding autofilters to the column headers
    ws.autofilter( row, 0, row, len(column_headers)-1 )

    row += 1
    col = 0

    # Use a breakpoint in the code line below to debug your script.
    print(f'Looking for mp3s in {mp3_dir}')  # Press Ctrl+F8 to toggle the breakpoint.

    result = [y for x in os.walk(mp3_dir) for y in glob(os.path.join(x[0], '*.mp3'))]
    num_mp3s = len(result)
    print( num_mp3s )

    num_mp3s = 0

    for name in result:
        if name.endswith(".mp3"):
            num_mp3s += 1
            # print("{:5d}) {}".format(num_mp3s, name))
            f = music_tag.load_file(name)

            artist = str(f['artist'])
            title = str(f['title'])
            album = str(f['album'])
            album_artist = str(f['album artist'])
            bitrate = int(f['#bitrate'])/1000
            codec = str(f['#codec'])
            length = int(f['#length'])
            sr = int(f['#samplerate'])
            # print("   {}, {}, {}, {}, {}, {}, {}".format(artist, title, album_artist, bitrate/1000, codec, length, sr))
            if ((is_low_bitrate is True) and (bitrate < 256)) or \
                    ((is_various is True) and
                     (
                            (album_artist == 'Various')
                            or (album_artist == 'various Artists')
                            or (album_artist == 'Various Artists')
                            or (album_artist == 'Various artists')
                            # or (album_artist == '')
                     )):
                print("%5d) %-*s %-*s %-*s %-*s %3d %-*s %5d, %-*s" %
                      (num_mp3s, 25, artist, 40, title, 20, album, 25, album_artist, bitrate, 6, codec, length, 64, name))
                if make_correction:
                    print("Making correction to artist {}".format(artist))
                    f['album_artist'] = artist
                    f.save()
                info = [artist, title, album, album_artist, bitrate, codec, length, sr, name]

                for item in info:
                    ws.write(row, col, item)
                    col += 1

                row += 1
                col = 0

    wb.close()

    return num_mp3s


if __name__ == '__main__':
    number_of_mp3s = 0
    music_dir = 'M:\\'
    # music_dir = 'E:\\Music'

    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory')
    parser.add_argument('-v', '--various', action='store_true')
    parser.add_argument('-l', '--low_bitrate', action='store_true')
    parser.add_argument('-c', '--correct', action='store_true')
    # parser.add_argument('-h', '--help')
    args = parser.parse_args()
    print(args.directory, args.various, args.low_bitrate)

    if args.directory:
        music_dir = args.directory
    else:
        print("no directory defined, using {}".format(music_dir))

    start_time = time.time()
    number_of_mp3s = find_mp3s( music_dir, args.low_bitrate, args.various, args.correct )
    print("Found {} mp3s at {} in {:4.2f} seconds".format(number_of_mp3s, music_dir, (time.time() - start_time)))
