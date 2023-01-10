from tkinter import *
import pygame
from tkinter import filedialog
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
import tkinter.ttk as ttk
from shutil import copyfile
from os import listdir, remove
from os.path import isfile
from random import shuffle
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import time


# bezposrednie stworzenie okna aplikacji
root = Tk()

# nazwanie okna jako Audio Player
root.title('Audio Player')

# ustawienie wielkosci okna aplikacji oraz jego polozenia na ekranie
root.geometry("700x600+200+50")

# Inicjalizacja modulu mixer
pygame.mixer.init()

# zmienna przechowujaca nazwe aktualnie wyswietlanej playlisty
global playlist
playlist = None


# #### funkcja odpowiadajaca za wyswietlanie czasu odtwarzania pliku audio oraz za aktualizacje suwaka czasu odtwarzania
def play_time():
    # jezeli utwor nie jest odtwarzany to nie kontynuujemy wykonywania funkcji (przerywamy petle)
    if stopped:
        return

    # zmienna przechowujaca czas odtwarzania muzyki
    current_time = pygame.mixer.music.get_pos() / 1000

    # do zmiennej song przypisujemy nazwe wybranego pliku i nastepnie do zmiennej przypisujemy sciezke pliku
    song = song_box.get(song_box.curselection())
    song = f'./audio/{song}'

    # zaladowanie muzyki dzieki modulowi Mutagen
    # sprawdzamy rozszerzenie pliku i uzywamy odpowiedniej funkcji
    if song[-4:] == '.mp3' or song[-4:] == '.MP3':
        song_mut = MP3(song)
    elif song[-4:] == '.wav' or song[-4:] == '.WAV':
        song_mut = WAVE(song)
    elif song[-5:] == '.flac' or song[-4:] == 'FLAC':
        song_mut = FLAC(song)
    elif song[-4:] == '.ogg' or song[-4:] == '.OGG':
        song_mut = OggVorbis(song)
    else:
        return

    # zmienna przechowujaca dlugosc utworu
    global song_length
    song_length = song_mut.info.length
    # konwertujemy do formatu minuty:sekundy
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    # zwiekszamy aktualny czas odtwarzania o 1
    current_time += 1

    # warunek jezeli nastepuje koniec utworu
    if int(slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length}  of  {converted_song_length}  ')
        next_song()
    # warunek jezeli utwor jest zapauzowany
    elif paused:
        pass
    # warunek jezeli pozycja wskaznika na suwaku jest rowna aktualnemu czasowi odtwarzania
    # (czyli nie ruszylismy wskaznika)
    elif int(slider.get()) == int(current_time):
        # aktualizujemy wskaznik na odpowiednia pozycje
        slider_position = int(song_length)
        slider.config(to=slider_position, value=int(current_time))
    # warunek kiedy ruszylismy wskaznik
    else:
        # aktualizujemy wartosc wskaznika na odpowiednia pozycje
        slider_position = int(song_length)
        slider.config(to=slider_position, value=int(slider.get()))

        # konwertujemy do formatu minuty:sekundy
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(slider.get())))

        # wyswietlamy uzyskane czasy w oknie
        status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')

        # przesuniecie wskaznika suwaka
        next_time = int(slider.get()) + 1
        slider.config(value=next_time)

    # po sekundzie odwolujemy sie ponownie do funkcji play_time()
    status_bar.after(1000, play_time)


# ##################################################### funkcja odpowiadajaca za dodanie jednej piosenki do bazy utworow
def add_song():
    # zmienna song przechowuje sciezke pliku audio
    song = filedialog.askopenfilename(initialdir='~', title="Choose A Song",
                                      filetypes=(("audio Files", "*.mp3 *.wav *.flac *.ogg *.mid"), ))

    # usuniecie informacji o katalogu i rozszerzeniu z nazwy utworu
    edited_song = song.split('/')[-1]
    copyfile(song, f'./audio/{edited_song}')

    # dodanie utworu do listboxa
    song_box.insert(END, edited_song)

