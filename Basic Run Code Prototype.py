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
 
# Get Bin 
# Use example values for now
# Prompt User for "Getting Data"
Getting_Data = 1
Distance = 3
Bin = 5

# Remember when the robot is facing forward:
# Motor.drive_direct(RIGHT MOTOR SPEED, LEFT MOTOR SPEED)

while (Getting_Data == 1):
    if(Bin == 5):                           # Check if object centered
        if(Distance > 5):                   # Distance in meters from object
            bot.drive_direct(200, 200)      # Drive straight towards object quickly
        elif(Distance > 1):
            bot.drive_direct(100, 100)      # Drive straight towards object
        elif(Distance < 1):
            bot.drive_direct(-100, -100)    # Drive away from object
        else:                               # Distance is equal to 1 or not found
            time.sleep(0.1)                 # Wait to see if object moves or is stationary
    elif(Bin < 5):                          # Object is to the left
        if(Bin < 2):                          
            bot.drive_direct(100, 50)       # Turn hard left
        elif (Bin <= 4 ):  
            bot.drive_direct(100, 75)       # Turn slight left
        else:
            break
    elif(Bin > 5):                          # Object is to the right
        if(Bin > 8):                          
            bot.drive_direct(50, 100)       # Turn hard right
        elif (Bin >= 6):  
            bot.drive_direct(75, 100)       # Turn Slight Right
        else:
            break
    else:                                   # Object not found, Bin value not in 0-10 range
        bot.drive_direct(50, -50)           # Turn in place until object detected

# Stop the bot
bot.drive_stop()

# Close the connection
bot.close()
