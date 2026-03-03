## **Dependancies:**
- Python (obvs)
- Pygame module installed (use pip)
- Mutagen module installed (use pip)
- MP3 files to play (if there's no metadata attached it WILL crash out lol)

## **How to create a playlist:**
  1. Find line 72 in music.py
  2. In the square brackets, for every song in the playlist do the following:
  3. Put "Song()" with the MP3s filepath as the argument to pass
  4. If it's not the last song in the playlist, add a comma after "Song()"
     e.g.
72     self.playlist = [Song("D:/My Music/Evanescence - Fallen/01 - Going Under.mp3"), Song("D:/My Music/Evanescence - Fallen/02 - Bring Me To Life.mp3")] # for every song in the playlist, put Song({file location})



## **Instructions for UI:**

### **First button (from top-right):**
  "Pause/Unpause"
  - Toggles playback, simples

### **Second button:**
  "Back"
  - If within the first 3 seconds of the song, it will play the previous song in the queue
  - If after the first 3 seconds, it restarts the song
    
### **Third button:**
  "Skip"
  - Skips to the next song in the queue

### **Fourth button:**
  "Shuffle"
  - If black it means shuffle is turned off, and the queue will be in the same order as the playlist
  - If white it means the queue has been shuffled

  - When turning shuffle on, the current song will jump to a random one, and the queue is shuffled randomly

### **Fifth button:**
  "Theme"
  - Switches through avaliable colour schemes

### **Time slider:**
  - The big bar under the MP3 artwork
  - Clicking anywhere on the bar will change the current time of the song to match where you clicked
  - I.e. allows you to skip to different parts of the song
  - Can hold down and slide around (though sounds wierd and isn't that useful)

**Volume slider:**
  - The thin bar with a circle under the song name and track time
  - Clicking anywhere on here changes the volume respectively
  - Can hold down and slide around
