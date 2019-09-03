# Osu! Music Player

A music player for osu!, deduplicate same songs.

This copys and parses your `osu!.db` & `collection.db`, write json data to `osudb.js`,  
so you can play your music by opening `OsuMusicPlayerLite.html`.

## Requirements

* Python, though I only tested this on Windows CPython3.6.
* Popular browser, tested on Chrome, Firefox on Windows and Android.

## How to use

Download this repo, or these 3 files to same directory:
 `OsuMusicPlayer.py`, `osudb.py`, `OsuMusicPlayerLite.html`.

Then, some one-time configuration is needed:

1. Configure the `osu_root_path` variable in `OsuMusicPlayer.py` as it is used to copy your databases. You may leave it as-is if you're a Windows user who uses the default osu! path.
2. Configure the `copy_db_path` variable in `OsuMusicPlayer.py`. It'll use this path to store copied osu! databases. This path must exist.

Then, run `OsuMusicPlayer.py` to update `osudb.js`.  
You'll have to run this everytime after you download some beatmaps to your osu! to add them.

Everytime you want to play music, just open `OsuMusicPlayerLite.html`.  
It'll load `osudb.js`. Select one collection and enjoy!  
It supports zxcv, space and up, down, left, right!

You may also copy your `Songs`, `OsuMusicPlayerLite.html`, `osudb.js` to your phone,
 and set `osuSongsPath` in `osudb.js` correctly to listen your osu! music using your phone.  
Or, even better, run a streaming server(you may use this [simple bottle server](https://github.com/KirkSuD/ChromecastLocalPlayer/blob/master/BottlePartialContent.py)) on your computer, copy your `OsuMusicPlayerLite.html`,
 `osudb.js` to your phone, and set `osuSongsPath` in `osudb.js` correctly.

## How it works

`OsuMusicPlayer.py` copys your databases, parses them using `osudb.py`, and save them to `osudb.js`.

`OsuMusicPlayerLite.html` reads `osudb.js` and present the contents to you.

## Related projects

* osudb, this project uses [osudb](https://github.com/KirkSuD/osudb) to parse osu! databases. `osudb.py` is a copy of it.

## Some screenshots

![Screenshot - OsuMusicPlayerLite.html](https://raw.githubusercontent.com/KirkSuD/OsuMusicPlayer/master/screenshot/screenshot.png)

## TODO

* The code is messy; clean it!
* Write `OsuMusicPlayer.html`.

## Bugs

Currently, there are no bugs found.

However, the databases' format may change, and the current parsing method may fail.  
If you find any bug, please inform me.
