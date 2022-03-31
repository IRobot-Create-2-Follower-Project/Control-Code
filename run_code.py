from  pycreate2 import Create2
import time

class Bot():
    def __init__(self, port):
        self.bot = Create2(port)
        # Start the Create 2
        self.bot.start()
        # Put the Create2 into 'safe' mode so we can drive it
        # This will still provide some protection
        self.bot.safe()

    def drive(self, bin, distance):
    # Get Bin
    # Use example values for now
    # Prompt User for "Getting Data"
    # Remember when the robot is facing forward:
    # Motor.drive_direct(RIGHT MOTOR SPEED, LEFT MOTOR SPEED)
        if(bin == 5):                           # Check if object centered
            if(distance > 5):                   # Distance in meters from object
                self.bot.drive_direct(200, 200)      # Drive straight towards object quickly
            elif(distance > 1):
                self.bot.drive_direct(100, 100)      # Drive straight towards object
            elif(distance < 1):
                self.bot.drive_direct(-100, -100)    # Drive away from object
            else:                               # Distance is equal to 1 or not found
                time.sleep(0.1)                 # Wait to see if object moves or is stationary
        elif(bin < 5):                          # Object is to the left
            if(bin < 2):
                self.bot.drive_direct(100, 50)       # Turn hard left
            elif (bin <= 4 ):
                self.bot.drive_direct(100, 75)       # Turn slight left
        elif(bin > 5):                          # Object is to the right
            if(bin > 8):
                self.bot.drive_direct(50, 100)       # Turn hard right
            elif (bin >= 6):
                self.bot.drive_direct(75, 100)       # Turn Slight Right
        else:                                   # Object not found, Bin value not in 0-10 range
            self.bot.drive_direct(50, -50)           # Turn in place until object detected

        return
    # Stop the bot
    # bot.drive_stop()

    # Close the connection
    # bot.close()
