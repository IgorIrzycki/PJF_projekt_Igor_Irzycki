# PJF_projekt_Igor_Irzycki

This project was made as a part of Functional Programming course for Military University of Technology.

![image](https://user-images.githubusercontent.com/97196620/211571868-1eb84e10-55d0-4ac2-aff9-ca914ca6f73a.png)

## :notes: Description :notes:
The project presents an application that is an Audio Player, which can play audio files in MP3, WAV, FLAC or OGGVorbis formats. 
It has an audio file and playlist database ("audio" and "playlists" folders) as well as many menu functions, such as:

* **Add one song** - users can add one song to audio file database (it will also show up in ListBox)
* **Add many songs** - users can add multiple songs at once to audio file database (they will also show up in ListBox)
* **Add many songs to a playlist** - users can add multiple songs at once to a playlist specified by themselves  
* **Delete a song** - users can choose a song shown in ListBox and delete it from audio file database 
* **Delete all songs** - users can delete all songs from audio file database
* **Create a playlist** - users can create (and name) a new playlist by choosing songs from audio file database
* **Load a playlist** - users can load an existing playlist by choosing it from playlist database (songs will show up in ListBox)
* **Remove a playlist** - users can delete an existing playlist by choosing it from playlist database (if deleted playlist has been shown up in ListBox, then the ListBox is being cleared)
* **Load all songs** - users can load all songs existing in an audio file database
* **Shuffle song order** - users can shuffle song order shown in the ListBox

There's also a few buttons:
* **forward button** - plays next song in the ListBox (if the current song is last on the list, it jumps to the first song)
* **back button** - plays previous song in the ListBox (if the current song is first on the list, it jumps to the last song)
* **play button** - plays a song selected in the ListBox
* **pause button** - pauses/unpauses selected song
* **stop button** - turns off a song and clears ListBox selection
* **mute button** - mutes sound volume
* **show waveform button** - shows waveform chart of a sog selected in the ListBox
* **show spectrogram button** - shows spectrogram chart of a sog selected in the ListBox

Let's not forget about sliders:
* **volume slider** - users can change volume of a song
* **song duration slider** - users can choose a specific moment of a song

The Audio Player also shows elapsed time of currently playing song and name of currently chosen playlist.

## :notes: Used technologies :notes:
* Python 3.11
* Tkinter
* Pygame 2.1.3.dev8
* Mutagen 1.46.0
* Shutil
* SoundFile 0.11.0
* NumPy 1.24.1
* Matplotlib 3.6.2

## :notes: Getting started :notes:
Make sure that you are using version 3.11 of Python.
To adding all modules and packages required for this project, open up a terminal and navigate to the directory of your Python project. Once you are there, type the following commands:
```
$ pip install mutagen
$ pip install pygame
$ pip install soundfile
$ pip install numpy
$ pip install matplotlib
```