# ######################################################### funkcja odpowiadajaca za dodanie wielu piosenek do playlisty
def add_many_songs_to_playlist():
    # zmienna songs przechowuje sciezki plikow audio, a zmienna file_name przechowuje sciezke pliku playlisty
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song",
                                        filetypes=(("audio Files", "*.mp3 *.wav *.flac *.ogg *.mid"),))
    file_name = filedialog.askopenfilename(initialdir='playlists/', title='Choose A Name Of The Playlist',
                                             filetypes=(("txt Files", "*.txt"),))

    # otwieramy plik playlisty w trybie dopisu
    with open(file_name, 'a') as file:
        # petla idaca po wszystkich wybranych utworach
        for song in songs:
            # zapisujemy sciezke utworu do pliku playlisty i przechodzimy do nowej linii
            file.write(song + '\n')

# ###################################################### funkcja odpowiadajaca za dodanie wielu piosenek do bazy utworow
def add_many_songs():
    # zmienna songs przechowuje sciezki plikow audio
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song",
                                        filetypes=(("audio Files", "*.mp3 *.wav *.flac *.ogg *.mid"), ))

    # w petli dodaj wszystkie wybrane utwory
    for song in songs:
        edited_song = song.split('/')[-1]
        copyfile(song, f'./audio/{edited_song}')
        song_box.insert(END, edited_song)

# ################################################################### funkcja odpowiadajaca za tworzenie nowej playlisty
def create_playlist():
    # zmienna songs przechowuje sciezki plikow audio, a zmienna file_name przechowuje sciezke pliku playlisty
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song",
                                        filetypes=(("audio Files", "*.mp3 *.wav *.flac *.ogg *.mid"), ))
    file_name = filedialog.asksaveasfilename(initialdir='playlists/', title='Choose A Name Of The Playlist',
                                             filetypes=(("txt Files", "*.txt"), ))

    # otwieramy plik playlisty w trybie zapisu
    with open(file_name, 'w') as file:
        # petla idaca po wszystkich wybranych utworach
        for song in songs:
            # zapisujemy sciezke utworu do pliku playlisty i przechodzimy do nowej linii
            file.write(song+'\n')

# ######################################################################### funkcja odpowiadajaca za usuniecie playlisty
def remove_playlist():
    # wybor pliku playlisty do usuniecia
    file_name = filedialog.askopenfilename(initialdir='playlists/', title='Choose A Playlist To Remove',
                                           filetypes=(("txt Files", "*.txt"), ))

    # funkcja usuniecia playlisty
    remove(file_name)

    # sprawdzamy czy usuwana playlista jest aktualnie wyswietlona
    edited_file_name = file_name.split('/')[-1].split('.')[0]
    if edited_file_name == playlist:
        stop()
        song_box.delete(0, END)
        playlist_name.config(text="Playlist = None")

# ####################################################################### funkcja odpowiadajaca za zaladowanie playlisty
def load_playlist():
    # zatrzymujemy muzyke, jesli jakas byla odtwarzana
    stop()
    # usuwamy utwory z listboxa
    song_box.delete(0, END)

    # wybor pliku playlisty do zaladowania
    file_name = filedialog.askopenfilename(initialdir='playlists/', title="Select A Playlist", 
                                           filetypes=(("txt Files", "*.txt"), ))

    # wyodrebniamy nazwe playlisty i zapisujemy do zmiennej playlist
    global playlist
    playlist = file_name.split('/')[-1].split('.')[0]

    # aktualizujemy wyswietlana nazwe obecnie odtwarzanej playlisty
    playlist_name.config(text=f"Playlist = {playlist}")

    # otwieramy plik playlisty w trybie odczytu
    with open(file_name, 'r') as file:
        # tworzymy liste utworow z pliku playlisty
        songs = file.readlines()
        # w petli idziemy po kolejnych utworach
        for song in songs:
            # sprawdzamy czy utwor jest na playliscie
            song = song.strip()
            if isfile(song):
                # wstawiamy utwor do listboxa
                song = song.split('/')[-1]
                song_box.insert(END, song)

