import pygame as p
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import io
import os
from random import randint

# enjoy my sparcely commented code lol

p.init()

screen = p.display.set_mode((240,270))

font = p.font.SysFont("arial", 10)

blip = p.mixer.Sound("blip.wav")

screen.blit(font.render("Loading...", True, (255,255,255)), (100, 100))
p.display.flip()

class Song:
    def __init__(self, file):
        # not gonna lie, this entire artwork function is written by AI, I still have no idea how to read mp3 metadata (I wrote the track info bit and the resize too tho lmao)
        def load_any_artwork(file):
            try:
                audio = MP3(file, ID3=ID3)
                track_length = audio.info.length
                if "TIT2" in audio:
                    track_name = audio["TIT2"].text[0]
                else:
                    track_name = "Unknown Title"
                for tag in audio.tags.values():
                    if isinstance(tag, APIC):
                        art = p.transform.scale(p.image.load(io.BytesIO(tag.data)), (200,200))
                        return art, track_length, track_name
                    
                folder_path = os.path.dirname(file)
                external_art = os.path.join(folder_path, "folder.jpg")
                
                if os.path.exists(external_art):
                    art = p.transform.scale(p.image.load(external_art), (200,200))
                    return art, track_length, track_name
                    
                print("No art found inside or beside the file.")
            except Exception as e:
                print(f"Error: {e}")
            return False, track_length, track_name
        # no more ai from here on out tho (thank goodness for that)

        def load_song(file):
            art, track_length, track_name = load_any_artwork(file)

            sound = p.mixer.Sound(file)

            return art, track_length, sound, track_name

        self.art, self.track_length, self.sound, self.track_name = load_song(file)
        self.seconds_played = 0
        self.playing = False
        self.channel = p.mixer.find_channel()

class Player:
    class Images:
        def __init__(self):
            self.icons = {
                "play" : p.image.load("icons/play.png").convert_alpha(),
                "pause" : p.image.load("icons/pause.png").convert_alpha(),
                "back" : p.image.load("icons/back.png").convert_alpha(),
                "forward" : p.image.load("icons/skip.png").convert_alpha(),
                "shuffle" : p.image.load("icons/shuffle.png").convert_alpha(),
                "shuffle_on" : p.image.load("icons/shuffle_on.png").convert_alpha()
            }

    def __init__(self):
        self.playlist = [] # for every song in the playlist, put Song({file location})
        self.current_song = 0
        self.play_song()
        self.textures = Player.Images()
        self.shuffle = False

    def render(self):
        screen.fill((30,30,30))
        if self.playlist[self.current_song].art != False:
            screen.blit(self.playlist[self.current_song].art, (0,0))
        
        screen.fill((50, 50, 50), p.Rect((5, 210), (190, 30)))
        screen.fill((150, 150, 150), p.Rect((6, 211), (self.playlist[self.current_song].seconds_played/self.playlist[self.current_song].track_length * 188, 28)))

        time_text = f"{round(self.playlist[self.current_song].seconds_played, 1)} / {round(self.playlist[self.current_song].track_length, 1)}"
        screen.blit(font.render(time_text, True, (255,255,255)), (195 - font.size(time_text)[0],245))

        name_text = self.playlist[self.current_song].track_name
        name_font = p.font.SysFont("arial", 10)
        i = 10
        while 5 + name_font.size(name_text)[0] > 195 - font.size(time_text)[0]:
            name_font = p.font.SysFont("arial", i)
            i -= 1
        
        screen.blit(name_font.render(name_text, True, (255,255,255)), (5,245))

        #buttons
        if self.playlist[self.current_song].playing:
            screen.blit(self.textures.icons["pause"], (205,5))
        else:
            screen.blit(self.textures.icons["play"], (205,5))
        screen.blit(self.textures.icons["back"], (205,40))
        screen.blit(self.textures.icons["forward"], (205,75))
        if self.shuffle:
            screen.blit(self.textures.icons["shuffle_on"], (205,110))
        else:
            screen.blit(self.textures.icons["shuffle"], (205,110))

        p.display.flip()

    def play_song(self):
        self.playlist[self.current_song].channel.play(self.playlist[self.current_song].sound)
        self.playlist[self.current_song].playing = True

    def next_song(self):
        if not self.shuffle:
            if self.current_song + 1 < len(self.playlist):
                self.current_song += 1
                self.playlist[self.current_song-1].playing = False
                self.playlist[self.current_song-1].channel.stop()
                self.playlist[self.current_song-1].seconds_played = 0
            else:
                self.playlist[len(self.playlist)-1].playing = False
                self.playlist[len(self.playlist)-1].channel.stop()
                self.playlist[len(self.playlist)-1].seconds_played = 0
                self.current_song = 0
        else:
            self.playlist[self.current_song].playing = False
            self.playlist[self.current_song].channel.stop()
            self.playlist[self.current_song].seconds_played = 0
            self.current_song = randint(0, len(self.playlist)-1)
        self.play_song()

    def last_song(self):
        if self.current_song - 1 >= 0:
            self.current_song -= 1
            self.playlist[self.current_song+1].playing = False
            self.playlist[self.current_song+1].channel.stop()
            self.playlist[self.current_song+1].seconds_played = 0
        else:
            self.playlist[0].playing = False
            self.playlist[0].channel.stop()
            self.playlist[0].seconds_played = 0
            self.current_song = len(self.playlist) - 1
        self.play_song()

    def pause_song(self):
        if self.playlist[self.current_song].playing == True:
            self.playlist[self.current_song].channel.pause()
            self.playlist[self.current_song].playing = False
        else:
            self.playlist[self.current_song].channel.unpause()
            self.playlist[self.current_song].playing = True
    
    def add_time(self):
        if self.playlist[self.current_song].track_length > self.playlist[self.current_song].seconds_played:
            dt = clock.tick(60) / 1000
            if self.playlist[self.current_song].playing:
                self.playlist[self.current_song].seconds_played += dt
        else:
            self.next_song()

    def handle_mouse_inputs(self):
        pos = p.mouse.get_pos()
        if (pos[0] > 205 and pos[0] < 235):
            if (pos[1] > 5 and pos[1] < 35):
                self.pause_song()
                blip.play()
            elif (pos[1] > 40 and pos[1] < 70):
                self.last_song()
                blip.play()
            elif (pos[1] > 75 and pos[1] < 105):
                self.next_song()
                blip.play()
            elif (pos[1] > 110 and pos[1] < 140):
                self.shuffle = not self.shuffle
                blip.play()

main_player = Player()

running = True

clock = p.time.Clock()

while running:
    main_player.add_time()
    for ev in p.event.get():
        if ev.type == p.QUIT:
            running = False
        elif ev.type == p.MOUSEBUTTONDOWN:
            main_player.handle_mouse_inputs()
    main_player.render()
p.quit()
quit()

