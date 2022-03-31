from  pycreate2 import Create2
import time

# Create a Create2.
port = "COM3"  # where is your serial port?
bot = Create2(port)

# Start the Create 2
bot.start()

# Put the Create2 into 'safe' mode so we can drive it
# This will still provide some protection
bot.safe()

# random MIDI songs I found on the internet
# they cannot be more than 16 midi notes or really 32 bytes arranged
# as [(note, duration), ...]
song0 = [50, 16, 50, 16, 62, 16, 0, 16, 57, 16, 0, 32, 56, 16, 0, 16, 55, 16, 0, 16, 53, 32, 50, 16, 53, 16, 55, 16]  #Megalovania

song_num0 = 0
bot.createSong(song_num0, song0)

song1 = [48, 16, 48, 16, 62, 16, 0, 16, 57, 16, 0, 32, 56, 16, 0, 16, 55, 16, 0, 16, 53, 32, 50, 16, 53, 16, 55, 16]  #Megalovania

song_num1 = 1
bot.createSong(song_num1, song1)

song2 = [47, 16, 47, 16, 62, 16, 0, 16, 57, 16, 0, 32, 56, 16, 0, 16, 55, 16, 0, 16, 53, 32, 50, 16, 53, 16, 55, 16]  #Megalovania

song_num2 = 2
bot.createSong(song_num2, song2)

song3 = [46, 16, 46, 16, 62, 16, 0, 16, 57, 16, 0, 32, 56, 16, 0, 16, 55, 16, 0, 16, 53, 32, 50, 16, 53, 16, 55, 16]  #Megalovania

# song number can be 0-3
song_num3 = 3
bot.createSong(song_num3, song3)

bot.playSong(song_num0)
time.sleep(4.05)
bot.playSong(song_num1)
time.sleep(4.05)
bot.playSong(song_num2)
time.sleep(4.05)
bot.playSong(song_num3)
time.sleep(4.05)
bot.playSong(song_num0)
time.sleep(4.05)
bot.playSong(song_num1)
time.sleep(4.05)
bot.playSong(song_num2)
time.sleep(4.05)
bot.playSong(song_num3)
time.sleep(4.05)

# Stop the bot
bot.drive_stop()

# Close the connection
bot.close()