# ######################################## funkcja odpowiadajace za losowa zmiane kolejnosci utworow na aktualnej liscie
def shuffle_songs():
    # zatrzymanie aktualnego utworu
    stop()

    # stworzenie zmiennej songs bedacej lista utworow
    songs = list(song_box.get(0, END))

    # funkcja przelosowania kolejnosci utworow w liscie
    shuffle(songs)

    #usuniecie utworow z listboxa
    song_box.delete(0, END)

    # w petli przechodzacej po kolejnych utworach w przelosowanej liscie dodajemy utwory do listboxa
    for song in songs:
        song_box.insert(END, song)


# ########################################################################## funkcja odpowiadajaca za odtworzenie muzyki
def play():
    if song_box.curselection() == ():
        song_box.selection_set(0)

    # ustawienie zmiennej stopped i paused na falsz, dzieki czemu utwor moze byc odtwarzany
    global stopped, paused
    stopped = False
    paused = False

    # do zmiennej song przypisujemy nazwe wybranego pliku i nastepnie do zmiennej przypisujemy sciezke pliku
    song = song_box.get(song_box.curselection())
    song = f'./audio/{song}'

    # uzywajac modulu mixer ladujemy utwor i go odtwarzamy (jednokrotnie)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # wywołanie funkcji play_time, aby uzyskać długość piosenki
    play_time()

    # aktualizujemy pozycje wskaznika suwaka czasu odtwarzania
    # ustawiamy wskaznik na poczatek suwaka oraz ustawiamy wartosc konca suwaka jako dlugosc utworu
    slider_position = int(song_length)
    slider.config(to=slider_position, value=0)


# ######################################################################### funkcja odpowiedzialna za zatrzymanie muzyki
global stopped
stopped = False
def stop():
    # resetujemy suwak czasu odtwarzania oraz status bar
    status_bar.config(text='')
    slider.config(value=0)

    # zatrzymujemy muzyke dzieki modulowi mixer
    pygame.mixer.music.stop()

    # usuwa zaznaczenie utworu w listboxie
    song_box.selection_clear(ACTIVE)

    # ustawienie zmiennej stopped na prawde
    global stopped
    stopped = True

# ############################################################### funkcja odpowiadajaca za odtworzenie nastepnego utworu
def next_song():
    # resetujemy suwak czasu odtwarzania oraz status bar
    status_bar.config(text='')
    slider.config(value=0)

    # zmienna next_one przechowuje numer aktualnego utworu
    next_one = song_box.curselection()

    # inkrementujemy zmienna next_one
    next_one = next_one[0]+1

    # jesli aktualny utwor jest ostatni na liscie, to przeskakujemy do pierwszego utworu na liscie
    if next_one > song_box.size()-1:
        next_one = 0

    # wybieramy nastepny utwor z listboxa
    song = song_box.get(next_one)

    # do zmiennej przypisujemy sciezke pliku
    song = f'./audio/{song}'

    # zaladowanie i odtworzenie utworu dzieki modulowi mixer
    global paused
    paused = False
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # odznaczenie poprzednio odtwarzanego utworu z listboxa
    song_box.selection_clear(0, END)

    # aktywowanie nowego utworu na listboxie
    song_box.activate(next_one)

    # zaznaczenie nowego utworu na listboxie
    song_box.selection_set(next_one, last=None)

# ############################################################ funkcja odpowiadajaca za uruchomienie poprzedniego utworu
def previous_song():
    # resetujemy suwak czasu odtwarzania oraz status bar
    status_bar.config(text='')
    slider.config(value=0)

    # zmienna next_one przechowuje numer aktualnego utworu
    next_one = song_box.curselection()

    # dekrementujemy zmienna next_one
    next_one = next_one[0]-1

    # jesli aktualny utwor jest pierwszy na liscie, to przeskakujemy do ostatniego utworu
    if next_one < 0:
        next_one = song_box.size()-1

    # wybieramy nastepny utwor z listboxa
    song = song_box.get(next_one)

    # do zmiennej przypisujemy sciezke pliku
    song = f'./audio/{song}'

    # zaladowanie i odtworzenie utworu dzieki modulowi mixer
    global paused
    paused = False
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # odznaczenie poprzednio odtwarzanego utworu z listboxa
    song_box.selection_clear(0, END)

    # aktywowanie nowego utworu na listboxie
    song_box.activate(next_one)

    # zaznaczenie nowego utworu na listboxie
    song_box.selection_set(next_one, last=None)

