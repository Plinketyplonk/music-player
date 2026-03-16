import pygame as p
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import io
import os
import random
import playlist_manager

# enjoy my sparcely commented code lol

p.init()

p.display.set_caption("MP3 Player")
p.display.set_icon(p.image.load("icons/play.png"))

screen = p.display.set_mode((240,280))

font = p.font.SysFont("arial", 10)

blip = p.mixer.Sound("blip.wav")

screen.blit(font.render("Loading...", True, (255,255,255)), (100, 100))
p.display.flip()

class Song:
    def __init__(self, file):
        # not gonna lie, this entire artwork grabbing function is written by AI, I still have no real grasp on how to read mp3 metadata (I wrote the track info bit and the resize too at least tho lol)
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
        
        self.filename = file
        self.art, self.track_length, self.track_name = load_any_artwork(file)
        self.seconds_played = 0
        self.playing = False

class Player:
    class Images:
        def __init__(self):
            self.icons = {
                "play" : p.image.load("icons/play.png").convert_alpha(),
                "pause" : p.image.load("icons/pause.png").convert_alpha(),
                "back" : p.image.load("icons/back.png").convert_alpha(),
                "forward" : p.image.load("icons/skip.png").convert_alpha(),
                "shuffle" : p.image.load("icons/shuffle.png").convert_alpha(),
                "shuffle_on" : p.image.load("icons/shuffle_on.png").convert_alpha(),
                "theme" : p.image.load("icons/theme.png").convert_alpha(),
                "playlist" : p.image.load("icons/playlist.png").convert_alpha(),
                "delete" : p.image.load("icons/delete.png").convert_alpha(),
                "add" : p.image.load("icons/add.png").convert_alpha()
            }

    def __init__(self):
        self.playlist = 0 # start on playlist "0"
        self.queue, self.playlist_name = self.load_playlist()
        self.current_song = 0
        self.textures = Player.Images()
        self.shuffle = False
        self.volume = 1
        self.colour_Schemes = [
            {#dark
            "bg" : (10, 10, 10),
            "text" : (255, 255, 255),
            "slider_in" : (50, 50, 50),
            "slider_out_ghost" : (100, 100, 100),
            "slider_out" : (150, 150, 150),
            "slider_circle" : (150, 150, 150)
            },
            {#light
            "bg" : (255, 255, 255),
            "text" : (10, 10, 10),
            "slider_in" : (50, 50, 50),
            "slider_out_ghost" : (100, 100, 100),
            "slider_out" : (150, 150, 150),
            "slider_circle" : (150, 150, 150)
            },
            {#spotify ripoff
            "bg" : (10, 10, 10),
            "text" : (255, 255, 255),
            "slider_in" : (50, 50, 50),
            "slider_out_ghost" : (100, 100, 100),
            "slider_out" : (20, 100, 20),
            "slider_circle" : (200, 200, 200)
            },
            {#red
            "bg" : (50, 10, 10),
            "text" : (230, 230, 230),
            "slider_in" : (60, 30, 30),
            "slider_out_ghost" : (100, 100, 100),
            "slider_out" : (120, 20, 20),
            "slider_circle" : (200, 200, 200)
            },
            {#green
            "bg" : (10, 30, 10),
            "text" : (230, 230, 230),
            "slider_in" : (30, 60, 30),
            "slider_out_ghost" : (100, 100, 100),
            "slider_out" : (20, 100, 20),
            "slider_circle" : (200, 200, 200)
            },
            {#blue
            "bg" : (10, 10, 50),
            "text" : (230, 230, 230),
            "slider_in" : (30, 30, 60),
            "slider_out_ghost" : (100, 100, 100),
            "slider_out" : (20, 20, 180),
            "slider_circle" : (200, 200, 200)
            }
        ]
        self.colour_scheme = 0 # 0 is dark
        self.render_mode = "Player"
        self.play_song()
        self.pause_song()
    
    def load_playlist(self, current_playlist = 0):
        # we do not talk about how bad the variable naming is
        print("Loading Playlist", end="")
        playlist = playlist_manager.playlists[current_playlist]
        song_playlist = []

        dots = 10
        if len(playlist) < dots:
            dots = len(playlist)

        songs_between_dots = len(playlist) // dots

        for i in range(1, len(playlist)): # indexed from 1 because 0 is the playlist name
            song_playlist.append(Song(playlist[i]))
            if i % songs_between_dots == 0:
                print(".", end="")
        playlist_name = playlist[0]
        print()
        return song_playlist, playlist_name

    def render(self):
        pos = p.mouse.get_pos()
        screen.fill(self.colour_Schemes[self.colour_scheme]["bg"])

        #buttons
        if self.queue[self.current_song].playing:
            screen.blit(self.textures.icons["pause"], (205,5))
        else:
            screen.blit(self.textures.icons["play"], (205,5))
        screen.blit(self.textures.icons["back"], (205,40))
        screen.blit(self.textures.icons["forward"], (205,75))
        if self.shuffle:
            screen.blit(self.textures.icons["shuffle_on"], (205,110))
        else:
            screen.blit(self.textures.icons["shuffle"], (205,110))
        screen.blit(self.textures.icons["theme"], (205,145))
        screen.blit(self.textures.icons["playlist"], (205,180))

        if self.render_mode == "Player":
            if self.queue[self.current_song].art != False:
                screen.blit(self.queue[self.current_song].art, (0,0))
            
            #time bar
            screen.fill(self.colour_Schemes[self.colour_scheme]["slider_in"], p.Rect((5, 210), (190, 30)))
            if (pos[0] > 6 and pos[0] < 194) and (pos[1] > 210 and pos[1] < 240):
                screen.fill(self.colour_Schemes[self.colour_scheme]["slider_out_ghost"], p.Rect((6, 211), (p.mouse.get_pos()[0]-6, 28)))
            screen.fill(self.colour_Schemes[self.colour_scheme]["slider_out"], p.Rect((6, 211), (self.queue[self.current_song].seconds_played/self.queue[self.current_song].track_length * 188, 28)))

            time_text = f"{round(self.queue[self.current_song].seconds_played, 1)} / {round(self.queue[self.current_song].track_length, 1)}"
            screen.blit(font.render(time_text, True, self.colour_Schemes[self.colour_scheme]["text"]), (195 - font.size(time_text)[0],245))

            name_text = self.queue[self.current_song].track_name
            name_font = p.font.SysFont("arial", 10)
            i = 10
            while 5 + name_font.size(name_text)[0] > 195 - font.size(time_text)[0]:
                name_font = p.font.SysFont("arial", i)
                i -= 1
            
            screen.blit(name_font.render(name_text, True, self.colour_Schemes[self.colour_scheme]["text"]), (5,245))

            # volume slider
            screen.fill(self.colour_Schemes[self.colour_scheme]["slider_in"], p.Rect((5, 270), (190, 3)))
            if (pos[0] > 5 and pos[0] < 195) and (pos[1] > 267 and pos[1] < 274):
                screen.fill(self.colour_Schemes[self.colour_scheme]["slider_out_ghost"], p.Rect((5, 270), ((p.mouse.get_pos()[0]-5), 3)))
            screen.fill(self.colour_Schemes[self.colour_scheme]["slider_out"], p.Rect((5, 270), (5 + 190 * self.volume, 3)))
            p.draw.circle(screen, self.colour_Schemes[self.colour_scheme]["slider_circle"], (5 + 190 * self.volume, 271), 5)
        else:
            for i in range(0, len(playlist_manager.playlists[self.playlist])):
                text = playlist_manager.playlists[self.playlist][i]
                if len(text) > 33:
                    text = playlist_manager.playlists[self.playlist][i][0:30] + "..."
                screen.blit(font.render(text, True, self.colour_Schemes[self.colour_scheme]["text"]), (10, 10 + i * 20))
                if i != 0: # cant delete playlist title lol
                    screen.blit(self.textures.icons["delete"], (175,10 + i * 20))

            screen.blit(self.textures.icons["add"], (205,245))

        p.display.flip()

    def play_song(self):
        p.mixer.music.load(self.queue[self.current_song].filename)
        p.mixer.music.play(0,0,0)
        self.queue[self.current_song].playing = True

    def next_song(self):
        if self.current_song + 1 < len(self.queue):
            self.current_song += 1
            self.queue[self.current_song-1].playing = False
            self.queue[self.current_song-1].seconds_played = 0
        else:
            self.queue[len(self.queue)-1].playing = False
            self.queue[len(self.queue)-1].seconds_played = 0
            self.current_song = 0
        self.play_song()

    def last_song(self):
        if self.queue[self.current_song].seconds_played < 1: # for actually going back
            if self.current_song - 1 >= 0:
                self.current_song -= 1
                self.queue[self.current_song+1].playing = False
                self.queue[self.current_song+1].seconds_played = 0
            else: # restarts song
                self.queue[0].playing = False
                self.queue[0].seconds_played = 0
                self.current_song = len(self.queue) - 1
            self.play_song()
        else:
            self.queue[self.current_song].seconds_played = 0
            p.mixer.music.set_pos(0)

    def pause_song(self):
        if self.queue[self.current_song].playing == True:
            p.mixer.music.pause()
            self.queue[self.current_song].playing = False
        else:
            p.mixer.music.unpause()
            self.queue[self.current_song].playing = True
    
    def add_time(self):
        if self.queue[self.current_song].track_length > self.queue[self.current_song].seconds_played:
            dt = clock.tick(60) / 1000
            if self.queue[self.current_song].playing:
                self.queue[self.current_song].seconds_played += dt
        else:
            self.next_song()

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
        if self.shuffle:
            p.mixer.music.stop()
            self.queue[self.current_song].playing = False
            self.queue[self.current_song].seconds_played = 0
            random.shuffle(self.queue)
            self.queue[self.current_song].playing = True
        else:
            self.queue, temp = self.load_playlist()
            self.queue[self.current_song].playing = True
        self.play_song()

    def change_theme(self):
        self.colour_scheme += 1
        if self.colour_scheme == len(self.colour_Schemes):
            self.colour_scheme = 0

    def playlist_mode(self):
        if self.render_mode == "Player":
            self.render_mode = "Playlist"
        else:
            self.render_mode = "Player"

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
                self.toggle_shuffle()
                blip.play()
            elif (pos[1] > 145 and pos[1] < 175):
                self.change_theme()
                blip.play()
            elif (pos[1] > 180 and pos[1] < 210):
                self.playlist_mode()
                blip.play()
        
        if self.render_mode == "Playlist":
            for i in range(1, len(playlist_manager.playlists[self.playlist])):
                if (pos[0] > 175 and pos[0] < 185) and (pos[1] > 10 + i * 20 and pos[1] < 20 + i * 20):
                    blip.play()
            if (pos[0] > 205 and pos[0] < 235) and (pos[1] > 245 and pos[1] < 275):
                playlist_manager.add_song(self.playlist)
                blip.play()
    
    def handle_sliders(self):
        if p.mouse.get_pressed()[0] and self.render_mode == "Player":
            pos = p.mouse.get_pos()
            if (pos[0] > 5 and pos[0] < 195) and (pos[1] > 267 and pos[1] < 274): #volume
                self.volume = (p.mouse.get_pos()[0]-5)/190
                p.mixer.music.set_volume((self.volume**2)/2)
                blip.set_volume((self.volume**2))

            elif (pos[0] > 5 and pos[0] < 195) and (pos[1] > 210 and pos[1] < 240): #time
                self.queue[self.current_song].seconds_played = self.queue[self.current_song].track_length * ((p.mouse.get_pos()[0]-5)/190)
                p.mixer.music.set_pos(self.queue[self.current_song].seconds_played)

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
    main_player.handle_sliders()
    main_player.render()
p.quit()
quit()
