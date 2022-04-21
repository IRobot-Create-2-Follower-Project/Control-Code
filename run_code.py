from  pycreate2 import Create2
import time

max_speed = 500
min_speed = 150
kp = 200
set_distance = 1
bin_max = 6
bin_min = 4

class Bot():
    def __init__(self, port):
        self.bot = Create2(port)
        # Start the Create 2
        self.bot.start()
        # Put the Create2 into 'safe' mode so we can drive it
        # This will still provide some protection
        self.bot.safe()

    def drive(self, bin, distance):
        #If can't see person, turn in place
        if bin == -1:
            self.bot.drive_direct(100, -100)
        elif bin == 11:
            self.bot.drive_direct(-100, 100)
        else:

            if distance - set_distance < 0:
                bin_max = 7
                bin_min = 3
            else:
                bin_max = 6
                bin_min = 4

            if(bin < bin_max and bin > bin_min):
                if distance < set_distance + 0.2 and distance > set_distance - 0.2:
                    self.bot.drive_direct(0, 0)  # Wait to see if object moves or is stationary
                else:
                    speed = int(kp*(distance - set_distance))
                    if speed > max_speed:
                        if distance - set_distance < 0:
                            speed = -max_speed
                        else:
                            speed = max_speed
                    if speed < min_speed:
                        if distance - set_distance < 0:
                            speed = -min_speed
                        else:
                            speed = min_speed
                    self.bot.drive_direct(speed, speed)
            #turn
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