# ############################################################################ funkcja odpowiadajaca za usuniecie utworu
def delete_song():
    # przechowanie nazwy wybranego do usuniecia utworu i zatrzymanie odtwarzania muzyki
    song = song_box.get(song_box.curselection())
    stop()

    # usuniecie wybranego utworu
    song_box.delete(ANCHOR)
    remove(f'./audio/{song}')

# ############################################################### funkcja odpowiadajaca za usuniecie wszysstkich utworow
def delete_all_songs():
    # zatrzymanie odtwarzania muzyki
    stop()

    # usuniecie utworow
    song_box.delete(0, END)
    songs = [f for f in listdir('./audio')]
    for song in songs:
        remove(f'./audio/{song}')

# ############################################################## funkcja odpowiadajaca za zaladowanie wszystkich utworow
def load_all_songs():
    # aktualizacja wyswietlania informacji o aktualnie uruchomionej playliscie
    global playlist
    playlist=None
    playlist_name.config(text= "Playlist = None")

    # usuniecie wszystkich aktualnych utworow z listboxa
    song_box.delete(0, END)

    # wstawienie do listboxa wszystkich utworow
    songs = [f for f in listdir('./audio')]
    for song in songs:
        song_box.insert(END, song)


# ############################################################## funkcja odpowiadajaca za pauzowanie/odpauzowanie muzyki
global paused
paused = False
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # odpauzuj
        pygame.mixer.music.unpause()
        paused = False
    else:
        # zapauzuj
        pygame.mixer.music.pause()
        paused = True

# ############ funkcja odpowiadajaca za dzialanie suwaka czasu odtwarzania (przeciagniecie wskaznika na dowolna pozycje)
def slide(x):
    # do zmiennej song przypisujemy nazwe wybranego pliku i nastepnie do zmiennej przypisujemy sciezke pliku
    song = song_box.get(song_box.curselection())
    song = f'./audio/{song}'

    # odtworzenie muzyki od momentu ustalonego przez pozycje wskaznika na suwaku czasu odtwarzania
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(slider.get()))

    if paused:
        pygame.mixer.music.pause()

# ######################################################################### funkcja odpowiadajaca za regulacje glosnosci
def volume(x):
    if volume_slider.get() == 0:
        mute_button['state'] = DISABLED
    else:
        mute_button['state'] = NORMAL
    # ustawienie glosnosci w zaleznosci od ustawienia suwaka glosnosci
    pygame.mixer.music.set_volume(volume_slider.get())

    # zmienna przechowuje aktualna glosnosc
    current_volume = pygame.mixer.music.get_volume()

    # dla ulatwienia mnozymy wartosc aktualnej glonosci (zakres od 0 do 1) przez 100
    current_volume = current_volume * 100

    # sprawdzamy w jakim przedziale miesci sie wartosc glosnosci i na tej podstawie
    # wyswietlamy odpowiednia ikone obrazujaca poziom glosnosci
    if int(current_volume) == 0:
        volume_meter.config(image=vol0)
    elif 0 < int(current_volume) <= 20:
        volume_meter.config(image=vol1)
    elif 20 <= int(current_volume) <= 40:
        volume_meter.config(image=vol2)
    elif 40 <= int(current_volume) <= 60:
        volume_meter.config(image=vol3)
    elif 60 <= int(current_volume) <= 80:
        volume_meter.config(image=vol4)
    elif 80 <= int(current_volume) <= 100:
        volume_meter.config(image=vol5)

