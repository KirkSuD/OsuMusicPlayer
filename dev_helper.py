#-*-coding:utf-8;-*-

"""
OsuMusicPlayer - A music player for osu, parse osu!.db, collection.db,
 then make json to form a static web music player.
Required 3rd-party module: osudb

This is the development helper script for observing the databases,
 also a tool to export .db files to readable .csv files,
 basically all info of osu!.db and collection.db can be viewed here.

Version 0.1
Written by: KirkSuD
Written @ 2019/08/22
Last modified @ 2019/08/22
Current found bugs: None
TODO: None

Roughly tested @ 2019/08/22
with osu!.db ver.20190816, collection.db ver.20190808.

osu! directory path:
Windows: %localappdata%/osu!
Mac OSX: /Applications/osu!.app/Contents/Resources/drive_c/Program Files/osu!/
"""

def build_beatmaps_attribute_set(beatmaps, attribute_index):
    res = set()
    for bm in beatmaps:
        res.add(bm[attribute_index])
    return res

def same_folder_different_attribute(beatmaps, attribute_index):
    for i,bm1 in enumerate(beatmaps):
        for j,bm2 in enumerate(beatmaps):
            if j<=i: continue
            if bm1[45] == bm2[45] and bm1[attribute_index] != bm2[attribute_index]:
                print()
                print(bm1[45]) ## 45 is folder name
                print(bm1[attribute_index])
                print(bm2[attribute_index])

def list_folders(path):
    for _, folders, _ in os.walk(path):
        return folders

def build_same_folder_attribute_set(beatmaps, attribute_index, folder_name):
    res = set()
    for bm in beatmaps:
        if bm[45] == folder_name:
            res.add(bm[attribute_index])
    return res

def get_song_from_beatmap(beatmap):
    return {"artist": beatmap[1], "title": beatmap[3], "file": beatmap[7], "folder": beatmap[45]}

def get_songs(beatmaps):
    """
    Generate a list of songs without duplication.
    """
    folders = set()
    res = []
    for bm in beatmaps:
        folder_name = bm[45]
        if folder_name in folders: continue
        folders.add(folder_name)
        res.append(get_song_from_beatmap(bm))
    return res

def generate_md5_to_song_dict(beatmaps):
    """
    Generate a dict from md5 to song with duplications.
    Used by md5_to_song_dict of get_songs_from_md5().
    """
    res = {}
    for bm in beatmaps:
        if bm[8] in res: raise ValueError("generate_md5_to_song_dict(beatmaps): md5 collision: "+bm[8])
        res[bm[8]] = get_song_from_beatmap(bm)
    return res

def get_songs_from_md5(md5_to_song_dict, md5_list):
    """
    Generate a list of songs from a given md5_list by using md5_to_song_dict.
    """
    """
    13 [1, 3, 7, 35, 42, 44, 45, 47, 48, 49, 50, 51, 52]

    These attributes are the same if having the same folders:
    1 Artist name
    3 Song title
    7 Audio file name
    # 35 Local beatmap offset # not knowing what this is # always 0 ?
    # 42 Is beatmap unplayed # not knowing what this is # always True ?
    # 44 Is the beatmap osz2 # always True ?
    45 Folder name of the beatmap, relative to Songs folder # used as Primary key
    # 47 Ignore beatmap sound
    # 48 Ignore beatmap skin
    # 49 Disable storyboard
    # 50 Disable video
    # 51 Visual override # 47-51 useless # mine are always True
    # 52 Last modification time (?) # not knowing what this is # always 0 ?
    """
    folder_set = set()
    res = []
    for md5 in md5_list:
        song = md5_to_song_dict[md5]
        if song["folder"] in folder_set: continue
        folder_set.add(song["folder"])
        res.append(song)
    return res

def get_collections(beatmaps, collections):
    md5_to_songs = generate_md5_to_song_dict(beatmaps)
    return [[col[0], get_songs_from_md5(md5_to_songs, col[2])] for col in collections]