# ################################################# funkcja odpowiadajaca za wyswietlenie tzw. "waveform" granego utworu
def showing_waveform():
    # do zmiennej song przypisujemy nazwe wybranego pliku i nastepnie do zmiennej przypisujemy sciezke pliku
    audio_file = song_box.get(song_box.curselection())
    audio_file = f'./audio/{audio_file}'

    # pobieranie danych z pliku o sciezce przechowanej w zmiennej audio_file
    data, samplerate = sf.read(audio_file)

    print(samplerate)

    # zmienna n przechowuje dlugosc tablic znajdujacych sie w zmiennej data
    n = len(data)

    # zmienna Fs przechowuje wartosc okreslajaca liczbe probek w jednostce czasu
    # pobranych ze zrodlowego sygnalu ciaglego w celu uzyskania sygnalu dyskretnego
    Fs = samplerate

    # rozdzielamy lewy i prawy kanał audio
    # w przypadku pliku mono nie rozdzielamy kanalow
    try:
        lchannel, rchannel = data.transpose()
    except:
        lchannel = data

    # zmienna time_axis reprezentuje os x wykresu
    # zmienna sound_axis reprezentuje os y wykresu (bierzemy pod uwage tylko jeden kanal audio)
    time_axis = np.linspace(0, n / Fs, n, endpoint=False)
    sound_axis = lchannel

    # edycja szerokosci okna w ktorym wyswietla sie wykres
    f = plt.figure('Waveform')
    f.set_figwidth(12)

    # nazywamy osie wykresu oraz wyswietlamy wykres
    plt.plot(time_axis, sound_axis)
    plt.xlabel("Time (s)")
    plt.ylabel("Audio")
    plt.show()

# ############################################# funkcja odpowiadajaca za wyswietlenie tzw. spektrogramu wybranego utworu
def showing_spectrogram():
    # do zmiennej song przypisujemy nazwe wybranego pliku i nastepnie do zmiennej przypisujemy sciezke pliku
    audio_file = song_box.get(song_box.curselection())
    audio_file = f'./audio/{audio_file}'

    # pobieranie danych z pliku o sciezce przechowanej w zmiennej audio_file
    data, samplerate = sf.read(audio_file)

    # zmienna Fs przechowuje wartosc okreslajaca liczbe probek w jednostce czasu
    # pobranych ze zrodlowego sygnalu ciaglego w celu uzyskania sygnalu dyskretnego
    Fs = samplerate

    # rozdzielamy lewy i prawy kanał audio
    # w przypadku pliku mono nie rozdzielamy kanalow
    try:
        lchannel, rchannel = data.transpose()
    except:
        lchannel = data

    # zmienna sound_axis reprezentuje os y wykresu (bierzemy pod uwage tylko jeden kanal audio)
    sound_axis = lchannel

    #edycja szerokosci okna w ktorym wyswietla sie wykres
    f = plt.figure('Spectrogram')
    f.set_figwidth(12)

    # nazywamy osie wykresu oraz wyswietlamy wykres
    plt.specgram(sound_axis, Fs=Fs)
    plt.colorbar(label='Intensity (dB)', orientation='horizontal')
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.show()

# ########################################################################## funkcja odpowiadajaca za wyciszenie dzwieku
def mute():
    # ustawiamy glosnosc na 0
    pygame.mixer.music.set_volume(0)

    # aktualizujemy miernik glosnosci
    volume_meter.config(image=vol0)

    # ustawiamy pozycje wskaznika na suwaku glosnosci
    volume_slider.config(value=0)

    # wylaczamy mozliwosc klikniecia przycisku
    mute_button['state'] = DISABLED

# -------------------------------------------TWORZENIE ELEMENTOW W OKNIE APLIKACJI--------------------------------------

# stworzenie Master Frame
master_frame = Frame(root)
master_frame.pack(pady=20)

# stworzenie elementu sluzacego do wyswietlania informacji dotyczacej aktualnie uruchomionej playlisty
playlist_name = Label(root, text=f"Playlist = {playlist}", relief=GROOVE)
playlist_name.pack(fill=X, padx=0)

# stworzenie elementu sluzacego do wyswietlania playlisty
song_box = Listbox(master_frame, bg="grey", fg="black", width=80, )
song_box.grid(row=0, column=0)

# stworzenie suwaka sluzacego do przeszukiwania playlisty
scrollbar = Scrollbar(master_frame, orient = 'vertical', command=song_box.yview,)
scrollbar.grid(row=0, column=1, sticky='NS')
song_box.config(yscrollcommand=scrollbar.set)

# definiujemy ikony przyciskow sterowania odtwarzaczem
back_btn_img = PhotoImage(file='images/back.png')
forward_btn_img =  PhotoImage(file='images/forward.png')
play_btn_img =  PhotoImage(file='images/play.png')
pause_btn_img =  PhotoImage(file='images/pause.png')
stop_btn_img =  PhotoImage(file='images/stop.png')

# definiujemy ikony obrazujace ustawiony poziom glosnosci
global vol0
global vol1
global vol2
global vol3
global vol4
global vol5
vol0 = PhotoImage(file='images/volume0.png')
vol1 = PhotoImage(file='images/volume1.png')
vol2 = PhotoImage(file='images/volume2.png')
vol3 = PhotoImage(file='images/volume3.png')
vol4 = PhotoImage(file='images/volume4.png')
vol5 = PhotoImage(file='images/volume5.png')

# stworzenie Controls Frame
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=20)

# stworzenie miernika glosnosci
volume_meter = Label(master_frame, image=vol0)
volume_meter.grid(row=1, column=1, padx=10)

# stworzenie ramki dla suwaka glosnosci
volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=2, column=1, padx=30)

# stworzenie ramki dla suwaka czasu odtwarzania
slider_frame = LabelFrame(master_frame, text="Song duration")
slider_frame.grid(row=2, column=0, padx=30)

# stworzenie przyciskow sterowania odtwarzaczem
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

# stworzenie Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# stworzenie zakladki Add Songs
add_songs_menu = Menu(my_menu)
my_menu.add_cascade(label="Add songs", menu=add_songs_menu)

# stworzenie opcji Add One Song
add_songs_menu.add_command(label="Add one song", command=add_song)

# stworzenie opcji Add Many Songs
add_songs_menu.add_command(label="Add many songs", command=add_many_songs)
add_songs_menu.add_command(label="Add many songs to a playlist", command=add_many_songs_to_playlist)

# stworzenie zakladki Remove Songs
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove songs", menu=remove_song_menu)

# stworzenie opcji Delete A Song
remove_song_menu.add_command(label="Delete a song", command=delete_song)

# stworzenie opcji Delete All Songs
remove_song_menu.add_command(label="Delete all songs", command=delete_all_songs)

# stworzenie zakladki Playlists
playlists_menu = Menu(my_menu)
my_menu.add_cascade(label="Playlists", menu=playlists_menu)
playlists_menu.add_command(label="Create a playlist", command=create_playlist)
playlists_menu.add_command(label="Load a playlist", command=load_playlist)
playlists_menu.add_command(label="Remove a playlist", command=remove_playlist)
playlists_menu.add_command(label="Load all songs", command=load_all_songs)

# stworzenie zakladki Additional
additional_menu = Menu(my_menu)
my_menu.add_cascade(label = "Additional", menu=additional_menu)
additional_menu.add_command(label="Shuffle song order", command=shuffle_songs)

# stworzenie Status Bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# stworzenie suwaka czasu odtwarzania
slider = ttk.Scale(slider_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
slider.pack(pady=10)

# stworzenie suwaka glosnosci
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=HORIZONTAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)

# stworzenie przycisku powodujacego wyciszenie dzwieku
mute_button = Button(volume_frame, text="Mute", command=mute)
mute_button.pack(pady=10)

# stworzenie przycisku powodujacego wyswietlenie wykresu
waveform_button = Button(root, text="Show waveform", command=showing_waveform)
waveform_button.pack(pady=30, anchor=CENTER)

# stworzenie przycisku powodujacego wyswietlenie spektrogramu
spectrogram_button = Button(root, text="Show spectrogram", command=showing_spectrogram)
spectrogram_button.pack(anchor=CENTER)

volume(100)

# nieskonczona petla, dzieki ktorej widzimy okno aplikacji
root.mainloop()