if __name__ == "__main__":
    osu_root_path = r"%localappdata%/osu!"
    copy_db_path = r"./copied_osu_db"
    beatmaps_csv_path = r"./exported_csv/beatmaps.csv"
    songs_csv_path = r"./exported_csv/songs.csv"
    collections_csv_path = r"./exported_csv/collections.csv"

    import osudb ## 3rd-party module for parsing osu! databases

    import os
    import shutil
    import csv

    pjoin = os.path.join ## shortcut

    osu_root_path = os.path.expandvars(osu_root_path) ## https://stackoverflow.com/questions/53112401/percent-signs-in-windows-path
    copy_db_path = os.path.abspath(os.path.realpath(copy_db_path)) ## https://stackoverflow.com/questions/37863476/why-would-one-use-both-os-path-abspath-and-os-path-realpath
    beatmaps_csv_path = os.path.abspath(os.path.realpath(beatmaps_csv_path))
    songs_csv_path = os.path.abspath(os.path.realpath(songs_csv_path))
    collections_csv_path = os.path.abspath(os.path.realpath(collections_csv_path))
    osu_songs_path = pjoin(osu_root_path, "Songs")
    print("osu! root path:", osu_root_path)
    print("osu! songs path:", osu_songs_path)
    print("Copy databases to:", copy_db_path)
    print("Save beatmaps.csv:", beatmaps_csv_path)
    print("Save songs.csv:", songs_csv_path)
    print("Save collections.csv:", collections_csv_path)
    input("Press ENTER to continue...")

    print()
    print("Copying osu!.db and collection.db...")
    shutil.copyfile(pjoin(osu_root_path, "osu!.db"), pjoin(copy_db_path, "osu!.db"))
    shutil.copyfile(pjoin(osu_root_path, "collection.db"), pjoin(copy_db_path, "collection.db"))
    print("Copied.")

    print()
    print("Parsing databases...")
    osu_data = osudb.parse_osu(pjoin(copy_db_path, "osu!.db"))
    collection_data = osudb.parse_collection(pjoin(copy_db_path, "collection.db"))
    print("Parsed.")

    print()
    print("osu!.db basic information: ")
    print("""Version: %d
Folders: %d
Account unlocked: %s
Unlock time: %d
Player name: %s
Beatmaps: %d""" % tuple(osu_data[:6]))

    print()
    print("collection.db basic information:")
    print("""Version: %d
Collections: %d""" % tuple(collection_data[:2]))

    print()
    print("Collections (beatmaps count):")
    for col in collection_data[2]:
        print("%s (%d)" % (col[0], col[1]))

    print()
    print("Folders not in osu!.db:")
    db_folder_names = build_beatmaps_attribute_set(osu_data[6],45)
    for i in sorted(list(set(list_folders(osu_songs_path))-db_folder_names)):
        print(i)

    print()
    md5_count = len(build_beatmaps_attribute_set(osu_data[6], 8))
    if md5_count != len(osu_data[6]): ## collision
        print("MD5 collision found!")
        print("Beatmaps: %d / MD5: %d" % (len(osu_data[6]), md5_count))
    else:
        print("No MD5 collision found.")
    
    print()
    print("Analyzing same folder attributes...")
    res = [i for i in range(54)]
    for n,folder in enumerate(db_folder_names):
        ## print(n, len(res))
        tmp = [i for i in res]
        for i in tmp:
            try:
                if len(build_same_folder_attribute_set(osu_data[6], i, folder)) != 1:
                    res.remove(i)
            except:
                res.remove(i)
    print(len(res),res)

    bm_info = [['Int', 'Size in bytes of the beatmap entry'],
 ['String', 'Artist name'],
 ['String', 'Artist name, in Unicode'],
 ['String', 'Song title'],
 ['String', 'Song title, in Unicode'],
 ['String', 'Creator name'],
 ['String', 'Difficulty (e.g. Hard, Insane, etc.)'],
 ['String', 'Audio file name'],
 ['String', 'MD5 hash of the beatmap'],
 ['String', 'Name of the .osu file corresponding to this beatmap'],
 ['Byte',
  'Ranked status (0 = unknown, 1 = unsubmitted, 2 = pending/wip/graveyard, 3 = '
  'unused, 4 = ranked, 5 = approved, 6 = qualified, 7 = loved)'],
 ['Short', 'Number of hitcircles'],
 ['Short', 'Number of sliders (note: this will be present in every mode)'],
 ['Short', 'Number of spinners (note: this will be present in every mode)'],
 ['Long', 'Last modification time, Windows ticks.'],
 ['Byte/Single',
  'Approach rate. Byte if the version is less than 20140609, Single '
  'otherwise.'],
 ['Byte/Single',
  'Circle size. Byte if the version is less than 20140609, Single otherwise.'],
 ['Byte/Single',
  'HP drain. Byte if the version is less than 20140609, Single otherwise.'],
 ['Byte/Single',
  'Overall difficulty. Byte if the version is less than 20140609, Single '
  'otherwise.'],
 ['Double', 'Slider velocity'],
 ['Int-Double pair*',
  'An Int indicating the number of following Int-Double pairs, then the '
  'aforementioned pairs. Star Rating info for osu! standard, in each pair, the '
  'Int is the mod combination, and the Double is the Star Rating. Only present '
  'if version is greater than or equal to 20140609.'],
 ['Int-Double pair*',
  'An Int indicating the number of following Int-Double pairs, then the '
  'aforementioned pairs. Star Rating info for Taiko, in each pair, the Int is '
  'the mod combination, and the Double is the Star Rating. Only present if '
  'version is greater than or equal to 20140609.'],
 ['Int-Double pair*',
  'An Int indicating the number of following Int-Double pairs, then the '
  'aforementioned pairs. Star Rating info for CTB, in each pair, the Int is '
  'the mod combination, and the Double is the Star Rating. Only present if '
  'version is greater than or equal to 20140609.'],
 ['Int-Double pair*',
  'An Int indicating the number of following Int-Double pairs, then the '
  'aforementioned pairs. Star Rating info for osu!mania, in each pair, the Int '
  'is the mod combination, and the Double is the Star Rating. Only present if '
  'version is greater than or equal to 20140609.'],
 ['Int', 'Drain time, in seconds'],
 ['Int', 'Total time, in milliseconds'],
 ['Int',
  'Time when the audio preview when hovering over a beatmap in beatmap select '
  'starts, in milliseconds.'],
 ['Timing point+',
  'An Int indicating the number of following Timing points, then the '
  'aforementioned Timing points.'],
 ['Int', 'Beatmap ID'],
 ['Int', 'Beatmap set ID'],
 ['Int', 'Thread ID'],
 ['Byte', 'Grade achieved in osu! standard.'],
 ['Byte', 'Grade achieved in Taiko.'],
 ['Byte', 'Grade achieved in CTB.'],
 ['Byte', 'Grade achieved in osu!mania.'],
 ['Short', 'Local beatmap offset'],
 ['Single', 'Stack leniency'],
 ['Byte',
  'Osu gameplay mode. 0x00 = osu!Standard, 0x01 = Taiko, 0x02 = CTB, 0x03 = '
  'Mania'],
 ['String', 'Song source'],
 ['String', 'Song tags'],
 ['Short', 'Online offset'],
 ['String', 'Font used for the title of the song'],
 ['Boolean', 'Is beatmap unplayed'],
 ['Long', 'Last time when beatmap was played'],
 ['Boolean', 'Is the beatmap osz2'],
 ['String', 'Folder name of the beatmap, relative to Songs folder'],
 ['Long', 'Last time when beatmap was checked against osu! repository'],
 ['Boolean', 'Ignore beatmap sound'],
 ['Boolean', 'Ignore beatmap skin'],
 ['Boolean', 'Disable storyboard'],
 ['Boolean', 'Disable video'],
 ['Boolean', 'Visual override'],
 ['Int', 'Last modification time (?)'],
 ['Byte', 'Mania scroll speed']]
    print()
    print("These attributes are the same if having the same folders:")
    for i in res:
        print(i, bm_info[i][1])

    print()
    print("Writing beatmaps.csv...")
    with open(beatmaps_csv_path, "w", newline="", encoding="utf-8") as wf:
        csvwriter = csv.writer(wf)
        csvwriter.writerows(osu_data[6])
    print("Written.")
    
    print()
    print("Loading songs without duplication...")
    songs = get_songs(osu_data[6])
    print("Loaded, writing songs.csv...")
    mycsv_fieldnames = ["folder", "title", "artist", "file"]
    with open(songs_csv_path, "w", newline="") as wf:
        csvwriter = csv.DictWriter(wf, fieldnames=mycsv_fieldnames)
        #csvwriter.writerow(mycsv_fieldnames)
        csvwriter.writerows(songs)
    print("Written.")

    print()
    print("Loading collections without songs duplication...")
    cols = get_collections(osu_data[6], collection_data[2])
    print("Loaded, writing collections.csv...")
    wf = open(collections_csv_path, "w", newline="")
    csvwriter = csv.writer(wf)
    for col in cols:
        csvwriter.writerow([])
        csvwriter.writerow([col[0]])
        csvwriter.writerow(mycsv_fieldnames)
        for song in col[1]:
            csvwriter.writerow([song[i] for i in mycsv_fieldnames])
    wf.close()
    print("Written.")

    r"""
Possible primary keys:
id count description
29 398 'Beatmap set ID'
30 397 'Thread ID'
39 400 'Song tags'
45 396 'Folder name of the beatmap, relative to Songs folder' ## chosen
    """

